# Hizli Baslangic

## Gereksinimler

- **Ana sunucu (Flask):** Python 3.11+, pip
- **Chroot sunucusu:** Debian 12 ARM64 (veya x64), SSH erisimi
- **Ogrenci:** Modern tarayici (veya SEB)

## 1. Production Kurulumu (Docker)

```bash
git clone https://github.com/bekiragirgun/enroll.git
cd enroll
docker compose up -d
```

Sistem `http://localhost:3333` adresinde baslar.

- Ogretmen paneli: `http://localhost:3333/teacher`
- Varsayilan sifre: `.env` dosyasinda tanimli

## 2. Lokal Gelistirme / Test

```bash
# Conda ortami
conda create -n kapadokya-DT python=3.11 -y
conda activate kapadokya-DT
pip install -r requirements.txt

# Test modu (SQLite, ornek veriler)
DB_TYPE=sqlite python app.py --test --host CHROOT_IP --user bekir --port 3333

# Production modu (SQLite)
DB_TYPE=sqlite python app.py --host CHROOT_IP
```

!!! warning "Test Modu"
    `--test` modu `test_yoklama.db` kullanir. Production `yoklama.db`'ye dokunmaz.
    Her baslatmada test DB sifirlanir.

## 3. Chroot Sunucusu Kurulumu

Bkz: [DEB Paketi Kurulumu](deb-paketi.md)

## 4. Ilk Yapilandirma

Ogretmen paneline girin ve **Ayarlar** sekmesinden:

1. **Chroot Host**: VM IP adresi (orn: `10.211.55.27`)
2. **SSH User/Pass**: VM kullanicisi
3. **Sistem IP**: Ogrencilerin eristigi adres (orn: `http://10.211.55.2:3333`)
4. **Ders Gunleri**: Hangi gunler ders var (varsayilan: Pazartesi)
5. **Baglanti Test Et** butonuyla dogrulayin
