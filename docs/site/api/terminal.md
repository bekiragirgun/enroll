# API Referansi — Terminal

## GET /api/terminal/aktif_oturumlar
Aktif terminal oturumlarini listeler. **Ogretmen yetkisi gerekir.**

**Response:**
```json
{
  "oturumlar": [
    {"sid": "abc123", "username": "t0001", "aktif": true}
  ]
}
```

## GET /api/terminal/durum
Terminal sisteminin genel durumu. **Ogretmen yetkisi gerekir.**

## GET /api/chroot/listele
VM sunucusundaki chroot klasorlerini DB ile karsilastirir. **Ogretmen yetkisi gerekir.**

**Response:**
```json
{
  "toplam": 41,
  "aktif": 38,
  "fazla": ["t0005", "t0009"],
  "fazla_sayisi": 2
}
```

## POST /api/chroot/temizle
DB'de olmayan tum eski chroot'lari siler. **Ogretmen yetkisi gerekir.**

## POST /api/chroot/sil
Secili chroot'lari siler. **Ogretmen yetkisi gerekir.**

**Body:** `{"secili": ["t0005", "t0009"]}`

**Not:** `ogretmen` ve `template` korunur — secilemez.

## SocketIO Olaylari (/terminal namespace)

| Olay | Yon | Aciklama |
|------|-----|----------|
| `ogrenci_baglan` | Client→Server | Ogrenci terminal acma |
| `terminal_girdi` | Client→Server | Klavye girisi |
| `terminal_cikti` | Server→Client | Terminal ciktisi |
| `ogretmen_izle` | Client→Server | Ogretmen izleme baslatma |
| `ogretmen_izle_birak` | Client→Server | Izleme durdurma |
| `ogretmen_izle_girdi` | Client→Server | Mudahale girisi |
| `izleme_cikti` | Server→Client | Izleme ciktisi |
| `ogretmen_mudahale_toggle` | Client→Server | Mudahale ac/kapat |
