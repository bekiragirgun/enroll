from datetime import datetime
from flask import request
from core.db import db_baglantisi

def bugun():
    return datetime.now().strftime('%Y-%m-%d')

def simdi():
    return datetime.now().strftime('%H:%M:%S')

def istemci_ip():
    """Gerçek istemci IP'sini al (proxy arkasında bile çalışır)."""
    xff = request.headers.get('X-Forwarded-For')
    if xff:
        return xff.split(',')[0].strip()
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
    
    klasor = ders_durumu.get('slayt_klasoru', '')
    if not klasor:
        return []
        
    yol = Path(klasor)
    if not yol.exists() or not yol.is_dir():
        return []
        
    dosyalar = sorted(
        f.name for f in yol.iterdir()
        if f.suffix.lower() == '.pdf'
        and not f.name.startswith('.')
    )
    return dosyalar

def sinif_listesi():
    """Kayıtlı sınıfları döndür."""
    with db_baglantisi() as db:
        return db.execute('SELECT id, ad FROM siniflar ORDER BY ad').fetchall()
