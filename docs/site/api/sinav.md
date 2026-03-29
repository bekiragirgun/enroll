# API Referansi — Sinav

Tum sinav endpoint'leri `/api/sinav/` prefix'i altindadir.

## GET /api/sinav/listele
Tum sinavlari listeler. **Ogretmen yetkisi gerekir.**

## POST /api/sinav/olustur
Yeni sinav olusturur. **Ogretmen yetkisi gerekir.**

**Body:** `{"baslik": "Linux Temelleri Quiz 1"}`

## POST /api/sinav/aktiflestir
Sinavi baslatir veya durdurur. **Ogretmen yetkisi gerekir.**

**Body:** `{"sinav_id": 1, "aktif": true, "sinav_terminal": true}`

`sinav_terminal: true` ile ogrenci split screen gorur (sol sinav, sag terminal).

## GET /api/sinav/aktif
Aktif sinavi ve sorularini dondurur (ogrenci icin).

## POST /api/sinav/soru_ekle
Sinava soru ekler. **Ogretmen yetkisi gerekir.**

## POST /api/sinav/cevap_kaydet
Ogrenci cevaplarini kaydeder.

**Body:**
```json
{
  "sinav_id": 1,
  "cevaplar": [
    {"soru_id": 1, "secenek_id": 3},
    {"soru_id": 2, "secenek_id": 7}
  ]
}
```

## GET /api/sinav/sonuclar/:sinav_id
Sinav sonuclarini listeler. **Ogretmen yetkisi gerekir.**
