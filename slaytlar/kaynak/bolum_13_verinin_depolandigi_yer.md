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
    margin-bottom: 10px;
  }

  h3 {
    color: #2D4A7C;
    font-size: 15pt;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 8px;
  }

  p, ul, ol, li {
    font-size: 13pt;
    line-height: 1.4;
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
    margin: 0;
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

  .two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-top: 20px;
  }

  .function-card {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border: 2px solid #6B9FE8;
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    min-height: 180px;
  }

  .function-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.15);
  }

  .function-card h3 {
    color: #2D4A7C;
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 16pt;
    text-align: center;
    border-bottom: 2px solid #6B9FE8;
    padding-bottom: 8px;
  }

  .function-card ul {
    margin: 0;
    padding-left: 20px;
    font-size: 12pt;
    line-height: 1.5;
  }

  .function-card li {
    margin-bottom: 4px;
  }

  .process-info-card, .process-tree-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 2px solid #6B9FE8;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    height: 100%;
  }

  .process-icon {
    font-size: 48px;
    text-align: center;
    margin-bottom: 15px;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
  }

  .tree-visualization {
    background: #2D4A7C;
    color: white;
    padding: 15px;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 11pt;
    line-height: 1.4;
    margin: 15px 0;
  }

  .process-tree-card h3, .process-info-card h3 {
    color: #2D4A7C;
    text-align: center;
    margin-top: 0;
    margin-bottom: 15px;
    border-bottom: 2px solid #6B9FE8;
    padding-bottom: 8px;
  }

  .memory-concept-card, .memory-command-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
    border: 2px solid #4A7FB8;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    height: 100%;
  }

  .memory-icon, .command-icon {
    font-size: 48px;
    text-align: center;
    margin-bottom: 15px;
    animation: float 3s ease-in-out infinite;
  }

  .command-icon {
    animation: rotate 4s linear infinite;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }

  @keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .memory-concept-card h3, .memory-command-card h3 {
    color: #2D4A7C;
    text-align: center;
    margin-top: 0;
    margin-bottom: 15px;
    border-bottom: 2px solid #4A7FB8;
    padding-bottom: 8px;
  }

  .fhs-purpose-card, .fhs-categorization-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0f8f0 100%);
    border: 2px solid #2D4A7C;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    height: 100%;
  }

  .fhs-icon {
    font-size: 48px;
    text-align: center;
    margin-bottom: 15px;
    animation: pulse 2s infinite;
  }

  .fhs-table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 12pt;
  }

  .fhs-table th, .fhs-table td {
    padding: 10px;
    border: 1px solid #2D4A7C;
    text-align: left;
    background-color: white;
    color: #333 !important;
  }

  .fhs-table th {
    background-color: #2D4A7C;
    color: white !important;
    font-weight: bold;
  }

  .fhs-purpose-card h3, .fhs-categorization-card h3 {
    color: #2D4A7C;
    text-align: center;
    margin-top: 0;
    margin-bottom: 15px;
    border-bottom: 2px solid #2D4A7C;
    padding-bottom: 8px;
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

  table {
    border-collapse: collapse;
    margin: 20px 0;
    width: 100%;
    font-size: 13pt;
  }

  th, td {
    padding: 10px;
    text-align: left;
    border: 1px solid #ddd;
  }

  th {
    background-color: #2D4A7C;
    color: white;
  }

  td {
    background-color: white;
    color: #333 !important;
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

  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
  }

  ul, ol {
    margin-left: 20px;
    margin-bottom: 15px;
  }

  li {
    margin-bottom: 5px;
  }

  /* İçerik taşması önleme */
  .info-box, .highlight-box, .compare-box {
    overflow: hidden;
    word-wrap: break-word;
  }

  pre {
    max-height: 300px;
    overflow: hidden;
  }

  /* Kod bloğu içeriği sığdırma */
  code {
    word-break: break-all;
    white-space: pre-wrap;
  }
---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Verinin Depolandığı Yer

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# İçerik

**NDG Linux Essentials - Bölüm 13**

---

![bg](../gorseller/3_normal_slayt.png)

# İçerik

## Bölüm 13 Konuları

1. Linux Kerneli ve Bellek Yönetimi
2. Process Yönetimi
3. Bellek Kullanımı ve İzleme
4. Log Dosyaları ve Sistem Mesajları
5. Dosya Sistemi Hiyerarşisi Standardı

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Linux Kerneli

---

![bg](../gorseller/3_normal_slayt.png)

# Linux Kerneli

## Kernel Nedir?

- Linux, GNU/Linux yazılım kombinasyonudur
- GNU: Ücretsiz yazılım ve UNIX komutları
- Linux Kerneli: İşletim sisteminin çekirdeği

## Kernel Fonksiyonları

<div class="two-columns">

<div class="function-card">
### 📋 Sistem Çağrıları
User-space ve kernel-space arasında köprü
- Sistem çağrı arayüzü
- API yönetimi
- Güvenlik kontrolü
</div>

<div class="function-card">
### 🔄 Process Yönetimi
Process'leri izleme ve kontrol
- Process oluşturma ve sonlandırma
- Zamanlama (scheduling)
- Process hiyerarşisi
</div>

<div class="function-card">
### 💾 Bellek Yönetimi
RAM ve sanal bellek yönetimi
- Memory allocation
- Virtual memory
- Bellek koruma
</div>

<div class="function-card">
### 📁 Sanal Dosya Sistemleri
Dosya sistemleri soyutlama katmanı
- /proc, /sys sanal dosya sistemleri
- Dosya sistemi API'si
- Mount noktaları
</div>

<div class="function-card">
### 🌐 Ağ Yönetimi
Ağ iletişimi ve protokoller
- Socket yönetimi
- Network stack
- Güvenlik duvarları
</div>

<div class="function-card">
### 🔧 Cihaz Sürücüleri
Donanım yazılım arayüzleri
- Device driver'lar
- Donanım erişimi
- IRQ yönetimi
</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Process Yönetimi

---

![bg](../gorseller/3_normal_slayt.png)

# Process Yönetimi

<div class="two-columns">

<div class="process-info-card">
### 🔄 Process Nedir?

<div class="process-icon">📊</div>

- **/proc dizininde sanal dosya sistemi**
- **Her process'in PID'si vardır**
- **PID 1 her zaman sistemdedir**
- **Parent-child ilişkisi vardır**
- **Process state'leri (running, sleeping, zombie)**

</div>

<div class="process-tree-card">
### 🌳 Process Hiyerarşisi

<div class="tree-visualization">
```
init (PID 1)
├── cron
├── sshd
├── login
│   └── bash
│       └── firefox
└── rsyslogd
```
</div>

**Ana Process'ler:**
- **init/systemd** - PID 1
- **kthreadd** - Kernel thread'ları
- **ksoftirqd** - SoftIRQ handler'ları

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Process Komutları

## ps Komutu

<div class="compare-box">
```bash
ps              # Mevcut shell process'leri
ps aux          # Tüm process'ler
ps -u root      # Root process'leri
ps --forest     # Hiyerarşik gösterim
```
</div>

## top Komutu

- Gerçek zamanlı izleme
- CPU ve bellek kullanımı
- Sistem yükü

---

![bg](../gorseller/3_normal_slayt.png)

# top Komutu

## Sistem Bilgisi

<div class="two-columns">
<div>

```bash
top - 15:26:56 up 28 days
Tasks: 156 total
%Cpu(s): 0.2 us, 99.6 id
KiB Mem: 132014640 total
```

**Kısayollar:**
- K: Process sonlandırma
- R: Öncelik ayarlama
- q: Çıkış

</div>
<div>

**Process Listesi:**
| PID | USER | COMMAND |
|-----|------|---------|
| 1   | root | init |
| 72  | admin| top |

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Bellek Yönetimi

---

![bg](../gorseller/3_normal_slayt.png)

# Bellek Yönetimi

<div class="two-columns">

<div class="memory-concept-card">
### 💾 Virtual Bellek

<div class="memory-icon">🧠</div>

**Özellikler:**
- **Fiziksel bellek paylaşılır**
- **Sanal adresleme çakışmaları önler**
- **User Space vs Kernel Space**
- **Memory protection**
- **Page fault handling**

</div>

<div class="memory-command-card">
### 📊 free Komutu

<div class="command-icon">⌨️</div>

```bash
free        # Bellek durumu
free -m      # MB cinsinden
free -g      # GB cinsinden
free -s 10   # 10 saniyede bir
free -h      # İnsan-okunur format
```

**En çok kullanılan:**
`free -h` (Human readable format)

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Bellek Analizi

## Çıktı Analizi

<div class="two-columns">
<div>

```bash
total        used        free
Mem: 132014640  47304084 84085528
Swap: 134196220   42544  134153676
```

</div>
<div>

**Bileşenler:**
- Mem: Fiziksel RAM
- Swap: Sanal bellek
- Available: Kullanılabilir
- Buffers/Cache: Geçici

</div>
</div>

<div class="highlight-box">
**⚠️ Uyarı:**
Düşük bellek sistem çökmesine neden olabilir
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Log Dosyaları

---

![bg](../gorseller/3_normal_slayt.png)

# Log Dosyaları

## Log Dosyaları

<div class="info-box">
**Önemi:**
- Sorun giderme
- Güvenlik denetimi
- Performans izleme
- Hata ayıklama
</div>

## /var/log Yapısı

| Dosya | İçerik |
|-------|--------|
| messages | Genel sistem mesajları |
| secure | Güvenlik logları |
| dmesg | Kernel başlangıç |
| boot.log | Sistem başlangıç |
| cron | Zamanlanmış görevler |

---

![bg](../gorseller/3_normal_slayt.png)

# Log İzleme

## journalctl

<div class="compare-box">
```bash
journalctl         # Tüm loglar
journalctl -n 100  # Son 100 satır
journalctl -u sshd # SSH logları
journalctl -f      # Gerçek zamanlı
```
</div>

## Geleneksel Komutlar

```bash
tail -f /var/log/messages
grep error /var/log/syslog
```

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Kernel Mesajları

---

![bg](../gorseller/3_normal_slayt.png)

# Kernel Mesajları

## dmesg Komutu

- Kernel ring buffer mesajları
- Donanım ve sürücü sorunları
- Başlangıç hataları

## Kullanım

<div class="compare-box">
```bash
dmesg                    # Tüm mesajlar
dmesg | grep -i usb     # USB mesajları
dmesg | grep -i memory  # Bellek mesajları
dmesg -w                 # Gerçek zamanlı
```
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# FHS Standardı

---

![bg](../gorseller/3_normal_slayt.png)

# FHS Standardı

<div class="two-columns">

<div class="fhs-purpose-card">
### 📁 Filesystem Hierarchy Standard

<div class="fhs-icon">🏗️</div>

<div class="highlight-box">
**Temel Amaçlar:**
- **Tutarlılık** - Tüm Linux dağıtımları aynı yapıyı kullanır
- **Bakım kolaylığı** - Yöneticiler klasör yapısını bilir
- **Otomasyon desteği** - Script'ler standart yolları kullanabilir
- **Standart öğrenme** - Tek standart öğrenme yeterli
</div>

</div>

<div class="fhs-categorization-card">
### 📋 Kategorizasyon

<table class="fhs-table">
<thead>
<tr>
  <th rowspan="2">Kategori</th>
  <th>Paylaşılabilir</th>
  <th>Paylaşılamaz</th>
</tr>
<tr>
  <th>Değişken</th>
  <th>Statik</th>
</tr>
</thead>
<tbody>
<tr>
  <td>📧 Veri</td>
  <td>/var/mail</td>
  <td>/var/lock</td>
</tr>
<tr>
  <td>🔧 Yazılım</td>
  <td>/opt</td>
  <td>/etc</td>
</tr>
</tbody>
</table>

**Önemli Kural:**
- **Paylaşılabilir** → Network üzerinden paylaşılabilir
- **Paylaşılamaz** → Makineye özgü

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Dizin Yapısı

## Root Hiyerarşisi

<div class="two-columns">
<div>

**Sistem:**
- / - Kök dizin
- /bin - Temel komutlar
- /boot - Başlangıç dosyaları
- /dev - Cihaz dosyaları
- /etc - Yapılandırma
- /lib - Kütüphaneler
- /proc - Sanal sistem

</div>
<div>

**Kullanıcı:**
- /home - Ev dizinleri
- /root - Root ev dizini
- /sys - Sistem bilgisi
- /tmp - Geçici dosyalar
- /usr - İkinci hiyerarşi
- /var - Değişken veri
- /srv - Servis dosyaları

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# /usr Hiyerarşisi

## İkinci Hiyerarşi

- Çoklu kullanıcı yazılımları
- Network paylaşılabilir
- Salt okunur

| Alt Dizin | İçerik |
|-----------|--------|
| /usr/bin | Kullanıcı komutları |
| /usr/sbin | Sistem komutları |
| /usr/lib | Kütüphaneler |
| /usr/share | Paylaşılır veri |
| /usr/local | Yerel yazılımlar |

## /usr/local

Paket yöneticisi: /usr altına
Manuel kurulum: /usr/local altına

---

![bg](../gorseller/3_normal_slayt.png)

# /var Hiyerarşisi

## Dördüncü Hiyerarşi

- Zamanla değişen dosyalar
- Yoğun I/O kullanımı
- Hızlı disk dolma

<div class="highlight-box">
**⚠️ Critical:**
- Hızlı dolar
- Düzenli temizlik gerekir
- logrotate kullanımı
- Ayrı partition önerilir
</div>

| Alt Dizin | İçerik |
|-----------|--------|
| /var/log | Log dosyaları |
| /var/cache | Önbellek |
| /var/spool | Kuyruklar |
| /var/mail | Posta kutuları |
| /var/tmp | Kalıcı temp |

---

![bg](../gorseller/3_normal_slayt.png)

# Pratik Komutlar

## Sistem Bilgileri

<div class="two-columns">
<div>

**Process:**
```bash
ps aux | head -10
top -b -n 1 | head -15
```

**Bellek:**
```bash
free -h
cat /proc/meminfo
```

**Disk:**
```bash
df -h
du -sh /var/log
```

</div>
<div>

**Sistem:**
```bash
uptime
cat /proc/loadavg
```

**Kernel:**
```bash
uname -a
dmesg | tail
```

**Kütüphane:**
```bash
ldd /usr/bin/firefox
ldconfig -p
```

</div>
</div>

---

<!-- _class: final-slide -->

# Özet

## Bölüm 13 Kapsamı

<div class="info-box">
**Öğrenilenler:**
- Linux kerneli fonksiyonları
- Process yönetimi (ps, top)
- Bellek yönetimi
- Log dosyaları ve izleme
- FHS standartı
- Kütüphane yönetimi

**Komutlar:**
- ps, top, free, journalctl, dmesg
- /proc, /sys, /var/log
</div>

---

<!-- _class: final-slide -->

# Teşekkürler

## Bölüm 14: Ağ Yapılandırması

**Sorularınız?**