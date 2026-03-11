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

  .two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-top: 20px;
    overflow: hidden;
  }

  .subtitle-box {
    background-color: #E6EAF3;
    padding: 15px 18px;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    margin-bottom: 20px;
  }

  .info-box {
    background-color: #FFFFFF;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    margin-bottom: 15px;
    overflow: hidden;
    word-wrap: break-word;
  }

  .info-box h3 {
    margin-top: 0;
    font-size: 12pt;
  }

  .info-box ul {
    margin: 8px 0;
    padding-left: 18px;
  }

  .info-box li {
    font-size: 10pt;
    line-height: 1.5;
    margin: 5px 0;
  }

  .highlight-box {
    background-color: #6B9FE8;
    color: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 3px solid #4A90E2;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
    margin-bottom: 15px;
    overflow: hidden;
    word-wrap: break-word;
  }

  .highlight-box h3,
  .highlight-box h2,
  .highlight-box h1,
  .highlight-box p,
  .highlight-box li,
  .highlight-box strong {
    color: white !important;
  }

  .highlight-box h3 {
    font-size: 12pt;
    margin-top: 0;
  }

  .highlight-box p {
    font-size: 10pt;
    line-height: 1.5;
  }

  .compare-box {
    background-color: #F5F5F5;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    overflow: hidden;
    word-wrap: break-word;
  }

  .compare-box h3 {
    font-size: 12pt;
    margin-top: 0;
  }

  .compare-box ul {
    margin: 8px 0;
    padding-left: 18px;
  }

  .compare-box li {
    font-size: 10pt;
    line-height: 1.5;
    margin: 5px 0;
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
    max-height: 450px;
    object-fit: contain;
  }

  table {
    font-size: 10pt;
    width: 100%;
    overflow: hidden;
    display: block;
  }

  footer {
    font-size: 9pt;
    color: #666;
    text-align: center;
  }
---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Linux'e Giriş

**Açık Kaynak Yazılım ve Linux Temelleri**

<br>

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Open Source & Licensing

---

![bg](../gorseller/3_normal_slayt.png)

# 📖 Open Source Software: Tanım ve Temel Kavramlar

<div class="two-columns">

<div>

<div class="info-box">

### 💡 Açık Kaynak Nedir?

**Open Source Software (OSS)**, kaynak kodunun herkes tarafından görülebilir, incelenebilir, değiştirilebilir ve dağıtılabilir olduğu yazılım geliştirme modelidir.

**Temel Prensipler:**
- Kaynak kodu serbestçe erişilebilir
- Herkes kodu inceleyebilir
- Değişiklik yapma hakkı
- Kopyalama ve dağıtım özgürlüğü
- Ticari kullanım mümkün

</div>

<div class="info-box">

### 🆓 Free Software vs Open Source

**Free Software (Özgür Yazılım):**
- FSF (Free Software Foundation) felsefesi
- Özgürlük odaklı
- "Free as in freedom"

**Open Source:**
- OSI (Open Source Initiative) tanımı
- Pratik faydalar odaklı
- İş dünyası dostu yaklaşım

</div>

</div>

<div>

<div class="highlight-box">

### 🔑 4 Temel Özgürlük (FSF)

**Özgürlük 0**: Programı herhangi bir amaç için çalıştırma özgürlüğü

**Özgürlük 1**: Programın nasıl çalıştığını inceleme ve ihtiyaçlarınıza göre değiştirme özgürlüğü (kaynak kodu erişimi ön koşuldur)

**Özgürlük 2**: Programın kopyalarını dağıtarak başkalarına yardım etme özgürlüğü

**Özgürlük 3**: Programın değiştirilmiş versiyonlarını başkalarına dağıtma özgürlüğü (böylece toplumun tamamı değişikliklerden faydalanabilir)

</div>

</div>

</div>

---

# 🌍 Açık Kaynak Tarihi ve Evrimi

<div class="two-columns">

<div>

<div class="info-box">

### 📅 Önemli Dönüm Noktaları

**1950-1960'lar: Başlangıç**
- Yazılım donanımla birlikte gelir
- Kaynak kodu paylaşılır
- Akademik işbirliği yaygın

**1970'ler: Ticari Dönüşüm**
- Yazılım ayrı bir ürün olur
- Kapalı kaynak modeli başlar
- AT&T UNIX'i lisanslar

**1980'ler: Özgür Yazılım Hareketi**
- 1983: Richard Stallman GNU Project'i başlatır
- 1985: Free Software Foundation kurulur
- 1989: GPL lisansı yayınlanır

</div>

</div>

<div>

<div class="info-box">

### 🚀 Modern Dönem

**1990'lar: Linux Devrimi**
- 1991: Linus Torvalds Linux Kernel'i yaratır
- 1993: Debian kurulur
- 1998: "Open Source" terimi ortaya çıkar
- 1998: OSI (Open Source Initiative) kurulur

**2000'ler: Ana Akım Kabul**
- Apache, MySQL, PHP yaygınlaşır
- Büyük şirketler açık kaynağa yönelir
- GitHub (2008) sosyal kodlamayı başlatır

**2010'lar ve Sonrası**
- Cloud computing ve açık kaynak
- Kubernetes, Docker popülerleşir
- Microsoft GitHub'ı satın alır (2018)

</div>

</div>

</div>

---

# 💪 Açık Kaynak Yazılımın Avantajları

<div class="two-columns">

<div>

<div class="highlight-box">

### 💰 Ekonomik Faydalar

**Düşük Maliyet:**
- Lisans ücreti yok
- Sınırsız kurulum
- Maliyet tahmin edilebilir

**TCO (Total Cost of Ownership):**
- Başlangıç maliyeti düşük
- Bakım maliyeti kontrol edilebilir
- Satıcı kilitlenmesi (vendor lock-in) yok

</div>

<div class="info-box">

### 🔒 Güvenlik ve Güvenilirlik

**Şeffaflık:**
- Kod herkes tarafından incelenebilir
- Gizli backdoor riski minimum
- Güvenlik açıkları hızla bulunur

**Community Review:**
- Binlerce göz kodu inceler
- "Many eyes" prensibi
- Hızlı güvenlik güncellemeleri

</div>

</div>

<div>

<div class="info-box">

### 🛠️ Teknik Avantajlar

**Esneklik ve Özelleştirme:**
- Kaynak koda tam erişim
- İhtiyaca göre değiştirme
- Özel özellikler eklenebilir

**Bağımsızlık:**
- Satıcıya bağımlılık yok
- Kendi yolunuzu çizebilirsiniz
- Uzun vadeli kontrol

**Standartlara Uyum:**
- Açık standartları destekler
- İnteroperabilite yüksek
- Platform bağımsız

</div>

<div class="info-box">

### 🌐 Topluluk ve Ekosistem

**Geniş Destek:**
- Forumlar ve mail listeleri
- Detaylı dokümantasyon
- Stack Overflow, GitHub

**İnovasyon:**
- Hızlı geliştirme döngüsü
- Topluluk katkıları
- Cutting-edge teknolojiler

</div>

</div>

</div>

---

# ⚖️ GPL (GNU General Public License)

<div class="two-columns">

<div>

<div class="info-box">

### 📜 GPL Nedir?

**Copyleft Lisansı** - En güçlü açık kaynak lisansı

**Temel Özellikler:**
- FSF tarafından oluşturuldu
- Özgürlükleri koruma odaklı
- Türev çalışmalar da GPL olmalı
- "Viral" lisans olarak bilinir

**Versiyonlar:**
- **GPLv1** (1989): İlk versiyon
- **GPLv2** (1991): Linux Kernel kullanır
- **GPLv3** (2007): Patent koruması eklendi

</div>

<div class="highlight-box">

### 🔐 Copyleft Kavramı

**Copyleft**, telif hakkının yazılımı özgür tutmak için kullanılmasıdır.

**Çalışma Prensibi:**
- Özgürlükleri garanti eder
- Türev çalışmaların da özgür olmasını zorunlu kılar
- "Kapalı kaynağa dönüştürülemez"

**GPL'in Gücü:**
- Özgürlükleri korur
- Topluluk ekosistemini güçlendirir
- Ticari sömürüyü engeller

</div>

</div>

<div>

<div class="info-box">

### ✅ GPL Yükümlülükleri

**Kaynak Kodu Paylaşımı:**
- GPL yazılımı dağıtırsanız kaynak kod zorunlu
- Aynı medyumda veya yazılı teklif ile

**Değişiklikleri Belgeleme:**
- Yaptığınız değişiklikleri işaretleyin
- Değişiklik tarihlerini kaydedin

**Lisans Bilgisi:**
- GPL metnini ekleyin
- Telif hakkı bilgilerini koruyun

**Türev Çalışmalar:**
- GPL ile lisanslanmalı
- Özgürlükler korunmalı

</div>

<div class="info-box">

### 🎯 GPL Kullanan Projeler

**İşletim Sistemleri:**
- Linux Kernel (GPLv2)
- GNU Utilities
- Bash Shell

**Geliştirme Araçları:**
- GCC (GNU Compiler Collection)
- Git (Version Control)
- GDB (Debugger)

**Uygulamalar:**
- GIMP (Image Editor)
- Inkscape (Vector Graphics)
- WordPress (GPLv2+)

</div>

</div>

</div>

---

# 🔓 BSD ve MIT Lisansları

<div class="two-columns">

<div>

<div class="info-box">

### 🎯 BSD License

**Permissive License** - Minimal kısıtlama

**Berkeley Software Distribution kökenli**

**Özellikler:**
- Çok kısa ve basit
- Ticari kullanıma açık
- Kaynak kodu kapatılabilir
- Telif hakkı bildirimi yeterli

**Varyasyonlar:**
- **2-Clause BSD**: En basit form
- **3-Clause BSD**: "No endorsement" maddesi
- **4-Clause BSD**: Reklam maddesi (eski)

**BSD Kullanan Projeler:**
- FreeBSD, OpenBSD, NetBSD
- Nginx Web Server
- PostgreSQL Database

</div>

<div class="info-box">

### ⭐ MIT License

**En Popüler Permissive License**

**Massachusetts Institute of Technology**

**Özellikler:**
- Çok kısa (11 satır)
- Maksimum özgürlük
- Ticari kullanım serbest
- Sublicensing mümkün
- Guarantee disclaimer

**Neden Popüler?**
- Anlaşılması kolay
- Ticari dostlaşı
- Minimal yasal risk
- Şirketler tarafından tercih edilir

**MIT Kullanan Projeler:**
- Node.js, React, jQuery
- Ruby on Rails
- .NET Core

</div>

</div>

<div>

<div class="highlight-box">

### 🆚 GPL vs BSD/MIT Karşılaştırması

**GPL (Copyleft):**
- ✅ Özgürlükleri garanti eder
- ✅ Topluluk ekosistemini korur
- ❌ Ticari kullanımı zorlaştırabilir
- ❌ Karmaşık lisans uyumluluğu

**BSD/MIT (Permissive):**
- ✅ Ticari dostlaşı
- ✅ Basit ve anlaşılır
- ❌ Kapalı kaynağa dönüşebilir
- ❌ Katkılar geri dönmeyebilir

</div>

<div class="compare-box">

### 📊 Hangi Lisansı Seçmeli?

**GPL Seçin Eğer:**
- Özgürlükleri korumak istiyorsanız
- Topluluk ekosistemi önceliyse
- Copyleft felsefesine inanıyorsanız

**BSD/MIT Seçin Eğer:**
- Maksimum esneklik istiyorsanız
- Ticari adoption önemliyse
- Basitlik önceliyse

</div>

</div>

</div>

---

# 🎨 Creative Commons ve Diğer Lisanslar

<div class="two-columns">

<div>

<div class="info-box">

### 🎨 Creative Commons (CC)

**İçerik için açık lisanslama sistemi**

**Temel Bileşenler:**

**BY (Attribution)**: İsim belirtme zorunlu

**SA (ShareAlike)**: Aynı lisansla paylaşım

**NC (NonCommercial)**: Ticari kullanım yasak

**ND (NoDerivatives)**: Değiştirme yasak

**Yaygın Kombinasyonlar:**
- **CC BY**: Sadece isim belirtme
- **CC BY-SA**: İsim + Aynı lisans (Wikipedia)
- **CC BY-NC**: İsim + Ticari değil
- **CC0**: Public Domain (hiç kısıtlama yok)

</div>

<div class="info-box">

### 📄 Apache License 2.0

**Kurumsal açık kaynak lisansı**

**Özellikler:**
- Patent hakları açıkça tanımlı
- Trademark koruması
- Katkıda bulunan anlaşması
- Permissive ama detaylı

**Apache Kullanan Projeler:**
- Apache HTTP Server
- Kubernetes
- Android (kısmen)
- Hadoop, Spark

</div>

</div>

<div>

<div class="info-box">

### 🔄 LGPL (Lesser GPL)

**GPL'in daha esnek versiyonu**

**Kullanım Alanı:**
- Kütüphaneler (libraries) için
- Dinamik linklemeye izin verir
- GPL'den daha az kısıtlayıcı

**LGPL Kullanan Projeler:**
- GTK+ (UI Toolkit)
- Qt (kısmen)
- LibreOffice (kısmen)

</div>

<div class="info-box">

### 🌐 Mozilla Public License (MPL)

**File-level copyleft**

**Özellikler:**
- Dosya bazında copyleft
- Farklı lisanslarla mixing mümkün
- Patent koruması

**MPL Kullanan Projeler:**
- Firefox
- Thunderbird
- LibreOffice (tri-license)

</div>

<div class="highlight-box">

### ⚠️ Lisans Uyumluluğu

**Dikkat Edilmesi Gerekenler:**
- GPL ile permissive lisanslar birleştirilebilir
- GPL ile BSD/MIT birleştirilebilir → GPL
- GPL ile proprietary birleştirilemez
- Çoklu lisanslama (dual/tri-license) mümkün

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Linux Fundamentals

---

![bg](../gorseller/3_normal_slayt.png)

# 🐧 Linux: UNIX'in Modern Varisi

<div class="two-columns">

<div>

<div class="info-box">

### 🌳 UNIX Kökleri

**UNIX Tarihi (1969):**
- AT&T Bell Labs'da geliştirildi
- Ken Thompson ve Dennis Ritchie
- C dilinde yazıldı
- Portable ve modüler tasarım

**UNIX Felsefesi:**
- Her program bir işi iyi yapsın
- Programlar birlikte çalışsın
- Text stream evrensel arayüz
- "Everything is a file"

**UNIX Türevleri:**
- **Commercial**: Solaris, AIX, HP-UX
- **BSD Family**: FreeBSD, OpenBSD, NetBSD
- **Unix-like**: Linux, macOS

</div>

<div class="highlight-box">

### 🐧 Linux'un Doğuşu (1991)

**Linus Torvalds:**
- Fin bilgisayar bilimi öğrencisi
- MINIX alternatifi yaratmak istedi
- İlk sürüm: 0.01 (10,000 satır kod)

**İlk Duyuru (comp.os.minix):**
> "I'm doing a (free) operating system (just a hobby, won't be big and professional like gnu) for 386(486) AT clones."

**Hızlı Büyüme:**
- Topluluk katkıları
- GNU araçlarıyla birleşme
- GPL lisansı seçimi kritikti

</div>

</div>

<div>

<div class="info-box">

### 🏗️ Linux Mimarisi

**Kernel (Çekirdek):**
- Donanım yönetimi
- İşlem zamanlama
- Bellek yönetimi
- Dosya sistemi
- Ağ protokolleri

**GNU Userland:**
- Shell (bash, zsh)
- Core utilities (ls, cp, mv)
- Text editors (vim, emacs)
- Compilers (gcc)

**System Libraries:**
- glibc (C standard library)
- System call interface

**Desktop Environment:**
- X Window System / Wayland
- GNOME, KDE, XFCE

</div>

<div class="compare-box">

### 📊 Linux vs UNIX

**Benzerlikler:**
- POSIX uyumlu
- Çoklu kullanıcı/işlem
- Aynı komutlar
- Dosya sistemi yapısı

**Farklar:**
- Linux kernel'i yeni yazıldı
- GPL lisanslı (UNIX proprietary)
- Geniş donanım desteği
- Aktif topluluk geliştirmesi

</div>

</div>

</div>

---

# 📦 Linux Dağıtımları (Distributions)

<div class="two-columns">

<div>

<div class="info-box">

### 🎯 Dağıtım Nedir?

**Distribution (Distro):**
Linux kernel + GNU tools + package manager + applications + configuration

**Neden Farklı Dağıtımlar?**
- Farklı kullanım senaryoları
- Farklı felsefeler
- Farklı paket yönetimi
- Farklı release döngüleri

**Ana Dağıtım Aileleri:**
- **Debian-based**: apt/dpkg
- **Red Hat-based**: rpm/yum/dnf
- **Arch-based**: pacman
- **Independent**: Gentoo, Slackware

</div>

<div class="info-box">

### 🟦 Debian Ailesi

**Debian:**
- 1993'te kuruldu
- En kararlı dağıtım
- Geniş paket havuzu (59,000+)
- Tamamen topluluk destekli
- Release cycle: ~2 yıl

**Ubuntu:**
- 2004, Canonical sponsorluğunda
- Kullanıcı dostu
- 6 aylık release cycle
- LTS versiyonlar (5 yıl destek)
- Masaüstü ve sunucu versiyonları

**Linux Mint:**
- Ubuntu tabanlı
- Windows-like deneyim
- Çoklu media codec desteği

</div>

</div>

<div>

<div class="info-box">

### 🔴 Red Hat Ailesi

**Red Hat Enterprise Linux (RHEL):**
- Kurumsal çözüm
- Ücretli destek
- 10 yıl destek süresi
- Enterprise standart

**Fedora:**
- RHEL'in upstream'i
- Bleeding edge teknolojiler
- 6 aylık release
- Yenilikçi özellikler

**CentOS / Rocky Linux / AlmaLinux:**
- RHEL klonları
- Ücretsiz
- Sunucu kullanımı yaygın
- Binary compatible RHEL

</div>

<div class="info-box">

### ⚡ Diğer Önemli Dağıtımlar

**Arch Linux:**
- Rolling release
- Minimalist ve DIY
- Cutting edge packages
- Mükemmel dokümantasyon (Arch Wiki)

**openSUSE:**
- SUSE sponsorluğunda
- YaST configuration tool
- Kurumsal ve bireysel

**Gentoo:**
- Source-based
- Maksimum optimizasyon
- İleri seviye kullanıcılar

</div>

</div>

</div>

---

# 🎯 Hangi Linux Dağıtımını Seçmeli?

<div class="two-columns">

<div>

<div class="highlight-box">

### 🎓 Yeni Başlayanlar

**Ubuntu / Linux Mint:**
- Kolay kurulum
- Geniş donanım desteği
- Çok fazla dokümantasyon
- Büyük topluluk
- "Just works" prensibi

**Avantajları:**
- Kullanıcı dostu arayüz
- Hazır multimedia desteği
- Uygulama mağazası
- Windows'dan geçiş kolay

</div>

<div class="info-box">

### 💻 Geliştiriciler

**Fedora:**
- Güncel paketler
- Developer tools
- Hızlı innovation
- SELinux entegrasyonu

**Ubuntu LTS:**
- Stabil ve predictable
- Uzun destek süresi
- CI/CD friendly
- Docker/Kubernetes desteği

**Arch Linux:**
- Her şeyi öğrenmek isteyenler
- Minimal başlangıç
- AUR (Arch User Repository)

</div>

</div>

<div>

<div class="info-box">

### 🖥️ Sunucu Kullanımı

**Debian:**
- Rock solid stability
- Uzun destek süresi
- Güvenlik odaklı
- Minimal sistem kaynağı

**Ubuntu Server LTS:**
- Modern paketler
- Cloud-friendly
- Canonical desteği
- Geniş dökümantasyon

**Rocky Linux / AlmaLinux:**
- RHEL uyumluluğu
- Kurumsal standart
- Uzun destek (10 yıl)
- Güvenlik sertifikaları

</div>

<div class="compare-box">

### 🎮 Özel Kullanım Senaryoları

**Gaming:**
- Pop!_OS (System76)
- Manjaro Gaming
- SteamOS (Valve)

**Privacy/Security:**
- Tails (Anonymity)
- Qubes OS (Security)
- Kali Linux (Penetration Testing)

**Eski Donanım:**
- Lubuntu (LXDE)
- Puppy Linux
- antiX

**Embedded/IoT:**
- Raspberry Pi OS
- Yocto Project
- Buildroot

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Command Line Interface & Scripting

---

![bg](../gorseller/3_normal_slayt.png)

# 💻 Linux Command Line Interface (CLI)

<div class="two-columns">

<div>

<div class="info-box">

### 🖥️ Shell Nedir?

**Shell**: Kullanıcı ile çekirdek arasındaki arayüz

**İşlevleri:**
- Komutları yorumlama ve çalıştırma
- Script execution
- Job control
- Environment variables
- I/O redirection
- Piping

**Shell vs Terminal:**
- **Terminal**: Text giriş/çıkış arayüzü
- **Shell**: Komut yorumlayıcısı program

</div>

<div class="info-box">

### 🐚 Popüler Shell'ler

**bash (Bourne Again Shell):**
- En yaygın shell
- POSIX uyumlu
- Scripting için güçlü
- Linux default'u

**zsh (Z Shell):**
- bash'in gelişmiş versiyonu
- Oh-My-Zsh framework
- Tab completion++
- macOS default (2019+)

**fish (Friendly Interactive Shell):**
- User-friendly
- Syntax highlighting
- Auto-suggestions
- Web-based configuration

**sh/dash:**
- Minimalist, hızlı
- System scripts için

</div>

</div>

<div>

<div class="highlight-box">

### 🎯 Neden CLI Kullanmalı?

**Verimlilik:**
- Tekrarlayan işler hızlı
- Keyboard shortcuts
- Tab completion
- Command history

**Güç:**
- Karmaşık işlemler basit
- Piping ve redirection
- Regular expressions
- Batch processing

**Otomasyon:**
- Shell scripting
- Cron jobs
- System administration
- DevOps workflows

**Uzak Erişim:**
- SSH bağlantıları
- Düşük bant genişliği
- Terminal multiplexing (tmux)

</div>

<div class="info-box">

### 📚 CLI Öğrenme Yolu

**Seviye 1 - Temel:**
- Navigation (cd, ls, pwd)
- File operations (cp, mv, rm)
- Viewing files (cat, less, head, tail)

**Seviye 2 - Orta:**
- Permissions (chmod, chown)
- Search (find, grep)
- Process management (ps, kill, top)

**Seviye 3 - İleri:**
- Text processing (sed, awk, cut)
- Piping ve redirection
- Shell scripting

</div>

</div>

</div>

---

# 📁 Temel Linux Komutları (1/2)

<div class="info-box">

### 🗂️ Dosya ve Dizin İşlemleri

```
# Dizin gezinme
pwd                    # Mevcut dizini göster
cd /path/to/directory  # Dizin değiştir
cd ~                   # Home dizinine git
cd ..                  # Üst dizine çık
cd -                   # Önceki dizine dön

# Dosya listeleme
ls                     # Dosyaları listele
ls -l                  # Detaylı liste
ls -la                 # Gizli dosyalarla
ls -lh                 # Human readable size
ls -ltr                # Zamana göre sırala

# Dosya oluşturma/silme
touch file.txt         # Boş dosya oluştur
mkdir directory        # Dizin oluştur
mkdir -p dir1/dir2     # Alt dizinlerle oluştur
rm file.txt            # Dosya sil
rm -r directory        # Dizin sil (recursive)
rm -rf directory       # Zorla sil (dikkat!)
```

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 📁 Temel Linux Komutları (2/2)

<div class="info-box">

### 📋 Dosya Kopyalama ve Taşıma

```
# Kopyalama
cp source dest         # Dosya kopyala
cp -r dir1 dir2        # Dizin kopyala
cp -i file dest        # İnteractive (onay sor)
cp -v file dest        # Verbose (göster)

# Taşıma/Yeniden adlandırma
mv old new             # Taşı veya yeniden adlandır
mv file /path/         # Dosyayı taşı
mv -i old new          # Onay iste

# Bağlantılar
ln -s target link      # Symbolic link oluştur
ln target hardlink     # Hard link oluştur
```

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 📁 Temel Linux Komutları (3/3)

<div class="two-columns">

<div>

<div class="info-box">

### 📖 Dosya İçeriğini Görüntüleme

```
# Tüm içerik
cat file.txt           # Dosyayı yazdır
tac file.txt           # Tersten yazdır

# Sayfa sayfa
less file.txt          # Sayfalama (q ile çık)
more file.txt          # Eski sayfalama

# Baştan/sondan
head file.txt          # İlk 10 satır
head -n 20 file.txt    # İlk 20 satır
tail file.txt          # Son 10 satır
tail -n 20 file.txt    # Son 20 satır
tail -f /var/log/syslog # Canlı takip

# Arama
grep "pattern" file    # Pattern ara
grep -i "text" file    # Case insensitive
grep -r "text" dir/    # Recursive arama
grep -v "text" file    # Ters arama (exclude)
```

</div>

</div>

<div>

<div class="info-box">

### 🔍 Dosya Arama

```
# find komutu
find /path -name "*.txt"       # İsme göre ara
find /path -type f             # Sadece dosyalar
find /path -type d             # Sadece dizinler
find /path -size +10M          # 10MB'dan büyük
find /path -mtime -7           # Son 7 gün
find /path -name "*.log" -delete # Bul ve sil

# locate komutu (daha hızlı)
locate filename        # Database'de ara
updatedb               # Database güncelle
```

</div>

</div>

</div>

---

# ⚙️ Sistem Yönetimi Komutları (1/2)

<div class="two-columns">

<div>

<div class="info-box">

### 📊 Sistem Bilgisi

```
# Sistem ve donanım
uname -a               # Sistem bilgisi
hostnamectl            # Hostname ve OS info
lscpu                  # CPU bilgisi
lsmem                  # Bellek bilgisi
lsblk                  # Disk ve partition
lspci                  # PCI devices
lsusb                  # USB devices
dmidecode              # Hardware details (root)

# Disk kullanımı
df -h                  # Disk free (human readable)
df -i                  # Inode kullanımı
du -sh /path           # Directory size
du -h --max-depth=1    # Alt dizin boyutları

# Bellek kullanımı
free -h                # RAM kullanımı
vmstat                 # Virtual memory stats
```

</div>

</div>

<div>

<div class="info-box">

### 🔄 Process Yönetimi

```
# Process listeleme
ps aux                 # Tüm processler
ps aux | grep nginx    # Belirli process
pstree                 # Process tree
top                    # Canlı process monitor
htop                   # İnteraktif top (daha iyi)

# Process kontrolü
kill PID               # Process sonlandır
kill -9 PID            # Zorla sonlandır
killall process_name   # İsme göre sonlandır
pkill pattern          # Pattern'e göre

# Background jobs
command &              # Background'da çalıştır
jobs                   # Background jobs listesi
fg %1                  # Foreground'a al
bg %1                  # Background'da devam
nohup command &        # Logout sonrası da çalış
```

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# ⚙️ Sistem Yönetimi Komutları (2/2)

<div class="two-columns">

<div>

<div class="info-box">

### 🔐 Dosya İzinleri ve Sahiplik

```
# İzinleri görüntüleme
ls -l file.txt         # Detaylı bilgi
stat file.txt          # Tam bilgi

# İzin değiştirme (chmod)
chmod 755 file         # rwxr-xr-x
chmod u+x file         # User'a execute ekle
chmod g-w file         # Group'tan write çıkar
chmod o=r file         # Other'a sadece read
chmod -R 755 directory # Recursive

# Sahiplik değiştirme
chown user:group file  # Sahip ve grup değiştir
chown user file        # Sadece sahip
chgrp group file       # Sadece grup
chown -R user:group dir # Recursive

# İzin numaraları
# 4 = read (r)
# 2 = write (w)
# 1 = execute (x)
# 0 = yok
```

</div>

</div>

<div>

<div class="highlight-box">

### 📦 Paket Yönetimi

**Debian/Ubuntu (apt):**
```
sudo apt update        # Paket listesi güncelle
sudo apt upgrade       # Paketleri yükselt
sudo apt install pkg   # Paket kur
sudo apt remove pkg    # Paket kaldır
apt search keyword     # Paket ara
apt show package       # Paket bilgisi
```

**Red Hat/Fedora (dnf/yum):**
```
sudo dnf update        # Güncelle
sudo dnf install pkg   # Kur
sudo dnf remove pkg    # Kaldır
dnf search keyword     # Ara
```

</div>

</div>

</div>

---

# 🔗 İleri Seviye CLI: Pipes ve Redirection (1/2)

<div class="two-columns">

<div>

<div class="info-box">

### 📤 I/O Redirection

**Output Redirection:**
```
command > file         # Çıktıyı dosyaya yaz (üzerine)
command >> file        # Çıktıyı dosyaya ekle (append)
command 2> file        # Error'ları dosyaya
command 2>&1           # Error'ları stdout'a
command &> file        # Her şeyi dosyaya
command > /dev/null    # Çıktıyı çöpe at
```

**Input Redirection:**
```
command < file         # Dosyadan input al
command << EOF         # Here document
...
EOF
```

**File Descriptors:**
- **0**: stdin (standard input)
- **1**: stdout (standard output)
- **2**: stderr (standard error)

</div>

</div>

<div>

<div class="info-box">

### 🔗 Piping

**Pipe Operatörü (|):**
Bir komutun çıktısını diğerinin girdisi yapar

```
# Basit örnekler
ls -l | grep ".txt"    # txt dosyalarını filtrele
cat file | wc -l       # Satır sayısını say
ps aux | grep nginx    # nginx processlerini bul

# Karmaşık örnekler
cat access.log | grep "404" | wc -l
# 404 hatalarını say

ls -l | awk '{print $9}' | sort
# Dosya isimlerini sırala

cat data.csv | cut -d',' -f2 | sort | uniq -c
# 2. kolonu unique say

# Chain piping
dmesg | grep -i error | tail -20 | less
# Kernel error'ları göster
```

</div>

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# 🔗 İleri Seviye CLI: Pipes ve Redirection (2/2)

<div class="two-columns">

<div>

<div class="highlight-box">

### 🛠️ Güçlü Kombinasyonlar

```
# En çok yer kaplayan dosyaları bul
du -h /path | sort -hr | head -10

# Sistemdeki tüm kullanıcıları listele
cat /etc/passwd | cut -d':' -f1 | sort

# Log dosyasında en çok tekrarlanan IP'leri bul
cat access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -10

# Port dinleyen servisleri göster
netstat -tuln | grep LISTEN

# Disk kullanımını analiz et
df -h | grep -v "tmpfs" | sort -k5 -hr

# Sistemdeki en çok CPU kullanan 5 process
ps aux | sort -nrk 3 | head -5

# Büyük dosyaları bul ve sil
find /path -type f -size +100M -exec rm -i {} \;

# Loglarda belirli zaman aralığını filtrele
grep "2024-01-20 14:" /var/log/syslog | less
```

</div>

</div>

<div>

<div class="info-box">

### 🎯 Kullanışlı Komut Kombinasyonları

```
# Disk doluluk alarmı
df -h | awk '{ if ($5 > 80) print $0 }'

# Port 80'i kim kullanıyor?
sudo lsof -i :80

# Belirli uzantıdaki dosyaları toplu yeniden adlandır
for f in *.txt; do mv "$f" "${f%.txt}.bak"; done

# Recursive dosya içinde ara ve değiştir
find . -name "*.php" -exec sed -i 's/old/new/g' {} \;

# Arşiv oluştur ve sıkıştır
tar -czf backup.tar.gz /path/to/directory
```

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Desktop Environments

---

![bg](../gorseller/3_normal_slayt.png)

# 🖥️ Linux Desktop: GNOME

<div class="two-columns">

<div>

<div class="info-box">

### 🎨 GNOME Nedir?

**GNU Network Object Model Environment**

**Genel Özellikler:**
- 1999'da başlatıldı
- GTK+ toolkit kullanır
- Modern ve minimalist tasarım
- Touchscreen friendly
- Wayland desteği

**GNOME Versiyonları:**
- GNOME 2 (2002-2011): Klasik
- GNOME 3 (2011-2020): Radikal değişim
- GNOME 40+ (2021+): Modern workflow

**Kullanan Dağıtımlar:**
- Ubuntu (Vanilla GNOME)
- Fedora Workstation
- Debian
- Pop!_OS (özelleştirilmiş)

</div>

<div class="info-box">

### 🎯 GNOME Bileşenleri

**Core Components:**
- **GNOME Shell**: Ana arayüz
- **Mutter**: Window manager (Wayland/X11)
- **Nautilus**: File manager
- **GNOME Terminal**: Terminal emulator

**Standart Uygulamalar:**
- **Files** (Nautilus): Dosya yöneticisi
- **Web** (Epiphany): Web browser
- **Calendar**: Takvim
- **Contacts**: Kişiler
- **Maps**: Harita
- **Photos**: Fotoğraf yöneticisi
- **Videos** (Totem): Video player
- **Music**: Müzik player

</div>

</div>

<div>

<div class="highlight-box">

### ✨ GNOME Özellikleri

**Activities Overview:**
- Super tuşu ile açılır
- Açık pencereler görünür
- Workspace geçişi
- Uygulama araması

**Workspace Management:**
- Dinamik workspace'ler
- Kolay geçiş (Super+PageUp/Down)
- Per-monitor workspaces

**Extension System:**
- JavaScript tabanlı
- extensions.gnome.org
- Özelleştirme imkanı
- Topluluk eklentileri

**Modern Özellikler:**
- Night Light (mavi ışık filtresi)
- Application grid
- Notification center
- Quick settings
- Search everything

</div>

<div class="info-box">

### 🔧 GNOME Özelleştirme

**GNOME Tweaks:**
- Appearance ayarları
- Font değiştirme
- Window behavior
- Extension yönetimi

**Popüler Extensionlar:**
- Dash to Dock
- User Themes
- Caffeine
- Clipboard Indicator
- GSConnect (KDE Connect)

**Tema ve İkonlar:**
- GTK themes
- Icon themes
- Cursor themes
- GNOME Looks website

</div>

</div>

</div>

---

# ⚡ Linux Desktop: KDE Plasma

<div class="two-columns">

<div>

<div class="info-box">

### 🎨 KDE Plasma Nedir?

**K Desktop Environment**

**Genel Özellikler:**
- 1996'da başlatıldı
- Qt toolkit kullanır
- Yüksek düzeyde özelleştirilebilir
- Windows benzeri deneyim
- Modern ve estetik

**Versiyonlar:**
- KDE 1-4 (1998-2014)
- KDE Plasma 5 (2014-2024)
- KDE Plasma 6 (2024+): Qt 6, Wayland

**Kullanan Dağıtımlar:**
- KDE Neon (resmi)
- Kubuntu
- openSUSE
- Manjaro KDE

</div>

<div class="info-box">

### 🧩 KDE Bileşenleri

**Core Components:**
- **Plasma Desktop**: Ana arayüz
- **KWin**: Window manager
- **Dolphin**: File manager (en iyi)
- **Konsole**: Terminal

**KDE Applications:**
- **Kate**: Text editor
- **Okular**: Document viewer
- **Spectacle**: Screenshot tool
- **KMail**: Email client
- **Kontact**: PIM suite
- **Gwenview**: Image viewer
- **Kdenlive**: Video editor (profesyonel)
- **Krita**: Digital painting

</div>

</div>

<div>

<div class="highlight-box">

### ⚙️ KDE Özelleştirme

**Extreme Customization:**
- Panel'leri dilediğiniz gibi düzenleyin
- Widget'lar ekleyin
- Window decorations değiştirin
- Desktop effects
- Icon themes, wallpapers
- Color schemes

**Plasma Widgets:**
- Küçük uygulamalar
- Desktop veya panel'e eklenebilir
- Hava durumu, sistem monitörü
- KDE Store'dan indirilebilir

**KDE Connect:**
- Telefon-PC entegrasyonu
- Dosya transferi
- Notification senkronizasyonu
- Clipboard paylaşımı
- Telefonu mouse olarak kullanma

</div>

<div class="compare-box">

### 🆚 KDE vs GNOME

**KDE Plasma:**
- ✅ Maksimum özelleştirme
- ✅ Windows benzeri
- ✅ Güçlü uygulamalar
- ✅ Her detay ayarlanabilir
- ⚠️ Karmaşık olabilir

**GNOME:**
- ✅ Minimalist ve modern
- ✅ Tutarlı deneyim
- ✅ Kolay kullanım
- ✅ Clean arayüz
- ⚠️ Sınırlı özelleştirme

**Performans:**
- Modern donanımda benzer
- KDE hafif olma iddiasında
- GNOME daha optimize edildi

</div>

</div>

</div>

---

# 🪶 Hafif Desktop Ortamları

<div class="two-columns">

<div>

<div class="info-box">

### 🎯 XFCE

**Xforms Common Environment**

**Özellikler:**
- Hafif ve hızlı
- Orta düzeyde özelleştirme
- Kararlı ve güvenilir
- GTK+ tabanlı

**Avantajları:**
- Düşük RAM kullanımı (~400MB)
- Eski donanımda çalışır
- Kullanıcı dostu
- Panel ve plugin sistemi

**Kullanan Dağıtımlar:**
- Xubuntu
- Manjaro XFCE
- MX Linux

**Uygulamalar:**
- Thunar (file manager)
- Xfce Terminal
- Mousepad (text editor)

</div>

<div class="info-box">

### 🔷 LXDE / LXQt

**Lightweight X11 Desktop Environment**

**LXDE (GTK):**
- Çok hafif
- Minimal kaynak (~300MB RAM)
- Basit ve hızlı

**LXQt (Qt):**
- LXDE'nin Qt versiyonu
- Daha modern
- Wayland hazırlığı

**Kullanan Dağıtımlar:**
- Lubuntu (LXQt)
- LXLE

**İdeal İçin:**
- Çok eski bilgisayarlar
- Netbook'lar
- Raspberry Pi

</div>

</div>

<div>

<div class="info-box">

### 🌿 MATE ve Cinnamon

**MATE Desktop:**
- GNOME 2'nin devamı
- Klasik deneyim
- Orta kaynak kullanımı
- Kararlı ve tanıdık

**Kullanan Dağıtımlar:**
- Ubuntu MATE
- Linux Mint MATE

**Cinnamon:**
- Linux Mint tarafından geliştirildi
- Modern ama geleneksel
- Windows benzeri workflow
- Güzel görünüm

**Kullanan Dağıtımlar:**
- Linux Mint (flagship)
- Debian (opsiyonel)

</div>

<div class="info-box">

### ⚡ Window Managers (Tiling)

**i3wm:**
- Tiling window manager
- Keyboard-driven
- Minimal RAM (~150MB)
- Extreme verimlilik

**Diğer Tiling WM:**
- **Sway**: i3 Wayland versiyonu
- **bspwm**: Binary space partitioning
- **dwm**: Dynamic window manager
- **awesome**: Lua configured

**Avantajları:**
- Maksimum ekran kullanımı
- Hızlı workflow
- Klavye odaklı
- Minimal kaynak

**Dezavantajları:**
- Öğrenme eğrisi yüksek
- Manuel konfigürasyon gerekir

</div>

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Modern Technologies

---

![bg](../gorseller/3_normal_slayt.png)

# ☁️ Cloud Computing Temelleri

<div class="two-columns">

<div>

<div class="info-box">

### ☁️ Cloud Computing Nedir?

**Tanım:**
İnternet üzerinden sunulan computing servisleri (servers, storage, databases, networking, software, analytics)

**NIST Tanımı:**
5 temel özellik, 3 servis modeli, 4 deployment modeli

**5 Temel Özellik:**
- **On-demand self-service**: İstediğinde kaynak
- **Broad network access**: Her yerden erişim
- **Resource pooling**: Paylaşımlı kaynaklar
- **Rapid elasticity**: Hızlı ölçeklendirme
- **Measured service**: Kullanım ölçümü

**Tarihçe:**
- 1960s: Time-sharing
- 1990s: Virtual private networks
- 2006: AWS EC2 lansmanı
- 2010s: Cloud mainstream

</div>

<div class="highlight-box">

### 📊 Cloud İstatistikleri

**Global Market:**
- **$600B+** pazar değeri (2024)
- **%20+** yıllık büyüme
- **94%** kurumlar cloud kullanıyor

**Top Cloud Providers:**
- **AWS**: %32 market share
- **Azure**: %23 market share
- **Google Cloud**: %10 market share
- **Alibaba Cloud**: %4 market share

**Avantajlar:**
- **%30-40** maliyet tasarrufu
- **%50** daha hızlı deployment
- **99.99%** uptime SLA'lar
- Global scale

</div>

</div>

<div>

<div class="info-box">

### 🏗️ Cloud Servis Modelleri

**IaaS (Infrastructure as a Service):**
- Sanal makineler, network, storage
- En esnek, en çok kontrol
- Siz OS ve uygulamaları yönetirsiniz
- **Örnekler**: AWS EC2, Azure VMs, Google Compute Engine

**PaaS (Platform as a Service):**
- Platform ve development araçları
- OS yönetimi sağlayıcıda
- Uygulamaya odaklanma
- **Örnekler**: Heroku, Google App Engine, AWS Elastic Beanstalk

**SaaS (Software as a Service):**
- Hazır yazılım uygulamaları
- Web üzerinden erişim
- Hiç yönetim yok
- **Örnekler**: Gmail, Office 365, Salesforce, Dropbox

</div>

<div class="info-box">

### 🌍 Cloud Deployment Modelleri

**Public Cloud:**
- Herkes için açık
- Shared infrastructure
- Pay-as-you-go
- **Örnekler**: AWS, Azure, GCP

**Private Cloud:**
- Tek kurum için
- On-premise veya hosted
- Maksimum kontrol
- **Örnekler**: OpenStack, VMware

**Hybrid Cloud:**
- Public + Private kombinasyonu
- Esneklik ve güvenlik dengesi
- Kritik data private'da

**Community Cloud:**
- Belirli topluluk için
- Ortak gereksinimler
- Maliyet paylaşımı

</div>

</div>

</div>

---

# 🖥️ Virtualization (Sanallaştırma)

<div class="two-columns">

<div>

<div class="info-box">

### 🎯 Sanallaştırma Nedir?

**Tanım:**
Fiziksel donanımın yazılımsal olarak bölünerek birden fazla sanal ortam oluşturulması

**Tarihçe:**
- 1960s: IBM mainframe'ler
- 1990s: x86 virtualization
- 2000s: Xen, KVM, VMware
- 2010s: Containers

**Neden Sanallaştırma?**
- Donanım verimliliği (%70-80)
- İzolasyon ve güvenlik
- Kolay yedekleme (snapshot)
- Hızlı deployment
- Testing ve development

**Kullanım Alanları:**
- Server consolidation
- Cloud computing
- Development & testing
- Disaster recovery

</div>

<div class="info-box">

### 🏗️ Hypervisor Türleri

**Type 1 (Bare Metal):**
- Doğrudan donanım üzerinde
- Maksimum performans
- Production kullanımı

**Örnekler:**
- **VMware ESXi**: Kurumsal standart
- **KVM**: Linux kernel modülü
- **Xen**: AWS kullanır
- **Microsoft Hyper-V**: Windows Server

**Type 2 (Hosted):**
- Host OS üzerinde çalışır
- Kolay kurulum
- Desktop virtualization

**Örnekler:**
- **VirtualBox**: Ücretsiz, cross-platform
- **VMware Workstation**: Profesyonel
- **Parallels**: macOS için
- **QEMU**: KVM ile birlikte

</div>

</div>

<div>

<div class="highlight-box">

### 🐧 Linux Virtualization: KVM

**Kernel-based Virtual Machine**

**Özellikler:**
- Linux kernel'e entegre (2007)
- Hardware virtualization (Intel VT-x, AMD-V)
- Near-native performance
- Ücretsiz ve açık kaynak

**Bileşenler:**
- **KVM**: Kernel modülü
- **QEMU**: Device emulation
- **libvirt**: Management API
- **virt-manager**: GUI tool

**Avantajları:**
- Mükemmel performans
- Linux mainline'da
- Geniş topluluk
- Enterprise support (Red Hat)

**Kullanım:**
```
# VM oluşturma
virt-install --name vm1 \
  --ram 2048 --vcpus 2 \
  --disk path=/var/lib/libvirt/images/vm1.qcow2

# VM yönetimi
virsh list --all
virsh start vm1
virsh shutdown vm1
```

</div>

<div class="info-box">

### 📦 Para-virtualization

**Xen:**
- Orijinal para-virtualization
- Dom0 (control domain)
- DomU (guest domains)
- AWS'in temeli

**Avantajları:**
- Yüksek performans
- Güvenlik izolasyonu
- Cloud-scale

</div>

</div>

</div>

---

# 🐳 Container Teknolojisi

<div class="two-columns">

<div>

<div class="info-box">

### 📦 Container Nedir?

**Tanım:**
OS-level virtualization - Uygulamaları izole ortamlarda çalıştırma

**VM vs Container:**

**Virtual Machines:**
- Tam OS içerir
- Hypervisor gerekir
- GB'larca boyut
- Dakikalar boot time
- Strong isolation

**Containers:**
- OS kernel paylaşır
- Container runtime
- MB'larca boyut
- Saniyeler boot time
- Process isolation

**Avantajlar:**
- Hafif ve hızlı
- Taşınabilir
- Tutarlı environment
- Mikroservis mimarisi

</div>

<div class="highlight-box">

### 🐳 Docker

**Container'ları popülerleştiren platform**

**Temel Kavramlar:**

**Image:**
- Read-only template
- Dockerfile ile oluşturulur
- Layered filesystem

**Container:**
- Image'in running instance'ı
- Writable layer
- İzole process

**Registry:**
- Image repository
- Docker Hub (public)
- Private registries

**Docker Komutları:**
```
# Image yönetimi
docker pull nginx
docker images
docker rmi image

# Container yönetimi
docker run -d -p 80:80 nginx
docker ps
docker stop container
docker rm container

# Build
docker build -t myapp .
docker push myapp
```

</div>

</div>

<div>

<div class="info-box">

### ⚓ Kubernetes (K8s)

**Container Orchestration Platform**

**Neden Kubernetes?**
- Container'ları yönetme
- Auto-scaling
- Self-healing
- Load balancing
- Rolling updates

**Temel Kavramlar:**

**Pod:** En küçük deployment birimi
**Service:** Pod'lara network erişimi
**Deployment:** Pod replica yönetimi
**Namespace:** Logical separation
**ConfigMap/Secret:** Configuration

**Mimarisi:**
- **Control Plane**: Master node
  - API Server
  - Scheduler
  - Controller Manager
  - etcd (database)
- **Worker Nodes**: Container'lar çalışır
  - kubelet
  - kube-proxy
  - Container runtime

</div>

<div class="info-box">

### 🔧 Diğer Container Teknolojileri

**Podman:**
- Daemonless alternative
- Docker-compatible
- Rootless containers
- Red Hat tarafından

**LXC/LXD:**
- System containers
- Tam OS container'ları
- VM benzeri deneyim

**containerd:**
- CNCF projesi
- Docker'ın alt yapısı
- Kubernetes kullanır

**CRI-O:**
- Kubernetes için
- OCI uyumlu
- Lightweight

</div>

</div>

</div>

---

# 🚀 Cloud Native ve Modern Teknolojiler

<div class="two-columns">

<div>

<div class="info-box">

### ☁️ Cloud Native Nedir?

**CNCF Tanımı:**
Cloud native teknolojileri, organizasyonların modern, dinamik ortamlarda (public, private, hybrid cloud) ölçeklenebilir uygulamalar geliştirmesini sağlar.

**Temel Prensipler:**
- **Microservices**: Küçük, bağımsız servisler
- **Containers**: Taşınabilir paketleme
- **Service Mesh**: Service-to-service iletişim
- **Immutable Infrastructure**: Değişmez altyapı
- **Declarative APIs**: Desired state

**12-Factor App:**
1. Codebase (version control)
2. Dependencies (explicit)
3. Config (environment)
4. Backing services
5. Build, release, run
6. Stateless processes
... ve 6 daha

</div>

<div class="info-box">

### 🛠️ DevOps ve CI/CD

**DevOps:**
Development + Operations kültürü

**Prensipler:**
- Automation
- Continuous Integration
- Continuous Delivery
- Infrastructure as Code
- Monitoring & Logging

**CI/CD Pipeline:**
```
Code → Build → Test → Deploy → Monitor
```

**Araçlar:**
- **CI/CD**: Jenkins, GitLab CI, GitHub Actions
- **IaC**: Terraform, Ansible, Puppet
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack, Loki

</div>

</div>

<div>

<div class="highlight-box">

### 📊 Linux'un Cloud'daki Dominance

**Server Market Share:**
- **%96.3** web server'lar Linux
- **%90+** public cloud instances
- **%100** top 500 supercomputers

**Neden Linux?**
- Açık kaynak ve ücretsiz
- Kararlı ve güvenli
- Geniş donanım desteği
- Container native
- Otomasyon friendly

**Cloud'da Linux:**
- AWS: Amazon Linux, Ubuntu
- Azure: Ubuntu, Red Hat
- GCP: Debian, Ubuntu
- Kubernetes: Linux containers

</div>

<div class="info-box">

### 🌐 Serverless Computing

**Function as a Service (FaaS)**

**Kavram:**
- Event-driven execution
- No server management
- Pay per execution
- Auto-scaling

**Örnekler:**
- AWS Lambda
- Azure Functions
- Google Cloud Functions
- OpenFaaS (open source)

**Use Cases:**
- API backends
- Data processing
- Scheduled tasks
- IoT data handling

</div>

</div>

</div>

---

# 🎓 Sonuç ve Özet

## Linux Fundamentals - Introduction to Open Source

---

<div class="two-columns">

<div>

### 📚 Öğrendiklerimiz

**Open Source Dünyası:**
- Özgür yazılım felsefesi
- Farklı lisans modelleri
- Topluluk gücü

**Linux Ekosistemi:**
- UNIX kökleri
- Kernel ve dağıtımlar
- Desktop ortamları

**Command Line:**
- Shell kullanımı
- Temel ve ileri komutlar
- Otomasyon gücü

</div>

<div>

**Modern Teknolojiler:**
- Cloud computing modelleri
- Virtualization teknolojileri
- Container ekosistemi
- Cloud native yaklaşım

### 🎯 Sonraki Adımlar

- Pratik yapın: Bir Linux dağıtımı kurun
- CLI'da çalışın: Komutları günlük kullanın
- Projelerkinkatıl: GitHub, GitLab
- Öğrenmeye devam edin: Dokümantasyon okuyun

</div>

</div>

---

<!-- _class: final-slide -->

# 🙏 Teşekkürler!
