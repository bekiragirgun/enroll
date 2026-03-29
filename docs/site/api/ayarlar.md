# API Referansi — Ayarlar ve Guvenlik

## POST /api/config
Sistem ayarlarini gunceller. **Ogretmen yetkisi gerekir.**

**Body:**
```json
{
  "chroot_host": "10.211.55.27",
  "chroot_port": "22",
  "chroot_user": "bekir",
  "chroot_pass": "sifre",
  "system_host": "http://10.211.55.2:3333",
  "ttyd_url": "/terminal",
  "kiosk_modu": "1",
  "ip_kontrol": "0",
  "cikis_izni": "1",
  "ders_gunleri": "1"
}
```

**Ders gunleri kodlari:** 0=Pzr, 1=Pzt, 2=Sal, 3=Car, 4=Per, 5=Cum, 6=Cmt

## SEB Endpoint'leri

### POST /api/seb_cikis
SEB kapandiginda beacon ile cikis loglama.

### POST /api/seb_cikis_talep
Ogrenci SEB cikis talebi olusturur.

### GET /api/seb_cikis_talepler
Bekleyen cikis taleplerini listeler. **Ogretmen yetkisi gerekir.**

### POST /api/seb_cikis_onayla
Talebi onaylar/reddeder. **Ogretmen yetkisi gerekir.**

**Body:** `{"id": 5, "durum": "onaylandi|reddedildi"}`

### POST /api/seb_cikis_toplu_onayla
Tum bekleyen talepleri toplu onaylar. **Ogretmen yetkisi gerekir.**

### GET /api/seb_cikis_log
SEB cikis/kapanma loglarini listeler. **Ogretmen yetkisi gerekir.**

## Guvenlik Endpoint'leri

### GET /api/sahte_girisler
Sahte giris tespit loglarini listeler. **Ogretmen yetkisi gerekir.**

### GET /api/yardim_talepler
Ogrenci yardim taleplerini listeler.

### POST /api/yardim_kabul
Yardim talebini onaylar/reddeder. **Ogretmen yetkisi gerekir.**

## SEB Config

### GET /seb-config
`.seb` dosyasini indirir (XML plist). Auth gerektirmez.

### GET /seb-quit
SEB quit URL — SEB bu sayfaya navigate edince kendini kapatir.

### GET /seb-gerekli
SEB zorunluluk sayfasi (indirme linkleri, kurulum rehberi).
