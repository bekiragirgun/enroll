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
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 11pt;
  }

  .flow-arrow {
    color: #6B9FE8;
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    margin: 5px 0;
  }
---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Linux'ta Metin Dosyalarıyla Çalışma

<br>
<br>

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# 📖 Giriş

---

![bg](../gorseller/3_normal_slayt.png)

# 📖 Linux'ta Metin Dosyaları

<div class="two-columns">
<div>

### 📄 Metin Dosyalarının Önemi

- Linux sistemlerinde dosyaların büyük çoğunluğu **metin dosyalarıdır**
- Yapılandırma, log ve script dosyaları
- Word benzeri biçimlendirme içermez

</div>
<div>

### 🛠️ Metin İşleme Araçları

- Dosyaları **görüntüleme** komutları
- Dosyaları **değiştirme** komutları
- Çıktı **yönlendirme** özellikleri

</div>
</div>

<div class="highlight-box">

**💡 Önemli:** Shell, komut çıktılarını dosyalara veya başka komutlara yönlendirebilir.

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# 🐱 cat Komutu

---

![bg](../gorseller/3_normal_slayt.png)

# 🐱 cat Komutu

<div class="two-columns">
<div>

### 📋 Temel Kullanım

`cat` (concatenate) komutu:
- Metin dosyalarını **görüntüler**
- Dosyaları **birleştirir**
- Yeni dosyalar **oluşturur**

```bash
$ cat dosya.txt
Dosya içeriği burada görüntülenir.
```

</div>
<div>

### 🔄 Yönlendirme ile Kullanım

```bash
# Dosya içeriğini başka dosyaya
$ cat dosya1.txt > dosya2.txt

# İki dosyayı birleştir
$ cat dosya1.txt dosya2.txt > yeni.txt
```

</div>
</div>

<div class="info-box">

**⚠️ Dikkat:** `cat` küçük dosyalar için idealdir. Büyük dosyalarda ekran hızlı kaydığı için içerik okunamaz.

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# 📄 Pager Komutları

---

![bg](../gorseller/3_normal_slayt.png)

# 📄 Pager Komutları: less ve more

<div class="two-columns">
<div>

### 📖 less Komutu

- **Gelişmiş** sayfalama özelliği
- İleri ve geri **hareket** imkanı
- `man` komutunun varsayılan sayfalayıcısı

```bash
$ less uzun_dosya.txt
```

</div>
<div>

### 📜 more Komutu

- UNIX'in **ilk** sayfalayıcısı
- Daha **basit** özellikler
- Her Linux dağıtımında **mevcut**

```bash
$ more uzun_dosya.txt
```

</div>
</div>

<div class="highlight-box">

**💡 İpucu:** `less` komutu daha fazla özellik sunar: "less is more" (less, more'dan fazlasıdır)

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# ⌨️ Pager Hareket Komutları

<div class="info-box">

| Tuş | İşlev |
|-----|-------|
| **Spacebar** | Bir sayfa ileri |
| **B** | Bir sayfa geri |
| **Enter** | Bir satır ileri |
| **Q** | Çıkış |
| **H** | Yardım menüsü |

</div>

<div class="two-columns">
<div>

### 🔽 İleri Gitme

- `f` veya `Ctrl+F` - Sayfa ileri
- `d` veya `Ctrl+D` - Yarım sayfa ileri
- `j` veya `Enter` - Satır ileri

</div>
<div>

### 🔼 Geri Gitme

- `b` veya `Ctrl+B` - Sayfa geri
- `u` veya `Ctrl+U` - Yarım sayfa geri
- `k` - Satır geri

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 🔍 Pager Arama Komutları

<div class="two-columns">
<div>

### ⬇️ İleri Arama

`/` tuşuna basıp aranacak metni yazın:

```bash
/aranacak_metin
```

Sonraki eşleşme için: `n`
Önceki eşleşme için: `Shift+N`

</div>
<div>

### ⬆️ Geri Arama

`?` tuşuna basıp aranacak metni yazın:

```bash
?aranacak_metin
```

Bulunamadığında:
`Pattern not found`

</div>
</div>

<div class="highlight-box">

**💡 Not:** Arama terimleri aslında **düzenli ifadeler** (regex) kullanır. Bu konuyu ilerleyen bölümlerde detaylı göreceğiz.

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# 📊 head ve tail Komutları

---

![bg](../gorseller/3_normal_slayt.png)

# 📊 head ve tail Komutları

<div class="two-columns">
<div>

### 🔝 head Komutu

Dosyanın **ilk** satırlarını gösterir:

```bash
# Varsayılan: ilk 10 satır
$ head /etc/passwd

# İlk 5 satır
$ head -5 /etc/passwd
$ head -n 5 /etc/passwd
```

</div>
<div>

### 🔚 tail Komutu

Dosyanın **son** satırlarını gösterir:

```bash
# Varsayılan: son 10 satır
$ tail /etc/passwd

# Son 5 satır
$ tail -5 /etc/passwd
```

</div>
</div>

<div class="info-box">

**🔄 Canlı İzleme:** `tail -f log_dosyasi.log` komutu, dosyaya eklenen yeni satırları anlık gösterir. Log takibi için idealdir!

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# 🔗 Pipe Kullanımı

---

![bg](../gorseller/3_normal_slayt.png)

# 🔗 Komut Satırı Pipe'ları

Pipe `|` karakteri, bir komutun çıktısını başka komutun girdisi olarak gönderir.

<div class="two-columns">
<div>

### 📤 Temel Kullanım

```bash
# /etc içeriğini sayfalı göster
$ ls /etc | less

# İlk 10 dosyayı listele
$ ls /etc | head
```

</div>
<div>

### 🔄 Çoklu Pipe

```bash
# Listele, numaralandır, son 5'i al
$ ls /etc/ssh | nl | tail -5
     6  ssh_host_ed25519_key.pub
     7  ssh_host_rsa_key
     8  ssh_host_rsa_key.pub
     9  ssh_import_id
    10  sshd_config
```

</div>
</div>

<div class="highlight-box">

**⚠️ Sıra Önemli:** `ls | nl | tail -5` ile `ls | tail -5 | nl` farklı sonuç verir!

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# 🔀 I/O Yönlendirme

---

![bg](../gorseller/3_normal_slayt.png)

# 🔀 I/O Yönlendirme

<div class="info-box">

| Akış | Kanal | Açıklama |
|------|-------|----------|
| **STDIN** | 0 | Standart girdi (klavye) |
| **STDOUT** | 1 | Standart çıktı (ekran) |
| **STDERR** | 2 | Standart hata (ekran) |

</div>

<div class="two-columns">
<div>

### 📥 Girdi Yönlendirme

`<` karakteri ile dosyadan okuma:

```bash
$ tr 'a-z' 'A-Z' < dosya.txt
```

</div>
<div>

### 📤 Çıktı Yönlendirme

`>` karakteri ile dosyaya yazma:

```bash
$ echo "Merhaba" > dosya.txt
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 📤 STDOUT Yönlendirme

<div class="two-columns">
<div>

### ➡️ Üzerine Yazma `>`

```bash
$ echo "Satır 1" > dosya.txt
$ cat dosya.txt
Satır 1

# Yeni içerik eskisini siler!
$ echo "Yeni satır" > dosya.txt
$ cat dosya.txt
Yeni satır
```

</div>
<div>

### ➕ Ekleme `>>`

```bash
$ echo "Satır 1" > dosya.txt
$ echo "Satır 2" >> dosya.txt
$ cat dosya.txt
Satır 1
Satır 2
```

</div>
</div>

<div class="highlight-box">

**⚠️ Dikkat:** Tek `>` mevcut dosya içeriğini **tamamen siler**! Eklemek için `>>` kullanın.

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# ❌ STDERR Yönlendirme

STDERR (kanal 2) hata mesajlarını yönlendirir:

<div class="two-columns">
<div>

### 🔴 Hata Çıktısı

```bash
$ ls /olmayan_dizin
ls: cannot access '/olmayan_dizin':
No such file or directory

# STDOUT yönlendirmesi hatayı
# yakalamaz!
$ ls /olmayan_dizin > out.txt
ls: cannot access ...
```

</div>
<div>

### 📁 STDERR Dosyaya

```bash
# 2> ile hataları dosyaya yaz
$ ls /olmayan_dizin 2> hata.txt

$ cat hata.txt
ls: cannot access '/olmayan_dizin':
No such file or directory
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 🔀 Çoklu Akış Yönlendirme

<div class="two-columns">
<div>

### 📊 Ayrı Dosyalara

```bash
# STDOUT → output.txt
# STDERR → error.txt
$ ls /etc /fake > output.txt 2> error.txt

$ cat error.txt
ls: cannot access '/fake'...

$ cat output.txt
/etc:
adduser.conf
...
```

</div>
<div>

### 📦 Tek Dosyaya

```bash
# Her iki akışı tek dosyaya
$ ls /etc /fake &> tumu.txt

# veya
$ ls /etc /fake > tumu.txt 2>&1
```

</div>
</div>

<div class="info-box">

**💡 İpucu:** `&>` kısayolu hem STDOUT hem STDERR'ı aynı dosyaya yönlendirir.

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 📥 STDIN Yönlendirme

<div class="two-columns">
<div>

### ⌨️ Klavyeden Girdi

```bash
$ cat
merhaba
merhaba
dünya
dünya
^C  # Ctrl+C ile çıkış
```

`cat` argümansız çağrılırsa STDIN'den (klavye) okur.

</div>
<div>

### 📄 Dosyadan Girdi

```bash
# tr komutu dosya argümanı almaz
$ tr 'a-z' 'A-Z' dosya.txt
tr: extra operand 'dosya.txt'

# < ile dosyadan oku
$ tr 'a-z' 'A-Z' < dosya.txt
MERHABA DÜNYA
```

</div>
</div>

<div class="highlight-box">

**💡 Kombinasyon:** `tr 'a-z' 'A-Z' < girdi.txt > cikti.txt` - Dosyadan oku, dönüştür, dosyaya yaz.

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# 🔤 sort Komutu

---

![bg](../gorseller/3_normal_slayt.png)

# 🔤 sort Komutu

`sort` komutu dosya veya girdiyi sıralar:

<div class="two-columns">
<div>

### 📝 Alfabetik Sıralama

```bash
$ cat isimler.txt
zeynep
ali
mehmet

$ sort isimler.txt
ali
mehmet
zeynep
```

</div>
<div>

### 🔢 Sayısal Sıralama

```bash
$ cat sayilar.txt
10
2
25

$ sort -n sayilar.txt
2
10
25
```

</div>
</div>

<div class="info-box">

**🔄 Ters Sıralama:** `-r` seçeneği sıralamayı tersine çevirir: `sort -r dosya.txt`

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# ⚙️ sort Seçenekleri

<div class="info-box">

| Seçenek | Açıklama |
|---------|----------|
| `-t:` | Alan ayırıcıyı belirle (örn: `:`) |
| `-k3` | 3. alana göre sırala |
| `-n` | Sayısal sıralama |
| `-r` | Ters sıralama |

</div>

<div class="two-columns">
<div>

### 📊 Alan Bazlı Sıralama

```bash
# 3. alana göre sayısal sırala
$ sort -t: -n -k3 /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:...
bin:x:2:2:bin:...
```

</div>
<div>

### 🔄 Çoklu Alan

```bash
# Önce 2. alan, sonra 1. alan
$ sort -t, -k2 -k1n veri.csv
1991,Linux,Torvalds
1987,Minix,Tanenbaum
1970,Unix,Thompson
```

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# 📊 wc ve cut Komutları

---

![bg](../gorseller/3_normal_slayt.png)

# 📊 wc Komutu

`wc` (word count) dosya istatistiklerini gösterir:

<div class="two-columns">
<div>

### 📈 Temel Kullanım

```bash
$ wc /etc/passwd
  35   56  1710  /etc/passwd
```

Çıktı: **satır**, **kelime**, **byte**, dosya adı

</div>
<div>

### ⚙️ Seçenekler

| Seçenek | Gösterir |
|---------|----------|
| `-l` | Satır sayısı |
| `-w` | Kelime sayısı |
| `-c` | Byte sayısı |

</div>
</div>

<div class="highlight-box">

**💡 Pipe ile Kullanım:**
```bash
$ ls /etc | wc -l
142
```
/etc dizinindeki dosya sayısını verir.

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# ✂️ cut Komutu

`cut` komutu dosyadan sütun/alan çıkarır:

<div class="two-columns">
<div>

### 📊 Alan Bazlı

```bash
# : ile ayrılmış 1. ve 7. alanlar
$ cut -d: -f1,7 /etc/passwd
root:/bin/bash
daemon:/usr/sbin/nologin
bin:/usr/sbin/nologin
```

</div>
<div>

### 📏 Karakter Bazlı

```bash
# 1-10 ve 50+ karakterler
$ ls -l | cut -c1-10,50-
drwxr-xr-x Desktop
drwxr-xr-x Documents
-rw-r--r-- dosya.txt
```

</div>
</div>

<div class="info-box">

| Seçenek | Açıklama |
|---------|----------|
| `-d:` | Alan ayırıcı (varsayılan: TAB) |
| `-f1,5-7` | 1, 5, 6, 7. alanları seç |
| `-c1-10` | 1-10 karakterleri seç |

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# 🔍 grep ve Regex

---

![bg](../gorseller/3_normal_slayt.png)

# 🔍 grep Komutu

`grep` komutu dosyada desen arar ve eşleşen satırları gösterir:

<div class="two-columns">
<div>

### 📝 Temel Kullanım

```bash
$ grep bash /etc/passwd
root:x:0:0:root:/root:/bin/bash
sysadmin:x:1001:...:/bin/bash

# Renkli çıktı
$ grep --color bash /etc/passwd
```

</div>
<div>

### ⚙️ Seçenekler

| Seçenek | İşlev |
|---------|-------|
| `-c` | Eşleşen satır sayısı |
| `-n` | Satır numarası göster |
| `-v` | Eşleşmeyenleri göster |
| `-i` | Büyük/küçük harf ayrımı yapma |
| `-w` | Tam kelime eşleşmesi |

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 🎯 Temel Düzenli İfadeler (Regex)

Düzenli ifadeler, metin desenleri tanımlamak için kullanılır:

<div class="info-box">

| Karakter | Anlamı |
|----------|--------|
| `.` | Herhangi tek karakter |
| `[ ]` | Karakter listesi/aralığı |
| `*` | Önceki karakter 0+ kez |
| `^` | Satır başı |
| `$` | Satır sonu |
| `\` | Özel karakteri escape et |

</div>

<div class="highlight-box">

**💡 İpucu:** Regex desenlerini tek tırnak içine alın: `grep 'desen' dosya`

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 🔘 Nokta Karakteri `.`

Nokta `.` karakteri, yeni satır hariç **herhangi bir karakterle** eşleşir:

<div class="two-columns">
<div>

### 📝 Örnek Kullanım

```bash
$ cat red.txt
red
reef
rot
rod
roof
root
```

</div>
<div>

### 🔍 Desen Arama

```bash
# r + 2 karakter + f
$ grep 'r..f' red.txt
reef
roof

# r + 2 karakter + t
$ grep 'r..t' red.txt
root
```

</div>
</div>

<div class="info-box">

**💡 Minimum Karakter:** `grep '....' dosya.txt` - En az 4 karakterli satırları bulur.

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 📦 Köşeli Parantez `[ ]`

Köşeli parantez içindeki karakterlerden **biriyle** eşleşir:

<div class="two-columns">
<div>

### 📊 Karakter Listesi

```bash
# Rakam içeren satırlar
$ grep '[0-9]' profile.txt
I am 37 years old.
3121991
I have 2 dogs.
```

</div>
<div>

### 🚫 Olumsuzlama

```bash
# Rakam içerMEYEN karakterler
$ grep '[^0-9]' profile.txt
Hello my name is Joe.
I am 37 years old.
My favorite food is avocados.
```

</div>
</div>

<div class="highlight-box">

**📝 Aralık Örnekleri:** `[a-z]` küçük harf, `[A-Z]` büyük harf, `[a-zA-Z0-9]` alfanümerik

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# ⭐ Yıldız Karakteri `*`

Yıldız `*` önceki karakterin **0 veya daha fazla** tekrarıyla eşleşir:

<div class="two-columns">
<div>

### 📝 Temel Kullanım

```bash
$ grep 're*d' red.txt
red    # 1 adet e
reeed  # 3 adet e
rd     # 0 adet e
reed   # 2 adet e
```

</div>
<div>

### 📦 Liste ile

```bash
# o veya e, 0+ kez
$ grep 'r[oe]*d' red.txt
red
reeed
rd
rod
reed
```

</div>
</div>

<div class="info-box">

**⚠️ Dikkat:** `e*` tüm satırlarla eşleşir çünkü "0 kez e" her yerde geçerlidir. `ee*` kullanarak "en az 1 e" arayın.

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# ⚓ Çapa ve Diğer Özel Karakterler

<div class="two-columns">
<div>

### 🔝 Satır Başı `^`

```bash
# root ile BAŞLAYAN satırlar
$ grep '^root' /etc/passwd
root:x:0:0:root:/root:/bin/bash
```

### 🔚 Satır Sonu `$`

```bash
# r ile BİTEN satırlar
$ grep 'r$' alpha.txt
B is for Bear
F is for Flower
```

</div>
<div>

### 🔙 Escape `\`

```bash
# Gerçek * karakterini ara
$ grep 're\*' dosya.txt
**Beware** of the ghost...
```

### ➕ Genişletilmiş Regex

```bash
# ? (0 veya 1 kez)
$ grep -E 'colou?r' dosya.txt

# + (1 veya daha fazla)
$ grep -E 'e+' dosya.txt

# | (veya)
$ grep -E 'gray|grey' dosya.txt
```

</div>
</div>

---

<!-- _class: final-slide -->

# Teşekkürler!

## Linux'ta Metin İşleme Komutları

**📧 İletişim:** bekir.agirgun@kapadokya.edu.tr

**🌐 Web:** www.kapadokya.edu.tr
