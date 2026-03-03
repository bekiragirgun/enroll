"""
Docker Terminal Yöneticisi - TEK VERSİYON
Tek container, çoklu kullanıcı
"""

import subprocess
import logging

IMAGE_NAME = "ogrenci-terminal:latest"
CONTAINER_NAME = "linux-lab"
SSH_PORT = 2222

log = logging.getLogger("docker_terminal")


def _docker(*args, timeout=30):
    """Docker CLI komutu çalıştır."""
    try:
        r = subprocess.run(
            ["docker"] + list(args),
            capture_output=True, text=True, timeout=timeout
        )
        return r.returncode, r.stdout.strip()
    except subprocess.TimeoutExpired:
        log.error("Docker komutu zaman aşımı: %s", args)
        return -1, ""
    except FileNotFoundError:
        log.error("Docker bulunamadı!")
        return -1, ""


def container_baslat():
    """Tek container başlat (sistem için bir kez)."""
    # Container var mı?
    rc, _ = _docker("inspect", "-f", "{{.State.Running}}", CONTAINER_NAME)

    if rc == 0:
        # Zaten çalışıyor
        return True

    # Eski container varsa temizle
    _docker("rm", "-f", CONTAINER_NAME)

    # Yeni container başlat
    rc, cid = _docker(
        "run", "-d",
        "--name", CONTAINER_NAME,
        "--memory", "2g",
        "--cpus", "2",
        "--hostname", "linux-egitim",
        "-p", f"{SSH_PORT}:22",
        IMAGE_NAME,
        "/bin/bash"
    )

    if rc == 0:
        log.info("Container başlatıldı: %s", CONTAINER_NAME)
        return True
    else:
        log.error("Container başlatılamadı!")
        return False


def kullanici_olustur(username, ad="", soyad=""):
    """Container'da yeni kullanıcı oluştur."""
    # Kullanıcı zaten var mı?
    rc, _ = _docker("exec", CONTAINER_NAME, "id", username)
    if rc == 0:
        log.info("Kullanıcı zaten var: %s", username)
        return True

    # Kullanıcı oluştur
    sifre = username  # Kullanıcı adı aynı zamanda şifre

    rc, _ = _docker(
        "exec", CONTAINER_NAME,
        "useradd", "-m", "-s", "/bin/bash",
        f"-p", f"$(openssl passwd -1 {sifre})",
        username
    )

    if rc == 0:
        # Ev dizini oluştur
        _docker(
            "exec", CONTAINER_NAME,
            "mkdir", "-p", f"/home/{username}/{egitim,pratik,testler,loglar}",
            "&&", "chown", "-R", f"{username}:{username}", f"/home/{username}"
        )

        # Bash yapılandırması
        bashrc = f'/home/{username}/.bashrc'
        ps1 = "\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ "

        _docker(
            "exec", CONTAINER_NAME,
            "sh", "-c",
            f'echo "export PS1=\'{ps1}\'" >> {bashrc} && echo "alias ll=\'ls -la\'" >> {bashrc}'
        )

        log.info("Kullanıcı oluşturuldu: %s", username)
        return True
    else:
        log.error("Kullanıcı oluşturulamadı: %s", username)
        return False


def container_ip_al():
    """Container IP adresini al."""
    rc, ip = _docker(
        "inspect", "-f",
        "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
        CONTAINER_NAME
    )

    if rc == 0 and ip:
        return ip

    # Bridge network yoksa localhost dön
    return "127.0.0.1"


def container_durum():
    """Container durumunu döndür."""
    rc, output = _docker("inspect", "-f", "{{.State.Running}}", CONTAINER_NAME)
    return rc == 0 and output == "true"


def image_var_mi():
    """Docker imajı mevcut mu?"""
    rc, _ = _docker("image", "inspect", IMAGE_NAME)
    return rc == 0


if __name__ == "__main__":
    print("Container başlatılıyor...")
    if container_baslat():
        print("✅ Container hazır!")
        print(f"IP: {container_ip_al()}")
    else:
        print("❌ Hata!")
