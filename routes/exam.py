import random
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
                'sure_dakika': s['sure_dakika'],
                'baslama_zamani': s['baslama_zamani'],
                'soru_sayisi': soru_sayisi
            })
    return jsonify({'sinavlar': sinavlar_array})

@exam_bp.route('/olustur', methods=['POST'])
@ogretmen_giris_gerekli
def sinav_olustur():
    veri = request.get_json()
    baslik = veri.get('baslik', '').strip()
    sure_dakika = int(veri.get('sure_dakika', 0))
    if not baslik:
        return jsonify({'durum': 'hata', 'mesaj': 'Sınav başlığı boş olamaz'}), 400
    
    with db_baglantisi() as db:
        cursor = db.execute("INSERT INTO sinavlar (baslik, sure_dakika, olusturma_tarihi) VALUES (?, ?, ?)", 
                            (baslik, sure_dakika, bugun()))
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
            ciktilar = db.execute("""
                SELECT oc.id as cikti_id, oc.numara, oc.metin
                FROM soru_cikti_iliskisi sci
                JOIN ogrenme_ciktilari oc ON sci.cikti_id = oc.id
                WHERE sci.soru_id = ?
            """, (soru['id'],)).fetchall()
            soru_listesi.append({
                'id': soru['id'],
                'metin': soru['metin'],
                'tip': soru['tip'],
                'puan': soru['puan'],
                'bloom_seviyesi': soru['bloom_seviyesi'] if 'bloom_seviyesi' in soru.keys() else '',
                'zorluk': soru['zorluk'] if 'zorluk' in soru.keys() else '',
                'secenekler': [dict(s) for s in secenekler],
                'ciktilar': [dict(c) for c in ciktilar]
            })
    return jsonify({'sorular': soru_listesi})

@exam_bp.route('/soru_ekle', methods=['POST'])
@ogretmen_giris_gerekli
def soru_ekle():
    veri = request.get_json()
    sinav_id = veri.get('sinav_id')
    metin = veri.get('metin', '').strip()
    puan = veri.get('puan', 10)
    tip = veri.get('tip', 'cok_secmeli')

    if not sinav_id or not metin:
        return jsonify({'durum': 'hata', 'mesaj': 'Sınav seçilmeli ve soru metni girilmeli'}), 400

    if tip not in ('cok_secmeli', 'dogru_yanlis', 'bosluk_doldurma', 'acik_uclu'):
        return jsonify({'durum': 'hata', 'mesaj': 'Geçersiz soru tipi'}), 400

    bloom = veri.get('bloom_seviyesi', '')
    zorluk = veri.get('zorluk', '')
    cikti_idler = veri.get('cikti_idler', [])  # [1, 3, 5]

    with db_baglantisi() as db:
        cursor = db.execute("INSERT INTO sorular (sinav_id, metin, tip, puan, bloom_seviyesi, zorluk) VALUES (?, ?, ?, ?, ?, ?)",
                            (sinav_id, metin, tip, puan, bloom, zorluk))
        soru_id = cursor.lastrowid

        # Öğrenme çıktısı ilişkileri
        for cid in cikti_idler:
            db.execute("INSERT INTO soru_cikti_iliskisi (soru_id, cikti_id) VALUES (?, ?)", (soru_id, cid))

        if tip == 'cok_secmeli':
            secenekler = veri.get('secenekler', [])
            if len(secenekler) < 2:
                return jsonify({'durum': 'hata', 'mesaj': 'En az 2 seçenek olmalı'}), 400
            if not any(s.get('dogru_mu') for s in secenekler):
                return jsonify({'durum': 'hata', 'mesaj': 'Doğru seçenek işaretlenmemiş'}), 400
            for secenek in secenekler:
                db.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, ?, ?)",
                           (soru_id, secenek.get('metin', '').strip(), 1 if secenek.get('dogru_mu') else 0))

        elif tip == 'dogru_yanlis':
            dogru_cevap = veri.get('dogru_cevap', '')
            if dogru_cevap not in ('dogru', 'yanlis'):
                return jsonify({'durum': 'hata', 'mesaj': 'Doğru veya Yanlış seçilmeli'}), 400
            db.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, 'Doğru', ?)",
                       (soru_id, 1 if dogru_cevap == 'dogru' else 0))
            db.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, 'Yanlış', ?)",
                       (soru_id, 1 if dogru_cevap == 'yanlis' else 0))

        elif tip == 'bosluk_doldurma':
            dogru_cevap = veri.get('dogru_cevap', '').strip()
            if not dogru_cevap:
                return jsonify({'durum': 'hata', 'mesaj': 'Doğru cevap girilmeli'}), 400
            db.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, ?, 1)",
                       (soru_id, dogru_cevap))

        # acik_uclu: seçenek gerekmez

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
            db.execute("UPDATE sinavlar SET aktif=1, baslama_zamani=CURRENT_TIMESTAMP WHERE id=?", (sinav_id,))
        else:
            db.execute("UPDATE sinavlar SET aktif=0, baslama_zamani=NULL WHERE id=?", (sinav_id,))
        db.commit()

    # App tarafındaki modu tetiklemek için terminal websocketlerinden faydalanılabilir ya da 1 sn. polling
    # Ders_durumu 'sinav' olarak isaretlenmeli.
    from core.config import ders_durumu
    sinav_terminal = veri.get('sinav_terminal', False)
    if aktif:
        ders_durumu['mod'] = 'sinav'
        ders_durumu['dosya'] = str(sinav_id)
        ders_durumu['sinav_terminal'] = bool(sinav_terminal)
        if sinav_terminal:
            # Terminal URL'sini ayarla (yoksa varsayılan)
            if not ders_durumu.get('terminal_url'):
                ders_durumu['terminal_url'] = '/terminal'
            import logging
            logging.getLogger('app').info(f"📝 Sınav başlatıldı: terminal_açık={sinav_terminal}, terminal_url={ders_durumu.get('terminal_url')}")
    else:
        ders_durumu['mod'] = 'bekleme'
        ders_durumu['sinav_terminal'] = False
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
        sinav = db.execute("SELECT *, CURRENT_TIMESTAMP as simdi FROM sinavlar WHERE aktif=1 LIMIT 1").fetchone()
        if not sinav:
            return jsonify({'aktif_sinav': None})
            
        sinav_id = sinav['id']
        
        # Süre kontrolü (Otomatik Kapanma)
        if sinav['sure_dakika'] > 0 and sinav['baslama_zamani']:
             from datetime import datetime
             # Not: CURRENT_TIMESTAMP'i db'den aldık (simdi) çünkü DB saati ile Python saati farklı olabilir (timezone vb)
             # SQLite ve PG dönen format farklı olabilir. RealDictCursor ise dict'tir.
             
             # Basitçe: Eğer sure_dakika dolmuşsa aktif=0 yap.
             # Bu kontrol her öğrenci aktif sınavı sorduğunda (polling) tetiklenir.
             
             # PostgreSQL tipik olarak datetime objesi döner. SQLite ise string döner.
             try:
                 baslama = sinav['baslama_zamani']
                 simdi = sinav['simdi']
                 
                 if isinstance(baslama, str):
                     # SQLite: YYYY-MM-DD HH:MM:SS formatında string
                     # . yerine : gelmiş olabilir, kontrol et.
                     fmt = '%Y-%m-%d %H:%M:%S'
                     baslama_dt = datetime.strptime(baslama.split('.')[0], fmt)
                     simdi_dt = datetime.strptime(simdi.split('.')[0], fmt)
                 else:
                     # PostgreSQL: datetime objeleri
                     baslama_dt = baslama
                     simdi_dt = simdi
                
                 gecen_sn = (simdi_dt - baslama_dt).total_seconds()
                 if gecen_sn > (sinav['sure_dakika'] * 60):
                     db.execute("UPDATE sinavlar SET aktif=0 WHERE id=?", (sinav_id,))
                     db.commit()
                     return jsonify({'aktif_sinav': None, 'mesaj': 'Sınav süresi doldu'})
                     
                 sinav_kalan_sn = (sinav['sure_dakika'] * 60) - gecen_sn
             except Exception as e:
                 print(f"Süre hesaplama hatası: {e}")
                 sinav_kalan_sn = sinav['sure_dakika'] * 60
        else:
             sinav_kalan_sn = None
        sorular = db.execute("SELECT id, metin, tip, puan FROM sorular WHERE sinav_id=?", (sinav_id,)).fetchall()

        soru_listesi = []
        for soru in sorular:
            soru_data = {
                'id': soru['id'],
                'metin': soru['metin'],
                'puan': soru['puan'],
                'tip': soru['tip']
            }
            # Seçenekleri sadece çoktan seçmeli ve doğru/yanlış için gönder
            if soru['tip'] in ('cok_secmeli', 'dogru_yanlis'):
                secenekler = db.execute("SELECT id, metin FROM secenekler WHERE soru_id=?", (soru['id'],)).fetchall()
                soru_data['secenekler'] = [{'id': s['id'], 'metin': s['metin']} for s in secenekler]
            else:
                soru_data['secenekler'] = []
            soru_listesi.append(soru_data)
            
        # Zaten cevaplamış mı kontrol et
        numara = session.get('numara')
        cevaplamis_mi = False
        if numara:
            kontrol = db.execute("SELECT id FROM ogrenci_cevaplari WHERE sinav_id=? AND ogrenci_numara=? AND taslak=0 LIMIT 1", (sinav_id, numara)).fetchone()
            if kontrol:
                cevaplamis_mi = True

        # Her öğrenci için soru ve seçenek sırasını karıştır
        # Deterministic seed: aynı öğrenci her yenilemede aynı sırayı görür
        if numara:
            rng = random.Random(f"{sinav_id}-{numara}")
            rng.shuffle(soru_listesi)
            for soru in soru_listesi:
                if soru.get('secenekler'):
                    rng.shuffle(soru['secenekler'])

    return jsonify({
        'aktif_sinav': {
            'id': sinav_id,
            'baslik': sinav['baslik'],
            'sorular': soru_listesi,
            'zaten_cevapladi': cevaplamis_mi,
            'kalan_sure': sinav_kalan_sn,
            'toplam_sure': sinav['sure_dakika']
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
        # Çift gönderimi önle (sadece kesin kayıtları kontrol et)
        kontrol = db.execute("SELECT id FROM ogrenci_cevaplari WHERE sinav_id=? AND ogrenci_numara=? AND taslak=0 LIMIT 1", (sinav_id, numara)).fetchone()
        if kontrol:
            return jsonify({'durum': 'hata', 'mesaj': 'Sınav zaten gönderilmiş'})

        # Taslak varsa temizle
        db.execute("DELETE FROM ogrenci_cevaplari WHERE sinav_id=? AND ogrenci_numara=? AND taslak=1", (sinav_id, numara))

        # Notlandırma
        for cevap in cevaplar:
            soru_id = cevap.get('soru_id')
            soru = db.execute("SELECT puan, tip FROM sorular WHERE id=?", (soru_id,)).fetchone()
            if not soru: continue

            if soru['tip'] in ('cok_secmeli', 'dogru_yanlis'):
                secenek_id = cevap.get('secenek_id')
                secenek = db.execute("SELECT dogru_mu FROM secenekler WHERE id=? AND soru_id=?",
                                     (secenek_id, soru_id)).fetchone()
                puan = soru['puan'] if (secenek and secenek['dogru_mu'] == 1) else 0
                verilen_cevap = str(secenek_id)

            elif soru['tip'] == 'bosluk_doldurma':
                metin_cevap = cevap.get('metin_cevap', '').strip()
                dogru = db.execute("SELECT metin FROM secenekler WHERE soru_id=? AND dogru_mu=1",
                                   (soru_id,)).fetchone()
                puan = soru['puan'] if (dogru and metin_cevap.lower() == dogru['metin'].strip().lower()) else 0
                verilen_cevap = metin_cevap

            elif soru['tip'] == 'acik_uclu':
                metin_cevap = cevap.get('metin_cevap', '').strip()
                puan = 0  # Öğretmen manuel puanlayacak
                verilen_cevap = metin_cevap

            else:
                continue

            db.execute("INSERT INTO ogrenci_cevaplari (sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan) VALUES (?, ?, ?, ?, ?)",
                       (sinav_id, numara, soru_id, verilen_cevap, puan))
        db.commit()

    return jsonify({'durum': 'ok'})


@exam_bp.route('/acik_uclu_cevaplar/<int:sinav_id>', methods=['GET'])
@ogretmen_giris_gerekli
def acik_uclu_cevaplar(sinav_id):
    """Açık uçlu soruların öğrenci cevaplarını getir (öğretmen puanlama için)."""
    with db_baglantisi() as db:
        cevaplar = db.execute("""
            SELECT oc.id, oc.ogrenci_numara, oc.soru_id, oc.verilen_cevap, oc.puan,
                   s.metin as soru_metin, s.puan as max_puan,
                   og.ad, og.soyad
            FROM ogrenci_cevaplari oc
            JOIN sorular s ON oc.soru_id = s.id
            LEFT JOIN ogrenciler og ON oc.ogrenci_numara = og.numara
            WHERE oc.sinav_id = ? AND s.tip = 'acik_uclu'
            ORDER BY oc.soru_id, oc.ogrenci_numara
        """, (sinav_id,)).fetchall()
    return jsonify({'cevaplar': [dict(c) for c in cevaplar]})


@exam_bp.route('/puan_ver', methods=['POST'])
@ogretmen_giris_gerekli
def puan_ver():
    """Açık uçlu soru cevabına öğretmen puanı ver."""
    veri = request.get_json()
    cevap_id = veri.get('cevap_id')
    puan = veri.get('puan', 0)

    if cevap_id is None:
        return jsonify({'durum': 'hata', 'mesaj': 'Cevap ID gerekli'}), 400

    with db_baglantisi() as db:
        db.execute("UPDATE ogrenci_cevaplari SET puan=? WHERE id=?", (puan, cevap_id))
        db.commit()

    return jsonify({'durum': 'ok'})


# ── Öğrenme Çıktıları (Rubrik) ──

@exam_bp.route('/ciktilar/<int:sinav_id>', methods=['GET'])
@ogretmen_giris_gerekli
def ciktilari_getir(sinav_id):
    with db_baglantisi() as db:
        ciktilar = db.execute("SELECT * FROM ogrenme_ciktilari WHERE sinav_id=? ORDER BY numara", (sinav_id,)).fetchall()
    return jsonify({'ciktilar': [dict(c) for c in ciktilar]})


@exam_bp.route('/cikti_ekle', methods=['POST'])
@ogretmen_giris_gerekli
def cikti_ekle():
    veri = request.get_json()
    sinav_id = veri.get('sinav_id')
    metin = veri.get('metin', '').strip()
    if not sinav_id or not metin:
        return jsonify({'durum': 'hata', 'mesaj': 'Sınav ID ve çıktı metni gerekli'}), 400

    with db_baglantisi() as db:
        mevcut = db.execute("SELECT MAX(numara) as m FROM ogrenme_ciktilari WHERE sinav_id=?", (sinav_id,)).fetchone()
        numara = (mevcut['m'] or 0) + 1
        cursor = db.execute("INSERT INTO ogrenme_ciktilari (sinav_id, numara, metin) VALUES (?, ?, ?)",
                            (sinav_id, numara, metin))
        db.commit()
    return jsonify({'durum': 'ok', 'id': cursor.lastrowid, 'numara': numara})


@exam_bp.route('/cikti_sil', methods=['POST'])
@ogretmen_giris_gerekli
def cikti_sil():
    veri = request.get_json()
    cikti_id = veri.get('cikti_id')
    if not cikti_id:
        return jsonify({'durum': 'hata'}), 400
    with db_baglantisi() as db:
        db.execute("DELETE FROM soru_cikti_iliskisi WHERE cikti_id=?", (cikti_id,))
        db.execute("DELETE FROM ogrenme_ciktilari WHERE id=?", (cikti_id,))
        db.commit()
    return jsonify({'durum': 'ok'})


@exam_bp.route('/rubrik/<int:sinav_id>', methods=['GET'])
@ogretmen_giris_gerekli
def rubrik_formu(sinav_id):
    """Rubrik formu verisi — sınav, çıktılar, sorular (bloom/zorluk/çıktılar) ve sonuçlar."""
    with db_baglantisi() as db:
        sinav = db.execute("SELECT * FROM sinavlar WHERE id=?", (sinav_id,)).fetchone()
        if not sinav:
            return jsonify({'durum': 'hata', 'mesaj': 'Sınav bulunamadı'}), 404

        ciktilar = db.execute("SELECT * FROM ogrenme_ciktilari WHERE sinav_id=? ORDER BY numara",
                              (sinav_id,)).fetchall()

        sorular = db.execute("SELECT * FROM sorular WHERE sinav_id=?", (sinav_id,)).fetchall()
        soru_listesi = []
        for soru in sorular:
            iliskiler = db.execute("""
                SELECT oc.numara, oc.metin FROM soru_cikti_iliskisi sci
                JOIN ogrenme_ciktilari oc ON sci.cikti_id = oc.id
                WHERE sci.soru_id = ?
            """, (soru['id'],)).fetchall()
            soru_listesi.append({
                'id': soru['id'],
                'metin': soru['metin'],
                'tip': soru['tip'],
                'puan': soru['puan'],
                'bloom_seviyesi': soru['bloom_seviyesi'] if 'bloom_seviyesi' in soru.keys() else '',
                'zorluk': soru['zorluk'] if 'zorluk' in soru.keys() else '',
                'ciktilar': [{'numara': r['numara'], 'metin': r['metin']} for r in iliskiler]
            })

        # Öğrenci sonuçları (varsa)
        cevaplar = db.execute("""
            SELECT oc.ogrenci_numara, oc.soru_id, oc.puan,
                   og.ad, og.soyad
            FROM ogrenci_cevaplari oc
            LEFT JOIN ogrenciler og ON oc.ogrenci_numara = og.numara
            WHERE oc.sinav_id = ?
            ORDER BY oc.ogrenci_numara, oc.soru_id
        """, (sinav_id,)).fetchall()

    return jsonify({
        'sinav': {'id': sinav['id'], 'baslik': sinav['baslik']},
        'ciktilar': [dict(c) for c in ciktilar],
        'sorular': soru_listesi,
        'ogrenci_cevaplari': [dict(c) for c in cevaplar]
    })


# ── Sınav İhlal (Tam Ekran Güvenlik) ──

@exam_bp.route('/taslak_kaydet', methods=['POST'])
@seb_gerekli
def taslak_kaydet():
    """Tam ekrandan çıkışta o anki cevapları taslak olarak kaydet."""
    veri = request.get_json()
    sinav_id = veri.get('sinav_id')
    cevaplar = veri.get('cevaplar', [])
    numara = session.get('numara')

    if not sinav_id or not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Eksik bilgi'}), 400

    with db_baglantisi() as db:
        # Zaten kesin gönderim varsa dokunma
        kesin = db.execute("SELECT id FROM ogrenci_cevaplari WHERE sinav_id=? AND ogrenci_numara=? AND taslak=0 LIMIT 1",
                           (sinav_id, numara)).fetchone()
        if kesin:
            return jsonify({'durum': 'ok', 'mesaj': 'Zaten gönderilmiş'})

        # Eski taslakları sil, yenisini yaz
        db.execute("DELETE FROM ogrenci_cevaplari WHERE sinav_id=? AND ogrenci_numara=? AND taslak=1",
                   (sinav_id, numara))

        for cevap in cevaplar:
            soru_id = cevap.get('soru_id')
            soru = db.execute("SELECT puan, tip FROM sorular WHERE id=?", (soru_id,)).fetchone()
            if not soru:
                continue

            if soru['tip'] in ('cok_secmeli', 'dogru_yanlis'):
                secenek_id = cevap.get('secenek_id')
                secenek = db.execute("SELECT dogru_mu FROM secenekler WHERE id=? AND soru_id=?",
                                     (secenek_id, soru_id)).fetchone()
                puan = soru['puan'] if (secenek and secenek['dogru_mu'] == 1) else 0
                verilen_cevap = str(secenek_id)
            elif soru['tip'] == 'bosluk_doldurma':
                metin_cevap = cevap.get('metin_cevap', '').strip()
                dogru = db.execute("SELECT metin FROM secenekler WHERE soru_id=? AND dogru_mu=1",
                                   (soru_id,)).fetchone()
                puan = soru['puan'] if (dogru and metin_cevap.lower() == dogru['metin'].strip().lower()) else 0
                verilen_cevap = metin_cevap
            elif soru['tip'] == 'acik_uclu':
                verilen_cevap = cevap.get('metin_cevap', '').strip()
                puan = 0
            else:
                continue

            db.execute("INSERT INTO ogrenci_cevaplari (sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan, taslak) VALUES (?, ?, ?, ?, ?, 1)",
                       (sinav_id, numara, soru_id, verilen_cevap, puan))
        db.commit()

    return jsonify({'durum': 'ok'})


@exam_bp.route('/ihlal_bildir', methods=['POST'])
@seb_gerekli
def ihlal_bildir():
    """Tam ekrandan çıkış ihlali bildirimi."""
    veri = request.get_json()
    sinav_id = veri.get('sinav_id')
    aciklama = veri.get('aciklama', '').strip()
    numara = session.get('numara')

    if not sinav_id or not numara:
        return jsonify({'durum': 'hata'}), 400

    with db_baglantisi() as db:
        # Zaten beklemede ihlal varsa güncelle
        mevcut = db.execute("SELECT id FROM sinav_ihlaller WHERE sinav_id=? AND ogrenci_numara=? AND durum='beklemede' LIMIT 1",
                            (sinav_id, numara)).fetchone()
        if mevcut:
            db.execute("UPDATE sinav_ihlaller SET aciklama=?, zaman=CURRENT_TIMESTAMP WHERE id=?",
                       (aciklama, mevcut['id']))
        else:
            db.execute("INSERT INTO sinav_ihlaller (sinav_id, ogrenci_numara, sebep, aciklama) VALUES (?, ?, 'fullscreen_exit', ?)",
                       (sinav_id, numara, aciklama))
        db.commit()

    return jsonify({'durum': 'ok'})


@exam_bp.route('/ihlal_durum', methods=['GET'])
@seb_gerekli
def ihlal_durum():
    """Öğrenci kendi ihlal durumunu kontrol eder (polling)."""
    sinav_id = request.args.get('sinav_id')
    numara = session.get('numara')

    if not sinav_id or not numara:
        return jsonify({'durum': 'yok'})

    with db_baglantisi() as db:
        ihlal = db.execute("SELECT durum FROM sinav_ihlaller WHERE sinav_id=? AND ogrenci_numara=? ORDER BY id DESC LIMIT 1",
                           (sinav_id, numara)).fetchone()

    if not ihlal:
        return jsonify({'durum': 'yok'})

    return jsonify({'durum': ihlal['durum']})


@exam_bp.route('/ihlaller/<int:sinav_id>', methods=['GET'])
@ogretmen_giris_gerekli
def ihlalleri_getir(sinav_id):
    """Öğretmen: aktif ihlalleri listele."""
    with db_baglantisi() as db:
        ihlaller = db.execute("""
            SELECT si.*, og.ad, og.soyad
            FROM sinav_ihlaller si
            LEFT JOIN ogrenciler og ON si.ogrenci_numara = og.numara
            WHERE si.sinav_id = ?
            ORDER BY si.id DESC
        """, (sinav_id,)).fetchall()
    return jsonify({'ihlaller': [dict(i) for i in ihlaller]})


@exam_bp.route('/ihlal_onayla', methods=['POST'])
@ogretmen_giris_gerekli
def ihlal_onayla():
    """Öğretmen: öğrenciyi sınava geri dahil et."""
    veri = request.get_json()
    ihlal_id = veri.get('ihlal_id')

    if not ihlal_id:
        return jsonify({'durum': 'hata'}), 400

    with db_baglantisi() as db:
        # İhlal kaydını onayla
        db.execute("UPDATE sinav_ihlaller SET durum='onaylandi' WHERE id=?", (ihlal_id,))

        # Taslak cevapları sil — öğrenci localStorage'dan devam edecek
        ihlal = db.execute("SELECT sinav_id, ogrenci_numara FROM sinav_ihlaller WHERE id=?", (ihlal_id,)).fetchone()
        if ihlal:
            db.execute("DELETE FROM ogrenci_cevaplari WHERE sinav_id=? AND ogrenci_numara=? AND taslak=1",
                       (ihlal['sinav_id'], ihlal['ogrenci_numara']))
        db.commit()

    return jsonify({'durum': 'ok'})


@exam_bp.route('/ihlal_reddet', methods=['POST'])
@ogretmen_giris_gerekli
def ihlal_reddet():
    """Öğretmen: sınavı sonlandır, taslak cevapları kesinleştir."""
    veri = request.get_json()
    ihlal_id = veri.get('ihlal_id')

    if not ihlal_id:
        return jsonify({'durum': 'hata'}), 400

    with db_baglantisi() as db:
        db.execute("UPDATE sinav_ihlaller SET durum='reddedildi' WHERE id=?", (ihlal_id,))

        # Taslak cevapları kesinleştir
        ihlal = db.execute("SELECT sinav_id, ogrenci_numara FROM sinav_ihlaller WHERE id=?", (ihlal_id,)).fetchone()
        if ihlal:
            db.execute("UPDATE ogrenci_cevaplari SET taslak=0 WHERE sinav_id=? AND ogrenci_numara=? AND taslak=1",
                       (ihlal['sinav_id'], ihlal['ogrenci_numara']))
        db.commit()

    return jsonify({'durum': 'ok'})
