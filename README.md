# Kapadokya Universitesi — Linux Laboratuvari Ders Takip Sistemi

Kapadokya Universitesi Linux dersleri icin gelistirilmis, gercek zamanli yoklama, slayt senkronizasyonu, sinav modulu ve izole terminal ortami saglayan kapsamli bir egitim platformudur.

## Ozellikler

### Ogretmen Paneli
- **Yoklama Yonetimi** — Gercek zamanli ogrenci giris takibi, tarih/paket filtreleme, CSV export
- **Devam Raporu** — Ogrenci bazinda haftalik/aylik devam matrisi, devamsizlik uyari esigi
- **Slayt Yayini** — HTML slaytlari ogrenci ekranlarinda senkronize gosterme
- **Terminal Yayini** — Ogretmen terminalini canli olarak ogrencilere yansitma
- **Terminal Izleme** — Herhangi bir ogrencinin terminalini canli izleme ve mudahale etme
- **Sinav Modulu** — Coktan secmeli sinav olusturma, otomatik puanlama
- **Ogrenci Yonetimi** — Sinif ve ogrenci ekleme/cikarma
- **Yardim Talepleri** — Kategorili yardim sistemi (komut, dosya, terminal, soru, diger)
- **Toplu Cikis** — Paket degisiminde tum ogrencileri tek tusla cikis yaptirma
- **IP Kontrol** — Ayni IP'den farkli ogrenci girisini engelleme (acilip kapatilabilir)
- **SEB Entegrasyonu** — Safe Exam Browser zorunlulugu ve cikis yonetimi

### Ogrenci Tarafi
- **Yoklama Girisi** — Sinif, ad soyad ve ogrenci numarasi ile giris
- **Devam Durumu** — Kendi devam gecmisini ve katilim yuzdesini gorme
- **Izole Terminal** — Chroot tabanli, tamamen izole Linux ortami
- **Sinav** — Coktan secmeli sinav cevaplama
- **Yardim Talebi** — Kategorili yardim isteme

### Altyapi
- **Chroot Izolasyon** — Her ogrenci icin ayri chroot ortami (debootstrap tabanli)
- **DEB Paketi** — VM tarafini tek komutla kuran `chroot-terminal` paketi
- **PTY Stabilite** — Otomatik PTY onarim ve temizleme servisleri
- **Kernel Optimizasyonu** — PTY, fd, TCP, ulimit ayarlari (deb ile otomatik)
- **Yuk Testi** — 40 esanlamli ogrenci giris simulasyonu

## Mimari

```
[Ogretmen Mac/PC]                    [Ogrenci Tarayici]
        |                                    |
        v                                    v
+------------------+              +------------------+
|  Flask + SocketIO |<--- HTTP -->|  Polling (1s)    |
|  (app.py :3333)   |             |  ogrenci.js      |
+------------------+              +------------------+
        |
        | SSH (sshpass)
        v
+------------------+
|  Ubuntu VM       |
|  (chroot-terminal|
|   deb paketi)    |
|  - chroot/user1  |
|  - chroot/user2  |
|  - ...           |
+------------------+
```

## Kurulum

### 1. Ana Sunucu (Flask)

```bash
# Python ortami
conda create -n ders_takip python=3.11 -y
conda activate ders_takip

# Bagimliliklar
pip install -r requirements.txt

# Baslat
python app.py
```

### 2. Ogrenci VM (Chroot Sunucusu)

```bash
# Repo indir
git clone https://github.com/bekiragirgun/enroll.git
cd enroll/deb-package

# DEB paketi olustur ve kur
bash build.sh
sudo apt install ./chroot-terminal_1.3.deb

# Chroot sablonunu olustur (ilk sefer, ~10dk)
sudo chroot-yonetici init

# Kontrol
chroot-yonetici health
```

DEB paketi otomatik olarak su ayarlari yapar:
- Kernel optimizasyonu (PTY, fd, TCP limitleri)
- Ulimit ayarlari (fork bomb korumasi dahil)
- SSH optimizasyonu (MaxSessions 80, keepalive)
- NTP senkronizasyonu (Europe/Istanbul)
- Boot'ta PTY onarimi servisi
- 10dk'da bir temizleme timer'i

### 3. Ayarlar (Ogretmen Paneli)

Ogretmen panelindeki Ayarlar tabindan:
- **Chroot Host**: VM IP adresi
- **Chroot Port**: SSH portu (varsayilan: 22)
- **Chroot User/Pass**: SSH kullanicisi ve sifresi
- **Kiosk Modu**: SEB zorunlulugu acma/kapama
- **IP Kontrol**: Ayni IP engelleme acma/kapama
- **Devamsizlik Esigi**: Uyari icin devamsizlik sayisi

## Kullanim

### Ogretmen

```
http://localhost:3333/teacher
Sifre: linux2024
```

- **Beklet/Slayt/Terminal** modlari arasinda gecis
- **Devam Raporu** tabindan devam takibi ve CSV export
- **Terminal sayfasindan** ogrenci terminallerini izleme/mudahale
- **Toplu Cikis** butonu ile paket degisiminde tum ogrencileri cikartma

### Ogrenci

```
http://sunucu-ip:3333
```

1. Sinif sec → Ad soyad sec → Ogrenci numarasi gir → Paket sec
2. "Derse Katil" butonu ile tam ekrana gec
3. Ogretmen mod degistirdikce slayt/terminal/sinav otomatik yuklenir

## Test Modu

Production DB'ye dokunmadan yuk testi:

```bash
# Terminal 1 — Test sunucusu
python app.py --test

# Terminal 2 — Yuk testi
pip install aiohttp
python tests/yuk_testi.py
```

Test modu: 40 test ogrencisi (T0001-T0040), ayri DB, kiosk/IP kontrol kapali.

## chroot-yonetici Komutlari

```bash
chroot-yonetici --help         # Yardim
chroot-yonetici --version      # Versiyon
chroot-yonetici init           # Sablon olustur
chroot-yonetici create <user>  # Ogrenci chroot olustur
chroot-yonetici list           # Chroot listele
chroot-yonetici mount <user>   # Mount et
chroot-yonetici delete <user>  # Sil
chroot-yonetici repair         # PTY onar
chroot-yonetici cleanup        # Zombie/stale temizligi
chroot-yonetici health         # Saglik raporu
chroot-yonetici persist        # Systemd servisi kur
```

## Dosya Yapisi

```
ders_takip/
  app.py                    # Flask + SocketIO sunucusu
  chroot_terminal.py        # SSH baglanti yonetimi (semaphore, cache, retry)
  chroot_yonetici.py        # Chroot ortam yonetimi (VM tarafinda calisir)
  requirements.txt          # Python bagimliliklari
  core/
    config.py               # Merkezi ayar yonetimi
    db.py                   # SQLite tablo olusturma ve migration
    paths.py                # Dosya yollari (test/production DB secimi)
    security.py             # Auth decorator'lari
    utils.py                # Yardimci fonksiyonlar
  routes/
    api.py                  # REST API endpoint'leri
    student.py              # Ogrenci giris/panel route'lari
    teacher.py              # Ogretmen panel route'lari
    terminal.py             # Terminal route'lari
    exam.py                 # Sinav route'lari
  templates/
    login.html              # Ogrenci giris formu
    ogrenci_ana.html        # Ogrenci ana panel (mod degisimi)
    ogretmen.html           # Ogretmen kontrol paneli
    ogretmen_giris.html     # Ogretmen giris formu
    ogretmen_terminal.html  # Ogretmen terminal + izleme
    terminal_workspace.html # Ogrenci terminal (xterm.js)
  static/
    css/stil.css            # Dark theme stiller
    js/ogrenci.js           # Ogrenci taraf JS (polling, mod, sinav)
    js/ogretmen.js          # Ogretmen taraf JS (yoklama, rapor, ayar)
  data/
    yoklama.db              # Production veritabani
    test_yoklama.db         # Test veritabani (--test ile)
  tests/
    test_seed.py            # Test DB seed (40 ogrenci)
    yuk_testi.py            # Esanlamli giris yuk testi
  deb-package/
    build.sh                # DEB paketi olusturma scripti
    chroot-terminal_1.1/    # Paket icerigi (sysctl, limits, ssh, systemd)
```

## Sorun Giderme

| Sorun | Cozum |
|-------|-------|
| PTY allocation failed | VM'de: `chroot-yonetici cleanup && chroot-yonetici repair` |
| SSH Connection refused | VM'de: `sudo systemctl start ssh` |
| Disk dolu | VM'de: `sudo growpart /dev/sda 2 && sudo resize2fs /dev/sda2` |
| Sunucu yanitlamiyor | `Ctrl+C` ile durdurup tekrar `python app.py` |
| Eski IP/ayarlar | Ogretmen paneli → Ayarlar tabindan guncelle |

---

*Kapadokya Universitesi — Veri Bilimi ve Analizi*
