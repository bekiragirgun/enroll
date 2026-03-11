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
  }
  
  /* Arka plan resmi olan slaytlar için özel stil */
  section[data-background-image] {
    background-color: transparent !important;
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

  p, li {
    font-size: 13pt;
    line-height: 1.6;
    margin-bottom: 8px;
  }

  ul, ol {
    margin-left: 20px;
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
  section.final-slide p {
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

  .warning-box {
    background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);
    color: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .warning-box h3 {
    color: white;
    margin-top: 0;
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
    max-height: 350px;
  }

  pre code {
    background: none;
    padding: 0;
    font-size: 12pt;
    line-height: 1.5;
  }

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

  td {
    color: #333 !important;
    background-color: white !important;
  }

  th {
    background-color: #2D4A7C;
    color: white;
    font-weight: bold;
  }

  /* Renkli kutulardaki tablolar - BEYAZ yazı */
  section .info-box table,
  section .highlight-box table,
  section .warning-box table {
    border-collapse: collapse !important;
    width: 100% !important;
  }

  section .info-box table th,
  section .info-box table td,
  section .highlight-box table th,
  section .highlight-box table td,
  section .warning-box table th,
  section .warning-box table td {
    color: white !important;
    background-color: transparent !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    padding: 8px !important;
  }

  section .info-box table th,
  section .highlight-box table th,
  section .warning-box table th {
    background-color: rgba(0,0,0,0.25) !important;
    font-weight: bold !important;
  }

  section div.info-box th,
  section div.info-box td,
  section div.highlight-box th,
  section div.highlight-box td,
  section div.warning-box th,
  section div.warning-box td {
    color: white !important;
    background: transparent !important;
  }

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

---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Bilgisayar Donanımını Anlamak

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

### Temel Bileşenler

- Anakart (Motherboard)
- İşlemci (CPU)
- Bellek (RAM)
- Veri Yolları (Buses)
- Sabit Diskler

</div>
<div class="info-box">

### Ek Konular

- SSD vs HDD
- Optik Sürücüler
- Aygıt Yönetimi
- Ekran Kartları
- Güç Kaynakları

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Giriş

---

![bg](../gorseller/3_normal_slayt.png)

# Donanımı Neden Anlamalıyız?

<div class="two-columns">
<div>

### Fiziksel ve Sanal

- Bilgisayarlar **fiziksel donanım** ile başlar
- **Sanal makineler** tamamen yazılımla oluşturulabilir
- Uzaktan erişim protokolleri ile kullanılır

### Temel Gereklilik

- Kurulum
- Yapılandırma
- Yönetim
- Güvenlik
- Sorun giderme

</div>
<div class="highlight-box">

### Bilgisayar Türleri

- Set-top box'lar
- Güvenlik duvarları
- Dizüstü bilgisayarlar
- Sunucular
- Özel amaçlı cihazlar

**Hepsi aynı temel bileşenleri içerir!**

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Anakart (Motherboard)

---

![bg](../gorseller/3_normal_slayt.png)

# Anakart Nedir?

<div class="two-columns">
<div>

### Tanım

**Anakart** (veya sistem kartı), bilgisayarın ana donanım kartıdır.

### Bağlı Bileşenler

- **CPU** (İşlemci)
- **RAM** (Bellek)
- Eklenti kartları
- Depolama aygıtları

</div>
<div>

### Bağlantı Türleri

- **CPU:** Doğrudan lehimli
- **RAM:** Doğrudan slot
- **Ekran kartı:** Bus üzerinden
- **Ağ kartı:** Bus üzerinden

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# İşlemci (CPU)

---

![bg](../gorseller/3_normal_slayt.png)

# CPU - Bilgisayarın Beyni

<div class="two-columns">
<div>

### Temel Bilgiler

- **CPU** = Central Processing Unit
- Kodun çalıştırıldığı yer
- Hesaplamaların yapıldığı yer
- Anakarta **lehimli** bağlantı

### İşlemci Türleri

- **Multiprocessor** - Birden fazla işlemci
- **Multi-core** - Tek çipte birden fazla çekirdek

</div>
<div class="highlight-box">

### x86 vs x86_64

**x86 (32-bit):**
- Bit: 32-bit
- Max RAM: 4 GB
- Güvenlik: Temel
- Verimlilik: Standart

**x86_64 (64-bit):**
- Bit: 64-bit
- Max RAM: Çok daha fazla
- Güvenlik: Gelişmiş
- Verimlilik: Yüksek

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# İşlemci Komutları

<div class="two-columns">
<div>

### arch Komutu

```bash
sysadmin@localhost:~$ arch
x86_64
```

İşlemci ailesini gösterir.

</div>
<div>

### lscpu Komutu

```bash
sysadmin@localhost:~$ lscpu
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
CPU(s):              4
Thread(s) per core:  1
Core(s) per socket:  4
Vendor ID:           GenuineIntel
```

Detaylı CPU bilgisi verir.

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Bellek (RAM)

---

![bg](../gorseller/3_normal_slayt.png)

# RAM - Rastgele Erişimli Bellek

<div class="two-columns">
<div>

### Temel Bilgiler

- Anakart üzerinde **slotlara** takılır
- 32-bit sistemler: max **4 GB**
- 64-bit sistemler: çok daha fazla

### RAM Yetersizliği

- Programlar RAM'e yüklenir
- Yetersiz RAM → **Swap** kullanımı
- Swap = Disk üzerinde sanal bellek

</div>
<div class="info-box">

### Swap Alanı

- Sık kullanılmayan veriler diske taşınır
- İhtiyaç olunca RAM'e geri alınır
- Sistem **otomatik** yönetir
- Yapılandırılmış olmalı

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# free Komutu

```bash
sysadmin@localhost:~$ free -m
             total       used       free     shared    buffers     cached
Mem:          1894        356       1537          0         25        177
-/+ buffers/cache:        153       1741
Swap:         4063          0       4063
```

<div class="two-columns">
<div>

### Seçenekler

- **`-m`:** Megabyte cinsinden
- **`-g`:** Gigabyte cinsinden
- **`-h`:** İnsan okunabilir

</div>
<div class="highlight-box">

### Çıktı Analizi

- **Toplam RAM:** 1894 MB
- **Kullanılan:** 356 MB
- **Swap:** 4063 MB (kullanılmıyor)

Swap kullanılmıyor çünkü yeterli RAM var.

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Veri Yolları (Buses)

---

![bg](../gorseller/3_normal_slayt.png)

# Bus Nedir?

<div class="two-columns">
<div>

### Tanım

**Bus**, bilgisayar bileşenleri arasında iletişim sağlayan yüksek hızlı bağlantıdır.

### Bus Türleri

- **PCI** - Peripheral Component Interconnect
- **USB** - Universal Serial Bus
- Monitör, klavye, fare bağlantıları

</div>
<div class="info-box">

### Sistem Türlerine Göre

- **Masaüstü/Sunucu:** Kart slotları ile genişleme
- **Laptop:** Çoğu bileşen anakarta entegre
- **Thin client:** Yükseltme imkanı sınırlı

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# lspci Komutu - PCI Aygıtları

```bash
sysadmin@localhost:~$ lspci
00:00.0 Host bridge: Intel Corporation 440BX/ZX/DX
00:07.1 IDE interface: Intel Corporation 82371AB/EB/MB PIIX4 IDE
00:0f.0 VGA compatible controller: VMware SVGA II Adapter
03:00.0 Serial Attached SCSI controller: VMware PVSCSI
0b:00.0 Ethernet controller: VMware VMXNET3 Ethernet Controller
```

<div class="highlight-box">

### Önemli Aygıtlar

- **VGA controller** - Monitör bağlantısı
- **SCSI controller** - Sabit disk
- **Ethernet controller** - Ağ bağlantısı

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# USB Aygıtları

<div class="two-columns">
<div>

### Cold-plug vs Hot-plug

- **Cold-plug:** Sistem kapalıyken bağlanır
- **Hot-plug:** Sistem çalışırken bağlanır

USB aygıtlar **hot-plug** özelliğine sahiptir.

</div>
<div class="warning-box">

### Dikkat!

USB aygıtlar hot-plug olsa da, **bağlı dosya sistemleri** doğru şekilde **unmount** edilmelidir.

Aksi halde **veri kaybı** veya **dosya sistemi bozulması** olabilir!

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# lsusb Komutu

```bash
sysadmin@localhost:~$ lsusb
Bus 001 Device 002: ID 0e0f:000b VMware, Inc.
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 002 Device 004: ID 0e0f:0008 VMware, Inc.
Bus 002 Device 003: ID 0e0f:0002 VMware, Inc. Virtual USB Hub
Bus 002 Device 002: ID 0e0f:0003 VMware, Inc. Virtual Mouse
Bus 002 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
```

<div class="info-box">

### Çıktı Bilgileri

- **Bus** - USB veri yolu numarası
- **Device** - Aygıt numarası
- **ID** - Üretici ve ürün kimliği

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Sabit Diskler

---

![bg](../gorseller/3_normal_slayt.png)

# Sabit Disk Temelleri

<div class="two-columns">
<div>

### Bağlantı Türleri

- Anakarta entegre
- PCI kart üzerinden
- USB bağlantılı

### Bölümlendirme (Partitioning)

Sabit diskler **bölümlere** ayrılır:
- Windows: Genellikle tek bölüm
- Linux: Birden fazla bölüm yaygın

</div>
<div class="info-box">

### MBR vs GPT

**MBR:**
- Tarih: 1983+
- Max Bölüm: 4 birincil
- Max Boyut: 2 TB

**GPT:**
- Tarih: 2000+
- Max Bölüm: 128+
- Max Boyut: 9.4 ZB

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Disk Araçları

<div class="two-columns">
<div>

### MBR Disk Araçları

- `fdisk`
- `cfdisk`
- `sfdisk`

### GPT Disk Araçları

- `gdisk`
- `cgdisk`
- `sgdisk`

</div>
<div class="highlight-box">

### Her İkisi İçin

- `parted` (komut satırı)
- `gparted` (grafiksel)

**gparted** kurulum sırasında bölümlendirme için sıkça kullanılır.

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Disk Aygıt Dosyaları

<div class="two-columns">
<div>

### Dosya Adlandırma

- **`hd`:** IDE diskler
- **`sd`:** USB, SATA, SCSI

### Örnekler

- `/dev/sda` - İlk SATA disk
- `/dev/sdb` - İkinci disk
- `/dev/sda1` - İlk diskin 1. bölümü
- `/dev/sda2` - İlk diskin 2. bölümü

</div>
<div>

### ls Komutu ile

```bash
root@localhost:~$ ls /dev/sd*
/dev/sda
/dev/sda1
/dev/sda2
/dev/sdb
/dev/sdb1
/dev/sdc
```

3 disk, toplam 3 bölüm

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# fdisk Komutu

```bash
root@localhost:~$ fdisk -l /dev/sda
Disk /dev/sda: 21.5 GB, 21474836480 bytes
255 heads, 63 sectors/track, 2610 cylinders
Units = sectors of 1 * 512 = 512 bytes

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    39845887    19921920   83  Linux
/dev/sda2        39847934    41940991     1046529    5  Extended
/dev/sda5        39847936    41940991     1046528   82  Linux swap
```

<div class="info-box">

### Bölüm Bilgileri

- **sda1** - Linux sistemi (boot edilebilir)
- **sda2** - Extended bölüm
- **sda5** - Swap alanı

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# SSD - Katı Hal Diskleri

---

![bg](../gorseller/3_normal_slayt.png)

# SSD vs HDD

<div class="two-columns">
<div>

### HDD (Geleneksel)

- Dönen plakalar
- Okuma kafaları
- Sıralı veri yazımı
- Mekanik parçalar

### SSD

- Bellek çipleri
- Hareketli parça yok
- Rastgele erişim
- Dahili işlemci

</div>
<div class="highlight-box">

### SSD Avantajları

- Düşük güç tüketimi
- Hızlı sistem başlatma
- Hızlı program yükleme
- Az ısı üretimi
- Titreşimsiz çalışma

### SSD Dezavantajları

- Yüksek maliyet
- Düşük kapasite/fiyat
- Anakarta lehimli olabilir

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Optik Sürücüler

---

![bg](../gorseller/3_normal_slayt.png)

# Optik Sürücüler

<div class="two-columns">
<div>

### Türler

- **CD-ROM** - Salt okunur
- **DVD** - Daha yüksek kapasite
- **Blu-Ray** - En yüksek kapasite

### Yazılabilir Formatlar

- CD-R, CD+R
- DVD+RW, DVD-RW
- BD-R, BD-RE

</div>
<div class="info-box">

### Mount Noktaları

- **Modern:** `/media/`
- **Eski:** `/mnt/`

**Örnek:** USB → `/media/usbthumb`

**Önemli:** Kullanım sonrası `umount` gerekli!

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Aygıt Yönetimi

---

![bg](../gorseller/3_normal_slayt.png)

# Linux'ta Aygıt Yönetimi

<div class="two-columns">
<div>

### Sürücü Sorunu

- Binlerce farklı aygıt
- Her aygıt için sürücü gerekli
- Üreticiler genellikle Windows için sağlar
- Linux desteği sınırlı olabilir

### Sürücü Kaynakları

- Kernel içinde derlenmiş
- Modül olarak yüklenmiş
- Kullanıcı uygulamaları

</div>
<div class="warning-box">

### Başarılı Aygıt Kullanımı

1. Dağıtımın sertifika listesini kontrol et
2. Çok yeni aygıtlardan kaçın
3. Satın almadan önce Linux desteğini sor
4. Topluluk forumlarını incele

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Ekran Aygıtları

---

![bg](../gorseller/3_normal_slayt.png)

# Video Kartları ve Monitörler

<div class="two-columns">
<div>

### Video Kartları

- Anakarta entegre olabilir
- PCI slotuna takılabilir
- Özel sürücü gerektirir

### Kablo Türleri

- **VGA:** 15 pin, Analog, eski
- **DVI:** 29 pin, Dijital
- **HDMI:** 19/29 pin, 4K desteği
- **DisplayPort:** 20 pin, En yeni

</div>
<div class="info-box">

### Linux ve Video

- Masaüstü: GUI sürücü önemli
- Sunucu: Çoğunlukla metin modu
- Büyük üreticiler Linux desteği sunuyor
- Topluluk sürücüleri de mevcut

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Güç Kaynakları

---

![bg](../gorseller/3_normal_slayt.png)

# Güç Kaynağı (PSU)

<div class="two-columns">
<div>

### İşlevi

- AC → DC dönüşümü
- 120V/240V → 3.3V, 5V, 12V
- Voltaj dalgalanmalarından koruma

### Voltajlar

- **3.3V:** RAM, chipset
- **5V:** USB, SSD
- **12V:** CPU, GPU, fanlar

</div>
<div class="warning-box">

### Dikkat Edilmesi Gerekenler

- **Kaliteli PSU** tercih edin
- Arızalı PSU sisteme zarar verebilir
- Masaüstü/sunucu daha savunmasız
- Laptop bataryayla korunur
- **UPS** kullanımı tavsiye edilir

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Özet: Temel Bileşenler

<div class="two-columns">
<div>

### Donanım

- **Anakart:** Ana bağlantı kartı
- **CPU:** İşlem ve hesaplama
- **RAM:** Geçici veri depolama
- **HDD/SSD:** Kalıcı depolama
- **PSU:** Güç dönüşümü

</div>
<div>

### Komutlar

- **`arch`:** CPU mimarisi
- **`lscpu`:** CPU detayları
- **`free`:** RAM kullanımı
- **`lspci`:** PCI aygıtları
- **`lsusb`:** USB aygıtları
- **`fdisk -l`:** Disk bölümleri

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Özet: Aygıt Dosyaları

<div class="two-columns">
<div>

### Disk Adlandırma

```
/dev/sda    → İlk disk
/dev/sda1   → İlk bölüm
/dev/sda2   → İkinci bölüm
/dev/sdb    → İkinci disk
```

### Bölümlendirme

- **MBR** - Eski sistemler (2TB limit)
- **GPT** - Modern sistemler

</div>
<div class="info-box">

### Hatırlanacaklar

- `hd*` → IDE diskler
- `sd*` → SATA/USB/SCSI diskler
- Hot-plug aygıtlar `umount` gerektirir
- SSD mekanik parça içermez
- 64-bit sistemler daha fazla RAM kullanabilir

</div>
</div>

---

<!-- _class: final-slide -->

# Teşekkürler!

### Sorularınız?

**Bekir Ağırgün**
bekir.agirgun@kapadokya.edu.tr

