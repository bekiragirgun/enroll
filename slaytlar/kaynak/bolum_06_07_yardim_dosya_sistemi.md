---
marp: true
theme: default
paginate: true
lang: tr
backgroundColor: #F7F7F7
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
    font-size: 24pt;
    font-weight: bold;
    margin-bottom: 20px;
    border-bottom: 3px solid #6B9FE8;
    padding-bottom: 10px;
  }

  h2 {
    color: #2D4A7C;
    font-size: 16pt;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 15px;
  }

  h3 {
    color: #2D4A7C;
    font-size: 13pt;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 10px;
  }

  p, li {
    font-size: 11pt;
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
    font-size: 10pt;
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
    font-size: 10pt;
    line-height: 1.5;
  }

  .two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-top: 20px;
  }

  .subtitle-box {
    background-color: #E6EAF3;
    padding: 15px 18px;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    margin-top: 20px;
  }

  .info-box {
    background-color: #FFFFFF;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    margin-top: 15px;
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

  .compare-box {
    background-color: #F5F5F5;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
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
    font-size: 36pt;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    border-bottom: none;
  }

  section.cover-slide p {
    position: absolute;
    bottom: 40px;
    right: 60px;
    color: white;
    font-size: 18pt;
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
    font-size: 36pt;
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
    font-size: 18pt;
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

  section.final-slide div *,
  section.final-slide a {
    color: white !important;
  }

  img {
    max-width: 95%;
    max-height: 500px;
    object-fit: contain;
    margin: 10px auto;
    display: block;
  }
---

<!-- 1. SLAYT: DERS BAŞLIĞI -->
<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# İşletim Sistemleri

Dr. Bekir Ağırgün

---

<!-- 2. SLAYT: HAFTALIK KONU -->
<!-- _class: topic-slide -->
<!-- _paginate: false -->

![bg](../gorseller/2_Konu_baslik.png)

# Linux'ta Yardım Alma ve Dosya Sistemi

Dr. Bekir Ağırgün

---

# 📚 İçerik

- **Man Pages (Manual Pages)**
- **Komut ve Dokümantasyon Bulma**
- **Info Dokümantasyonu**
- **Ek Yardım Kaynakları**
- **Dosya Sisteminde Gezinme**

---

# 🔧 Linux'ta Yardım Sistemlerinin Önemi

<div class="highlight-box">

### Neden Yardım Gerekir?

- **Binlerce komut** ve birçok seçenek mevcut
- Komut satırı **güçlü ama karmaşık** olabilir
- Yeni komutlar öğrenirken **bilgi kaynağı**
- Komutların nasıl çalıştığını **hatırlatıcı**

</div>

<div class="info-box">

**💡 Temel Prensip:** Linux'ta kaybolduğunuzda, yardım her zaman bir komut uzağınızda!

</div>

---

# 📖 Man Pages (Manual Pages)

<div class="subtitle-box">

## UNIX Kökeni
UNIX geliştiricileri tarafından oluşturulmuş yardım belgeleri

</div>

### Man Page Özellikleri

- Komutların **özelliklerini açıklar**
- Komutun **amacını** detaylandırır
- **Kullanılabilir seçenekleri** listeler
- Komut satırı referans kaynağı

---

# 📄 Man Page Görüntüleme

<div class="two-columns">
<div>

### Sözdizimi
```bash
man komut_adı
```

### Örnek: ls Komutu
```bash
man ls
```

</div>
<div>

### Çıktı Örneği
```
LS(1)         User Commands        LS(1)

NAME
    ls - list directory contents

SYNOPSIS
    ls [OPTION]... [FILE]...

DESCRIPTION
    List information about the FILEs
```

</div>
</div>

### Gezinme
- **Ok tuşları** ile gezinme
- **Q tuşu** ile çıkış

---

# 📑 Man Page Bölümleri

| Bölüm | Açıklama |
|-------|----------|
| **NAME** | Komut adı ve kısa açıklama |
| **SYNOPSIS** | Komutun nasıl kullanılacağı |
| **DESCRIPTION** | Detaylı açıklama |
| **OPTIONS** | Kullanılabilir seçenekler |
| **FILES** | İlişkili dosyalar |
| **AUTHOR** | Yazarın adı |
| **REPORTING BUGS** | Hata raporu bilgisi |
| **COPYRIGHT** | Telif hakkı bilgisi |
| **SEE ALSO** | İlgili komutlar |

---

# 📋 SYNOPSIS Bölümünü Anlamak

<div class="info-box">

### Sembollerin Anlamı

```bash
cal [-31jy] [-A number] [-B number] [-d yyyy-mm] [[month] year]
```

- **[ ]** = İsteğe bağlı (opsiyonel)
- **| (pipe)** = Veya (alternatif seçenekler)
- **...** = Birden fazla öğe kullanılabilir
- **[ ] içinde [ ]** = Karmaşık opsiyonel yapılar

</div>

### Örnek Açıklama

```bash
date [-u|--utc|--universal] [MMDDhhmm[[CC]YY][.ss]]
```

✅ `-u` **veya** `--utc` **veya** `--universal` kullanılabilir (aynı işlevi görürler)

---

# 🔎 Man Page'lerde Arama

<div class="highlight-box">

### Arama İşlemi

1. **Man page içinde `/` tuşuna bas**
2. **Arama terimini yaz**
3. **Enter tuşuna bas**
4. **n** = Sonraki eşleşme
5. **Shift+N** = Önceki eşleşme

</div>

### Örnek
```bash
man ls
# Açıldıktan sonra:
/size        # "size" kelimesini ara
```

**Sonuç:** Eşleşmeler vurgulanır, `n` ile sonraki eşleşmeye geç

---

# 📚 Man Page Kategorileri (Sections)

<div class="two-columns">
<div>

### 9 Ana Kategori

1. **General Commands** (Genel Komutlar)
2. **System Calls** (Sistem Çağrıları)
3. **Library Calls** (Kütüphane Çağrıları)
4. **Special Files** (Özel Dosyalar)
5. **File Formats** (Dosya Formatları)

</div>
<div>

6. **Games** (Oyunlar)
7. **Miscellaneous** (Çeşitli)
8. **System Admin Commands** (Sistem Yönetim Komutları)
9. **Kernel Routines** (Çekirdek Rutinleri)

</div>
</div>

<div class="info-box">

**Not:** Man komutu bu kategorileri **sırayla arar** ve **ilk eşleşmeyi** gösterir.

</div>

---

# 🔢 Kategoriye Göre Man Page Görüntüleme

<div class="subtitle-box">

## Aynı İsimde Birden Fazla Man Page

</div>

### Sorun
- `passwd` **komutu** (şifre değiştirme)
- `passwd` **dosyası** (kullanıcı hesap bilgileri)

### Çözüm: Kategori Numarası Belirtme

```bash
man passwd        # Komut (Kategori 1)
man 5 passwd      # Dosya (Kategori 5)
```

---

# 🔍 Man Page Arama Komutları

<div class="two-columns">
<div>

### `man -f` (whatis)
**İsme göre kesin arama**

```bash
man -f passwd
```
**Çıktı:**
```
passwd (5) - the password file
passwd (1) - change user password
passwd (1ssl) - compute password hashes
```

</div>
<div>

### `man -k` (apropos)
**Anahtar kelimeye göre arama**

```bash
man -k copy
```
**Çıktı:**
```
cp (1) - copy files and directories
scp (1) - secure copy
install (1) - copy files and set attributes
```

</div>
</div>

<div class="highlight-box">

**💡 İpucu:** Tam komut adını bilmiyorsanız `man -k` kullanın!

</div>

---

# 📂 Komut ve Dokümantasyon Bulma

<div class="subtitle-box">

## `whereis` - Komut ve Man Page Konumları

</div>

### Kullanım
```bash
whereis ls
```

### Çıktı
```
ls: /bin/ls /usr/share/man/man1p/ls.1.gz /usr/share/man/man1/ls.1.gz
```

<div class="info-box">

**Açıklama:**
- `/bin/ls` = Komutun yeri
- `.gz` uzantılı dosyalar = Sıkıştırılmış man page'ler

</div>

---

# 🔎 Dosya ve Dizin Arama

<div class="highlight-box">

## `locate` Komutu
Sistemdeki **tüm dosya ve dizinleri** aramak için

</div>

### Temel Kullanım
```bash
locate gshadow
```

### Özellikler
- **Veritabanı** kullanır (hızlı arama)
- Veritabanı **her gece güncellenir**
- Bugün oluşturulan dosyalar bulunamayabilir

### Manuel Güncelleme (root gerekir)
```bash
sudo updatedb
```

---

# 🔢 Locate Komutunun Gelişmiş Kullanımı

<div class="two-columns">
<div>

### Sonuç Sayısını Öğrenme
```bash
locate -c passwd
```
**Çıktı:** `98`

### Basename Arama
```bash
locate -b "\passwd"
```
**Sonuç:**
```
/etc/passwd
/usr/bin/passwd
```

</div>
<div>

### Ne Fark Eder?

**Normal arama:**
```bash
locate passwd
```
→ Yolda "passwd" geçen **tüm dosyalar**

**Basename arama:**
```bash
locate -b "\passwd"
```
→ Sadece **tam adı "passwd"** olan dosyalar

</div>
</div>

---

# ℹ️ Info Dokümantasyonu

<div class="subtitle-box">

## Man Page'lere Alternatif

</div>

### Info vs Man Pages

<div class="two-columns">
<div>

**Man Pages**
- Her sayfa **bağımsız**
- Referans odaklı
- Hızlı bilgi edinme

</div>
<div>

**Info Dokümantasyonu**
- **Birbirine bağlı** yapı
- Öğretici (tutorial) tarzı
- Mantıksal organizasyon

</div>
</div>

<div class="highlight-box">

**💡 Fark:** Info dokümantasyonu bir **kitap**, man pages ise **sözlük** gibi!

</div>

---

# 📖 Info Dokümantasyon Görüntüleme

### Sözdizimi
```bash
info komut_adı
```

### Örnek
```bash
info ls
```

<div class="info-box">

### Çıktı Örneği
```
Next: dir invocation, Up: Directory listing

10.1 'ls': List directory contents
==================================

The 'ls' program lists information about files (of any type, including
directories). Options and file arguments can be intermixed arbitrarily.
```

</div>

---

# 🧭 Info Dokümantasyon Gezinme

| Tuş | İşlev |
|-----|-------|
| **Shift+H** | Yardım menüsünü göster |
| **Yukarı/Aşağı** | Satır satır gezinme |
| **PgUp/PgDn** | Sayfa sayfa gezinme |
| **Home/End** | Node başına/sonuna git |
| **TAB** | Sonraki hiperlinke atla |
| **Enter** | Hiperlinke tıkla |
| **L** | Son görüntülenen yere geri dön |
| **U** | Bir seviye yukarı çık |
| **Q** | Info'dan çık |

---

# 🗂️ Info Dokümantasyon Yapısı

<div class="highlight-box">

### Node (Düğüm) Sistemi

**Node** = Kitaptaki bölüm gibi

</div>

<div class="info-box">

### Gezinme Örneği
```
Next: Details about version sort
Prev: What information is listed
Up: ls invocation

10.1.3 Sorting the output
-------------------------

These options change the order in which 'ls' sorts...
```

- **Next** = Sonraki node
- **Prev** = Önceki node
- **Up** = Üst seviye node

</div>

---

# 🌐 Üst Seviye Info Menüsü

### Komut
```bash
info
```

### Çıktı
```
File: dir,  Node: Top,  This is the top of the INFO tree.

* Menu:

Basics
* Common options: (coreutils)Common options.
* Coreutils: (coreutils).        Core GNU utilities.
* Date input formats: (coreutils)Date input formats.
* File permissions: (coreutils)File permissions.
```

<div class="highlight-box">

**💡 Keşfet:** `info` komutu Linux yeteneklerini keşfetmek için harika bir başlangıç noktası!

</div>

---

# 🆘 Ek Yardım Kaynakları

<div class="subtitle-box">

## `--help` Seçeneği

</div>

### Kullanım
```bash
komut --help
```

### Örnek: `cat --help`
```
Usage: cat [OPTION]... [FILE]...
Concatenate FILE(s) to standard output.

  -A, --show-all           equivalent to -vET
  -b, --number-nonblank    number nonempty output lines
  -n, --number             number all output lines
      --help               display this help and exit
```

---

# 📄 Sistem Dokümantasyon Dizinleri

<div class="highlight-box">

### README Dosyaları

Yazılım satıcıları tarafından sağlanan ek dokümantasyon

</div>

### Tipik Konumlar

```bash
/usr/share/doc
/usr/doc
```

### Örnek
```bash
ls /usr/share/doc
```

<div class="info-box">

**Not:** Sistem yöneticileri için **kurulum rehberleri** ve **yapılandırma örnekleri** içerir.

</div>

---

# 🗂️ Linux Dosya Sistemi Yapısı

<div class="subtitle-box">

## Windows vs Linux

</div>

<div class="two-columns">
<div>

### Windows
- **Üst seviye:** My Computer
- **Sürücüler:** C:, D:, E:
- Her sürücü **bağımsız**

</div>
<div>

### Linux
- **Üst seviye:** `/` (root)
- **Sürücü harfi yok**
- Her cihaz **bir dizin** altında

</div>
</div>

<div class="highlight-box">

**Temel Fark:** Linux'ta her şey **tek bir ağaç yapısı** altında!

</div>

---

# 🗂️ Windows Dizin Yapısı

![Windows Dizin Yapısı](../gorseller/LEv2_7_2.png)

---

# 🗂️ Linux Root Dizini

![Linux Root Dizini](../gorseller/LEv2_7_4.png)

---

# 🌳 Linux Dosya Sistemi Ağacı

```
/
├── bin
├── boot
├── dev
├── etc
├── home
│   └── sysadmin
│       ├── Desktop
│       ├── Documents
│       └── Downloads
├── lib
├── media
├── opt
├── root
├── usr
└── var
```

---

# 🌳 Linux Dosya Sistemi Ağacı (Görsel)

![Linux Dosya Sistemi Ağacı](../gorseller/LEv2_7_3.png)

---

# 🏠 Home Dizini (Ev Dizini)

<div class="info-box">

### `/home` Dizini
Her kullanıcı için **kişisel çalışma alanı**

</div>

### Yapı
```
/home
├── user1
├── user2
└── sysadmin
```

### Özellikler
- Kullanıcı **tam kontrole** sahip
- Dosya oluşturma/silme izni var
- Diğer kullanıcılar **erişemez** (güvenlik)

---

# 🏠 Home Dizin Yapısı

![Home Dizin Yapısı](../gorseller/LEv2_7_5.png)

---

# 🏠 Home Dizini Sembolü: `~`

<div class="highlight-box">

### Tilde (~) Karakteri

`~` = Kısa yol (Home dizinini temsil eder)

</div>

### Kullanım Örnekleri

```bash
~           # /home/sysadmin (kendi home'un)
~bob        # /home/bob (bob'un home'u)
```

### Pratik Örnek
```bash
cd ~           # Home dizinine git
cd ~/Documents # Documents klasörüne git
```

---

# 🏠 Home Dizini İçeriği

![Home Dizini İçeriği](../gorseller/LEv2_7_6.png)

---

# 📍 Mevcut Dizin Kontrolü: `pwd`

<div class="subtitle-box">

## Print Working Directory

</div>

### Kullanım
```bash
pwd
```

### Örnek Çıktı
```bash
sysadmin@localhost:~$ pwd
/home/sysadmin
```

<div class="info-box">

**Açıklama:** Dosya sisteminde **nerede olduğunuzu** gösterir.

</div>

---

# 📍 Mevcut Dizin Gösterimi

![Mevcut Dizin Gösterimi](../gorseller/LEv2_7_8.png)

---

# 🚶 Dizin Değiştirme: `cd`

<div class="subtitle-box">

## Change Directory

</div>

### Sözdizimi
```bash
cd [seçenekler] [yol]
```

### Örnekler
```bash
cd Documents        # Documents dizinine git
cd                  # Home dizinine git
cd /etc             # /etc dizinine git
cd ..               # Üst dizine git
```

---

# 🚶 Dizin Navigasyonu Gösterimi

![Dizin Navigasyonu](../gorseller/LEv2_7_7.png)

---

# 🛤️ Yol (Path) Türleri

<div class="two-columns">
<div>

### Mutlak Yol (Absolute)
- **Kökten** (`/`) başlar
- Her zaman **aynı konumu** gösterir

**Örnek:**
```bash
/home/sysadmin/Documents
```

</div>
<div>

### Göreceli Yol (Relative)
- **Bulunduğunuz konumdan** başlar
- `/` ile **başlamaz**

**Örnek:**
```bash
Documents/School/Art
```

</div>
</div>

<div class="highlight-box">

**💡 Hangi Path Kullanmalı?**
- **Mutlak yol:** Her yerden aynı konuma gitmek için
- **Göreceli yol:** Yakın dizinler için daha kısa

</div>

---

# 🛤️ Dizin Yolu Örnekleri

![Dizin Yolu Örnekleri](../gorseller/sysadmin_2.png

---

# 🎯 Yol Kısayolları

| Sembol | Anlamı | Örnek |
|--------|--------|-------|
| **~** | Home dizini | `cd ~` |
| **.** | Mevcut dizin | `ls .` |
| **..** | Üst dizin | `cd ..` |

### Kullanım Örnekleri

```bash
cd ../..              # İki seviye yukarı çık
cd ../../Downloads    # İki üst, sonra Downloads
cd ~/Documents        # Home'dan Documents'e
```

---

# 🎯 Dizin Hiyerarşisi Örneği

![Dizin Hiyerarşisi Örneği](../gorseller/sysadmin.png

---

# 📋 Dosya Listeleme: `ls`

<div class="subtitle-box">

## List - En Çok Kullanılan Komut

</div>

### Temel Kullanım
```bash
ls                    # Mevcut dizin
ls /var               # Belirtilen dizin
```

### Çıktı
```bash
sysadmin@localhost:~$ ls
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos
```

<div class="info-box">

**Not:** Renkli çıktı genellikle **alias** ile sağlanır (`ls --color=auto`)

</div>

---

# 📋 ls Komutu Çıktısı

![ls Komutu Çıktısı](../gorseller/LEv2_7_11.png)

---

# 🙈 Gizli Dosyaları Gösterme

<div class="highlight-box">

### Gizli Dosya = `.` ile Başlayan Dosya

Genellikle **yapılandırma dosyaları**

</div>

### `-a` Seçeneği
```bash
ls -a
```

### Çıktı
```bash
.              .bashrc           Documents    Pictures
..             .cache            Downloads    Public
.bash_logout   .profile          Music        Videos
```

**Özel Dizinler:**
- `.` = Mevcut dizin
- `..` = Üst dizin

---

# 📊 Detaylı Listeleme: `ls -l`

### Long Format
```bash
ls -l /var/log
```

### Çıktı Örneği
```
total 900
-rw-r--r-- 1 root   root   15322 Dec 10 21:33 alternatives.log
drwxr-xr-x 1 root   root    4096 Jul 19 06:52 apt
-rw-r----- 1 syslog adm      371 Dec 15 16:38 auth.log
```

---

# 🔍 Detaylı Listeleme Alanları

```
-rw-r--r-- 1 root root 15322 Dec 10 21:33 alternatives.log
│          │ │    │    │     │            │
│          │ │    │    │     │            └─ Dosya adı
│          │ │    │    │     └─ Değiştirilme tarihi
│          │ │    │    └─ Dosya boyutu (byte)
│          │ │    └─ Group owner
│          │ └─ User owner
│          └─ Hard link sayısı
└─ Dosya tipi ve izinler
```

---

# 📁 Dosya Tipleri

| Sembol | Tip | Açıklama |
|--------|-----|----------|
| **-** | Regular file | Normal dosya |
| **d** | Directory | Dizin |
| **l** | Symbolic link | Sembolik bağlantı |
| **s** | Socket | İletişim soketi |
| **p** | Pipe | Boru hattı |
| **b** | Block file | Blok cihazı |
| **c** | Character file | Karakter cihazı |

---

# 📏 İnsan Okunabilir Boyutlar: `ls -lh`

<div class="subtitle-box">

## `-h` = Human Readable

</div>

### Karşılaştırma

```bash
ls -l /var/log/lastlog
-rw-rw-r-- 1 root utmp 292584 Dec 15 16:38 /var/log/lastlog

ls -lh /var/log/lastlog
-rw-rw-r-- 1 root utmp 286K Dec 15 16:38 /var/log/lastlog
```

<div class="highlight-box">

**💡 Fark:** `292584 byte` → `286K` (çok daha anlaşılır!)

</div>

---

# 🗂️ Dizin Bilgisini Gösterme: `ls -ld`

### Sorun
```bash
ls -l
```
→ Dizinin **içeriğini** gösterir

### Çözüm: `-d` Seçeneği
```bash
ls -ld
```
→ Dizinin **kendisini** gösterir

### Örnek
```bash
ls -ld
drwxr-xr-x 1 sysadmin sysadmin 224 Nov 7 17:07 .
```

---

# 🔄 Recursive Listeleme: `ls -R`

<div class="highlight-box">

### Tüm Alt Dizinleri de Listele

</div>

### Kullanım
```bash
ls -R /etc/ppp
```

### Çıktı
```
/etc/ppp:
ip-down.d  ip-up.d

/etc/ppp/ip-down.d:
bind9

/etc/ppp/ip-up.d:
bind9
```

<div class="info-box">

**⚠️ Dikkat:** Büyük dizinlerde çok uzun çıktı üretir!

</div>

---

# 📊 Sıralama Seçenekleri

<div class="two-columns">
<div>

### Boyuta Göre: `-S`
```bash
ls -lS
```
**Büyükten küçüğe**

### Zamana Göre: `-t`
```bash
ls -lt
```
**En yeni dosyalar önce**

</div>
<div>

### Ters Sıralama: `-r`
```bash
ls -lSr    # Küçükten büyüğe
ls -ltr    # En eski önce
```

### Tam Zaman: `--full-time`
```bash
ls -l --full-time
```
**Saat, dakika, saniye dahil**

</div>
</div>

---

# 📚 Teşekkürler!

<div>

📧 **Email:** bekir.agirgun@kapadokya.edu.tr
🌐 **Website:** www.kapadokya.edu.tr
💼 **LinkedIn:** Kapadokya Üniversitesi

</div>
