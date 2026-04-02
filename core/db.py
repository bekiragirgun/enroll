import os
import sqlite3
import logging
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None

from core.paths import DB_YOLU

_log = logging.getLogger('app')

# Global DB sağlık durumu — False ise öğrenci girişi engellenir
db_saglikli = True

def db_baglantisi():
    global db_saglikli
    db_type = os.environ.get('DB_TYPE', 'sqlite').lower()

    if db_type == 'postgres':
        if not psycopg2:
            _log.error("❌ psycopg2 kütüphanesi yüklü değil! 'pip install psycopg2-binary' komutunu çalıştırın.")
            raise ImportError("psycopg2 not installed")
        
        try:
            baglanti = psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                port=os.environ.get('DB_PORT', '5432'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASS', 'postgres_pass'),
                dbname=os.environ.get('DB_NAME', 'ders_takip')
            )
            # SQLite 'Row' benzeri davranış için RealDictCursor kullanıyoruz
            # Ancak biz genel bir wrapper yazacağımız için standardı koruyalım veya cursor factory ayarlı kalsın
            if not db_saglikli:
                _log.info("✅ PostgreSQL bağlantısı kuruldu")
                db_saglikli = True
            return baglanti
        except Exception as e:
            db_saglikli = False
            _log.error(f"❌ PostgreSQL bağlantı hatası: {e}")
            raise
    else:
        # Varsayılan SQLite
        DB_YOLU.parent.mkdir(exist_ok=True)
        try:
            baglanti = sqlite3.connect(DB_YOLU, timeout=5)
            baglanti.row_factory = sqlite3.Row
            if not db_saglikli:
                _log.info("✅ SQLite bağlantısı kuruldu")
                db_saglikli = True
            return baglanti
        except sqlite3.OperationalError as e:
            db_saglikli = False
            _log.error(f"❌ SQLite açılamıyor: {e}")
            raise

class DBWrapper:
    """SQLite (?) ve PostgreSQL (%s) parametre uyumsuzluğunu çözen wrapper"""
    def __init__(self, conn):
        self.conn = conn
        self.db_type = 'postgres' if hasattr(conn, 'cursor_factory') or 'psycopg2' in str(type(conn)) else 'sqlite'

    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        if self.db_type == 'postgres':
            # ? -> %s dönüşümü
            query = query.replace('?', '%s')
            # AUTOINCREMENT -> SERIAL (Sadece tablo oluştururken lazım, ama genel execute için de ufak dokunuşlar gerekebilir)
            # Create table sorgularında manuel kontrol daha güvenli
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor

    def commit(self):
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

def _kolon_ekle(cursor, db_type, tablo, kolon, tip_default):
    """Kolon yoksa ekle — PostgreSQL ve SQLite uyumlu."""
    if db_type == 'postgres':
        cursor.execute(
            "SELECT 1 FROM information_schema.columns WHERE table_name=%s AND column_name=%s",
            (tablo, kolon)
        )
        if not cursor.fetchone():
            cursor.execute(f"ALTER TABLE {tablo} ADD COLUMN {kolon} {tip_default}")
    else:
        # SQLite: PRAGMA ile kontrol
        cursor.execute(f"PRAGMA table_info({tablo})")
        kolonlar = [row[1] for row in cursor.fetchall()]
        if kolon not in kolonlar:
            cursor.execute(f"ALTER TABLE {tablo} ADD COLUMN {kolon} {tip_default}")


def db_olustur():
    db_type = os.environ.get('DB_TYPE', 'sqlite').lower()
    
    with db_baglantisi() as conn:
        cursor = conn.cursor()
        
        # PostgreSQL için AUTOINCREMENT yerine SERIAL, PRIMARY KEY AUTOINCREMENT yerine SERIAL PRIMARY KEY
        id_type = "SERIAL PRIMARY KEY" if db_type == 'postgres' else "INTEGER PRIMARY KEY AUTOINCREMENT"
        
        # Tabloları oluştur
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS yoklama (
                id        {id_type},
                tarih     TEXT NOT NULL,
                ad_soyad  TEXT NOT NULL,
                numara    TEXT NOT NULL,
                saat      TEXT NOT NULL,
                sinif     TEXT NOT NULL DEFAULT '',
                paket     TEXT NOT NULL DEFAULT '—',
                ip        TEXT NOT NULL DEFAULT '',
                kaynak    TEXT NOT NULL DEFAULT 'web'
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS siniflar (
                id   {id_type},
                ad   TEXT UNIQUE NOT NULL
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ogrenciler (
                id        {id_type},
                sinif_id  INTEGER NOT NULL,
                numara    TEXT UNIQUE NOT NULL,
                ad        TEXT NOT NULL,
                soyad     TEXT NOT NULL,
                sifre     TEXT NOT NULL DEFAULT ''
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS sahte_giris_log (
                id             {id_type},
                tarih          TEXT NOT NULL,
                saat           TEXT NOT NULL,
                ip             TEXT NOT NULL,
                gercek_numara  TEXT NOT NULL,
                gercek_ad      TEXT NOT NULL,
                denenen_numara TEXT NOT NULL DEFAULT '',
                denenen_ad     TEXT NOT NULL DEFAULT '',
                sinif          TEXT NOT NULL DEFAULT ''
            )
        """)
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ayarlar (
                anahtar  TEXT PRIMARY KEY,
                deger    TEXT NOT NULL
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS terminal_guvenlik_log (
                id             {id_type},
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

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS sinavlar (
                id {id_type},
                baslik TEXT NOT NULL,
                aktif INTEGER DEFAULT 0,
                olusturma_tarihi TEXT NOT NULL
            )
        """)
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS sorular (
                id {id_type},
                sinav_id INTEGER NOT NULL,
                metin TEXT NOT NULL,
                tip TEXT NOT NULL DEFAULT 'cok_secmeli',
                puan INTEGER DEFAULT 10
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS secenekler (
                id {id_type},
                soru_id INTEGER NOT NULL,
                metin TEXT NOT NULL,
                dogru_mu INTEGER DEFAULT 0
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ogrenci_cevaplari (
                id {id_type},
                sinav_id INTEGER NOT NULL,
                ogrenci_numara TEXT NOT NULL,
                soru_id INTEGER NOT NULL,
                verilen_cevap TEXT NOT NULL,
                puan INTEGER DEFAULT 0,
                cevap_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ogrenme_ciktilari (
                id {id_type},
                sinav_id INTEGER NOT NULL,
                numara INTEGER NOT NULL,
                metin TEXT NOT NULL
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS soru_cikti_iliskisi (
                id {id_type},
                soru_id INTEGER NOT NULL,
                cikti_id INTEGER NOT NULL
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS sinav_ihlaller (
                id {id_type},
                sinav_id INTEGER NOT NULL,
                ogrenci_numara TEXT NOT NULL,
                sebep TEXT NOT NULL DEFAULT 'fullscreen_exit',
                aciklama TEXT DEFAULT '',
                zaman TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                durum TEXT NOT NULL DEFAULT 'beklemede'
            )
        """)

        # Mevcut tablolara yeni kolonlar (ALTER — yoksa ekle, varsa atla)
        _kolon_ekle(cursor, db_type, 'sorular', 'bloom_seviyesi', "TEXT DEFAULT ''")
        _kolon_ekle(cursor, db_type, 'sorular', 'zorluk', "TEXT DEFAULT ''")
        _kolon_ekle(cursor, db_type, 'ogrenci_cevaplari', 'taslak', "INTEGER DEFAULT 0")

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS seb_cikis_log (
                id {id_type},
                tarih TEXT NOT NULL,
                saat TEXT NOT NULL,
                numara TEXT NOT NULL,
                ad_soyad TEXT NOT NULL,
                ip TEXT NOT NULL
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS seb_cikis_talepleri (
                id {id_type},
                tarih TEXT NOT NULL,
                saat TEXT NOT NULL,
                numara TEXT NOT NULL,
                ad_soyad TEXT NOT NULL,
                durum TEXT DEFAULT 'bekliyor'
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS yardim_talepleri (
                id {id_type},
                tarih TEXT NOT NULL,
                saat TEXT NOT NULL,
                numara TEXT NOT NULL,
                ad_soyad TEXT NOT NULL,
                durum TEXT DEFAULT 'bekliyor',
                kategori TEXT DEFAULT ''
            )
        """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ogrenci_cikis_log (
                id       {id_type},
                tarih    TEXT NOT NULL,
                saat     TEXT NOT NULL,
                numara   TEXT NOT NULL,
                ad_soyad TEXT NOT NULL,
                paket    TEXT NOT NULL,
                ip       TEXT NOT NULL DEFAULT '',
                kaynak   TEXT NOT NULL DEFAULT 'ogrenci'
            )
        """)

        # Yeni Aktivite Log Tablosu
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ogrenci_aktivite_log (
                id            {id_type},
                numara        TEXT NOT NULL,
                ip            TEXT NOT NULL,
                aktivite_tipi TEXT NOT NULL,
                detay         TEXT,
                tarih         TEXT NOT NULL,
                saat          TEXT NOT NULL
            )
        """)

        conn.commit()


def test_verilerini_yukle(count=30):
    """Test modu için örnek sınıflar ve öğrenciler ekler."""
    with db_baglantisi() as conn:
        cursor = conn.cursor()
        
        # 1. Örnek Sınıflar
        siniflar = [
            (f'Test Sınıfı ({count} Kişi)',),
            ('Bilgisayar Programcılığı',),
            ('Siber Güvenlik',),
            ('İnsansız Hava Aracı Teknolojisi',)
        ]
        for sinif in siniflar:
            cursor.execute("INSERT INTO siniflar (ad) VALUES (?) ON CONFLICT(ad) DO NOTHING", sinif)
        
        # Sınıf ID'lerini al
        cursor.execute("SELECT id, ad FROM siniflar")
        sinif_map = {ad: id for id, ad in cursor.fetchall()}
        test_sinif_id = sinif_map[f'Test Sınıfı ({count} Kişi)']
        
        # 2. N Tane Test Öğrencisi Oluştur
        ogrenciler = []
        for i in range(1, count + 1):
            numara = f"test{i}"
            ogrenciler.append((test_sinif_id, numara, f"Öğrenci-{i}", "TEST", "1234"))
        
        for ogr in ogrenciler:
            cursor.execute("""
                INSERT INTO ogrenciler (sinif_id, numara, ad, soyad, sifre) 
                VALUES (?, ?, ?, ?, ?) 
                ON CONFLICT(numara) DO NOTHING
            """, ogr)
        
        conn.commit()
        
        # 2.5 Test modu için varsayılan ayarları ekle
        test_ayarlar = [
            ('kiosk_modu', '0'),          # SEB zorunluluğunu kapat
            ('ip_kontrol', '0'),          # Aynı IP'den birden fazla giriş engeli kaldır
            ('ders_gunleri', '0,1,2,3,4,5,6'),  # Her gün ders günü olsun
            ('ogretmen_sifre', '1234'),   # Bilinen bir öğretmen şifresi
            ('cikis_izni', '1'),          # SEB çıkış izni açık
            ('devamsizlik_esik', '3'),    # Devamsızlık eşiği
        ]
        for anahtar, deger in test_ayarlar:
            cursor.execute("INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES (?, ?)", (anahtar, deger))
        
        conn.commit()
        
        # 3. Tüm test öğrencilerini bugünün yoklamasına ekle (otomatik giriş)
        from datetime import datetime
        tarih = datetime.now().strftime('%Y-%m-%d')
        saat = datetime.now().strftime('%H:%M')
        sinif_ad = f'Test Sınıfı ({count} Kişi)'
        
        for i in range(1, count + 1):
            numara = f"test{i}"
            ad_soyad = f"Öğrenci-{i} TEST"
            cursor.execute("""
                INSERT INTO yoklama (tarih, ad_soyad, numara, saat, sinif, paket, ip, kaynak)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT DO NOTHING
            """, (tarih, ad_soyad, numara, saat, sinif_ad, 'test-paket', '127.0.0.1', 'test'))
        
        conn.commit()
        _log.info(f"📊 {count} test öğrencisi başarıyla yüklendi.")

        # 4. Test Sınavı Oluştur
        cursor.execute("INSERT INTO sinavlar (baslik, aktif, olusturma_tarihi) VALUES (?, ?, ?)",
                       ("İşletim Sistemleri Quiz", 1, tarih))
        sinav_id = cursor.lastrowid

        # 5. Öğrenme Çıktıları
        ciktilar = [
            "Dosya yönetim komutlarını bilir ve uygular",
            "Dizin oluşturma ve yönetmeyi bilir",
            "Arşivleme araçlarını (tar, zip, gzip) bilir ve uygular",
        ]
        cikti_idler = []
        for i, metin in enumerate(ciktilar, 1):
            cursor.execute("INSERT INTO ogrenme_ciktilari (sinav_id, numara, metin) VALUES (?, ?, ?)",
                           (sinav_id, i, metin))
            cikti_idler.append(cursor.lastrowid)

        # 6. Farklı tipte sorular (bloom + zorluk + çıktı ilişkisi)
        import random

        # Soru 1: Çoktan seçmeli
        cursor.execute("INSERT INTO sorular (sinav_id, metin, tip, puan, bloom_seviyesi, zorluk) VALUES (?, ?, ?, ?, ?, ?)",
                       (sinav_id, "cp komutu ne işe yarar?", "cok_secmeli", 20, "bilgi", "kolay"))
        s1 = cursor.lastrowid
        s1_secenekler = []
        for metin, dogru in [("Dosya kopyalar", 1), ("Dosya siler", 0), ("Dosya taşır", 0), ("Klasör listeler", 0)]:
            cursor.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, ?, ?)", (s1, metin, dogru))
            s1_secenekler.append((cursor.lastrowid, dogru))
        cursor.execute("INSERT INTO soru_cikti_iliskisi (soru_id, cikti_id) VALUES (?, ?)", (s1, cikti_idler[0]))

        # Soru 2: Çoktan seçmeli
        cursor.execute("INSERT INTO sorular (sinav_id, metin, tip, puan, bloom_seviyesi, zorluk) VALUES (?, ?, ?, ?, ?, ?)",
                       (sinav_id, "Hangi komut dizin oluşturur?", "cok_secmeli", 20, "kavrama", "kolay"))
        s2 = cursor.lastrowid
        s2_secenekler = []
        for metin, dogru in [("mkdir", 1), ("touch", 0), ("rmdir", 0), ("ls", 0)]:
            cursor.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, ?, ?)", (s2, metin, dogru))
            s2_secenekler.append((cursor.lastrowid, dogru))
        cursor.execute("INSERT INTO soru_cikti_iliskisi (soru_id, cikti_id) VALUES (?, ?)", (s2, cikti_idler[1]))

        # Soru 3: Doğru/Yanlış
        cursor.execute("INSERT INTO sorular (sinav_id, metin, tip, puan, bloom_seviyesi, zorluk) VALUES (?, ?, ?, ?, ?, ?)",
                       (sinav_id, "tar komutu dosyaları arşivlemek için kullanılır", "dogru_yanlis", 10, "bilgi", "cok_kolay"))
        s3 = cursor.lastrowid
        cursor.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, 'Doğru', 1)", (s3,))
        s3_dogru_id = cursor.lastrowid
        cursor.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, 'Yanlış', 0)", (s3,))
        s3_yanlis_id = cursor.lastrowid
        cursor.execute("INSERT INTO soru_cikti_iliskisi (soru_id, cikti_id) VALUES (?, ?)", (s3, cikti_idler[2]))

        # Soru 4: Boşluk doldurma
        cursor.execute("INSERT INTO sorular (sinav_id, metin, tip, puan, bloom_seviyesi, zorluk) VALUES (?, ?, ?, ?, ?, ?)",
                       (sinav_id, "Dosya silmek için kullanılan komut: ___", "bosluk_doldurma", 25, "uygulama", "orta"))
        s4 = cursor.lastrowid
        cursor.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, 'rm', 1)", (s4,))
        for cid in [cikti_idler[0], cikti_idler[1]]:
            cursor.execute("INSERT INTO soru_cikti_iliskisi (soru_id, cikti_id) VALUES (?, ?)", (s4, cid))

        # Soru 5: Açık uçlu
        cursor.execute("INSERT INTO sorular (sinav_id, metin, tip, puan, bloom_seviyesi, zorluk) VALUES (?, ?, ?, ?, ?, ?)",
                       (sinav_id, "Linux dosya sistemi hiyerarşisini kısaca açıklayın", "acik_uclu", 25, "analiz", "zor"))
        s5 = cursor.lastrowid
        cursor.execute("INSERT INTO soru_cikti_iliskisi (soru_id, cikti_id) VALUES (?, ?)", (s5, cikti_idler[0]))

        # 7. Öğrenci Cevaplarını Simüle Et (sadece çoktan seçmeli + D/Y için)
        for j in range(1, count + 1):
            numara = f"test{j}"
            # S1: çoktan seçmeli
            sec_id, dogru = random.choice(s1_secenekler)
            cursor.execute("INSERT INTO ogrenci_cevaplari (sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan) VALUES (?, ?, ?, ?, ?)",
                           (sinav_id, numara, s1, str(sec_id), 20 if dogru else 0))
            # S2: çoktan seçmeli
            sec_id, dogru = random.choice(s2_secenekler)
            cursor.execute("INSERT INTO ogrenci_cevaplari (sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan) VALUES (?, ?, ?, ?, ?)",
                           (sinav_id, numara, s2, str(sec_id), 20 if dogru else 0))
            # S3: doğru/yanlış
            sec_id = random.choice([s3_dogru_id, s3_yanlis_id])
            cursor.execute("INSERT INTO ogrenci_cevaplari (sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan) VALUES (?, ?, ?, ?, ?)",
                           (sinav_id, numara, s3, str(sec_id), 10 if sec_id == s3_dogru_id else 0))
            # S4: boşluk doldurma
            cevap = random.choice(["rm", "rm", "rm", "delete", "del"])
            cursor.execute("INSERT INTO ogrenci_cevaplari (sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan) VALUES (?, ?, ?, ?, ?)",
                           (sinav_id, numara, s4, cevap, 25 if cevap.lower() == "rm" else 0))
            # S5: açık uçlu (puan=0, öğretmen değerlendirecek)
            cursor.execute("INSERT INTO ogrenci_cevaplari (sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan) VALUES (?, ?, ?, ?, ?)",
                           (sinav_id, numara, s5, "/ kök dizin, /home kullanıcılar, /etc ayarlar...", 0))

        conn.commit()
        _log.info("📝 Test sınavı (5 tip soru + rubrik) ve öğrenci cevapları simüle edildi.")


