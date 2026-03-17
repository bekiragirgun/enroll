# Ogretmen Panel ve Ogrenci Deneyimi Gelistirmeleri

**Tarih:** 2026-03-17
**Proje:** Ders Takip Sistemi - Kapadokya Universitesi

## Ozet

Ogretmen paneline yoklama raporlama, terminal izleme/mudahale ozellikleri; ogrenci tarafina devam goruntuleleme ve kategorili yardim sistemi eklenmesi.

## 1. Yoklama Raporlama (Ogretmen Paneli)

### Amac
Ogretmenin ogrenci bazinda devam durumunu haftalik/aylik gorebilmesi ve devamsizlik uyari sistemi.

### Tasarim

**Yeni tab:** "Devam Raporu" — ogretmen panelindeki tab menusune eklenir.

**API Endpoint'leri:**

- `GET /api/yoklama/rapor` — Parametreler: `sinif_id`, `baslangic_tarih`, `bitis_tarih`, `paket` (opsiyonel)
  - Donus: Ogrenci bazinda tarih matrisi (her tarih icin geldi/gelmedi)
  - Ozet: Toplam ders sayisi, katilim sayisi, devamsizlik sayisi, katilim yuzdesi
  - Uyari: Devamsizlik esik degerini asan ogrenciler isaretlenir

- `GET /api/yoklama/devamsizlik_esik` — Mevcut esik degerini getir (varsayilan: 3)
- `POST /api/yoklama/devamsizlik_esik` — Esik degerini guncelle

**UI Bileenleri:**

- Filtreler: Sinif dropdown, tarih araligi (baslangic/bitis), paket secimi
- Tablo: Satirlar = ogrenciler, sutunlar = tarihler
  - Hucre renkleri: Yesil (geldi), kirmizi (gelmedi), gri (ders yapilmadi)
  - Satir arka plani: Devamsizlik esigini asanlar kirmizi tonla isaretlenir
- Ozet satiri: Her ogrencinin toplam katilim yuzdesi (son sutun)
- CSV export butonu: Filtrelenmis raporu indirir
- Esik ayari: Ayarlar tabinda "Devamsizlik uyari esigi" input'u

**Veri Kaynagi:** Mevcut `yoklama` tablosu + `ogrenciler` tablosu join edilir. Ders yapilan gunler `yoklama` tablosundaki DISTINCT tarihlerden cikarilir.

### Kenar Durumlar
- Ogrenci sinif degistirdiyse: Her iki sinifta da kaydi gorunur
- Paket bazinda filtrelemede: Sadece o paketin dersleri sayilir
- Ders yapilmayan gun: Hic yoklama kaydi yoksa gri gosterilir

---

## 2. Ogrenci Devam Goruntuleleme

### Amac
Ogrencinin giris yaptiktan sonra kendi devam gecmisini ve ozet istatistiklerini gorebilmesi.

### Tasarim

**Konum:** `ogrenci_ana.html` bekleme ekraninda, ogrenci adi altinda.

**API Endpoint'i:**

- `GET /api/ogrenci/devam` — Session'daki `numara` uzerinden calisan ogrencinin devam bilgilerini doner
  - Donus:
    ```json
    {
      "ozet": {
        "toplam_ders": 15,
        "katilim": 12,
        "devamsizlik": 3,
        "yuzde": 80
      },
      "gecmis": [
        {"tarih": "2026-03-17", "paket": "1. Paket", "durum": "geldi"},
        {"tarih": "2026-03-16", "paket": "1. Paket", "durum": "gelmedi"}
      ]
    }
    ```

**UI Bileenleri:**

- Ozet kutusu: Bekleme ekraninda ogrenci adinin altinda
  - "12/15 derse katildiniz (%80)" formatinda
  - Renk: %70 ustu yesil, %50-70 sari, %50 alti kirmizi
- Gecmis tablosu: "Devam Durumum" acilir panel (toggle)
  - Tarih | Paket | Durum (geldi/gelmedi ikonu)
  - Scroll edilebilir, en yeni uste
- Sadece kendi verileri gorunur (session bazli)

### Guvenlik
- Endpoint session kontrolu yapar, numara session'dan alinir (URL'den degil)
- Baska ogrencinin verisine erisim mumkun degil

---

## 3. Kategorili Yardim Sistemi

### Amac
Ogrencinin yardim talebine kategori eklemesi, ogretmenin kategoriye gore filtreleyebilmesi.

### Tasarim

**Kategoriler (sabit liste):**
1. "Komut calismıyor"
2. "Dosya bulamiyorum"
3. "Terminal dondu"
4. "Soru sormak istiyorum"
5. "Diger"

**Veritabani Degisikligi:**
- `yardim_talepleri` tablosuna `kategori TEXT DEFAULT ''` kolonu eklenir

**API Degisiklikleri:**
- `POST /api/yardim_talep` — Yeni parametre: `kategori`
- `GET /api/yardim_talepler` — Donus'e `kategori` alani eklenir

**Ogrenci UI:**
- "Yardim Iste" butonuna basinca modal acilir
- 5 kategori butonu gosterilir (ikon + metin)
- Secim yapinca talep gonderilir, modal kapanir
- Buton "Yardim Bekleniyor..." durumuna gecer

**Ogretmen UI:**
- Yardim talepleri listesinde kategori etiketi/ikonu gosterilir
  - Komut: wrench ikonu
  - Dosya: folder ikonu
  - Terminal: terminal ikonu
  - Soru: soru isareti ikonu
  - Diger: genel ikon
- Kategori bazli filtreleme dropdown'u

---

## 4. Terminal Izleme ve Mudahale

### Amac
Ogretmenin herhangi bir ogrencinin terminalini canli izleyebilmesi ve komut yazabilmesi.

### Tasarim

**Mimari:** Mevcut Socket.IO `/terminal` namespace'i uzerinde calisir. Ogretmenin kendi yayin terminali etkilenmez.

**API/Socket Degisiklikleri:**

- `GET /api/terminal/aktif_oturumlar` — Aktif terminal oturumlarinin listesi
  - Donus: `[{sid, username, ad_soyad, baglanti_suresi}]`

- Socket event: `ogretmen_izle` — Ogretmen bir ogrencinin terminaline baglanir (read-only)
  - Parametre: `{username: "u25901002"}`
  - Sunucu ogrencinin PTY ciktisini ogretmene de yonlendirir

- Socket event: `ogretmen_izle_girdi` — Ogretmen izledigi terminale komut gonderir
  - Parametre: `{username: "u25901002", data: "ls -la\n"}`
  - Sunucu komutu ogrencinin PTY'sine yazar

- Socket event: `ogretmen_izle_birak` — Izlemeyi sonlandirir

**Ogretmen UI:**

- Yeni tab veya ogretmen terminal sayfasinda ek panel: "Ogrenci Terminalleri"
- Aktif oturum listesi (ogrenci adi, sure, durum)
- Bir ogrenciyi tiklayinca: Yeni xterm.js penceresi acilir (izleme modu)
- "Mudahale Et" toggle butonu: Aktiflesince ogretmen yazabilir, deaktiflesince read-only
- Gosterge: Izleme modunda mavi cerceve, mudahale modunda turuncu cerceve

**Sunucu Mantigi (app.py):**

- `ogrenci_surecleri` dict'inden ogrencinin PTY fd'sini bulur
- Izleme: `_pty_oku_ve_yayinla` benzeri bir mekanizma ile ogretmen room'una da emit eder
- Mudahale: Ogrencinin PTY fd'sine `os.write()` ile yazar
- Ayni anda sadece 1 ogrenci izlenebilir (basitlik icin)

### Guvenlik
- Sadece ogretmen session'i ile erisim (ogretmen_giris_gerekli)
- Mudahale loglama: Ogretmenin hangi ogrenciye ne zaman mudahale ettigi loglanir
- Ogrenci tarafi: Ogretmenin izledigini gosterme/gostermeme ayarlanabilir

### Kenar Durumlar
- Ogrenci disconnect olursa: Izleme otomatik sonlanir
- Ogretmen baska ogrenciye gecerse: Onceki izleme birakilir
- Ogretmenin kendi yayin terminali ile cakisma: Ayri socket event'leri, ayri xterm instance

---

## Implementasyon Oncelikleri

| Oncelik | Ozellik | Karmasiklik | Etki |
|---------|---------|-------------|------|
| 1 | Kategorili Yardim | Dusuk | Hemen fayda |
| 2 | Ogrenci Devam Goruntuleleme | Dusuk | Ogrenci memnuniyeti |
| 3 | Yoklama Raporlama | Orta | Ogretmen verimliligi |
| 4 | Terminal Izleme/Mudahale | Yuksek | Ogretim kalitesi |

## Teknik Notlar

- Mevcut `yoklama`, `ogrenciler`, `yardim_talepleri` tablolari kullanilir
- Yeni tablo gerekmez (sadece kolon ekleme: `yardim_talepleri.kategori`)
- Frontend tamamen mevcut stil sistemini kullanir (stil.css dark theme)
- Terminal izleme mevcut Socket.IO altyapisini genisletir
- Tum endpoint'ler mevcut auth mekanizmasini kullanir
