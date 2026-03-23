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
                       ("Python Temelleri Test Sınavı", 1, tarih))
        sinav_id = cursor.lastrowid

        # 5. 5 Tane Soru Ekle
        sorular = [
            ("Python'da ekrana yazı yazdırmak için hangi fonksiyon kullanılır?", 20),
            ("Hangi veri tipi tam sayıları ifade eder?", 20),
            ("Listeye eleman eklemek için hangi metod kullanılır?", 20),
            ("Python dosya uzantısı nedir?", 20),
            ("Hangisi bir döngü tipidir?", 20)
        ]
        
        secenek_kumeleri = [
            [("print()", 1), ("output()", 0), ("echo", 0), ("write()", 0)],
            [("int", 1), ("str", 0), ("float", 0), ("bool", 0)],
            [("append()", 1), ("add()", 0), ("insert_last()", 0), ("push()", 0)],
            [(".py", 1), (".python", 0), (".txt", 0), (".exe", 0)],
            [("for", 1), ("if", 0), ("def", 0), ("class", 0)]
        ]

        import random
        for i, (soru_metni, puan) in enumerate(sorular):
            cursor.execute("INSERT INTO sorular (sinav_id, metin, puan) VALUES (?, ?, ?)", 
                           (sinav_id, soru_metni, puan))
            soru_id = cursor.lastrowid
            
            eklenen_secenekler = []
            for sec_metin, dogru_mu in secenek_kumeleri[i]:
                cursor.execute("INSERT INTO secenekler (soru_id, metin, dogru_mu) VALUES (?, ?, ?)", 
                               (soru_id, sec_metin, dogru_mu))
                eklenen_secenekler.append((cursor.lastrowid, dogru_mu))

            # 6. Öğrenci Cevaplarını Simüle Et
            for j in range(1, count + 1):
                numara = f"test{j}"
                # Rastgele bir seçenek seç (öğrencilerin bir kısmı doğru bilsin)
                secilen_id, dogru_mu = random.choice(eklenen_secenekler)
                ogr_puan = puan if dogru_mu else 0
                
                cursor.execute("""
                    INSERT INTO ogrenci_cevaplari (sinav_id, ogrenci_numara, soru_id, verilen_cevap, puan)
                    VALUES (?, ?, ?, ?, ?)
                """, (sinav_id, numara, soru_id, str(secilen_id), ogr_puan))
        
        conn.commit()
        _log.info("📝 Test sınavı ve 30 öğrencinin cevapları simüle edildi.")


