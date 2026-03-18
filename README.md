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
- **Force Cikis** — Tek ogrenciyi terminal panelinden zorla cikartma
- **IP Kontrol** — Ayni IP'den farkli ogrenci girisini engelleme (acilip kapatilabilir)
- **SEB Entegrasyonu** — Safe Exam Browser zorunlulugu ve cikis yonetimi
- **Sistem Loglari** — Canli log goruntuleyici (incremental polling, seviye filtresi)
- **VM Temizligi** — Eski/artik chroot klasorlerini tara ve secili olarak sil
- **Ogrenci Cikis Logu** — Tum cikis olaylarini takip etme (ogrenci/ogretmen/toplu)

### Ogrenci Tarafi
- **Yoklama Girisi** — Sinif, ad soyad ve ogrenci numarasi ile giris
- **Devam Durumu** — Kendi devam gecmisini ve katilim yuzdesini gorme
- **Izole Terminal** — Chroot tabanli, tamamen izole Linux ortami
- **Sinav** — Coktan secmeli sinav cevaplama
- **Yardim Talebi** — Kategorili yardim isteme
- **Cikis Yap** — Paket saatleri icinde oturum kapatma (ogretmen kontrolunde)
- **SEB Cikis** — SEB icerisinden cikis talep etme veya dogrudan cikma

### Altyapi
- **Chroot Izolasyon** — Her ogrenci icin ayri chroot ortami (debootstrap tabanli)
- **DEB Paketi (v1.5)** — VM tarafini tek komutla kuran `chroot-terminal` paketi
- **PTY Stabilite** — ptmxmode=666, boot'ta PTY onarimi (SSH'den once)
- **LXC Boot Optimizasyonu** — Gereksiz servisler mask'lenir, timeout 10s
- **SSH Connection Pool** — ControlMaster ile hizli baglantilar, otomatik pool reset
- **Kernel Optimizasyonu** — PTY, fd, TCP, ulimit ayarlari (deb ile otomatik)
- **Yuk Testi** — 40 esanlamli ogrenci giris simulasyonu

## Mimari

```
[Ogretmen Mac/PC]                    [Ogrenci Tarayici/SEB]
        |                                    |
        v                                    v
+------------------+              +------------------+
|  Flask + SocketIO |<--- HTTP -->|  Polling (3s)    |
|  (app.py :3333)   |             |  ogrenci.js      |
+------------------+              +------------------+
        |
        | SSH (ControlMaster pool)
        v
+------------------+
|  Ubuntu VM (LXC) |
|  (chroot-terminal|
|   deb v1.5)      |
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
sudo apt install ./chroot-terminal_1.5.deb

# Chroot sablonunu olustur (ilk sefer, ~10dk)
sudo chroot-yonetici init

# Kontrol
chroot-yonetici health
```

DEB paketi v1.5 otomatik olarak su ayarlari yapar:
- LXC boot optimizasyonu (udevd, multipathd, resolved mask'lenir)
- Systemd timeout'lari 10s (boot hizlandirma)
- Kernel optimizasyonu (PTY 16384, fd 262144, TCP, ulimit)
- SSH optimizasyonu (MaxSessions 80, keepalive, no compression)
- PTY onarimi servisi (SSH'den once calisir, ptmxmode=666)
- 10dk'da bir temizleme timer'i
- NTP senkronizasyonu (Europe/Istanbul)

### 3. Ayarlar (Ogretmen Paneli)

Ogretmen panelindeki Ayarlar tabindan:
- **Sistem IP / Hostname**: Ogrencilerin eristigi adres (orn: `http://10.211.55.2:3333`)
- **Chroot Host**: VM IP adresi
- **Chroot Port**: SSH portu (varsayilan: 22)
- **Chroot User/Pass**: SSH kullanicisi ve sifresi
- **Kiosk Modu (SEB)**: SEB zorunlulugu acma/kapama
- **SEB Cikis Izni**: Ogrenci cikis butonunu gosterme/gizleme
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
- **Guvenlik Log** tabindan SEB cikis talepleri ve ogrenci cikis loglarini izleme
- **Sistem Loglari** tabindan canli uygulama loglarini izleme
- **Ayarlar > VM Temizligi** ile eski chroot klasorlerini tara ve sec/sil

### Ogrenci

```
http://sunucu-ip:3333
```

1. Sinif sec → Ad soyad sec → Ogrenci numarasi gir → Paket sec
2. "Derse Katil" butonu ile tam ekrana gec
3. Ogretmen mod degistirdikce slayt/terminal/sinav otomatik yuklenir

### SEB (Safe Exam Browser) Akisi

1. Ogretmen panelinden **Kiosk Modu: Acik** yap
2. Ogrenci normal tarayicidan sisteme girince `/seb-gerekli` sayfasina yonlendirilir
3. Sayfadan SEB indirilir, kurulur, `.seb` config dosyasi indirilip acilir
4. SEB otomatik olarak sisteme baglanir (startURL config'den alinir)
5. Ogretmen **SEB Cikis Izni** ile cikis butonlarini kontrol eder
6. Ogrenci cikisi: "Cikis Yap" butonu → `/seb-quit` → SEB kapanir
7. Ogretmen kiosk modunu kapatinca ogrenci sayfasi 3sn icinde otomatik yonlenir

## Test Modu

Production DB'ye dokunmadan test:

```bash
# Terminal 1 — Test sunucusu (paket saatleri kontrol edilmez)
python app.py --test

# Terminal 2 — Yuk testi
pip install aiohttp
python tests/yuk_testi.py
```

Test modu: 40 test ogrencisi (T0001-T0040), ayri DB, paket saati kontrolu devre disi.

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
  chroot_terminal.py        # SSH baglanti yonetimi (pool, semaphore, retry, auto-reset)
  chroot_yonetici.py        # Chroot ortam yonetimi (VM tarafinda calisir)
  requirements.txt          # Python bagimliliklari
  core/
    config.py               # Merkezi ayar yonetimi
    db.py                   # SQLite tablo olusturma ve migration
    paths.py                # Dosya yollari (test/production DB secimi)
    security.py             # Auth + SEB decorator'lari (UA loglama)
    state.py                # Paylasimli durum (log buffer, ogrenci sidleri)
    utils.py                # Yardimci fonksiyonlar (paket saati, IP tespiti)
  routes/
    api.py                  # REST API endpoint'leri
    student.py              # Ogrenci giris/panel + SEB config/quit route'lari
    teacher.py              # Ogretmen panel route'lari
    terminal.py             # Terminal route'lari
    exam.py                 # Sinav route'lari
  templates/
    login.html              # Ogrenci giris formu
    ogrenci_ana.html        # Ogrenci ana panel (mod degisimi, cikis modali)
    ogretmen.html           # Ogretmen kontrol paneli (loglar, VM temizligi)
    ogretmen_giris.html     # Ogretmen giris formu
    ogretmen_terminal.html  # Ogretmen terminal + izleme + force cikis
    terminal_workspace.html # Ogrenci terminal (xterm.js)
    seb_gerekli.html        # SEB indirme/kurulum sayfasi + cikis butonlari
  static/
    css/stil.css            # Dark theme stiller
    js/ogrenci.js           # Ogrenci taraf JS (polling, mod, sinav, cikis)
    js/ogretmen.js          # Ogretmen taraf JS (yoklama, rapor, log, VM temizligi)
  data/
    yoklama.db              # Production veritabani
    test_yoklama.db         # Test veritabani (--test ile)
  tests/
    test_seed.py            # Test DB seed (40 ogrenci)
    yuk_testi.py            # Esanlamli giris yuk testi
  deb-package/
    build.sh                # DEB paketi olusturma scripti
    chroot-terminal_1.5/    # v1.5 paket icerigi (LXC opt, PTY fix, SSH)
```

## Sorun Giderme

| Sorun | Cozum |
|-------|-------|
| PTY allocation failed | VM'de: `chroot-yonetici cleanup && chroot-yonetici repair` |
| SSH Connection refused | VM'de: `sudo systemctl restart sshd` |
| SSH pool stale | Otomatik: pool reset + retry. Manuel: `rm /tmp/ssh_pool_*` |
| sudo-rs PTY hatasi | `echo SIFRE \| sudo -S mount -t devpts devpts /dev/pts` |
| Boot cok yavas (LXC) | `sudo apt install ./chroot-terminal_1.5.deb` (servisleri mask'ler) |
| SEB baglanmiyor | `.seb` dosyasini tekrar indirin (system_host + port kontrolu) |
| SEB cikis calismiyor | `/seb-quit` route'u mevcut, SEB config'de quitURL kontrol edin |
| Disk dolu | VM'de: `sudo growpart /dev/sda 2 && sudo resize2fs /dev/sda2` |
| Sunucu yanitlamiyor | `Ctrl+C` ile durdurup tekrar `python app.py` |
| Eski IP/ayarlar | Ogretmen paneli → Ayarlar tabindan guncelle |

---

*Kapadokya Universitesi — Veri Bilimi ve Analizi*
