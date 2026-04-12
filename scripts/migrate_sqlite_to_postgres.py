#!/usr/bin/env python3
"""
SQLite → PostgreSQL migration.

Kullanım:
    python scripts/migrate_sqlite_to_postgres.py \
        --sqlite data/yoklama.db \
        --pg-host localhost --pg-port 5432 \
        --pg-user postgres --pg-pass postgres_pass --pg-db ders_takip \
        [--truncate] [--dry-run]

Öntanım: TRUNCATE yapmaz. Mevcut PostgreSQL verisini silmek için --truncate ver.
"""
import argparse
import sqlite3
import sys
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    print("HATA: psycopg2 yüklü değil. 'pip install psycopg2-binary' çalıştır.", file=sys.stderr)
    sys.exit(1)

# Parent → child sırasıyla (FK bağımlılıkları). Bu sıra ile TRUNCATE tersten, INSERT düzden yapılır.
TABLOLAR = [
    "siniflar",
    "ogrenciler",
    "sinavlar",
    "sorular",
    "secenekler",
    "ogrenme_ciktilari",
    "soru_cikti_iliskisi",
    "ogrenci_cevaplari",
    "sinav_ihlaller",
    "yoklama",
    "ogrenci_aktivite_log",
    "ogrenci_cikis_log",
    "sahte_giris_log",
    "seb_cikis_log",
    "seb_cikis_talepleri",
    "terminal_guvenlik_log",
    "yardim_talepleri",
    "ayarlar",
]


def pg_kolonlari(pg_cur, tablo):
    pg_cur.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema='public' AND table_name=%s "
        "ORDER BY ordinal_position",
        (tablo,),
    )
    return [r[0] for r in pg_cur.fetchall()]


def sqlite_kolonlari(sqlite_con, tablo):
    cur = sqlite_con.execute(f'PRAGMA table_info("{tablo}")')
    return [r[1] for r in cur.fetchall()]


def tablo_kopyala(sqlite_con, pg_cur, tablo, dry_run=False):
    pg_cols = pg_kolonlari(pg_cur, tablo)
    sq_cols = sqlite_kolonlari(sqlite_con, tablo)

    if not pg_cols:
        print(f"  ⚠️  {tablo}: PostgreSQL'de tablo yok, atlandı")
        return 0
    if not sq_cols:
        print(f"  ⚠️  {tablo}: SQLite'ta tablo yok, atlandı")
        return 0

    ortak = [c for c in pg_cols if c in sq_cols]
    eksik_pg = [c for c in sq_cols if c not in pg_cols]
    eksik_sq = [c for c in pg_cols if c not in sq_cols]
    if eksik_pg:
        print(f"  ℹ️  {tablo}: SQLite'ta var, PG'de yok → {eksik_pg}")
    if eksik_sq:
        print(f"  ℹ️  {tablo}: PG'de var, SQLite'ta yok → {eksik_sq} (NULL/DEFAULT bırakılacak)")

    kolon_listesi = ",".join(f'"{c}"' for c in ortak)
    sq_cur = sqlite_con.execute(f'SELECT {kolon_listesi} FROM "{tablo}"')
    rows = sq_cur.fetchall()
    if not rows:
        print(f"  ⏭️  {tablo}: 0 satır")
        return 0

    if dry_run:
        print(f"  [dry-run] {tablo}: {len(rows)} satır kopyalanacak")
        return len(rows)

    # execute_values ile toplu insert
    sql = f'INSERT INTO "{tablo}" ({kolon_listesi}) VALUES %s'
    execute_values(pg_cur, sql, rows, page_size=500)
    print(f"  ✅ {tablo}: {len(rows)} satır kopyalandı")
    return len(rows)


def sequence_guncelle(pg_cur, tablo):
    """id tabanlı tablolarda sequence'i MAX(id)+1'e taşı."""
    pg_cur.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema='public' AND table_name=%s AND column_name='id'",
        (tablo,),
    )
    if not pg_cur.fetchone():
        return
    try:
        pg_cur.execute(
            f"SELECT setval(pg_get_serial_sequence('\"{tablo}\"','id'), "
            f"COALESCE((SELECT MAX(id) FROM \"{tablo}\"), 1), true)"
        )
    except Exception as e:
        print(f"  ⚠️  {tablo}: sequence güncellenemedi → {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sqlite", default="data/yoklama.db")
    ap.add_argument("--pg-host", default="localhost")
    ap.add_argument("--pg-port", default="5432")
    ap.add_argument("--pg-user", default="postgres")
    ap.add_argument("--pg-pass", default="postgres_pass")
    ap.add_argument("--pg-db", default="ders_takip")
    ap.add_argument("--truncate", action="store_true",
                    help="Önce tüm hedef tabloları TRUNCATE et (DİKKAT: veri silinir)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Hiçbir şey yazma, sadece raporla")
    args = ap.parse_args()

    sqlite_yolu = Path(args.sqlite)
    if not sqlite_yolu.exists():
        print(f"HATA: SQLite dosyası yok: {sqlite_yolu}", file=sys.stderr)
        sys.exit(1)

    print(f"📦 Kaynak  : {sqlite_yolu}")
    print(f"🎯 Hedef   : postgres://{args.pg_user}@{args.pg_host}:{args.pg_port}/{args.pg_db}")
    print(f"🧹 Truncate: {args.truncate}   🧪 Dry-run: {args.dry_run}\n")

    sqlite_con = sqlite3.connect(sqlite_yolu)
    sqlite_con.row_factory = sqlite3.Row

    pg_con = psycopg2.connect(
        host=args.pg_host, port=args.pg_port,
        user=args.pg_user, password=args.pg_pass, dbname=args.pg_db,
    )
    pg_con.autocommit = False
    pg_cur = pg_con.cursor()

    try:
        # FK kontrollerini geçici olarak devre dışı bırak
        pg_cur.execute("SET session_replication_role = 'replica'")

        if args.truncate and not args.dry_run:
            print("🧹 TRUNCATE (ters sırayla)...")
            for tablo in reversed(TABLOLAR):
                try:
                    pg_cur.execute(f'TRUNCATE TABLE "{tablo}" RESTART IDENTITY CASCADE')
                    print(f"  🗑️  {tablo}")
                except psycopg2.errors.UndefinedTable:
                    pg_con.rollback()
                    pg_cur.execute("SET session_replication_role = 'replica'")
            print()

        print("📥 Kopyalama...")
        toplam = 0
        for tablo in TABLOLAR:
            toplam += tablo_kopyala(sqlite_con, pg_cur, tablo, dry_run=args.dry_run)

        if not args.dry_run:
            print("\n🔢 Sequence'ler güncelleniyor...")
            for tablo in TABLOLAR:
                sequence_guncelle(pg_cur, tablo)

        pg_cur.execute("SET session_replication_role = 'origin'")

        if args.dry_run:
            pg_con.rollback()
            print(f"\n🧪 Dry-run: toplam {toplam} satır kopyalanacaktı (hiçbir şey yazılmadı)")
        else:
            pg_con.commit()
            print(f"\n✅ TAMAM: toplam {toplam} satır kopyalandı ve commit edildi")

    except Exception as e:
        pg_con.rollback()
        print(f"\n❌ HATA: {e}", file=sys.stderr)
        raise
    finally:
        pg_cur.close()
        pg_con.close()
        sqlite_con.close()


if __name__ == "__main__":
    main()
