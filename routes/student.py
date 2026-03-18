from flask import Blueprint, render_template, request, redirect, url_for, session, Response
from core.db import db_baglantisi
from core.config import ayar_getir, ders_durumu
from core.utils import bugun, simdi, istemci_ip, paket_hesapla, sinif_listesi
from core.security import seb_gerekli
import threading
import logging
import time as _time

log = logging.getLogger('app')
student_bp = Blueprint('student_bp', __name__)

PAKET_SECENEKLERI = [
    '1. Paket (09:00-11:35)',
    '2. Paket (12:40-15:15)',
    '3. Paket (15:25-18:00)',
]

@student_bp.route('/')
@seb_gerekli
def ana():
    """Ana sayfa - Giriş formu veya Öğrenci Paneli."""
    if session.get('numara'):
        tarih = bugun()
        with db_baglantisi() as db:
            yoklama = db.execute(
                'SELECT ad_soyad, saat, paket FROM yoklama WHERE tarih=? AND numara=? ORDER BY id DESC LIMIT 1',
                (tarih, session['numara'])
            ).fetchone()
            
            if yoklama:
                if not session.get('ad') or not session.get('soyad'):
                    ogrenci = db.execute('SELECT ad, soyad FROM ogrenciler WHERE numara=?', (session['numara'],)).fetchone()
                    if ogrenci:
                        session['ad'] = ogrenci['ad']
                        session['soyad'] = ogrenci['soyad']

                return render_template('ogrenci_ana.html', 
                                       ad_soyad=yoklama['ad_soyad'], 
                                       saat=yoklama['saat'], 
                                       paket=yoklama['paket'],
                                       tekrar_giris=True)

    siniflar = sinif_listesi()
    return render_template('login.html', siniflar=siniflar, paket_varsayilan=paket_hesapla(), paket_secenekleri=PAKET_SECENEKLERI)

@student_bp.route('/giris', methods=['POST'])
@seb_gerekli
def giris():
    sinif_id  = request.form.get('sinif_id', '').strip()
    ad_soyad  = request.form.get('ad_soyad', '').strip().upper()
    numara    = request.form.get('numara', '').strip()
    ders_paketi = request.form.get('ders_paketi', '').strip()
    siniflar = sinif_listesi()

    def hata_goster(mesaj):
        return render_template('login.html',
                               hata=mesaj,
                               siniflar=siniflar,
                               paket_secenekleri=PAKET_SECENEKLERI,
                               paket_varsayilan=ders_paketi or paket_hesapla())

    if not sinif_id or not ad_soyad or not numara or not ders_paketi:
        return hata_goster('Lütfen tüm alanları doldurun.')

    if ders_paketi not in PAKET_SECENEKLERI:
        ders_paketi = paket_hesapla()

    with db_baglantisi() as db:
        ogrenci = db.execute(
            'SELECT ad, soyad, numara FROM ogrenciler WHERE UPPER(ad || " " || soyad)=? AND sinif_id=?',
            (ad_soyad, sinif_id)
        ).fetchone()

    if not ogrenci:
        return hata_goster('Bu öğrenci numarası seçili sınıfa kayıtlı değil.')

    if ogrenci['numara'] != numara:
        return hata_goster('Hatalı şifre!')

    saat      = simdi()
    tarih     = bugun()
    istemci   = istemci_ip()

    with db_baglantisi() as db:
        sinif_row = db.execute('SELECT ad FROM siniflar WHERE id=?', (sinif_id,)).fetchone()
        sinif_ad  = sinif_row['ad'] if sinif_row else ''

        # IP kontrol ayarı açıksa fraud kontrolü yap
        if ders_durumu.get('ip_kontrol', '1') == '1':
            ip_var_mi = db.execute(
                "SELECT DISTINCT numara FROM yoklama WHERE tarih=? AND ip=? AND paket=? AND kaynak='web'",
                (tarih, istemci, ders_paketi)
            ).fetchall()

            if ip_var_mi:
                ip_numaralar = {row['numara'] for row in ip_var_mi}
                if numara not in ip_numaralar and len(ip_numaralar) > 0:
                    db.execute(
                        'INSERT INTO sahte_giris_log '
                        '(tarih, saat, ip, gercek_numara, gercek_ad, denenen_numara, denenen_ad, sinif) '
                        'VALUES (?,?,?,?,?,?,?,?)',
                        (tarih, saat, istemci, list(ip_numaralar)[0], 'Aynı IP', numara, ad_soyad, sinif_ad)
                    )
                    db.commit()
                    return hata_goster(f'Bu cihazdan bugün başka öğrenci numaraları girildi: {", ".join(ip_numaralar)}. Başkası adına giriş yapılamaz.')

        var_mi = db.execute(
            'SELECT id, saat FROM yoklama WHERE tarih=? AND numara=? AND paket=?',
            (tarih, numara, ders_paketi)
        ).fetchone()
        
        if var_mi:
            session['numara'] = numara
            session['ad'] = ogrenci['ad']
            session['soyad'] = ogrenci['soyad']
            session['giris_zamani'] = _time.time()
            return redirect(url_for('student_bp.ana'))

        db.execute(
            'INSERT INTO yoklama (tarih, ad_soyad, numara, saat, sinif, paket, ip, kaynak) '
            'VALUES (?,?,?,?,?,?,?,?)',
            (tarih, ad_soyad, numara, saat, sinif_ad, ders_paketi, istemci, 'web')
        )
        db.commit()

    session['numara'] = numara
    session['ad'] = ogrenci['ad']
    session['soyad'] = ogrenci['soyad']
    session['giris_zamani'] = _time.time()

    try:
        from chroot_terminal import chroot_var_mi, chroot_olustur
        if not chroot_var_mi(numara):
            log.info(f"Oturum açıldı, chroot otomatik oluşturuluyor: {numara}")
            threading.Thread(target=chroot_olustur, args=(numara,)).start()
    except Exception as e:
        log.error(f"Otomatik chroot oluşturma hatası: {e}")

    return redirect(url_for('student_bp.ana'))

@student_bp.route('/seb-quit')
def seb_quit():
    """SEB quitURL endpoint — SEB bu URL'ye navigate edildiğinde kendini kapatır."""
    from flask import session
    numara = session.get('numara', 'bilinmiyor')
    session.clear()
    return Response(
        f"""<!DOCTYPE html>
<html><head><title>SEB Çıkış</title></head>
<body style="background:#000;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;font-family:sans-serif;">
<h2>SEB kapatılıyor... ({numara})</h2>
</body></html>""",
        mimetype='text/html'
    )

@student_bp.route('/seb-gerekli')
def seb_gerekli_sayfasi():
    return render_template('seb_gerekli.html')

@student_bp.route('/seb-config')
def seb_config():
    system_host = ayar_getir('system_host', '')
    if system_host:
        if not system_host.startswith('http'):
            url = f"http://{system_host}/"
        else:
            url = system_host
            if not url.endswith('/'): url += '/'
    else:
        url = request.host_url
        
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>originatorVersion</key>
    <string>SEB_OSX_3.3.2_52D4</string>
    <key>startURL</key>
    <string>{url}</string>
    <key>allowVirtualMachine</key>
    <true/>
    <key>sendBrowserExamKey</key>
    <true/>
    <key>browserWindowAllowReload</key>
    <true/>
    <key>enableZoomPage</key>
    <true/>
    <key>allowSpellCheck</key>
    <false/>
    <key>showTaskBar</key>
    <false/>
    <key>enableQuitButton</key>
    <true/>
    <key>allowQuit</key>
    <true/>
    <key>quitURL</key>
    <string>{url}seb-quit</string>
    <key>quitURLConfirm</key>
    <false/>
    <key>quitPassword</key>
    <string>linux2024</string>
    <key>hashedQuitPassword</key>
    <string></string>
    <key>allowPreferencesWindow</key>
    <false/>
    <key>showReloadButton</key>
    <true/>
    <key>showTime</key>
    <true/>
    <key>taskBarHeight</key>
    <integer>40</integer>
    <key>newBrowserWindowAllow</key>
    <false/>
    <key>allowDeveloperConsole</key>
    <false/>
    <key>enableTouchExit</key>
    <false/>
</dict>
</plist>"""
    return Response(xml_content, mimetype='application/seb', headers={
        "Content-Disposition": "attachment; filename=ders_takip.seb"
    })
