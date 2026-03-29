import csv
import io
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from core.db import db_baglantisi
from core.config import ders_durumu, ayar_kaydet, ayar_getir
from core.security import ogretmen_giris_gerekli
from core.utils import bugun, simdi, paket_hesapla, paket_zaman_kontrolu, istemci_ip
from docker_terminal import image_var_mi, container_durum

log = logging.getLogger('app')
api_bp = Blueprint('api_bp', __name__, url_prefix='/api')

@api_bp.route('/durum')
def api_durum():
    hash_param = request.args.get('hash', '')
    if hash_param:
        ders_durumu['slayt_hash'] = hash_param

    cikis_onaylandi = False
    from flask import session
    numara = session.get('numara')
    if numara:
        with db_baglantisi() as db:
            kayit = db.execute("SELECT durum FROM seb_cikis_talepleri WHERE numara=? AND tarih=? ORDER BY id DESC LIMIT 1", (numara, bugun())).fetchone()
            if kayit and kayit['durum'] == 'onaylandi':
                cikis_onaylandi = True

    # Toplu çıkış kontrolü
    toplu_cikis = False
    giris_zamani = session.get('giris_zamani', 0)
    toplu_cikis_zamani = ders_durumu.get('toplu_cikis_zamani', 0)
    if toplu_cikis_zamani and giris_zamani and toplu_cikis_zamani > giris_zamani:
        toplu_cikis = True
        session.clear()

    # Bireysel force-çıkış kontrolü (öğretmen tek öğrenciyi çıkarır)
    if not toplu_cikis and numara:
        force_cikis_zamani = ders_durumu.get('force_cikis', {}).get(numara, 0)
        if force_cikis_zamani and giris_zamani and force_cikis_zamani > giris_zamani:
            toplu_cikis = True
            session.clear()
            # Temizle — tek seferlik
            ders_durumu.get('force_cikis', {}).pop(numara, None)

    response = {
        'mod': ders_durumu['mod'],
        'dosya': ders_durumu['dosya'],
        'slayt_hash': ders_durumu.get('slayt_hash', ''),
        'terminal_url': ders_durumu.get('terminal_url', ''),
        'cikis_onaylandi': cikis_onaylandi,
        'toplu_cikis': toplu_cikis,
        'cikis_izni': ders_durumu.get('cikis_izni', '0') == '1',
        'kiosk_modu': ders_durumu.get('kiosk_modu', '1') == '1',
        'sinav_terminal': ders_durumu.get('sinav_terminal', False),
        'db_saglikli': __import__('core.db', fromlist=['db_saglikli']).db_saglikli,
        'giris_acik': ders_durumu.get('giris_acik', False)
    }
    return jsonify(response)

@api_bp.route('/slayt_hash', methods=['POST'])
@ogretmen_giris_gerekli
def api_slayt_hash():
    veri = request.get_json() or {}
    hash_val = veri.get('hash', '')
    if hash_val:
        ders_durumu['slayt_hash'] = hash_val
    return jsonify({'durum': 'ok'})

@api_bp.route('/mod', methods=['POST'])
@ogretmen_giris_gerekli
def api_mod_degistir():
    veri = request.get_json()
    if veri.get('mod') in ('bekleme', 'slayt', 'terminal'):
        log.info(f"Mod Değişimi: {ders_durumu['mod']} -> {veri.get('mod')} (Dosya: {veri.get('dosya')}, Terminal URL: {veri.get('terminal_url')})")
        ders_durumu['mod']   = veri['mod']
        ders_durumu['dosya'] = veri.get('dosya', '')
        ders_durumu['terminal_url'] = veri.get('terminal_url', '')

        if 'slayt_hash' in veri and not veri['slayt_hash']:
            ders_durumu['slayt_hash'] = ''
    return jsonify({'durum': 'ok', 'mod': ders_durumu['mod']})

@api_bp.route('/config', methods=['GET'])
@ogretmen_giris_gerekli
def api_config_get():
    return jsonify({
        'ders_gunleri': ayar_getir('ders_gunleri', '1'),
    })

@api_bp.route('/config', methods=['POST'])
@ogretmen_giris_gerekli
def api_config():
    veri = request.get_json()
    if 'chroot_host' in veri:
        host = veri['chroot_host']
        ders_durumu['chroot_host'] = host
        ayar_kaydet('chroot_host', host)
        try:
            import chroot_terminal
            chroot_terminal.CHROOT_HOST = host
        except: pass
            
    if 'chroot_port' in veri:
        try:
            port = int(veri['chroot_port'])
            ders_durumu['chroot_port'] = port
            ayar_kaydet('chroot_port', port)
            import chroot_terminal
            chroot_terminal.CHROOT_SSH_PORT = port
            chroot_terminal.CHROOT_REAL_SSH_PORT = port
        except: pass

    if 'chroot_user' in veri:
        user = veri['chroot_user']
        ders_durumu['chroot_user'] = user
        ayar_kaydet('chroot_user', user)
        try:
            import chroot_terminal
            chroot_terminal.CHROOT_USER = user
        except: pass

    if 'chroot_pass' in veri:
        pw = veri['chroot_pass']
        ders_durumu['chroot_pass'] = pw
        ayar_kaydet('chroot_pass', pw)
        try:
            import chroot_terminal
            chroot_terminal.CHROOT_PASS = pw
        except: pass

    if 'system_host' in veri:
        host = veri['system_host']
        ders_durumu['system_host'] = host
        ayar_kaydet('system_host', host)
            
    if 'ttyd_url' in veri:
        url = veri['ttyd_url']
        ders_durumu['terminal_url'] = url
        ayar_kaydet('terminal_url', url)

    if 'kiosk_modu' in veri:
        kiosk = str(veri['kiosk_modu'])
        ders_durumu['kiosk_modu'] = kiosk
        ayar_kaydet('kiosk_modu', kiosk)

    if 'ip_kontrol' in veri:
        ip_k = str(veri['ip_kontrol'])
        ders_durumu['ip_kontrol'] = ip_k
        ayar_kaydet('ip_kontrol', ip_k)

    if 'cikis_izni' in veri:
        cikis = str(veri['cikis_izni'])
        ders_durumu['cikis_izni'] = cikis
        ayar_kaydet('cikis_izni', cikis)

    if 'ders_gunleri' in veri:
        ayar_kaydet('ders_gunleri', str(veri['ders_gunleri']))

    if 'slayt_klasoru' in veri:
        klasor = str(veri['slayt_klasoru'])
        ders_durumu['slayt_klasoru'] = klasor
        ayar_kaydet('slayt_klasoru', klasor)

    # Veritabanı Ayarları
    db_keys = ['db_type', 'db_host', 'db_port', 'db_user', 'db_pass', 'db_name']
    for key in db_keys:
        if key in veri:
            ayar_kaydet(key, str(veri[key]))
            # ders_durumu güncellemesi (isteğe bağlı, db_baglantisi os.environ veya ayar_getir kullanmalı)

    return jsonify({'durum': 'ok'})


@api_bp.route('/giris_toggle', methods=['POST'])
@ogretmen_giris_gerekli
def api_giris_toggle():
    """Öğrenci girişini aç/kapat."""
    veri = request.get_json() or {}
    acik = veri.get('acik', not ders_durumu.get('giris_acik', False))
    ders_durumu['giris_acik'] = bool(acik)
    durum = 'açıldı' if acik else 'kapatıldı'
    log.info(f"🚪 Öğrenci girişi {durum}")
    return jsonify({'durum': 'ok', 'giris_acik': ders_durumu['giris_acik']})


@api_bp.route('/healthcheck', methods=['POST'])
@ogretmen_giris_gerekli
def api_healthcheck():
    veri = request.get_json()
    host = veri.get('chroot_host', '')
    port = veri.get('chroot_port', 22)
    user = veri.get('chroot_user', 'root')
    password = veri.get('chroot_pass', '')

    try:
        from chroot_terminal import _is_local
        if _is_local(host):
            return jsonify({'durum': 'ok', 'mesaj': 'Bağlantı Başarılı (Yerel Sistem)'})

        import subprocess
        ssh_cmd = [
            "ssh", "-o", "ConnectTimeout=5",
            "-o", "StrictHostKeyChecking=no",
            "-o", "BatchMode=yes" if not password else "BatchMode=no",
            "-p", str(port),
            f"{user}@{host}",
            "echo ok"
        ]

        if password:
            import shutil
            if not shutil.which("sshpass"):
                return jsonify({'durum': 'hata', 'mesaj': 'sshpass yüklü değil, şifreli giriş yapılamaz.'})
            ssh_cmd = ["sshpass", "-p", password] + ssh_cmd

        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return jsonify({'durum': 'ok', 'mesaj': 'Bağlantı Başarılı'})
        else:
            return jsonify({'durum': 'hata', 'mesaj': f"Bağlantı Hatası: {result.stderr.strip().splitlines()[-1] if result.stderr.strip() else 'Bilinmeyen Hata'}"})
    except subprocess.TimeoutExpired:
        return jsonify({'durum': 'hata', 'mesaj': 'Bağlantı zaman aşımına uğradı.'})
    except Exception as e:
        return jsonify({'durum': 'hata', 'mesaj': str(e)})

@api_bp.route('/yoklama')
@ogretmen_giris_gerekli
def api_yoklama():
    paket = request.args.get('paket', '')
    tarih = request.args.get('tarih', bugun())
    with db_baglantisi() as db:
        if paket:
            satirlar = db.execute(
                'SELECT ad_soyad, numara, saat, sinif, paket, kaynak, ip FROM yoklama WHERE tarih=? AND paket=? ORDER BY saat',
                (tarih, paket)
            ).fetchall()
        else:
            satirlar = db.execute(
                'SELECT ad_soyad, numara, saat, sinif, paket, kaynak, ip FROM yoklama WHERE tarih=? ORDER BY saat',
                (tarih,)
            ).fetchall()
    return jsonify({
        'tarih': tarih,
        'paket': paket,
        'ogrenciler': [dict(s) for s in satirlar]
    })

@api_bp.route('/siniflar')
@ogretmen_giris_gerekli
def api_siniflar():
    with db_baglantisi() as db:
        siniflar = db.execute('SELECT id, ad FROM siniflar ORDER BY ad').fetchall()
        sonuc = []
        for s in siniflar:
            kayitli = db.execute('SELECT COUNT(*) as sayi FROM ogrenciler WHERE sinif_id=?', (s['id'],)).fetchone()['sayi']
            bugunki = db.execute('SELECT COUNT(*) as sayi FROM yoklama WHERE tarih=? AND sinif=?', (bugun(), s['ad'])).fetchone()['sayi']
            sonuc.append({'id': s['id'], 'ad': s['ad'], 'kayitli': kayitli, 'bugun': bugunki})
    return jsonify({'siniflar': sonuc})

@api_bp.route('/ogrenci_listesi/<int:sinif_id>')
def api_ogrenci_listesi(sinif_id):
    with db_baglantisi() as db:
        ogrenciler = db.execute('SELECT numara, ad, soyad FROM ogrenciler WHERE sinif_id=? ORDER BY soyad, ad', (sinif_id,)).fetchall()
    return jsonify({'ogrenciler': [{'numara': o['numara'], 'ad_soyad': (o['ad'] + ' ' + o['soyad']).upper()} for o in ogrenciler]})

@api_bp.route('/ogrenci/devam')
def api_ogrenci_devam():
    """Öğrencinin kendi devam durumunu görmesi."""
    from flask import session
    numara = session.get('numara')
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Oturum yok'}), 401

    with db_baglantisi() as db:
        katilimlar = db.execute(
            'SELECT DISTINCT tarih, paket FROM yoklama WHERE numara=? ORDER BY tarih DESC',
            (numara,)
        ).fetchall()
        tum_gunler = db.execute(
            'SELECT DISTINCT tarih FROM yoklama ORDER BY tarih DESC'
        ).fetchall()

    katilim_tarihleri = {r['tarih'] for r in katilimlar}
    tum_tarihler_ham = [r['tarih'] for r in tum_gunler]

    # Ders günü filtresi
    from datetime import datetime as _dt
    ders_gunleri_ayar = ayar_getir('ders_gunleri', '')
    if ders_gunleri_ayar:
        gecerli_gunler = {int(g.strip()) for g in ders_gunleri_ayar.split(',') if g.strip().isdigit()}
        tum_tarihler = [t for t in tum_tarihler_ham if _dt.strptime(t, '%Y-%m-%d').weekday() in gecerli_gunler]
    else:
        tum_tarihler = tum_tarihler_ham

    gecmis = []
    for tarih in tum_tarihler:
        if tarih in katilim_tarihleri:
            for k in katilimlar:
                if k['tarih'] == tarih:
                    gecmis.append({'tarih': tarih, 'paket': k['paket'], 'durum': 'geldi'})
        else:
            gecmis.append({'tarih': tarih, 'paket': '-', 'durum': 'gelmedi'})

    toplam = len(tum_tarihler)
    katilim = len(katilim_tarihleri)
    devamsizlik = toplam - katilim
    yuzde = round((katilim / toplam * 100)) if toplam > 0 else 0

    return jsonify({
        'ozet': {'toplam_ders': toplam, 'katilim': katilim, 'devamsizlik': devamsizlik, 'yuzde': yuzde},
        'gecmis': gecmis
    })

@api_bp.route('/sinif_ogrencileri/<int:sinif_id>')
@ogretmen_giris_gerekli
def api_sinif_ogrencileri(sinif_id):
    with db_baglantisi() as db:
        ogrenciler = db.execute('SELECT numara, ad, soyad FROM ogrenciler WHERE sinif_id=? ORDER BY soyad, ad', (sinif_id,)).fetchall()
        bugunki = {r['numara']: r['paket'] for r in db.execute('SELECT numara, paket FROM yoklama WHERE tarih=?', (bugun(),)).fetchall()}
    return jsonify({'ogrenciler': [{'numara': o['numara'], 'ad_soyad': o['ad'] + ' ' + o['soyad'], 'geldi': o['numara'] in bugunki, 'paket': bugunki.get(o['numara'], '')} for o in ogrenciler]})

@api_bp.route('/manuel_giris', methods=['POST'])
@ogretmen_giris_gerekli
def api_manuel_giris():
    veri = request.get_json()
    sinif_id = veri.get('sinif_id')
    numara   = veri.get('numara')
    if not sinif_id or not numara: return jsonify({'durum': 'hata', 'mesaj': 'Eksik parametre'}), 400
    with db_baglantisi() as db:
        ogrenci = db.execute('SELECT ad, soyad FROM ogrenciler WHERE numara=? AND sinif_id=?', (numara, sinif_id)).fetchone()
        if not ogrenci: return jsonify({'durum': 'hata', 'mesaj': 'Öğrenci bulunamadı'}), 404
        sinif_row = db.execute('SELECT ad FROM siniflar WHERE id=?', (sinif_id,)).fetchone()
        sinif_ad  = sinif_row['ad'] if sinif_row else ''
        tarih, paket = bugun(), paket_hesapla()
        if db.execute('SELECT id FROM yoklama WHERE tarih=? AND numara=? AND paket=?', (tarih, numara, paket)).fetchone():
            return jsonify({'durum': 'hata', 'mesaj': 'Bu öğrenci bugün bu pakette zaten kayıtlı'}), 409
        tam_ad = (ogrenci['ad'] + ' ' + ogrenci['soyad']).upper()
        saat = simdi()
        db.execute('INSERT INTO yoklama (tarih, ad_soyad, numara, saat, sinif, paket, ip, kaynak) VALUES (?,?,?,?,?,?,?,?)', (tarih, tam_ad, numara, saat, sinif_ad, paket, 'manuel', 'manuel'))
        db.commit()
    return jsonify({'durum': 'ok', 'ad_soyad': tam_ad, 'saat': saat, 'paket': paket})

@api_bp.route('/sahte_log')
@ogretmen_giris_gerekli
def api_sahte_log():
    with db_baglantisi() as db:
        kayitlar = db.execute('SELECT * FROM sahte_giris_log ORDER BY tarih DESC, saat DESC').fetchall()
    return jsonify({'kayitlar': [dict(k) for k in kayitlar]})

@api_bp.route('/sahte_log/sil_tek', methods=['POST'])
@ogretmen_giris_gerekli
def api_sahte_log_sil_tek():
    veri = request.get_json()
    if not veri or not veri.get('id'): return jsonify({'durum': 'hata', 'mesaj': 'ID gerekli'}), 400
    with db_baglantisi() as db:
        silinen = db.execute('DELETE FROM sahte_giris_log WHERE id=?', (veri['id'],))
        db.commit()
    if silinen.rowcount == 0: return jsonify({'durum': 'hata', 'mesaj': 'Kayıt bulunamadı'}), 404
    return jsonify({'durum': 'ok', 'silinen': 1})

@api_bp.route('/yoklama/tarihler')
@ogretmen_giris_gerekli
def api_yoklama_tarihler():
    """Yoklama kaydı olan tüm tarihleri listele."""
    with db_baglantisi() as db:
        tarihler = db.execute(
            'SELECT DISTINCT tarih, COUNT(*) as sayi FROM yoklama GROUP BY tarih ORDER BY tarih DESC'
        ).fetchall()
    return jsonify({'tarihler': [{'tarih': t['tarih'], 'sayi': t['sayi']} for t in tarihler]})

@api_bp.route('/yoklama/paketler')
@ogretmen_giris_gerekli
def api_yoklama_paketler():
    """Bugünkü yoklamadaki paketleri listele."""
    tarih = request.args.get('tarih', bugun())
    with db_baglantisi() as db:
        paketler = db.execute(
            'SELECT DISTINCT paket, COUNT(*) as sayi FROM yoklama WHERE tarih=? GROUP BY paket ORDER BY paket',
            (tarih,)
        ).fetchall()
    return jsonify({'paketler': [{'paket': p['paket'], 'sayi': p['sayi']} for p in paketler]})

@api_bp.route('/yoklama/csv')
@ogretmen_giris_gerekli
def api_yoklama_csv():
    with db_baglantisi() as db:
        satirlar = db.execute('SELECT ad_soyad, numara, saat, sinif, paket, kaynak FROM yoklama WHERE tarih=? ORDER BY sinif, saat', (bugun(),)).fetchall()
    tarih_timestamp = datetime.now().strftime('%Y%m%d%H%M')
    cikti = io.StringIO()
    yazar = csv.writer(cikti)
    yazar.writerow(['Tarih', 'Saat', 'Ad Soyad', 'Öğrenci No', 'Sınıf', 'Paket', 'Kaynak'])
    for s in satirlar: yazar.writerow([bugun(), s['saat'], s['ad_soyad'], s['numara'], s['sinif'], s['paket'], s['kaynak']])
    cikti.seek(0)
    return send_file(io.BytesIO(cikti.getvalue().encode('utf-8-sig')), mimetype='text/csv', as_attachment=True, download_name=f"yoklama_{tarih_timestamp}.csv")

@api_bp.route('/yoklama/tarih_csv')
@ogretmen_giris_gerekli
def api_yoklama_tarih_csv():
    tarih_param = request.args.get('tarih', bugun())
    try:
        tarih_db = '-'.join(tarih_param.split('-')) if '-' in tarih_param else f"{tarih_param[:4]}-{tarih_param[4:6]}-{tarih_param[6:8]}"
    except: tarih_db = bugun()
    with db_baglantisi() as db:
        satirlar = db.execute('SELECT ad_soyad, numara, saat, sinif, paket, kaynak FROM yoklama WHERE tarih=? ORDER BY sinif, saat', (tarih_db,)).fetchall()
    if not satirlar: return jsonify({'durum': 'hata', 'mesaj': f'{tarih_db} tarihinde kayıt bulunamadı.'}), 404
    tarih_obj = datetime.strptime(tarih_db, '%Y-%m-%d')
    cikti = io.StringIO()
    yazar = csv.writer(cikti)
    yazar.writerow(['Tarih', 'Saat', 'Ad Soyad', 'Öğrenci No', 'Sınıf', 'Paket', 'Kaynak'])
    for s in satirlar: yazar.writerow([tarih_db, s['saat'], s['ad_soyad'], s['numara'], s['sinif'], s['paket'], s['kaynak']])
    cikti.seek(0)
    return send_file(io.BytesIO(cikti.getvalue().encode('utf-8-sig')), mimetype='text/csv', as_attachment=True, download_name=f"yoklama_{tarih_obj.strftime('%Y%m%d%H%M')}.csv")

@api_bp.route('/yoklama/csv_manuel', methods=['POST'])
@ogretmen_giris_gerekli
def api_yoklama_csv_manuel():
    tarih = request.get_json().get('tarih', '') if request.get_json() else ''
    if not tarih: return jsonify({'durum': 'hata', 'mesaj': 'Tarih gerekli'}), 400
    try:
        tarih_db = tarih if '-' in tarih else datetime.strptime(tarih, '%Y%m%d').strftime('%Y-%m-%d')
        tarih_obj = datetime.strptime(tarih_db, '%Y-%m-%d')
    except ValueError: return jsonify({'durum': 'hata', 'mesaj': 'Geçersiz tarih formatı.'}), 400
    with db_baglantisi() as db:
        satirlar = db.execute('SELECT ad_soyad, numara, saat, sinif, paket, kaynak FROM yoklama WHERE tarih=? ORDER BY sinif, saat', (tarih_db,)).fetchall()
    if not satirlar: return jsonify({'durum': 'hata', 'mesaj': f'{tarih_db} tarihinde kayıt bulunamadı.'}), 404
    cikti = io.StringIO()
    yazar = csv.writer(cikti)
    yazar.writerow(['Tarih', 'Saat', 'Ad Soyad', 'Öğrenci No', 'Sınıf', 'Paket', 'Kaynak'])
    for s in satirlar: yazar.writerow([tarih_db, s['saat'], s['ad_soyad'], s['numara'], s['sinif'], s['paket'], s['kaynak']])
    cikti.seek(0)
    return send_file(io.BytesIO(cikti.getvalue().encode('utf-8-sig')), mimetype='text/csv', as_attachment=True, download_name=f"yoklama_{tarih_obj.strftime('%Y%m%d%H%M')}.csv")

@api_bp.route('/yoklama/sil', methods=['POST'])
@ogretmen_giris_gerekli
def api_yoklama_sil():
    if not request.get_json() or not request.get_json().get('onay'): return jsonify({'durum': 'hata', 'mesaj': 'Onay gerekli'}), 400
    with db_baglantisi() as db:
        silinen = db.execute('DELETE FROM yoklama WHERE tarih=?', (bugun(),))
        db.commit()
    return jsonify({'durum': 'ok', 'silinen': silinen.rowcount})

@api_bp.route('/yoklama/sil_tek', methods=['POST'])
@ogretmen_giris_gerekli
def api_yoklama_sil_tek():
    numara = request.get_json().get('numara') if request.get_json() else None
    if not numara: return jsonify({'durum': 'hata', 'mesaj': 'Numara gerekli'}), 400
    with db_baglantisi() as db:
        silinen = db.execute('DELETE FROM yoklama WHERE tarih=? AND numara=?', (bugun(), numara))
        db.commit()
    if silinen.rowcount == 0: return jsonify({'durum': 'hata', 'mesaj': 'Kayıt bulunamadı'}), 404
    return jsonify({'durum': 'ok', 'silinen': 1})

@api_bp.route('/terminal/guvenlik_log')
@ogretmen_giris_gerekli
def api_terminal_guvenlik_log():
    with db_baglantisi() as db:
        loglar = db.execute("SELECT * FROM terminal_guvenlik_log ORDER BY id DESC LIMIT 50").fetchall()
    return jsonify({'loglar': [dict(l) for l in loglar]})

@api_bp.route('/terminal/aktif_oturumlar')
@ogretmen_giris_gerekli
def api_terminal_aktif_oturumlar():
    """Aktif terminal oturumlarının listesi."""
    try:
        from core.state import ogrenci_sidleri, ogrenci_surecleri
        oturumlar = []
        for sid, username in ogrenci_sidleri.items():
            oturumlar.append({
                'sid': sid,
                'username': username,
                'aktif': sid in ogrenci_surecleri
            })
        return jsonify({'oturumlar': oturumlar})
    except Exception as e:
        return jsonify({'oturumlar': [], 'hata': str(e)})

@api_bp.route('/terminal/durum')
@ogretmen_giris_gerekli
def api_terminal_durum():
    # Bu kısmı SocketIo loglarını app üzerinden çekmek zor olabilir.
    # Geçici olarak 0 döndürüp sonra `app.py` den `ogrenci_sidleri` ni import edebiliriz,
    # ya da sadece duruma odaklanıriz.  
    # To fix this elegantly, we'll try importing dynamic counters or just omit the live student count here or handle it at the app wrapper.
    import docker_terminal
    # app.py'de ogrenci_sidleri var, ama blueprint içinde erişmek zor.
    # Şimdilik globalden deneyelim, hata durumunda len=0
    import app as main_app
    try: bagli = len(main_app.ogrenci_sidleri)
    except: bagli = 0
    return jsonify({
        'image_hazir': docker_terminal.image_var_mi(),
        'konteyner_calisiyor': docker_terminal.container_durum(),
        'bagli_ogrenciler': bagli
    })

@api_bp.route('/seb_cikis', methods=['POST'])
def api_seb_cikis():
    from flask import session
    from core.utils import istemci_ip
    
    numara = session.get('numara')
    if not numara:
        return jsonify({'durum': 'ok'})
        
    ad_soyad = f"{session.get('ad', '')} {session.get('soyad', '')}".strip()
    
    with db_baglantisi() as db:
        db.execute(
            'INSERT INTO seb_cikis_log (tarih, saat, numara, ad_soyad, ip) VALUES (?, ?, ?, ?, ?)',
            (bugun(), simdi(), numara, ad_soyad, istemci_ip())
        )
        db.commit()
    return jsonify({'durum': 'ok'})

@api_bp.route('/seb_cikis_log')
@ogretmen_giris_gerekli
def api_seb_cikis_log():
    with db_baglantisi() as db:
        loglar = db.execute("SELECT * FROM seb_cikis_log WHERE tarih=? ORDER BY id DESC", (bugun(),)).fetchall()
    return jsonify({'loglar': [dict(l) for l in loglar]})

@api_bp.route('/seb_cikis_talep', methods=['POST'])
def api_seb_cikis_talep():
    from flask import session
    numara = session.get('numara')
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Oturum yok'})
        
    ad_soyad = f"{session.get('ad', '')} {session.get('soyad', '')}".strip()
    
    with db_baglantisi() as db:
        mevcut = db.execute("SELECT id, durum FROM seb_cikis_talepleri WHERE numara=? AND tarih=? AND durum != 'reddedildi'", (numara, bugun())).fetchone()
        if mevcut:
            return jsonify({'durum': 'ok', 'mesaj': 'Zaten talebiniz var.'})
            
        db.execute(
            'INSERT INTO seb_cikis_talepleri (tarih, saat, numara, ad_soyad, durum) VALUES (?, ?, ?, ?, ?)',
            (bugun(), simdi(), numara, ad_soyad, 'bekliyor')
        )
        db.commit()
    return jsonify({'durum': 'ok'})

@api_bp.route('/seb_cikis_talepler', methods=['GET'])
@ogretmen_giris_gerekli
def api_seb_cikis_talepler():
    with db_baglantisi() as db:
        liste = db.execute("SELECT * FROM seb_cikis_talepleri WHERE tarih=? AND durum='bekliyor' ORDER BY id ASC", (bugun(),)).fetchall()
    return jsonify({'talepler': [dict(l) for l in liste]})

@api_bp.route('/seb_cikis_onayla', methods=['POST'])
@ogretmen_giris_gerekli
def api_seb_cikis_onayla():
    data = request.json
    talep_id = data.get('id')
    durum_val = data.get('durum', 'onaylandi')
    
    with db_baglantisi() as db:
        db.execute("UPDATE seb_cikis_talepleri SET durum=? WHERE id=?", (durum_val, talep_id))
        db.commit()
    return jsonify({'durum': 'ok'})

@api_bp.route('/toplu_cikis', methods=['POST'])
@ogretmen_giris_gerekli
def api_toplu_cikis():
    """Tüm öğrencileri çıkış yaptır (paket değişimi vb.)."""
    import time
    ders_durumu['toplu_cikis_zamani'] = time.time()
    ders_durumu['mod'] = 'bekleme'
    ders_durumu['dosya'] = ''
    log.info(f"🚪 Toplu çıkış tetiklendi - tüm öğrenci oturumları sonlandırılıyor")
    return jsonify({'durum': 'ok', 'mesaj': 'Tüm öğrenciler çıkış yapacak'})


@api_bp.route('/paket_sonu', methods=['POST'])
@ogretmen_giris_gerekli
def api_paket_sonu():
    """Paket sonu: Toplu çıkış + o paketin öğrencilerinin chroot'larını sil.

    Body (JSON):
        paket: str — hangi paketin chroot'ları silinecek (boş ise mevcut paket)
    """
    import time
    import threading
    from core.utils import paket_hesapla

    veri = request.get_json(silent=True) or {}
    hedef_paket = veri.get('paket', '') or paket_hesapla()

    # 1. Toplu çıkış tetikle (öğrenciler giriş sayfasına yönlendirilir)
    ders_durumu['toplu_cikis_zamani'] = time.time()
    ders_durumu['mod'] = 'bekleme'
    ders_durumu['dosya'] = ''

    # 2. O pakete ait öğrenci numaralarını al
    with db_baglantisi() as db:
        kayitlar = db.execute(
            'SELECT DISTINCT numara FROM yoklama WHERE tarih=? AND paket=?',
            (bugun(), hedef_paket)
        ).fetchall()

    numaralar = [r['numara'] for r in kayitlar]
    log.info(f"📦 Paket sonu: {hedef_paket} — {len(numaralar)} öğrencinin chroot'u silinecek")

    # 3. Chroot silmeyi arka planda çalıştır (API hemen döner)
    def _chroot_temizle():
        try:
            from chroot_terminal import chroot_sil_batch
            sonuclar = chroot_sil_batch(numaralar)
            silindi = sum(1 for v in sonuclar.values() if v)
            log.info(f"✅ Paket sonu temizliği tamamlandı: {silindi}/{len(numaralar)} chroot silindi")
        except Exception as e:
            log.error(f"Paket sonu chroot temizliği hatası: {e}")

    threading.Thread(target=_chroot_temizle, daemon=True).start()

    return jsonify({
        'durum': 'ok',
        'mesaj': f'{len(numaralar)} öğrencinin VM\'i siliniyor, lütfen bekleyin.',
        'paket': hedef_paket,
        'ogrenci_sayisi': len(numaralar)
    })

@api_bp.route('/seb_cikis_toplu_onayla', methods=['POST'])
@ogretmen_giris_gerekli
def api_seb_cikis_toplu_onayla():
    with db_baglantisi() as db:
        db.execute("UPDATE seb_cikis_talepleri SET durum='onaylandi' WHERE tarih=? AND durum='bekliyor'", (bugun(),))
        db.commit()
    return jsonify({'durum': 'ok'})

@api_bp.route('/ogrenci_cikis', methods=['POST'])
def api_ogrenci_cikis():
    """Öğrenci paket saatleri içinde kendi oturumunu kapatır."""
    from flask import session
    numara = session.get('numara')
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Oturum yok'}), 401

    ad_soyad = f"{session.get('ad', '')} {session.get('soyad', '')}".strip()

    # Bugünkü paketi bul
    with db_baglantisi() as db:
        kayit = db.execute(
            'SELECT paket FROM yoklama WHERE tarih=? AND numara=? ORDER BY id DESC LIMIT 1',
            (bugun(), numara)
        ).fetchone()

    if not kayit:
        return jsonify({'durum': 'hata', 'mesaj': 'Bugün yoklama kaydınız bulunamadı.'})

    paket = kayit['paket']

    # Test modunda paket saati kontrolü atlanır
    if not ders_durumu.get('test_modu'):
        bas, bit, gecerli = paket_zaman_kontrolu(paket)
        if not gecerli:
            return jsonify({
                'durum': 'hata',
                'mesaj': f'Çıkış yalnızca paket saatleri içinde yapılabilir ({bas}–{bit}).',
                'zaman_disi': True,
                'paket': paket,
                'bas': bas,
                'bit': bit,
            })

    # Çıkışı kaydet
    with db_baglantisi() as db:
        db.execute(
            'INSERT INTO ogrenci_cikis_log (tarih, saat, numara, ad_soyad, paket, ip, kaynak) VALUES (?,?,?,?,?,?,?)',
            (bugun(), simdi(), numara, ad_soyad, paket, istemci_ip(), 'ogrenci')
        )
        db.commit()

    log.info(f"🚪 Öğrenci çıkış: {numara} ({ad_soyad}) — {paket}")
    session.clear()
    return jsonify({'durum': 'ok', 'mesaj': 'Çıkış başarılı.'})


@api_bp.route('/ogrenci_cikis_log')
@ogretmen_giris_gerekli
def api_ogrenci_cikis_log():
    """Öğrenci çıkış loglarını listele."""
    tarih = request.args.get('tarih', bugun())
    with db_baglantisi() as db:
        kayitlar = db.execute(
            'SELECT * FROM ogrenci_cikis_log WHERE tarih=? ORDER BY id DESC',
            (tarih,)
        ).fetchall()
    return jsonify({'kayitlar': [dict(k) for k in kayitlar]})


@api_bp.route('/ogrenci_force_cikis', methods=['POST'])
@ogretmen_giris_gerekli
def api_ogrenci_force_cikis():
    """Öğretmen tek bir öğrenciyi zorla çıkartır."""
    import time
    veri = request.get_json(silent=True) or {}
    numara = veri.get('numara', '').strip()
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Numara gerekli'}), 400

    if 'force_cikis' not in ders_durumu:
        ders_durumu['force_cikis'] = {}
    ders_durumu['force_cikis'][numara] = time.time()

    # Log kaydı
    with db_baglantisi() as db:
        ad_soyad_row = db.execute('SELECT ad, soyad FROM ogrenciler WHERE numara=?', (numara,)).fetchone()
        ad_soyad = f"{ad_soyad_row['ad']} {ad_soyad_row['soyad']}" if ad_soyad_row else numara
        paket = paket_hesapla()
        db.execute(
            'INSERT INTO ogrenci_cikis_log (tarih, saat, numara, ad_soyad, paket, ip, kaynak) VALUES (?,?,?,?,?,?,?)',
            (bugun(), simdi(), numara, ad_soyad, paket, 'ogretmen', 'force')
        )
        db.commit()

    log.info(f"👨‍🏫 Öğretmen force-çıkış: {numara}")
    return jsonify({'durum': 'ok', 'mesaj': f'{numara} çıkartıldı.'})


@api_bp.route('/yardim_talep', methods=['POST'])
def api_yardim_talep():
    from flask import session
    numara = session.get('numara')
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Oturum yok'})

    ad_soyad = f"{session.get('ad', '')} {session.get('soyad', '')}".strip()

    # Kategori parametresini JSON body'den al
    gecerli_kategoriler = ('komut', 'dosya', 'terminal', 'soru', 'diger')
    veri = request.get_json(silent=True) or {}
    kategori = veri.get('kategori', '')
    if kategori and kategori not in gecerli_kategoriler:
        kategori = ''

    with db_baglantisi() as db:
        mevcut = db.execute("SELECT id, durum FROM yardim_talepleri WHERE numara=? AND tarih=? AND durum != 'tamamlandi'", (numara, bugun())).fetchone()
        if mevcut:
            return jsonify({'durum': 'ok', 'mesaj': 'Zaten aktif bir yardım talebiniz var.'})

        db.execute(
            'INSERT INTO yardim_talepleri (tarih, saat, numara, ad_soyad, durum, kategori) VALUES (?, ?, ?, ?, ?, ?)',
            (bugun(), simdi(), numara, ad_soyad, 'bekliyor', kategori)
        )
        db.commit()
    return jsonify({'durum': 'ok'})

@api_bp.route('/yardim_talepler', methods=['GET'])
@ogretmen_giris_gerekli
def api_yardim_talepler():
    with db_baglantisi() as db:
        liste = db.execute("SELECT * FROM yardim_talepleri WHERE tarih=? AND (durum='bekliyor' OR durum='kabul_edildi') ORDER BY CASE WHEN durum='bekliyor' THEN 0 ELSE 1 END, id ASC", (bugun(),)).fetchall()
    return jsonify({'talepler': [dict(l) for l in liste]})

@api_bp.route('/yardim_kabul', methods=['POST'])
@ogretmen_giris_gerekli
def api_yardim_kabul():
    data = request.json
    talep_id = data.get('id')
    durum_val = data.get('durum', 'kabul_edildi') # 'kabul_edildi' veya 'tamamlandi' / 'reddedildi'
    
    with db_baglantisi() as db:
        db.execute("UPDATE yardim_talepleri SET durum=? WHERE id=?", (durum_val, talep_id))
        db.commit()
    return jsonify({'durum': 'ok'})


# ── Öğrenci Yönetimi ─────────────────────────────────────────────

@api_bp.route('/ogrenci_ekle', methods=['POST'])
@ogretmen_giris_gerekli
def api_ogrenci_ekle():
    veri = request.get_json()
    sinif_id = veri.get('sinif_id')
    numara = veri.get('numara', '').strip()
    ad = veri.get('ad', '').strip().upper()
    soyad = veri.get('soyad', '').strip().upper()
    if not sinif_id or not numara or not ad or not soyad:
        return jsonify({'durum': 'hata', 'mesaj': 'Tüm alanlar gerekli (sınıf, numara, ad, soyad)'}), 400
    with db_baglantisi() as db:
        mevcut = db.execute('SELECT id FROM ogrenciler WHERE numara=?', (numara,)).fetchone()
        if mevcut:
            return jsonify({'durum': 'hata', 'mesaj': f'{numara} numaralı öğrenci zaten kayıtlı'}), 409
        db.execute('INSERT INTO ogrenciler (sinif_id, numara, ad, soyad, sifre) VALUES (?,?,?,?,?)',
                   (sinif_id, numara, ad, soyad, numara))
        db.commit()
    return jsonify({'durum': 'ok', 'mesaj': f'{ad} {soyad} ({numara}) eklendi'})

@api_bp.route('/ogrenci_sil', methods=['POST'])
@ogretmen_giris_gerekli
def api_ogrenci_sil():
    veri = request.get_json()
    numara = veri.get('numara', '').strip() if veri else ''
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Numara gerekli'}), 400
    with db_baglantisi() as db:
        silinen = db.execute('DELETE FROM ogrenciler WHERE numara=?', (numara,))
        db.commit()
    if silinen.rowcount == 0:
        return jsonify({'durum': 'hata', 'mesaj': 'Öğrenci bulunamadı'}), 404

    # Öğrenci silinince chroot VM'i de arka planda temizle
    import threading
    def _chroot_sil():
        try:
            from chroot_terminal import chroot_sil, _slugify
            chroot_sil(_slugify(numara))
            log.info(f"🗑️ Öğrenci silindi, chroot temizlendi: {numara}")
        except Exception as e:
            log.warning(f"Öğrenci {numara} chroot silinemedi: {e}")
    threading.Thread(target=_chroot_sil, daemon=True).start()

    return jsonify({'durum': 'ok', 'mesaj': f'{numara} numaralı öğrenci ve VM silindi'})

@api_bp.route('/ogrenci_guncelle', methods=['POST'])
@ogretmen_giris_gerekli
def api_ogrenci_guncelle():
    veri = request.get_json()
    numara = veri.get('numara', '').strip()
    yeni_ad = veri.get('ad', '').strip().upper()
    yeni_soyad = veri.get('soyad', '').strip().upper()
    yeni_sinif_id = veri.get('sinif_id')
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Numara gerekli'}), 400
    with db_baglantisi() as db:
        mevcut = db.execute('SELECT id FROM ogrenciler WHERE numara=?', (numara,)).fetchone()
        if not mevcut:
            return jsonify({'durum': 'hata', 'mesaj': 'Öğrenci bulunamadı'}), 404
        if yeni_ad and yeni_soyad:
            db.execute('UPDATE ogrenciler SET ad=?, soyad=? WHERE numara=?', (yeni_ad, yeni_soyad, numara))
        if yeni_sinif_id:
            db.execute('UPDATE ogrenciler SET sinif_id=? WHERE numara=?', (yeni_sinif_id, numara))
        db.commit()
    return jsonify({'durum': 'ok', 'mesaj': 'Öğrenci güncellendi'})

@api_bp.route('/sinif_ekle', methods=['POST'])
@ogretmen_giris_gerekli
def api_sinif_ekle():
    veri = request.get_json()
    ad = veri.get('ad', '').strip() if veri else ''
    if not ad:
        return jsonify({'durum': 'hata', 'mesaj': 'Sınıf adı gerekli'}), 400
    with db_baglantisi() as db:
        mevcut = db.execute('SELECT id FROM siniflar WHERE ad=?', (ad,)).fetchone()
        if mevcut:
            return jsonify({'durum': 'hata', 'mesaj': f'"{ad}" sınıfı zaten var'}), 409
        db.execute('INSERT INTO siniflar (ad) VALUES (?)', (ad,))
        db.commit()
    return jsonify({'durum': 'ok', 'mesaj': f'"{ad}" sınıfı eklendi'})

@api_bp.route('/sinif_sil', methods=['POST'])
@ogretmen_giris_gerekli
def api_sinif_sil():
    veri = request.get_json()
    sinif_id = veri.get('sinif_id') if veri else None
    if not sinif_id:
        return jsonify({'durum': 'hata', 'mesaj': 'Sınıf ID gerekli'}), 400
    with db_baglantisi() as db:
        ogrenci_sayisi = db.execute('SELECT COUNT(*) as sayi FROM ogrenciler WHERE sinif_id=?', (sinif_id,)).fetchone()['sayi']
        if ogrenci_sayisi > 0:
            return jsonify({'durum': 'hata', 'mesaj': f'Bu sınıfta {ogrenci_sayisi} öğrenci var. Önce öğrencileri silin veya taşıyın.'}), 409
        silinen = db.execute('DELETE FROM siniflar WHERE id=?', (sinif_id,))
        db.commit()
    if silinen.rowcount == 0:
        return jsonify({'durum': 'hata', 'mesaj': 'Sınıf bulunamadı'}), 404
    return jsonify({'durum': 'ok', 'mesaj': 'Sınıf silindi'})


# ── Yoklama Raporlama ────────────────────────────────────────────

@api_bp.route('/yoklama/rapor')
@ogretmen_giris_gerekli
def api_yoklama_rapor():
    """Ogrenci bazinda devam raporu matrisi."""
    sinif_id = request.args.get('sinif_id', '')
    baslangic = request.args.get('baslangic', '')
    bitis = request.args.get('bitis', '')
    paket = request.args.get('paket', '')

    with db_baglantisi() as db:
        # Tarih filtrelemeli ders gunleri
        tarih_sql = 'SELECT DISTINCT tarih FROM yoklama WHERE 1=1'
        tarih_params = []
        if baslangic:
            tarih_sql += ' AND tarih >= ?'
            tarih_params.append(baslangic)
        if bitis:
            tarih_sql += ' AND tarih <= ?'
            tarih_params.append(bitis)
        if paket:
            tarih_sql += ' AND paket = ?'
            tarih_params.append(paket)
        tarih_sql += ' ORDER BY tarih'
        tum_tarihler = [r['tarih'] for r in db.execute(tarih_sql, tarih_params).fetchall()]

        # Ders günü filtresi: sadece belirlenen hafta günlerindeki kayıtları say
        from datetime import datetime as _dt
        ders_gunleri_ayar = ayar_getir('ders_gunleri', '')  # "1" veya "1,3" gibi
        if ders_gunleri_ayar:
            gecerli_gunler = {int(g.strip()) for g in ders_gunleri_ayar.split(',') if g.strip().isdigit()}
            ders_gunleri = [t for t in tum_tarihler if _dt.strptime(t, '%Y-%m-%d').weekday() in gecerli_gunler]
        else:
            ders_gunleri = tum_tarihler  # Ayar yoksa tüm günleri say

        # Ogrenci listesi (sinif filtreli)
        if sinif_id:
            ogrenciler = db.execute(
                'SELECT numara, ad, soyad FROM ogrenciler WHERE sinif_id=? ORDER BY soyad, ad',
                (sinif_id,)
            ).fetchall()
        else:
            ogrenciler = db.execute(
                'SELECT numara, ad, soyad FROM ogrenciler ORDER BY soyad, ad'
            ).fetchall()

        # Yoklama verileri — hangi ogrenci hangi gun gelmis
        yoklama_sql = 'SELECT DISTINCT numara, tarih FROM yoklama WHERE 1=1'
        yoklama_params = []
        if baslangic:
            yoklama_sql += ' AND tarih >= ?'
            yoklama_params.append(baslangic)
        if bitis:
            yoklama_sql += ' AND tarih <= ?'
            yoklama_params.append(bitis)
        if paket:
            yoklama_sql += ' AND paket = ?'
            yoklama_params.append(paket)
        yoklama_kayitlari = db.execute(yoklama_sql, yoklama_params).fetchall()

        # Devamsizlik esigi
        esik_row = db.execute("SELECT deger FROM ayarlar WHERE anahtar='devamsizlik_esik'").fetchone()
        esik = int(esik_row['deger']) if esik_row else 3

    # Set olustur: {(numara, tarih)}
    katilim_set = {(r['numara'], r['tarih']) for r in yoklama_kayitlari}
    toplam_ders = len(ders_gunleri)

    rapor = []
    for o in ogrenciler:
        katilim = sum(1 for t in ders_gunleri if (o['numara'], t) in katilim_set)
        devamsizlik = toplam_ders - katilim
        yuzde = round((katilim / toplam_ders * 100)) if toplam_ders > 0 else 0
        gunler = {}
        for t in ders_gunleri:
            gunler[t] = 'geldi' if (o['numara'], t) in katilim_set else 'gelmedi'

        rapor.append({
            'numara': o['numara'],
            'ad_soyad': o['ad'] + ' ' + o['soyad'],
            'katilim': katilim,
            'devamsizlik': devamsizlik,
            'yuzde': yuzde,
            'uyari': devamsizlik >= esik,
            'gunler': gunler
        })

    return jsonify({
        'tarihler': ders_gunleri,
        'toplam_ders': toplam_ders,
        'esik': esik,
        'rapor': rapor
    })


@api_bp.route('/yoklama/duzenle', methods=['POST'])
@ogretmen_giris_gerekli
def api_yoklama_duzenle():
    """Öğretmen yoklama kaydını düzenler: gelmedi→geldi veya geldi→gelmedi."""
    veri = request.get_json() or {}
    numara = veri.get('numara', '').strip()
    tarih = veri.get('tarih', '').strip()
    durum = veri.get('durum', '')  # 'geldi' veya 'gelmedi'
    paket = veri.get('paket', '').strip()

    if not numara or not tarih or durum not in ('geldi', 'gelmedi'):
        return jsonify({'durum': 'hata', 'mesaj': 'Eksik veya geçersiz parametre'}), 400

    with db_baglantisi() as db:
        ogrenci = db.execute('SELECT ad, soyad FROM ogrenciler WHERE numara=?', (numara,)).fetchone()
        if not ogrenci:
            return jsonify({'durum': 'hata', 'mesaj': 'Öğrenci bulunamadı'}), 404

        ad_soyad = (ogrenci['ad'] + ' ' + ogrenci['soyad']).upper()

        if durum == 'geldi':
            # Zaten kayıt var mı kontrol et
            mevcut = db.execute(
                'SELECT id FROM yoklama WHERE tarih=? AND numara=?', (tarih, numara)
            ).fetchone()
            if mevcut:
                return jsonify({'durum': 'ok', 'mesaj': 'Zaten kayıtlı'})
            # Manuel yoklama ekle
            db.execute(
                'INSERT INTO yoklama (tarih, ad_soyad, numara, saat, sinif, paket, ip, kaynak) VALUES (?,?,?,?,?,?,?,?)',
                (tarih, ad_soyad, numara, '00:00', '', paket or '-', '', 'ogretmen_duzeltme')
            )
            db.commit()
            log.info(f"✏️ Yoklama düzeltme: {numara} ({ad_soyad}) {tarih} → geldi (öğretmen)")
        else:
            # Yoklama kaydını sil
            db.execute('DELETE FROM yoklama WHERE tarih=? AND numara=?', (tarih, numara))
            db.commit()
            log.info(f"✏️ Yoklama düzeltme: {numara} ({ad_soyad}) {tarih} → gelmedi (öğretmen)")

    return jsonify({'durum': 'ok'})


@api_bp.route('/yoklama/devamsizlik_esik', methods=['GET'])
@ogretmen_giris_gerekli
def api_devamsizlik_esik_getir():
    esik = ayar_getir('devamsizlik_esik', '3')
    return jsonify({'esik': int(esik)})


@api_bp.route('/yoklama/devamsizlik_esik', methods=['POST'])
@ogretmen_giris_gerekli
def api_devamsizlik_esik_kaydet():
    veri = request.get_json()
    esik = veri.get('esik', 3)
    ayar_kaydet('devamsizlik_esik', str(esik))
    return jsonify({'durum': 'ok', 'esik': int(esik)})


@api_bp.route('/chroot/listele')
@ogretmen_giris_gerekli
def api_chroot_listele():
    """VM sunucusundaki chroot klasörlerini listele, DB ile karşılaştır."""
    try:
        from chroot_terminal import chroot_listesi, _slugify
        mevcut_chroots = [c['username'] for c in chroot_listesi()]

        with db_baglantisi() as db:
            ogrenciler = db.execute('SELECT numara FROM ogrenciler').fetchall()
        aktif_numaralar = {_slugify(r['numara']) for r in ogrenciler}
        aktif_numaralar.add('ogretmen')  # Öğretmen chroot'u korunacak

        fazla = [u for u in mevcut_chroots if u not in aktif_numaralar]
        return jsonify({
            'toplam': len(mevcut_chroots),
            'aktif': len(aktif_numaralar),
            'fazla': fazla,
            'fazla_sayisi': len(fazla),
        })
    except Exception as e:
        log.error(f"Chroot listele hatası: {e}")
        return jsonify({'hata': str(e)}), 500


@api_bp.route('/chroot/temizle', methods=['POST'])
@ogretmen_giris_gerekli
def api_chroot_temizle():
    """DB'de olmayan (artık silinmiş öğrencilere ait) chroot'ları sil."""
    import threading
    try:
        from chroot_terminal import chroot_listesi, chroot_sil_batch, _slugify
        mevcut_chroots = [c['username'] for c in chroot_listesi()]

        with db_baglantisi() as db:
            ogrenciler = db.execute('SELECT numara FROM ogrenciler').fetchall()
        aktif_numaralar = {_slugify(r['numara']) for r in ogrenciler}
        aktif_numaralar.add('ogretmen')

        fazla = [u for u in mevcut_chroots if u not in aktif_numaralar]
        if not fazla:
            return jsonify({'durum': 'ok', 'mesaj': 'Temizlenecek eski chroot yok.', 'silinen': 0})

        log.info(f"🧹 Eski chroot temizliği başlıyor: {len(fazla)} adet — {fazla}")

        def _temizle():
            sonuclar = chroot_sil_batch(fazla)
            silindi = sum(1 for v in sonuclar.values() if v)
            log.info(f"✅ Eski chroot temizliği tamamlandı: {silindi}/{len(fazla)} silindi")

        threading.Thread(target=_temizle, daemon=True).start()

        return jsonify({
            'durum': 'ok',
            'mesaj': f'{len(fazla)} eski chroot siliniyor...',
            'silinen': len(fazla),
            'liste': fazla,
        })
    except Exception as e:
        log.error(f"Chroot temizle hatası: {e}")
        return jsonify({'hata': str(e)}), 500


@api_bp.route('/chroot/sil', methods=['POST'])
@ogretmen_giris_gerekli
def api_chroot_sil_secili():
    """Seçilen chroot VM'lerini sil."""
    import threading
    veri = request.get_json() or {}
    secili = veri.get('secili', [])
    if not secili:
        return jsonify({'hata': 'Silinecek VM seçilmedi'}), 400

    # Güvenlik: ogretmen ve template silinemez
    korunmus = {'ogretmen', 'template'}
    secili = [s for s in secili if s not in korunmus]
    if not secili:
        return jsonify({'hata': 'Seçilen VM\'ler korumalı (ogretmen/template)'}), 400

    try:
        from chroot_terminal import chroot_sil_batch
        log.info(f"🗑️ Seçili chroot silme: {secili}")

        def _sil():
            sonuclar = chroot_sil_batch(secili)
            silindi = sum(1 for v in sonuclar.values() if v)
            log.info(f"✅ Seçili silme tamamlandı: {silindi}/{len(secili)}")

        threading.Thread(target=_sil, daemon=True).start()
        return jsonify({'durum': 'ok', 'silinen': len(secili), 'liste': secili})
    except Exception as e:
        log.error(f"Chroot seçili silme hatası: {e}")
        return jsonify({'hata': str(e)}), 500


@api_bp.route('/loglar')
@ogretmen_giris_gerekli
def api_loglar():
    """Son N uygulama logu döndür (in-memory buffer)."""
    from core.state import log_buffer
    limit = min(int(request.args.get('limit', 200)), 500)
    since_ts = int(request.args.get('since', 0))
    kayitlar = [e for e in log_buffer if e['ts'] > since_ts]
    return jsonify({'loglar': list(kayitlar)[-limit:]})

