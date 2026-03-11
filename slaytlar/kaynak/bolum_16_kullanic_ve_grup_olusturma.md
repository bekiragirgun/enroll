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
    padding: 85px 50px 30px 50px;
    background-color: #F7F7F7;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
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
    margin-bottom: 15px;
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
  }

  strong {
    color: #2D4A7C;
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

  .info-box h3 {
    color: white;
    margin-top: 0;
  }

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

  .compare-box {
    background: #f0f4f8;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #6B9FE8;
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

  td {
    color: #333 !important;
    background-color: white !important;
  }

  th {
    background-color: #2D4A7C;
    color: white;
  }

  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
  }
---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Kullanıcı ve Grup Oluşturma

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Giriş

---

![bg](../gorseller/3_normal_slayt.png)
# Giriş

Linux sistemlerde kurulum sırasında genellikle bir normal kullanıcı oluşturulur ve bu kullanıcıya yönetici komutlarını sudo ile çalıştırma izni verilir veya root kullanıcı hesabının şifresi yapılandırma sürecinin bir parçası olarak ayarlanır.

<div class="two-columns">
<div>

### Kurulum Sonrası Yapılandırma

- Çoğu Linux sistemi, bir yetkisiz (root olmayan) kullanıcının oturum açmasına izin verir
- Kullanıcı, doğrudan veya dolaylı olarak root kullanıcısı olarak komutları etkili bir şekilde yürütebilir
- Tek kişilik kullanım için tek hesap yeterli olabilir

<h3>Birden Fazla Kullanıcı Avantajları</h3>

<ul>
<li>Her kullanıcının ayrı ev dizini vardır, diğerleri tarafından erişilemez</li>
<li>Dosyalara veya servislere seçici erişim sağlanabilir</li>
<li>sudo komutu seçili yönetici komutlarını çalıştırma izni verilebilir</li>
<li>Sistem, kullanıcıların bu komutları gerçekleştirdiğini günlüğe kaydeder</li>
</ul>

</div>
<div class="info-box">

### 📌 Önemli Notlar

<h3>Grup Yapılandırması</h3>

<ul>
<li>Kullanıcılar grup üyeliklerine ve ilgili haklara sahip olabilir</li>
<li>Yönetim esnekliği sağlanır</li>
<li>Bazı dağıtımlarda yeni kullanıcı için otomatik grup oluşturulur (UPG)</li>
</ul>

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Gruplar

---

![bg](../gorseller/3_normal_slayt.png)
# Gruplar

<div class="two-columns">
<div>

### Grup Oluşturma Nedenleri

Grup oluşturmanın en yaygın nedeni, kullanıcıların dosyaları paylaşması için bir yol sağlamaktır.

<div class="info-box">
<h3>🔄 İşbirlik Senaryosu</h3>

Aynı proje üzerinde çalışan ve proje dosyalarında saklanan belgeler üzerinde işbirliği yapması gereken birkaç kişi varsa.
</div>

<h3>Grup Avantajları</h3>

<ul>
<li>Grup üyeleri dosyaları paylaşabilir</li>
<li>Yönetici, kullanıcıları ortak gruba üye yapabilir</li>
<li>Dizin sahipliğini yeni gruba değiştirebilir</li>
<li>Dizin izinlerini grup üyelerine erişim için yapılandırabilir</li>
</ul>

</div>
<div class="highlight-box">

<h3>📋 Grup Kontrol Komutları</h3>

<h4>/etc/group Dosyası</h4>
<pre><code>grep root /etc/group</code></pre>

<h4>Getent Komutu</h4>
<pre><code>getent group root</code></pre>

<p>Yerel kullanım için her iki komut aynı sonucu verir.</p>

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Grup Oluşturma

---

![bg](../gorseller/3_normal_slayt.png)
# Grup Oluşturma (groupadd)

### groupadd Komutu

root kullanıcısı yeni grup oluşturmak için `groupadd` komutunu kullanabilir.

<div class="info-box">

### 🆕 Grup ID Atama (-g Seçeneği)

```bash
groupadd -g 1005 research
grep research /etc/group
```
**Çıktı:** research:x:1005:

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Grup Oluşturma (devam)

<div class="compare-box">

### 📊 Otomatik GID Atama

-g seçeneği sağlanmazsa, `groupadd` otomatik bir GID sağlar (mevcut en yüksek GID + 1).

```bash
groupadd development
grep development /etc/group
```
**Çıktı:** development:x:1006:

</div>

<div class="highlight-box">

### ⚙️ UPG (User Private Group) Etkisi

- UID ve UPG'nin ID'si eşleşmelidir
- GID oluştururken UID aralığındaki sayıları kullanmaktan kaçının

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Grup İsimlendirme

---

![bg](../gorseller/3_normal_slayt.png)
# Grup İsimlendirme

<div class="compare-box">

### 📋 Taşınabilirlik İçin İsimlendirme Yönergeleri

| Yönerge | Açıklama |
|---------|-----------|
| İlk karakter | Alt çizgi (_) veya küçük harf (a-z) |
| Karakter uzunluğu | En fazla 32 karakter (16'den fazlası sorun yaratır) |
| Kalan karakterler | Alfasayısal, tire (-) veya alt çizgi (_) |
| Son karakter | Tire (-) karakteri olmamalı |

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Grup İsimlendirme (devam)

<div class="highlight-box">

### ⚠️ Önemli Notlar

- Bu yönergeler her zaman zorlanmaz
- `groupadd` komutu başarısız olmayabilir
- Ancak diğer komutlar veya sistem servisleri doğru çalışmayabilir

</div>

<div class="info-box">

### 🔒 Sistem Grupları için -r Seçeneği

GID değerleri 500 (RedHat) veya 1000 (Debian) altındaki değerler sistem için ayrılmıştır.

```bash
groupadd -r sales
getent group sales
```
**Çıktı:** sales:x:999:

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Grup Düzenleme

---

![bg](../gorseller/3_normal_slayt.png)
# Grup Düzenleme (groupmod)

### groupmod Komutu

Grup adını veya GID'yi değiştirmek için `groupmod` komutu kullanılır.

<div class="info-box">

### 🔄 Grup Adı Değiştirme (-n)

```bash
groupmod -n clerks sales
ls -l index.html
```
**Çıktı:** -rw-r-----. 1 root clerks 0 Aug 1 13:21 index.html

Dosya sahibi grup adı değişir ancak GID aynı kalır.

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Grup Düzenleme (devam)

<div class="highlight-box">

### ⚙️ GID Değiştirme (-g) - ÖNERİLMEZ!

Grup GID'sini değiştirmek **önerilmez**! Dosyalar artık gruba bağlı olmayacaktır.

```bash
groupmod -g 10003 clerks
```

Grubu olmayan dosyalar "orphaned files" olarak adlandırılır: `find / -nogroup`

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Grup Silme

---

![bg](../gorseller/3_normal_slayt.png)
# Grup Silme (groupdel)

### groupdel Komutu

`groupdel` komutu ile grubu silebilirsiniz ancak dikkatli olun!

<div class="info-box">

### ⚠️ Sızılmış Dosya Riski

- Silinecek gruba ait dosyalar sızılmış olacaktır
- Sadece tamamlayıcı gruplar silinebilir
- Bir grubu silebilmek için, kullanıcının birincil grubunu değiştirin

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Grup Silme (devam)

<div class="compare-box">

### 📋 Grup Silme Örnekleri

| Durum | Komut | Sonuç |
|-------|-------|-------|
| Birincil grup değil | `groupdel clerks` | ✅ Başarılı |
| Birincil grup ise | `groupdel clerks` | ❌ Başarısız |

</div>

<div class="highlight-box">

### 🔒 Kullanıcı Birincil Grup Değiştirme

Yönetici, hangi grubun birincil grup olduğunu değiştirebilir:
```bash
usermod -g users username
```

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Kullanıcı Yapılandırma Dosyaları

---

![bg](../gorseller/3_normal_slayt.png)
# Kullanıcı Yapılandırma Dosyaları

### useradd -D Komutu

`useradd -D` komutu varsayılan değerleri görüntüler veya değiştirir.

<div class="info-box">

### 📋 /etc/default/useradd Dosyası

```bash
useradd -D
GROUP=100
HOME=/home
INACTIVE=-1
SHELL=/bin/bash
SKEL=/etc/skel
```

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Kullanıcı Yapılandırma Dosyaları (devam)

<div class="highlight-box">

### ⚙️ Ana Varsayılan Değerler

| Ayar | Varsayılan | Açıklama |
|------|------------|----------|
| GROUP | 100 | Birincil grup GID |
| HOME | /home | Ev dizini temel dizini |
| INACTIVE | -1 | Şifre sonrası kapanma günleri |
| SHELL | /bin/bash | Varsayılan kabuk programı |
| SKEL | /etc/skel | Şablon dizini |

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# /etc/login.defs Dosyası

---

![bg](../gorseller/3_normal_slayt.png)
# /etc/login.defs Dosyası

### /etc/login.defs Yapılandırması

Bu dosya yeni kullanıcılara uygulanan varsayılan değerleri içerir.

```bash
grep -Ev '^#|^$' /etc/login.defs
PASS_MAX_DAYS 99999
PASS_MIN_DAYS 0
UID_MIN 500
UID_MAX 60000
ENCRYPT_METHOD SHA512
```

---

![bg](../gorseller/3_normal_slayt.png)
# /etc/login.defs Dosyası (devam)

<div class="highlight-box">

### ⚙️ Şifre Politikaları

| Parametre | Varsayılan | Açıklama |
|-----------|------------|----------|
| PASS_MAX_DAYS | 99999 | Şifre geçerlilik süresi (gün) |
| PASS_MIN_DAYS | 0 | Şifre değişme minimum süre (gün) |
| PASS_MIN_LEN | 5 | Minimum şifre uzunluğu |
| PASS_WARN_AGE | 7 | Şifre değiştirme uyarısı (gün önce) |

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Kullanıcı Hesabı Dikkatleri

---

![bg](../gorseller/3_normal_slayt.png)
# Kullanıcı Hesabı Dikkatleri

### Kullanıcı Adı (Username)

<div class="info-box">

### 📝 İsimlendirme Yönergeleri

- İlk karakter: alt çizgi (_) veya küçük harf (a-z)
- En fazla 32 karakter (16'den fazlası sorun yaratır)
- Son karakter: tire (-) olmamalı

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Kullanıcı Hesabı - UID

<div class="highlight-box">

### 🔑 UID Kullanımı (-u Seçeneği)

```bash
useradd -u 1000 jane
```

</div>

<div class="compare-box">

### 📊 UID Aralıkları

| Tür | Aralık | Açıklama |
|-----|--------|----------|
| root | 0 | Yönetici hesabı |
| Sistem | 1-999 | Servis hesapları |
| Normal | 1000-60000 | Standart kullanıcılar |

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Birincil ve Yardımcı Gruplar

---

![bg](../gorseller/3_normal_slayt.png)
# Birincil ve Yardımcı Gruplar

### Birincil Grup (-g Seçeneği)

UPG kullanan dağıtımlarda, grup otomatik oluşturulur.

```bash
useradd -g users jane
```

### 👥 Yardımcı Gruplar (-G Seçeneği)

```bash
useradd -G sales,research jane
```
Virgülle ayrılmış grup listesi, dosya paylaşımı için idealdir.

---

![bg](../gorseller/3_normal_slayt.png)
# Birincil ve Yardımcı Gruplar (devam)

<div class="compare-box">

### 📊 Grup Tipleri

| Grup Türü | Açıklama |
|-----------|----------|
| Birincil Grup | Kullanıcının ana grubu, /etc/passwd'de belirtilir |
| Yardımcı Gruplar | Ek grup üyelikleri, /etc/group dosyasında saklanır |
| UPG | Kullanıcının adıyla otomatik oluşturulur |

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Ev Dizini ve Kabuk

---

![bg](../gorseller/3_normal_slayt.png)
# Ev Dizini ve Kabuk

### 🏠 Ev Dizini Seçenekleri

| Seçenek | Açıklama |
|---------|----------|
| -m | Ev dizini oluştur (varsayılan /home/kullanıcı_adı) |
| -M | Ev dizini oluşturma (hesap var, dizin yok) |
| -d | Özel ev dizini belirtme (tam yol) |
| -b | Temel dizini değiştirme (/home yerine farklı) |

---

![bg](../gorseller/3_normal_slayt.png)
# Ev Dizini ve Kabuk (devam)

<div class="highlight-box">

### 🐚 Kabuk (Shell) Yapılandırması

```bash
useradd -s /bin/sh jane
```

Varsayılan /bin/bash'tir, -s seçeneği ile değiştirin.

</div>

<div class="compare-box">

### 📋 /etc/passwd Örnek

`jane:x:1008:1010::/home/jane:/bin/sh`

Biçim: kullanıcı_adı:şifre_x:UID:GID:gerçek_adı:ev_dizini:kabuk

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Şablon Dizini (Skeleton Directory)

---

![bg](../gorseller/3_normal_slayt.png)
# Şablon Dizini (Skeleton Directory)

### /etc/skel Dizini

Varsayılan şablon dizini. İçeriği yeni kullanıcının ev dizinine kopyalanır.

<div class="info-box">

### 📁 /etc/skel İçeriği

```bash
ls -a /etc/skel
```
- Yeni kullanıcının ev dizinine kopyalanır
- Dosyalar yeni kullanıcıya aittir

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Şablon Dizini (devam)

<div class="highlight-box">

### 🔄 -k Seçeneği (Özel Şablon)

```bash
useradd -mk /home/sysadmin jane
```
-k seçeneği ile farklı şablon belirtin, -m zorunludur.

</div>

<div class="compare-box">

### 📊 Şablon Kullanım Senaryoları

| Senaryo | Yaklaşım |
|---------|----------|
| Varsayılan | /etc/skel kullanılır |
| Sistem yöneticisi | /home/sysadmin şablonu |
| Özel kullanıcı | Proje şablonları |

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Özet ve En İyi Uygulamalar

---

![bg](../gorseller/3_normal_slayt.png)
# Özet - Önemli Komutlar

<div class="info-box">

### ✅ Grup ve Kullanıcı Komutları

**Gruplar:** `groupadd` (oluştur) | `groupmod` (düzenle) | `groupdel` (sil)

**Kullanıcılar:** `useradd` (oluştur) | `useradd -D` (varsayılanlar) | `usermod` (düzenle)

</div>

<div class="highlight-box">

### ⚙️ Yapılandırma Dosyaları

- **/etc/default/useradd** - useradd varsayılanları
- **/etc/login.defs** - Genel kullanıcı politikaları
- **/etc/passwd, /etc/shadow, /etc/group** - Hesap bilgileri

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Özet - En İyi Uygulamalar

<div class="compare-box">

### 📋 En İyi Uygulamalar

| Yönerge | Açıklama |
|---------|----------|
| Grup planlama | Kullanıcılardan önce grupları oluşturun |
| UID/GID aralıkları | Sistem aralıklarından kaçının |
| İsimlendirme | 16 karakter idealdir |
| GID değiştirme | Grup adını değiştirebilirsiniz, GID değiştirmeyin |

</div>

---

<!-- _class: final-slide -->

# Teşekkürler!

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü
