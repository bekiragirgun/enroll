"""
Chroot Terminal Yöneticisi
CT 991 (ogrenci-vm) üzerindeki chroot ortamlarını yönetir
"""

import subprocess
import os
import time
import threading
from pathlib import Path
import logging
import atexit

log = logging.getLogger("chroot_terminal")

# ── SSH Kuyruk Sistemi ─────────────────────────────────────────
# Eş zamanlı SSH bağlantı sayısını sınırla (MaxSessions/MaxStartups aşımını önler)
_ssh_semaphore = threading.Semaphore(10)  # Aynı anda max 10 SSH bağlantısı
_sync_lock = threading.Lock()
_last_sync_time = 0
_SYNC_INTERVAL = 60  # Sync script'i en fazla 60 saniyede bir gönder

# Chroot listesi cache (her seferinde SSH ile sorgulamayı önler)
_chroot_cache = set()
_chroot_cache_time = 0
_CHROOT_CACHE_TTL = 30  # 30 saniye cache

# ── SSH Connection Pool (ControlMaster) ───────────────────────
# Tek master bağlantı üzerinden tüm SSH komutları multiplexing ile gider
_pool_lock = threading.Lock()
_pool_process = None   # Master SSH süreci
_pool_socket = None    # ControlPath socket yolu
_pool_ready = False    # Pool hazır mı?

from dotenv import load_dotenv
load_dotenv()

# CT 991 (ogrenci-vm) bilgileri
CHROOT_HOST = os.environ.get("CHROOT_HOST", "192.168.111.51")  # CT 991 IP adresi
CHROOT_SSH_PORT = int(os.environ.get("CHROOT_SSH_PORT", "22"))            # Chroot içindeki SSH portu (V14 Default: 22)
CHROOT_REAL_SSH_PORT = int(os.environ.get("CHROOT_REAL_SSH_PORT", "22"))       # CT 991 ana sistem SSH portu (V14 Default: 22)
CHROOT_USER = os.environ.get("CHROOT_USER", "root")            # SSH kullanıcı adı (V15 Default: root)
CHROOT_PASS = os.environ.get("CHROOT_PASS", "")                # SSH şifresi (Opsiyonel, sshpass gerektirir)

CHROOT_MANAGE_SCRIPT = "/root/enroll/chroot_yonetici.py" # Varsayılan, ayarlari_yukle ile güncellenir
PYTHON_PATH = "python3" # PCT 991'deki python yolu (Venv yerine sistem python kullanıyoruz)
CHROOT_BASE = "/home/chroot"


def _slugify(text):
    """Kullanıcı adını Linux dostu hale getir (küçük harf, rakam ve alt çizgi)."""
    import re
    import unicodedata
    if not text: return ""
    text = str(text).strip()
    # Sayısal ise veya rakamla başlıyorsa 'u' öneki ekle (Linux için daha güvenli)
    if text.isdigit():
        text = f"u{text}"
    
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '_', text)
    
    # Hala rakamla başlıyorsa (slugify sonrası) u ekle
    if text and text[0].isdigit():
        text = f"u{text}"
    return text


def _is_local(host):
    """Host yerel mi kontrol et (Eski hostname/IP'leri de kapsar - V15.1)."""
    if host in ["localhost", "127.0.0.1", "::1"]:
        return True
    
    # Kendi hostname'i ile karşılaştır
    try:
        if Path("/etc/hostname").exists():
            if host == Path("/etc/hostname").read_text().strip():
                return True
    except: pass

    # Sistemin tüm yerel IP'lerini kontrol et (Burası en kritik kısım)
    try:
        import socket
        me = socket.gethostname()
        local_ips = socket.gethostbyname_ex(me)[2]
        if host in local_ips:
            return True
        
        # Ekstra: aktif interface IP'sini al
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            active_ip = s.getsockname()[0]
            if host == active_ip:
                return True
        finally:
            s.close()
    except: pass
    
    return False

def _ssh_pool_baslat() -> bool:
    """SSH ControlMaster bağlantısını arka planda başlat (yoksa).

    Başarılı olursa sonraki tüm _ct991_exec çağrıları bu socket üzerinden
    ~5ms latency ile çalışır (handshake yok).
    """
    global _pool_process, _pool_socket, _pool_ready

    if _is_local(CHROOT_HOST):
        return False  # Yerel modda pool'a gerek yok

    with _pool_lock:
        # Zaten çalışıyorsa socket var mı kontrol et
        if _pool_ready and _pool_socket and Path(_pool_socket).exists():
            return True

        socket_path = f"/tmp/ssh_pool_{CHROOT_HOST}_{CHROOT_REAL_SSH_PORT}_{CHROOT_USER}"
        _pool_socket = socket_path

        # Önceki socket temizle
        try:
            if Path(socket_path).exists():
                Path(socket_path).unlink()
        except Exception:
            pass

        cmd = [
            "ssh",
            "-o", "ConnectTimeout=15",
            "-o", "StrictHostKeyChecking=no",
            "-o", "BatchMode=yes" if not CHROOT_PASS else "BatchMode=no",
            "-o", "ControlMaster=yes",
            "-o", f"ControlPath={socket_path}",
            "-o", "ControlPersist=120",  # 120 saniye boşta kalırsa kapat
            "-p", str(CHROOT_REAL_SSH_PORT),
            "-N",  # Komut çalıştırma, sadece bağlantı tut
            f"{CHROOT_USER}@{CHROOT_HOST}",
        ]

        if CHROOT_PASS:
            import shutil
            if shutil.which("sshpass"):
                cmd = ["sshpass", "-p", CHROOT_PASS] + cmd

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            _pool_process = proc

            # Socket oluşana kadar bekle (max 5 saniye)
            for _ in range(50):
                if Path(socket_path).exists():
                    _pool_ready = True
                    log.info(f"✅ SSH pool hazır: {socket_path}")
                    return True
                time.sleep(0.1)

            log.warning("SSH pool socket oluşmadı, fallback moduna geçiliyor")
            _pool_ready = False
            return False

        except Exception as e:
            log.warning(f"SSH pool başlatılamadı: {e}")
            _pool_ready = False
            return False


def _ssh_pool_kapat():
    """Uygulama kapanırken pool bağlantısını temizle."""
    global _pool_process, _pool_ready
    _pool_ready = False
    if _pool_process:
        try:
            _pool_process.terminate()
        except Exception:
            pass
    if _pool_socket:
        try:
            if Path(_pool_socket).exists():
                Path(_pool_socket).unlink()
        except Exception:
            pass


atexit.register(_ssh_pool_kapat)


def _ssh_pool_reset():
    """Stale pool bağlantısını temizle — sonraki çağrı yeniden oluşturur."""
    global _pool_ready, _pool_process
    _pool_ready = False
    if _pool_process:
        try:
            _pool_process.terminate()
        except Exception:
            pass
        _pool_process = None
    if _pool_socket:
        try:
            Path(_pool_socket).unlink(missing_ok=True)
        except Exception:
            pass
    log.info("🔄 SSH pool sıfırlandı, yeniden bağlanılacak")


def _ct991_exec(command: list, retries: int = 2) -> subprocess.CompletedProcess:
    """CT 991 üzerinde komut çalıştır (Local veya SSH üzerinden).

    SSH bağlantıları semaphore ile sınırlandırılır (max 3 eşzamanlı).
    Başarısız bağlantılarda retry + backoff uygulanır.
    """
    if _is_local(CHROOT_HOST):
        log.debug(f"Executing locally: {' '.join(command)}")
        return subprocess.run(command, capture_output=True, text=True)

    final_command = command
    if CHROOT_USER != "root":
        # Sudo ile komutu çalıştır, -S ile şifreyi stdin'den almasını sağla
        if CHROOT_PASS:
            final_command = ["sudo", "-S"] + command
        else:
            final_command = ["sudo"] + command

    # Pool hazırsa ControlPath ile hızlı bağlan, değilse pool'u başlat
    use_pool = _ssh_pool_baslat()
    control_path = _pool_socket if use_pool else "none"

    ssh_cmd = [
        "ssh", "-o", "ConnectTimeout=10",
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes" if not CHROOT_PASS else "BatchMode=no",
        "-o", f"ControlPath={control_path}",
        "-o", "ControlMaster=no",  # Master zaten _pool_process, biz slave olarak bağlanıyoruz
        "-p", str(CHROOT_REAL_SSH_PORT),
        f"{CHROOT_USER}@{CHROOT_HOST}"
    ]

    if CHROOT_PASS and not use_pool:
        # Pool sshpass kullanıyorsa slave bağlantılarda tekrar gerekmez
        import shutil
        if not shutil.which("sshpass"):
            log.error("sshpass paketi yüklü değil!")
            return subprocess.CompletedProcess(ssh_cmd, 1, stderr="sshpass not found")
        ssh_cmd = ["sshpass", "-p", CHROOT_PASS] + ssh_cmd

    ssh_cmd += final_command

    for attempt in range(retries + 1):
        _ssh_semaphore.acquire()
        try:
            log.debug(f"SSH exec (attempt {attempt+1}): {' '.join(command)}")
            # Şifre gerekiyorsa stdin'e gönder (sudo -S için)
            input_data = f"{CHROOT_PASS}\n" if (CHROOT_USER != "root" and CHROOT_PASS) else None
            
            result = subprocess.run(
                ssh_cmd, 
                capture_output=True, 
                text=True, 
                input=input_data, 
                check=False
            )

            if result.returncode == 0:
                return result

            # SSH bağlantı hatası (exit 255) → pool'u sıfırla ve retry
            if result.returncode == 255 and attempt < retries:
                _ssh_pool_reset()
                wait = (attempt + 1) * 2
                log.warning(f"SSH bağlantı hatası, pool sıfırlandı, {wait}s sonra tekrar denenecek ({attempt+1}/{retries})")
                time.sleep(wait)
                # Yeni pool ile ssh_cmd'yi yeniden oluştur
                use_pool = _ssh_pool_baslat()
                control_path = _pool_socket if use_pool else "none"
                ssh_cmd = [
                    "ssh", "-o", "ConnectTimeout=10",
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "BatchMode=yes" if not CHROOT_PASS else "BatchMode=no",
                    "-o", f"ControlPath={control_path}",
                    "-o", "ControlMaster=no",
                    "-p", str(CHROOT_REAL_SSH_PORT),
                    f"{CHROOT_USER}@{CHROOT_HOST}"
                ]
                if CHROOT_PASS and not use_pool:
                    import shutil
                    if shutil.which("sshpass"):
                        ssh_cmd = ["sshpass", "-p", CHROOT_PASS] + ssh_cmd
                ssh_cmd += final_command
                continue

            if result.returncode != 0:
                log.error(f"Remote command failed: {' '.join(command)}")
                if result.stderr:
                    log.error(f"Stderr: {result.stderr.strip()[:200]}")
            return result
        except subprocess.TimeoutExpired:
            log.error(f"SSH zaman aşımı: {' '.join(command)}")
            _ssh_pool_reset()
            if attempt < retries:
                time.sleep((attempt + 1) * 2)
                continue
            return subprocess.CompletedProcess(ssh_cmd, 1, stderr="Timeout")
        finally:
            _ssh_semaphore.release()

    return subprocess.CompletedProcess(ssh_cmd, 1, stderr="Max retries exceeded")


def sync_manager_script():
    """Local chroot_yonetici.py dosyasını PCT 991'e senkronize et.

    Son senkronizasyondan bu yana _SYNC_INTERVAL saniye geçmediyse atlar.
    """
    global _last_sync_time
    with _sync_lock:
        now = time.time()
        if now - _last_sync_time < _SYNC_INTERVAL:
            return True  # Son sync yeterince yakın, atla
        _last_sync_time = now
    try:
        local_path = Path(__file__).parent / "chroot_yonetici.py"
        if not local_path.exists():
            log.error(f"Senkronizasyon hatası: {local_path} bulunamadı")
            return False
            
        if _is_local(CHROOT_HOST):
            # Yerel modda dosya zaten burada, sadece erişimi kontrol et
            if not Path(CHROOT_MANAGE_SCRIPT).exists():
                # Eğer CHROOT_MANAGE_SCRIPT farklı bir yerse kopyala
                if str(local_path) != CHROOT_MANAGE_SCRIPT:
                    import shutil
                    os.makedirs(os.path.dirname(CHROOT_MANAGE_SCRIPT), exist_ok=True)
                    shutil.copy2(local_path, CHROOT_MANAGE_SCRIPT)
                    os.chmod(CHROOT_MANAGE_SCRIPT, 0o755)
            return True

        content = local_path.read_text()
        
        # Dizin varlığı ve pipe için komut
        target_dir = os.path.dirname(CHROOT_MANAGE_SCRIPT)
        remote_cmd = f"mkdir -p {target_dir} && cat > {CHROOT_MANAGE_SCRIPT} && chmod +x {CHROOT_MANAGE_SCRIPT}"
        if CHROOT_USER != "root":
            remote_cmd = f"sudo mkdir -p {target_dir} && sudo tee {CHROOT_MANAGE_SCRIPT} > /dev/null && sudo chmod +x {CHROOT_MANAGE_SCRIPT}"

        # Dizin varlığından emin ol ve dosyayı SSH üzerinden pipe ile gönder
        ssh_cmd = [
            "ssh", "-o", "ConnectTimeout=5",
            "-o", "BatchMode=yes" if not CHROOT_PASS else "BatchMode=no",
            "-o", "ControlPath=none",
            "-p", str(CHROOT_REAL_SSH_PORT),
            f"{CHROOT_USER}@{CHROOT_HOST}",
            remote_cmd
        ]

        # Şifre varsa sshpass kullan
        if CHROOT_PASS:
            ssh_cmd = ["sshpass", "-p", CHROOT_PASS] + ssh_cmd
        
        subprocess.run(ssh_cmd, input=content, text=True, check=True)
        log.info(f"✅ chroot_yonetici.py {CHROOT_HOST} üzerine senkronize edildi.")
        
        # PTY Onarımını tetikle (V14)
        chroot_onar()
        
        return True
    except Exception as e:
        log.error(f"Senkronizasyon hatası: {e}")
        return False


def chroot_onar() -> bool:
    """CT 991 üzerinde PTY onarımını tetikle."""
    log.info("🛠️ CT 991 üzerinde PTY onarımı başlatılıyor...")
    result = _ct991_exec([PYTHON_PATH, CHROOT_MANAGE_SCRIPT, "repair"])
    if result.returncode == 0:
        log.info("✅ PTY onarımı başarılı.")
        return True
    else:
        log.error(f"❌ PTY onarımı başarısız: {result.stderr}")
        return False


def chroot_persist() -> bool:
    """CT 991 üzerinde onarımı kalıcı yap (Service kur)."""
    log.info("📡 CT 991 üzerinde kalıcı onarım servisi kuruluyor...")
    result = _ct991_exec([PYTHON_PATH, CHROOT_MANAGE_SCRIPT, "persist"])
    if result.returncode == 0:
        log.info("✅ Kalıcı onarım servisi kuruldu.")
        return True
    else:
        log.error(f"❌ Servis kurulum hatası: {result.stderr}")
        return False


def chroot_var_mi(username: str) -> bool:
    """Öğrenci chroot ortamı var mı? (Cache'li)"""
    global _chroot_cache, _chroot_cache_time

    sync_manager_script()  # Cache'li, gereksiz yere çağırmaz

    username = _slugify(username)

    # Cache'de varsa ve güncel ise hemen dön
    now = time.time()
    if username in _chroot_cache and (now - _chroot_cache_time) < _CHROOT_CACHE_TTL:
        return True

    # Cache süresi dolmuşsa veya kullanıcı bulunamadıysa listeyi güncelle
    if (now - _chroot_cache_time) >= _CHROOT_CACHE_TTL:
        result = _ct991_exec([PYTHON_PATH, CHROOT_MANAGE_SCRIPT, "list"])
        if result.returncode != 0:
            log.error(f"Chroot listesi alınamadı: {result.stderr}")
            return False

        output = result.stdout.strip()
        chroots = {line.strip().replace("- ", "").strip() for line in output.split('\n') if line.strip()}
        _chroot_cache = chroots
        _chroot_cache_time = now

    return username in _chroot_cache


def chroot_olustur(username: str, ad: str = "", soyad: str = "") -> bool:
    """Yeni chroot ortamı oluştur."""
    try:
        # Script güncel olduğundan emin ol
        sync_manager_script()
        
        username = _slugify(username)
        tam_ad = f"{ad} {soyad}".strip()
        log.info(f"Chroot oluşturuluyor: {username} ({tam_ad})")

        # CT 991 üzerinde yönetici script'ini çalıştır (Ad-Soyad ile)
        result = _ct991_exec(
            [PYTHON_PATH, CHROOT_MANAGE_SCRIPT, "create", username, tam_ad]
        )

        if result.returncode == 0:
            log.info(f"✅ Chroot oluşturuldu: {username}")
            _chroot_cache.add(username)  # Cache'e ekle
            # Mount işlemini tetikle
            _ct991_exec([PYTHON_PATH, CHROOT_MANAGE_SCRIPT, "mount", username])
            return True
        else:
            log.error(f"Chroot oluşturma hatası: {result.stderr}")
            return False

    except Exception as e:
        log.error(f"Chroot oluşturma hatası: {e}")
        return False


def chroot_olustur_batch(users: list) -> dict:
    """Birden fazla chroot ortamını tek SSH bağlantısında oluştur.

    Args:
        users: [{"username": str, "ad": str, "soyad": str}, ...] listesi

    Returns:
        {"username": True/False, ...} — her kullanıcı için sonuç
    """
    if not users:
        return {}

    sync_manager_script()

    # Slug'lı kullanıcı listesi
    prepared = []
    for u in users:
        slug = _slugify(u.get("username", ""))
        if not slug:
            continue
        tam_ad = f"{u.get('ad', '')} {u.get('soyad', '')}".strip()
        prepared.append((slug, tam_ad))

    if not prepared:
        return {}

    # Tek SSH bağlantısında bash loop — tüm create + mount komutları sırayla
    # JSON çıktısı ile sonuç takibi: "OK:username" veya "ERR:username"
    loop_lines = []
    sudo_prefix = "sudo -S " if CHROOT_USER != "root" else ""
    for slug, tam_ad in prepared:
        safe_ad = tam_ad.replace("'", "'\\''")
        sudo_prefix = "sudo -S " if CHROOT_USER != "root" else ""
        # Her komut grubunu parantez içine alıp stdin'i kontrollü yönlendir
        cmd = (
            f"{{ echo '{CHROOT_PASS}'; }} | {sudo_prefix}{PYTHON_PATH} {CHROOT_MANAGE_SCRIPT} create '{slug}' '{safe_ad}' && "
            f"{{ echo '{CHROOT_PASS}'; }} | {sudo_prefix}{PYTHON_PATH} {CHROOT_MANAGE_SCRIPT} mount '{slug}' && "
            f"echo 'OK:{slug}' || echo 'ERR:{slug}'"
        )
        loop_lines.append(cmd)

    # Hepsini tek ssh ile çalıştır (pool varsa socket üzerinden)
    batch_script = "\n".join(loop_lines)
    result = _ct991_exec(["bash", "-c", batch_script])

    sonuclar = {}
    for slug, _ in prepared:
        sonuclar[slug] = False  # Varsayılan: başarısız

    if result.returncode == 255:
        log.error("Batch chroot: SSH bağlantı hatası")
        return sonuclar

    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("OK:"):
            slug = line[3:]
            sonuclar[slug] = True
            _chroot_cache.add(slug)
            log.info(f"✅ Chroot oluşturuldu (batch): {slug}")
        elif line.startswith("ERR:"):
            slug = line[4:]
            sonuclar[slug] = False
            log.error(f"❌ Chroot oluşturulamadı (batch): {slug}")
            
    if not any(sonuclar.values()):
        log.error(f"Batch oluşturma başarısız görünüyor! stdout: {result.stdout}, stderr: {result.stderr}")

    return sonuclar


def chroot_sil(username: str) -> bool:
    """Öğrenci chroot ortamını sil (paket sonu / ders sonu temizliği)."""
    username = _slugify(username)
    log.info(f"Chroot siliniyor: {username}")
    result = _ct991_exec([PYTHON_PATH, CHROOT_MANAGE_SCRIPT, "delete", username])
    if result.returncode == 0:
        _chroot_cache.discard(username)
        log.info(f"✅ Chroot silindi: {username}")
        return True
    else:
        log.error(f"Chroot silme hatası ({username}): {result.stderr}")
        return False


def chroot_sil_batch(usernames: list) -> dict:
    """Birden fazla chroot'u tek SSH bağlantısında sil.

    Args:
        usernames: Silinecek kullanıcı adları listesi

    Returns:
        {"username": True/False, ...}
    """
    if not usernames:
        return {}

    slugged = [_slugify(u) for u in usernames if _slugify(u)]
    if not slugged:
        return {}

    # Tek SSH oturumunda hepsini sil
    loop_lines = []
    for slug in slugged:
        loop_lines.append(
            f"{PYTHON_PATH} {CHROOT_MANAGE_SCRIPT} delete '{slug}' "
            f"&& echo 'OK:{slug}' || echo 'ERR:{slug}'"
        )

    batch_script = "\n".join(loop_lines)
    result = _ct991_exec(["bash", "-c", batch_script])

    sonuclar = {slug: False for slug in slugged}

    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("OK:"):
            slug = line[3:]
            sonuclar[slug] = True
            _chroot_cache.discard(slug)
            log.info(f"✅ Chroot silindi (batch): {slug}")
        elif line.startswith("ERR:"):
            slug = line[4:]
            log.warning(f"⚠️ Chroot silinemedi (batch): {slug} (zaten yok olabilir)")

    return sonuclar


def chroot_ip_al(username: str) -> str:
    """SSH IP adresini döndür (CT 991 IP)."""
    return CHROOT_HOST


def chroot_durum(username: str) -> bool:
    """Chroot durumu kontrol et."""
    return chroot_var_mi(username)


def chroot_listesi() -> list:
    """Tüm chroot ortamlarını listele."""
    result = _ct991_exec([PYTHON_PATH, CHROOT_MANAGE_SCRIPT, "list"])

    if result.returncode != 0:
        log.error(f"Chroot listesi alınamadı: {result.stderr}")
        return []

    import re
    chroots = []
    for line in result.stdout.strip().split('\n'):
        username = line.strip().replace("- ", "").strip()
        # Yalnızca geçerli Unix kullanıcı adı formatındaki satırları kabul et
        # (harf/rakam/alt çizgi ile başlar, en az 2 karakter)
        if username and re.match(r'^[a-z0-9_][a-z0-9_]{1,}$', username):
            chroots.append({
                "username": username,
                "active": True
            })

    return chroots


def ssh_bilgi(username: str) -> dict:
    """SSH bağlantı bilgileri."""
    username = _slugify(username)
    return {
        "host": CHROOT_HOST,
        "port": CHROOT_SSH_PORT,
        "username": username,
        "password": username,  # Kullanıcı adı ile aynı
        "command": f"ssh -p {CHROOT_SSH_PORT} {username}@{CHROOT_HOST}"
    }


if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print(f"Chroot kontrol: {username}")
        print(f"Var mı: {chroot_var_mi(username)}")
        print(f"Durum: {chroot_durum(username)}")
        print(f"SSH: {ssh_bilgi(username)}")
        
        if username == "sync":
            sync_manager_script()
        elif username == "repair":
            chroot_onar()
        elif username == "persist":
            chroot_persist()
