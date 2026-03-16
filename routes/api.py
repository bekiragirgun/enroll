import csv
import io
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from core.db import db_baglantisi
from core.config import ders_durumu, ayar_kaydet
from core.security import ogretmen_giris_gerekli
from core.utils import bugun, simdi, paket_hesapla
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

    response = {
        'mod': ders_durumu['mod'],
        'dosya': ders_durumu['dosya'],
        'slayt_hash': ders_durumu.get('slayt_hash', ''),
        'terminal_url': ders_durumu.get('terminal_url', ''),
        'cikis_onaylandi': cikis_onaylandi,
        'toplu_cikis': toplu_cikis
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
            chroot_terminal.CT_991_HOST = host
        except: pass
            
    if 'chroot_port' in veri:
        try:
            port = int(veri['chroot_port'])
            ders_durumu['chroot_port'] = port
            ayar_kaydet('chroot_port', port)
            import chroot_terminal
            chroot_terminal.CT_991_SSH_PORT = port
            chroot_terminal.CT_991_REAL_SSH_PORT = port
        except: pass

    if 'chroot_user' in veri:
        user = veri['chroot_user']
        ders_durumu['chroot_user'] = user
        ayar_kaydet('chroot_user', user)
        try:
            import chroot_terminal
            chroot_terminal.CT_991_USER = user
        except: pass

    if 'chroot_pass' in veri:
        pw = veri['chroot_pass']
        ders_durumu['chroot_pass'] = pw
        ayar_kaydet('chroot_pass', pw)
        try:
            import chroot_terminal
            chroot_terminal.CT_991_PASS = pw
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

    return jsonify({'durum': 'ok'})

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

@api_bp.route('/seb_cikis_toplu_onayla', methods=['POST'])
@ogretmen_giris_gerekli
def api_seb_cikis_toplu_onayla():
    with db_baglantisi() as db:
        db.execute("UPDATE seb_cikis_talepleri SET durum='onaylandi' WHERE tarih=? AND durum='bekliyor'", (bugun(),))
        db.commit()
    return jsonify({'durum': 'ok'})

@api_bp.route('/yardim_talep', methods=['POST'])
def api_yardim_talep():
    from flask import session
    numara = session.get('numara')
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Oturum yok'})
        
    ad_soyad = f"{session.get('ad', '')} {session.get('soyad', '')}".strip()
    
    with db_baglantisi() as db:
        mevcut = db.execute("SELECT id, durum FROM yardim_talepleri WHERE numara=? AND tarih=? AND durum != 'tamamlandi'", (numara, bugun())).fetchone()
        if mevcut:
            return jsonify({'durum': 'ok', 'mesaj': 'Zaten aktif bir yardım talebiniz var.'})
            
        db.execute(
            'INSERT INTO yardim_talepleri (tarih, saat, numara, ad_soyad, durum) VALUES (?, ?, ?, ?, ?)',
            (bugun(), simdi(), numara, ad_soyad, 'bekliyor')
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
    return jsonify({'durum': 'ok', 'mesaj': f'{numara} numaralı öğrenci silindi'})

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

