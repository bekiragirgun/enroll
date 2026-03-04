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

    # Ubuntu base kur (debootstrap)
    if not STUDENT_TEMPLATE.exists():
        STUDENT_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
        _run([
            "debootstrap", "--arch=amd64", "jammy",
            str(STUDENT_TEMPLATE),
            "http://archive.ubuntu.com/ubuntu/"
        ])

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

    # Temel paketler
    _run(["chroot", str(STUDENT_TEMPLATE), "apt-get", "update"])
    _run(["chroot", str(STUDENT_TEMPLATE), "apt-get", "install", "-y",
          "sudo", "bash", "vim", "nano", "curl", "wget", "htop",
          "iputils-ping", "iproute2", "net-tools", "man-db"])

    # Öğrenci grubu oluştur
    try:
        grp.getgrnam(STUDENT_GROUP)
    except KeyError:
        _run(["groupadd", STUDENT_GROUP])

    log.info("✅ Şablon chroot hazır!")


def create_student_chroot(username, real_name=""):
    """Öğrenci için chroot ortamı oluştur."""
    student_path = CHROOT_BASE / username

    if student_path.exists():
        log.warning(f"{username} için chroot zaten var")
        # Mevcut chroot'u tamir etmeyi deneyelim (grup ve profile eksikse)
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
    # Dev, Proc, Sys dizinlerini oluştur (Mount için)
    for d in ["dev", "proc", "sys", "var/run"]:
        (student_path / d).mkdir(parents=True, exist_ok=True)

    # Host sistemde kullanıcıyı oluştur (SSH için)
    try:
        try:
            grp.getgrnam(STUDENT_GROUP)
        except KeyError:
            _run(["groupadd", STUDENT_GROUP])
    except KeyError:
        # --badname: Sayısal kullanıcı adlarına (örn: 123) izin ver
        _run(["useradd", "--badname", "-m", "-s", "/bin/bash", "-G", STUDENT_GROUP, "-c", real_name, username])

    # Host üzerindeki gerçek UID ve GID'leri al
    user_info = pwd.getpwnam(username)
    group_info = grp.getgrnam(STUDENT_GROUP)
    REAL_UID = user_info.pw_uid
    REAL_GID = group_info.gr_gid

    # Chroot içinde konfigürasyon dosyaları
    passwd_file = student_path / "etc" / "passwd"
    shadow_file = student_path / "etc" / "shadow"
    group_file = student_path / "etc" / "group"

    # Chroot içinde grubun varlığından emin ol (cannot find name for group ID 1000 hatası için)
    try:
        group_content = group_file.read_text() if group_file.exists() else ""
        group_line = f"{STUDENT_GROUP}:x:{REAL_GID}:{username}\n"
        if f"{STUDENT_GROUP}:x:{REAL_GID}:" not in group_content:
            with open(group_file, 'a') as f:
                f.write(group_line)
    except Exception as e:
        log.error(f"Grup dosyası güncelleme hatası: {e}")
 
    # Chroot içinde kullanıcı girişi
    try:
        passwd_content = passwd_file.read_text() if passwd_file.exists() else ""
        passwd_line = f"{username}:x:{REAL_UID}:{REAL_GID}:{real_name}:/home/{username}:/bin/bash\n"
        if f"{username}:x:{REAL_UID}:" not in passwd_content:
            with open(passwd_file, 'a') as f:
                f.write(passwd_line)
    except Exception as e:
        log.error(f"Passwd dosyası güncelleme hatası: {e}")

    # Host sistemdeki shadow hash'ini kopyala (Shadow dosyası yoksa oluştur)
    if not shadow_file.exists(): shadow_file.write_text("")
    result = subprocess.run(["grep", f"^{username}:", "/etc/shadow"], capture_output=True, text=True)
    if result.returncode == 0:
        shadow_content = shadow_file.read_text()
        if f"{username}:" not in shadow_content:
            with open(shadow_file, 'a') as f:
                f.write(result.stdout.strip() + '\n')
    _run(["chmod", "0600", str(shadow_file)])

    # Hostname ve /etc/hosts (Sudo hatası için önemli)
    hosts_file = student_path / "etc" / "hosts"
    hosts_content = "127.0.0.1\tlocalhost\n127.0.1.1\togrenci-vm\n"
    hosts_file.write_text(hosts_content)
    (student_path / "etc" / "hostname").write_text("ogrenci-vm\n")

    # Home dizini ve Shell ortamı
    student_home = student_path / "home" / username
    student_home.mkdir(mode=0o755, exist_ok=True)
    
    # .bashrc
    (student_home / ".bashrc").write_text(f"""
export PS1="\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ "
alias ll='ls -la'
alias ..='cd ..'
alias root='sudo su -'
echo "Kapadokya Üniversitesi Linux Laboratuvarı"
echo "Kullanıcı: {username} | Yetki: sudo su - ile root olabilirsiniz"
echo ""
""")

    # .profile (Login shell desteği için)
    (student_home / ".profile").write_text("""
if [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.bashrc" ]; then
        . "$HOME/.bashrc"
    fi
fi
""")

    # Chown gerçek UID/GID (Host sistemdeki ile senkron)
    _run(["chown", "-R", f"{REAL_UID}:{REAL_GID}", str(student_home)])

    # Sudoers
    sudoers = student_path / "etc" / "sudoers"
    sudoers.write_text(f"{username} ALL=(ALL:ALL) NOPASSWD:ALL\n")
    _run(["chmod", "0440", str(sudoers)])

    log.info(f"✅ {username} chroot ortamı yapılandırıldı.")
    return True


def create_ssh_entry(username):
    """SSH ve sudoers yapılandırması."""
    # Kullanıcının shell'i /bin/bash olsun (chrootlogin değil)
    _run([
        "usermod", "-s", "/bin/bash", username
    ])

    # Sudoers'a chroot yetkisi ekle
    sudoers_line = f"{username} ALL=(ALL) NOPASSWD: /usr/sbin/chroot\n"
    sudoers_file = Path("/etc/sudoers.d/chroot-ogrenciler")

    # Sudoers dosyasına ekle (tekrarı önle)
    existing_sudoers = sudoers_file.read_text() if sudoers_file.exists() else ""
    if sudoers_line not in existing_sudoers:
        with open(sudoers_file, 'a') as f:
            f.write(sudoers_line)
        _run(["chmod", "0440", str(sudoers_file)])

    # SSH config'e ForceCommand ekle
    ssh_config = Path("/etc/ssh/sshd_config")
    force_command = f"Match User {username}\n    ForceCommand sudo /usr/sbin/chroot {CHROOT_BASE}/{username} /bin/su - {username}\n"

    # SSH config'e ekle (tekrarı önle)
    ssh_config_text = ssh_config.read_text()
    if force_command not in ssh_config_text:
        with open(ssh_config, 'a') as f:
            f.write(force_command)

    # chrootlogin script'ini chroot içine kopyala
    chrootlogin_src = Path("/usr/sbin/chrootlogin")
    chrootlogin_dst = student_path / "usr" / "sbin" / "chrootlogin"
    if chrootlogin_src.exists():
        subprocess.run(["cp", str(chrootlogin_src), str(chrootlogin_dst)], check=False)
        subprocess.run(["chmod", "+x", str(chrootlogin_dst)], check=False)

    # SSH'yi restart et
    _run(["systemctl", "restart", "sshd"])

    log.info(f"✅ {username} SSH/Sudoers yapılandırması tamam")


def list_student_chroots():
    """Tüm öğrenci chroot'larını listele."""
    if not CHROOT_BASE.exists():
        return []

    return [d.name for d in CHROOT_BASE.iterdir() if d.is_dir() and d.name != "template"]


def delete_student_chroot(username):
    """Öğrenci chroot'unu sil."""
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


def mount_student_chroot(username):
    """Chroot için gerekli filesystem'leri mount et."""
    student_path = CHROOT_BASE / username

    # dev, proc, sys mount et
    dev_path = student_path / "dev"
    proc_path = student_path / "proc"
    sys_path = student_path / "sys"

    dev_path.mkdir(exist_ok=True)
    proc_path.mkdir(exist_ok=True)
    sys_path.mkdir(exist_ok=True)

    subprocess.run(["mount", "-o", "bind", "/dev", str(dev_path)], check=False)
    subprocess.run(["mount", "-o", "bind", "/dev/pts", str(student_path / "dev" / "pts")], check=False)
    subprocess.run(["mount", "-t", "proc", "proc", str(proc_path)], check=False)
    subprocess.run(["mount", "-o", "bind", "/sys", str(sys_path)], check=False)
    
    # Resolv.conf kopyala (İnternet erişimi için)
    subprocess.run(["cp", "/etc/resolv.conf", str(student_path / "etc" / "resolv.conf")], check=False)

    log.info(f"✅ {username} chroot filesystem'ları mount edildi.")


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
        create_student_chroot(sys.argv[2])
        create_ssh_entry(sys.argv[2])

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
