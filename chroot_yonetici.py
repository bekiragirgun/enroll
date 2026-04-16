#!/usr/bin/env python3
"""
Chroot + PAM Çoklu Kullanıcı Terminal Yöneticisi

Her öğrenci için izole chroot ortamı.
Öğrenci kendi chroot'unda sudo su - ile root olabilir.
"""

import os
import subprocess
import pwd
import grp
import shutil
import socket
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

VERSION = "2026-04-06-CHROOT-MULTIARCH-V14"
log.info(f"🚀 Chroot Manager Script Version: {VERSION}")

# Yapılandırma
CHROOT_BASE = Path("/home/chroot")
STUDENT_TEMPLATE = CHROOT_BASE / "template"
STUDENT_GROUP = "ogrenciler"
SUDOERS_FILE = "/etc/sudoers.d/chroot-ogrenciler"


def _run(cmd, check=True, **kwargs):
    """Komut çalıştır."""
    log.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if check and result.returncode != 0:
        log.error(f"Command failed: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result


def _fix_su_binary(chroot_path):
    """
    Chroot içindeki su binary'sinin GLIBC uyumluluğunu kontrol et.
    Host'un su'su (GLIBC 2.38+) Debian 12 chroot'ta (GLIBC 2.36) çalışmaz.
    Çözüm: chroot'un kendi util-linux paketindeki su'yu kullan veya wget ile indir.
    """
    su_usr = chroot_path / "usr" / "bin" / "su"
    su_bin = chroot_path / "bin" / "su"

    # 1. Mevcut su çalışıyor mu test et
    if su_usr.exists():
        result = subprocess.run(["chroot", str(chroot_path), "/usr/bin/su", "--version"],
                                capture_output=True, text=True)
        if result.returncode == 0 and "GLIBC" not in result.stderr:
            log.info(f"✅ su binary uyumlu: {chroot_path}")
            return

    log.info(f"🔧 su binary düzeltiliyor: {chroot_path}")

    # 2. Chroot içinden apt ile kurmayı dene (mount'lar gerekli değil — zaten kurulu olabilir)
    #    login paketi su'yu içerir (Debian 12'de su login paketinde)
    #    Ama mount olmadan apt çalışmaz, bu yüzden doğrudan wget ile indir

    # 3. wget ile Debian 12 util-linux'tan su binary'sini indir
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        deb_path = Path(tmpdir) / "util-linux.deb"
        extract_path = Path(tmpdir) / "extract"
        arch = "arm64" if platform.machine() == "aarch64" else "amd64"

        # Birden fazla mirror dene
        mirrors = [
            f"http://deb.debian.org/debian/pool/main/u/util-linux/util-linux_2.38.1-5+deb12u3_{arch}.deb",
            f"http://ftp.debian.org/debian/pool/main/u/util-linux/util-linux_2.38.1-5+deb12u3_{arch}.deb",
            f"http://mirror.leaseweb.com/debian/pool/main/u/util-linux/util-linux_2.38.1-5+deb12u3_{arch}.deb",
        ]

        downloaded = False
        for url in mirrors:
            log.info(f"⬇️  Deneniyor: {url}")
            result = subprocess.run(["wget", "-q", "--no-check-certificate", "-O", str(deb_path), url],
                                    capture_output=True, text=True)
            if result.returncode == 0 and deb_path.exists() and deb_path.stat().st_size > 100000:
                downloaded = True
                break
            log.warning(f"⚠️  İndirilemedi, sonraki mirror deneniyor...")

        if not downloaded:
            log.error("❌ su binary hiçbir mirror'dan indirilemedi!")
            return

        # deb paketinden su binary'sini çıkar
        subprocess.run(["dpkg", "-x", str(deb_path), str(extract_path)], check=False)
        src_su = extract_path / "bin" / "su"

        if not src_su.exists():
            log.error("❌ İndirilen pakette /bin/su bulunamadı!")
            return

        # Eski su'ları temizle (symlink veya binary)
        for su_path in [su_usr, su_bin]:
            if su_path.exists() or su_path.is_symlink():
                su_path.unlink()

        # Gerçek binary'yi kopyala (symlink DEĞİL!)
        shutil.copy2(str(src_su), str(su_usr))
        os.chmod(str(su_usr), 0o4755)

        # /bin → /usr/bin symlink ise /bin/su otomatik görünür
        # Değilse /bin/su'ya da kopyala
        if not su_bin.exists():
            shutil.copy2(str(src_su), str(su_bin))
            os.chmod(str(su_bin), 0o4755)

        # Doğrula
        result = subprocess.run(["chroot", str(chroot_path), "/usr/bin/su", "--version"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            log.info(f"✅ su binary düzeltildi: {chroot_path}")
        else:
            log.error(f"❌ su binary düzeltme başarısız: {result.stderr}")


def _fix_etc_hosts(chroot_path):
    """Chroot içindeki /etc/hosts'a hostname satırı ekle.

    Yoksa `sudo` her çağrıda "unable to resolve host ..." uyarısı verir.
    Host sisteminin hostname'ini (genelde Debian12) 127.0.0.1'e bağlarız.
    """
    hosts_file = chroot_path / "etc" / "hosts"
    if not hosts_file.exists():
        return

    try:
        hostname = socket.gethostname().strip() or "Debian12"
    except Exception:
        hostname = "Debian12"

    try:
        icerik = hosts_file.read_text()
    except Exception as e:
        log.warning(f"⚠️ /etc/hosts okunamadı ({chroot_path}): {e}")
        return

    if hostname in icerik:
        return

    try:
        with open(hosts_file, "a") as f:
            f.write(f"127.0.0.1 {hostname}\n")
        log.info(f"✅ /etc/hosts güncellendi: {hostname} → {chroot_path}")
    except Exception as e:
        log.warning(f"⚠️ /etc/hosts yazılamadı ({chroot_path}): {e}")


def _fix_ping_caps(chroot_path):
    """ping binary'sine cap_net_raw+ep yetkisi ver.

    rsync varsayılanı extended attribute (xattr) kopyalamaz — bu yüzden
    template'ten öğrenci chroot'una geçerken capability kaybolur ve
    sıradan kullanıcı `ping: Operation not permitted` alır.
    Her iki olası yola da setcap uygular.
    """
    adaylar = [
        chroot_path / "bin" / "ping",
        chroot_path / "usr" / "bin" / "ping",
    ]
    uygulanan = False
    for p in adaylar:
        if not p.exists() or p.is_symlink():
            continue
        result = subprocess.run(
            ["setcap", "cap_net_raw+ep", str(p)],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            uygulanan = True
            log.info(f"✅ ping capability ayarlandı: {p}")
        else:
            log.warning(f"⚠️ setcap başarısız ({p}): {result.stderr.strip()}")

    if not uygulanan:
        log.warning(f"⚠️ ping binary bulunamadı: {chroot_path}")


def repair_system_pty():
    """
    Host sistemdeki (CT 991) PTY ve /dev/pts yapılandırmasını onarır.
    LXC içinde PTY allocation hatasını (5, 2) çözmek için kritiktir.
    """
    log.info("🛠️ Sistem PTY ve /dev/pts onarılıyor...")
    
    # 1. /dev/pts mount edilmiş mi kontrol et (devpts türünde olmalı)
    try:
        mounts = subprocess.run(["mount"], capture_output=True, text=True).stdout
        if "devpts on /dev/pts type devpts" not in mounts:
            log.warning("⚠️ /dev/pts devpts olarak mount edilmemiş! Düzeltiliyor...")
            subprocess.run(["umount", "-l", "/dev/pts"], check=False)
            _run(["mount", "-t", "devpts", "devpts", "/dev/pts", "-o", "rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=666"], check=False)
    except Exception as e:
        log.error(f"PTS mount kontrolünde hata: {e}")
    
    # 2. /dev/ptmx kontrolü ve onarımı
    ptmx = Path("/dev/ptmx")
    if ptmx.exists():
        # Eğer symlink değilse ve karakter cihazıysa, bazen symlink olması daha iyidir (LXC)
        # Ama önce izinleri düzeltmeyi deneyelim
        _run(["chmod", "666", "/dev/ptmx"], check=False)
        _run(["chown", "root:tty", "/dev/ptmx"], check=False)
    else:
        # Ptmx yoksa oluştur (mknod veya ln)
        log.warning("⚠️ /dev/ptmx bulunamadı! Oluşturuluyor...")
        # Önce symlink dene (LXC için önerilen)
        _run(["ln", "-s", "/dev/pts/ptmx", "/dev/ptmx"], check=False)
        _run(["chmod", "666", "/dev/ptmx"], check=False)

    # 3. /dev/tty izinleri
    _run(["chmod", "666", "/dev/tty"], check=False)
    
    log.info("✅ Sistem PTY onarımı tamamlandı.")


def setup_persistence():
    """
    Onarım işlemini her açılışta çalışacak bir systemd servisi olarak kurar.
    """
    service_content = f"""[Unit]
Description=Chroot PTY Repair Service
After=network.target

[Service]
Type=oneshot
ExecStart={os.path.abspath(__file__)} repair
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
"""
    service_path = Path("/etc/systemd/system/chroot-pty-fix.service")
    log.info(f"📝 Servis dosyası oluşturuluyor: {service_path}")
    
    try:
        service_path.write_text(service_content)
        _run(["systemctl", "daemon-reload"])
        _run(["systemctl", "enable", "chroot-pty-fix.service"])
        _run(["systemctl", "start", "chroot-pty-fix.service"])
        log.info("✅ PTY onarım servisi başarıyla kuruldu ve başlatıldı.")
    except Exception as e:
        log.error(f"❌ Servis kurulum hatası: {e}")


def setup_template():
    """Şablon chroot ortamı oluştur."""
    log.info("Şablon chroot ortamı kuruluyor...")

    # ÖNCE SİSTEM PTY ONAR (V14)
    repair_system_pty()

    # Mimari Tespiti (V13)
    import platform
    machine = platform.machine() # x86_64 veya aarch64
    if machine == "x86_64":
        target_arch = "amd64"
    elif machine == "aarch64":
        target_arch = "arm64"
    else:
        target_arch = machine # Fallback
    log.info(f"Detected architecture: {machine} (Target arch for mmdebstrap: {target_arch})")

    # ÖNCE TEMİZLİK (V11): Eski mount'ları temizle ki rm -rf veya init hata vermesin
    log.info("🧹 Eski şablon mount'ları temizleniyor...")
    for p in ["proc", "sys", "dev/pts", "dev"]:
        subprocess.run(["umount", "-l", str(STUDENT_TEMPLATE / p)], check=False)

    # Debian 12 base kur (mmdebstrap — SSL/hash bypass ile)
    if not STUDENT_TEMPLATE.exists():
        STUDENT_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
        log.info("⬇️  mmdebstrap ile Debian 12 bookworm template indiriliyor...")
        _run([
            "mmdebstrap", f"--arch={target_arch}",
            '--aptopt=Acquire::https::Verify-Peer "false"',
            '--aptopt=Acquire::Check-Valid-Until "false"',
            '--aptopt=Acquire::AllowInsecureRepositories "true"',
            '--aptopt=APT::Get::AllowUnauthenticated "true"',
            "--include=gnupg,debian-archive-keyring,gpgv,ca-certificates",
            "bookworm",
            str(STUDENT_TEMPLATE),
            "http://deb.debian.org/debian"
        ])

    # 1. Full Repositories (Debian 12)
    sources_list = STUDENT_TEMPLATE / "etc" / "apt" / "sources.list"
    
    repo_content = f"""
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
"""
    sources_list.write_text(repo_content.strip() + "\n")
    log.info("📝 sources.list Debian 12 mirrorları ile güncellendi.")

    # DNS filtering - şablonda yap
    resolv_conf = STUDENT_TEMPLATE / "etc" / "resolv.conf"
    resolv_conf.write_text("nameserver 185.228.168.168\n")
    resolv_conf.write_text("nameserver 185.228.169.168\n")

    # Hosts dosyası - sosyal medya engelle
    hosts_file = STUDENT_TEMPLATE / "etc" / "hosts"
    blocked_sites = [
        "www.facebook.com facebook.com",
        "www.twitter.com twitter.com x.com",
        "www.instagram.com instagram.com",
        "www.tiktok.com tiktok.com",
        "www.youtube.com youtube.com",
        "www.linkedin.com linkedin.com",
        "www.reddit.com reddit.com",
        "www.cnn.com cnn.com",
        "www.bbc.com bbc.com",
        "www.nytimes.com nytimes.com",
        "www.hurriyet.com.tr hurriyet.com.tr",
        "www.milliyet.com.tr milliyet.com.tr",
        "www.sozcu.com.tr sozcu.com.tr",
    ]

    for site in blocked_sites:
        with open(hosts_file, 'a') as f:
            f.write(f"127.0.0.1 {site}\n")

    # Temel ve Geliştirici Paketleri (V7/V8)
    # Apt işlemleri için /proc, /sys ve /dev mount edilmeli
    p = STUDENT_TEMPLATE / "proc"
    s = STUDENT_TEMPLATE / "sys"
    d = STUDENT_TEMPLATE / "dev"
    pts = d / "pts"

    for path in [p, s, d, pts]: path.mkdir(exist_ok=True)

    log.info("📦 Apt paketleri için geçici filesystem'ler mount ediliyor...")
    subprocess.run(["mount", "-t", "proc", "proc", str(p)], check=False)
    subprocess.run(["mount", "-t", "sysfs", "sysfs", str(s)], check=False)
    
    # LXC DESTEĞİ: /dev bind mount et ama nodev/nosuid gibi bayraklar gelmiş olabilir
    subprocess.run(["mount", "-o", "bind", "/dev", str(d)], check=False)
    subprocess.run(["mount", "-o", "bind", "/dev/pts", str(pts)], check=False)
    
    # KRİTİK: Cihazları onar (V11)
    _restore_device_nodes(d)

    # DNS Ayarları
    log.info("🌐 DNS ayarları yapılandırılıyor...")
    with open(STUDENT_TEMPLATE / "etc" / "resolv.conf", "w") as f:
        f.write("nameserver 8.8.8.8\nnameserver 1.1.1.1\n")

    # Time Sync Fix (Zaman uyumsuzluğu nedeniyle apt-get update hatasını önlemek için)
    log.info("🕒 Apt-get zaman uyumsuzluğu kontrolleri esnetiliyor...")
    (STUDENT_TEMPLATE / "etc" / "apt" / "apt.conf.d").mkdir(parents=True, exist_ok=True)
    with open(STUDENT_TEMPLATE / "etc" / "apt" / "apt.conf.d" / "99ignore-time-errors", "w") as f:
        f.write('Acquire::Check-Valid-Until "false";\n'
                'Acquire::Check-Date "false";\n'
                'Acquire::https::Verify-Peer "false";\n'
                'Acquire::AllowInsecureRepositories "true";\n'
                'APT::Get::AllowUnauthenticated "true";\n')

    try:
        # Temel paketleri kur
        log.info("📦 Temel paketler chroot içinde kuruluyor...")
        # Ortam değişkenlerini ayarla (interaktif prompt'ları engellemek için)
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        
        # APT konfigürasyonunu zorlayarak çalıştır (Release file invalid yet hatasını kesin önlemek için)
        _run(["chroot", str(STUDENT_TEMPLATE), "apt-get",
              "-o", "Acquire::Check-Valid-Until=false",
              "-o", "Acquire::Check-Date=false",
              "-o", "Acquire::AllowInsecureRepositories=true",
              "-o", "APT::Get::AllowUnauthenticated=true",
              "update"], env=env)
        
        _run(["chroot", str(STUDENT_TEMPLATE), "apt-get", "install", "-y", "--allow-unauthenticated",
              "build-essential", "python3", "python3-pip",
              "git", "curl", "wget", "vim", "nano", "sudo", "locales",
              "login", "util-linux", "passwd",
              "dnsutils", "net-tools", "iputils-ping", "iproute2",
              "man-db", "tree", "zip", "unzip", "bzip2", "xz-utils", "tar", "gzip",
              "htop", "psmisc", "acl", "gawk", "sed", "grep", "findutils", "lsof",
              "openssh-client", "less", "file"], env=env)
    finally:
        log.info("🧹 Geçici filesystem'ler çözülüyor...")
        subprocess.run(["umount", "-l", str(pts)], check=False)
        subprocess.run(["umount", "-l", str(d)], check=False)
        subprocess.run(["umount", "-l", str(s)], check=False)
        subprocess.run(["umount", "-l", str(p)], check=False)
    
    # İzinler
    _run(["chmod", "1777", str(STUDENT_TEMPLATE / "tmp")])

    # su binary fix: Host'un su'su GLIBC uyumsuz — Debian 12'nin kendi su'sunu kullan
    _fix_su_binary(STUDENT_TEMPLATE)

    # /etc/hosts: sudo "unable to resolve host" uyarısını engelle
    _fix_etc_hosts(STUDENT_TEMPLATE)

    # ping capability: rsync xattr taşımadığı için template'te de setcap çağır
    _fix_ping_caps(STUDENT_TEMPLATE)

    # Temizlik
    _run(["chroot", str(STUDENT_TEMPLATE), "apt-get", "clean"])

    # Öğrenci grubu oluştur
    try:
        grp.getgrnam(STUDENT_GROUP)
    except KeyError:
        _run(["groupadd", STUDENT_GROUP])

    # Skel'i Ubuntu-benzeri varsayılan home yapısıyla doldur
    setup_skel()

    log.info("✅ Şablon chroot hazır!")




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


def sync_chroot_configs(username, real_name=""):
    """Chroot içindeki konfigürasyon dosyalarını host ile senkronize et."""
    username = _slugify(username)
    # real_name sanitization: remove ":" and newlines to prevent passwd/shadow corruption
    if real_name:
        real_name = str(real_name).replace(":", " ").replace("\n", " ").strip()
    
    student_path = CHROOT_BASE / username
    if not student_path.exists():
        log.error(f"Chroot dizini yok: {student_path}")
        return False

    log.info(f"🔄 {username} için konfigürasyonlar senkronize ediliyor... (Path: {student_path})")

    try:
        # Host'tan kullanıcı bilgilerini al
        try:
            user_info = pwd.getpwnam(username)
        except KeyError:
            log.error(f"❌ Host'ta kullanıcı bulunamadı: {username}")
            return False

        try:
            group_info = grp.getgrnam(STUDENT_GROUP)
        except KeyError:
            log.warning(f"⚠️ {STUDENT_GROUP} grubu bulunamadı, oluşturuluyor...")
            _run(["groupadd", STUDENT_GROUP])
            group_info = grp.getgrnam(STUDENT_GROUP)
        
        # /etc/passwd senkronizasyonu
        passwd_file = student_path / "etc" / "passwd"
        if passwd_file.exists():
            lines = passwd_file.read_text().splitlines()
            original_len = len(lines)
            # Mevcut kullanıcıyı temizle
            lines = [l for l in lines if not l.startswith(f"{username}:")]
            # Yeni satırı ekle
            passwd_line = f"{username}:x:{user_info.pw_uid}:{user_info.pw_gid}:{real_name or user_info.pw_gecos}:{user_info.pw_dir}:{user_info.pw_shell}"
            lines.append(passwd_line)
            passwd_file.write_text("\n".join(lines) + "\n")
            log.info(f"📝 {passwd_file} güncellendi ({original_len} -> {len(lines)} satır)")
        else:
            log.error(f"❌ {passwd_file} bulunamadı!")

        # /etc/group senkronizasyonu
        group_file = student_path / "etc" / "group"
        if group_file.exists():
            lines = group_file.read_text().splitlines()
            # Mevcut grubu temizle
            lines = [l for l in lines if not l.startswith(f"{STUDENT_GROUP}:")]
            # Yeni satırı ekle (Host'taki gerçek GID'yi kullan)
            lines.append(f"{STUDENT_GROUP}:x:{user_info.pw_gid}:{username}")
            # tty grubunu da ekle (PTY ve sudo için önemli)
            if not any(l.startswith("tty:") for l in lines):
                lines.append("tty:x:5:")
            group_file.write_text("\n".join([l for l in lines if l.strip()]) + "\n")
            log.info(f"📝 {group_file} güncellendi (GID: {user_info.pw_gid})")

        # /etc/shadow senkronizasyonu (Authentication failure çözümü)
        shadow_file = student_path / "etc" / "shadow"
        host_shadow = Path("/etc/shadow")
        if shadow_file.exists() and host_shadow.exists():
            # Host'tan bu kullanıcıya ait satırı bul
            with open(host_shadow, 'r') as f:
                shadow_lines = f.readlines()
            user_shadow_line = next((l for l in shadow_lines if l.startswith(f"{username}:")), None)
            
            if user_shadow_line:
                lines = shadow_file.read_text().splitlines()
                # Mevcut kullanıcıyı temizle
                lines = [l for l in lines if not l.startswith(f"{username}:")]
                lines.append(user_shadow_line.strip())
                shadow_file.write_text("\n".join(lines) + "\n")
                _run(["chmod", "0640", str(shadow_file)])
                log.info(f"📝 {shadow_file} güncellendi")
            else:
                # Host'ta yoksa placeholder ekle (şifresiz ama kilitli olmayan)
                lines = shadow_file.read_text().splitlines()
                if not any(l.startswith(f"{username}:") for l in lines):
                    lines.append(f"{username}:*:19000:0:99999:7:::")
                    shadow_file.write_text("\n".join(lines) + "\n")
                    log.info(f"📝 {shadow_file} için placeholder eklendi")

        # /etc/hosts ve /etc/hostname senkronizasyonu (Sudo fix)
        try:
            hosts_file = student_path / "etc" / "hosts"
            hosts_content = "127.0.0.1\tlocalhost\n127.0.1.1\togrenci-vm\n"
            hosts_file.write_text(hosts_content)
            (student_path / "etc" / "hostname").write_text("ogrenci-vm\n")
            log.info(f"📝 {hosts_file} ve hostname güncellendi")
        except Exception as e:
            log.warning(f"⚠️ Hosts güncelleme hatası: {e}")

        # Sudoers dosyasını kopyala ve içeriği doğrula
        sudo_dst = student_path / "etc" / "sudoers.d" / "chroot-ogrenciler"
        sudo_dst.parent.mkdir(parents=True, exist_ok=True)
        # Doğrudan içeriği yaz (Host'a güvenmek yerine). PTY sorunlarını önlemek için !use_pty eklendi.
        sudo_content = f"Defaults:%{STUDENT_GROUP} !use_pty\n%{STUDENT_GROUP} ALL=(ALL) NOPASSWD: ALL\n{username} ALL=(ALL) NOPASSWD: ALL\n"
        sudo_dst.write_text(sudo_content)
        _run(["chmod", "0440", str(sudo_dst)], check=False)
        log.info(f"📝 Sudoers yapılandırıldı: {sudo_dst}")

        return True
    except Exception as e:
        log.error(f"❌ Konfigürasyon senkronizasyon hatası: {e}")
        import traceback
        log.error(traceback.format_exc())
        return False
def create_student_chroot(username, real_name=""):
    """Öğrenci için chroot ortamı oluştur."""
    # Username'i normalize et
    raw_username = username
    username = _slugify(username)
    student_path = CHROOT_BASE / username

    if student_path.exists() and (student_path / "etc" / "passwd").exists():
        log.warning(f"{username} için chroot zaten var, konfigürasyonu güncelliyorum.")
    else:
        log.info(f"{username} için chroot oluşturuluyor/onarılıyor...")
        student_path.mkdir(parents=True, exist_ok=True)
        # Şablondan kopyala
        result = subprocess.run(
            ["rsync", "-a", "--exclude=/dev/*", "--exclude=/proc/*",
                   "--exclude=/sys/*", "--exclude=/var/run/*",
                   f"{STUDENT_TEMPLATE}/", f"{student_path}/"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            log.error(f"Chroot kopyalama hatası: {result.stderr}")
            return False

    # Gerekli dizinleri manuel oluştur
    for d in ["dev", "proc", "sys", "var/run"]:
        (student_path / d).mkdir(parents=True, exist_ok=True)

    # Host sistemde kullanıcıyı oluştur (SSH için)
    try:
        try:
            pwd.getpwnam(username)
        except KeyError:
            # --badname: Sayısal kullanıcı adlarına (örn: 123) izin ver
            # real_name parametresini -c olarak ekliyoruz
            display_name = real_name if real_name else raw_username
            _run(["useradd", "--badname", "-m", "-s", "/bin/bash", "-G", STUDENT_GROUP, "-c", display_name, username])
    except Exception as e:
        log.error(f"Kullanıcı oluşturma hatası: {e}")
        # Kritik hata değilse devam et (belki sync düzeltebilir)

    # Konfigürasyonları senkronize et
    if not sync_chroot_configs(username, real_name):
        log.error("Konfigürasyon senkronizasyonu başarısız!")
        # Burada durmuyoruz ama hata logu kritik

    # Home dizini — skel'den kopyala (ilk kez ise)
    student_home = student_path / "home" / username
    skel_path = STUDENT_TEMPLATE / "etc" / "skel"

    if not student_home.exists():
        student_home.mkdir(mode=0o755, parents=True)

        # Skel varsa içeriğini kopyala (Ubuntu varsayılan home yapısı)
        if skel_path.exists():
            subprocess.run(
                ["cp", "-a", f"{skel_path}/.", str(student_home)],
                check=False
            )
            log.info(f"📂 Skel kopyalandı → {student_home}")
        else:
            # Skel yoksa en azından temel dosyaları oluştur
            (student_home / ".bashrc").write_text(
                f'export PS1="\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ "\n'
                f'alias ll="ls -la"\nalias root="sudo su -"\nexport IGNOREEOF=10\n'
            )
            (student_home / ".profile").write_text(
                '[ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc"\n'
            )

    # Home sahipliğini öğrenciye ver
    try:
        user_info = pwd.getpwnam(username)
        _run(["chown", "-R", f"{user_info.pw_uid}:{user_info.pw_gid}", str(student_home)], check=False)
    except KeyError:
        pass

    # su binary fix — rsync sonrası host su'su gelmiş olabilir
    _fix_su_binary(student_path)

    # /etc/hosts + ping capability — rsync xattr taşımaz, her chroot'ta yeniden uygula
    _fix_etc_hosts(student_path)
    _fix_ping_caps(student_path)

    log.info(f"✅ {username} chroot ortamı hazır.")
    return True


def create_ssh_entry(username):
    """Kullanıcı için SSH Match block ve Sudoers yetkisi oluştur."""
    username = _slugify(username)
    student_path = CHROOT_BASE / username
    
    # Kullanıcının shell'i /bin/bash olsun
    subprocess.run(["usermod", "-s", "/bin/bash", username], check=False)

    # Sudoers'a chroot yetkisi ekle
    sudoers_line = f"{username} ALL=(ALL) NOPASSWD: /usr/sbin/chroot\n"
    sudoers_file = Path("/etc/sudoers.d/chroot-ogrenciler")

    # Sudoers dosyasına ekle
    existing_sudoers = sudoers_file.read_text() if sudoers_file.exists() else ""
    if sudoers_line not in existing_sudoers:
        with open(sudoers_file, 'a') as f:
            f.write(sudoers_line)
        subprocess.run(["chmod", "0440", str(sudoers_file)], check=False)

    # SSH config'e Match Group ekle (tek blok, $USER ile — per-user Match gerekmez)
    ssh_config = Path("/etc/ssh/sshd_config")
    group_match = 'Match Group ogrenciler'
    ssh_config_text = ssh_config.read_text()
    if group_match not in ssh_config_text:
        with open(ssh_config, 'a') as f:
            f.write(f"\n{group_match}\n")
            f.write('    ForceCommand /bin/bash -c "while true; do sudo /usr/sbin/chroot /home/chroot/$USER /bin/su - $USER; echo \'Oturum kapatilamaz, yeniden baslatiliyor...\'; sleep 1; done"\n')

    # Chroot login script'ini kopyala
    chrootlogin_src = Path("/usr/sbin/chrootlogin")
    chrootlogin_dst = student_path / "usr" / "sbin" / "chrootlogin"
    if chrootlogin_src.exists():
        chrootlogin_dst.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", str(chrootlogin_src), str(chrootlogin_dst)], check=False)
        subprocess.run(["chmod", "+x", str(chrootlogin_dst)], check=False)

    # SSH'yi restart et
    subprocess.run(["systemctl", "restart", "sshd"], check=False)
    log.info(f"✅ {username} SSH/Sudoers yapılandırması tamam")


def setup_skel():
    """
    Template içindeki /etc/skel'i Ubuntu benzeri varsayılan home yapısıyla doldur.

    Yeni öğrenci oluşturulduğunda bu skel kopyalanır.
    Mevcut öğrenciler etkilenmez.
    """
    skel = STUDENT_TEMPLATE / "etc" / "skel"
    skel.mkdir(parents=True, exist_ok=True)

    # ── Standart Ubuntu home klasörleri ──────────────────────────
    for klasor in ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos", "Public", "Templates"]:
        (skel / klasor).mkdir(exist_ok=True)

    # ── Laboratuvar klasörü ───────────────────────────────────────
    lab = skel / "lab"
    lab.mkdir(exist_ok=True)

    # Karşılama / tanıtım dosyası
    (lab / "00_hos_geldiniz.txt").write_text("""\
╔══════════════════════════════════════════════════════╗
║   Kapadokya Üniversitesi — Linux Laboratuvarı        ║
╚══════════════════════════════════════════════════════╝

Bu terminal sizin izole çalışma alanınızdır.
Burada yaptığınız değişiklikler sadece size aittir.

Faydalı komutlar:
  ls -la         → Dosya listesi (gizli dosyalar dahil)
  pwd            → Bulunduğunuz dizin
  cd ~/lab       → Lab klasörüne git
  sudo su -      → Root kullanıcısına geç
  man <komut>    → Komut kılavuzunu aç

Alıştırmalar için: cd ~/lab/alistirmalar
""")

    # Alıştırma klasörü
    alist = lab / "alistirmalar"
    alist.mkdir(exist_ok=True)

    (alist / "01_dosya_islemleri.sh").write_text("""\
#!/bin/bash
# Alıştırma 1: Temel Dosya İşlemleri
# Bu dosyayı inceleyin ve komutları teker teker çalıştırın.

echo "=== Dizin Yapısı ==="
ls -la ~/

echo ""
echo "=== Yeni Dizin Oluştur ==="
mkdir -p ~/Documents/proje1
echo "proje1 dizini oluşturuldu"

echo ""
echo "=== Dosya Oluştur ve Düzenle ==="
echo "Merhaba Dünya" > ~/Documents/proje1/readme.txt
cat ~/Documents/proje1/readme.txt

echo ""
echo "Alıştırma 1 tamamlandı!"
""")
    (alist / "01_dosya_islemleri.sh").chmod(0o755)

    (alist / "02_izinler.sh").write_text("""\
#!/bin/bash
# Alıştırma 2: Dosya İzinleri
# chmod ve chown komutlarını öğrenin.

echo "=== Mevcut İzinleri Gör ==="
ls -la ~/lab/alistirmalar/

echo ""
echo "=== İzin Değiştir ==="
touch ~/Documents/test_dosyasi.txt
chmod 644 ~/Documents/test_dosyasi.txt
ls -la ~/Documents/test_dosyasi.txt

echo ""
echo "=== İzin Sembolik Gösterim ==="
echo "r=4, w=2, x=1"
echo "644 = rw-r--r-- (Sahibi: okuma+yazma, Diğerleri: sadece okuma)"
echo "755 = rwxr-xr-x (Sahibi: tam yetki, Diğerleri: okuma+çalıştırma)"
""")
    (alist / "02_izinler.sh").chmod(0o755)

    (alist / "03_metin_islemleri.sh").write_text("""\
#!/bin/bash
# Alıştırma 3: Metin İşleme (grep, awk, sed)

echo "=== grep ile Arama ==="
grep "root" /etc/passwd

echo ""
echo "=== awk ile Sütun Alma ==="
awk -F: '{print $1}' /etc/passwd | head -5

echo ""
echo "=== sed ile Değiştirme ==="
echo "merhaba dünya" | sed 's/dünya/linux/'

echo ""
echo "=== Pipeline ==="
cat /etc/passwd | grep -v "^#" | awk -F: '{print $1, $7}' | head -5
""")
    (alist / "03_metin_islemleri.sh").chmod(0o755)

    # ── Ders Notları ─────────────────────────────────────────────
    notlar = lab / "notlar"
    notlar.mkdir(exist_ok=True)

    (notlar / "01_linux_temelleri.md").write_text("""\
# Linux Temelleri

## Dosya Sistemi

Linux'ta her şey bir dosyadır. Kök dizin `/` ile başlar.

```
/
├── bin/    → Temel komutlar (ls, cp, mv...)
├── etc/    → Yapılandırma dosyaları
├── home/   → Kullanıcı home dizinleri
├── tmp/    → Geçici dosyalar
├── usr/    → Kullanıcı programları
└── var/    → Değişken veri (log, cache...)
```

## Temel Komutlar

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `ls`  | Dosya listele | `ls -la` |
| `cd`  | Dizin değiştir | `cd /etc` |
| `pwd` | Bulunduğun dizin | `pwd` |
| `mkdir` | Dizin oluştur | `mkdir proje` |
| `rm` | Sil | `rm dosya.txt` |
| `cp` | Kopyala | `cp a.txt b.txt` |
| `mv` | Taşı/Yeniden adlandır | `mv eski.txt yeni.txt` |
| `cat` | İçerik göster | `cat /etc/hostname` |
| `man` | Kılavuz sayfası | `man ls` |

## Dosya İzinleri

```
-rw-r--r-- 1 kullanici grup 1234 Mar 17 10:00 dosya.txt
│└──┘└──┘└──┘
│ │   │   └── Diğerleri izinleri
│ │   └────── Grup izinleri
│ └────────── Sahip izinleri
└──────────── Dosya tipi (- = dosya, d = dizin)
```

**Sayısal gösterim:** r=4, w=2, x=1
- `chmod 755 dosya` → rwxr-xr-x
- `chmod 644 dosya` → rw-r--r--

## Metin İşleme

```bash
grep "arama" dosya.txt        # Metin ara
grep -r "arama" ./dizin/      # Dizinde ara
cat dosya.txt | grep "arama"  # Pipeline ile ara
sed 's/eski/yeni/g' dosya.txt # Metni değiştir
awk '{print $1}' dosya.txt    # İlk sütunu al
```
""")

    (notlar / "02_kullanici_yonetimi.md").write_text("""\
# Kullanıcı ve Grup Yönetimi

## Temel Kavramlar

- Her dosyanın bir **sahibi** (user) ve **grubu** (group) var
- **root** kullanıcısı (UID=0) tam yetkiye sahip
- Normal kullanıcılar kendi dosyaları üzerinde işlem yapabilir

## Komutlar

```bash
whoami              # Mevcut kullanıcı
id                  # Kullanıcı ID ve grup bilgisi
sudo su -           # Root kullanıcısına geç
passwd              # Şifre değiştir

# Kullanıcı yönetimi (root yetkisi gerekir)
useradd yeni_kullanici
userdel eski_kullanici
usermod -G grup kullanici

# Grup yönetimi
groupadd yeni_grup
groups kullanici    # Kullanıcının grupları
```

## /etc/passwd Yapısı

```
kullanici:x:1001:1001:Ad Soyad:/home/kullanici:/bin/bash
    │      │  │    │      │           │              └── Shell
    │      │  │    │      │           └── Home dizini
    │      │  │    │      └── GECOS (Açıklama)
    │      │  │    └── GID (Grup ID)
    │      │  └── UID (Kullanıcı ID)
    │      └── Şifre (x = shadow'da)
    └── Kullanıcı adı
```

## sudo Kullanımı

```bash
sudo komut              # Tek komut root ile çalıştır
sudo su -               # Root shell'e geç
sudo cat /etc/shadow    # Root gerektiren dosyayı oku
```
""")

    (notlar / "03_ag_komutlari.md").write_text("""\
# Ağ Komutları

## Bağlantı Kontrol

```bash
ping 8.8.8.8            # ICMP ile bağlantı testi
ping -c 4 google.com    # 4 paket gönder
traceroute google.com   # Rota takip
nslookup google.com     # DNS sorgusu
dig google.com          # Detaylı DNS sorgusu
```

## Ağ Arayüzleri

```bash
ip addr                 # IP adresleri (modern)
ip addr show eth0       # Belirli arayüz
ifconfig                # Ağ arayüzleri (eski)
ip route                # Yönlendirme tablosu
```

## Bağlantı Durumu

```bash
ss -tuln                # Açık portlar
ss -tnp                 # TCP bağlantıları + process
netstat -tuln           # Eski stil port listesi
curl -I http://site.com # HTTP başlık bilgisi
wget http://site.com    # Dosya indir
```

## SSH

```bash
ssh kullanici@sunucu         # SSH bağlantısı
ssh -p 2222 kullanici@sunucu # Port belirt
scp dosya.txt k@sunucu:~/    # Dosya kopyala
```
""")

    log.info(f"✅ Ders notları skel'e eklendi: {notlar}")

    # ── .bashrc (zenginleştirilmiş) ───────────────────────────────
    (skel / ".bashrc").write_text("""\
# ~/.bashrc — Kapadokya Üniversitesi Linux Lab

export PS1="\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ "
export LANG=tr_TR.UTF-8
export IGNOREEOF=10

# Takma adlar
alias ll='ls -la --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias ls='ls --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias root='sudo su -'
alias lab='cd ~/lab'
alias alistirma='cd ~/lab/alistirmalar'

# Renkli grep
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Bilgi mesajı (sadece interaktif oturumda)
if [[ $- == *i* ]]; then
    echo "──────────────────────────────────────────"
    echo "  Kapadokya Üniversitesi Linux Laboratuvarı"
    echo "  Kullanıcı : $USER"
    echo "  Sunucu    : $(hostname)"
    echo "  Alıştırma : cd ~/lab && ls"
    echo "──────────────────────────────────────────"
fi
""")

    # ── .profile ─────────────────────────────────────────────────
    (skel / ".profile").write_text("""\
if [ -n "$BASH_VERSION" ]; then
    [ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc"
fi
[ -d "$HOME/bin" ] && PATH="$HOME/bin:$PATH"
""")

    # ── .bash_history (örnek komutlar, başlangıç rehberi) ─────────
    (skel / ".bash_history").write_text("""\
ls -la
cd ~/lab
cat ~/lab/00_hos_geldiniz.txt
cd ~/lab/alistirmalar
ls -la
bash 01_dosya_islemleri.sh
""")

    log.info(f"✅ /etc/skel Ubuntu-benzeri yapıyla dolduruldu: {skel}")


def list_student_chroots():
    """Tüm öğrenci chroot'larını listele."""
    if not CHROOT_BASE.exists():
        return []

    return [d.name for d in CHROOT_BASE.iterdir() if d.is_dir() and d.name != "template"]


def delete_student_chroot(username):
    """Öğrenci chroot'unu sil."""
    username = _slugify(username)
    student_path = CHROOT_BASE / username

    if not student_path.exists():
        log.warning(f"{username} chroot bulunamadı")
        return False

    # Önce mount'ları unmount et (V11 Robustness)
    # Lazy unmount (-l) busy olsa bile temizler
    log.info(f"🧹 {username} mount noktaları temizleniyor...")
    for p in ["dev/pts", "dev", "proc", "sys"]:
        subprocess.run(["umount", "-l", str(student_path / p)], check=False)

    # Dizini sil
    shutil.rmtree(student_path)
    log.info(f"✅ {username} chroot silindi")
    return True



def _restore_device_nodes(dev_path):
    """
    Kritik cihaz düğümlerini (/dev/null, /dev/ptmx vb.) onarır.
    LXC içinde mknod çalışmazsa, host'tan bind-mount ile aktarır (V11).
    """
    devices = [
        ("null", "c 1 3"),
        ("zero", "c 1 5"),
        ("full", "c 1 7"),
        ("tty", "c 5 0"),
        ("random", "c 1 8"),
        ("urandom", "c 1 9")
    ]
    
    for dev_name, mode in devices:
        d_p = dev_path / dev_name
        
        # 1. Eğer zaten doğru bir karakter cihazıysa, sadece izinleri tazele (V12 Safety)
        if d_p.exists() and d_p.is_char_device():
            subprocess.run(["chmod", "666", str(d_p)], check=False)
            continue

        # 2. Karakter cihazı değilse (veya yoksa) silmeyi dene
        # Busy hatası almamak için sadece karakter cihazı değilse sileriz
        if d_p.exists() and not d_p.is_char_device():
            subprocess.run(["rm", "-f", str(d_p)], check=False)
        
        # 3. mknod dene (Privileged modda çalışır)
        if not d_p.exists():
            res = subprocess.run(["mknod", "-m", "666", str(d_p)] + mode.split(), capture_output=True)
            
            # 4. mknod başarısızsa (LXC Unprivileged), Host'tan BIND-MOUNT yap (V11 fallback)
            if res.returncode != 0:
                if not d_p.exists():
                    subprocess.run(["touch", str(d_p)], check=False)
                subprocess.run(["mount", "-o", "bind", f"/dev/{dev_name}", str(d_p)], check=False)
                subprocess.run(["chmod", "666", str(d_p)], check=False)
        else:
            # Dosya var ama karakter cihazı değilse (yukarıdaki rm başarısız olduysa)
            log.warning(f"⚠️ {d_p} karakter cihazı değil ve silinemedi (Busy olabilir).")

    # /dev/ptmx (Sembolik Link) - PTY ler için hayati
    ptmx_node = dev_path / "ptmx"
    subprocess.run(["rm", "-f", str(ptmx_node)], check=False)
    subprocess.run(["ln", "-snf", "pts/ptmx", str(ptmx_node)], check=False)


def mount_student_chroot(username):
    """Chroot için gerekli filesystem'leri mount et ve konfigürasyonları tazele."""
    username = _slugify(username)
    student_path = CHROOT_BASE / username

    if not student_path.exists():
        log.error(f"Mount hatası: {username} için chroot dizini yok!")
        return False

    # Konfigürasyonları senkronize et
    sync_chroot_configs(username)

    # dev, proc, sys yollarını hazırla
    dev_path = student_path / "dev"
    proc_path = student_path / "proc"
    sys_path = student_path / "sys"
    pts_path = dev_path / "pts"

    # ÖNCE TEMİZLİK (Clean Slate): Mevcut mount'ları çöz ki çakışma olmasın
    for p in [pts_path, dev_path, proc_path, sys_path]:
        subprocess.run(["umount", "-l", str(p)], check=False)

    # Dizinlerin varlığından emin ol
    for d in [dev_path, proc_path, sys_path]:
        d.mkdir(parents=True, exist_ok=True)
    pts_path.mkdir(parents=True, exist_ok=True)

    # 1. /proc ve /sys (Standard mount)
    subprocess.run(["mount", "-t", "proc", "proc", str(proc_path)], check=False)
    subprocess.run(["mount", "-t", "sysfs", "sysfs", str(sys_path)], check=False)

    # 2. /dev (Bind Mount) - LXC içinde en güvenli yöntem
    subprocess.run(["mount", "-o", "bind", "/dev", str(dev_path)], check=False)
    
    # 3. /dev/pts (Bind Mount) - LXC içinde PTY paylaşımı için kritik
    subprocess.run(["mount", "-o", "bind", "/dev/pts", str(pts_path)], check=False)
    
    # 4. KRİTİK CİHAZ DÜZELTMELERİ (V9)
    _restore_device_nodes(dev_path)
    
    # Resolv.conf tazele
    subprocess.run(["cp", "-f", "/etc/resolv.conf", str(student_path / "etc" / "resolv.conf")], check=False)

    log.info(f"✅ {username} chroot (V11) hazır ve mount edildi.")
    return True


def cleanup_stale_resources():
    """Zombie SSH oturumlarını, stale mount'ları ve kullanılmayan PTY'leri temizle."""
    log.info("🧹 Stale kaynak temizliği başlatılıyor...")
    cleaned = 0

    # 1. Zombie SSH oturumlarını bul ve öldür
    try:
        result = subprocess.run(
            ["ps", "aux"], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            # Defunct (zombie) SSH process'leri
            if "defunct" in line and ("ssh" in line or "sshd" in line):
                parts = line.split()
                pid = parts[1]
                subprocess.run(["kill", "-9", pid], check=False)
                log.info(f"  Zombie SSH process temizlendi: PID {pid}")
                cleaned += 1

            # 60 dakikadan uzun süredir idle olan chroot oturumları
            if "chroot" in line and "/bin/su" in line:
                parts = line.split()
                pid = parts[1]
                # Process yaşını kontrol et
                age_result = subprocess.run(
                    ["ps", "-o", "etimes=", "-p", pid],
                    capture_output=True, text=True
                )
                try:
                    elapsed = int(age_result.stdout.strip())
                    if elapsed > 3600:  # 1 saatten eski
                        subprocess.run(["kill", "-TERM", pid], check=False)
                        log.info(f"  Eski chroot oturumu temizlendi: PID {pid} ({elapsed}s)")
                        cleaned += 1
                except (ValueError, IndexError):
                    pass
    except Exception as e:
        log.warning(f"Process temizleme hatası: {e}")

    # 2. Stale mount'ları temizle (chroot dizini yoksa mount'u çöz)
    try:
        result = subprocess.run(
            ["mount"], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if "/home/chroot/" in line and ("/dev" in line or "/proc" in line or "/sys" in line):
                mount_point = line.split(" on ")[1].split(" type ")[0] if " on " in line else ""
                if mount_point:
                    # Chroot dizini hâlâ var mı?
                    chroot_dir = str(Path(mount_point).parent.parent) if "/dev/" in mount_point else str(Path(mount_point).parent)
                    if not Path(chroot_dir).exists() or not any(Path(chroot_dir).iterdir()):
                        subprocess.run(["umount", "-l", mount_point], check=False)
                        log.info(f"  Stale mount temizlendi: {mount_point}")
                        cleaned += 1
    except Exception as e:
        log.warning(f"Mount temizleme hatası: {e}")

    # 3. /dev/pts repairini her temizlikte çalıştır
    repair_system_pty()

    log.info(f"✅ Temizlik tamamlandı: {cleaned} kaynak temizlendi")
    return cleaned


def health_check():
    """Sistem PTY ve chroot sağlık durumunu kontrol et."""
    print("=" * 50)
    print("  Chroot Terminal Sağlık Raporu")
    print("=" * 50)

    issues = []

    # 1. PTY durumu
    try:
        with open("/proc/sys/kernel/pty/max", "r") as f:
            pty_max = int(f.read().strip())
        with open("/proc/sys/kernel/pty/nr", "r") as f:
            pty_used = int(f.read().strip())
        pct = (pty_used / pty_max * 100) if pty_max > 0 else 0
        status = "✅" if pct < 70 else ("⚠️" if pct < 90 else "❌")
        print(f"  {status} PTY Kullanımı: {pty_used}/{pty_max} ({pct:.0f}%)")
        if pct >= 70:
            issues.append(f"PTY kullanımı yüksek: {pct:.0f}%")
    except Exception as e:
        print(f"  ❌ PTY bilgisi okunamadı: {e}")
        issues.append("PTY bilgisi okunamadı")

    # 2. /dev/pts mount durumu
    if os.path.ismount("/dev/pts"):
        print("  ✅ /dev/pts mount edilmiş")
    else:
        print("  ❌ /dev/pts mount EDİLMEMİŞ!")
        issues.append("/dev/pts mount değil")

    # 3. SSH durumu
    ssh_result = subprocess.run(
        ["systemctl", "is-active", "ssh"], capture_output=True, text=True
    )
    ssh_status = ssh_result.stdout.strip()
    if ssh_status == "active":
        print("  ✅ SSH servisi çalışıyor")
    else:
        print(f"  ❌ SSH servisi: {ssh_status}")
        issues.append("SSH servisi çalışmıyor")

    # 4. Aktif SSH oturumları
    ssh_sessions = subprocess.run(
        ["ss", "-tnp", "state", "established", "sport", "=", ":22"],
        capture_output=True, text=True
    )
    session_count = len([l for l in ssh_sessions.stdout.splitlines() if l.strip() and "ESTAB" not in l[:5]])
    print(f"  📊 Aktif SSH oturumları: {session_count}")

    # 5. Disk durumu
    disk_result = subprocess.run(
        ["df", "-h", "/"], capture_output=True, text=True
    )
    for line in disk_result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 5:
            usage = parts[4].replace("%", "")
            status = "✅" if int(usage) < 85 else ("⚠️" if int(usage) < 95 else "❌")
            print(f"  {status} Disk: {parts[3]} boş ({parts[4]} kullanımda)")
            if int(usage) >= 90:
                issues.append(f"Disk {parts[4]} dolu")

    # 6. Chroot sayısı
    students = list_student_chroots()
    print(f"  📋 Toplam chroot: {len(students)}")

    # 7. Chroot mount durumları
    mount_issues = 0
    for student in students[:5]:  # İlk 5'i kontrol et
        pts_path = CHROOT_BASE / student / "dev" / "pts"
        if not os.path.ismount(str(pts_path)):
            mount_issues += 1
    if mount_issues > 0:
        print(f"  ⚠️ {mount_issues} chroot'ta /dev/pts mount eksik")
        issues.append(f"{mount_issues} chroot'ta PTY mount eksik")
    else:
        print(f"  ✅ Kontrol edilen chroot'lar mount durumu iyi")

    print("=" * 50)
    if issues:
        print(f"  ⚠️ {len(issues)} sorun bulundu:")
        for i in issues:
            print(f"    - {i}")
        print("  Çözüm: chroot-yonetici cleanup && chroot-yonetici repair")
    else:
        print("  ✅ Tüm kontroller geçti!")
    print("=" * 50)
    return len(issues)


def main():
    """Ana fonksiyon."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║     Chroot + PAM Çoklu Kullanıcı Terminal Yöneticisi     ║
║  Her öğrenci izole chroot ortamında root olabilir         ║
╚═══════════════════════════════════════════════════════════╝
""")

    import sys

    def yardim():
        print(f"  Version: {VERSION}")
        print(f"  Chroot dizini: {CHROOT_BASE}")
        print()
        print("  Komutlar:")
        print()
        print("  Kurulum & Bakim:")
        print("    init                    Ubuntu chroot sablonunu olustur (ilk kurulum)")
        print("    repair                  /dev/pts ve PTY izinlerini onar")
        print("    persist                 PTY onarimi icin systemd servisi kur")
        print("    cleanup                 Zombie process ve stale mount temizligi")
        print("    health                  Sistem saglk raporu (PTY, SSH, disk, mount)")
        print()
        print("  Ogrenci Yonetimi:")
        print("    create <user> [ad]      Yeni ogrenci chroot ortami olustur")
        print("    mount <user>            Chroot icin /dev, /proc, /sys mount et")
        print("    delete <user>           Ogrenci chroot ortamini sil")
        print("    list                    Tum chroot ortamlarini listele")
        print()
        print("  Ornekler:")
        print("    chroot-yonetici init")
        print("    chroot-yonetici create u25901001 'AHMET YILMAZ'")
        print("    chroot-yonetici health")
        print("    chroot-yonetici cleanup && chroot-yonetici repair")
        print()
        print("  DEB Paketi:")
        print("    Kurulum:   sudo dpkg -i chroot-terminal_1.1.deb")
        print("    Kaldirma:  sudo dpkg -r chroot-terminal")
        print()

    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h', 'help'):
        yardim()
        return

    command = sys.argv[1]

    if command == "init":
        setup_template()

    elif command == "repair":
        repair_system_pty()

    elif command == "persist":
        setup_persistence()

    elif command == "create":
        if len(sys.argv) < 3:
            print("Kullanim: chroot-yonetici create <username> [ad soyad]")
            return
        username = sys.argv[2]
        real_name = sys.argv[3] if len(sys.argv) > 3 else ""
        create_student_chroot(username, real_name)
        create_ssh_entry(username)

    elif command == "list":
        students = list_student_chroots()
        print("Ogrenci Chroot'lari:")
        for s in students:
            print(f"  - {s}")

    elif command == "mount":
        if len(sys.argv) < 3:
            print("Kullanim: chroot-yonetici mount <username>")
            return
        mount_student_chroot(sys.argv[2])

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Kullanim: chroot-yonetici delete <username>")
            return
        delete_student_chroot(sys.argv[2])

    elif command == "cleanup":
        cleanup_stale_resources()

    elif command == "health":
        health_check()

    elif command == "--version":
        print(f"chroot-yonetici {VERSION}")

    else:
        print(f"Bilinmeyen komut: {command}")
        print("Yardim icin: chroot-yonetici --help")


if __name__ == "__main__":
    main()
