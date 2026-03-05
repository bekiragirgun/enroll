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
