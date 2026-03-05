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
    """Host yerel mi kontrol et."""
    return host in ["localhost", "127.0.0.1", "::1"] or host == Path("/etc/hostname").read_text().strip() if Path("/etc/hostname").exists() else False

def _ct991_exec(command: list) -> subprocess.CompletedProcess:
    """CT 991 üzerinde komut çalıştır (Local veya SSH üzerinden)."""
    
    if _is_local(CT_991_HOST):
        log.debug(f"Executing locally: {' '.join(command)}")
        return subprocess.run(command, capture_output=True, text=True)

    # Chroot komutları genellikle root yetkisi gerektirir
    final_command = command
    if CT_991_USER != "root":
        final_command = ["sudo"] + command

    # SSH üzerinden bağlat
    ssh_cmd = [
        "ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes" if not CT_991_PASS else "BatchMode=no",
        "-p", str(CT_991_REAL_SSH_PORT),
        f"{CT_991_USER}@{CT_991_HOST}"
    ]
    
    # Şifre varsa sshpass kullan
    if CT_991_PASS:
        ssh_cmd = ["sshpass", "-p", CT_991_PASS] + ssh_cmd

    ssh_cmd += final_command
    
    log.debug(f"Remoting (PCT 991): {' '.join(ssh_cmd)}")
    result = subprocess.run(ssh_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        log.error(f"Remote command failed: {' '.join(command)}")
        if result.stderr: log.error(f"Stderr: {result.stderr.strip()}")
    
    return result


def sync_manager_script():
    """Local chroot_yonetici.py dosyasını PCT 991'e senkronize et."""
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
        return True
    except Exception as e:
        log.error(f"Senkronizasyon hatası: {e}")
        return False


def chroot_var_mi(username: str) -> bool:
    """Öğrenci chroot ortamı var mı?"""
    # Script güncel olduğundan emin ol
    sync_manager_script()
    
    username = _slugify(username)
    result = _ct991_exec([PYTHON_PATH, CHROOT_MANAGE_SCRIPT, "list"])
    if result.returncode != 0:
        log.error(f"Chroot listesi alınamadı: {result.stderr}")
        return False

    output = result.stdout.strip()
    # "  - ogrenci1" formatını temizle
    chroots = [line.strip().replace("- ", "").strip() for line in output.split('\n')]
    return username in chroots


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
