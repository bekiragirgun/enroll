import logging
from core.db import db_baglantisi

import os
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger('app')

ders_durumu = {
    'mod':   'bekleme',   # bekleme | slayt
    'dosya': '',           # aktif slayt dosyası
    'slayt_klasoru': os.environ.get('SLIDE_KLASORU', ''),
    'terminal_url': '/terminal',
    'chroot_host': os.environ.get('CHROOT_HOST', '192.168.111.51'),
    'chroot_port': int(os.environ.get('CHROOT_SSH_PORT', '22')),
    'chroot_user': os.environ.get('CHROOT_USER', 'root'),
    'chroot_pass': os.environ.get('CHROOT_PASS', ''),
    'db_type': os.environ.get('DB_TYPE', 'sqlite'),
    'db_host': os.environ.get('DB_HOST', 'db'),
    'db_port': os.environ.get('DB_PORT', '5432'),
    'db_user': os.environ.get('DB_USER', 'postgres'),
    'db_pass': os.environ.get('DB_PASS', 'postgres_pass'),
    'db_name': os.environ.get('DB_NAME', 'ders_takip'),
    'system_host': '', # Boş ise otomatik IP kullanılır (V14.2)
    'kiosk_modu': '1',
    'cikis_izni': '0',
    'ip_kontrol': '1',
    'toplu_cikis_zamani': 0,
    'force_cikis': {}    # {numara: timestamp} — öğretmen bireysel çıkartma
}

def ayar_kaydet(anahtar, deger):
    from core.db import DBWrapper
    with db_baglantisi() as conn:
        db = DBWrapper(conn)
        db.execute("INSERT INTO ayarlar (anahtar, deger) VALUES (?, ?) ON CONFLICT (anahtar) DO UPDATE SET deger = EXCLUDED.deger" if db.db_type == 'postgres' else "INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES (?, ?)", (anahtar, str(deger)))
        conn.commit()

def ayar_getir(anahtar, varsayilan=None):
    from core.db import DBWrapper
    try:
        with db_baglantisi() as conn:
            db = DBWrapper(conn)
            satir = db.execute("SELECT deger FROM ayarlar WHERE anahtar=?", (anahtar,)).fetchone()
            # Psycopg2 vs SQLite row handling
            if satir:
                return satir[0] if isinstance(satir, tuple) else satir['deger']
            return varsayilan
    except Exception as e:
        log.error(f"Ayar getirme hatası ({anahtar}): {e}")
        return varsayilan

def ayarlari_yukle():
    """Veritabanındaki ayarları belleğe ve modüllere yükle."""
    log.info("⚙️ Ayarlar yükleniyor...")
    
    chroot_host = ayar_getir('chroot_host', os.environ.get('CHROOT_HOST', '192.168.111.51'))
    chroot_port = int(ayar_getir('chroot_port', int(os.environ.get('CHROOT_SSH_PORT', '22'))))
    terminal_url = ayar_getir('terminal_url', '/terminal')
    system_host = ayar_getir('system_host', '')
    chroot_user = ayar_getir('chroot_user', os.environ.get('CHROOT_USER', 'root'))
    chroot_pass = ayar_getir('chroot_pass', os.environ.get('CHROOT_PASS', ''))
    kiosk_modu  = ayar_getir('kiosk_modu', '1')
    cikis_izni  = ayar_getir('cikis_izni', '0')
    ip_kontrol  = ayar_getir('ip_kontrol', '1')
    ders_gunleri = ayar_getir('ders_gunleri', '1')  # 0=Pzr,1=Pzt,2=Sal,...,6=Cmt — virgülle ayrılmış
    slayt_klasoru = ayar_getir('slayt_klasoru', os.environ.get('SLIDE_KLASORU', ''))
    
    # DB Ayarları
    db_type = ayar_getir('db_type', os.environ.get('DB_TYPE', 'sqlite'))
    db_host = ayar_getir('db_host', os.environ.get('DB_HOST', 'db'))
    db_port = ayar_getir('db_port', os.environ.get('DB_PORT', '5432'))
    db_user = ayar_getir('db_user', os.environ.get('DB_USER', 'postgres'))
    db_pass = ayar_getir('db_pass', os.environ.get('DB_PASS', 'postgres_pass'))
    db_name = ayar_getir('db_name', os.environ.get('DB_NAME', 'ders_takip'))

    ders_durumu['chroot_host'] = chroot_host
    ders_durumu['chroot_port'] = chroot_port
    ders_durumu['terminal_url'] = terminal_url
    ders_durumu['system_host'] = system_host
    ders_durumu['chroot_user'] = chroot_user
    ders_durumu['chroot_pass'] = chroot_pass
    ders_durumu['kiosk_modu'] = kiosk_modu
    ders_durumu['cikis_izni'] = cikis_izni
    ders_durumu['ip_kontrol'] = ip_kontrol
    ders_durumu['slayt_klasoru'] = slayt_klasoru
    
    ders_durumu['db_type'] = db_type
    ders_durumu['db_host'] = db_host
    ders_durumu['db_port'] = db_port
    ders_durumu['db_user'] = db_user
    ders_durumu['db_pass'] = db_pass
    ders_durumu['db_name'] = db_name
    
    try:
        import chroot_terminal
        chroot_terminal.CHROOT_HOST = chroot_host
        chroot_terminal.CHROOT_SSH_PORT = chroot_port
        chroot_terminal.CHROOT_REAL_SSH_PORT = chroot_port
        chroot_terminal.CHROOT_USER = chroot_user
        chroot_terminal.CHROOT_PASS = chroot_pass
        # Script yolunu kullanıcıya göre güncelle
        if chroot_user == "root":
            chroot_terminal.CHROOT_MANAGE_SCRIPT = "/root/enroll/chroot_yonetici.py"
        else:
            chroot_terminal.CHROOT_MANAGE_SCRIPT = f"/home/{chroot_user}/enroll/chroot_yonetici.py"
        log.info(f"✅ Ayarlar yüklendi: Host={chroot_host}, Port={chroot_port}, User={chroot_user}")
    except Exception as e:
        log.error(f"❌ Modül ayarları yüklenirken hata: {e}")
