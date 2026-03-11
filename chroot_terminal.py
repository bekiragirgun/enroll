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

# CT 991 (ogrenci-vm) bilgileri
CT_991_HOST = "192.168.111.51"  # CT 991 IP adresi
CT_991_SSH_PORT = 22            # Chroot içindeki SSH portu (V14 Default: 22)
CT_991_REAL_SSH_PORT = 22       # CT 991 ana sistem SSH portu (V14 Default: 22)
CT_991_USER = "root"            # SSH kullanıcı adı (V15 Default: root)
CT_991_PASS = ""                # SSH şifresi (Opsiyonel, sshpass gerektirir)
CHROOT_MANAGE_SCRIPT = "/root/enroll/chroot_yonetici.py" # PCT 991'deki tam yol
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

def _ct991_exec(command: list, retries: int = 2) -> subprocess.CompletedProcess:
    """CT 991 üzerinde komut çalıştır (Local veya SSH üzerinden).

    SSH bağlantıları semaphore ile sınırlandırılır (max 3 eşzamanlı).
    Başarısız bağlantılarda retry + backoff uygulanır.
    """
    if _is_local(CT_991_HOST):
        log.debug(f"Executing locally: {' '.join(command)}")
        return subprocess.run(command, capture_output=True, text=True)

    final_command = command
    if CT_991_USER != "root":
        final_command = ["sudo"] + command

    ssh_cmd = [
        "ssh", "-o", "ConnectTimeout=10",
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes" if not CT_991_PASS else "BatchMode=no",
        "-o", "ControlPath=none",
        "-p", str(CT_991_REAL_SSH_PORT),
        f"{CT_991_USER}@{CT_991_HOST}"
    ]

    if CT_991_PASS:
        import shutil
        if not shutil.which("sshpass"):
            log.error("sshpass paketi yüklü değil!")
            return subprocess.CompletedProcess(ssh_cmd, 1, stderr="sshpass not found")
        ssh_cmd = ["sshpass", "-p", CT_991_PASS] + ssh_cmd

    ssh_cmd += final_command

    for attempt in range(retries + 1):
        _ssh_semaphore.acquire()
        try:
            log.debug(f"SSH exec (attempt {attempt+1}): {' '.join(command)}")
            result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return result

            # SSH bağlantı hatası (exit 255) → retry
            if result.returncode == 255 and attempt < retries:
                wait = (attempt + 1) * 2
                log.warning(f"SSH bağlantı hatası, {wait}s sonra tekrar denenecek ({attempt+1}/{retries})")
                time.sleep(wait)
                continue

            if result.returncode != 0:
                log.error(f"Remote command failed: {' '.join(command)}")
                if result.stderr:
                    log.error(f"Stderr: {result.stderr.strip()[:200]}")
            return result
        except subprocess.TimeoutExpired:
            log.error(f"SSH zaman aşımı: {' '.join(command)}")
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
            
        if _is_local(CT_991_HOST):
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
        if CT_991_USER != "root":
            remote_cmd = f"sudo mkdir -p {target_dir} && sudo tee {CHROOT_MANAGE_SCRIPT} > /dev/null && sudo chmod +x {CHROOT_MANAGE_SCRIPT}"

        # Dizin varlığından emin ol ve dosyayı SSH üzerinden pipe ile gönder
        ssh_cmd = [
            "ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes" if not CT_991_PASS else "BatchMode=no",
            "-p", str(CT_991_REAL_SSH_PORT),
            f"{CT_991_USER}@{CT_991_HOST}",
            remote_cmd
        ]

        # Şifre varsa sshpass kullan
        if CT_991_PASS:
            ssh_cmd = ["sshpass", "-p", CT_991_PASS] + ssh_cmd
        
        subprocess.run(ssh_cmd, input=content, text=True, check=True)
        log.info(f"✅ chroot_yonetici.py {CT_991_HOST} üzerine senkronize edildi.")
        
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


def chroot_ip_al(username: str) -> str:
    """SSH IP adresini döndür (CT 991 IP)."""
    return CT_991_HOST


def chroot_durum(username: str) -> bool:
    """Chroot durumu kontrol et."""
    return chroot_var_mi(username)


def chroot_listesi() -> list:
    """Tüm chroot ortamlarını listele."""
    result = _ct991_exec([PYTHON_PATH, CHROOT_MANAGE_SCRIPT, "list"])

    if result.returncode != 0:
        log.error(f"Chroot listesi alınamadı: {result.stderr}")
        return []

    chroots = []
    for line in result.stdout.strip().split('\n'):
        if line.strip() and line.strip() != "Öğrenci Chroot'ları:":
            username = line.strip().replace("- ", "").strip()
            if username:
                chroots.append({
                    "username": username,
                    "active": True
                })

    return chroots


def ssh_bilgi(username: str) -> dict:
    """SSH bağlantı bilgileri."""
    username = _slugify(username)
    return {
        "host": CT_991_HOST,
        "port": CT_991_SSH_PORT,
        "username": username,
        "password": username,  # Kullanıcı adı ile aynı
        "command": f"ssh -p {CT_991_SSH_PORT} {username}@{CT_991_HOST}"
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
