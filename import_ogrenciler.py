#!/usr/bin/env python3
"""
Öğrenci listesini XML'den SQLite veritabanına aktarır.

Kullanım:
    python3 import_ogrenciler.py <xml_dosyasi> [sinif_adi]

Örnek:
    python3 import_ogrenciler.py ogrenciler.xml "Yazılım Geliştirme"
"""

import sys
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

DB_YOLU = Path(__file__).parent / 'data' / 'yoklama.db'


def db_tabloları_olustur(db):
    db.execute("""
        CREATE TABLE IF NOT EXISTS siniflar (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            ad   TEXT UNIQUE NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS ogrenciler (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            sinif_id  INTEGER NOT NULL REFERENCES siniflar(id),
            numara    TEXT UNIQUE NOT NULL,
            ad        TEXT NOT NULL,
            soyad     TEXT NOT NULL
        )
    """)
    db.commit()


def import_ogrenciler(xml_yolu, sinif_adi):
    tree = ET.parse(xml_yolu)
    root = tree.getroot()

    ogrenciler = []
    atlananlar = []

    for row in root.findall('Table1'):
        numara = (row.findtext('DATATEXT3') or '').strip()
        ad     = (row.findtext('DATATEXT4') or '').strip().upper()
        soyad  = (row.findtext('DATATEXT5') or '').strip().upper()

        if not numara or not ad or not soyad:
            atlananlar.append(f"numara={numara!r}, ad={ad!r}, soyad={soyad!r}")
            continue

        ogrenciler.append((numara, ad, soyad))

    if atlananlar:
        print(f"  ⚠️  Eksik veri nedeniyle {len(atlananlar)} satır atlandı:")
        for a in atlananlar:
            print(f"       {a}")

    print(f"  📋 {len(ogrenciler)} öğrenci bulundu.")

    DB_YOLU.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_YOLU) as db:
        db.row_factory = sqlite3.Row
        db_tabloları_olustur(db)

        # Sınıfı ekle (varsa güncelleme yok, sadece yoksayma)
        db.execute("INSERT OR IGNORE INTO siniflar (ad) VALUES (?)", (sinif_adi,))
        sinif_id = db.execute(
            "SELECT id FROM siniflar WHERE ad=?", (sinif_adi,)
        ).fetchone()[0]

        eklenen = 0
        guncellenen = 0

        for numara, ad, soyad in ogrenciler:
            mevcut = db.execute(
                "SELECT id FROM ogrenciler WHERE numara=?", (numara,)
            ).fetchone()

            if mevcut:
                db.execute(
                    "UPDATE ogrenciler SET ad=?, soyad=?, sinif_id=? WHERE numara=?",
                    (ad, soyad, sinif_id, numara)
                )
                guncellenen += 1
            else:
                db.execute(
                    "INSERT INTO ogrenciler (sinif_id, numara, ad, soyad) VALUES (?,?,?,?)",
                    (sinif_id, numara, ad, soyad)
                )
                eklenen += 1

        db.commit()

    print(f"  ✅ {eklenen} öğrenci eklendi, {guncellenen} öğrenci güncellendi.")
    print(f"  📚 Sınıf: '{sinif_adi}' (id={sinif_id})")

    # Özet listesi
    print()
    print("  Kayıtlı öğrenciler:")
    print("  " + "-" * 40)
    for i, (numara, ad, soyad) in enumerate(ogrenciler, 1):
        print(f"  {i:2d}. {numara}  {ad} {soyad}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    xml_yolu  = sys.argv[1]
    sinif_adi = sys.argv[2] if len(sys.argv) > 2 else 'Yazılım Geliştirme'

    print()
    print(f"  📥 '{xml_yolu}' → '{sinif_adi}' sınıfına aktarılıyor...")
    print()
    import_ogrenciler(xml_yolu, sinif_adi)
    print()
