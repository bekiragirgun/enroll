from datetime import datetime
from flask import request
from core.paths import SLAYT_DIR
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

def slayt_listesi():
    if not SLAYT_DIR.exists():
        return []
    dosyalar = sorted(
        f.name for f in SLAYT_DIR.iterdir()
        if f.suffix == '.html'
        and '_test' not in f.name
        and '_analyzed' not in f.name
    )
    return dosyalar

def sinif_listesi():
    """Kayıtlı sınıfları döndür."""
    with db_baglantisi() as db:
        return db.execute('SELECT id, ad FROM siniflar ORDER BY ad').fetchall()
