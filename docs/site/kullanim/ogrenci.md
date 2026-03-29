# Ogrenci Tarafi

## Giris

```
http://SUNUCU_IP:3333
```

1. Sinif secin
2. Ad soyad secin (dropdown)
3. Ogrenci numaranizi girin
4. Ders paketini secin
5. "Derse Katil" butonuna basin

!!! note "Giris Kapali"
    Ogretmen dersi baslatana kadar giris formu devre disi olur.
    "Giris henuz acilmadi" mesaji gorulur. Sayfa otomatik yenilenir.

## Ders Modlari

Ogretmen mod degistirdikce ekran otomatik degisir:

| Mod | Aciklama |
|-----|----------|
| Bekleme | Ogretmen girisini bekleyin |
| Slayt | Ders slaytlari goruntulenir |
| Terminal | Linux terminali acilir (izole chroot) |
| Sinav | Sinav sorulari goruntulenir |

## Cikis

- **Cikis Yap**: Paket saatleri icinde kullanilabilir
- **SEB Cikis Talep**: SEB icerisindeyken ogretmen onayi gerekir
- **Sinav sonrasi**: "Sinavi Bitir ve Cik" butonu otomatik gorulur

## Terminal

Her ogrenci izole bir Linux (chroot) ortaminda calisir:

- Kendi home dizininiz (`/home/kullanici_adi/`)
- Root yetkisi (chroot icinde)
- Diger ogrencilerin dosyalarina erisim yok
- Ogretmen terminalinizi izleyebilir ve mudahale edebilir

## Yardim

Ders sirasinda "Yardim Iste" butonuyla kategori secin:
- Komut Yardimi
- Dosya Sorunu
- Terminal Sorunu
- Sorum Var
- Diger
