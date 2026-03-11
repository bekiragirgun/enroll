---
marp: true
theme: default
paginate: true
lang: tr
backgroundColor: #F7F7F7
style: |
  section {
    font-family: 'Trebuchet MS', Arial, sans-serif;
    font-size: 90%;
    padding: 85px 50px 30px 50px;
    background-color: #F7F7F7;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    position: relative;
  }

  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
    position: absolute;
    bottom: 10px;
    right: 30px;
    color: #666;
    font-size: 12pt;
    pointer-events: none;
    z-index: 1;
  }

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
    margin-top: 20px;
    margin-bottom: 10px;
  }

  h3 {
    color: #2D4A7C;
    font-size: 15pt;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 8px;
  }

  p, li {
    font-size: 13pt;
    line-height: 1.5;
    color: #333;
  }

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

  section.cover-slide::after {
    content: none;
  }

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

  section.topic-slide::after {
    content: none;
  }

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

  section.final-slide h1 {
    color: white !important;
    margin-left: 0;
  }

  section.final-slide::after {
    content: none;
  }

  .two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-top: 20px;
  }

  .info-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .info-box h3 { color: white; margin-top: 0; }

  .highlight-box {
    background: linear-gradient(135deg, #6B9FE8 0%, #4A7FB8 100%);
    color: white;
    padding: 14px;
    border-radius: 12px;
    margin: 15px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .highlight-box h3 { color: white; margin-top: 0; }

  .compare-box {
    background: #f0f4f8;
    padding: 12px;
    border-radius: 10px;
    border-left: 4px solid #6B9FE8;
  }

  .warning-box {
    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
    color: #333;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .warning-box h3 { color: #333; margin-top: 0; }

  .success-box {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .success-box h3 { color: white; margin-top: 0; }

  td {
    color: #333 !important;
    background-color: white !important;
  }

  th {
    background-color: #2D4A7C;
    color: white;
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
    padding: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  }

  pre code {
    background: none;
    padding: 0;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 11pt;
    line-height: 1.4;
  }
---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Özel Dizinler ve Dosyalar

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Giriş

---

![bg](../gorseller/3_normal_slayt.png)
# Giriş

<div class="two-columns">
<div>

### Özel İzinler Neden Gerekli?

- Temel izinler (rwx) çoğu durumda yeterlidir
- Ancak birden fazla kullanıcı aynı dosyalar üzerinde çalışırken yetersiz kalabilir
- **Özel izinler** bu sorunları çözmek için tasarlanmıştır

### Bu Bölümde Öğrenecekleriniz

- Setuid (SUID) izni
- Setgid (SGID) izni
- Sticky Bit izni
- Hard ve Symbolic linkler

</div>
<div class="info-box">

### 🔐 Üç Özel İzin

| İzin | Amaç |
|------|------|
| **setuid** | Program sahibi olarak çalıştır |
| **setgid** | Grup sahibi olarak çalıştır |
| **sticky bit** | Silme işlemini kısıtla |

Bu izinler dosya ve dizinlere uygulanabilir.

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Setuid (SUID)

---

![bg](../gorseller/3_normal_slayt.png)
# Setuid Nedir?

<div class="two-columns">
<div>

### Tanım

- Setuid **çalıştırılabilir dosyalara** uygulanır
- Program, çalıştıran kullanıcı olarak değil **dosya sahibi** olarak çalışır
- Normal kullanıcıların root yetkisi gerektiren işlemleri yapmasını sağlar

### Neden Gerekli?

`/etc/shadow` dosyasına normal kullanıcı erişemez:

```bash
$ more /etc/shadow
Permission denied
$ ls -l /etc/shadow
-rw-r----- 1 root root 5195 ...
```

</div>
<div class="highlight-box">

### 💡 passwd Komutu Örneği

`passwd` komutu `/etc/shadow` dosyasını değiştirir - ama nasıl?

```bash
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root ...
```

**s** harfi setuid iznini gösterir!

Kullanıcı `passwd` çalıştırdığında, komut **root** olarak çalışır.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Setuid İzin Gösterimi

### ls -l Çıktısında Setuid

```bash
-rwsr-xr-x 1 root root 31768 Jan 28 2010 /usr/bin/passwd
```

<div class="two-columns">
<div class="compare-box">

| Gösterim | Anlam |
|----------|-------|
| **s** (küçük) | setuid + execute aktif |
| **S** (büyük) | setuid aktif, execute YOK |

Küçük `s` = İkisi de var ✓
Büyük `S` = Sadece setuid (sorunlu)

</div>
<div class="warning-box">

### ⚠️ Büyük S Uyarısı

Büyük **S** görürseniz, setuid ayarlanmış ama execute izni eksik demektir.

Bu durumda setuid **çalışmaz**!

Execute iznini de eklemeniz gerekir.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Setuid Ayarlama

<div class="two-columns">
<div>

### Sembolik Yöntem

**Eklemek için:**
```bash
chmod u+s dosya
```

**Kaldırmak için:**
```bash
chmod u-s dosya
```

### Sayısal Yöntem

**Eklemek için:** (4000 ekle)
```bash
chmod 4775 dosya
```

**Kaldırmak için:**
```bash
chmod 0775 dosya
```

</div>
<div class="info-box">

### 🔢 Özel İzin Numaraları

| Değer | İzin |
|-------|------|
| **4000** | setuid |
| **2000** | setgid |
| **1000** | sticky bit |

3 haneli izin kullanılırsa, ilk hane 0 kabul edilir.

4 hane belirtilmelidir: `chmod 4755 dosya`

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Setgid (SGID)

---

![bg](../gorseller/3_normal_slayt.png)
# Setgid Nedir?

<div class="two-columns">
<div>

### İki Farklı Davranış

**Dosyalarda:**
- Setuid'e benzer
- Program **grup sahibi** yetkileriyle çalışır

**Dizinlerde:**
- Dizinde oluşturulan dosyalar **dizinin grubuna** ait olur
- Alt dizinler de setgid miras alır

</div>
<div class="highlight-box">

### 📁 Örnek: wall Komutu

```bash
$ ls -l /usr/bin/wall
-rwxr-sr-x 1 root tty 30800 ...
```

**s** grup execute konumunda = setgid

wall komutu `tty` grubu yetkisiyle çalışır ve terminallere yazabilir.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Dosyalarda Setgid

### wall Komutu Nasıl Çalışır?

```bash
$ ls -l /dev/tty?
crw--w---- 1 root tty 4, 0 ... /dev/tty0
crw--w---- 1 root tty 4, 1 ... /dev/tty1
```

<div class="two-columns">
<div class="compare-box">

### Terminal Dosyaları

- `/dev/tty*` dosyaları **tty** grubuna ait
- Sadece grup üyeleri yazabilir
- "Others" için izin yok

</div>
<div class="info-box">

### 🔑 Setgid Etkisi

`wall` komutu setgid ile tty grubuna geçici üyelik kazanır.

Bu sayede terminallere mesaj yazabilir.

Setgid olmadan `wall` başarısız olurdu!

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Dizinlerde Setgid

### Ortak Çalışma Senaryosu

<div class="two-columns">
<div>

**Problem:**
- bob, sue, tim aynı projede çalışıyor
- bob dosya oluşturuyor → grup: `payroll`
- sue ve tim bu dosyaya erişemiyor!

**Çözüm:** Setgid dizini

```bash
$ ls -ld /tmp/data
drwxrwsrwx 2 root demo ...
```

Artık herkes dosya oluşturursa grup **demo** olur.

</div>
<div class="success-box">

### ✓ Setgid Dizin Avantajı

```bash
# bob dosya oluşturur
$ touch /tmp/data/file.txt
$ ls -l /tmp/data/file.txt
-rw-rw-r-- 1 bob demo ...
```

Grup otomatik olarak **demo** oldu!

sue ve tim artık erişebilir.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Setgid Ayarlama

<div class="two-columns">
<div>

### Sembolik Yöntem

**Eklemek için:**
```bash
chmod g+s dizin
```

**Kaldırmak için:**
```bash
chmod g-s dizin
```

### Sayısal Yöntem

**Eklemek için:** (2000 ekle)
```bash
chmod 2775 dizin
```

**Kaldırmak için:**
```bash
chmod 0775 dizin
```

</div>
<div class="compare-box">

### Setgid Gösterimi

| Gösterim | Anlam |
|----------|-------|
| **s** (küçük) | setgid + execute aktif |
| **S** (büyük) | setgid aktif, execute YOK |

```bash
drwxrwsrwx  # s = Her ikisi de var
drwxrwSr-x  # S = Execute yok (sorunlu)
```

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Sticky Bit

---

![bg](../gorseller/3_normal_slayt.png)
# Sticky Bit Nedir?

<div class="two-columns">
<div>

### Amaç

- Paylaşılan dizinlerde **dosya silmeyi kısıtlar**
- Yazma izni olan herkes dosya oluşturabilir
- Ama sadece **dosya sahibi** veya **root** silebilir

### Kullanım Alanları

- `/tmp` dizini
- `/var/tmp` dizini
- Herkesin yazabildiği paylaşılan dizinler

</div>
<div class="warning-box">

### ⚠️ Sticky Bit Olmadan

Yazma iznine sahip **herkes** dizindeki **tüm dosyaları** silebilir!

Bu büyük bir güvenlik sorunudur.

```bash
# Sticky bit bu sorunu çözer
$ ls -ld /tmp
drwxrwxrwt 1 root root ...
```

**t** harfi sticky bit'i gösterir.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Sticky Bit Gösterimi ve Ayarlama

<div class="two-columns">
<div>

### ls -l Çıktısında

```bash
$ ls -ld /tmp
drwxrwxrwt 1 root root 4096 ...
```

| Gösterim | Anlam |
|----------|-------|
| **t** (küçük) | sticky + execute aktif |
| **T** (büyük) | sticky aktif, execute YOK |

**T** durumunda grup execute varsa sorun yok.

</div>
<div>

### Ayarlama Komutları

**Sembolik:**
```bash
chmod o+t dizin   # Ekle
chmod o-t dizin   # Kaldır
```

**Sayısal:** (1000 ekle/çıkar)
```bash
chmod 1777 dizin  # Ekle
chmod 0777 dizin  # Kaldır
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Özel İzinler Özeti

<div class="compare-box">

| İzin | Değer | Sembolik | Uygulama | Etki |
|------|-------|----------|----------|------|
| **setuid** | 4000 | `u+s` | Dosya | Sahip olarak çalıştır |
| **setgid** | 2000 | `g+s` | Dosya | Grup olarak çalıştır |
| **setgid** | 2000 | `g+s` | Dizin | Dosyalar dizin grubuna ait |
| **sticky** | 1000 | `o+t` | Dizin | Sadece sahip silebilir |

</div>

<div class="info-box">

### 🔢 Birleşik Örnek

```bash
chmod 4755 program    # setuid + rwxr-xr-x
chmod 2775 paylaşım   # setgid + rwxrwxr-x
chmod 1777 /tmp       # sticky + rwxrwxrwx
```

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Linkler (Bağlantılar)

---

![bg](../gorseller/3_normal_slayt.png)
# Linkler Neden Kullanılır?

<div class="two-columns">
<div>

### Problem Senaryosu

Derin bir dizindeki dosyaya sürekli erişmeniz gerekiyor:

```
/usr/share/doc/package/
  data/2013/october/
    valuable-info.txt
```

Bu yolu her seferinde yazmak zor!

### Çözüm: Link Oluştur

Ana dizininizde bir link oluşturun, asıl dosyaya bu link üzerinden erişin.

</div>
<div class="highlight-box">

### 🔗 İki Link Türü

**Hard Link (Sabit Bağ)**
- Aynı inode'a işaret eder
- Dosya kopyası gibi davranır
- Orijinal silinse bile veri kalır

**Symbolic Link (Sembolik Bağ)**
- Dosya yoluna işaret eder
- Kısayol gibi davranır
- Orijinal silinirse bozulur

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Inode Kavramı

<div class="two-columns">
<div>

### Inode Nedir?

- Her dosyanın benzersiz **inode numarası** vardır
- Inode tablosu dosya meta verilerini içerir:
  - İzinler
  - Sahiplik
  - Zaman damgaları
  - Veri blok işaretçileri

**Dosya adı inode'da değildir!**

</div>
<div class="compare-box">

### Dizin İçeriği Örneği

| Dosya Adı | Inode No |
|-----------|----------|
| passwd | 123 |
| shadow | 175 |
| group | 144 |

Sistem dosya adını inode numarasına çevirir, sonra veriye erişir.

```bash
$ ls -i /tmp/file.txt
215220874 /tmp/file.txt
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Hard Link Oluşturma

### ln Komutu

```bash
ln hedef link_adı
```

<div class="two-columns">
<div>

### Örnek

```bash
$ echo "veri" > file.original
$ ls -li file.original
278772 -rw-rw-r-- 1 sysadmin ...

$ ln file.original file.hard.1
$ ls -li file.*
278772 -rw-rw-r-- 2 sysadmin ... file.hard.1
278772 -rw-rw-r-- 2 sysadmin ... file.original
```

Aynı inode (278772), link sayısı 2 oldu.

</div>
<div class="info-box">

### 🔢 Link Sayısı

`ls -l` çıktısındaki izinlerden sonraki sayı **link sayısıdır**.

```
-rw-rw-r-- 2 ...
           ^
           Link sayısı
```

Her hard link bu sayıyı 1 artırır.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Symbolic Link Oluşturma

### ln -s Komutu

```bash
ln -s hedef link_adı
```

<div class="two-columns">
<div>

### Örnek

```bash
$ ln -s /etc/passwd mypasswd
$ ls -l mypasswd
lrwxrwxrwx 1 sysadmin ... mypasswd -> /etc/passwd
```

**l** = link türü dosya
**->** = hedef dosyayı gösterir

</div>
<div class="highlight-box">

### 💡 Symbolic Link Özellikleri

- Dosya türü `l` ile başlar
- Hedef yolu açıkça gösterilir
- Hedef silinirse link **bozulur**
- Farklı dosya sistemlerine link verilebilir
- Dizinlere link verilebilir

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Hard vs Symbolic Link Karşılaştırma

<div class="compare-box">

| Özellik | Hard Link | Symbolic Link |
|---------|-----------|---------------|
| **Hedef silinirse** | Veri kalır ✓ | Link bozulur ✗ |
| **Görünürlük** | Zor (find gerekir) | Kolay (ls gösterir) |
| **Farklı dosya sistemi** | Hayır ✗ | Evet ✓ |
| **Dizinlere link** | Hayır ✗ | Evet ✓ |
| **Inode** | Aynı inode | Farklı inode |

</div>

<div class="warning-box">

### ⚠️ Hard Link Kısıtlamaları

```bash
$ ln /boot/vmlinuz Linux.Kernel
ln: Invalid cross-device link    # Farklı dosya sistemi!

$ ln /bin binary
ln: hard link not allowed for directory    # Dizin!
```

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Hard Link Avantajı: Tek Başarısızlık Noktası Yok

<div class="two-columns">
<div>

### Hard Link

5 hard link varsa, 4'ünü silseniz bile veri **kaybolmaz**.

Inode en az 1 dosya adına bağlı kaldığı sürece veri güvende.

</div>
<div>

### Symbolic Link - Kırılabilir

```bash
$ ls -l mytest.txt
lrwxrwx... mytest.txt -> test.txt

$ more mytest.txt
hi there

$ rm test.txt    # Orijinal silindi!

$ more mytest.txt
No such file or directory
```

</div>
</div>

<div class="success-box">

### ✓ Hard Link ile veri koruması sağlanır, Symbolic Link ile esneklik kazanılır.

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Symbolic Link Avantajları

<div class="two-columns">
<div>

### 1. Görünürlük

Hard link bulmak için `find` gerekir:

```bash
$ ls -i file.original
278772 file.original

$ find / -inum 278772
/home/sysadmin/file.hard.1
/home/sysadmin/file.original
```

Symbolic link `ls -l` ile hemen görünür.

</div>
<div>

### 2. Esneklik

**Farklı dosya sistemine link:**
```bash
$ ln -s /boot/vmlinuz Linux.Kernel
# Çalışır!
```

**Dizine link:**
```bash
$ ln -s /bin binary
$ ls -l binary
lrwxrwx... binary -> /bin
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Özet

<div class="two-columns">
<div>

### Özel İzinler

| İzin | Komut | Etki |
|------|-------|------|
| setuid | `chmod u+s` / `4xxx` | Sahip olarak çalıştır |
| setgid | `chmod g+s` / `2xxx` | Grup olarak çalıştır |
| sticky | `chmod o+t` / `1xxx` | Sadece sahip silebilir |

### Link Komutları

| Komut | İşlev |
|-------|-------|
| `ln hedef link` | Hard link |
| `ln -s hedef link` | Symbolic link |
| `ls -i` | Inode görüntüle |

</div>
<div class="info-box">

### 🎯 Hatırlanacak Noktalar

1. **setuid** → `s` user execute konumunda
2. **setgid** → `s` group execute konumunda
3. **sticky** → `t` others execute konumunda
4. Büyük harf (**S**,**T**) = execute eksik
5. Hard link = Aynı inode, güvenli
6. Soft link = Esnek, kırılabilir

</div>
</div>

---

<!-- _class: final-slide -->

# Teşekkürler!
