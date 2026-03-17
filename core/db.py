import sqlite3
from core.paths import DB_YOLU

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
        try: db.execute("ALTER TABLE yoklama ADD COLUMN sinif TEXT NOT NULL DEFAULT ''")
        except: pass
        try: db.execute("ALTER TABLE yoklama ADD COLUMN paket TEXT NOT NULL DEFAULT '—'")
        except: pass
        try: db.execute("ALTER TABLE yoklama ADD COLUMN ip TEXT NOT NULL DEFAULT ''")
        except: pass
        try: db.execute("ALTER TABLE yoklama ADD COLUMN kaynak TEXT NOT NULL DEFAULT 'web'")
        except: pass

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
        try: db.execute("ALTER TABLE ogrenciler ADD COLUMN sifre TEXT NOT NULL DEFAULT ''")
        except: pass

        # Şüpheli giriş denemeleri logu (başkası adına imza atma)
        db.execute("""
            CREATE TABLE IF NOT EXISTS sahte_giris_log (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
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
        
        # Sistem ayarları tablosu (V14 Persistence)
        db.execute("""
            CREATE TABLE IF NOT EXISTS ayarlar (
                anahtar  TEXT PRIMARY KEY,
                deger    TEXT NOT NULL
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

        # ── Sınav / Quiz Modülü Tabloları ──
        
        # 1. Sınavlar
        db.execute("""
            CREATE TABLE IF NOT EXISTS sinavlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                baslik TEXT NOT NULL,
                aktif INTEGER DEFAULT 0,
                olusturma_tarihi TEXT NOT NULL
            )
        """)
        
        # 2. Sorular
        db.execute("""
            CREATE TABLE IF NOT EXISTS sorular (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sinav_id INTEGER NOT NULL REFERENCES sinavlar(id) ON DELETE CASCADE,
                metin TEXT NOT NULL,
                tip TEXT NOT NULL DEFAULT 'cok_secmeli',
                puan INTEGER DEFAULT 10
            )
        """)

        # 3. Seçenekler
        db.execute("""
            CREATE TABLE IF NOT EXISTS secenekler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                soru_id INTEGER NOT NULL REFERENCES sorular(id) ON DELETE CASCADE,
                metin TEXT NOT NULL,
                dogru_mu INTEGER DEFAULT 0
            )
        """)

        # 4. Öğrenci Cevapları
        db.execute("""
            CREATE TABLE IF NOT EXISTS ogrenci_cevaplari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sinav_id INTEGER NOT NULL REFERENCES sinavlar(id) ON DELETE CASCADE,
                ogrenci_numara TEXT NOT NULL,
                soru_id INTEGER NOT NULL REFERENCES sorular(id) ON DELETE CASCADE,
                verilen_cevap TEXT NOT NULL,
                puan INTEGER DEFAULT 0
            )
        """)

        # SEB Çıkış Logları
        db.execute("""
            CREATE TABLE IF NOT EXISTS seb_cikis_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT NOT NULL,
                saat TEXT NOT NULL,
                numara TEXT NOT NULL,
                ad_soyad TEXT NOT NULL,
                ip TEXT NOT NULL
            )
        """)

        # SEB Çıkış Talepleri
        db.execute("""
            CREATE TABLE IF NOT EXISTS seb_cikis_talepleri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT NOT NULL,
                saat TEXT NOT NULL,
                numara TEXT NOT NULL,
                ad_soyad TEXT NOT NULL,
                durum TEXT DEFAULT 'bekliyor'
            )
        """)

        # Yardım Talepleri
        db.execute("""
            CREATE TABLE IF NOT EXISTS yardim_talepleri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT NOT NULL,
                saat TEXT NOT NULL,
                numara TEXT NOT NULL,
                ad_soyad TEXT NOT NULL,
                durum TEXT DEFAULT 'bekliyor',
                kategori TEXT DEFAULT ''
            )
        """)
        try: db.execute("ALTER TABLE yardim_talepleri ADD COLUMN kategori TEXT DEFAULT ''")
        except: pass


