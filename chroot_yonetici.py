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
        return False

    log.info(f"{username} için chroot oluşturuluyor...")

    # Şablondan kopyala (rsync ile, device'leri hariç tutarak)
    import subprocess
    result = subprocess.run(
        ["rsync", "-a", "--exclude=/dev/*", "--exclude=/proc/*",
               "--exclude=/sys/*", "--exclude=/var/run/*",
               f"{STUDENT_TEMPLATE}/", f"{student_path}/"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        log.error(f"Chroot kopyalama hatası: {result.stderr}")
        return False

    # Gerekli dizinleri manuel oluştur (rsync bunları kopyalamaz)
    essential_dirs = [
        student_path / "dev",
        student_path / "proc",
        student_path / "sys",
        student_path / "var/run",
    ]

    for d in essential_dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Temel device file'lerini oluştur
    devices = ["null", "zero", "full", "random", "tty", "urandom"]
    for device in devices:
        dev_path = student_path / "dev" / device
        if not dev_path.exists():
            subprocess.run(["mknod", "-m", "666", str(dev_path), "c", "1", "5"],
                           check=False)

    # Kullanıcı oluştur (host sistemi)
    try:
        # Grubun varlığından emin ol
        try:
            grp.getgrnam(STUDENT_GROUP)
        except KeyError:
            _run(["groupadd", STUDENT_GROUP])
            
        pwd.getpwnam(username)
    except KeyError:
        _run([
            "useradd", "-m", "-s", "/bin/bash",
            "-G", STUDENT_GROUP,
            "-c", real_name,
            username
        ])

    # Chroot içinde kullanıcı oluştur
    passwd_file = student_path / "etc" / "passwd"
    shadow_file = student_path / "etc" / "shadow"
    group_file = student_path / "etc" / "group"

    # Kullanıcı ekle (chroot içinde)
    with open(passwd_file, 'a') as f:
        f.write(f"{username}:x:1000:1000:{real_name}:/home/{username}:/bin/bash\n")

    # Parola (kullanıcı adı ile aynı) - host sistemdeki shadow'dan al
    # Önce host sistemde kullanıcının hash'ini al
    result = subprocess.run(
        ["grep", f"^{username}:", "/etc/shadow"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        # Host sistemdeki hash'i chroot içine kopyala
        host_shadow_entry = result.stdout.strip()
        with open(shadow_file, 'a') as f:
            f.write(host_shadow_entry + '\n')
    else:
        # Yedek: openssl ile hash oluştur
        hashed_pw = subprocess.run(
            ["openssl", "passwd", "-1", username],
            capture_output=True, text=True
        ).stdout.strip()
        with open(shadow_file, 'a') as f:
            f.write(f"{username}:{hashed_pw}:18000:0:99999:7:::\n")

    # Home dizini oluştur
    student_home = student_path / "home" / username
    student_home.mkdir(mode=0o755, exist_ok=True)
    _run(["chown", f"{username}:{username}", str(student_home)])

    # .bashrc yapılandırması
    bashrc = student_home / ".bashrc"
    bashrc.write_text("""
export PS1="\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ "
alias ll='ls -la'
alias ..='cd ..'
alias root='sudo su -'
echo "Özel Linux Ortamı - sudo su - ile root olabilirsiniz"
echo ""
""")

    # Sudoers yapılandırması (chroot içinde)
    sudoers = student_path / "etc" / "sudoers"
    sudoers.write_text(f"""
# Öğrenci kendi chroot'unda root olabilir
{username} ALL=(ALL:ALL) NOPASSWD:ALL
""")

    _run(["chmod", "0440", str(sudoers)])

    log.info(f"✅ {username} için chroot oluşturuldu!")
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
    subprocess.run(["mount", "-t", "proc", "proc", str(proc_path)], check=False)
    subprocess.run(["mount", "-o", "bind", "/sys", str(sys_path)], check=False)


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
