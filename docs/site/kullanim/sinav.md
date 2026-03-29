# Sinav Modulu

## Sinav Olusturma

Ogretmen paneli → **Sinav** sekmesi:

1. Sinav basligi girin
2. Sorulari ekleyin (coktan secmeli)
3. Her soru icin secenekler ve dogru cevap belirleyin

## Sinav Baslatma

Sinav listesinde **"Baslat"** butonuna basin.

Dialog kutusu acilir:

- **Terminal acik kalsin** checkbox'i: Isaretlerseniz ogrenci split screen gorur
  (sol: sinav sorulari, sag: Linux terminali)
- **Baslat**: Sinav tum ogrencilerde otomatik acilir

## Sinav Modlari

### Normal Sinav
Tam ekran sinav sorulari. Ogrenci cevaplari secip "Cevaplari Gonder" der.

### Terminalli Sinav (Split Screen)
```
+------------------+------------------+
|                  |                  |
|  Sinav Sorulari  |  Linux Terminal  |
|                  |                  |
|  1. Hangi komut  |  $ ls -la       |
|     ...          |  $ grep ...     |
|                  |                  |
|  [Cevaplari      |                  |
|   Gonder]        |                  |
+------------------+------------------+
```

Ogrenci terminalde komut calistirirken sorulari cevaplayabilir.

## Sinav Bitimi

- Ogrenci cevaplari gonderdikten sonra "Sinav Tamamlandi" mesaji gorur
- SEB icerisindeyse **"Sinavi Bitir ve Cik"** butonu otomatik gorulur
  (`cikis_izni` ayarindan bagimsiz)
- Ogretmen sinavi **"Yayindan Kaldir"** ile bitirir

## Puanlama

Otomatik puanlama: dogru cevap sayisi / toplam soru sayisi
Sonuclar ogretmen panelinde gorulur.
