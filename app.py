"""
Ders Takip Sistemi — Flask Sunucusu
Kapadokya Üniversitesi Linux Dersleri

Başlatmak için:
    python3 app.py

Öğretmen paneli: http://localhost:3333/teacher
"""

import eventlet
eventlet.monkey_patch()

import os
import csv
import sqlite3
import io
import pty
import select
import struct
import fcntl
import termios
import subprocess
import signal
import threading
from datetime import datetime
from functools import wraps
from pathlib import Path

import requests
from flask import (Flask, render_template, request, jsonify,
                   redirect, url_for, send_file, session, abort, Response)
from flask_socketio import SocketIO, emit, join_room, leave_room, Namespace

from docker_terminal import (container_baslat, container_ip_al,
                               container_durum, image_var_mi)

# ── Yapılandırma ──────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent
DB_YOLU       = BASE_DIR / 'data' / 'yoklama.db'
SLAYT_DIR     = BASE_DIR / 'slaytlar'
GORSELLER_DIR = BASE_DIR.parent / '01_SUNUMLAR' / 'gorseller'
OGRETMEN_SIFRE = 'linux2024'   # İstersen değiştir
SECRET_KEY = 'kapadokya-linux-2024'

# ── Uygulama ──────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Static dosyaları cache'leme
log = app.logger

# ── SocketIO ─────────────────────────────────────────────────
# eventlet ile daha performanslı ve stabil WebSocket desteği
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Ders durumu (bellek içi)
ders_durumu = {
    'mod':   'bekleme',   # bekleme | slayt
    'dosya': '',           # aktif slayt dosyası
    'terminal_url': '/terminal'
}

@app.route('/favicon.ico')
def favicon():
    return Response(status=204)

# ── Veritabanı ve Yardımcılar ─────────────────────────────────
def db_baglantisi():
    DB_YOLU.parent.mkdir(exist_ok=True)
    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.row_factory = sqlite3.Row
    return baglanti

def db_olustur():
    with db_baglantisi() as db:
        # Ana yoklama tablosu
        db.execute("""
            CREATE TABLE IF NOT EXISTS yoklama (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih     TEXT NOT NULL,
                ad_soyad  TEXT NOT NULL,
                numara    TEXT NOT NULL,
                saat      TEXT NOT NULL,
                sinif     TEXT NOT NULL DEFAULT ''
            )
        """)
        # Migration: eski veritabanına eksik kolonları ekle
        try:
            db.execute("ALTER TABLE yoklama ADD COLUMN sinif TEXT NOT NULL DEFAULT ''")
        except Exception:
            pass
        try:
            db.execute("ALTER TABLE yoklama ADD COLUMN paket TEXT NOT NULL DEFAULT '—'")
        except Exception:
            pass
        try:
            db.execute("ALTER TABLE yoklama ADD COLUMN ip TEXT NOT NULL DEFAULT ''")
        except Exception:
            pass
        try:
            db.execute("ALTER TABLE yoklama ADD COLUMN kaynak TEXT NOT NULL DEFAULT 'web'")
        except Exception:
            pass

        # Sınıf listesi tablosu
        db.execute("""
            CREATE TABLE IF NOT EXISTS siniflar (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                ad   TEXT UNIQUE NOT NULL
            )
        """)

        # Kayıtlı öğrenci tablosu (whitelist)
        db.execute("""
            CREATE TABLE IF NOT EXISTS ogrenciler (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                sinif_id  INTEGER NOT NULL REFERENCES siniflar(id),
                numara    TEXT UNIQUE NOT NULL,
                ad        TEXT NOT NULL,
                soyad     TEXT NOT NULL,
                sifre     TEXT NOT NULL DEFAULT ''
            )
        """)
        # Migration: eski veritabanına sifre kolonunu ekle
        try:
            db.execute("ALTER TABLE ogrenciler ADD COLUMN sifre TEXT NOT NULL DEFAULT ''")
        except Exception:
            pass

        # Şüpheli giriş denemeleri logu (başkası adına imza atma)
        db.execute("""
            CREATE TABLE IF NOT EXISTS sahte_giris_log (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih          TEXT NOT NULL,
                saat           TEXT NOT NULL,
                ip             TEXT NOT NULL,
                gercek_numara  TEXT NOT NULL,
                gercek_ad      TEXT NOT NULL,
                denenen_numara TEXT NOT NULL,
                denenen_ad     TEXT NOT NULL,
                sinif          TEXT NOT NULL DEFAULT ''
            )
        """)

        # Terminal güvenlik logu (yanlış öğrenci terminal erişimi)
        db.execute("""
            CREATE TABLE IF NOT EXISTS terminal_guvenlik_log (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih          TEXT NOT NULL,
                saat           TEXT NOT NULL,
                ip             TEXT NOT NULL,
                session_numara TEXT NOT NULL,
                session_ad     TEXT NOT NULL,
                girilen_numara TEXT NOT NULL,
                durum          TEXT NOT NULL,
                uyari_gonderildi INTEGER DEFAULT 0
            )
        """)
        db.commit()

# ── Yardımcı ──────────────────────────────────────────────────
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

def ogretmen_giris_gerekli(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('ogretmen'):
            # JSON API için 401 dön, sayfa için redirect
            if request.path.startswith('/api/'):
                return jsonify({'hata': 'Öğretmen girişi gerekli'}), 401
            return redirect(url_for('ogretmen_giris'))
        return f(*args, **kwargs)
    return decorated

# ── Öğrenci Rotaları ──────────────────────────────────────────
PAKET_SECENEKLERI = [
    '1. Paket (09:00-11:35)',
    '2. Paket (12:40-15:15)',
    '3. Paket (15:25-18:00)',
]

@app.route('/')
def ana():
    """Ana sayfa - Giriş formu veya Öğrenci Paneli."""
    # Eğer zaten giriş yapmışsa, paneli göster (PRG için)
    if session.get('numara'):
        tarih = bugun()
        with db_baglantisi() as db:
            yoklama = db.execute(
                'SELECT ad_soyad, saat, paket FROM yoklama WHERE tarih=? AND numara=? ORDER BY id DESC LIMIT 1',
                (tarih, session['numara'])
            ).fetchone()
            
            if yoklama:
                # Session'da ad/soyad eksikse (eski oturum), veritabanından tamamla
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

@app.route('/giris', methods=['POST'])
def giris():
    sinif_id  = request.form.get('sinif_id', '').strip()
    ad_soyad  = request.form.get('ad_soyad', '').strip().upper()
    numara    = request.form.get('numara', '').strip()
    ders_paketi = request.form.get('ders_paketi', '').strip()

    siniflar = sinif_listesi()

    # Hata durumunda formu tekrar göstermek için yardımcı
    def hata_goster(mesaj):
        return render_template('login.html',
                               hata=mesaj,
                               siniflar=siniflar,
                               paket_secenekleri=PAKET_SECENEKLERI,
                               paket_varsayilan=ders_paketi or paket_hesapla())

    if not sinif_id or not ad_soyad or not numara or not ders_paketi:
        return hata_goster('Lütfen tüm alanları doldurun.')

    # Paket doğrulma
    if ders_paketi not in PAKET_SECENEKLERI:
        ders_paketi = paket_hesapla()   # Geçersizse saate göre dön

    # ── Whitelist kontrolü ──
    with db_baglantisi() as db:
        ogrenci = db.execute(
            'SELECT ad, soyad, numara FROM ogrenciler WHERE ad || " " || soyad=? AND sinif_id=?',
            (ad_soyad, sinif_id)
        ).fetchone()

    if not ogrenci:
        return hata_goster('Bu öğrenci numarası seçili sınıfa kayıtlı değil.')

    # Şifre kontrolü (öğrenci numarası ile)
    if ogrenci['numara'] != numara:
        return hata_goster('Hatalı şifre!')

    saat      = simdi()
    tarih     = bugun()
    istemci   = istemci_ip()

    with db_baglantisi() as db:
        # Sınıf adını al
        sinif_row = db.execute('SELECT ad FROM siniflar WHERE id=?', (sinif_id,)).fetchone()
        sinif_ad  = sinif_row['ad'] if sinif_row else ''

        # ── 1. AYNI IP'DEN FARKLI ÖĞRENCİ KONTROLÜ ────────────────────
        # Aynı IP'den bugün BU PAKET'te FARKLI bir öğrenci giriş yapmış mı?
        # (Aynı öğrenci tekrar giriyorsa NUMARA AYNI olacağı için atlanır)
        ip_var_mi = db.execute(
            "SELECT DISTINCT numara FROM yoklama WHERE tarih=? AND ip=? AND paket=? AND kaynak='web'",
            (tarih, istemci, ders_paketi)
        ).fetchall()

        # Birden fazla farklı numara varsa ve girilen numara bunlardan farklıysa şüpheli
        if ip_var_mi:
            ip_numaralar = {row['numara'] for row in ip_var_mi}
            if numara not in ip_numaralar and len(ip_numaralar) > 0:
                # Şüpheli! Aynı IP'den FARKLI numara giriliyor
                # ── Şüpheli girişi logla ──────────────────────────────
                db.execute(
                    'INSERT INTO sahte_giris_log '
                    '(tarih, saat, ip, gercek_numara, gercek_ad, denenen_numara, denenen_ad, sinif) '
                    'VALUES (?,?,?,?,?,?,?,?)',
                    (tarih, saat, istemci,
                     list(ip_numaralar)[0],  # İlk numara
                     'Aynı IP',  # Gerçek ad (IP logu)
                     numara, ad_soyad,
                     sinif_ad)
                )
                db.commit()
                # ─────────────────────────────────────────────────────
                return hata_goster(f'Bu cihazdan bugün başka öğrenci numaraları girildi: {", ".join(ip_numaralar)}. '
                                  f'Başkası adına giriş yapılamaz.')

        # ── 2. AYNI NUMARA DAHA ÖNCE GİRİŞ YAPMIŞ KONTROLÜ ───────────
        # Aynı gün aynı numara BU PAKET'te daha önce girmiş mi?
        var_mi = db.execute(
            'SELECT id, saat FROM yoklama WHERE tarih=? AND numara=? AND paket=?',
            (tarih, numara, ders_paketi)
        ).fetchone()
        if var_mi:
            # Öğrenci zaten giriş yapmış
            session['numara'] = numara
            session['ad'] = ogrenci['ad']
            session['soyad'] = ogrenci['soyad']
            return redirect(url_for('ana'))

        # ── 3. YENİ KAYIT ──────────────────────────────────────────
        db.execute(
            'INSERT INTO yoklama (tarih, ad_soyad, numara, saat, sinif, paket, ip, kaynak) '
            'VALUES (?,?,?,?,?,?,?,?)',
            (tarih, ad_soyad, numara, saat, sinif_ad, ders_paketi, istemci, 'web')
        )
        db.commit()

    # Öğrenci session bilgileri (terminal sayfası için gerekli)
    session['numara'] = numara
    session['ad'] = ogrenci['ad']
    session['soyad'] = ogrenci['soyad']

    # Chroot ortamını login sırasında otomatik oluştur (hız için)
    try:
        from chroot_terminal import chroot_olustur, chroot_var_mi
        if not chroot_var_mi(numara):
            log.info(f"Oturum açıldı, chroot otomatik oluşturuluyor: {numara}")
            threading.Thread(target=chroot_olustur, args=(numara,)).start()
    except Exception as e:
        log.error(f"Otomatik chroot oluşturma hatası: {e}")

    return redirect(url_for('ana'))

@app.route('/api/durum')
def api_durum():
    # Öğrenci için durum
    # Eğer öğretmenden hash query parametresi geldiyse, kaydet (Cloudflare Access CORS sorunu için)
    hash_param = request.args.get('hash', '')
    if hash_param:
        ders_durumu['slayt_hash'] = hash_param

    response = {
        'mod': ders_durumu['mod'],
        'dosya': ders_durumu['dosya'],
        'slayt_hash': ders_durumu.get('slayt_hash', ''),
        'terminal_url': ders_durumu.get('terminal_url', '')
    }
    return jsonify(response)

@app.route('/api/slayt_hash', methods=['POST'])
@ogretmen_giris_gerekli
def api_slayt_hash():
    """Öğretmen slayt içinde gezindiğinde hash'i kaydet"""
    veri = request.get_json() or {}
    hash = veri.get('hash', '')

    if hash:
        ders_durumu['slayt_hash'] = hash

    return jsonify({'durum': 'ok'})

@app.route('/slayt/<path:dosya_adi>')
def slayt_goster(dosya_adi):
    slayt_yolu = SLAYT_DIR / dosya_adi
    if not slayt_yolu.exists() or slayt_yolu.suffix != '.html':
        abort(404)
    return send_file(slayt_yolu)

@app.route('/gorseller/<path:dosya_adi>')
def gorseller_goster(dosya_adi):
    """Marp slaytlarının kullandığı arka plan görselleri"""
    gorsel_yolu = GORSELLER_DIR / dosya_adi
    if not gorsel_yolu.exists():
        abort(404)
    return send_file(gorsel_yolu)

# ── Öğretmen Rotaları ─────────────────────────────────────────
@app.route('/teacher/login', methods=['GET', 'POST'])
def ogretmen_giris():
    hata = None
    if request.method == 'POST':
        if request.form.get('sifre') == OGRETMEN_SIFRE:
            session['ogretmen'] = True
            return redirect(url_for('ogretmen_panel'), 303)
        hata = 'Hatalı şifre!'
    return render_template('ogretmen_giris.html', hata=hata)

@app.route('/teacher/logout')
def ogretmen_cikis():
    session.pop('ogretmen', None)
    return redirect(url_for('ogretmen_giris'))

@app.route('/teacher')
@ogretmen_giris_gerekli
def ogretmen_panel():
    return render_template(
        'ogretmen.html',
        tarih=bugun(),
        slaytlar=slayt_listesi(),
        aktif_mod=ders_durumu['mod'],
        aktif_dosya=ders_durumu['dosya']
    )

@app.route('/api/mod', methods=['POST'])
@ogretmen_giris_gerekli
def api_mod_degistir():
    veri = request.get_json()
    if veri.get('mod') in ('bekleme', 'slayt', 'terminal'):
        log.info(f"Mod Değişimi: {ders_durumu['mod']} -> {veri.get('mod')} (Dosya: {veri.get('dosya')}, Terminal URL: {veri.get('terminal_url')})")
        ders_durumu['mod']   = veri['mod']
        ders_durumu['dosya'] = veri.get('dosya', '')
        ders_durumu['terminal_url'] = veri.get('terminal_url', '')

        # Hash'i sıfırla (slayt moduna geçildiğinde)
        if 'slayt_hash' in veri and not veri['slayt_hash']:
            ders_durumu['slayt_hash'] = ''

    return jsonify({'durum': 'ok', 'mod': ders_durumu['mod']})

@app.route('/api/config', methods=['POST'])
@ogretmen_giris_gerekli
def api_config():
    veri = request.get_json()
    if 'chroot_host' in veri:
        ders_durumu['chroot_host'] = veri['chroot_host']
        # chroot_terminal modülündeki IP'yi güncelle
        try:
            import chroot_terminal
            chroot_terminal.CT_991_HOST = veri['chroot_host']
        except:
            pass
            
    if 'ttyd_url' in veri:
        ders_durumu['terminal_url'] = veri['ttyd_url']
        
    return jsonify({'durum': 'ok'})

@app.route('/api/yoklama')
@ogretmen_giris_gerekli
def api_yoklama():
    with db_baglantisi() as db:
        satirlar = db.execute(
            'SELECT ad_soyad, numara, saat, sinif, paket, kaynak FROM yoklama WHERE tarih=? ORDER BY saat',
            (bugun(),)
        ).fetchall()
    return jsonify({
        'tarih':      bugun(),
        'ogrenciler': [dict(s) for s in satirlar]
    })

@app.route('/api/siniflar')
@ogretmen_giris_gerekli
def api_siniflar():
    """Sınıf bazlı kayıtlı ve bugün gelen öğrenci sayıları."""
    with db_baglantisi() as db:
        siniflar = db.execute('SELECT id, ad FROM siniflar ORDER BY ad').fetchall()
        sonuc = []
        for s in siniflar:
            kayitli = db.execute(
                'SELECT COUNT(*) as sayi FROM ogrenciler WHERE sinif_id=?', (s['id'],)
            ).fetchone()['sayi']
            bugunki = db.execute(
                'SELECT COUNT(*) as sayi FROM yoklama WHERE tarih=? AND sinif=?',
                (bugun(), s['ad'])
            ).fetchone()['sayi']
            sonuc.append({
                'id': s['id'],
                'ad': s['ad'],
                'kayitli': kayitli,
                'bugun': bugunki
            })
    return jsonify({'siniflar': sonuc})

@app.route('/api/ogrenci_listesi/<int:sinif_id>')
def api_ogrenci_listesi(sinif_id):
    """Bir sınıftaki öğrenci listesi — giriş formu dropdown'u için (public)."""
    with db_baglantisi() as db:
        ogrenciler = db.execute(
            'SELECT numara, ad, soyad FROM ogrenciler WHERE sinif_id=? ORDER BY soyad, ad',
            (sinif_id,)
        ).fetchall()
    return jsonify({
        'ogrenciler': [
            {
                'numara':   o['numara'],
                'ad_soyad': (o['ad'] + ' ' + o['soyad']).upper()
            }
            for o in ogrenciler
        ]
    })

@app.route('/api/sinif_ogrencileri/<int:sinif_id>')
@ogretmen_giris_gerekli
def api_sinif_ogrencileri(sinif_id):
    """Bir sınıftaki tüm kayıtlı öğrencileri + bugün gelip gelmediklerini döndür."""
    with db_baglantisi() as db:
        ogrenciler = db.execute(
            'SELECT numara, ad, soyad FROM ogrenciler WHERE sinif_id=? ORDER BY soyad, ad',
            (sinif_id,)
        ).fetchall()
        bugunki = {
            r['numara']: r['paket'] for r in db.execute(
                'SELECT numara, paket FROM yoklama WHERE tarih=?', (bugun(),)
            ).fetchall()
        }
    return jsonify({
        'ogrenciler': [
            {
                'numara':   o['numara'],
                'ad_soyad': o['ad'] + ' ' + o['soyad'],
                'geldi':    o['numara'] in bugunki,
                'paket':    bugunki.get(o['numara'], '')
            }
            for o in ogrenciler
        ]
    })

@app.route('/api/manuel_giris', methods=['POST'])
@ogretmen_giris_gerekli
def api_manuel_giris():
    """Öğretmen bir öğrenciyi manuel olarak giriş yapmış sayar (notebook bozuk vs.)."""
    veri = request.get_json()
    sinif_id = veri.get('sinif_id')
    numara   = veri.get('numara')

    if not sinif_id or not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Eksik parametre'}), 400

    with db_baglantisi() as db:
        ogrenci = db.execute(
            'SELECT ad, soyad FROM ogrenciler WHERE numara=? AND sinif_id=?',
            (numara, sinif_id)
        ).fetchone()
        if not ogrenci:
            return jsonify({'durum': 'hata', 'mesaj': 'Öğrenci bulunamadı'}), 404

        sinif_row = db.execute('SELECT ad FROM siniflar WHERE id=?', (sinif_id,)).fetchone()
        sinif_ad  = sinif_row['ad'] if sinif_row else ''

        tarih = bugun()
        paket = paket_hesapla()
        var_mi = db.execute(
            'SELECT id FROM yoklama WHERE tarih=? AND numara=? AND paket=?',
            (tarih, numara, paket)
        ).fetchone()
        if var_mi:
            return jsonify({'durum': 'hata', 'mesaj': 'Bu öğrenci bugün bu pakette zaten kayıtlı'}), 409

        tam_ad = (ogrenci['ad'] + ' ' + ogrenci['soyad']).upper()
        saat   = simdi()

        db.execute(
            'INSERT INTO yoklama (tarih, ad_soyad, numara, saat, sinif, paket, ip, kaynak) '
            'VALUES (?,?,?,?,?,?,?,?)',
            (tarih, tam_ad, numara, saat, sinif_ad, paket, 'manuel', 'manuel')
        )
        db.commit()

    return jsonify({'durum': 'ok', 'ad_soyad': tam_ad, 'saat': saat, 'paket': paket})

@app.route('/api/sahte_log')
@ogretmen_giris_gerekli
def api_sahte_log():
    """Başkası adına giriş denemeleri logu (tüm zamanlar, en yeni önce)."""
    with db_baglantisi() as db:
        kayitlar = db.execute(
            'SELECT id, tarih, saat, ip, gercek_numara, gercek_ad, '
            '       denenen_numara, denenen_ad, sinif '
            'FROM sahte_giris_log '
            'ORDER BY tarih DESC, saat DESC'
        ).fetchall()
    return jsonify({'kayitlar': [dict(k) for k in kayitlar]})

@app.route('/api/sahte_log/sil_tek', methods=['POST'])
@ogretmen_giris_gerekli
def api_sahte_log_sil_tek():
    """Tek bir şüpheli giriş kaydını sil."""
    veri = request.get_json()
    kayit_id = veri.get('id') if veri else None

    if not kayit_id:
        return jsonify({'durum': 'hata', 'mesaj': 'ID gerekli'}), 400

    with db_baglantisi() as db:
        silinen = db.execute('DELETE FROM sahte_giris_log WHERE id=?', (kayit_id,))
        db.commit()

    if silinen.rowcount == 0:
        return jsonify({'durum': 'hata', 'mesaj': 'Kayıt bulunamadı'}), 404

    return jsonify({'durum': 'ok', 'silinen': 1})

@app.route('/api/yoklama/csv')
@ogretmen_giris_gerekli
def api_yoklama_csv():
    """Bugünkü yoklamayı CSV olarak dışa aktar."""
    with db_baglantisi() as db:
        satirlar = db.execute(
            'SELECT ad_soyad, numara, saat, sinif, paket, kaynak FROM yoklama WHERE tarih=? ORDER BY sinif, saat',
            (bugun(),)
        ).fetchall()

    # Tarih formatı: 202603011135
    tarih_timestamp = datetime.now().strftime('%Y%m%d%H%M')
    dosya_adi = f"yoklama_{tarih_timestamp}.csv"

    cikti = io.StringIO()
    yazar = csv.writer(cikti)
    yazar.writerow(['Tarih', 'Saat', 'Ad Soyad', 'Öğrenci No', 'Sınıf', 'Paket', 'Kaynak'])
    for s in satirlar:
        yazar.writerow([
            bugun(),
            s['saat'],
            s['ad_soyad'],
            s['numara'],
            s['sinif'],
            s['paket'],
            s['kaynak']
        ])

    cikti.seek(0)

    return send_file(
        io.BytesIO(cikti.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=dosya_adi
    )

@app.route('/api/yoklama/tarih_csv')
@ogretmen_giris_gerekli
def api_yoklama_tarih_csv():
    """Belirli bir tarih için yoklama CSV export."""
    from flask import request
    tarih_param = request.args.get('tarih', bugun())  # Format: 2026-03-01

    # Tarih formatını düzelt
    try:
        # YYYY-MM-DD formatını YYYYMMDD'ye çevir
        tarih_parts = tarih_param.split('-')
        if len(tarih_parts) == 3:
            tarih_db = '-'.join(tarih_parts)  # YYYY-MM-DD
        else:
            # Zaten YYYYMMDD formatında mı?
            if len(tarih_param) == 8 and tarih_param.isdigit():
                tarih_db = f"{tarih_param[:4]}-{tarih_param[4:6]}-{tarih_param[6:8]}"
            else:
                return jsonify({'durum': 'hata', 'mesaj': 'Geçersiz tarih formatı. YYYY-MM-DD veya YYYYMMDD kullanın.'}), 400
    except:
        tarih_db = bugun()

    with db_baglantisi() as db:
        satirlar = db.execute(
            'SELECT ad_soyad, numara, saat, sinif, paket, kaynak FROM yoklama WHERE tarih=? ORDER BY sinif, saat',
            (tarih_db,)
        ).fetchall()

    if not satirlar:
        return jsonify({'durum': 'hata', 'mesaj': f'{tarih_db} tarihinde kayıt bulunamadı.'}), 404

    # Tarih formatı: 202603011135
    tarih_obj = datetime.strptime(tarih_db, '%Y-%m-%d')
    tarih_timestamp = tarih_obj.strftime('%Y%m%d%H%M')
    dosya_adi = f"yoklama_{tarih_timestamp}.csv"

    cikti = io.StringIO()
    yazar = csv.writer(cikti)
    yazar.writerow(['Tarih', 'Saat', 'Ad Soyad', 'Öğrenci No', 'Sınıf', 'Paket', 'Kaynak'])
    for s in satirlar:
        yazar.writerow([
            tarih_db,
            s['saat'],
            s['ad_soyad'],
            s['numara'],
            s['sinif'],
            s['paket'],
            s['kaynak']
        ])

    cikti.seek(0)

    return send_file(
        io.BytesIO(cikti.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=dosya_adi
    )

@app.route('/api/yoklama/csv_manuel', methods=['POST'])
@ogretmen_giris_gerekli
def api_yoklama_csv_manuel():
    """Manuel olarak istenen tarih için CSV export."""
    veri = request.get_json()
    tarih = veri.get('tarih', '') if veri else ''

    if not tarih:
        return jsonify({'durum': 'hata', 'mesaj': 'Tarih gerekli'}), 400

    # Tarih formatı düzeltme
    try:
        if '-' in tarih:
            # YYYY-MM-DD formatı
            tarih_db = tarih
            tarih_obj = datetime.strptime(tarih, '%Y-%m-%d')
        else:
            # YYYYMMDD formatı
            tarih_obj = datetime.strptime(tarih, '%Y%m%d')
            tarih_db = tarih_obj.strftime('%Y-%m-%d')
    except ValueError:
        return jsonify({'durum': 'hata', 'mesaj': 'Geçersiz tarih formatı. YYYY-MM-DD kullanın.'}), 400

    with db_baglantisi() as db:
        satirlar = db.execute(
            'SELECT ad_soyad, numara, saat, sinif, paket, kaynak FROM yoklama WHERE tarih=? ORDER BY sinif, saat',
            (tarih_db,)
        ).fetchall()

    if not satirlar:
        return jsonify({'durum': 'hata', 'mesaj': f'{tarih_db} tarihinde kayıt bulunamadı.'}), 404

    # Tarih formatı: 202603011135
    tarih_timestamp = tarih_obj.strftime('%Y%m%d%H%M')
    dosya_adi = f"yoklama_{tarih_timestamp}.csv"

    cikti = io.StringIO()
    yazar = csv.writer(cikti)
    yazar.writerow(['Tarih', 'Saat', 'Ad Soyad', 'Öğrenci No', 'Sınıf', 'Paket', 'Kaynak'])
    for s in satirlar:
        yazar.writerow([
            tarih_db,
            s['saat'],
            s['ad_soyad'],
            s['numara'],
            s['sinif'],
            s['paket'],
            s['kaynak']
        ])

    cikti.seek(0)

    return send_file(
        io.BytesIO(cikti.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=dosya_adi
    )

@app.route('/api/yoklama/sil', methods=['POST'])
@ogretmen_giris_gerekli
def api_yoklama_sil():
    """Bugünkü yoklamayı temizle."""
    veri = request.get_json()
    onay = veri.get('onay') if veri else False

    if not onay:
        return jsonify({'durum': 'hata', 'mesaj': 'Onay gerekli'}), 400

    with db_baglantisi() as db:
        silinen = db.execute('DELETE FROM yoklama WHERE tarih=?', (bugun(),))
        db.commit()

    return jsonify({'durum': 'ok', 'silinen': silinen.rowcount})

@app.route('/api/yoklama/sil_tek', methods=['POST'])
@ogretmen_giris_gerekli
def api_yoklama_sil_tek():
    """Tek bir öğrenci kaydını sil."""
    veri = request.get_json()
    numara = veri.get('numara') if veri else None

    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Numara gerekli'}), 400

    with db_baglantisi() as db:
        silinen = db.execute(
            'DELETE FROM yoklama WHERE tarih=? AND numara=?',
            (bugun(), numara)
        )
        db.commit()

    if silinen.rowcount == 0:
        return jsonify({'durum': 'hata', 'mesaj': 'Kayıt bulunamadı'}), 404

    return jsonify({'durum': 'ok', 'silinen': 1})

@app.route('/api/terminal/guvenlik_log')
@ogretmen_giris_gerekli
def api_terminal_guvenlik_log():
    """Terminal güvenlik loglarını getir."""
    with db_baglantisi() as db:
        loglar = db.execute("""
            SELECT * FROM terminal_guvenlik_log
            ORDER BY id DESC
            LIMIT 50
        """).fetchall()

    return jsonify({
        'loglar': [
            {
                'id': l['id'],
                'tarih': l['tarih'],
                'saat': l['saat'],
                'ip': l['ip'],
                'session_numara': l['session_numara'],
                'session_ad': l['session_ad'],
                'girilen_numara': l['girilen_numara'],
                'durum': l['durum']
            }
            for l in loglar
        ]
    })

# ── Terminal Rotaları ─────────────────────────────────────────
@app.route('/terminal', strict_slashes=False)
def terminal_sayfasi():
    """Terminal doğrulama ve otomatik yönlendirme sayfası."""
    # Ana oturumda numara var mı?
    if not session.get('numara'):
        return render_template('terminal_login.html', hata='Önce ana sayfadan giriş yapmalısınız.')

    # OTOMATİK GİRİŞ (User request: Student terminal should open automatically)
    # Eğer terminal oturumu yoksa veya farklıysa, otomatik oluştur
    session_numara = session['numara']
    session_ad = session.get('ad', '')
    session_soyad = session.get('soyad', '')

    if session.get('terminal_numara') != session_numara:
        # Chroot kontrol/yarat
        from chroot_terminal import chroot_var_mi, chroot_olustur, chroot_ip_al
        if not chroot_var_mi(session_numara):
            log.info(f"Otomatik terminal girişi için chroot oluşturuluyor: {session_numara}")
            chroot_olustur(session_numara, session_ad, session_soyad)
            
        ssh_ip = chroot_ip_al(session_numara)
        session['terminal_numara'] = session_numara
        session['terminal_ad'] = session_ad
        session['terminal_soyad'] = session_soyad
        session['terminal_ip'] = ssh_ip
        
        # Logla (başarılı otomatik giriş)
        try:
            with db_baglantisi() as db:
                db.execute("""
                    INSERT INTO terminal_guvenlik_log
                    (tarih, saat, ip, session_numara, session_ad, girilen_numara, durum)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (bugun(), simdi(), istemci_ip(), session_numara, f"{session_ad} {session_soyad}".strip(), session_numara, 'OTOMATIK_GIRIS'))
                db.commit()
        except Exception as e:
            log.error(f"Terminal loglama hatası: {e}")

    return redirect('/terminal/workspace')


@app.route('/terminal/login', methods=['POST'])
def terminal_login():
    """Terminal login ve güvenlik kontrolü."""
    # Session bilgileri (Artık hepsi 'numara', 'ad', 'soyad' altında)
    session_numara = session.get('numara', '')
    session_ad = session.get('ad', '')
    session_soyad = session.get('soyad', '')
    session_ad_soyad = f"{session_ad} {session_soyad}".strip()

    # Formdan gelen doğrulama
    girilen_numara = request.form.get('numara_dogrulama', '').strip()

    # Validasyon
    if not girilen_numara:
        return render_template('terminal_guvenlik.html',
                               session_numara=session_numara,
                               session_ad=session_ad,
                               session_soyad=session_soyad,
                               session_ad_soyad=f"{session_ad} {session_soyad}".strip(),
                               hata='Lütfen numaranızı girin.')

    if not girilen_numara.isdigit():
        return render_template('terminal_guvenlik.html',
                               session_numara=session_numara,
                               session_ad=session_ad,
                               session_soyad=session_soyad,
                               session_ad_soyad=f"{session_ad} {session_soyad}".strip(),
                               hata='Numara sadece rakamlardan oluşmalı.')

    # GÜVENLİK KONTROLÜ
    ip = istemci_ip()
    session_ad_soyad = f"{session_ad} {session_soyad}".strip()

    if girilen_numara == session_numara:
        # ✅ BAŞARILI: Aynı öğrenci
        durum = 'BASARILI'

        # Logla (başarılı)
        with db_baglantisi() as db:
            db.execute("""
                INSERT INTO terminal_guvenlik_log
                (tarih, saat, ip, session_numara, session_ad, girilen_numara, durum)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (bugun(), simdi(), ip, session_numara, session_ad_soyad, girilen_numara, durum))
            db.commit()

        # Chroot ortamını kontrol et/yarat
        from chroot_terminal import chroot_var_mi, chroot_olustur, chroot_ip_al

        if not chroot_var_mi(girilen_numara):
            # Chroot ortamı yok, oluştur
            log.info(f"Chroot ortamı oluşturuluyor: {girilen_numara}")
            chroot_olustur(girilen_numara, session_ad, session_soyad)

        # SSH IP adresini al
        ssh_ip = chroot_ip_al(girilen_numara)

        # Session bilgilerini sakla (Terminal çalışma alanı için spesifik değil, genel kullanıyoruz)
        session['terminal_numara'] = girilen_numara
        session['terminal_ad'] = session_ad
        session['terminal_soyad'] = session_soyad
        session['terminal_ip'] = ssh_ip

        return redirect('/terminal/workspace')

    else:
        # ❌ GÜVENLİK İHLALİ: Farklı öğrenci!
        durum = 'GUVENLIK_IHLALI'

        # Logla (başarısız + alarm)
        with db_baglantisi() as db:
            log_id = db.execute("""
                INSERT INTO terminal_guvenlik_log
                (tarih, saat, ip, session_numara, session_ad, girilen_numara, durum)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (bugun(), simdi(), ip, session_numara, session_ad_soyad, girilen_numara, durum))
            db.commit()

        # Öğretmene bildirim gönder (WebSocket)
        try:
            mesaj = (
                f"⚠️ GÜVENLİK UYARISI ⚠️\n\n"
                f"Terminal Erişim İhlali!\n\n"
                f"Oturum açan: {session_ad_soyad} ({session_numara})\n"
                f"Girmeye çalışan: {girilen_numara}\n"
                f"IP: {ip}\n"
                f"Tarih: {bugun()} {simdi()}"
            )
            socketio.emit('guvenlik_uyari', mesaj, namespace='/terminal')
        except Exception as e:
            log.error(f"Öğretmen bildirimi hatası: {e}")

        # Öğrenciye uyarı göster
        return render_template('terminal_guvenlik.html',
                               session_numara=session_numara,
                               session_ad=session_ad,
                               session_soyad=session_soyad,
                               session_ad_soyad=session_ad_soyad,
                               hata=(
                                   f"⚠️ GÜVENLİK UYARISI!\n\n"
                                   f"Bu terminal {session_numara} numaralı öğrenci içindir.\n"
                                   f"Siz {girilen_numara} numarasını girdiniz.\n\n"
                                   f"Bu erişim girişimi LOGlanmıştır ve öğretmene "
                                   f"bildirilmiştir."
                               ))


@app.route('/terminal/workspace')
def terminal_workspace():
    """Terminal çalışma alanı - authentication gerekli."""
    if not session.get('terminal_numara'):
        return redirect('/terminal')

    numara = session['terminal_numara']
    ad = session['terminal_ad']
    soyad = session['terminal_soyad']
    ip = session['terminal_ip']

    return render_template('terminal_workspace.html',
                           numara=numara,
                           ad_soyad=f"{ad} {soyad}".upper(),
                           container_ip=ip)

@app.route('/teacher/terminal')
@ogretmen_giris_gerekli
def ogretmen_terminal_sayfasi():
    """Öğretmen terminal yayın sayfası."""
    return render_template('ogretmen_terminal.html')

@app.route('/api/terminal/durum')
@ogretmen_giris_gerekli
def api_terminal_durum():
    """Terminal sistemi durum bilgisi."""
    return jsonify({
        'image_hazir': image_var_mi(),
        'konteyner_calisiyor': container_durum(),
        'bagli_ogrenciler': len(ogrenci_sidleri)
    })


# ── SocketIO Terminal Olayları ────────────────────────────────
# Global terminal süreçleri takibi
ogrenci_surecleri = {}  # {sid: (process, master_fd)}
ogrenci_sidleri   = {}  # {sid: username}
ogrenci_pty_locks = {}  # {fd: threading.Lock()} - Eventlet çakışmasını önlemek için

ogretmen_pty_fd   = None
ogretmen_pty_pid  = None
ogretmen_pty_lock = threading.Lock()
ogretmen_sid = None
ogretmen_komut_tampon = ""

# Öğrenci Docker exec süreçleri: {sid: (subprocess.Popen, fd)}
ogrenci_surecleri = {}


def _pty_oku_ve_yayinla(fd, hedef_event, hedef_room=None, broadcast=False):
    """PTY'den oku ve SocketIO ile yayınla (thread içinde çalışır)."""
    while True:
        try:
            r, _, _ = select.select([fd], [], [], 0.1)
            if r:
                data = os.read(fd, 4096)
                if not data:
                    break
                text = data.decode('utf-8', errors='replace')
                if broadcast:
                    socketio.emit(hedef_event, text, namespace='/terminal')
                elif hedef_room:
                    socketio.emit(hedef_event, text, room=hedef_room, namespace='/terminal')
        except (OSError, IOError):
            break


@socketio.on('connect', namespace='/terminal')
def terminal_baglan():
    pass


@socketio.on('disconnect', namespace='/terminal')
def terminal_kopma():
    global ogretmen_sid, ogretmen_pty_fd, ogretmen_pty_pid
    sid = request.sid

    # Öğretmen mi?
    if sid == ogretmen_sid:
        if ogretmen_pty_pid:
            try:
                os.kill(ogretmen_pty_pid, signal.SIGHUP)
            except ProcessLookupError:
                pass
        ogretmen_sid = None
        ogretmen_pty_fd = None
        ogretmen_pty_pid = None
        return

    # Öğrenci mi?
    if sid in ogrenci_sidleri:
        numara = ogrenci_sidleri.pop(sid, None)
        # Docker exec sürecini kapat
        if sid in ogrenci_surecleri:
            proc, fd = ogrenci_surecleri.pop(sid)
            try:
                os.close(fd)
            except OSError:
                pass
            try:
                proc.terminate()
            except Exception:
                pass
        # Single container approach - individual container durdurma gerekmez

        # Öğrenci sayısını güncelle
        if ogretmen_sid:
            socketio.emit('bagli_ogrenci_sayisi', len(ogrenci_sidleri),
                          room=ogretmen_sid, namespace='/terminal')


@socketio.on('ogretmen_baglan', namespace='/terminal')
def ogretmen_baglan_event(veri=None):
    """Öğretmen bağlandığında Docker container başlat."""
    global ogretmen_sid, ogretmen_pty_fd, ogretmen_pty_pid, ders_durumu

    ogretmen_sid = request.sid
    ogretmen_numara = 'ogretmen'

    # Chroot ortamını kontrol et/yarat (PCT 991 üzerinde)
    from chroot_terminal import chroot_var_mi, chroot_olustur, CT_991_HOST, CT_991_REAL_SSH_PORT, CHROOT_BASE, _slugify
    
    # Username'i normalize et
    ogretmen_numara = _slugify(ogretmen_numara)
    
    try:
        if not chroot_var_mi(ogretmen_numara):
            log.info(f"Öğretmen chroot ortamı oluşturuluyor...")
            chroot_olustur(ogretmen_numara, "Öğretmen", "Paneli")

        # PCT 991'e ROOT olarak bağlan ve komutla chroot'a gir
        # Bu yöntem öğrenci/öğretmen için ayrı SSH anahtarı gereksinimini ortadan kaldırır
        master_fd, slave_fd = pty.openpty()
        
        # Kullanıcı adını ve yolu tırnak içine al (boşluklu kullanıcı adları için)
        safe_username = ogretmen_numara.replace("'", "'\\''")
        safe_chroot_path = f"{CHROOT_BASE}/{safe_username}".replace("'", "'\\''")
        
        ssh_cmd = [
            'ssh', '-t', '-o', 'StrictHostKeyChecking=no', 
            '-p', str(CT_991_REAL_SSH_PORT), 
            f'root@{CT_991_HOST}',
            f"chroot '{safe_chroot_path}' /bin/su - '{safe_username}'"
        ]
        
        proc = subprocess.Popen(ssh_cmd, stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)
        os.close(slave_fd)

        ogretmen_pty_fd = master_fd
        ogretmen_pty_pid = proc.pid

        # PTY çıktısını oku ve yayınla
        t = threading.Thread(target=_pty_oku_ve_yayinla,
                             args=(master_fd, 'ogretmen_cikti', None, True), daemon=True)
        t.start()
        
        log.info("Öğretmen terminali PCT 991 üzerinden bağlandı.")
        
        # OTOMATİK MOD DEĞİŞİMİ: Öğretmen terminale bağlandığında öğrencileri de terminale yönlendir
        global ders_durumu
        if ders_durumu['mod'] != 'terminal':
            log.info(f"Otomatik mod değişimi tetiklendi: {ders_durumu['mod']} -> terminal")
            ders_durumu['mod'] = 'terminal'
            # URL'in de doğru olduğundan emin ol
            if not ders_durumu.get('terminal_url'):
                ders_durumu['terminal_url'] = '/terminal'
            
        emit('bagli_ogrenci_sayisi', len(ogrenci_sidleri))

    except Exception as e:
        log.error(f"Öğretmen terminal bağlantı hatası: {str(e)}")
        emit('hata', f'Terminal bağlantı hatası: {str(e)}')


@socketio.on('ogretmen_girdi', namespace='/terminal')
def ogretmen_girdi_event(veri):
    """Öğretmenin tuş vuruşlarını PTY'ye gönder ve komutları tamponla."""
    global ogretmen_pty_fd, ogretmen_komut_tampon
    char = veri.get('data', '')
    
    if ogretmen_pty_fd is not None:
        with ogretmen_pty_lock:
            try:
                os.write(ogretmen_pty_fd, char.encode('utf-8'))
            except OSError:
                pass

    # Komut yakalama mantığı (Enter tuşuna kadar tamponla)
    if char == '\r' or char == '\n':
        if ogretmen_komut_tampon.strip():
            # Tamamlanmış komutu tüm öğrencilere yayınla
            socketio.emit('ogretmen_komut', ogretmen_komut_tampon.strip(), namespace='/terminal')
        ogretmen_komut_tampon = ""
    elif char == '\x7f' or char == '\x08': # Backspace
        ogretmen_komut_tampon = ogretmen_komut_tampon[:-1]
    elif len(char) == 1 and char.isprintable():
        ogretmen_komut_tampon += char


@socketio.on('ogretmen_temizle', namespace='/terminal')
def ogretmen_temizle_event():
    """Öğretmen ekranı temizledi — öğrencilere de bildir."""
    socketio.emit('ogretmen_temizle', namespace='/terminal')


@socketio.on('ogrenci_baglan', namespace='/terminal')
def ogrenci_baglan_event(veri):
    """Öğrenci bağlandığında username ile Docker container'a bağlan."""
    sid = request.sid
    username = veri.get('username', '')

    if not username:
        emit('hata', 'Kullanıcı adı gerekli!')
        return

    ogrenci_sidleri[sid] = username

    # Container'a (PCT 991) SSH ile bağlan (PTY modunda)
    # ROOT üzerinden bağlanıp chroot'a geçiyoruz (auth sorunlarını çözmek için)
    try:
        master_fd, slave_fd = pty.openpty()
        # Username'i normalize et
        username = _slugify(username)
        
        # Chroot ortamını kontrol et/yarat/senkronize et (Her bağlantıda zorla ki fixler yansısın)
        from chroot_terminal import CT_991_HOST, CT_991_REAL_SSH_PORT, CHROOT_BASE, _slugify, chroot_var_mi, chroot_olustur
        
        # Öğrencinin adını soyadını DB'den al (Log ve passwd için)
        ad_soyad = "Ogrenci"
        with db_baglantisi() as db:
            row = db.execute("SELECT ad, soyad FROM ogrenciler WHERE numara=?", (username,)).fetchone()
            if row:
                ad_soyad = f"{row['ad']} {row['soyad']}"
            elif username.startswith('u') and username[1:].isdigit():
                # Slugify edilmiş halini de kontrol et
                row = db.execute("SELECT ad, soyad FROM ogrenciler WHERE numara=?", (username[1:],)).fetchone()
                if row:
                    ad_soyad = f"{row['ad']} {row['soyad']}"

        log.info(f"Ogrenci terminal bağlantısı: {username} ({ad_soyad}) - Chroot kontrol ediliyor...")
        chroot_olustur(username, ad_soyad, "") # Bu fonksiyon mevcutsa bile sync eder
        
        # Kullanıcı adını ve yolu tırnak içine al (boşluklu kullanıcı adları için)
        safe_username = username.replace("'", "'\\''")
        safe_chroot_path = f"{CHROOT_BASE}/{safe_username}".replace("'", "'\\''")

        ssh_cmd = [
            'ssh', '-t', '-o', 'StrictHostKeyChecking=no', 
            '-p', str(CT_991_REAL_SSH_PORT), 
            f'root@{CT_991_HOST}',
            f"chroot '{safe_chroot_path}' /bin/su - '{safe_username}'"
        ]
        
        proc = subprocess.Popen(ssh_cmd, stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)
        os.close(slave_fd)

        ogrenci_surecleri[sid] = (proc, master_fd)
        ogrenci_pty_locks[master_fd] = threading.Lock()

        socketio.emit('container_hazir', room=sid, namespace='/terminal')

        # Çıktıyı oku ve öğrenciye gönder
        t = threading.Thread(target=_pty_oku_ve_yayinla,
                             args=(master_fd, 'terminal_cikti', sid), daemon=True)
        t.start()

    except Exception as e:
        log.error(f"[Socket] Terminal bağlantı hatası (User: {username}): {str(e)}")
        socketio.emit('hata', f'Terminal bağlantı hatası: {str(e)}',
                      room=sid, namespace='/terminal')


@socketio.on('terminal_girdi', namespace='/terminal')
def ogrenci_girdi_event(veri):
    """Öğrencinin tuş vuruşlarını kendi container'ına gönder."""
    sid = request.sid
    if sid in ogrenci_surecleri:
        _, fd = ogrenci_surecleri[sid]
        lock = ogrenci_pty_locks.get(fd)
        if lock:
            with lock:
                try:
                    os.write(fd, veri['data'].encode('utf-8'))
                except OSError:
                    pass
        else:
            # Fallback (lock henüz oluşmamışsa)
            try:
                os.write(fd, veri['data'].encode('utf-8'))
            except OSError:
                pass


# ── Başlat ────────────────────────────────────────────────────
if __name__ == '__main__':
    db_olustur()

    # Yerel IP'yi göster
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        yerel_ip = s.getsockname()[0]
        s.close()
    except Exception:
        yerel_ip = '127.0.0.1'

    print()
    print('=' * 55)
    print('  🐧 Ders Takip Sistemi başlatıldı!')
    print('=' * 55)
    print(f'  Öğrenciler için    : http://{yerel_ip}:3333')
    print(f'  Öğretmen paneli    : http://localhost:3333/teacher')
    from chroot_terminal import CT_991_HOST, CT_991_REAL_SSH_PORT
    print(f'  Öğretmen terminal  : http://localhost:3333/teacher/terminal')
    print(f'  Şifre              : {OGRETMEN_SIFRE}')
    print(f'  Chroot Host (991)  : ✅ {CT_991_HOST}:{CT_991_REAL_SSH_PORT}')
    print('=' * 55)
    print()

    # Single container approach - temizleme gerekmez

    # SocketIO ile başlat (WebSocket desteği)
    socketio.run(app, host='0.0.0.0', port=3333, debug=False)
