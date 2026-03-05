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
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

VERSION = "2026-03-05-CHROOT-PTY-FIX-V11"
log.info(f"🚀 Chroot Manager Script Version: {VERSION}")

# Yapılandırma
CHROOT_BASE = Path("/home/chroot")
STUDENT_TEMPLATE = CHROOT_BASE / "template"
STUDENT_GROUP = "ogrenciler"
SUDOERS_FILE = "/etc/sudoers.d/chroot-ogrenciler"


def _run(cmd, check=True):
    """Komut çalıştır."""
    log.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        log.error(f"Command failed: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result


def setup_template():
    """Şablon chroot ortamı oluştur."""
    log.info("Şablon chroot ortamı kuruluyor...")

    # ÖNCE TEMİZLİK (V11): Eski mount'ları temizle ki rm -rf veya init hata vermesin
    log.info("🧹 Eski şablon mount'ları temizleniyor...")
    for p in ["proc", "sys", "dev/pts", "dev"]:
        subprocess.run(["umount", "-l", str(STUDENT_TEMPLATE / p)], check=False)

    # Ubuntu base kur (debootstrap)
    if not STUDENT_TEMPLATE.exists():
        STUDENT_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
        # GNUPG ve Keyring'i baştan dahil et ki apt update doğrulamada hata vermesin (V8)
        _run([
            "debootstrap", "--arch=amd64", 
            "--include=gnupg,ubuntu-keyring,gpgv,ca-certificates",
            "jammy",
            str(STUDENT_TEMPLATE),
            "http://archive.ubuntu.com/ubuntu/"
        ])

    # 1. Full Repositories (V7)
    sources_list = STUDENT_TEMPLATE / "etc" / "apt" / "sources.list"
    repo_content = """
deb http://archive.ubuntu.com/ubuntu/ jammy main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ jammy-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse
"""
    sources_list.write_text(repo_content.strip() + "\n")
    log.info("📝 sources.list full depo desteği ile güncellendi.")

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

    try:
        _run(["chroot", str(STUDENT_TEMPLATE), "apt-get", "update"])
        _run(["chroot", str(STUDENT_TEMPLATE), "apt-get", "install", "-y",
              "sudo", "bash", "vim", "nano", "curl", "wget", "htop",
              "iputils-ping", "iproute2", "net-tools", "man-db",
              "gnupg", "ubuntu-keyring", "gpgv", "ca-certificates",
              "build-essential", "python3-full", "python3-pip", "git",
              "software-properties-common", "apt-transport-https", "dnsutils"])
    finally:
        log.info("🧹 Geçici filesystem'ler çözülüyor...")
        subprocess.run(["umount", "-l", str(pts)], check=False)
        subprocess.run(["umount", "-l", str(d)], check=False)
        subprocess.run(["umount", "-l", str(s)], check=False)
        subprocess.run(["umount", "-l", str(p)], check=False)
    
    # İzinler
    _run(["chmod", "1777", str(STUDENT_TEMPLATE / "tmp")])
    
    # Temizlik
    _run(["chroot", str(STUDENT_TEMPLATE), "apt-get", "clean"])

    # Öğrenci grubu oluştur
    try:
        grp.getgrnam(STUDENT_GROUP)
    except KeyError:
        _run(["groupadd", STUDENT_GROUP])

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
        # Doğrudan içeriği yaz (Host'a güvenmek yerine)
        sudo_content = f"%{STUDENT_GROUP} ALL=(ALL) NOPASSWD: ALL\n{username} ALL=(ALL) NOPASSWD: ALL\n"
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

    if student_path.exists():
        log.warning(f"{username} için chroot zaten var, konfigürasyonu güncelliyorum.")
    else:
        log.info(f"{username} için chroot oluşturuluyor...")
        # Şablondan kopyala
        import subprocess
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

    # Home dizini ve Shell ortamı (ilk kez ise)
    student_home = student_path / "home" / username
    student_home.mkdir(mode=0o755, exist_ok=True)
    
    bashrc = student_home / ".bashrc"
    if not bashrc.exists():
        bashrc.write_text(f"""
export PS1="\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ "
alias ll='ls -la'
alias ..='cd ..'
alias root='sudo su -'
export IGNOREEOF=10
echo "Kapadokya Üniversitesi Linux Laboratuvarı"
echo "Kullanıcı: {username} | Yetki: sudo su - ile root olabilirsiniz"
echo "İpucu: Ctrl+D hemen çıkış yapmaz (10 kez basılmalıdır)."
echo ""
""")

    # .profile
    profile = student_home / ".profile"
    if not profile.exists():
        profile.write_text("""
if [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.bashrc" ]; then
        . "$HOME/.bashrc"
    fi
fi
""")

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

    # SSH config'e ForceCommand ekle (V10 - Sticky Shell)
    ssh_config = Path("/etc/ssh/sshd_config")
    # Önemli: Chroot dizini ve su komutunu bir döngüye al
    force_command = f"Match User {username}\n    ForceCommand /bin/bash -c \"while true; do sudo /usr/sbin/chroot {student_path} /bin/su - {username}; echo 'Oturum kapatılamaz, yeniden başlatılıyor...'; sleep 1; done\"\n"

    # SSH config'e ekle
    ssh_config_text = ssh_config.read_text()
    if force_command not in ssh_config_text:
        with open(ssh_config, 'a') as f:
            f.write(force_command)

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

    # Önce mount'ları unmount et
    subprocess.run(["umount", f"{student_path}/dev"], check=False)
    subprocess.run(["umount", f"{student_path}/proc"], check=False)
    subprocess.run(["umount", f"{student_path}/sys"], check=False)

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
        
        # Eğer zaten doğru bir karakter cihazıysa dokunma, sadece izinleri tazele
        if d_p.exists() and d_p.is_char_device():
            subprocess.run(["chmod", "666", str(d_p)], check=False)
            continue

        # Değilse, Önce Silmeyi Dene (Eğer busy değilse)
        subprocess.run(["rm", "-f", str(d_p)], check=False)
        
        # 1. mknod dene (Privileged modda çalışır)
        res = subprocess.run(["mknod", "-m", "666", str(d_p)] + mode.split(), capture_output=True)
        
        # 2. mknod başarısızsa (LXC Unprivileged), Host'tan BIND-MOUNT yap (En sağlam yöntem)
        if res.returncode != 0:
            if not d_p.exists():
                subprocess.run(["touch", str(d_p)], check=False)
            subprocess.run(["mount", "-o", "bind", f"/dev/{dev_name}", str(d_p)], check=False)
            subprocess.run(["chmod", "666", str(d_p)], check=False)

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


def main():
    """Ana fonksiyon."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║     Chroot + PAM Çoklu Kullanıcı Terminal Yöneticisi     ║
║  Her öğrenci izole chroot ortamında root olabilir         ║
╚═══════════════════════════════════════════════════════════╝
""")

    import sys

    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  python3 chroot_yonetici.py init          # Şablonu kur")
        print("  python3 chroot_yonetici.py create <user> # Öğrenci ekle")
        print("  python3 chroot_yonetici.py list          # Listele")
        print("  python3 chroot_yonetici.py mount <user>  # Mount et")
        print("  python3 chroot_yonetici.py delete <user> # Sil")
        return

    command = sys.argv[1]

    if command == "init":
        setup_template()

    elif command == "create":
        if len(sys.argv) < 3:
            print("Kullanıcı adı gerekli")
            return
        username = sys.argv[2]
        real_name = sys.argv[3] if len(sys.argv) > 3 else ""
        create_student_chroot(username, real_name)
        create_ssh_entry(username)

    elif command == "list":
        students = list_student_chroots()
        print("Öğrenci Chroot'ları:")
        for s in students:
            print(f"  - {s}")

    elif command == "mount":
        if len(sys.argv) < 3:
            print("Kullanıcı adı gerekli")
            return
        mount_student_chroot(sys.argv[2])

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Kullanıcı adı gerekli")
            return
        delete_student_chroot(sys.argv[2])

    else:
        print(f"Bilinmeyen komut: {command}")


if __name__ == "__main__":
    main()
