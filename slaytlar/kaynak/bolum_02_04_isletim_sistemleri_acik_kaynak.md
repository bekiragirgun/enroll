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

  /* Logo artık 3_normal_slayt.png arka planında mevcut */

  h1 {
    color: #2D4A7C;
    font-size: 24pt;
    font-weight: bold;
    margin-bottom: 20px;
    margin-left: 350px;
    padding-bottom: 10px;
    border-bottom: none !important;
    text-align: left;
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

  /* Haftalık Konu Slaytı (2. slayt) */
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

  img {
    max-width: 100%;
    max-height: 400px;
    object-fit: contain;
  }

---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# İşletim Sistemleri

Dr. Bekir Ağırgün

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Açık Kaynak Kodlu Yazılım

---

![bg](../gorseller/3_normal_slayt.png)
# Yazılım Lisanslama Temelleri

<div class="two-columns">

<div>

## 📋 Yazılım Bileşenleri

Yazılım satın alırken üç farklı bileşen vardır:

**Mülkiyet**
- Fikri mülkiyet hakları
- Yaratıcı/şirket sahipliği
- Telif hakkı koruması

**Para Transferi**
- İş modeli çeşitleri
- Ödeme yapıları
- Dağıtım yöntemleri

</div>

<div>

**Lisanslama**
- Kullanım hakları
- Yeniden dağıtım koşulları
- Değiştirme izinleri

<div class="highlight-box">

### 💡 Kritik Nokta

**Lisanslama, açık kaynak ile kapalı kaynak yazılımı ayırır**

Yazılımla ne yapabileceğinizi belirleyen fiyat etiketi değil, lisanstır!

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)
# Kapalı Kaynak vs Açık Kaynak

<div class="two-columns">

<div class="compare-box">

## 🔒 Kapalı Kaynak: Microsoft Windows

- Microsoft fikri mülkiyete sahip
- EULA (Son Kullanıcı Lisans Sözleşmesi)
- Sadece binary dağıtımı
- Tek bilgisayar kurulumu
- Kaynak koduna erişim yok
- Tersine mühendislik yasak
- Kopya başına ücret

</div>

<div class="compare-box">

## 🔓 Açık Kaynak: Linux Çekirdeği

- Linus Torvalds sahip
- GPLv2 Lisansı
- Kaynak kod erişimi zorunlu
- Sınırsız dağıtım
- Değiştirmek serbest
- Değişiklikleri paylaşma zorunlu
- Sadece dağıtım maliyeti

</div>

</div>

<div class="info-box">

### 🎓 Temel İlke

**FOSS (Free and Open Source Software)** yaratıcının belirli haklardan vazgeçtiği anlamına gelir - herkes kaynak kodunu görebilir ve yeniden dağıtabilir.

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Özgür Yazılım Vakfı (FSF)

---

![bg](../gorseller/3_normal_slayt.png)
# Özgür Yazılım Vakfı (FSF)

<div class="two-columns">

<div>

## 📅 Tarih ve Felsefe

**Kuruluş:** 1985, Richard Stallman

**Temel İnanç:**
- Fiyattan ziyade özgürlük
- "Özgür bira değil, özgür konuşma"
- Teknoloji üzerinde kullanıcı kontrolü
- Şeffaf, incelenebilir kod

**Copyleft Kavramı:**
- Değiştirilmiş versiyonlar da özgür kalmalı
- İyileştirmeleri paylaşma zorunlu
- Topluluk hesap verebilirliği

</div>

<div>

<div class="highlight-box">

### 💡 FSF Misyonu

**"Kullanıcılar evlerimizde, okullarımızda ve işyerlerimizde kullandığımız teknoloji üzerinde kontrole sahip olmalı"**

Özgürlükler:
- Yazılımı **paylaşma**
- Kaynak kodunu **inceleme**
- İhtiyaca göre **değiştirme**
- Değişiklikleri **dağıtma**

</div>

## 📜 FSF Lisansları

- GNU GPL v2 & v3
- GNU LGPL v2 & v3
- Güçlü copyleft koruması
- Tivoization önleme (GPLv3)

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Açık Kaynak Girişimi (OSI)

---

![bg](../gorseller/3_normal_slayt.png)
# Açık Kaynak Girişimi (OSI)

<div class="two-columns">

<div>

## 🌐 Oluşum ve Felsefe

**Kuruluş:** 1998
**Kurucular:** Bruce Perens & Eric Raymond

**FSF'den Farkları:**
- Daha az politik yüklü
- Daha izin verici yaklaşım
- Copyleft zorunlu değil
- İş dostu lisanslama

**OSI Onay Süreci:**
- Lisansları inceler
- "Açık kaynak" olarak sertifikalandırır
- Onaylı liste tutar
- İlkeler belirler, lisans oluşturmaz

</div>

<div>

<div class="info-box">

### 🎓 BSD Lisans Örneği

**Berkeley Software Distribution**

**İzinler:**
- Özgürce yeniden dağıt
- İhtiyaç halinde değiştir
- Ticari kullan
- Kapalı kaynak yapılabilir

**Gereksinimler:**
- Telif bildirimlerini koru
- Yazarlığı üstlenme
- Onay ima etme

</div>

<div class="highlight-box">

### 💡 İzin Verici vs Copyleft

**İzin Verici:** Kapalı türevler oluşturulabilir
**Copyleft:** Açık kaynak kalmalı

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# FOSS, FLOSS ve Lisans Türleri

---

![bg](../gorseller/3_normal_slayt.png)
# FOSS, FLOSS ve Lisans Türleri

<div class="two-columns">

<div>

## 🔤 Terminoloji

**FOSS:** Free and Open Source Software
(Özgür ve Açık Kaynak Yazılım)

**FLOSS:** Free/Libre/Open Source Software
- Netlik için "Libre" ekler
- İngilizcede "Free" belirsiz
- Özgürlük vs. bedava

<div class="info-box">

### 🎓 Topluluk Anlaşması

Topluluk FSF ve OSI kampları arasındaki felsefi tartışmalardan kaçınmak için **FOSS** ve **FLOSS** terimlerini toplu olarak kullanır.

</div>

</div>

<div>

## 📊 Lisans Karşılaştırması

| Özellik | GPL | BSD | MIT |
|---------|-----|-----|-----|
| **Açık Kaynak** | ✅ | ✅ | ✅ |
| **Copyleft** | ✅ | ❌ | ❌ |
| **Ticari Kullanım** | ✅ | ✅ | ✅ |
| **Kapalı Türevler** | ❌ | ✅ | ✅ |
| **Değişiklikleri Paylaş** | Zorunlu | İsteğe bağlı | İsteğe bağlı |

<div class="highlight-box">

### 💡 Önemli Nokta

**Tüm FOSS lisansları açık kaynaktır, ancak tüm açık kaynak lisansları copyleft ilkelerini uygulamaz**

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Creative Commons Lisanslama

---

![bg](../gorseller/3_normal_slayt.png)
# Creative Commons Lisanslama

<div class="two-columns">

<div>

## 🎨 Yazılımın Ötesinde

**Amaç:** Yazılım dışı içerikleri lisansla
- Belgeler, görseller, müzik
- Eğitim materyalleri
- Sanatsal eserler

## 📋 Lisans Bileşenleri

**BY** - İsim Belirtme (zorunlu)
**SA** - Aynı Koşullarla Paylaş (copyleft)
**NC** - Ticari Olmayan
**ND** - Türev Çalışma Yapılamaz

</div>

<div>

## 🔧 Altı Ana Lisans

1. **CC BY** - BSD benzeri, atıf gerekli
2. **CC BY-SA** - Copyleft versiyonu
3. **CC BY-ND** - Değişiklik yapılamaz
4. **CC BY-NC** - Sadece ticari olmayan
5. **CC BY-NC-SA** - NC + copyleft
6. **CC BY-NC-ND** - NC + değişiklik yok

**CC0** - Kamu malı bağışı

<div class="info-box">

### 🎓 Kullanım Notu

Creative Commons, FOSS ilkelerini yaratıcı eserler için uyarlayarak yazılım lisanslarının ele almadığı boşluğu doldurur.

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# UNIX Tarihi ve Linux Evrimi

---

![bg](../gorseller/3_normal_slayt.png)
# UNIX Tarihi ve Linux Evrimi

<div class="two-columns">

<div>

## 📅 UNIX Zaman Çizelgesi

**1969** - UNIX yaratıldı
**1973** - C dilinde yeniden yazıldı
**1984** - Berkeley 4.2BSD (TCP/IP)
**1990'lar başı** - X/Open standartları

## 🐧 Linux'un Ortaya Çıkışı

**Ana Faktörler:**
- Tescilli UNIX hakimiyeti
- C programlama dili
- İnternet büyümesi
- Geliştirici topluluğu

</div>

<div>

**Başarı Faktörleri:**
- Stabilite ve sağlamlık
- Maliyet etkinliği
- Açık işbirliği
- Standartlara uyum

<div class="highlight-box">

### 💡 Tarihsel Etki

**Linux tamamen açık kaynak olarak UNIX tasarımını yansıtır**

Bu kombinasyon çekti:
- Kurumsal kullanıcılar
- Üniversiteler
- Devlet kurumları
- Bağımsız geliştiriciler

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Açık Kaynak İş Modelleri

---

![bg](../gorseller/3_normal_slayt.png)
# Açık Kaynak İş Modelleri

<div class="two-columns">

<div>

## 💰 FOSS ile Para Kazanma

**Temel Bilgi:**
- GPL yazılım satışına izin verir
- "Özgür" özgürlük demek, fiyat değil
- Katma değer hizmetleri karlı

## 🏢 İş Stratejileri

**Destek ve Garanti**
- Red Hat, Canonical
- Kurumsal yönetim araçları
- Eğitim ve sertifikasyon

**Donanım Entegrasyonu**
- TiVo, gömülü sistemler
- IoT cihazları, DVR'lar
- Tüketici elektroniği

</div>

<div>

**Yazılım Geliştirme**
- Projelere katkı
- Endüstri yönü belirleme
- Dahili kullanım faydaları

<div class="info-box">

### 🎓 Wireshark Örnek Çalışması

**Gerald Combs** tarafından 1990'larda ağ analiz aracı olarak başladı. Şimdi:
- 600+ katkıda bulunan
- Ticari araçlardan daha iyi
- Başarılı şirket kurdu
- Daha büyük kuruluş tarafından satın alındı

</div>

<div class="highlight-box">

### 💡 Modern Gerçeklik

**Milyarlarca dolarlık endüstri: DVR'lar, güvenlik kameraları, fitness cihazları, bulut hizmetleri**

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Hobiden Kurumsal Uygulamaya

---

![bg](../gorseller/3_normal_slayt.png)
# Hobiden Kurumsal Uygulamaya

<div class="two-columns">

<div>

## 🎯 Kurumsal Benimseme Yolculuğu

**Başlangıç Şüphesi:**
- "Bedava" yazılıma şüphe
- Kanıtlanmamış iş modeli
- Kalite endişeleri

**Gerçeklik:**
- En iyi programcılar Linux'ta çalışıyor
- Tescilli sistemlerden üstün performans
- Maliyet etkin yükseltmeler
- Kanıtlanmış güvenilirlik

**Modern Manzara:**
- Büyük organizasyonlar FOSS'u benimsiyor
- Açık kaynak için özel ekipler
- Rekabet avantajı
- Endüstri standardı platformlar

</div>

<div>

<div class="highlight-box">

### 💡 Dönüm Noktası

**Linux'u hobi olarak kullanan mühendisler şirketlerini profesyonel olarak benimsemeye ikna etti**

Bu tabandan gelen benimseme, geleneksel satış yaklaşımlarından daha etkili oldu.

</div>

<div class="info-box">

### 🎓 Başarı Faktörleri

**Stabilite** - Güvenilir sunucu performansı
**Geliştirme** - Kolay uygulama yaratma
**Topluluk** - Küresel işbirliği
**Maliyet** - Ekonomik altyapı
**Standartlar** - Platformlar arası uyum

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Açık Kaynağın Etkisi

---

![bg](../gorseller/3_normal_slayt.png)
# Açık Kaynağın Etkisi

<div class="two-columns">

<div>

## 🌍 Küresel Dönüşüm

**Teknik Etki:**
- İnternet altyapısı
- Bulut bilişim omurgası
- Mobil cihaz temeli (Android)
- Süper bilgisayar hakimiyeti

**Sosyal Etki:**
- Demokratik yazılım geliştirme
- Bilgi paylaşım kültürü
- Eğitim erişilebilirliği
- İnovasyon hızlanması

**Ekonomik Etki:**
- Milyarlarca dolarlık endüstri
- Dünya çapında iş yaratma
- Düşük yazılım maliyetleri
- Yeni iş modelleri

</div>

<div>

<div class="highlight-box">

### 💡 Gelecek Görünümü

**Bilgisayardaki her yenilik başkalarının çalışmaları üzerine inşa edilir**

Açık kaynak sağlar:
- Sınırlar arası **işbirliği**
- Birlikte çalışabilirlik için **standartlar**
- Ölçekte **yenilik**
- Herkes için **erişilebilirlik**

</div>

<div class="info-box">

### 🎓 Temel İlke

**"Devlerin omuzlarında durmak"**

Açık kaynak yazılım, insanlığın teknolojiye işbirlikçi yaklaşımını temsil eder - herhangi bir bireyin tek başına başarabileceğinden daha büyük bir şey yaratmak için bilgi paylaşımı.

</div>

</div>

</div>

---

<!-- _class: final-slide -->

# Teşekkürler!
