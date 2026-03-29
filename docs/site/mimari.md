# Mimari

## Genel Yapi

```
ders_takip/
  app.py                    # Flask + SocketIO sunucusu
  chroot_terminal.py        # SSH baglanti yonetimi (pool, retry, auto-reset)
  chroot_yonetici.py        # Chroot ortam yonetimi (VM tarafinda calisir)
  core/
    config.py               # Merkezi ayar yonetimi + ders_durumu state
    db.py                   # SQLite/PostgreSQL baglanti + saglik kontrolu
    paths.py                # DB yollari (test/production secimi)
    security.py             # Auth + SEB decorator'lari
    state.py                # Paylasimli durum (log buffer, ogrenci sidleri)
    utils.py                # Yardimci fonksiyonlar
  routes/
    api.py                  # REST API endpoint'leri
    student.py              # Ogrenci giris/panel + SEB config/quit
    teacher.py              # Ogretmen panel
    terminal.py             # Terminal route'lari
    exam.py                 # Sinav route'lari
  templates/                # Jinja2 HTML sablonlari
  static/
    css/stil.css            # Dark theme
    js/ogrenci.js           # Ogrenci polling, mod, sinav, cikis
    js/ogretmen.js          # Ogretmen yoklama, rapor, log, VM
  data/
    yoklama.db              # Production SQLite DB
    test_yoklama.db         # Test SQLite DB
    backups/                # Otomatik backup'lar
  deb-package/
    chroot-terminal_1.9/    # DEB paket icerigi
```

## Veri Akisi

### Ogrenci Girisi
1. Ogrenci formu doldurur ve POST yapar
2. `giris_acik` kontrolu (ogretmen acmamissa engellenir)
3. `seb_gerekli` kontrolu (kiosk modunda SEB zorunlu)
4. DB'de ogrenci dogrulanir
5. Yoklama yazilir, session olusturulur
6. Chroot arka planda olusturulur (yoksa)
7. Ogrenci ana sayfaya yonlendirilir

### Polling Dongusu
- `ogrenci.js` her 3 saniyede `/api/durum` ceker
- Mod degisirse ekran guncellenir
- Toplu cikis algilanirsa SEB'de `/seb-quit`, normalde `/` yonlendirilir
- Login sayfasinda `giris_acik` polling'i: acilinca otomatik yenilenir

### SSH Pool
- ControlMaster ile tek SSH baglantisi acik tutulur
- Slave baglantilar bu socket uzerinden ~5ms latency ile calisir
- Hata durumunda pool otomatik sifirlanir ve yeniden olusturulur
- Retry: 3 deneme, exponential backoff (2s, 4s)

## Guvenlik Katmanlari

| Katman | Mekanizma |
|--------|-----------|
| SEB Zorunlulugu | `@seb_gerekli` decorator, UA kontrolu |
| Ogretmen Auth | `@ogretmen_giris_gerekli` decorator |
| IP Kontrol | Ayni IP'den farkli numara engelleme |
| Chroot Izolasyon | Her ogrenci ayri chroot ortami |
| DB Guvenlik | `db_saglikli` flag, test/prod ayirimi |
| Giris Kapisi | `giris_acik` flag, ogretmen kontrolunde |
| Session | Flask session cookie (SameSite=Lax) |

## Veritabani Tablolari

| Tablo | Aciklama |
|-------|----------|
| `ogrenciler` | Ogrenci listesi (numara, ad, soyad, sinif_id) |
| `siniflar` | Sinif tanimlari |
| `yoklama` | Gunluk yoklama kayitlari |
| `sinavlar` | Sinav tanimlari |
| `sorular` | Sinav sorulari |
| `secenekler` | Soru secenekleri |
| `ogrenci_cevaplari` | Sinav cevaplari |
| `ayarlar` | Anahtar-deger sistem ayarlari |
| `sahte_giris_log` | IP fraud tespiti |
| `seb_cikis_log` | SEB kapanma kayitlari |
| `seb_cikis_talepleri` | Ogrenci cikis talepleri |
| `ogrenci_cikis_log` | Ogrenci cikis kayitlari |
| `yardim_talepleri` | Yardim istekleri |
| `terminal_guvenlik_log` | Terminal guvenlik olaylari |
