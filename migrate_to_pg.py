import sqlite3
import psycopg2
import os
from pathlib import Path
from core.db import db_olustur

def migrate_single_db(db_path, pg_conn):
    print(f"🚀 Migrating: {db_path} -> PostgreSQL")
    
    sl_conn = sqlite3.connect(db_path)
    sl_conn.row_factory = sqlite3.Row
    sl_cursor = sl_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    tables = [
        'siniflar', 'ogrenciler', 'yoklama', 'ayarlar', 
        'sahte_giris_log', 'terminal_guvenlik_log',
        'sinavlar', 'sorular', 'secenekler', 'ogrenci_cevaplari',
        'seb_cikis_log', 'seb_cikis_talepleri', 'yardim_talepleri', 'ogrenci_cikis_log'
    ]
    
    for table in tables:
        try:
            # Check if table exists in SQLite
            sl_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not sl_cursor.fetchone():
                continue

            print(f"  📦 Table: {table}...")
            sl_cursor.execute(f"SELECT * FROM {table}")
            rows = sl_cursor.fetchall()
            if not rows:
                continue
            
            columns = rows[0].keys()
            placeholders = ", ".join(["%s"] * len(columns))
            cols_str = ", ".join(columns)
            
            # Note: No TRUNCATE here to allow merging multiple DBs
            for row in rows:
                try:
                    pg_cursor.execute(
                        f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING",
                        tuple(row)
                    )
                except Exception:
                    pg_conn.rollback() # Individual row fail handle
                    continue
            
            pg_conn.commit()
            print(f"    ✅ {len(rows)} rows processed.")
        except Exception as e:
            print(f"    ❌ Error migrating {table}: {e}")
            pg_conn.rollback()
            continue

def main():
    print("🛠️ PostgreSQL tabloları kontrol ediliyor/oluşturuluyor...")
    db_olustur()
    
    pg_conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', '5432'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASS', 'postgres_pass'),
        dbname=os.environ.get('DB_NAME', 'ders_takip')
    )
    
    data_dir = Path("data")
    db_files = list(data_dir.glob("*.db"))
    
    if not db_files:
        print("⚠️ No .db files found in data/ directory.")
        return

    for db_file in db_files:
        migrate_single_db(db_file, pg_conn)
            
    pg_conn.close()
    print("✨ Overall Migration completed successfully!")

if __name__ == "__main__":
    main()
