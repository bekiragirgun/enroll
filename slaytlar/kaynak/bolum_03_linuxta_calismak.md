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
    overflow-x: auto;
    overflow-y: auto;
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

  .info-box p, .info-box li, .info-box strong {
    color: white !important;
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

  .highlight-box p, .highlight-box li, .highlight-box strong {
    color: white !important;
  }

  .compare-box {
    background: #f0f4f8;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #6B9FE8;
  }

  .info-box th, .info-box td,
  .highlight-box th, .highlight-box td {
    color: white !important;
    background-color: transparent !important;
    border-color: rgba(255,255,255,0.3) !important;
  }

  .info-box th,
  .highlight-box th {
    background-color: rgba(0,0,0,0.2) !important;
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
    display: none;
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
    max-width: 100%;
    max-height: 400px;
    object-fit: contain;
  }

  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
  }

---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Linux'ta Çalışmak

**Kapadokya Üniversitesi**
Veri Bilimi ve Analizi Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Linux Masaüstü

---

![bg](../gorseller/3_normal_slayt.png)
# Linux Masaüstüne Giriş

<div class="two-columns">

<div>

## 🖥️ Neden Linux Masaüstü?

Linux sistem yöneticisi olmak için önce Linux'u **günlük masaüstü** olarak kullanmak gerekir.

**Sistem yöneticileri:**
- Sunucuları yönetir
- Kullanıcılara yapılandırma desteği verir
- Yeni yazılım önerir
- Dokümantasyon günceller

**İlk adım:** Büyük bir dağıtımı USB'ye yükleyip eski bir PC'ye kurmak.

</div>

<div>

![w:360](../../06_KAYNAKLAR/LEv2_3_4.png)

<div class="info-box">

### 💡 Tanıdık Arayüz

Linux masaüstü; simgeler, ayarlar uygulaması, WiFi ve kullanıcı hesapları ile Windows/Mac'e benzer bir deneyim sunar.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Komut Satırına Erişim

<div class="two-columns">

<div>

## ⌨️ CLI'ye Ulaşma Yolları

**1. GUI Terminal:**
- Menüden: Uygulamalar → Sistem Araçları → Terminal
- Arama çubuğunda "terminal" yazarak

**2. Sanal Terminal (Virtual Terminal):**
- GUI ile aynı anda çalışır
- Ayrı oturum açma gerektirir
- Tam ekran CLI deneyimi

**CLI Görevleri:**
- Program başlatma, betik çalıştırma
- Yapılandırma dosyası düzenleme

</div>

<div>

![w:380](../../06_KAYNAKLAR/LEv2_3_1.png)

<div class="highlight-box">

### 💡 Neden CLI?

Sunucuların çoğu doğrudan CLI'ye açılır. GUI kaynak tüketir ve sunucu işlemleri için genellikle gereksizdir.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Uygulamalar ve Çekirdek

---

![bg](../gorseller/3_normal_slayt.png)
# Çekirdek (Kernel) ve Uygulamalar

<div class="two-columns">

<div>

## 🎯 Çekirdeğin Görevi

Çekirdek bir **hava trafik kontrolörü** gibidir:

- Hangi programın hangi belleği alacağına karar verir
- Uygulamaları başlatır ve durdurur
- Ekranda metin/grafik gösterimini yönetir
- Kaynak çakışmalarını çözer

**Çoklu Görev (Multitasking):**
- Sınırlı CPU ve bellek paylaşımı
- Görevler arası hızlı geçiş
- Kullanıcıya eşzamanlı çalışma hissi

</div>

<div>

## 🔄 Süreç (Process) Kavramı

Çekirdek, kullanıcı uygulaması ile sistem servisi arasında ayrım yapmaz. Her görev bir **süreç** olarak izlenir.

<div class="info-box">

### 💡 API Soyutlama

Uygulamalar çekirdeğin **API**'sini kullanır. Diskin SSD mi, HDD mi yoksa ağ paylaşımı mı olduğunu bilmek zorunda değildir.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Uygulama Türleri

<div class="two-columns">

<div>

## 📦 Üç Temel Kategori

**🖥️ Sunucu Uygulamaları:**
- Monitör/klavye ile doğrudan etkileşim yok
- Diğer bilgisayarlara (istemcilere) bilgi sunar
- Arka planda veri işler

**🖱️ Masaüstü Uygulamaları:**
- Kullanıcıyla doğrudan etkileşim
- Web tarayıcı, metin editörü, müzik çalar
- İstemci/sunucu mimarisinin "istemci" tarafı

</div>

<div>

**🔧 Araçlar (Tools):**
- Sistem yönetimini kolaylaştırır
- Kabuklar (shell), derleyiciler (compiler)
- Ekran yapılandırma araçları

<div class="highlight-box">

### 💡 Linux'un Avantajı

Aynı sunucu uygulamalarını masaüstünde veya ucuz sanal sunucuda çalıştırarak üretim ortamını **simüle edebilirsiniz**. Pahalı donanım veya lisans gerekmez.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Sunucu Uygulamaları

---

![bg](../gorseller/3_normal_slayt.png)
# Web Sunucuları

<div class="two-columns">

<div>

## 🌐 HTTP/HTTPS ile İçerik Sunma

**Statik Sayfa:** Dosya diskte olduğu gibi gönderilir
**Dinamik Sayfa:** İstek bir uygulamaya yönlendirilir (ör. WordPress)

## 🏆 Başlıca Web Sunucuları

**Apache HTTPD:**
- En yaygın web sunucusu
- Apache Software Foundation
- 100+ açık kaynak proje barındırır

**NGINX:**
- Performans odaklı, Rusya kökenli
- Modern UNIX çekirdek özelliklerini kullanır

</div>

<div>

<div class="info-box">

### 💡 WordPress

En popüler dinamik web platformu. Kullanıcılar tarayıcı üzerinden içerik geliştirir, yazılım bunu tam işlevli bir web sitesine dönüştürür.

</div>

<div class="compare-box">

### 📊 Pazar Payı

Web sitelerinin **%65'inden fazlası** Apache veya NGINX tarafından sunulmaktadır.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Özel Bulut ve Veritabanı Sunucuları

<div class="two-columns">

<div>

## ☁️ Özel Bulut Sunucuları

**ownCloud (2010):**
- Veri depolama, senkronizasyon ve paylaşım
- GNU AGPLv3 + kurumsal lisans

**Nextcloud (2016):**
- ownCloud'dan çatallandı (fork)
- Açık ve şeffaf geliştirme süreci
- Güvenlik ve uyumluluk odaklı

</div>

<div>

## 🗄️ Veritabanı Sunucuları

Dinamik web uygulamalarının **omurgası**.

**MariaDB:** MySQL'in topluluk çatalı
**PostgreSQL:** Gelişmiş özellikler
**Firebird:** Hafif ve taşınabilir

<div class="highlight-box">

### 💡 SQL

**Structured Query Language** ile veri sorgulama, toplama ve raporlama yapılır. Örneğin: satış rakamlarını ürün ve tarihe göre gruplamak.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# E-posta Sunucuları

<div class="two-columns">

<div>

## 📧 Üç Temel Bileşen

**1. MTA (Mail Transfer Agent):**
- E-postaları sistemler arası transfer eder
- **Sendmail:** En bilinen MTA
- **Postfix:** Daha basit ve güvenli

**2. MDA (Mail Delivery Agent):**
- E-postayı kullanıcı posta kutusuna depolar
- Zincirdeki son MTA tarafından çağrılır

**3. POP/IMAP Sunucu:**
- İstemci ile sunucu arası iletişim
- **Dovecot:** Kolay kullanım, düşük bakım

</div>

<div>

<div class="info-box">

### 💡 Açık Kaynak vs Kapalı Kaynak

**Microsoft Exchange:** Tek paket, tüm bileşenler Microsoft'tan.

**Linux e-posta:** Modüler yapı — MTA, MDA ve POP/IMAP sunucusu ayrı ayrı seçilebilir ve değiştirilebilir.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Dosya Paylaşımı ve Dizin Hizmetleri

<div class="two-columns">

<div>

## 📁 Dosya Paylaşım Protokolleri

| Protokol | Kullanım |
|----------|----------|
| **Samba** | Windows dosya paylaşımı |
| **Netatalk** | macOS dosya paylaşımı |
| **NFS** | UNIX/Linux yerel paylaşım |

**Samba:** Linux'u Windows gibi gösterir.
**NFS:** Çekirdek düzeyinde, uzak dosya sistemi yerel disk gibi bağlanır.

</div>

<div>

## 🗂️ Dizin Hizmetleri

**DNS:** İsim → IP adresi çözümleme
- **BIND:** En popüler DNS sunucusu

**LDAP:** Kullanıcı hesapları ve roller
- **OpenLDAP:** Linux altyapısında standart

**DHCP:** Otomatik IP adresi atama
- **ISC DHCP:** En yaygın açık kaynak DHCP

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Masaüstü Uygulamaları

---

![bg](../gorseller/3_normal_slayt.png)
# E-posta ve Yaratıcı Uygulamalar

<div class="two-columns">

<div>

## 📨 E-posta İstemcileri

**Mozilla Thunderbird:**
- Tam özellikli masaüstü e-posta istemcisi
- POP/IMAP bağlantısı, SMTP ile gönderim

**Diğerleri:**
- **Evolution:** GNOME projesi
- **KMail:** KDE projesi
- POP/IMAP standardizasyonu sayesinde istemciler arası geçiş kolay

</div>

<div>

## 🎨 Yaratıcı Uygulamalar

| Uygulama | Alan |
|----------|------|
| **Blender** | 3D film/animasyon |
| **GIMP** | 2D görüntü işleme |
| **Audacity** | Ses düzenleme |

<div class="info-box">

### 💡 Profesyonel Kullanım

**Blender** bağımsız filmlerden Hollywood yapımlarına kadar kullanılır. **GIMP** çoklu dil desteğiyle betik yazılabilir.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Verimlilik Uygulamaları

<div class="two-columns">

<div>

## 📊 Ofis Paketleri

**LibreOffice:**
- OpenOffice.org çatalı (fork)
- Microsoft Office uyumlu formatlar
- Writer, Calc, Impress, Draw

**Özellikler:**
- Grafik ve formül desteği
- Belgeler arası bağlantı (link)
- PDF okuma/yazma
- Wiki entegrasyonu (eklentilerle)

</div>

<div>

![w:380](../../06_KAYNAKLAR/LEv2_3_2.png)

<div class="highlight-box">

### 💡 Linux Becerisi

Günlük işlerde açık kaynak uygulamalar kullanmak, Linux becerilerinizi güçlendirmenin en etkili yoludur.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Web Tarayıcıları

<div class="two-columns">

<div>

## 🌍 Linux'ta Tarayıcılar

**Mozilla Firefox:**
- Açık kaynak, hızlı, zengin özellikler
- Web geliştirici desteği mükemmel

**Google Chrome:**
- Açık kaynak (Chromium tabanlı)
- Çapraz platform desteği

<div class="compare-box">

### 🔄 Rekabet = Gelişim

İki tarayıcı arasındaki rekabet her birinin gelişimini hızlandırır.

</div>

</div>

<div>

<div class="info-box">

### 💡 Gizlilik Ayarları

Tarayıcı yapılandırmasını değiştirerek paylaştığınız bilgi miktarını **sınırlayabilirsiniz**.

</div>

<div class="highlight-box">

### 🔒 Gizli Mod

Tarayıcıların **özel/gizli modu** pencere kapatıldığında çerezleri ve izleme piksellerini siler.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Konsol Araçları

---

![bg](../gorseller/3_normal_slayt.png)
# Konsol Araçları Neden Önemli?

<div class="two-columns">

<div>

## 🛠️ Geliştirme ve Yönetim Kesişimi

UNIX tarihinde yazılım geliştirme ve sistem yönetimi becerileri büyük ölçüde **örtüşür**.

**Sistem yönetim araçları:**
- Döngüler (loops) gibi programlama özellikleri içerir
- Betik dilleri ile otomasyon sağlar
- Tekrarlayan görevleri otomatikleştirir

</div>

<div>

<div class="info-box">

### 💡 Temel Beceri

En az temel düzeyde programlama bilgisi, yetkin bir sistem yöneticisi için **zorunludur**. Kabuklar, editörler ve betik dilleri bu becerinin temelini oluşturur.

</div>

<div class="highlight-box">

### 🎓 İki Temel Araç

**Kabuklar (Shells):** Komut girişi ve betik yazma
**Metin Editörleri:** Yapılandırma dosyası düzenleme

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Kabuklar (Shells)

<div class="two-columns">

<div>

## 🐚 Kabuk Nedir?

Kullanıcı komutlarını kabul eden ve Linux çekirdeğine ileten arayüz.

**Yetenekleri:**
- Dosya manipülasyonu ve uygulama başlatma
- Betik yazma (scripting)
- Ortam özelleştirme

## 📜 İki Ana Aile

**Bourne Ailesi:** sh → **Bash** (varsayılan)
**C Ailesi:** csh → **tcsh**

</div>

<div>

## 🔧 Modern Kabuklar

| Kabuk | Özellik |
|-------|---------|
| **Bash** | Çoğu sistemde varsayılan |
| **Zsh** | Gelişmiş özelleştirme |
| **Ksh** | Korn kabuğu |
| **tcsh** | C dili sözdizimi |

<div class="info-box">

### 💡 Kabuk Seçimi

Kabuk seçimi kişisel tercihtir. **Bash**'e hakim olan kullanıcı çoğu Linux sisteminde etkili çalışabilir.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Metin Editörleri

<div class="two-columns">

<div>

## ✏️ Konsol Editörleri

Yapılandırma dosyalarını düzenlemek için.

**Gelişmiş Editörler:**

| Editör | Özellik |
|--------|---------|
| **Vi/Vim** | Her Linux'ta mevcut, güçlü |
| **Emacs** | Eklenti desteği, takvim vb. |

**Basit Editörler:**
- **Nano:** Kolay kullanım, temel düzenleme
- **Pico:** Nano'nun ilham kaynağı

</div>

<div>

<div class="highlight-box">

### 💡 Vi Neden Önemli?

Vi neredeyse **her Linux sisteminde** mevcuttur. Sistem kurtarma modunda çalışırken kritik bir araçtır. En iyi öğrenme zamanı: sisteminizi tamir etmeniz gerekmeden **önce**.

</div>

<div class="compare-box">

### 🔄 Nano vs Vi

**Nano:** Basit, hızlı, kolay öğrenilir
**Vi:** Dik öğrenme eğrisi ama çok güçlü

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Paket Yönetimi

---

![bg](../gorseller/3_normal_slayt.png)
# Paket Yönetimi Nedir?

<div class="two-columns">

<div>

## 📦 Paket Kavramı

Eskiden: kaynak kodu indir → derle → dosyaları kopyala.

**Modern paketler:**
- Sıkıştırılmış dosyalar
- Uygulama + bağımlılıklar bir arada
- Doğru dizinlere otomatik yerleştirme
- Sembolik bağlantılar oluşturma

## 🔧 Paket Yöneticisi

- Dosya-paket ilişkisini takip eder
- Uzak depolardan güncelleme indirir
- Bağımlılıkları otomatik çözer

</div>

<div>

<div class="info-box">

### 💡 İki Büyük Sistem

**1. Debian (.deb):** Debian, Ubuntu, Mint
**2. Red Hat (.rpm):** RHEL, Fedora, CentOS, SUSE

Her iki sistem de bağımlılıkları takip eder ve yazılım güncelleme/kaldırma işlemlerini güvenli yapar.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Debian Paket Yönetimi (.deb)

<div class="two-columns">

<div>

## 🌀 Araç Hiyerarşisi

**Dağıtımlar:** Debian, Ubuntu, Mint

| Katman | Araç | Açıklama |
|--------|------|----------|
| Düşük | `dpkg` | Temel paket yönetimi |
| Orta | `apt-get` | dpkg ön yüzü |
| Orta | `aptitude` | Gelişmiş CLI aracı |
| Yüksek | Synaptic | GUI ön yüzü |
| Yüksek | Software Center | Kullanıcı dostu GUI |

</div>

<div>

<div class="highlight-box">

### 💡 apt-get Örneği

```
sudo apt-get update
sudo apt-get install firefox
sudo apt-get remove firefox
```

`apt-get` bağımlılık çözümlemesini otomatik yapar. `dpkg` ise tek tek paketlerle çalışır.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# RPM Paket Yönetimi (.rpm)

<div class="two-columns">

<div>

## 🎩 Araç Hiyerarşisi

**Dağıtımlar:** RHEL, Fedora, CentOS, SUSE

| Katman | Araç | Açıklama |
|--------|------|----------|
| Düşük | `rpm` | Temel paket yönetimi |
| Orta | `yum` | Bağımlılık çözümlemesi |
| Orta | `zypper` | SUSE/openSUSE için |
| Yüksek | Yumex | GUI ön yüzü |
| Yüksek | PackageKit | GNOME GUI |

</div>

<div>

<div class="info-box">

### 💡 Root Yetkisi

Paket **sorgulama ve arama** → normal kullanıcı yeterli.
Paket **ekleme, güncelleme, silme** → **root yetkisi** gerekli.

</div>

<div class="compare-box">

### 🔄 ZYpp (zypper)

openSUSE ve SLES'in paket yönetim aracı:
`zypper in paket_adi`

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Geliştirme Dilleri

---

![bg](../gorseller/3_normal_slayt.png)
# Derlenen Diller

<div class="two-columns">

<div>

## ⚙️ Derleme (Compiled)

Kod bir seferde makine diline çevrilir.

**C Dili:**
- Linux'un kendisi C ile yazılmıştır
- Küçük ve verimli kod üretir
- Makine koduna yakın haritalama

**C++ ve Objective-C:**
- C++: Nesne yönelimli C uzantısı
- Objective-C: Apple ürünlerinde yoğun kullanım

</div>

<div>

## ☕ Java

Farklı bir derleme yaklaşımı:

**Java Virtual Machine (JVM):**
- Kod önce JVM bytecode'a derlenir
- Her platformda JVM çalıştırılır
- "Bir kere yaz, her yerde çalıştır"

<div class="info-box">

### 💡 JVM Avantajı

JVM bellek yönetimi gibi karmaşık işleri otomatik halleder. JVM iyileştirmeleri anında tüm Java uygulamalarına yansır.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Yorumlanan Diller

<div class="two-columns">

<div>

## 🔄 Yorumlama (Interpreted)

Kod çalışma sırasında makine diline çevrilir.

| Dil | Öne Çıkan Alan |
|-----|----------------|
| **JavaScript** | Web, etkileşimli sayfalar |
| **Perl** | Metin işleme, otomasyon |
| **PHP** | Dinamik web (WordPress) |
| **Ruby** | Web (Rails), otomasyon (Chef) |
| **Python** | Veri bilimi, web (Django) |

</div>

<div>

<div class="highlight-box">

### 💡 JavaScript

Web'in temel teknolojilerinden biri. Basit animasyonlardan karmaşık sunucu uygulamalarına kadar geniş kullanım.

</div>

<div class="info-box">

### 🎓 Kütüphaneler

- **ImageMagick:** Görüntü işleme
- **OpenSSL:** Kriptografi
- **C Kütüphanesi:** Dosya okuma/yazma

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Güvenlik

---

![bg](../gorseller/3_normal_slayt.png)
# Çerezler ve İzleme

<div class="two-columns">

<div>

## 🍪 Çerez (Cookie) Nedir?

Web sunucusunun tarayıcıya gönderdiği küçük metin.

**İyi kullanım:**
- Alışveriş sepeti takibi
- Oturum açık tutma

**Sorunlu kullanım:**
- Üçüncü taraf izleme pikselleri
- Reklamcılar birden fazla siteyi izler
- "Beğen" butonları ile sosyal ağ takibi

</div>

<div>

![w:360](../../06_KAYNAKLAR/LEv2_3_3.png)

<div class="info-box">

### 💡 Korunma Yolları

- "Do Not Track" sinyali gönder
- Üçüncü taraf çerezleri engelle
- Tarayıcı kapatıldığında çerezleri sil

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Parola Yönetimi

<div class="two-columns">

<div>

## 🔑 Parola Güvenliği

**Root hesabı:**
- Sistemdeki en yetkili kullanıcı
- İlk savunma: root erişimini devre dışı bırak

**Parola seviyeleri:**
- Kullanıcı oturum açma
- Grup ve yetki bazlı erişim
- Servis parolaları (veritabanı vb.)
- Uzak erişim (SSH, FTP)

</div>

<div>

<div class="highlight-box">

### 💡 İyi Parola Kuralları

- En az **10 karakter** uzunluk
- Büyük/küçük harf, rakam, özel karakter
- Her site için **benzersiz** parola
- **Parola yöneticisi** kullan (ör. KeePassX)

</div>

<div class="compare-box">

### 🔐 İki Faktörlü Doğrulama (2FA)

Parola + ikinci faktör (telefona gönderilen kod). Güvenliği önemli ölçüde artırır.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Kendinizi Koruma ve Gizlilik Araçları

<div class="two-columns">

<div>

## 🛡️ Temel Koruma Adımları

- Güçlü, benzersiz parolalar kullan
- Sitelere sadece **gerekli** bilgiyi ver
- Düzenli güncelleme kontrolü yap
- Güvenlik duvarı (iptables/ufw) kullan

![w:320](../../06_KAYNAKLAR/LEv2_3_5.png)

</div>

<div>

## 🔒 Gizlilik Araçları

**Şifreleme (Encryption):**
- HTTPS: Web trafiği şifreleme

**VPN (Virtual Private Network):**
- İki sistem arası şifreli kanal
- Uzak çalışanlar ve gizlilik

**Tor Tarayıcı:**
- İstekleri sunucu ağı üzerinden yönlendirir
- Kimlik gizliliği sağlar

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Bulut Bilişim

---

![bg](../gorseller/3_normal_slayt.png)
# Bulut Bilişim Nedir?

<div class="two-columns">

<div>

## ☁️ Bulutun Tanımı

Uzak veri merkezlerinden internet üzerinden erişilen bilgi işlem kaynakları.

**Bulutta depolanabilecekler:**
- Veri ve sunucular
- Depolama alanı
- Uygulama barındırma
- Analitik ve diğer hizmetler

**Bulut benimseme (Cloud Adoption):**
Kuruluşun BT süreçlerini bulut hizmetlerine taşıması.

</div>

<div>

<div class="info-box">

### 💡 Neden Bulut?

- BT altyapı yönetimini **üçüncü tarafa** devret
- Sadece **kullanılan kadar** öde
- **Küresel erişim** ve paylaşım
- Hızlı **ölçeklendirme**

</div>

<div class="highlight-box">

### 🌍 Dijital Dönüşüm

Bulut bilişim, önümüzdeki on yılın en önemli **yıkıcı teknolojilerinden** biri olarak görülmektedir.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Bulut Dağıtım Modelleri

<div class="two-columns">

<div>

## 🏗️ Dört Temel Model

**☁️ Genel Bulut (Public):**
- Genel halka ve kuruluşlara açık
- Birden fazla kiracı (tenant) paylaşır
- Amazon, Google, Azure

**🔒 Özel Bulut (Private):**
- Tek bir kuruluş için ayrılmış
- Daha fazla gizlilik ve kontrol
- Rackspace, IBM tarafından yönetilebilir

</div>

<div>

**👥 Topluluk Bulutu (Community):**
- Ortak hedefleri olan kuruluşlar grubu
- Maliyetler paylaşılır
- Daha yüksek güvenlik

**🔀 Hibrit Bulut (Hybrid):**
- İki veya daha fazla bulut türünün birleşimi
- Veri ve uygulama taşınabilirliği
- Hassas kaynaklar kontrol altında tutulur

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Linux ve Bulut: Esneklik ve Erişilebilirlik

<div class="two-columns">

<div>

## 🐧 Bulutta Linux'un Rolü

Genel bulut iş yüklerinin **%90'ı** Linux tarafından desteklenmektedir.

## 🔄 Esneklik (Flexibility)

- Linux modüler tasarımdır
- Büyük açık kaynak uygulama ekosistemi
- Küçük sensörden büyük sunucu çiftliğine kadar ölçeklenir

</div>

<div>

## 🌐 Erişilebilirlik (Accessibility)

Bulutta uygulamalara **her yerden, her cihazdan** erişilir:
- Masaüstü, Mobil, Thin client

<div class="info-box">

### 💡 Her Cihazda Linux

Masaüstünden mobil cihazlara kadar **her cihaz türü** için bir Linux sürümü mevcuttur.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Linux ve Bulut: Maliyet ve Güvenlik

<div class="two-columns">

<div>

## 💰 Maliyet Etkinliği

- Linux çekirdeği **tamamen ücretsiz**
- En güç verimli işletim sistemlerinden biri
- Kullanıcı lisans ücreti yok
- Ticari dağıtımlar bile rakiplerden ucuz

## 🛠️ Yönetilebilirlik

- Linux yönetimi temel BT becerisi
- C tabanlı yapı → otomasyon araçlarına uygun
- Sunucuların çoğu **otomatik** yönetilir

</div>

<div>

## 🔒 Güvenlik

<div class="highlight-box">

### 💡 Linux Güvenlik Avantajı

- Açık kaynak: kod herkes tarafından incelenebilir
- Güvenlik açıkları topluluk tarafından hızla tespit edilir

</div>

<div class="info-box">

### 🎓 Açık Kaynak = Güvenlik

Kaynak kodun açık olması, geniş topluluk tarafından güvenlik açıklarının incelenmesini sağlar.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Sanallaştırma ve Konteynerler

---

![bg](../gorseller/3_normal_slayt.png)
# Sanallaştırma Temelleri

<div class="two-columns">

<div>

## 🖥️ Sanallaştırma Nedir?

Bir fiziksel bilgisayar (**host**) üzerinde birden fazla işletim sistemi kopyası (**guest**) çalıştırma.

**Hypervisor:** Guest'ler arası kaynak dağıtan yazılım.

**Avantajlar:**
- Tek host'ta düzinelerce guest
- Güç ve alan tasarrufu
- Farklı OS'ler aynı anda

</div>

<div>

**Araçlar:**
- **VMware Workstation**
- **Oracle VirtualBox**
- **Bare metal hypervisor**

<div class="info-box">

### 💡 Bulut ve Sanallaştırma

Sanal makineler uzak veri merkezinde barındırılır, sadece kullanılan kaynaklar için ödeme yapılır. **Ölçek ekonomisi** sayesinde düşük fiyatlar sunulur.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Konteynerler: Docker ve Kubernetes

<div class="two-columns">

<div>

## 📦 Konteynerizasyon

Geleneksel sanallaştırmanın ötesinde yeni bir yaklaşım.

**Konteyner:**
- Tek bir işlev (veritabanı, depolama vb.)
- İşletim sistemi yükü olmadan çalışır
- Otomatik oluşturulup yok edilebilir

**Yapı:**
- **Konteynerler** → Pod'lar içinde
- **Pod'lar** → Node'lar içinde
- **Node'lar** → Master node yönetiminde

</div>

<div>

<div class="highlight-box">

### 💡 Docker ve Kubernetes

**Docker:** Konteynerleri oluşturma ve çalıştırma
**Kubernetes:** Konteynerlerin orkestrasyon ve yönetimi

Her bileşen birbirinden **bağımsız** çalışır.

</div>

<div class="info-box">

### 🎓 Geleceğin Altyapısı

Bu mimari geleneksel OS ihtiyacını azaltsa da, altta yatan teknoloji hâlâ **Linux**'tur.

</div>

</div>

</div>

---

<!-- _class: final-slide -->

# Teşekkürler!

### Linux'ta Çalışmak
**Kapadokya Üniversitesi**
Veri Bilimi ve Analizi Bölümü
bekir.agirgun@kapadokya.edu.tr
