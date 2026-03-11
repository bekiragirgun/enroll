---
marp: true
theme: default
paginate: true
lang: tr
backgroundColor: #F7F7F7
footer: "KAPADOKYA ÜNİVERSİTESİ - Linux Temel Eğitimi"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Trebuchet+MS:wght@400;700&display=swap');

  section {
    font-family: 'Trebuchet MS', Arial, sans-serif;
    font-size: 90%;
    padding: 30px 50px;
    background-image: url('../gorseller/3_normal_slayt.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  /* Kapadokya arka planı üzerine hafif beyaz overlay - yazılar net okunabilir */
  section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(247, 247, 247, 0.92);
    z-index: 0;
  }

  /* İçeriği overlay'in üzerine getir */
  section > * {
    position: relative;
    z-index: 1;
  }

  h1 {
    color: #2D4A7C;
    font-size: 26pt;
    font-weight: bold;
    margin-bottom: 20px;
    border-bottom: 3px solid #6B9FE8;
    padding-bottom: 10px;
  }

  h2 {
    color: #2D4A7C;
    font-size: 18pt;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 15px;
    border-bottom: 2px solid #6B9FE8;
    padding-bottom: 8px;
  }

  h3 {
    color: #2D4A7C;
    font-size: 15pt;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 10px;
  }

  p, li {
    font-size: 13pt;
    line-height: 1.6;
    color: #333;
  }

  ul, ol {
    margin-left: 20px;
    max-height: 500px;
    overflow: hidden;
  }

  strong {
    color: #2D4A7C;
    font-weight: bold;
  }

  code {
    background-color: #1a1a1a;
    color: #e0e0e0;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12pt;
  }

  pre {
    background-color: #1a1a1a;
    color: #e0e0e0;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    overflow: hidden;
    overflow: hidden;
    max-height: 400px;
  }

  pre code {
    background: none;
    padding: 0;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12pt;
    line-height: 1.5;
  }

  .highlight-box {
    background-color: #6B9FE8;
    color: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 3px solid #4A90E2;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
    margin-top: 15px;
  }

  .highlight-box h1,
  .highlight-box h2,
  .highlight-box h3,
  .highlight-box p,
  .highlight-box strong,
  .highlight-box li {
    color: white !important;
  }

  /* 1. SLAYT: Ders Başlığı */
  section.cover-slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
    padding-left: 80px;
    background: linear-gradient(135deg, #F7F7F7 0%, #E6EAF3 100%);
    position: relative;
  }

  section.cover-slide h1 {
    color: white;
    font-size: 38pt;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    border-bottom: none;
  }

  section.cover-slide p {
    position: absolute;
    bottom: 40px;
    right: 60px;
    color: white;
    font-size: 20pt;
    font-weight: normal;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
  }

  /* 2. SLAYT: Haftalık Konu */
  section.topic-slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
  }

  section.topic-slide h1 {
    color: white;
    font-size: 38pt;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    border-bottom: none;
    margin: 0;
  }

  section.topic-slide p {
    position: absolute;
    bottom: 40px;
    right: 60px;
    color: white;
    font-size: 20pt;
    font-weight: normal;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
  }

  /* SON SLAYT: Kapanış */
  section.final-slide {
    background-color: #2D4A7C !important;
    color: white !important;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    position: relative;
  }

  section.final-slide::before {
    background-color: transparent !important;
  }

  section.final-slide::after {
    content: '';
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 150px;
    height: 75px;
    background-image: url('../gorseller/1_ana_slayt.png');
    background-size: contain;
    background-repeat: no-repeat;
    filter: brightness(0) invert(1);
    z-index: 10;
  }

  section.final-slide h1,
  section.final-slide h2,
  section.final-slide h3,
  section.final-slide p,
  section.final-slide strong,
  section.final-slide li,
  section.final-slide div,
  section.final-slide a {
    color: white !important;
    border-bottom-color: white !important;
  }

  img {
    max-width: 95%;
    max-height: 500px;
    object-fit: contain;
    margin: 10px auto;
    display: block;
  }

  /* Footer Bar Styling */
  footer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #2D4A7C;
    color: white;
    padding: 5px 20px;
    font-size: 12pt;
    font-weight: normal;
    border-top: 2px solid #6B9FE8;
    z-index: 5;
    display: flex;
    justify-content: space-between;
    align-items: center;
    line-height: 1.2;
  }

  /* Hide footer on cover and topic slides */
  section.cover-slide footer,
  section.topic-slide footer {
    display: none;
  }

  /* Adjust padding for slides with footer */
  section:not(.cover-slide):not(.topic-slide) {
    padding-bottom: 50px;
  }

  /* Fix syntax highlighting colors for better readability */
  pre code span.hljs-string,
  pre code span.hljs-literal,
  pre code span.hljs-attr {
    color: #f07d12;
  }
---

<!-- 1. SLAYT: DERS BAŞLIĞI -->
<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Linux Dosya, Dizin ve Metin İşlemleri

Dr. Bekir Ağırgün

---

<!-- 2. SLAYT: HAFTALIK KONU -->
<!-- _class: topic-slide -->
<!-- _paginate: false -->

![bg](../gorseller/2_Konu_baslik.png)

# Bölüm 8, 9, 10 - Kapsamlı Eğitim

Dr. Bekir Ağırgün

---

# 📚 İçerik Planı

- **Bölüm 8:** Dosya ve Dizinleri Yönetme (25 slayt)
- **Bölüm 9:** Arşivleme ve Sıkıştırma (20 slayt)
- **Bölüm 10:** Metin ile Çalışma (25 slayt)

**Toplam:** 70 slayt

---

<!-- _class: topic-slide -->
<!-- _paginate: false -->

![bg](../gorseller/2_Konu_baslik.png)

# Dosya Yönetimi Komutları

---

## Dosya Yönetimi Komutları - Diyagram

![width:900px height:400px](gorseller/file_management_diagram.svg)

---

## 📌 Bölüm 8 Özeti

Bu bölümde **dosya ve dizinleri etkili bir şekilde yönetmeyi** öğreneceksiniz:

- **Globbing (Wildcard):** `*`, `?`, `[ ]`, `[!]` karakterleri ile dosya seçme
- **Dosya Kopyalama:** `cp` ve `cp -r` komutları
- **Dosya Taşıma/Yeniden Adlandırma:** `mv` komutu
- **Dosya/Dizin Silme:** `rm`, `rmdir` komutları
- **Dosya Oluşturma:** `touch` komutu
- **Dizin Oluşturma:** `mkdir` komutu

Bu komutları doğru kullanmak, Linux'te verilerinizi güvenli ve organize şekilde yönetmek için çok önemlidir.

---

## 8.1 Giriş ve Case Sensitivity

- Linux'te **her şey büyük/küçük harf duyarlı**
- `hello.txt` ≠ `Hello.txt` ≠ `HELLO.txt`
- Dosya ve komutlarla çalışırken dikkat gerekli
- UTF-8 karakter standartı kullanılır

---

## 8.2 Globbing (Wildcard) - Giriş

**Glob karakterleri** = özel anlamı olan semboller

- Shell tarafından yorumlanır
- Komut çalışmadan önce genişletilir
- Tüm komutlarla kullanılabilir

```bash
echo /etc/t*
# Çıktı: /etc/terminfo /etc/timezone /etc/tmpfiles.d
```

---

## 8.2.1 Asterisk (*) Karakteri

**Sıfır veya daha fazla herhangi bir karakter**

```bash
# /etc içinde 't' ile başlayan dosyalar
echo /etc/t*

# .d ile biten dosyalar
echo /etc/*.d

# 'r' ile başlayan, '.conf' ile biten dosyalar
echo /etc/r*.conf
```

---

## 8.2.2 Question Mark (?) Karakteri

**Tam olarak bir karakter**

```bash
# 't' ile başlayan ve sonra 7 karakter olan dosyalar
echo /etc/t???????
# Çıktı: /etc/terminfo /etc/timezone

# 20+ karakterli dosyalar
echo /etc/*????????????????????
```

---

## 8.2.3 Bracket [ ] Karakterleri

**Karakter aralığı veya listesi**

```bash
# 'g' veya 'u' ile başlayan
echo /etc/[gu]*

# 'a' ile 'd' arasında başlayan
echo /etc/[a-d]*

# Sayı içeren dosyalar
echo /etc/*[0-9]*
```

---

## 8.2.4 Exclamation Point (!) - Olumsuzlama

**Listelenen karakterleri HARİÇ tut**

```bash
# D veya P ile başlamayan
echo /etc/[!DP]*

# a'dan t'ye kadar (olumsuzlama)
echo /etc/[!a-t]*
```

---

## 8.2.5 ls ile Globbing ve -d Seçeneği

```bash
# Sorunlu: Dizin içeriğini gösterir
ls /etc/ap*

# Çözüm: -d ile dizin adını göster
ls -d /etc/x*
# Çıktı: /etc/xdg
```

---

## 8.3 Dosya Kopyalama - cp Komutu

**Temel sözdizimi:**

```bash
cp kaynak hedef
```

**Örnekler:**

```bash
# /etc/hosts'u home dizinine kopyala
cp /etc/hosts ~

# Farklı ad ile kopyala
cp /etc/hosts ~/hosts.copy
```

---

## 8.3.1 Verbose Modu (-v)

```bash
cp -v /etc/hosts ~
# Çıktı: `/etc/hosts' -> `/home/sysadmin/hosts'
```

**Başarı mesajı görmek için kullanılır.**

---

## 8.3.2 Üzerine Yazma Koruması

**Tehlike:** Mevcut dosyalar silinir!

```bash
# Dosya silinecek - dikkat!
cp /etc/hostname example.txt
```

**Çözüm:** `-i` (interactive) veya `-n` (no clobber)

---

## 8.3.2 İnteraktif Modu (-i)

```bash
# Her silmeden önce sor
cp -i /etc/hosts example.txt
# cp: overwrite `/home/sysadmin/example.txt'? n
```

**Güvenli:** Her işlem öncesi onay ister.

---

## 8.3.2 No Clobber Modu (-n)

```bash
# Otomatik olarak yazmayı reddet (sorma)
cp -n /etc/skel/.* ~
```

**Daha otomatik:** Sorulmadan üzerine yazmaz.

---

## 8.3.3 Dizinleri Kopyalama (-r)

```bash
cp -r kaynak_dizin hedef_dizin
```

**Dikkat:** Tüm içerik kopyalanır!

- `-r` = recursive (özyinelemeli)
- `-R` = alternatif (GNU)

---

## 8.4 Dosya Taşıma - mv Komutu

```bash
mv kaynak hedef
```

**Örnekler:**

```bash
# Dosyayı taşı
mv hosts Videos/

# Başka dizine ve yeni ad
mv example.txt Videos/newexample.txt
```

---

## 8.4.1 Dosya Yeniden Adlandırma

```bash
cd Videos
mv newexample.txt myfile.txt
# Yine aynı dizinde!
```

**Hedef aynı dizin = yeniden adlandırma**

---

## 8.4.2 mv Seçenekleri

| Seçenek | Anlam |
|---------|-------|
| `-i` | İnteraktif: Üzerine yazılacak mı? |
| `-n` | No Clobber: Yazmayı reddet |
| `-v` | Verbose: Sonucu göster |

---

## 8.5 Boş Dosya Oluşturma - touch

```bash
touch sample

# Kontrol
ls -l sample
# -rw-rw-r-- 1 sysadmin sysadmin 0 Nov  9 16:48 sample
```

**Boyut = 0 bytes** (boş dosya)

---

## 8.6 Dosya Silme - rm Komutu

```bash
rm sample
rm hosts.copy
```

<div class="highlight-box">
⚠️ **Dikkat:** Silme **kalıcı**! Geri alma yok!
</div>

---

## 8.6 -i Seçeneği ile Güvenli Silme

```bash
touch sample.txt example.txt test.txt

rm -i *.txt
# rm: remove regular empty file `example.txt'? y
# rm: remove regular empty file `sample.txt'? n
```

---

## 8.6 Dizinleri Silme (rm -r)

```bash
# Hata: Varsayılan davranış
rm Videos
# rm: cannot remove `Videos': Is a directory

# Çözüm: -r (recursive)
rm -r Videos

# Veya boş dizini sil
rmdir Documents
```

---

## 8.7 Dizin Oluşturma - mkdir

```bash
mkdir test

ls
# Desktop  Documents  Downloads  test
```

---

## Bölüm 8 Özeti

✅ **Globbing:** *, ?, [ ], [!]
✅ **Dosya Kopyalama:** cp, cp -r
✅ **Taşıma/Yeniden Adlandırma:** mv
✅ **Silme:** rm, rmdir
✅ **Oluşturma:** touch, mkdir

---

<!-- _class: topic-slide -->
<!-- _paginate: false -->

![bg](../gorseller/2_Konu_baslik.png)

# Arşivleme ve Sıkıştırma

---

## Arşivleme ve Sıkıştırma - Diyagram

![width:900px height:400px](gorseller/compression_diagram.svg)

---

## 📌 Bölüm 9 Özeti

Bu bölümde **dosyaları arşivleme ve sıkıştırmayı** öğreneceksiniz:

- **Sıkıştırma Türleri:** Lossless vs. Lossy sıkıştırma
- **Sıkıştırma Araçları:** `gzip`, `bzip2`, `xz` komutları
- **Tar Arşiv Komutu:** `tar` ile dosyaları arşivleme
  - Create mode: `tar -czf`
  - Extract mode: `tar -xzf`
  - List mode: `tar -tzf`
- **Kombinasyon Formatları:** `.tar.gz`, `.tar.bz2`, `.tar.xz`
- **ZIP Formatı:** `zip` ve `unzip` komutları

Verilerinizi verimli şekilde depolama ve paylaşma için bu teknikler gereklidir.

---

## 9.1 Giriş - Neden Arşivleme?

- **Arşivleme:** Çok dosya → bir dosya
- **Sıkıştırma:** Dosya boyutunu küçült
- Taşıma kolaylığı
- Depolama ve aktarım verimliliği
- Yedekleme

---

## 9.2 Sıkıştırma Türleri

| Tür | Açıklama |
|-----|----------|
| **Lossless** | Hiç veri kaybı yok (belge, log) |
| **Lossy** | Bazı veriler çıkarılabilir (resim, ses) |

**Linux'ta:** Lossless tercih edilir.

---

## 9.2 gzip Komutu

```bash
ls -l longfile.txt
# 66540 bytes

gzip longfile.txt

ls -l longfile.txt.gz
# 341 bytes (99.5% küçültme!)
```

---

## 9.2 Sıkıştırma Oranını Kontrol Et

```bash
gzip -l longfile.txt.gz
# compressed        uncompressed  ratio
#       341               66540  99.5%
```

---

## 9.2 Dosya Açma - gunzip & gzip -d

```bash
# Yöntem 1
gunzip longfile.txt.gz

# Yöntem 2
gzip -d longfile.txt.gz

# Sonuç
ls -l longfile.txt
# 66540 bytes (orijinal boyut)
```

---

## 9.2 Diğer Sıkıştırma Araçları

| Araç | Uzantı | Özellik |
|------|--------|---------|
| gzip | .gz | Standart |
| bzip2 | .bz2 | Daha iyi sıkıştırma |
| xz | .xz | Çok iyi sıkıştırma |

---

## 9.3 Arşivleme - tar Komutu

```bash
tar -c [-f ARCHIVE] [OPTIONS] [FILE...]
```

**tar Modları:**

- Create: Yeni arşiv oluştur
- Extract: Dosyaları çıkar
- List: İçeriği listele

---

## 9.3.1 Create Mode (Arşiv Oluştur)

```bash
# Basit tar
tar -cf alpha_files.tar alpha*

ls -l alpha_files.tar
# 10240 bytes

# gzip ile sıkıştır
tar -czf alpha_files.tar.gz alpha*

ls -l alpha_files.tar.gz
# 417 bytes (96.1% küçültme)
```

---

## 9.3.1 bzip2 ile Sıkıştırma

```bash
# tar + bzip2 (-j)
tar -cjf folders.tbz School

# Uzantılar: .tar.bz2, .tbz, .tbz2
```

---

## 9.3.2 List Mode (İçeriği Göster)

```bash
tar -tjf folders.tbz

# Çıktı:
# School/
# School/Engineering/
# School/Engineering/hello.sh
```

---

## 9.3.3 Extract Mode (Dosyaları Çıkar)

```bash
cd Downloads
tar -xjf folders.tbz

ls -l
# School/ ve folders.tbz

# Verbose modu (-v)
tar -xjvf folders.tbz
```

---

## 9.3.3 Seçici Çıkarma

```bash
# Belirli dosyayı çıkar
tar -xjvf folders.tbz School/Art/linux.txt

# Pattern ile çıkar
tar -xjf folders.tbz School/Art/*
```

---

## 9.4 ZIP Dosyaları

**zip:** Microsoft standartı

```bash
# Oluştur
zip alpha_files.zip alpha*

# Yinelemeli
zip -r School.zip School
```

---

## 9.4 ZIP Listeleme ve Çıkarma

```bash
# Listele
unzip -l School.zip

# Çıkar
unzip School.zip

# Belirli dosya
unzip School.zip School/Art/linux.txt
```

---

<!-- _class: topic-slide -->
<!-- _paginate: false -->

![bg](../gorseller/2_Konu_baslik.png)

# Pipes ve Redirection

---

## Pipes ve Redirection - Diyagram

![width:900px height:350px](gorseller/pipes_redirection_diagram.svg)

---

## 📌 Bölüm 10 Özeti

Bu bölümde **metin dosyalarıyla verimli şekilde çalışmayı** öğreneceksiniz:

- **Dosya Görüntüleme:** `cat`, `less`, `head`, `tail` komutları
- **Pipes (|):** Komutların çıktısını zincirleyerek kullanma
- **I/O Yönlendirme:** `>`, `>>`, `<`, `2>`, `&>` operatörleri
- **Standart Akışlar:** STDIN, STDOUT, STDERR kavramları
- **Sıralama:** `sort` komutu ile verileri düzenleme
- **Metin Filtreleme:** `grep` ile pattern matching
- **Sütun Çıkarma:** `cut` komutu
- **Dosya İstatistikleri:** `wc` (word count) komutu
- **Regular Expressions:** Temel regex desenleri

---

## 10.1 Dosya Görüntüleme

**cat:** Dosya içeriğini göster

```bash
cat food.txt
# Food is good.

# Birden çok dosya
cat file1.txt file2.txt
```

---

## 10.1.2 less - Pager

```bash
less words
```

**Hareket Komutları:**

- `Space` = Sayfa ileri
- `b` = Sayfa geri
- `Enter` = Bir satır ileri
- `q` = Çıkış
- `h` = Yardım

---

## 10.1.2 less - Arama

```bash
# İleri ara
/frog

# Geri ara
?pattern

# Sonraki match
n

# Önceki match
Shift+N
```

---

## 10.1.3 head Komutu

```bash
# İlk 10 satır (varsayılan)
head /etc/sysctl.conf

# İlk 3 satır
head -n 3 /etc/sysctl.conf

# Alternatif
head -3 /etc/sysctl.conf
```

---

## 10.1.3 tail Komutu

```bash
# Son 10 satır (varsayılan)
tail /etc/sysctl.conf

# Son 5 satır
tail -5 /etc/sysctl.conf

# 25. satırdan sona kadar
tail -n +25 /etc/passwd
```

---

## 10.1.3 tail -f (Canlı İzleme)

```bash
# Log dosyasını gerçek zamanlı izle
tail -f /var/log/mail.log

# Ctrl+C ile çık
```

---

## 10.2 Pipe (|) - Komut Zinciri

**Bir komutun çıktısını diğerine iletmek**

```bash
# ls çıktısı → head'e
ls /etc | head

# Çıktı:
# X11
# adduser.conf
```

---

## 10.2 Pipe Örnekleri

```bash
# Satır sayısını say
ls /etc | wc -l

# 142

# Dosyaları numarala
ls /etc/ssh | nl
```

---

## 10.2 Çoklu Pipes

```bash
# ls → nl → tail
ls /etc/ssh | nl | tail -5

# nl → tail → nl (sıra önemli!)
ls /etc/ssh | tail -5 | nl
```

---

## 10.3 Standart Akışlar

| Akış | Numarası | Açıklama |
|------|----------|----------|
| **STDIN** | 0 | Giriş (klavye) |
| **STDOUT** | 1 | Çıktı (başarılı) |
| **STDERR** | 2 | Hata mesajları |

---

## 10.3.1 STDOUT Yönlendirmesi (>)

```bash
echo "Line 1" > example.txt

# Dosyayı kontrol et
cat example.txt
# Line 1

# ⚠️ Üzerine yazma!
echo "New line" > example.txt
```

---

## 10.3.1 STDOUT Ekleme (>>)

```bash
cat example.txt
# New line 1

echo "Another line" >> example.txt

cat example.txt
# New line 1
# Another line
```

---

## 10.3.2 STDERR Yönlendirmesi (2>)

```bash
# Hata mesajı gözlemle
ls /fake
# ls: cannot access /fake: No such file or directory

# STDOUT yönlendir (hata gözüksün)
ls /fake > output.txt
# ls: cannot access /fake: No such file or directory

# STDERR yönlendir
ls /fake 2> error.txt
```

---

## 10.3.3 Birden Çok Akış

```bash
# İkisi de aynı dosyaya
ls /fake /etc/ppp &> all.txt

# Farklı dosyalara
ls /fake /etc/ppp > out.txt 2> err.txt
```

---

## 10.3.4 STDIN Yönlendirmesi (<)

```bash
# tr komutu STDIN'den okur
tr 'a-z' 'A-Z' < example.txt

# Çıktıyı başka dosyaya yaz
tr 'a-z' 'A-Z' < example.txt > newexample.txt
```

---

## 10.4 sort - Sıralama

```bash
sort mypasswd
# Alfabetik sıralama

# Ters sıralama
sort -r mypasswd
```

---

## 10.4.1 Alan Bazında Sıralama

```bash
# ':' sınırlayıcı, 3. alan, sayısal
sort -t: -n -k3 mypasswd

# Ters sıralama
sort -t: -n -r -k3 mypasswd
```

---

## 10.4.1 Çoklu Alan Sıralaması

```bash
# CSV: 2. alan → 1. alan (sayısal) → 3. alan
sort -t, -k2 -k1n -k3 os.csv

# Linux
# Minix
# Unix (1970 Thompson)
```

---

## 10.5 wc - Dosya İstatistikleri

```bash
wc /etc/passwd
#   35   56 1710 /etc/passwd

# Sadece satırları say
wc -l /etc/passwd
# 35

# Pipe ile kulllan
ls /etc/ | wc -l
# 142 dosya/dizin
```

---

## 10.6 cut - Sütun Çıkarma

```bash
# 1., 5., 6., 7. alanları göster
cut -d: -f1,5-7 mypasswd

# Karakter konumuna göre
ls -l | cut -c1-11,50-
```

---

## 10.7 grep - Filtreleme

```bash
# bash içeren satırları bul
grep bash /etc/passwd

# Renkle göster
grep --color bash /etc/passwd

# Kaç satır eşleşti?
grep -c bash /etc/passwd
# 2
```

---

## 10.7 grep Seçenekleri

```bash
# Satır numarası göster (-n)
grep -n bash /etc/passwd

# Olumsuzlama (-v)
grep -v nologin /etc/passwd

# Küçük/büyük harf duyarsız (-i)
grep -i the newhome.txt

# Tam kelime (-w)
grep -w are newhome.txt
```

---

## 10.8 Temel Regex - Dönem (.)

**Herhangi bir tek karakter**

```bash
# r + 2 karakter + f
grep 'r..f' red.txt
# reef
# roof

# 4+ karakter
grep '....' red.txt
```

---

## 10.8.2 Bracket [ ] Regex

```bash
# 0-9 arası sayı
grep '[0-9]' profile.txt

# Olumsuzlama: 0-9 hariç
grep '[^0-9]' profile.txt
```

---

## 10.8.3 Asterisk (*) Regex

```bash
# 0+ 'e' karakteri
grep 're*d' red.txt

# Liste
grep 'r[oe]*d' red.txt

# En az 1 'e'
grep 'ee*' red.txt
```

---

## 10.8.4 Anchor Karakterleri

```bash
# Başında (^)
grep '^root' /etc/passwd

# Sonunda ($)
grep 'r$' alpha-first.txt

# Başında ve sonunda
grep '^root$' /etc/passwd
```

---

## 10.8.5 Backslash (\) - Kaçış

```bash
# Özel karakter eşleştir
grep 're\*' newhome.txt

# Asterisk'in kendisini bul!
```

---

## 10.8.6 Extended Regex (-E)

```bash
# 0 veya 1 'u' (?)
grep -E 'colou?r' spelling.txt

# 1+ 'e' (+)
grep -E 'e+' red.txt

# VEYA (|)
grep -E 'gray|grey' spelling.txt
```

---

## Bölüm 10 Özeti

✅ **Görüntüleme:** cat, less, head, tail
✅ **Pipes:** | ile komutları zincirle
✅ **Yönlendirme:** >, >>, <, 2>
✅ **İşleme:** sort, wc, cut, grep
✅ **Regex:** ., [ ], *, ^, $, -E

---

<!-- SON SLAYT: İLETİŞİM -->
<!-- _class: final-slide -->
<!-- _paginate: false -->

# 📚 Teşekkürler!

**KAPADOKYA ÜNİVERSİTESİ**
Linux Temel Eğitimi

📧 **Email:** info@kapadokya.edu.tr
🌐 **Website:** www.kapadokya.edu.tr
💼 **Dr. Bekir Ağırgün**
