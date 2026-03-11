---
marp: true
theme: default
paginate: true
lang: tr
backgroundColor: #F7F7F7
style: |
  /* Genel Section Ayarları */
  section {
    font-family: 'Trebuchet MS', Arial, sans-serif;
    font-size: 90%;
    padding: 85px 50px 30px 50px;
    background-color: #F7F7F7;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  /* Başlık Stilleri */
  h1 {
    color: #2D4A7C;
    font-size: 26pt;
    font-weight: bold;
    margin-bottom: 20px;
    margin-left: 350px;
    padding-bottom: 10px;
    border-bottom: none !important;
    text-align: left;
  }

  h2 {
    color: #2D4A7C;
    font-size: 18pt;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 12px;
  }

  h3 {
    color: #4A7FB8;
    font-size: 15pt;
    font-weight: bold;
    margin-top: 12px;
    margin-bottom: 10px;
  }

  /* Paragraf ve Liste Stilleri */
  p, li {
    font-size: 13pt;
    line-height: 1.6;
    margin-bottom: 8px;
  }

  ul, ol {
    margin-left: 20px;
  }

  /* Cover Slide */
  section.cover-slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
    padding-left: 80px;
    position: relative;
  }

  section.cover-slide h1 {
    color: white;
    font-size: 38pt;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    border-bottom: none;
    margin-left: 0;
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

  /* Topic Slide */
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
    margin-left: 0;
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

  /* Final Slide */
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
    background-image: url('../gorseller/kapadokya_logo.png');
    background-size: contain;
    background-repeat: no-repeat;
    filter: brightness(0) invert(1);
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

  /* Layout - İki Sütun */
  .two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-top: 20px;
  }

  /* Info Box */
  .info-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .info-box h3 {
    color: white;
    margin-top: 0;
  }

  /* Highlight Box */
  .highlight-box {
    background: linear-gradient(135deg, #6B9FE8 0%, #4A7FB8 100%);
    color: white;
    padding: 18px;
    border-radius: 12px;
    margin: 15px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .highlight-box h3 {
    color: white;
    margin-top: 0;
  }

  /* Compare Box */
  .compare-box {
    background: #f0f4f8;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #6B9FE8;
  }

  /* Kod Blokları */
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

  /* Syntax Highlighting */
  pre code span.hljs-string,
  pre code span.hljs-literal,
  pre code span.hljs-attr {
    color: #f07d12;
  }

  /* Tablolar */
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
  }

  th, td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
  }

  th {
    background-color: #2D4A7C;
    color: white;
    font-weight: bold;
  }

  /* Info-box ve Highlight-box içindeki tablolar */
  .info-box table,
  .highlight-box table {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
  }

  .info-box th,
  .info-box td,
  .highlight-box th,
  .highlight-box td {
    color: black;
    border: 1px solid rgba(0, 0, 0, 0.2);
  }

  .info-box th,
  .highlight-box th {
    background-color: rgba(0, 0, 0, 0.1);
    font-weight: bold;
  }

  /* Sayfa Numarası */
  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
    position: absolute;
    bottom: 10px;
    right: 20px;
    font-size: 12pt;
    color: #666;
  }

  section.cover-slide::after,
  section.final-slide::after {
    content: '';
  }

  /* Diagram Box */
  .diagram-box {
    background: #f8f9fa;
    border: 2px solid #6B9FE8;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
  }

  /* Warning Box */
  .warning-box {
    background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);
    color: white;
    padding: 18px;
    border-radius: 12px;
    margin: 15px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .warning-box h3 {
    color: white;
    margin-top: 0;
  }

---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Temel Betik Yazımı

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Bu Ünitede Neler Öğreneceksiniz?

---

![bg](../gorseller/3_normal_slayt.png)

# Bu Ünitede Neler Öğreneceksiniz?

<div class="two-columns">
<div>

### Temel Konular

- Shell script nedir ve neden kullanılır?
- Script dosyası oluşturma ve çalıştırma
- Shebang (`#!`) kullanımı
- `nano` metin editörü ile düzenleme

</div>
<div class="info-box">

### Programlama Kavramları

- **Değişkenler** - Veri saklama
- **Koşullu İfadeler** - if/else/case
- **Döngüler** - for/while
- **Çıkış Kodları** - $?

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Giriş

---

![bg](../gorseller/3_normal_slayt.png)

# Giriş

<div class="two-columns">
<div>

### Shell Script Nedir?

- **Tekrar kullanılabilir komut dizileri**
- Öğrendiğiniz tüm komutları birleştirme
- Otomasyon ve verimlilik
- Tutarlı sonuçlar

</div>
<div class="highlight-box">

### Neden Script Yazmalıyız?

- Her gün aynı 5 komutu mı çalıştırıyorsunuz?
- **Tek bir komutla** hepsini yapın!
- Zaman kazancı
- Hata oranını düşürme

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Shell Script Temelleri

---

![bg](../gorseller/3_normal_slayt.png)

# Shell Script Nedir?

<div class="two-columns">
<div>

### Tanım

Bir shell script, bir metin dosyasında saklanan **çalıştırılabilir komutlar** dosyasıdır.

- Dosya çalıştırıldığında her komut sırayla işlenir
- Shell'in tüm komutlarına erişim
- **Mantıksal yapılar** kullanabilir (if, for, while)

</div>
<div class="info-box">

### Örnek: En Basit Script

```bash
echo "Hello, World!"
```

`test.sh` dosyası - tek satırlık bir script!

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Script Çalıştırma Yöntemleri

<div class="two-columns">
<div>

### Yöntem 1: Shell'e Argüman Olarak

```bash
sysadmin@localhost:~$ sh test.sh
Hello, World!
```

### Yöntem 2: Doğrudan Çalıştırma

```bash
sysadmin@localhost:~$ ./test.sh
-bash: ./test.sh: Permission denied
sysadmin@localhost:~$ chmod +x ./test.sh
sysadmin@localhost:~$ ./test.sh
Hello, World!
```

</div>
<div class="warning-box">

### Permission Denied Hatası

Script'i doğrudan çalıştırmak için:

1. **Çalıştırma izni** gerekli
2. `chmod +x script.sh` komutu
3. `./` prefix'i (mevcut dizin)

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Shebang (#!) Nedir?

<div class="two-columns">
<div>

### Shebang Satırı

```bash
#!/bin/bash
echo "Hello, World!"
```

veya

```bash
#!/bin/sh
echo "Hello, World!"
```

- `#!` karakterleri = **"shebang"** veya **"crunchbang"**
- İlk satırda bulunmalı
- Hangi yorumlayıcının kullanılacağını belirtir

</div>
<div class="info-box">

### Neden Önemli?

- Farklı shell'lerin **farklı sözdizimi** var
- `/bin/bash` - Bash shell
- `/bin/sh` - POSIX shell
- Perl, Ruby, Python için de kullanılır

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Metin Editörleri

---

![bg](../gorseller/3_normal_slayt.png)

# Shell Script Düzenleme

<div class="two-columns">
<div>

### Metin Editörleri

| Editör | Özellik |
|--------|---------|
| **nano** | Basit, öğrenmesi kolay |
| **vi/vim** | Güçlü, öğrenmesi zor |

### Önemli Not

LibreOffice gibi ofis araçları **uygun değil!** - biçimlendirme bilgileri içerir.

</div>
<div class="highlight-box">

### nano Editör

```bash
nano test.sh
```

- Basit ve kullanışlı
- Küçük dosyalar için ideal
- Klavye kısayolları altta görünür

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# nano Editör Arayüzü

```
GNU nano 2.2.6              File: test.sh              modified

#!/bin/sh

echo "Hello, World!"
echo -n "the time is "
date


^G Get Help  ^O WriteOut  ^R Read File ^Y Prev Page ^K Cut Text
^X Exit      ^J Justify   ^W Where Is  ^V Next Page ^U UnCut Text
```

<div class="info-box">

### Temel Kısayollar

- `^X` = Ctrl+X → Çıkış
- `^O` = Ctrl+O → Kaydet (WriteOut)
- `^K` = Ctrl+K → Satır Kes
- `^U` = Ctrl+U → Yapıştır

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# nano Komutları

<div class="two-columns">
<div>

| Kısayol | Açıklama |
|---------|----------|
| Ctrl + W | Ara |
| Ctrl + W, Ctrl + R | Bul ve Değiştir |
| Ctrl + G | Yardım |
| Ctrl + Y/V | Sayfa Yukarı/Aşağı |
| Ctrl + C | Konum Göster |
| Ctrl + K | Satır Kes |
| Ctrl + U | Yapıştır |

</div>
<div class="highlight-box">

### Kaydetme ve Çıkış

1. `Ctrl + X` → Çıkış
2. `Y` → Kaydet
3. `Enter` → Dosya adını onayla

**veya**

`Ctrl + O` → Kaydet (çıkmadan)

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Scripting Temelleri

---

![bg](../gorseller/3_normal_slayt.png)

# Scripting'in 3 Temel Kavramı

<div class="two-columns">
<div>

### 1. Değişkenler (Variables)

Script içinde geçici bilgi saklama

### 2. Koşullu İfadeler (Conditionals)

Testlere göre farklı işlemler yapma

### 3. Döngüler (Loops)

Aynı işlemi tekrar tekrar yapma

</div>
<div class="diagram-box">

```
┌──────────────────┐
│   DEĞİŞKENLER    │
│  ANIMAL="cat"    │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   KOŞULLAR       │
│  if [ ... ]; then│
└────────┬─────────┘
         │
┌────────▼─────────┐
│    DÖNGÜLER      │
│  for X in ...; do│
└──────────────────┘
```

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Değişkenler

---

![bg](../gorseller/3_normal_slayt.png)

# Değişken Tanımlama ve Kullanma

<div class="two-columns">
<div>

### Tanımlama

```bash
#!/bin/bash
ANIMAL="penguin"
echo "My favorite animal is a $ANIMAL"
```

**Çıktı:**
```
My favorite animal is a penguin
```

</div>
<div class="warning-box">

### Dikkat!

```bash
# DOĞRU
ANIMAL="penguin"

# YANLIŞ (boşluk yok!)
ANIMAL = "penguin"
```

Boşluk kullanırsanız "command not found" hatası alırsınız!

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Değişken Kuralları

<div class="two-columns">
<div>

### Atama vs Erişim

```bash
# Atama ($ yok)
ANIMAL="penguin"

# Erişim ($ var)
echo $ANIMAL
```

### Değişkeni Değişkene Atama

```bash
ANIMAL=penguin
SOMETHING=$ANIMAL
echo "Favori: $SOMETHING"
```

</div>
<div class="info-box">

### İsimlendirme

- **BÜYÜK HARF** kullanımı tavsiye edilir
- Değişkenler ile komutları ayırt etmeyi kolaylaştırır
- Örnek: `$USER`, `$HOME`, `$PATH`

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Komut Çıktısını Değişkene Atama

<div class="two-columns">
<div>

### Backtick Kullanımı

```bash
#!/bin/bash
CURRENT_DIRECTORY=`pwd`
echo "You are in $CURRENT_DIRECTORY"
```

### Modern Yöntem

```bash
#!/bin/bash
CURRENT_DIRECTORY=$(pwd)
echo "You are in $CURRENT_DIRECTORY"
```

</div>
<div class="highlight-box">

### Kullanım Alanları

- Metin işleme
- `sed` ve `awk` çıktıları
- Tarih/saat bilgisi alma
- Sistem bilgisi toplama

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Kullanıcıdan Girdi Alma

<div class="two-columns">
<div>

### read Komutu

```bash
#!/bin/bash

echo -n "What is your name? "
read NAME
echo "Hello $NAME!"
```

**Çalıştırma:**
```
What is your name? Bekir
Hello Bekir!
```

</div>
<div class="info-box">

### Özel Değişkenler

| Değişken | Anlamı |
|----------|--------|
| `$0` | Script adı |
| `$1` | 1. argüman |
| `$2` | 2. argüman |
| `$?` | Son komutun çıkış kodu |

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Argümanlar ve Çıkış Kodları

<div class="two-columns">
<div>

### Argüman Kullanımı

```bash
#!/bin/bash
echo "Hello $1"
```

```bash
$ ./test.sh World
Hello World
```

### Çıkış Kodu Kontrolü

```bash
$ grep -q root /etc/passwd
$ echo $?
0    # Bulundu

$ grep -q xyz /etc/passwd
$ echo $?
1    # Bulunamadı
```

</div>
<div class="highlight-box">

### exit Komutu

```bash
#!/bin/bash
# Hata durumunda
exit 1
```

- `0` = Başarılı
- `1-255` = Hata (programa özel)

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Koşullu İfadeler

---

![bg](../gorseller/3_normal_slayt.png)

# if İfadesi

<div class="two-columns">
<div>

### Temel Yapı

```bash
if somecommand; then
  # çıkış kodu 0 ise çalışır
fi
```

### Örnek: grep ile

```bash
#!/bin/bash

if grep -q root /etc/passwd; then
  echo "root dosyada var"
else
  echo "root dosyada yok"
fi
```

</div>
<div class="info-box">

### if/else/fi

- `if` → Koşul başlangıcı
- `then` → Koşul doğruysa
- `else` → Koşul yanlışsa
- `fi` → Blok sonu (`if`'in tersi)

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# test Komutu ve [ ]

<div class="two-columns">
<div>

### test Komut Örnekleri

| Komut | Açıklama |
|-------|----------|
| `test -f /path` | Dosya var mı? |
| `test -d /path` | Dizin var mı? |
| `test -x file` | Çalıştırılabilir mi? |
| `test 1 -eq 1` | Sayısal eşitlik |
| `test "a" = "a"` | String eşitlik |

</div>
<div class="highlight-box">

### Kısa Yazım: [ ]

```bash
# İkisi aynı:
if test -f /tmp/foo; then
if [ -f /tmp/foo ]; then
```

**Not:** `[` aslında bir komuttur!

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Karşılaştırma Operatörleri

<div class="two-columns">
<div>

### Sayısal Karşılaştırma

| Operatör | Anlamı |
|----------|--------|
| `-eq` | Eşit |
| `-ne` | Eşit değil |
| `-gt` | Büyük |
| `-lt` | Küçük |
| `-ge` | Büyük veya eşit |
| `-le` | Küçük veya eşit |

</div>
<div>

### String Karşılaştırma

| Operatör | Anlamı |
|----------|--------|
| `=` | Eşit |
| `!=` | Eşit değil |
| `-z` | Boş string |
| `-n` | Boş değil |

### Mantıksal

| Operatör | Anlamı |
|----------|--------|
| `-a` | AND |
| `-o` | OR |
| `!` | NOT |

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# elif ve Çoklu Koşullar

```bash
#!/bin/bash

if [ "$1" = "hello" ]; then
  echo "hello yourself"
elif [ "$1" = "goodbye" ]; then
  echo "nice to have met you"
  echo "I hope to see you again"
else
  echo "I didn't understand that"
fi
```

<div class="info-box">

### Önemli Noktalar

- `$1` değişkeni **tırnak içinde** → boş olduğunda hata önler
- String karşılaştırması `=` kullanır (`-eq` değil!)
- `elif` = "else if" kısaltması

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# if-then-elif-else Akış Şeması

<div class="diagram-box">

### Bash Koşul Yapısının Akış Şeması

```
        ┌───────┐
        │ START │
        └───┬───┘
            │
            ▼
      ┌─────────────┐
      │ Condition 1? │
      └─────┬───────┘
        TRUE │ FALSE
            ▼
      ┌─────────────┐
      │Execute THEN │
      │   commands   │
      └─────┬───────┘
            │
            ▼
      ┌─────────────┐
      │    fi (end)  │
      └─────┬───────┘
            │
            ▼
        ┌───────┐
        │  END  │
        └───────┘

Condition 1? FALSE path:
      ┌─────────────┐
      │Condition 2?  │
      │    (elif)    │
      └─────┬───────┘
        TRUE │ FALSE
            ▼
      ┌─────────────┐
      │Execute ELIF │
      │   commands   │
      └─────┬───────┘
            │
            ▼
      ┌─────────────┐
      │Execute ELSE │
      │   commands   │
      └─────┬───────┘
            │
            ▼
      ┌─────────────┐
      │    fi (end)  │
      └─────┬───────┘
```

</div>

<div class="highlight-box">

### Örnek: Notlandırma Sistemi

```bash
if [ $score -ge 90 ]; then
    echo "Grade: A"
elif [ $score -ge 70 ]; then
    echo "Grade: B"
elif [ $score -ge 50 ]; then
    echo "Grade: C"
else
    echo "Grade: F"
fi
```

**Akış mantığı:** Yukarıdan aşağıya doğru koşulları kontrol et, ilk doğru olanı çalıştır!

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# case İfadesi

<div class="two-columns">
<div>

```bash
#!/bin/bash

case "$1" in
hello|hi)
  echo "hello yourself"
  ;;
goodbye)
  echo "nice to have met you"
  echo "I hope to see you again"
  ;;
*)
  echo "I didn't understand that"
esac
```

</div>
<div class="highlight-box">

### case Yapısı

- `case EXPRESSION in` → Başlangıç
- `pattern)` → Desen eşleşmesi
- `|` → VEYA (birden fazla desen)
- `;;` → Blok sonu
- `*)` → Varsayılan (else gibi)
- `esac` → case'in tersi (bitiş)

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Döngüler

---

![bg](../gorseller/3_normal_slayt.png)

# for Döngüsü

<div class="two-columns">
<div>

### Temel Yapı

```bash
#!/bin/bash

SERVERS="servera serverb serverc"
for S in $SERVERS; do
  echo "Processing $S"
done
```

### Doğrudan Liste

```bash
for NAME in Sean Jon Isaac David; do
  echo "Hello $NAME"
done
```

</div>
<div class="info-box">

### Dosya Glob ile

```bash
#!/bin/bash

for S in *; do
  echo "Processing $S"
done
```

`*` → Mevcut dizindeki tüm dosyalar

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# while Döngüsü

<div class="two-columns">
<div>

### Temel Yapı

```bash
#!/bin/bash

i=0
while [ $i -lt 10 ]; do
  echo $i
  i=$(( $i + 1 ))
done
echo "Done counting"
```

**Çıktı:** 0, 1, 2, ... 9

</div>
<div class="highlight-box">

### while vs for

| for | while |
|-----|-------|
| Bilinen liste | Bilinmeyen boyut |
| Sonlu koleksiyon | Koşul sağlanana kadar |
| Dosyalar, isimler | Sayaçlar, girdi bekleme |

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Aritmetik İşlemler

<div class="two-columns">
<div>

### $(( )) Sözdizimi

```bash
#!/bin/bash

i=0
while [ $i -lt 10 ]; do
  echo $i
  i=$(( $i + 1 ))
done
```

### Diğer İşlemler

```bash
result=$(( 5 + 3 ))    # Toplama
result=$(( 10 - 4 ))   # Çıkarma
result=$(( 6 * 7 ))    # Çarpma
result=$(( 20 / 4 ))   # Bölme
result=$(( 17 % 5 ))   # Mod
```

</div>
<div class="info-box">

### Kısa Yazımlar

```bash
(( i++ ))     # i = i + 1
(( i-- ))     # i = i - 1
(( i += 5 ))  # i = i + 5
(( i *= 2 ))  # i = i * 2
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Özet: Script Yapısı (1/2)

<div class="two-columns">
<div>

### Shebang ve Değişkenler

```bash
#!/bin/bash
# Yorum satırı

# Değişkenler
NAME="World"
COUNT=5
```

</div>
<div class="info-box">

### Koşullu İfade

```bash
# if kullanımı
if [ -n "$NAME" ]; then
    echo "Name is set"
fi
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Özet: Script Yapısı (2/2)

<div class="two-columns">
<div>

### for Döngüsü

```bash
for i in 1 2 3 4 5; do
    echo "Number: $i"
done
```

</div>
<div class="highlight-box">

### while Döngüsü

```bash
i=0
while [ $i -lt $COUNT ]; do
    echo "Count: $i"
    i=$(( $i + 1 ))
done

exit 0  # Başarılı çıkış
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Özet Tablosu

<div class="two-columns">
<div>

### Değişkenler

| İşlem | Sözdizimi |
|-------|-----------|
| Atama | `VAR="value"` |
| Erişim | `$VAR` veya `${VAR}` |
| Komut çıktısı | `VAR=$(command)` |
| Kullanıcı girdisi | `read VAR` |

</div>
<div>

### Kontrol Yapıları

| Yapı | Kullanım |
|------|----------|
| if/else | Koşullu dallanma |
| case | Çoklu seçenek |
| for | Bilinen liste |
| while | Koşullu tekrar |

</div>
</div>

---

<!-- _class: final-slide -->

# Teşekkürler!

### Sorularınız?

**Bekir Ağırgün**
bekir.agirgun@kapadokya.edu.tr

