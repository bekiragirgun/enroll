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
- **Chroot Izolasyon** — Her ogrenci icin ayri chroot ortami (mmdebstrap tabanli)
- **DEB Paketi (v1.16.7)** — VM tarafini tek komutla kuran `chroot-terminal` paketi
- **Template Cache (V26)** — /var/cache/chroot-terminal/template.tar.zst (~388 MB zstd) — snapshot revert sonrasi init 10 dk yerine ~1.3 saniyede tamamlanir
- **devpts Private Propagation (V27)** — host <-> chroot mount bulasmasi kesilir; "PTY allocation request failed" regresyonu biter
- **TR Locale (V28)** — Chroot isletim sistemi tamamen Turkce: tr_TR.UTF-8, Europe/Istanbul, manpages-tr, PAGER=less, LESS="-R -M -i --mouse"
- **PTY Stabilite** — ptmxmode=666, boot'ta PTY onarimi (SSH'den once)
- **LXC Boot Optimizasyonu** — Gereksiz servisler mask'lenir, timeout 10s
- **SSH Multiplexing** — ControlMaster auto, 10 dk persist, chacha20-poly1305 cipher; 1. baglanti ~280ms, sonrakiler ~15-22ms (22x speedup 30 ogrenci icin)
- **Kernel Optimizasyonu** — PTY, fd, TCP, ulimit ayarlari (deb ile otomatik)
- **Yuk Testi** — 40 esanlamli ogrenci giris simulasyonu

## Mimari

```
[Ogretmen Mac/PC baremetal]          [Ogrenci Tarayici/SEB]
        |                                    |
        v                                    v
+--------------------------+      +------------------+
|  Flask + SocketIO        |<-----|  Polling (3s)    |
|  (manage.sh / :3333)     |      |  ogrenci.js      |
|  + Docker PostgreSQL     |      +------------------+
|    (127.0.0.1:5432)      |
+--------------------------+
        |
        | SSH (ControlMaster multiplexed, ~15ms)
        v
+---------------------------------+
|  Parallels Debian 12 VM         |
|  (chroot-terminal deb v1.16.7)  |
|  - /home/chroot/template        |  <-- tr_TR.UTF-8
|  - /var/cache/.../template.tar.zst (388 MB zstd cache)
|  - /home/chroot/u25901002       |  <-- rsync from template
|  - /home/chroot/u25901003       |
|  - ... (devpts private, TR locale)
+---------------------------------+
```

Baremetal Flask + Docker-yalnizca-PostgreSQL konfigurasyonu (derste weak-network ogrencilerin NAT latency sorunlarini azaltmak icin Nisan 2026'da Docker-app'ten tasindi).

## Kurulum

### 1. Ana Sunucu (Flask baremetal)

```bash
# Python ortami (iki secenek, manage.sh ikisini de destekler)
# Opsiyon A: local venv
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Opsiyon B: conda
conda create -n kapadokya-DT python=3.11 -y
conda activate kapadokya-DT
pip install -r requirements.txt

# PostgreSQL (Docker'da tutuluyor)
docker compose up -d db   # db container'i 127.0.0.1:5432'de dinler

# Flask'i baremetal baslat (docker disinda)
nohup bash manage.sh > logs/app.log 2>&1 &

# Logu izle
tail -f logs/app.log
```

`.env` icin minimum config:
```ini
SECRET_KEY=<guvenli-string>
CHROOT_HOST=10.211.55.27        # Parallels VM IP
CHROOT_USER=bekir
CHROOT_PASS=<sifre>
DB_TYPE=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres_pass
DB_NAME=ders_takip
SLIDE_HOST_BASE=/path/to/slaytlar
```

### 2. Ogrenci VM (Chroot Sunucusu)

```bash
# DEB paketi kur
sudo dpkg -i chroot-terminal_1.16.7.deb
sudo apt-get install -f  # eksik depends varsa

# Chroot sablonunu olustur
sudo chroot-yonetici init
# Ilk sefer: ~10dk (mmdebstrap + apt-get)
# Sonraki: ~1.3s (template.tar.zst cache'inden restore)

# Kontrol
chroot-yonetici health
```

DEB paketi v1.16.7 otomatik olarak su ayarlari yapar:
- LXC boot optimizasyonu (udevd, multipathd, resolved mask'lenir)
- Systemd timeout'lari 10s (boot hizlandirma)
- Kernel optimizasyonu (PTY 16384, fd 262144, TCP, ulimit)
- SSH optimizasyonu (MaxSessions 80, keepalive, no compression)
- PTY onarimi servisi (SSH'den once calisir, ptmxmode=666, devpts private)
- 10dk'da bir temizleme timer'i
- NTP senkronizasyonu (Europe/Istanbul)
- TR locale: tr_TR.UTF-8 + manpages-tr + Europe/Istanbul timezone

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
    build.sh                    # DEB paketi olusturma scripti
    chroot-terminal_1.16.7/     # v1.16.7 paket icerigi (V28 TR locale)
```

## Sorun Giderme

| Sorun | Cozum |
|-------|-------|
| PTY allocation failed | VM'de: `chroot-yonetici cleanup && chroot-yonetici repair` (V27 host devpts'yi --make-private yapar) |
| Tum chroot'larin mount'u kopmus | `for u in $(ls /home/chroot \| grep -v template); do sudo chroot-yonetici mount $u; done` |
| SSH Connection refused | VM'de: `sudo systemctl restart sshd` |
| CSRF token expired | `WTF_CSRF_TIME_LIMIT = None` (app.py'de set). Ogrenci sayfayi F5 yapip yeni token alsin. |
| Chroot'ta LANG=C / Ingilizce | `chroot-yonetici mount <user>` — `_apply_tr_locale` idempotent (V28) |
| info / pager calismiyor | V28'de manpages-tr + PAGER=less + LESS="-R -M -i --mouse" — fresh chroot'larda hazir |
| Template init 10 dk suruyor | Ilk seferden sonra /var/cache/chroot-terminal/template.tar.zst olusur, sonrakiler ~1.3s |
| Snapshot revert sonrasi | V26 cache olduysa init saniyeler icinde tamamlanir; yoksa full rebuild |
| Paket Sonu 0 ogrenci buluyor | `yoklama.paket` bos kalmis olabilir (UTC timezone bug, V-dan once). TR timezone fix artik hazir |
| SEB baglanmiyor | `.seb` dosyasini tekrar indirin (system_host + port kontrolu) |
| SEB cikis calismiyor | `/seb-quit` route'u mevcut, SEB config'de quitURL kontrol edin |
| Disk dolu | VM'de: `sudo growpart /dev/sda 2 && sudo resize2fs /dev/sda2` |
| Flask sunucu yanitlamiyor | `pkill -f manage.sh && nohup bash manage.sh > logs/app.log 2>&1 &` |
| Eski IP/ayarlar | Ogretmen paneli → Ayarlar tabindan guncelle |

---

*Kapadokya Universitesi — Veri Bilimi ve Analizi*
