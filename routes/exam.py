from flask import Blueprint, request, jsonify, session
from core.db import db_baglantisi
from core.security import ogretmen_giris_gerekli, seb_gerekli
from core.utils import bugun

exam_bp = Blueprint('exam_bp', __name__, url_prefix='/api/sinav')

# ── Öğretmen İşlemleri ──

@exam_bp.route('/liste', methods=['GET'])
@ogretmen_giris_gerekli
def sinav_listesi():
    with db_baglantisi() as db:
        sinavlar = db.execute("SELECT * FROM sinavlar ORDER BY id DESC").fetchall()
        sinavlar_array = []
        for s in sinavlar:
            soru_sayisi = db.execute("SELECT COUNT(id) as sayi FROM sorular WHERE sinav_id=?", (s['id'],)).fetchone()['sayi']
            sinavlar_array.append({
                'id': s['id'],
                'baslik': s['baslik'],
                'aktif': bool(s['aktif']),
                'olusturma_tarihi': s['olusturma_tarihi'],
                'soru_sayisi': soru_sayisi
            })
    return jsonify({'sinavlar': sinavlar_array})

@exam_bp.route('/olustur', methods=['POST'])
@ogretmen_giris_gerekli
def sinav_olustur():
    veri = request.get_json()
    baslik = veri.get('baslik', '').strip()
    if not baslik:
        return jsonify({'durum': 'hata', 'mesaj': 'Sınav başlığı boş olamaz'}), 400
    
    with db_baglantisi() as db:
        cursor = db.execute("INSERT INTO sinavlar (baslik, olusturma_tarihi) VALUES (?, ?)", (baslik, bugun()))
        db.commit()
    return jsonify({'durum': 'ok', 'id': cursor.lastrowid})

@exam_bp.route('/sorular/<int:sinav_id>', methods=['GET'])
@ogretmen_giris_gerekli
def sorulari_getir(sinav_id):
    with db_baglantisi() as db:
        sorular = db.execute("SELECT * FROM sorular WHERE sinav_id=?", (sinav_id,)).fetchall()
        soru_listesi = []
        for soru in sorular:
            secenekler = db.execute("SELECT * FROM secenekler WHERE soru_id=?", (soru['id'],)).fetchall()
            soru_listesi.append({
                'id': soru['id'],
                'metin': soru['metin'],
                'tip': soru['tip'],
                'puan': soru['puan'],
                'secenekler': [dict(s) for s in secenekler]
            })
    return jsonify({'sorular': soru_listesi})

@exam_bp.route('/soru_ekle', methods=['POST'])
@ogretmen_giris_gerekli
def soru_ekle():
    veri = request.get_json()
    sinav_id = veri.get('sinav_id')
    metin = veri.get('metin', '').strip()
    puan = veri.get('puan', 10)
    secenekler = veri.get('secenekler', []) # [{'metin': '', 'dogru_mu': bool}]

    if not sinav_id or not metin or len(secenekler) < 2:
        return jsonify({'durum': 'hata', 'mesaj': 'Sınav seçilmeli, soru metni ve en az 2 seçenek olmalı'}), 400

    # Doğru seçeneğin olduğundan emin ol
    if not any(s.get('dogru_mu') for s in secenekler):
         return jsonify({'durum': 'hata', 'mesaj': 'Sorunun doğru seçeneği işaretlenmemiş'}), 400
    
    with db_baglantisi() as db:
        # Soruyu ekle
        cursor = db.execute("INSERT INTO sorular (sinav_id, metin, puan) VALUES (?, ?, ?)", (sinav_id, metin, puan))
        soru_id = cursor.lastrowid
        
        # Seçenekleri ekle
        for secenek in secenekler:
            db.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, ?, ?)", 
                       (soru_id, secenek.get('metin','').strip(), 1 if secenek.get('dogru_mu') else 0))
        db.commit()

    return jsonify({'durum': 'ok', 'soru_id': soru_id})

@exam_bp.route('/aktiflestir', methods=['POST'])
@ogretmen_giris_gerekli
def sinav_aktiflestir():
    veri = request.get_json()
    sinav_id = veri.get('sinav_id')
    aktif = veri.get('aktif', False)

    if not sinav_id:
        return jsonify({'durum': 'hata'}), 400

    with db_baglantisi() as db:
        if aktif:
            # Sadece 1 sınav aktif olabilir
            db.execute("UPDATE sinavlar SET aktif=0")
        db.execute("UPDATE sinavlar SET aktif=? WHERE id=?", (1 if aktif else 0, sinav_id))
        db.commit()

    # App tarafındaki modu tetiklemek için terminal websocketlerinden faydalanılabilir ya da 1 sn. polling
    # Ders_durumu 'sinav' olarak isaretlenmeli.
    from core.config import ders_durumu
    if aktif:
        ders_durumu['mod'] = 'sinav'
        ders_durumu['dosya'] = str(sinav_id) # 'dosya' field holds exam_id when mod is 'sinav'
    else:
        ders_durumu['mod'] = 'bekleme'
        ders_durumu['dosya'] = ''

    return jsonify({'durum': 'ok'})

@exam_bp.route('/sonuclar/<int:sinav_id>', methods=['GET'])
@ogretmen_giris_gerekli
def sinav_sonuclari(sinav_id):
    with db_baglantisi() as db:
        cevaplar = db.execute("""
            SELECT o.ogrenci_numara, o.puan, og.ad, og.soyad 
            FROM ogrenci_cevaplari o 
            LEFT JOIN ogrenciler og ON o.ogrenci_numara = og.numara
            WHERE o.sinav_id = ?
        """, (sinav_id,)).fetchall()
        
        # Öğrenci bazında grupla ve topla
        sonuclar = {}
        for row in cevaplar:
            num = row['ogrenci_numara']
            if num not in sonuclar:
                sonuclar[num] = {
                    'numara': num,
                    'ad_soyad': f"{row['ad']} {row['soyad']}" if row['ad'] else "Bilinmiyor",
                    'toplam_puan': 0
                }
            sonuclar[num]['toplam_puan'] += row['puan']
            
    return jsonify({'sonuclar': list(sonuclar.values())})

# ── Öğrenci İşlemleri ──

@exam_bp.route('/aktif', methods=['GET'])
@seb_gerekli
def aktif_sinav():
    """Öğrenciye aktif sınavı ve sorularını getir (cevaplar olmadan)."""
    with db_baglantisi() as db:
        # Aktif sınavı bul
        sinav = db.execute("SELECT * FROM sinavlar WHERE aktif=1 LIMIT 1").fetchone()
        if not sinav:
            return jsonify({'aktif_sinav': None})
            
        sinav_id = sinav['id']
        sorular = db.execute("SELECT id, metin, puan FROM sorular WHERE sinav_id=?", (sinav_id,)).fetchall()
        
        soru_listesi = []
        for soru in sorular:
            secenekler = db.execute("SELECT id, metin FROM secenekler WHERE soru_id=?", (soru['id'],)).fetchall()
            soru_listesi.append({
                'id': soru['id'],
                'metin': soru['metin'],
                'puan': soru['puan'],
                'secenekler': [{'id': s['id'], 'metin': s['metin']} for s in secenekler]
            })
            
        # Zaten cevaplamış mı kontrol et
        numara = session.get('numara')
        cevaplamis_mi = False
        if numara:
            kontrol = db.execute("SELECT id FROM ogrenci_cevaplari WHERE sinav_id=? AND ogrenci_numara=? LIMIT 1", (sinav_id, numara)).fetchone()
            if kontrol:
                cevaplamis_mi = True
                
    return jsonify({
        'aktif_sinav': {
            'id': sinav_id,
            'baslik': sinav['baslik'],
            'sorular': soru_listesi,
            'zaten_cevapladi': cevaplamis_mi
        }
    })

@exam_bp.route('/cevap_kaydet', methods=['POST'])
@seb_gerekli
def cevap_kaydet():
    veri = request.get_json()
    sinav_id = veri.get('sinav_id')
    cevaplar = veri.get('cevaplar', []) # [{'soru_id': 1, 'secenek_id': 2}]
    numara = session.get('numara')

    if not sinav_id or not numara or not cevaplar:
        return jsonify({'durum': 'hata', 'mesaj': 'Eksik bilgi'})

    with db_baglantisi() as db:
        # Çift gönderimi önle
        kontrol = db.execute("SELECT id FROM ogrenci_cevaplari WHERE sinav_id=? AND ogrenci_numara=? LIMIT 1", (sinav_id, numara)).fetchone()
        if kontrol:
            return jsonify({'durum': 'hata', 'mesaj': 'Sınav zaten gönderilmiş'})
            
        # Notlandırma
        for cevap in cevaplar:
            soru_id = cevap.get('soru_id')
            secenek_id = cevap.get('secenek_id')
            
            # Soru verisi
            soru = db.execute("SELECT puan FROM sorular WHERE id=?", (soru_id,)).fetchone()
            if not soru: continue
            
            # Seçenek doğru mu?
            secenek = db.execute("SELECT dogru_mu FROM secenekler WHERE id=? AND soru_id=?", (secenek_id, soru_id)).fetchone()
            puan = soru['puan'] if (secenek and secenek['dogru_mu'] == 1) else 0
            
            # Kaydet
            db.execute("INSERT INTO ogrenci_cevaplari (sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan) VALUES (?, ?, ?, ?, ?)",
                       (sinav_id, numara, soru_id, str(secenek_id), puan))
        db.commit()

    return jsonify({'durum': 'ok'})
