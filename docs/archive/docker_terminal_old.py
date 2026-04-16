"""
Docker Terminal Yöneticisi
Her öğrenci için izole Docker container başlatır/durdurur.
subprocess ile docker CLI kullanır (ek bağımlılık yok).
"""

import subprocess
import logging
import threading

IMAGE_NAME = "ogrenci-terminal:latest"
CONTAINER_PREFIX = "terminal-"

# Aktif container'lar: {numara: container_id}
aktif_konteynerler = {}
_lock = threading.Lock()

log = logging.getLogger("docker_terminal")


def _docker(*args, timeout=30):
    """Docker CLI komutu çalıştır, (returncode, stdout) döndür."""
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
        log.error("Docker bulunamadı! Docker kurulu mu?")
        return -1, ""


def konteyner_baslat(numara: str) -> str:
    """Öğrenci için container başlat. Container ID döndürür."""
    isim = CONTAINER_PREFIX + numara

    with _lock:
        # Zaten çalışıyor mu?
        if numara in aktif_konteynerler:
            rc, state = _docker("inspect", "-f", "{{.State.Running}}", isim)
            if rc == 0 and state == "true":
                return aktif_konteynerler[numara]
            else:
                # Ölmüş, temizle
                _docker("rm", "-f", isim)
                del aktif_konteynerler[numara]

        # Aynı isimde eski container varsa sil
        _docker("rm", "-f", isim)

        # Yeni container başlat
        rc, cid = _docker(
            "run", "-d",
            "--name", isim,
            "--memory=256m",
            "--cpus=0.5",
            "--hostname", f"lab-{numara}",
            "-it",
            IMAGE_NAME,
            "/bin/bash"
        )

        if rc == 0 and cid:
            aktif_konteynerler[numara] = cid[:12]
            log.info("Container başlatıldı: %s → %s", numara, cid[:12])
            return cid[:12]
        else:
            log.error("Container başlatılamadı: numara=%s", numara)
            return ""


def konteyner_durdur(numara: str) -> bool:
    """Öğrenci container'ını durdur ve sil."""
    isim = CONTAINER_PREFIX + numara
    with _lock:
        rc, _ = _docker("stop", "-t", "3", isim)
        _docker("rm", "-f", isim)
        aktif_konteynerler.pop(numara, None)
    return rc == 0


def konteyner_temizle():
    """Tüm öğrenci container'larını durdur (shutdown sırasında çağır)."""
    rc, cikti = _docker("ps", "-a", "--filter", f"name={CONTAINER_PREFIX}",
                        "--format", "{{.Names}}")
    if rc == 0 and cikti:
        for isim in cikti.splitlines():
            _docker("stop", "-t", "2", isim)
            _docker("rm", "-f", isim)
    with _lock:
        aktif_konteynerler.clear()
    log.info("Tüm öğrenci container'ları temizlendi.")


def konteyner_listesi() -> list:
    """Aktif öğrenci container listesi."""
    rc, cikti = _docker("ps", "--filter", f"name={CONTAINER_PREFIX}",
                        "--format", "{{.Names}}\t{{.Status}}")
    if rc != 0 or not cikti:
        return []
    sonuc = []
    for satir in cikti.splitlines():
        parcalar = satir.split("\t")
        if len(parcalar) >= 2:
            numara = parcalar[0].replace(CONTAINER_PREFIX, "")
            sonuc.append({"numara": numara, "durum": parcalar[1]})
    return sonuc


def image_var_mi() -> bool:
    """ogrenci-terminal:latest imajı mevcut mu?"""
    rc, _ = _docker("image", "inspect", IMAGE_NAME)
    return rc == 0
