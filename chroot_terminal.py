"""
Chroot Terminal Yöneticisi
CT 991 (ogrenci-vm) üzerindeki chroot ortamlarını yönetir
"""

import subprocess
import os
from pathlib import Path
import logging
import requests

log = logging.getLogger("chroot_terminal")

# CT 991 (ogrenci-vm) bilgileri
CT_991_HOST = "192.168.111.51"  # CT 991 IP adresi
CT_991_SSH_PORT = 2222
CHROOT_MANAGE_SCRIPT = "/root/enroll/chroot_yonetici.py"


def _ct991_exec(command: list) -> subprocess.CompletedProcess:
    """CT 991 üzerinde komut çalıştır."""
    full_command = ["pct", "exec", "991"] + command
    return subprocess.run(full_command, capture_output=True, text=True)


def chroot_var_mi(username: str) -> bool:
    """Öğrenci chroot ortamı var mı?"""
    result = _ct991_exec(["python3", CHROOT_MANAGE_SCRIPT, "list"])
    if result.returncode != 0:
        log.error(f"Chroot listesi alınamadı: {result.stderr}")
        return False

    chroots = result.stdout.strip().split('\n')
    return username in chroots


def chroot_olustur(username: str, ad: str = "", soyad: str = "") -> bool:
    """Yeni chroot ortamı oluştur."""
    try:
        log.info(f"Chroot oluşturuluyor: {username}")

        # CT 991 üzerinde yönetici script'ini çalıştır
        result = _ct991_exec(
            ["python3", CHROOT_MANAGE_SCRIPT, "create", username]
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
    """SSH IP adresini döndür (CT 991 IP)."""
    return CT_991_HOST


def chroot_durum(username: str) -> bool:
    """Chroot durumu kontrol et."""
    return chroot_var_mi(username)


def chroot_listesi() -> list:
    """Tüm chroot ortamlarını listele."""
    result = _ct991_exec(["python3", CHROOT_MANAGE_SCRIPT, "list"])

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
