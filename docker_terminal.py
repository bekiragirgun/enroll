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
        log.debug("Docker CLI bulunamadı, muhtemelen Chroot modu kullanılıyor.")
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

    # Yeni container başlat - DNS filtering + hosts dosyası engelleme ile
    # CleanBrowsing Family Shield DNS bloke: sosyal medya, haber siteleri, vs.
    rc, cid = _docker(
        "run", "-d",
        "--name", CONTAINER_NAME,
        "--memory", "2g",
        "--cpus", "2",
        "--hostname", "linux-egitim",
        "--dns", "185.228.168.168",  # CleanBrowsing Family Shield (Primary)
        "--dns", "185.228.169.168",  # CleanBrowsing Family Shield (Secondary)
        # Sosyal medya sitelerini engelle
        "--add-host", "www.facebook.com:127.0.0.1",
        "--add-host", "facebook.com:127.0.0.1",
        "--add-host", "www.twitter.com:127.0.0.1",
        "--add-host", "twitter.com:127.0.0.1",
        "--add-host", "x.com:127.0.0.1",
        "--add-host", "www.instagram.com:127.0.0.1",
        "--add-host", "instagram.com:127.0.0.1",
        "--add-host", "www.tiktok.com:127.0.0.1",
        "--add-host", "tiktok.com:127.0.0.1",
        "--add-host", "www.youtube.com:127.0.0.1",
        "--add-host", "youtube.com:127.0.0.1",
        "--add-host", "m.youtube.com:127.0.0.1",
        "--add-host", "www.linkedin.com:127.0.0.1",
        "--add-host", "linkedin.com:127.0.0.1",
        "--add-host", "www.reddit.com:127.0.0.1",
        "--add-host", "reddit.com:127.0.0.1",
        # Haber sitelerini engelle
        "--add-host", "www.cnn.com:127.0.0.1",
        "--add-host", "cnn.com:127.0.0.1",
        "--add-host", "www.bbc.com:127.0.0.1",
        "--add-host", "bbc.com:127.0.0.1",
        "--add-host", "www.nytimes.com:127.0.0.1",
        "--add-host", "nytimes.com:127.0.0.1",
        "--add-host", "www.theguardian.com:127.0.0.1",
        "--add-host", "theguardian.com:127.0.0.1",
        # Türkçe haber sitelerini engelle
        "--add-host", "www.hurriyet.com.tr:127.0.0.1",
        "--add-host", "hurriyet.com.tr:127.0.0.1",
        "--add-host", "www.milliyet.com.tr:127.0.0.1",
        "--add-host", "milliyet.com.tr:127.0.0.1",
        "--add-host", "www.sozcu.com.tr:127.0.0.1",
        "--add-host", "sozcu.com.tr:127.0.0.1",
        "--add-host", "www.ensonhaber.com:127.0.0.1",
        "--add-host", "ensonhaber.com:127.0.0.1",
        "-p", f"{SSH_PORT}:22",
        IMAGE_NAME,
        "/bin/bash"
    )

    if rc == 0:
        log.info("Container başlatıldı: %s", CONTAINER_NAME)
        log.info("DNS filtering ve hosts dosyası engelleme aktif")
        log.info("Sosyal medya, haber siteleri ve içerik engellendi")
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
