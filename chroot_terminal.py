"""
Chroot Terminal Yöneticisi
Her öğrenci için izole chroot ortamı
"""

import subprocess
import os
from pathlib import Path
import logging

log = logging.getLogger("chroot_terminal")

CHROOT_BASE = Path("/home/chroot")
SSH_PORT = 2222


def chroot_var_mi(username: str) -> bool:
    """Öğrenci chroot ortamı var mı?"""
    chroot_path = CHROOT_BASE / username
    return chroot_path.exists() and chroot_path.is_dir()


def chroot_olustur(username: str, ad: str = "", soyad: str = "") -> bool:
    """Yeni chroot ortamı oluştur."""
    try:
        log.info(f"Chroot oluşturuluyor: {username}")

        # Yönetici script'ini çalıştır
        result = subprocess.run(
            ["python3", "chroot_yonetici.py", "create", username],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            log.info(f"✅ Chroot oluşturuldu: {username}")
            return True
        else:
            log.error(f"Chroot oluşturma hatası: {result.stderr}")
            return False

    except Exception as e:
        log.error(f"Chroot oluşturma hatası: {e}")
        return False


def chroot_ip_al(username: str) -> str:
    """SSH IP adresini döndür (host IP)."""
    # Chroot'ta ayrı IP yok, host IP döndür
    import socket
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return "127.0.0.1"


def chroot_durum(username: str) -> bool:
    """Chroot durumu kontrol et."""
    chroot_path = CHROOT_BASE / username
    if not chroot_path.exists():
        return False

    # /bin/bash var mı?
    bash_path = chroot_path / "bin" / "bash"
    return bash_path.exists()


def chroot_listesi() -> list:
    """Tüm chroot ortamlarını listele."""
    if not CHROOT_BASE.exists():
        return []

    chroots = []
    for d in CHROOT_BASE.iterdir():
        if d.is_dir() and d.name != "template":
            chroots.append({
                "username": d.name,
                "path": str(d),
                "active": chroot_durum(d.name)
            })

    return chroots


def ssh_bilgi(username: str) -> dict:
    """SSH bağlantı bilgileri."""
    return {
        "host": chroot_ip_al(username),
        "port": SSH_PORT,
        "username": username,
        "password": username,  # Kullanıcı adı ile aynı
        "command": f"ssh -p {SSH_PORT} {username}@<server_ip>"
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
