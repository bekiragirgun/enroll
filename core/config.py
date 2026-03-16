import logging
from core.db import db_baglantisi

log = logging.getLogger('app')

ders_durumu = {
    'mod':   'bekleme',   # bekleme | slayt
    'dosya': '',           # aktif slayt dosyası
    'terminal_url': '/terminal',
    'chroot_host': '192.168.111.51',
    'chroot_port': 22,
    'chroot_user': 'root',
    'chroot_pass': '',
    'system_host': '', # Boş ise otomatik IP kullanılır (V14.2)
    'kiosk_modu': '1',
    'cikis_izni': '0',
    'ip_kontrol': '1',
    'toplu_cikis_zamani': 0
}

def ayar_kaydet(anahtar, deger):
    with db_baglantisi() as db:
        db.execute("INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES (?, ?)", (anahtar, str(deger)))

def ayar_getir(anahtar, varsayilan=None):
    try:
        with db_baglantisi() as db:
            satir = db.execute("SELECT deger FROM ayarlar WHERE anahtar=?", (anahtar,)).fetchone()
            return satir['deger'] if satir else varsayilan
    except:
        return varsayilan

def ayarlari_yukle():
    """Veritabanındaki ayarları belleğe ve modüllere yükle."""
    log.info("⚙️ Ayarlar yükleniyor...")
    
    chroot_host = ayar_getir('chroot_host', '192.168.111.51')
    chroot_port = int(ayar_getir('chroot_port', 22))
    terminal_url = ayar_getir('terminal_url', '/terminal')
    system_host = ayar_getir('system_host', '')
    chroot_user = ayar_getir('chroot_user', 'root')
    chroot_pass = ayar_getir('chroot_pass', '')
    kiosk_modu  = ayar_getir('kiosk_modu', '1')
    cikis_izni  = ayar_getir('cikis_izni', '0')
    ip_kontrol  = ayar_getir('ip_kontrol', '1')
    
    ders_durumu['chroot_host'] = chroot_host
    ders_durumu['chroot_port'] = chroot_port
    ders_durumu['terminal_url'] = terminal_url
    ders_durumu['system_host'] = system_host
    ders_durumu['chroot_user'] = chroot_user
    ders_durumu['chroot_pass'] = chroot_pass
    ders_durumu['kiosk_modu'] = kiosk_modu
    ders_durumu['cikis_izni'] = cikis_izni
    ders_durumu['ip_kontrol'] = ip_kontrol
    
    try:
        import chroot_terminal
        chroot_terminal.CT_991_HOST = chroot_host
        chroot_terminal.CT_991_SSH_PORT = chroot_port
        chroot_terminal.CT_991_REAL_SSH_PORT = chroot_port
        chroot_terminal.CT_991_USER = chroot_user
        chroot_terminal.CT_991_PASS = chroot_pass
        log.info(f"✅ Ayarlar yüklendi: Host={chroot_host}, Port={chroot_port}, User={chroot_user}")
    except Exception as e:
        log.error(f"❌ Modül ayarları yüklenirken hata: {e}")
