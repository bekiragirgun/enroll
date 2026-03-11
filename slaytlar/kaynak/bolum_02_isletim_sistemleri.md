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

# İşletim Sistemleri

**Kapadokya Üniversitesi**
Veri Bilimi ve Analizi Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# İşletim Sistemleri Nedir?

---

![bg](../gorseller/3_normal_slayt.png)
# İşletim Sistemi Tanımı

<div class="two-columns">

<div>

## 🖥️ Temel Tanım

İşletim sistemi, bir bilgi işlem cihazında çalışan ve **donanım ile yazılım bileşenlerini yöneten** yazılımdır.

**Modern işletim sistemleri:**
- Çoklu görev yönetimi (multitasking)
- Donanım kaynak paylaşımı
- Standart hizmet sunumu
- Kullanıcı isteklerini işleme

**Üç Büyük İşletim Sistemi:**
- Microsoft Windows
- Apple macOS
- Linux

</div>

<div>

![w:360](../../06_KAYNAKLAR/LEv2_2_1.png)

<div class="info-box">

### 💡 Katmanlı Yapı

Kullanıcılar → Uygulamalar → İşletim Sistemi → Donanım

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Üç Büyük İşletim Sistemi

<div class="two-columns">

<div>

## 🔍 Temel Karşılaştırma

| Özellik | Windows | macOS | Linux |
|---------|---------|-------|-------|
| **Kod Tabanı** | Tescilli | BSD/UNIX | Açık Kaynak |
| **Yönetim** | GUI ağırlıklı | GUI + CLI | CLI ağırlıklı |
| **Donanım** | Çoklu üretici | Sadece Apple | Çoklu üretici |
| **Lisans** | Ücretli | Apple ile gelir | Ücretsiz |

</div>

<div>

<div class="highlight-box">

### 💡 Önemli Bilgi

**Sadece Windows** tamamen tescilli kod tabanına sahiptir. macOS, BSD Unix tabanlı UNIX sertifikalı bir sistemdir. Linux ise yüzlerce farklı dağıtım ile gelir.

</div>

<div class="compare-box">

### 🎓 Yönetim Farkı

Windows çoğunlukla GUI ile yönetilirken, Linux ve UNIX sistemlerde **terminal komutları** (CLI) birincil yönetim aracıdır.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# İşletim Sistemi Seçim Kriterleri

---

![bg](../gorseller/3_normal_slayt.png)
# Rol, İşlev ve Yaşam Döngüsü

<div class="two-columns">

<div>

## 🎯 Rol (Role)

**Masaüstü mü, Sunucu mu?**
- **Masaüstü:** GUI, verimlilik uygulamaları, web tarama
- **Sunucu:** CLI, uzak erişim, kaynak sunma
- Sunucular genellikle raf içinde, paylaşılan klavye/monitör

## ⚙️ İşlev (Function)

- Hangi yazılımlar çalışacak?
- Kaç makine aynı anda çalışacak?
- Yönetim ekibinin yetkinliği nedir?

</div>

<div>

## 🔄 Yaşam Döngüsü (Life Cycle)

**Sürüm Döngüsü:** Yazılım güncellemelerinin periyodu
**Bakım Döngüsü:** Destek süresi

<div class="info-box">

### 💡 Sanallaştırma

Modern veri merkezleri **sanallaştırma** ile tek fiziksel makinede düzinelerce hatta yüzlerce sanal makine barındırır. Bu:
- Alan ve güç tasarrufu sağlar
- Otomasyon imkanı sunar
- Donanım yükseltme ihtiyacını azaltır

</div>

**Bulut Hizmetleri:** AWS, Rackspace, Azure gibi sağlayıcılar fiziksel donanım ihtiyacını büyük ölçüde azaltmıştır.

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Kararlılık, Uyumluluk, Maliyet ve Arayüz

<div class="two-columns">

<div>

## 📊 Kararlılık (Stability)

- **Beta:** Yeni özellikler, test edilmemiş
- **Kararlı (Stable):** Sahada test edilmiş
- Üretim sunucuları genellikle kararlı sürüm kullanır
- Açık kaynak yazılım erken aşamada peer review alır

## 🔗 Geriye Dönük Uyumluluk

- Yeni sürümlerin eski yazılımlarla çalışması
- İşletim sistemi yükseltmesi gerektiğinde kritik
- Açık kaynak: uyumluluğu öncelik olarak korur

</div>

<div>

## 💰 Maliyet (Cost)

- Microsoft: yıllık lisans ücretleri
- Linux: genellikle ücretsiz, destek ücretli olabilir
- Sanallaştırma: sadece kullanılan kadar öde

## 🖱️ Arayüz (Interface)

<div class="highlight-box">

### 💡 GUI vs CLI

- **GUI:** Fare ve butonlarla etkileşim (1970'lerde Xerox PARC, 1980'lerde Apple)
- **CLI:** Metin tabanlı komut satırı, Linux'ta birincil yönetim aracı
- Günümüzde tüm işletim sistemleri her ikisini de sunar

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Microsoft Windows

---

![bg](../gorseller/3_normal_slayt.png)
# Microsoft Windows

<div class="two-columns">

<div>

## 🪟 Masaüstü ve Sunucu

**Masaüstü Sürüm:**
- Güncel sürüm: Windows 11
- 1985'ten bu yana 16 sürüm
- Geriye dönük uyumluluk öncelikli
- Sanal makine teknolojisi ile eski yazılım desteği

**Sunucu Sürüm:**
- Windows Server 2019+
- GUI veya Server Core (CLI)
- PowerShell ile güçlü komut satırı
- WSL (Windows Subsystem for Linux)

</div>

<div>

<div class="info-box">

### 💡 Önemli Gelişmeler

**PowerShell** ve **WSL** ile Microsoft, Linux'a rekabet yanıtı olarak komut satırı yeteneklerinde büyük ilerleme kaydetmiştir.

Ayrıca **Azure** bulut hizmeti kurumsal müşteriler için önemli bir entegrasyon noktasıdır.

</div>

<div class="compare-box">

### 🔄 Sürüm Döngüsü

Windows yeni sürümleri **birkaç yılda bir** çıkarır. Linux dağıtımları ise genellikle **yılda iki kez** (Mart ve Eylül) güncellenir.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Apple macOS

---

![bg](../gorseller/3_normal_slayt.png)
# Apple macOS

<div class="two-columns">

<div>

## 🍎 Masaüstü ve Sunucu

**macOS Masaüstü:**
- FreeBSD tabanlı, UNIX sertifikalı
- "Kullanımı kolay" felsefesi
- Okullar ve küçük işletmelerde popüler
- Programcılar arasında çok tercih edilen
- Yaratıcı endüstrilerde (grafik, video) standart

**macOS Server:**
- Küçük organizasyonlar için
- Düşük maliyetli eklenti
- iOS cihaz entegrasyonu
- Kaynak paylaşım yönetimi

</div>

<div>

<div class="highlight-box">

### 💡 Neden Tercih Ediliyor?

- **Programcılar:** Sağlam UNIX altyapısı
- **Yaratıcılar:** Kararlı platform, uyumluluk
- **IT Departmanları:** Daha az destek ihtiyacı
- **Donanım:** İşletim sistemi ile sıkı entegrasyon

</div>

<div class="info-box">

### 🎓 Apple Avantajı

Apple donanımı işletim sistemiyle çok sıkı entegre çalışır. Uygulama programlama **standartlarına uyum** sayesinde yaratıcı profesyonellere kararlı bir platform sunar.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Linux

---

![bg](../gorseller/3_normal_slayt.png)
# Linux Dağıtımları

<div class="two-columns">

<div>

## 🐧 Linux Dağıtımı Nedir?

Bir Linux dağıtımı şunları içerir:
- **Linux çekirdeği** (kernel)
- Yardımcı araçlar ve yönetim yazılımları
- Uygulama yazılımları
- Paket yöneticisi
- Güncelleme ve güvenlik yamaları

**Dağıtım şunları yapar:**
- Depolama alanını ayarlar
- Çekirdeği derler ve kurar
- Donanım sürücülerini yükler
- Uygulamaları kurar

</div>

<div>

![w:400](../../06_KAYNAKLAR/LEv2_2_2.png)

<div class="highlight-box">

### 💡 GUI ve CLI

Linux hem GUI hem de CLI arayüz sunar. GUI'de birden fazla terminal penceresi açılarak uzak sunucular yönetilebilir.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Linux Seçim Kriterleri

<div class="two-columns">

<div>

## 🎯 Rol ve İşlev

**Rol seçenekleri:**
- Geleneksel sunucu veya masaüstü
- Ağ güvenlik duvarı
- Süper bilgisayar
- Gömülü sistemler
- POS (Satış noktası) sistemleri

**İşlev:**
- Devlet ve büyük kurumlar ticari destek tercih eder
- Güvenlik: Açık kaynak topluluk denetimi
- Firefox, LibreOffice gibi uygulamalar tüm dağıtımlarda mevcut

</div>

<div>

## 🔄 Yaşam Döngüsü

**İki kategori:**
- **Meraklı (Enthusiast):** Hızlı güncelleme, kısa destek
  - openSUSE Tumbleweed, Fedora, Ubuntu Desktop
- **Kurumsal (Enterprise):** Kararlı, uzun destek (5-13 yıl)
  - Red Hat, Canonical, SUSE

<div class="info-box">

### 💡 LTS (Uzun Süreli Destek)

Bazı sürümler **5 yıl veya daha fazla** desteklenirken, diğerleri sadece 2 yıl veya daha az destek alır. Kurumsal ortamlarda LTS sürümleri tercih edilir.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Başlıca Linux Dağıtımları

---

![bg](../gorseller/3_normal_slayt.png)
# Red Hat ve SUSE Aileleri

<div class="two-columns">

<div>

## 🎩 Red Hat

- **RPM** paket yöneticisini tanıttı
- **RHEL:** Kurumsal, ücretli, uzun sürüm döngüsü
- **Fedora:** Topluluk projesi, en yeni yazılımlar
- **CentOS:** RHEL'in ücretsiz yeniden derlemesi
- **Scientific Linux:** Bilimsel hesaplama (CERN)

<div class="compare-box">

### 🔄 Akış

Fedora → Test → RHEL → CentOS (ücretsiz)

</div>

</div>

<div>

## 🦎 SUSE

- Slackware'den türetilmiş
- RHEL ile birçok benzerlik
- Novell → Attachmate → Micro Focus → Bağımsız (2018)
- **SLES:** Kurumsal, tescilli kod içerir
- **openSUSE:** Tamamen açık ve ücretsiz

<div class="info-box">

### 💡 Topluluk → Kurumsal

Hem Fedora→RHEL hem de openSUSE→SLES ilişkisinde topluluk sürümü, kurumsal sürüm için **test ortamı** görevi görür.

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Debian, Ubuntu ve Diğerleri

<div class="two-columns">

<div>

## 🌀 Debian Ailesi

**Debian:**
- Topluluk odaklı, standartlara bağlı
- **.deb** paket formatı
- Çoklu platform desteği (Intel dışı)

**Ubuntu:**
- En popüler Debian türevi (Canonical)
- Masaüstü, sunucu ve özel sürümler
- LTS: Masaüstü 3 yıl, Sunucu 5 yıl

**Linux Mint:** Ubuntu çatalı, tescilli codec desteği

</div>

<div>

## 🤖 Android ve Diğerleri

**Android:**
- Google sponsorluğunda, en popüler Linux dağıtımı
- Dalvik sanal makinesi kullanır
- Masaüstü Linux ile **uyumsuz**

**Raspberry Pi:** Eğitim ve prototipleme için düşük maliyetli platform

<div class="info-box">

### 💡 Dağıtım Çeşitliliği

Yüzlerce Linux dağıtımı mevcut, ancak birçok program ve komut **aynı veya çok benzer** kalır.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Gömülü Sistemler ve IoT

---

![bg](../gorseller/3_normal_slayt.png)
# Gömülü Linux ve Nesnelerin İnterneti

<div class="two-columns">

<div>

## 🔌 Gömülü Sistemler

**Tarihçe:**
- Linux başlangıçta sadece Intel 386 PC'de çalışıyordu
- Topluluk katkılarıyla diğer donanımlar da desteklendi
- Küçük boyut, düşük güç tüketimi odaklı çipler

**Kullanım Alanları:**
- Cep telefonları ve akıllı TV'ler
- Uzaktan izleme sistemleri
- Dijital video kaydediciler (DVR)
- Güvenlik kameraları
- Fitness cihazları

</div>

<div>

## 🌐 Nesnelerin İnterneti (IoT)

<div class="info-box">

### 💡 IoT Devrimi

Ucuz, her yerde bulunan akıllı sensörler ve kontrolörler:
- Petrol kuyularından güneş enerjisi çiftliklerine
- **Gerçek zamanlı** süreç ayarlama
- Merkezi kontrol istasyonlarına raporlama
- **Makine öğrenimi** ve **yapay zeka** ile entegrasyon

</div>

**Raspberry Pi Etkisi:**
- Ucuz, küçük, uyarlanabilir tek kart bilgisayar
- Hızlı prototipleme imkanı
- Eğitimciler tarafından çok tercih edilen
- Çevre izlemeden robotik tasarıma kadar kullanım

</div>

</div>

---

<!-- _class: final-slide -->

# Teşekkürler!

### İşletim Sistemleri
**Kapadokya Üniversitesi**
Veri Bilimi ve Analizi Bölümü
bekir.agirgun@kapadokya.edu.tr
