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
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .info-box h3 { color: white; margin-top: 0; }

  .highlight-box {
    background: linear-gradient(135deg, #6B9FE8 0%, #4A7FB8 100%);
    color: white;
    padding: 18px;
    border-radius: 12px;
    margin: 15px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .highlight-box h3 { color: white; margin-top: 0; }

  .compare-box {
    background: #f0f4f8;
    padding: 15px;
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

# Dosya Sahipliği ve İzinler

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

### Dosya Güvenliği

- Dosya sahipliği, dosya güvenliği için kritik öneme sahiptir
- Her dosyanın bir **kullanıcı sahibi** ve bir **grup sahibi** vardır
- İzinler, dosya ve dizinlere erişimi kontrol eder

### Bu Bölümde Öğrenecekleriniz

- Dosya sahipliğini belirleme ve değiştirme
- İzin kavramları ve türleri
- İzinleri değiştirme yöntemleri
- Varsayılan izinler (umask)

</div>
<div class="info-box">

### 🔐 Neden Önemli?

Linux çok kullanıcılı bir işletim sistemidir. Dosya sahipliği ve izinler:

- Verilerin yetkisiz erişimden korunmasını sağlar
- Kullanıcı eylemlerini sınırlar
- Sistem bütünlüğünü korur

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Dosya Sahipliği

---

![bg](../gorseller/3_normal_slayt.png)
# Dosya Sahipliği

<div class="two-columns">
<div>

### Kullanıcı ve Grup Sahipliği

- Kullanıcılar varsayılan olarak oluşturdukları dosyaların sahibidir
- Her dosyanın bir **kullanıcı sahibi** ve bir **grup sahibi** vardır
- Sahiplik UID ve GID ile ilişkilendirilir

### Varsayılan Davranış

- Yeni dosyanın kullanıcı sahibi: Dosyayı oluşturan kullanıcı
- Yeni dosyanın grup sahibi: Kullanıcının birincil grubu

</div>
<div class="highlight-box">

### 💡 UID ve GID

- **UID:** User ID (Kullanıcı Kimliği)
- **GID:** Group ID (Grup Kimliği)

İşletim sistemi sahipliği isim değil, bu numaralar üzerinden takip eder.

Kullanıcı silinirse, dosya "sahipsiz" kalır ve UID numarası gösterilir.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# id Komutu

### Kullanıcı Kimlik Bilgilerini Görüntüleme

`id` komutu mevcut kullanıcının kimlik bilgilerini gösterir:

```bash
sysadmin@localhost:~$ id
uid=1001(sysadmin) gid=1001(sysadmin) groups=1001(sysadmin),4(adm),27(sudo),1005(research),1006(development)
```

<div class="two-columns">
<div class="compare-box">

| Alan | Açıklama |
|------|----------|
| `uid=1001(sysadmin)` | Kullanıcı ID ve adı |
| `gid=1001(sysadmin)` | Birincil Grup ID ve adı |
| `groups=...` | Tüm grup üyelikleri |

</div>
<div class="info-box">

### 🔑 UPG (User Private Group)

UID ve GID aynıysa, kullanıcı **User Private Group** içindedir.

Bu, her kullanıcının kendi özel grubuna sahip olduğu anlamına gelir.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Dosya Sahipliğini Görüntüleme

### ls -l Komutu ile Sahiplik Bilgisi

```bash
sysadmin@localhost:~$ touch /tmp/filetest1
sysadmin@localhost:~$ ls -l /tmp/filetest1
-rw-rw-r--. 1 sysadmin sysadmin 0 Oct 21 10:18 /tmp/filetest1
```

<div class="compare-box">

| Bileşen | Açıklama |
|---------|----------|
| `-rw-rw-r--` | İzinler |
| `1` | Bağlantı sayısı |
| `sysadmin` (ilk) | **Kullanıcı sahibi** |
| `sysadmin` (ikinci) | **Grup sahibi** |
| `0` | Dosya boyutu |
| `Oct 21 10:18` | Son değişiklik tarihi |
| `/tmp/filetest1` | Dosya yolu |

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Grup Değiştirme

---

![bg](../gorseller/3_normal_slayt.png)
# Grup Değiştirme (newgrp)

<div class="two-columns">
<div>

### newgrp Komutu

Yeni dosyaların farklı bir gruba ait olmasını istiyorsanız, `newgrp` komutu ile birincil grubu değiştirebilirsiniz.

```bash
newgrp grup_adı
```

### groups Komutu

Hangi gruplara ait olduğunuzu gösterir:

```bash
sysadmin@localhost:~$ groups
sysadmin adm sudo research development
```

</div>
<div class="info-box">

### 📝 Örnek Kullanım

```bash
# Mevcut grup bilgisi
$ id
gid=1001(sysadmin)...

# Grup değiştir
$ newgrp research

# Yeni grup bilgisi
$ id
gid=1005(research)...
```

Artık oluşturulan dosyalar `research` grubuna ait olacak.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# newgrp Kullanımı

### Adım Adım Örnek

```bash
# 1. Başlangıç durumu
sysadmin@localhost:~$ id
uid=1001(sysadmin) gid=1001(sysadmin) groups=...

# 2. Birincil grubu değiştir
sysadmin@localhost:~$ newgrp research

# 3. Yeni durumu doğrula
sysadmin@localhost:~$ id
uid=1001(sysadmin) gid=1005(research) groups=...

# 4. Dosya oluştur
sysadmin@localhost:~$ touch /tmp/filetest2
sysadmin@localhost:~$ ls -l /tmp/filetest2
-rw-r--r--. 1 sysadmin research 0 Oct 21 10:53 /tmp/filetest2
```

<div class="warning-box">

### ⚠️ Önemli Not

`newgrp` yeni bir kabuk açar. Orijinal gruba dönmek için `exit` yazın.

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Grup Sahipliğini Değiştirme

---

![bg](../gorseller/3_normal_slayt.png)
# chgrp Komutu

<div class="two-columns">
<div>

### Sözdizimi

```bash
chgrp grup_adı dosya
```

### Örnek Kullanım

```bash
# Dosya oluştur
$ touch sample
$ ls -l sample
-rw-rw-r-- 1 sysadmin sysadmin ...

# Grup sahipliğini değiştir
$ chgrp research sample
$ ls -l sample
-rw-rw-r-- 1 sysadmin research ...
```

</div>
<div class="highlight-box">

### 🔑 Kurallar

- **root:** Herhangi bir dosyanın grubunu herhangi bir gruba değiştirebilir
- **Normal kullanıcı:** Sadece kendi dosyalarının grubunu, üyesi olduğu bir gruba değiştirebilir

```bash
# Başkasının dosyasında hata
$ chgrp development /etc/passwd
chgrp: Operation not permitted
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Özyinelemeli Grup Değişikliği

### -R Seçeneği

Bir dizin ve içindeki tüm dosya/alt dizinlerin grup sahipliğini değiştirmek için:

```bash
chgrp -R grup_adı dizin
```

### Örnek

```bash
sysadmin@localhost:~$ chgrp -R development test_dir
```

<div class="info-box">

### 📊 stat Komutu

Detaylı dosya bilgisi için `stat` komutunu kullanabilirsiniz:

```bash
$ stat /tmp/filetest1
  File: `/tmp/filetest1'
  Access: (0664/-rw-rw-r--)  Uid: (1001/sysadmin)  Gid: (1001/sysadmin)
```

Hem sayısal hem sembolik izinleri gösterir.

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Kullanıcı Sahipliğini Değiştirme

---

![bg](../gorseller/3_normal_slayt.png)
# chown Komutu

<div class="two-columns">
<div>

### Üç Kullanım Şekli

**1. Sadece kullanıcı değiştir:**
```bash
chown kullanıcı dosya
```

**2. Hem kullanıcı hem grup:**
```bash
chown kullanıcı:grup dosya
chown kullanıcı.grup dosya
```

**3. Sadece grup değiştir:**
```bash
chown :grup dosya
chown .grup dosya
```

</div>
<div class="warning-box">

### ⚠️ Yetki Gereksinimi

- **Kullanıcı sahipliği değiştirme:** Sadece root yapabilir
- **Grup sahipliği değiştirme:** Dosya sahibi veya root yapabilir

Normal kullanıcılar başkasına dosya "veremez"!

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# chown Örnekleri

### Kullanıcı Değiştirme (root yetkisi gerekir)

```bash
root@localhost:~# chown jane /tmp/filetest1
root@localhost:~# ls -l /tmp/filetest1
-rw-rw-r-- 1 jane sysadmin 0 Dec 19 18:44 /tmp/filetest1
```

### Hem Kullanıcı Hem Grup Değiştirme

```bash
root@localhost:~# chown jane:users /tmp/filetest2
root@localhost:~# ls -l /tmp/filetest2
-rw-r--r-- 1 jane users 0 Dec 19 18:53 /tmp/filetest2
```

### Sadece Grup Değiştirme (normal kullanıcı yapabilir)

```bash
jane@localhost:~$ chown .users /tmp/filetest1
jane@localhost:~$ ls -l /tmp/filetest1
-rw-rw-r-- 1 jane users 0 Dec 19 18:44 /tmp/filetest1
```

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# İzinler (Permissions)

---

![bg](../gorseller/3_normal_slayt.png)
# İzin Yapısı

### ls -l Çıktısının İlk 10 Karakteri

```bash
-rw-r--r--. 1 root root 4135 May 27 21:08 /etc/passwd
```

<div class="two-columns">
<div>

### Dosya Türü (1. karakter)

| Karakter | Tür |
|----------|-----|
| `-` | Normal dosya |
| `d` | Dizin |
| `l` | Sembolik bağlantı |
| `b` | Blok cihaz |
| `c` | Karakter cihaz |
| `p` | Pipe |
| `s` | Soket |

</div>
<div class="info-box">

### 🔐 İzin Grupları (2-10. karakterler)

```
-rw-r--r--
 ├─┘├─┘├─┘
 │  │  └── Others (diğerleri)
 │  └───── Group (grup)
 └──────── User (kullanıcı)
```

Her grup 3 karakter: **r** (read), **w** (write), **x** (execute)

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# İzin Türleri

<div class="two-columns">
<div>

### Dosyalar İçin

| İzin | Anlam |
|------|-------|
| **r** (read) | Dosya içeriğini okuma |
| **w** (write) | Dosya içeriğini değiştirme |
| **x** (execute) | Dosyayı çalıştırma |

### Dizinler İçin

| İzin | Anlam |
|------|-------|
| **r** | Dizin içeriğini listeleme (`ls`) |
| **w** | Dosya ekleme/silme |
| **x** | Dizine girme (`cd`) |

</div>
<div class="warning-box">

### ⚠️ Kritik Notlar

**Dosyalar için:**
- `w` izni düzgün çalışması için `r` izni gerektirir

**Dizinler için:**
- `w` izni düzgün çalışması için `x` izni gerektirir
- `r` olmadan `ls` yapılamaz
- `x` olmadan dizine girilemez

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# İzin Grupları Detay

### Kullanıcı, Grup ve Diğerleri

```
-rw-r--r-- 1 root root 4135 May 27 21:08 /etc/passwd
```

<div class="compare-box">

| Konum | Karakterler | Açıklama |
|-------|-------------|----------|
| 2-4 | `rw-` | **User Owner** - Dosya sahibinin izinleri |
| 5-7 | `r--` | **Group Owner** - Grup üyelerinin izinleri |
| 8-10 | `r--` | **Others** - Diğer herkesin izinleri |

</div>

<div class="info-box">

### 🔑 İzin Kontrolü Sırası

1. Dosya sahibiyseniz → Kullanıcı izinleri uygulanır
2. Grup üyesiyseniz → Grup izinleri uygulanır
3. Hiçbiri değilseniz → Others izinleri uygulanır

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# İzinleri Anlama

---

![bg](../gorseller/3_normal_slayt.png)
# Senaryo 1: Dizin Erişimi

### Soru: bob kullanıcısı abc.txt dosyasına erişebilir mi?

```
drwxr-xr-x. 17 root root 4096 23:38 /
drwxr-xr--. 10 root root 128  03:38 /data
-rwxr-xr--.  1 bob  bob  100  21:08 /data/abc.txt
```

<div class="two-columns">
<div class="warning-box">

### ❌ Cevap: HAYIR

bob kullanıcısı `/data` dizininde "others" grubundadır.

Others izinleri: `r--`

**x izni yok** = dizine giremez!

</div>
<div class="highlight-box">

### 📚 Ders

Bir dosyaya erişmek için **tüm üst dizinlerde x izni** gerekir!

Dosya izinlerinden önce dizin izinleri kontrol edilir.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Senaryo 2: Dizin İçeriğini Listeleme

### Soru: Kim `/data` dizinini listeleyebilir (ls /data)?

```
drwxr-xr-x. 17 root root 4096 23:38 /
drwxr-xr--. 10 root root 128  03:38 /data
```

<div class="two-columns">
<div class="info-box">

### ✅ Cevap: Herkes

Dizin içeriğini listelemek için sadece **r** izni gerekir.

Tüm kullanıcılar `/data` üzerinde `r` iznine sahip.

</div>
<div class="highlight-box">

### 📚 Ders

- `r` → Dizin içeriğini listeleme
- `ls -l` için hem `r` hem `x` gerekir
- Sadece `r` ile `ls` çalışır ama `ls -l` çalışmaz

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Senaryo 3: Dosya Silme

### Soru: Kim `/data/abc.txt` dosyasını silebilir?

```
drwxr-xr-x. 17 root root 4096 23:38 /
drwxrw-rw-. 10 root root 128  03:38 /data
-rwxr-xr--.  1 bob  bob  100  21:08 /data/abc.txt
```

<div class="two-columns">
<div class="warning-box">

### Cevap: Sadece root

Dosya silmek için dizinde `w` **ve** `x` izni gerekir.

Herkes `w` iznine sahip AMA sadece root `x` iznine sahip.

</div>
<div class="highlight-box">

### 📚 Ders

Dosya silmek için dosya üzerinde izin gerekmez!

Dizin üzerinde **w + x** izni gerekir.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Senaryo 4: İzin Önceliği

### Soru: bob `more /data/abc.txt` çalıştırabilir mi?

```
drwxr-xr-x. 17 root root 4096 23:38 /
dr-xr-x---. 10 bob  bob  128  03:38 /data
----rw-rwx.  1 bob  bob  100  21:08 /data/abc.txt
```

<div class="two-columns">
<div class="warning-box">

### ❌ Cevap: HAYIR

bob dosyanın sahibi, bu yüzden **sadece kullanıcı izinleri** uygulanır.

Kullanıcı izinleri: `---`

Grup ve others daha fazla izne sahip olsa bile fayda etmez!

</div>
<div class="highlight-box">

### 📚 Ders

Sahip izinleri her zaman önceliklidir.

Gruba ve others'a verilen izinler sahip için geçerli değildir!

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# İzinleri Değiştirme

---

![bg](../gorseller/3_normal_slayt.png)
# chmod Komutu

### İki Yöntem

<div class="two-columns">
<div>

### Sembolik Yöntem

Mevcut izinleri değiştirmek için kullanışlı.

```bash
chmod [ugoa][+-=][rwx] dosya
```

**Kim:**
- `u` = user (kullanıcı)
- `g` = group (grup)
- `o` = others (diğerleri)
- `a` = all (hepsi)

**İşlem:**
- `+` = ekle
- `-` = kaldır
- `=` = eşitle

</div>
<div>

### Sayısal Yöntem

Tüm izinleri birden değiştirmek için kullanışlı.

| Değer | İzin |
|-------|------|
| 4 | Read (r) |
| 2 | Write (w) |
| 1 | Execute (x) |

| Toplam | İzinler |
|--------|---------|
| 7 | rwx |
| 6 | rw- |
| 5 | r-x |
| 4 | r-- |
| 0 | --- |

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Sembolik Yöntem Örnekleri

### Temel Örnekler

```bash
# Başlangıç: -rw-r--r--

# Gruba yazma izni ekle
chmod g+w abc.txt
# Sonuç: -rw-rw-r--

# Kullanıcı ve gruba çalıştırma ekle, others'dan okuma kaldır
chmod ug+x,o-r abc.txt
# Sonuç: -rwxrwx---

# Kullanıcıyı sadece rx yap (w kaldırılır)
chmod u=rx abc.txt
# Sonuç: -r-xrwx---
```

<div class="info-box">

### 💡 İpucu

Virgül ile birden fazla değişiklik yapabilirsiniz: `chmod u+x,g-w,o=r dosya`

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Sayısal Yöntem Örnekleri

### Hesaplama

```
rwx = 4 + 2 + 1 = 7
rw- = 4 + 2 + 0 = 6
r-x = 4 + 0 + 1 = 5
r-- = 4 + 0 + 0 = 4
```

### Örnekler

```bash
# rwxr-xr-- ayarla
chmod 754 abc.txt

# rw-rw-r-- ayarla
chmod 664 abc.txt

# rwx------ ayarla (sadece sahip)
chmod 700 script.sh

# rwxr-xr-x ayarla (çalıştırılabilir dosya)
chmod 755 program
```

<div class="highlight-box">

### 🔢 Yaygın Değerler

**755** - Çalıştırılabilir dosyalar | **644** - Normal dosyalar | **700** - Özel dosyalar

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Varsayılan İzinler (umask)

---

![bg](../gorseller/3_normal_slayt.png)
# umask Komutu

<div class="two-columns">
<div>

### Varsayılan İzinler

Dosya ve dizinler oluşturulduğunda varsayılan izinler atanır.

**Maksimum izinler:**
- Dosyalar: `666` (rw-rw-rw-)
- Dizinler: `777` (rwxrwxrwx)

### umask Değeri

umask, maksimum izinlerden **çıkarılacak** değeri belirtir.

```bash
$ umask
0022
```

</div>
<div class="compare-box">

### Hesaplama Örneği

**umask = 027 ise:**

| | Dosya | Dizin |
|---|-------|-------|
| Maksimum | 666 | 777 |
| umask | -027 | -027 |
| **Sonuç** | **640** | **750** |

Dosya: `rw-r-----`
Dizin: `rwxr-x---`

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)
# umask Kullanımı

### Örnek

```bash
# umask değerini ayarla
sysadmin@localhost:~$ umask 027

# Dosya oluştur
sysadmin@localhost:~$ touch sample
sysadmin@localhost:~$ ls -l sample
-rw-r-----. 1 sysadmin sysadmin 0 Oct 28 20:14 sample

# Dizin oluştur
sysadmin@localhost:~$ mkdir test-dir
sysadmin@localhost:~$ ls -ld test-dir
drwxr-x---. 1 sysadmin sysadmin 4096 Oct 28 20:25 test-dir
```

<div class="warning-box">

### ⚠️ Önemli Notlar

- umask sadece mevcut oturum için geçerlidir
- Kalıcı yapmak için `~/.bashrc` dosyasına ekleyin
- root varsayılan: `0022` | Normal kullanıcı: `0002`

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Özet

<div class="two-columns">
<div>

### Sahiplik Komutları

| Komut | İşlev |
|-------|-------|
| `id` | Kullanıcı/grup bilgisi |
| `groups` | Grup üyelikleri |
| `newgrp` | Birincil grubu değiştir |
| `chgrp` | Grup sahipliğini değiştir |
| `chown` | Kullanıcı/grup sahipliğini değiştir |

### İzin Komutları

| Komut | İşlev |
|-------|-------|
| `chmod` | İzinleri değiştir |
| `umask` | Varsayılan izinleri ayarla |
| `stat` | Detaylı dosya bilgisi |

</div>
<div class="info-box">

### 🎯 Hatırlanacak Noktalar

1. Dosya erişimi için **tüm üst dizinlerde x** gerekir
2. Dosya silmek için **dizinde w+x** gerekir
3. Sahip izinleri **her zaman öncelikli**
4. **umask** varsayılan izinleri belirler
5. **755** çalıştırılabilir, **644** normal dosya

</div>
</div>

---

<!-- _class: final-slide -->

# Teşekkürler!
