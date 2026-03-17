"""
Test DB seed data — 40 öğrenci + test sınıfı + ayarlar
python app.py --test ile başlatıldığında otomatik çağrılır.
"""

def seed_test_db():
    """Test DB'sine 40 öğrenci, test sınıfı ve ayarları yükle."""
    from core.db import db_baglantisi

    with db_baglantisi() as db:
        # Test sınıfı oluştur
        db.execute("INSERT OR IGNORE INTO siniflar (id, ad) VALUES (99, 'YUK-TEST')")

        # 40 test öğrencisi
        for i in range(1, 41):
            numara = f'T{i:04d}'
            ad = f'TEST{i:02d}'
            soyad = 'OGRENCI'
            db.execute(
                'INSERT OR IGNORE INTO ogrenciler (sinif_id, numara, ad, soyad, sifre) VALUES (?, ?, ?, ?, ?)',
                (99, numara, ad, soyad, numara)
            )

        # Chroot host ayarı (yeni VM IP)
        db.execute("INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES ('chroot_host', '10.211.55.17')")
        db.execute("INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES ('chroot_port', '22')")
        db.execute("INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES ('chroot_user', 'bekir')")
        db.execute("INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES ('chroot_pass', '123123!!')")
        db.execute("INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES ('kiosk_modu', '0')")
        db.execute("INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES ('ip_kontrol', '0')")

        db.commit()

    print('  ✅ Test DB seed tamamlandı: 40 öğrenci (T0001-T0040), sınıf: YUK-TEST')
    print('  📡 Chroot Host: 10.211.55.17 (bekir/123123!!)')
    print('  🔓 Kiosk modu: Kapalı, IP kontrol: Kapalı')
