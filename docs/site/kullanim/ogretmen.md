# Ogretmen Paneli

## Giris

```
http://localhost:3333/teacher
```

Test modunda sifre: `1234`
Production'da: `.env`'de tanimli

## Ders Akisi

### 1. Giris Ac

Ders baslamadan once **"Giris Ac"** butonuna basin. Bu butona basana kadar ogrenciler giris yapamaz.

### 2. Mod Secimi

| Buton | Mod | Aciklama |
|-------|-----|----------|
| Beklet | `bekleme` | Ogrenci bekleme ekraninda |
| Slayt | `slayt` | Slayt yayini baslat |
| Terminal | `terminal` | Terminal modu ac |

### 3. Ders Sonu

- **Toplu Cikis**: Tum ogrenci oturumlarini kapatir (giris de otomatik kapanir)
- **Paket Sonu**: Toplu cikis + chroot VM'lerini siler (disk kazanimi)

!!! info "Paket Sonu DB'ye dokunmaz"
    Yoklama kayitlari, ogrenci listeleri ve sinav sonuclari korunur.
    Sadece chroot dosya sistemi silinir.

## Sekmeler

### Yoklama
- Canli katilim listesi (paket ve tarih filtreli)
- CSV export

### Devam Raporu
- Ogrenci bazinda haftalik/aylik devam matrisi
- Devamsizlik uyari esigi (ayarlanabilir)
- Sadece ders gunleri sayilir (test gunleri haric)

### Terminal Izleme
`http://localhost:3333/teacher/terminal`

- Aktif oturumlar listesi
- Ogrenci terminalini canli izleme
- Mudahale (ogretmen yazabilir)
- Zorla cikis butonu (ogrenci yaninda)

### Sinav
- Sinav olustur / duzenle
- Sinavi baslat (terminal acik secenegi ile)
- Otomatik puanlama
- Sinav sonuclari

### Guvenlik Log
- SEB cikis talepleri (onayla/reddet)
- Ogrenci cikis logu
- Sahte giris tespit logu

### Sistem Loglari
- Canli log goruntuleyici (seviye filtresi)
- Incremental polling (sadece yeni loglar)

### Ayarlar
- Chroot sunucu baglantisi (IP, port, user, pass)
- Sistem IP / Hostname
- Kiosk Modu (SEB zorunlulugu)
- SEB Cikis Izni
- IP Kontrol (sahte giris engelleme)
- Ders Gunleri (Pzt-Pzr checkboxlari)
- Devamsizlik esigi
- VM Temizligi (tara + secili sil)
