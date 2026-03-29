# API Referansi — Genel

Tum API endpoint'leri `/api/` prefix'i altindadir.

## Kimlik Dogrulama

- Ogrenci endpoint'leri: Flask session (cookie)
- Ogretmen endpoint'leri: `@ogretmen_giris_gerekli` decorator
- SEB kontrollu endpoint'ler: `@seb_gerekli` decorator

## Ortak Endpoint'ler

### GET /api/durum
Sistem durumunu dondurur. Ogrenci polling'i bu endpoint'i kullanir.

**Response:**
```json
{
  "mod": "bekleme|slayt|terminal|sinav",
  "dosya": "slayt_adi.html",
  "terminal_url": "/terminal",
  "cikis_onaylandi": false,
  "toplu_cikis": false,
  "cikis_izni": true,
  "kiosk_modu": true,
  "sinav_terminal": false,
  "db_saglikli": true,
  "giris_acik": false
}
```

### POST /api/giris_toggle
Ogrenci girisini ac/kapat. **Ogretmen yetkisi gerekir.**

**Body:** `{"acik": true}`
**Response:** `{"durum": "ok", "giris_acik": true}`

### GET /api/config
Sistem ayarlarini dondurur. **Ogretmen yetkisi gerekir.**

### POST /api/config
Sistem ayarlarini gunceller. **Ogretmen yetkisi gerekir.**

### POST /api/healthcheck
Chroot sunucusu SSH baglanti testi. **Ogretmen yetkisi gerekir.**

### POST /api/toplu_cikis
Tum ogrenci oturumlarini kapatir. **Ogretmen yetkisi gerekir.**

### POST /api/paket_sonu
Toplu cikis + chroot VM'lerini siler. **Ogretmen yetkisi gerekir.**

### GET /api/loglar
Sistem loglarini dondurur. `?limit=200&since=TIMESTAMP` parametreleri desteklenir.
