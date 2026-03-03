"""
Ders Takip Sistemi — Flask Sunucusu
Kapadokya Üniversitesi Linux Dersleri

Başlatmak için:
    python3 app.py

Öğretmen paneli: http://localhost:3333/teacher
"""

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

# ── SocketIO ─────────────────────────────────────────────────
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Ders durumu (bellek içi)
ders_durumu = {
    'mod':   'bekleme',   # bekleme | slayt
    'dosya': ''              # aktif slayt dosyası
}

# ── Veritabanı ────────────────────────────────────────────────
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
    """Ana sayfa - Giriş formu."""
    return render_template('login.html')

@app.route('/giris', methods=['POST'])
def giris():
    ad_soyad = request.form.get('ad_soyad', '').strip().upper()
    numara   = request.form.get('numara', '').strip()
    sinif_id = request.form.get('sinif_id', '').strip()
    paket    = request.form.get('paket', '').strip()

    siniflar = sinif_listesi()

    # Hata durumunda formu tekrar göstermek için yardımcı
    def hata_goster(mesaj):
        return render_template('ogrenci_giris.html',
                               hata=mesaj,
                               siniflar=siniflar,
                               paket_secenekleri=PAKET_SECENEKLERI,
                               paket_varsayilan=paket or paket_hesapla())

    if not ad_soyad or not numara or not sinif_id:
        return hata_goster('Lütfen tüm alanları doldurun.')

    # Paket doğrulama
    if paket not in PAKET_SECENEKLERI:
        paket = paket_hesapla()   # Geçersizse saate göre dön

    # ── Whitelist kontrolü ──
    with db_baglantisi() as db:
        ogrenci = db.execute(
            'SELECT ad, soyad, sifre FROM ogrenciler WHERE numara=? AND sinif_id=?',
            (numara, sinif_id)
        ).fetchone()

    if not ogrenci:
        return hata_goster('Bu öğrenci numarası seçili sınıfa kayıtlı değil.')

    tam_ad = (ogrenci['ad'] + ' ' + ogrenci['soyad']).upper()
    if ad_soyad != tam_ad:
        return hata_goster('İsim ve numara uyuşmuyor.')

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
            (tarih, istemci, paket)
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
                     numara, tam_ad,
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
            (tarih, numara, paket)
        ).fetchone()
        if var_mi:
            # Öğrenci zaten giriş yapmış, tekrar hoş geldin!
            session['ogrenci_numara'] = numara
            session['ogrenci_ad'] = tam_ad
            return render_template('ogrenci_ana.html',
                                   ad_soyad=tam_ad,
                                   saat=var_mi['saat'],
                                   paket=paket,
                                   tekrar_giris=True)

        # ── 3. YENİ KAYIT ──────────────────────────────────────────
        db.execute(
            'INSERT INTO yoklama (tarih, ad_soyad, numara, saat, sinif, paket, ip, kaynak) '
            'VALUES (?,?,?,?,?,?,?,?)',
            (tarih, tam_ad, numara, saat, sinif_ad, paket, istemci, 'web')
        )
        db.commit()

    # Öğrenci session bilgileri (terminal sayfası için gerekli)
    session['ogrenci_numara'] = numara
    session['ogrenci_ad'] = tam_ad

    return render_template('ogrenci_ana.html', ad_soyad=tam_ad, saat=saat, paket=paket)

@app.route('/api/durum')
def api_durum():
    # Öğrenci için durum
    response = {
        'mod': ders_durumu['mod'],
        'dosya': ders_durumu['dosya']
    }
    return jsonify(response)

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
    if veri.get('mod') in ('bekleme', 'slayt'):
        ders_durumu['mod']   = veri['mod']
        ders_durumu['dosya'] = veri.get('dosya', '')

    return jsonify({'durum': 'ok', 'mod': ders_durumu['mod']})

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

# ── Terminal Rotaları ─────────────────────────────────────────
@app.route('/terminal')
def terminal_sayfasi():
    """Terminal login sayfası."""
    return render_template('terminal_login.html')


@app.route('/terminal/login', methods=['POST'])
def terminal_login():
    """Terminal login ve container başlatma."""
    ad = request.form.get('ad', '').strip()
    soyad = request.form.get('soyad', '').strip()
    numara = request.form.get('numara', '').strip()

    # Validasyon
    if not ad or not soyad or not numara:
        return render_template('terminal_login.html', hata='Tüm alanları doldurun.')

    # Numara sadece rakam
    if not numara.isdigit():
        return render_template('terminal_login.html', hata='Numara sadece rakamlardan oluşmalı.')

    # Container başlat
    cid = container_baslat(numara)
    if not cid:
        return render_template('terminal_login.html', hata='Container başlatılamadı. Docker çalışıyor mu?')

    # IP adresini al
    ip = container_ip_al(numara)
    if not ip:
        return render_template('terminal_login.html', hata='Container IP adresi alınamadı.')

    # Session bilgilerini sakla
    session['terminal_ad'] = ad
    session['terminal_soyad'] = soyad
    session['terminal_numara'] = numara
    session['terminal_ip'] = ip
    session['terminal_cid'] = cid

    return redirect('/terminal/workspace')


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
        'aktif_konteynerler': konteyner_listesi(),
        'bagli_ogrenciler': len(ogrenci_sidleri)
    })


# ── SocketIO Terminal Olayları ────────────────────────────────
# Öğretmenin PTY dosya tanımlayıcıları
ogretmen_pty_fd = None
ogretmen_pty_pid = None
ogretmen_sid = None

# Bağlı öğrenciler: {sid: numara}
ogrenci_sidleri = {}

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
        # Container'ı durdur
        if numara:
            threading.Thread(target=konteyner_durdur, args=(numara,), daemon=True).start()

        # Öğrenci sayısını güncelle
        if ogretmen_sid:
            socketio.emit('bagli_ogrenci_sayisi', len(ogrenci_sidleri),
                          room=ogretmen_sid, namespace='/terminal')


@socketio.on('ogretmen_baglan', namespace='/terminal')
def ogretmen_baglan_event():
    """Öğretmen bağlandığında Docker container başlat."""
    global ogretmen_sid, ogretmen_pty_fd, ogretmen_pty_pid

    ogretmen_sid = request.sid
    ogretmen_numara = 'ogretmen'  # Öğretmen için özel numara

    # Docker container başlat
    cid = konteyner_baslat(ogretmen_numara)
    if not cid:
        emit('hata', 'Öğretmen container başlatılamadı!')
        return

    # Container'a docker exec ile bağlan (PTY modunda)
    try:
        master_fd, slave_fd = pty.openpty()
        proc = subprocess.Popen(
            ['docker', 'exec', '-it', f'terminal-{ogretmen_numara}', '/bin/bash'],
            stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
            preexec_fn=os.setsid
        )
        os.close(slave_fd)

        ogretmen_pty_fd = master_fd
        ogretmen_pty_pid = proc.pid

        # PTY çıktısını oku ve tüm öğrencilere yayınla
        t = threading.Thread(target=_pty_oku_ve_yayinla,
                             args=(master_fd, 'ogretmen_cikti', None, True), daemon=True)
        t.start()

        emit('bagli_ogrenci_sayisi', len(ogrenci_sidleri))
    except Exception as e:
        emit('hata', f'Container bağlantı hatası: {str(e)}')


@socketio.on('ogretmen_girdi', namespace='/terminal')
def ogretmen_girdi_event(veri):
    """Öğretmenin tuş vuruşlarını PTY'ye gönder."""
    global ogretmen_pty_fd
    if ogretmen_pty_fd is not None:
        try:
            os.write(ogretmen_pty_fd, veri['data'].encode('utf-8'))
        except OSError:
            pass


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

    # Tek container'ı başlat (ilk öğrenci için)
    if not container_durum():
        if not container_baslat():
            emit('hata', 'Container başlatılamadı! Docker çalışıyor mu?')
            return

    # Kullanıcıyı container'da oluştur
    if not kullanici_olustur(username):
        emit('hata', 'Kullanıcı oluşturulamadı!')
        return

    # Container'a docker exec ile bağlan (PTY modunda)
    try:
        master_fd, slave_fd = pty.openpty()
        proc = subprocess.Popen(
            ['docker', 'exec', '-it', 'linux-lab', 'su', '-', username],
            stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
            preexec_fn=os.setsid
        )
        os.close(slave_fd)

        ogrenci_surecleri[sid] = (proc, master_fd)

            socketio.emit('container_hazir', room=sid, namespace='/terminal')

            # Çıktıyı oku ve öğrenciye gönder
            _pty_oku_ve_yayinla(master_fd, 'terminal_cikti', hedef_room=sid)

        except Exception as e:
            socketio.emit('hata', f'Terminal bağlantı hatası: {str(e)}',
                          room=sid, namespace='/terminal')

    threading.Thread(target=_container_baslat, daemon=True).start()


@socketio.on('terminal_girdi', namespace='/terminal')
def ogrenci_girdi_event(veri):
    """Öğrencinin tuş vuruşlarını kendi container'ına gönder."""
    sid = request.sid
    if sid in ogrenci_surecleri:
        _, fd = ogrenci_surecleri[sid]
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
    print(f'  Öğretmen terminal  : http://localhost:3333/teacher/terminal')
    print(f'  Şifre              : {OGRETMEN_SIFRE}')
    print(f'  Docker imaj durumu : {"✅ Hazır" if image_var_mi() else "❌ Yok — ./build_image.sh çalıştırın"}')
    print('=' * 55)
    print()

    # Kapatma sırasında container'ları temizle
    import atexit
    atexit.register(konteyner_temizle)

    # SocketIO ile başlat (WebSocket desteği)
    socketio.run(app, host='0.0.0.0', port=3333, debug=False, allow_unsafe_werkzeug=True)
