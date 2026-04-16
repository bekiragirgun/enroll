import re
from datetime import datetime
from flask import request
from core.db import db_baglantisi

# IPv4 ve IPv6 temel doğrulama deseni
_IP_PATTERN = re.compile(
    r'^('
    r'(\d{1,3}\.){3}\d{1,3}'        # IPv4
    r'|'
    r'[0-9a-fA-F:]{2,39}'           # IPv6 (basitleştirilmiş)
    r')$'
)

def bugun():
    return datetime.now().strftime('%Y-%m-%d')

def simdi():
    return datetime.now().strftime('%H:%M:%S')

def istemci_ip():
    """Gerçek istemci IP'sini al (proxy arkasında bile çalışır)."""
    xff = request.headers.get('X-Forwarded-For')
    if xff:
        candidate = xff.split(',')[0].strip()
        # Sadece geçerli IP formatındaysa güven
        if _IP_PATTERN.match(candidate) and len(candidate) <= 45:
            return candidate
        # Geçersiz format — X-Forwarded-For'a güvenme, remote_addr kullan
    return request.remote_addr or '0.0.0.0'

def paket_hesapla():
    """Şu anki saate göre ders paketini belirle (3 paket × ~2.5 saat)."""
    from datetime import time as t
    now = datetime.now().time()
    if t(9, 0) <= now <= t(11, 35):
        return '1. Paket (09:00-11:35)'
    elif t(12, 40) <= now <= t(15, 15):
        return '2. Paket (12:40-15:15)'
    elif t(15, 25) <= now <= t(18, 0):
        return '3. Paket (15:25-18:00)'
    else:
        return '—'

# Paket string → (baslangic, bitis) zaman aralığı
_PAKET_SAATLERI = {
    '09:00': ('09:00', '11:35'),
    '12:40': ('12:40', '15:15'),
    '15:25': ('15:25', '18:00'),
}

def paket_zaman_kontrolu(paket_str: str) -> tuple:
    """Verilen paket string'i için (baslangic_str, bitis_str, gecerli_mi) döndür."""
    from datetime import time as t
    now = datetime.now().time()
    for anahtar, (bas, bit) in _PAKET_SAATLERI.items():
        if anahtar in paket_str:
            bs = t(int(bas[:2]), int(bas[3:]))
            bt = t(int(bit[:2]), int(bit[3:]))
            return bas, bit, (bs <= now <= bt)
    return '', '', False

def slayt_listesi():
    from core.config import ders_durumu
    from pathlib import Path
    import logging
    log = logging.getLogger('app')

    klasor = ders_durumu.get('slayt_klasoru', '')
    if not klasor:
        log.warning("📁 slayt_klasoru ayarı boş — Ayarlar sekmesinden tanımla.")
        return []

    yol = Path(klasor)
    if not yol.exists():
        log.warning(f"📁 Slayt klasörü bulunamadı: {klasor} (container içinden erişilemiyor — docker-compose volume mount kontrol et)")
        return []
    if not yol.is_dir():
        log.warning(f"📁 Slayt yolu bir klasör değil: {klasor}")
        return []

    dosyalar = sorted(
        f.name for f in yol.iterdir()
        if f.suffix.lower() in ('.html', '.pdf')
        and not f.name.startswith('.')
    )
    if not dosyalar:
        log.warning(f"📁 Slayt klasörü boş ({klasor}) — .html veya .pdf dosyası bulunamadı.")
    return dosyalar

def sinif_listesi():
    """Kayıtlı sınıfları döndür."""
    with db_baglantisi() as db:
        return db.execute('SELECT id, ad FROM siniflar ORDER BY ad').fetchall()
