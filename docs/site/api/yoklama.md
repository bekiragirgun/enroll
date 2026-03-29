# API Referansi — Yoklama

## GET /api/yoklama
Yoklama kayitlarini listeler. **Ogretmen yetkisi gerekir.**

**Parametreler:** `?tarih=2026-03-29&paket=1.+Paket+(09:00-11:35)`

## GET /api/yoklama/devam_raporu
Ogrenci bazinda devam raporu matrisi. **Ogretmen yetkisi gerekir.**

**Parametreler:** `?sinif_id=1&baslangic=2026-03-01&bitis=2026-03-31&paket=...`

**Not:** Sadece ayarlardaki ders gunleri sayilir (varsayilan: Pazartesi).

## GET /api/ogrenci/devam
Ogrencinin kendi devam durumu. **Ogrenci session gerekir.**

## POST /api/yoklama/duzenle
Ogretmen yoklama duzeltmesi. **Ogretmen yetkisi gerekir.**

**Body:** `{"numara": "12345", "tarih": "2026-03-29", "durum": "geldi", "paket": "1. Paket"}`

## GET /api/yoklama/devamsizlik_esik
Devamsizlik uyari esigini dondurur.

## POST /api/yoklama/devamsizlik_esik
Devamsizlik esigini gunceller. **Body:** `{"esik": 3}`

## GET /api/ogrenci_listesi/:sinif_id
Sinifa ait ogrenci listesi (giris formundaki dropdown icin).

## POST /api/ogrenci_cikis
Ogrenci cikis yapar (paket saati kontrolu, test modunda atlanir).

## POST /api/ogrenci_force_cikis
Ogretmen tek ogrenciyi zorla cikartir. **Body:** `{"numara": "12345"}`

## GET /api/ogrenci_cikis_log
Ogrenci cikis kayitlarini listeler. **Ogretmen yetkisi gerekir.**
