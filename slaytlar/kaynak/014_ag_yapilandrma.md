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
    line-height: 1.5;
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
    background-image: url('.../gorseller/1_ana_slayt.png');
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

  td {
    color: #333 !important;
    background-color: white !important;
  }

  th {
    background-color: #2D4A7C;
    color: white;
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

  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
  }

  section.compact-top {
    padding: 40px 50px 30px 50px !important;
  }
---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Ağ Yapılandırması

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Ağ Yapılandırmasına Giriş

---

![bg](../gorseller/3_normal_slayt.png)

# Ağ Yapılandırmasına Giriş

<div class="info-box">

### 🌐 Ağ Erişimin Önemi
Linux sistemlerde ağ erişimi temel bir özelliktir:
- Web tarama
- E-posta gönderme/alma
- Dosya transferi
- Uzak sistem yönetimi

</div>

### Linux Ağ Araçları
- **Yapılandırma araçları**: Ağ ayarlarını değiştirme
- **İzleme araçları**: Ağ performansını gözlemleme
- **Troubleshooting**: Sorun giderme komutları

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Temel Ağ Terminolojisi

---

![bg](../gorseller/3_normal_slayt.png)

# Temel Ağ Terminolojisi

<div class="two-columns">
<div>

### Temel Kavramlar

**Host**
- Ağa bağlı herhangi bir cihaz
- Bilgisayar, telefon, tablet, TV

**Network**
- İki veya daha fazla host'un birbiriyle iletişimi
- Kablolu veya kablosuz

**Internet**
- Milyonlarca host'u birbirine bağlayan küresel ağ
- Dünya çapında erişilebilir ağ

**Wi-Fi**
- Kablosuz ağ teknolojisi

**Service**
- Bir host tarafından sağlanan özellik
- Örnek: Web sayfası sunma

**Client**
- Server'a erişen host
- Örnek: Web tarayıcısı kullanan bilgisayar

**Router**
- Farklı ağları birbirine bağlayan makine
- Ağ trafiğini yönlendirir

</div>
<div>

<div class="highlight-box">

### Server

**Diğer host'lara hizmet sağlayan host**
- Web sunucusu, e-posta sunucusu
- Dosya sunucusu, veritabanı sunucusu
- 7/24 çalışan güçlü sistemler

</div>

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Temel Ağ Terminolojisi

<div class="highlight-box">

### 💡 Pratik Örnek

Ağınızdaki cihazları tanıyalım:

```bash
# Host bilgilerini görüntüle
hostname

# Ağ arayüzlerini listele
ip link show

# Varsayılan ağ geçidini görüntüle
ip route show
```

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Ağ Özellikleri Terminolojisi

---

![bg](../gorseller/3_normal_slayt.png)

# Ağ Özellikleri Terminolojisi

<div class="two-columns">
<div>

### İletişim Terimleri

**Packet**
- Ağ iletişimini küçük parçalara bölme
- Veri transferinde verimlilik sağlar

**IP Address**
- Ağdaki her host için benzersiz numara
- Ağ paketlerinde adresleme için kullanılır

**Mask (Subnet Mask)**
- Hangi IP adreslerinin aynı ağda olduğunu tanımlar
- Ağların sınırlarını belirler

**Hostname**
- Host'lar için insanların hatırlayabileceği isim
- IP adreslerine çevrilir

**URL**
- İnternetteki kaynakların konumu
- Örnek: `http://www.example.com`

</div>
<div class="highlight-box">

### 🔧 Protokoller ve Hizmetler

**DHCP**
- Dinamik Host Yapılandırma Protokolü
- Host'lara otomatik IP atar

**DNS**
- Domain Name System
- Domain isimlerini IP adreslerine çevirir

**Ethernet**
- Kablolu ağlarda fiziksel bağlantı
- Farklı hızları destekler (10 Mbps - 100 Gbps)

**TCP/IP**
- Ağ iletişimi için protokol koleksiyonu
- IP adresleme ve routing tanımlar

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# IP Adresleri

---

![bg](../gorseller/3_normal_slayt.png)

# IP Adresleri

<div class="two-columns">
<div>

### IPv4

**Yapı:**
- 32-bit adres (4 x 8-bit)
- Örnek: `192.168.10.120`
- Her sayı: 0-255 arası

**Sınırlar:**
- Teknik sınır: ~4.3 milyar adres
- Birçoğu kullanılamaz
- Adres tükenmesi sorunu

</div>
<div class="highlight-box">

### 📊 IPv6

**Yapı:**
- 128-bit adres
- Örnek: `2001:0db8:85a3:0042:1000:8a2e:0370:7334`
- Çok daha büyük adres havuzu

**Avantajları:**
- Daha iyi hız
- Gelişmiş paket yönetimi
- Verimli veri transferi

**Durum:**
- %98-99 cihaz hâlâ IPv4 kullanıyor
- Geçiş yavaş ilerliyor

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# IPv4'ten IPv6'ye Geçiş Neden Yavaş?

---

![bg](../gorseller/3_normal_slayt.png)

# IPv4'ten IPv6'ye Geçiş Neden Yavaş?

<div class="two-columns">
<div>

### 🔄 NAT (Network Address Translation)

**Çözüm:**
- Birden fazla host'un tek IP adresini paylaşması
- Özel ağ + özel router → tek IP
- Adres tükenmesi sorununu çözdü

**Sonuç:**
- IPv6'ye geçiş aciliği azaldı
- Organizasyonlar NAT kullanıyor

</div>
<div class="info-box">

### ⚙️ Porting (Teknoloji Değişimi)

**Sorun:**
- Tüm host'ların IPv6 özelliklerini kullanabilmesi gerekli
- İnternetteki tüm cihazların değiştirilmesi zor

**Meydan Okuma:**
- Büyük ölçekli değişim zorlu
- Uyum sorunları
- Maliyet ve zaman

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Ağ Cihazlarını Yapılandırma

---

![bg](../gorseller/3_normal_slayt.png)

# Ağ Cihazlarını Yapılandırma

<div class="two-columns">
<div>

### Temel Sorular

**Kablolu veya Kablosuz?**
- Kablosuz: Güvenlik ayarları eklenir
- Kablolu: Daha kararlı çalışır

**DHCP veya Statik IP?**
- DHCP: Otomatik yapılandırma
- Statik: Manuel yapılandırma

### Kullanım Senaryoları

**Masaüstü Bilgisayarlar**
- Genellikle kablolu ağ
- Statik IP veya DHCP

**Dizüstü Bilgisayarlar**
- Kablosuz ağ
- Neredeyse her zaman DHCP

**Sunucular**
- Kablolu ağ
- Statik IP (genellikle)

</div>
<div class="highlight-box">

### 💡 Pratik Örnek

```bash
# DHCP ile IP al
sudo dhclient eth0

# Statik IP atama (geçici)
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0

# Varsayılan ağ geçidini ayarla
sudo route add default gw 192.168.1.1

# DNS sunucusunu ayarla
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Ağ Yapılandırma Dosyaları

---

![bg](../gorseller/3_normal_slayt.png)

# Ağ Yapılandırma Dosyaları

<div class="info-box">

### 📁 CentOS/RHEL - IPv4 Yapılandırma Dosyası

**Konum:** `/etc/sysconfig/network-scripts/ifcfg-eth0`

```bash
DEVICE="eth0"
BOOTPROTO=none
NM_CONTROLLED="yes"
ONBOOT=yes
TYPE="Ethernet"
IPADDR=192.168.1.100
PREFIX=24
GATEWAY=192.168.1.1
DNS1=192.168.1.1
```

**DHCP için:**
```bash
BOOTPROTO=dhcp
# IPADDR, GATEWAY, DNS1 kaldırılır
```

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Ağ Yapılandırma Dosyaları

<div class="info-box">

### 📝 Yapılandırma Notları

**Temel parametreler:**
- `DEVICE`: Ağ arayüzü adı
- `BOOTPROTO`: none (statik) veya dhcp (dinamik)
- `ONBOOT`: Başlangıçta aktif et
- `IPADDR`: IPv4 adresi
- `PREFIX`: Subnet maskesi (örn: /24)
- `GATEWAY`: Varsayılan ağ geçidi
- `DNS1`: Birincil DNS sunucusu

**Değişiklikleri uygulamak için:**
```bash
sudo systemctl restart network
```

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# IPv6 Yapılandırması

---

![bg](../gorseller/3_normal_slayt.png)

# IPv6 Yapılandırması

<div class="two-columns">
<div>

### Statik IPv6 Adresi

**ifcfg-eth0 dosyasına ekle:**
```bash
IPV6INIT=yes
IPV6ADDR=2001:db8::100
IPV6_DEFAULTGW=2001:db8::1
```

**/etc/sysconfig/network dosyası:**
```bash
NETWORKING_IPV6=yes
```

### DHCPv6 İstemcisi

**ifcfg-eth0 dosyasına ekle:**
```bash
IPV6INIT=yes
DHCPV6C=yes
```

</div>
<div class="compare-box">

### ⚠️ Ağ Arayüzünü Yeniden Başlatma

**Yöntem 1 - Sadece tek arayüz:**
```bash
sudo ifdown eth0
sudo ifup eth0
```

**Yöntem 2 - Tüm ağ servisi:**
```bash
sudo systemctl restart network
# Eski sistemlerde:
sudo service network restart
```

**⚠️ Dikkat:** Yöntem 2 tüm ağ arayüzlerini etkiler!

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# DNS Yapılandırması

---

![bg](../gorseller/3_normal_slayt.png)

# DNS Yapılandırması

<div class="two-columns">
<div>

### /etc/resolv.conf Dosyası

**DNS sunucusu adresi:**
```bash
sysadmin@localhost:~$ cat /etc/resolv.conf
nameserver 127.0.0.1
nameserver 8.8.8.8
nameserver 8.8.4.4
```

### DNS Sorgusu

**host komutu ile:**
```bash
sysadmin@localhost:~$ host example.com
example.com has address 192.168.1.2
```

**Birden fazla nameserver:**
- Bir sunucu yanıt vermezse diğeri dener
- Yedeklilik sağlar

</div>
<div>

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# DNS Yapılandırması

<div class="highlight-box">

### 💡 Pratik DNS Testleri

```bash
# DNS sorgusu
dig example.com

# DNS sunucusu test
nslookup google.com

# Reverse DNS sorgusu
host 192.168.1.2

# /etc/resolv.conf dosyasını görüntüle
cat /etc/resolv.conf
```

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Ağ Yapılandırma Dosyaları - Genel Bakış

---

![bg](../gorseller/3_normal_slayt.png)

# Ağ Yapılandırma Dosyaları - Genel Bakış

<div class="compare-box">

### 📋 Kritik 3 Dosya

| Dosya | Açıklama |
|-------|-----------|
| **/etc/hosts** | Hostname → IP adres tablosu |
| **/etc/resolv.conf** | DNS sunucuları listesi |
| **/etc/nsswitch.conf** | Name resolution sırası |

### Name Resolution Sırası

**1. /etc/nsswitch.conf:**
```bash
hosts: files dns
```
- Önce `/etc/hosts` dosyasına bakar
- Sonra DNS sunucularına sorgular

**2. /etc/hosts:**
```bash
127.0.0.1   localhost
192.168.1.2  server.example.com
```

**3. /etc/resolv.conf:**
```bash
nameserver 10.0.2.3
nameserver 10.0.2.4
```

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Ağ İzleme Araçları

---

![bg](../gorseller/3_normal_slayt.png)

# Ağ İzleme Araçları

<div class="info-box">

### 🔍 Kullanım Alanları

**Neden İhtiyacımız Var?**
- Ağ sorunlarını giderme
- Ağ performansını izleme
- Bağlantı sorunlarını tespit
- Güvenlik analizi

**Temel Araçlar:**
1. `ifconfig` - Arayüz bilgileri
2. `ip` - Modern ağ komutu
3. `ping` - Ulaşılabilirlik testi
4. `netstat` - Bağlantı istatistikleri
5. `ss` - Socket istatistikleri
6. `dig`/`host` - DNS sorguları
7. `ssh` - Uzak bağlantı

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# ifconfig Komutu

---

![bg](../gorseller/3_normal_slayt.png)

# ifconfig Komutu

<div class="highlight-box">

### 📱 Interface Yapılandırması

```bash
root@localhost:~# ifconfig
eth0      Link encap:Ethernet  HWaddr 00:0c:29:71:f0:bb
          inet addr:192.168.1.2  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:fe71:f0bb/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8506 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1201 errors:0 dropped:0 overruns:0 carrier:0

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
```

</div>

<div class="two-columns">
<div>

### Önemli Bilgiler

**eth0 arayüzü:**
- IPv4: 192.168.1.2
- Durum: UP (aktif)
- MAC: 00:0c:29:71:f0:bb

**lo (loopback):**
- 127.0.0.1
- Yerel iletişim için

### 💡 Pratik Kullanım

```bash
# Tüm arayüzleri görüntüle
ifconfig

# Sadece eth0 arayüzü
ifconfig eth0

# Geçici IP atama
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0
```

</div>
<div class="compare-box">

### ⚠️ Deprecation Uyarısı

**ifconfig eskimektir!**
- Yerini `ip` komutu aldı
- Bazı dağıtımlarda artık mevcut değil
- Ancak uyumluluk için hâlâ kullanılıyor

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# ip Komutu

---

![bg](../gorseller/3_normal_slayt.png)

# ip Komutu

<div class="highlight-box">

### 🔧 Modern Ağ Komutu

**Sözdizimi:**
```bash
ip [OPTIONS] OBJECT COMMAND
```

**Adres görüntüleme:**
```bash
root@localhost:~# ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP>
    inet 127.0.0.1/8 scope host lo

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>
    inet 192.168.1.2/24 brd 192.168.1.255 scope global eth0
```

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# ip Komutu

<div class="two-columns">
<div>

### ip vs ifconfig

**ip avantajları:**
- Daha fazla işlevsellik
- Tüm ağ işlemleri tek komutla
- `route`, `arp` gibi eski komutların yerini alıyor

### 💡 Pratik Örnekler

```bash
# Tüm arayüzleri listele
ip addr show

# IPv4 adresleri görüntüle
ip -4 addr show

# IPv6 adresleri görüntüle
ip -6 addr show

# Arayüz istatistikleri
ip -s link show eth0
```

</div>
<div class="info-box">

### 📊 ip Komutu Ailesi

**Yaygın kullanımlar:**
- `ip addr show` - Adres bilgisi
- `ip route show` - Routing tablosu
- `ip link show` - Link bilgisi
- `ip -s link` - İstatistikler

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# route Komutu

---

![bg](../gorseller/3_normal_slayt.png)

# route Komutu

<div class="two-columns">
<div>

### Routing Tablosu

```bash
root@localhost:~# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
192.168.1.0     *               255.255.255.0   U     0      0        0 eth0
default         192.168.1.1     0.0.0.0        UG    0      0        0 eth0
```

**Açıklama:**
- 192.168.1.0/24 → Yerel ağ, gateway yok
- default → İnternet, gateway: 192.168.1.1

### 💡 Pratik Örnekler

```bash
# Routing tablosunu görüntüle
route

# Sayısal çıktı
route -n

# Varsayılan gateway'i ekle
sudo route add default gw 192.168.1.1

# Gateway'i sil
sudo route del default gw 192.168.1.1
```

</div>
<div class="highlight-box">

### 🔄 Modern Alternatif: ip route

**Eski:** `route -n`

**Yeni:** `ip route show`

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# ping Komutu

---

![bg](../gorseller/3_normal_slayt.png)

# ping Komutu

<div class="two-columns">
<div>

### Ulaşılabilirlik Testi

**Başarılı ping:**
```bash
$ ping -c 4 192.168.1.2
PING 192.168.1.2 (192.168.1.2) 56(84) bytes of data.
64 bytes from 192.168.1.2: icmp_req=1 ttl=64 time=0.051 ms
64 bytes from 192.168.1.2: icmp_req=2 ttl=64 time=0.064 ms
64 bytes from 192.168.1.2: icmp_req=3 ttl=64 time=0.050 ms
64 bytes from 192.168.1.2: icmp_req=4 ttl=64 time=0.043 ms

--- 192.168.1.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
```

**Başarısız ping:**
```bash
$ ping -c 4 192.168.1.1
From 192.168.1.2 icmp_seq=1 Destination Host Unreachable
--- 192.168.1.1 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss
```

</div>
<div class="info-box">

### ⚠️ Önemli Notlar

**Ping başarısız olabilir:**
- Hedef sistem ping'i yanıt vermiyor olabilir
- Güvenlik nedeniyle engellenmiş olabilir
- Firewall ping'i bloklamış olabilir

**Pratik yaklaşım:**
1. Önce hostname ile ping
2. Başarısızsa IP adresi ile dene
3. Bu, DNS sorununu ayırt eder

**💡 Kullanım:**
```bash
# 4 paket gönder
ping -c 4 google.com

# Sonsuz döngü (Ctrl+C ile durdur)
ping 192.168.1.1
```

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# netstat Komutu

---

![bg](../gorseller/3_normal_slayt.png)

# netstat Komutu

<div class="two-columns">
<div>

### Ağ İstatistikleri

**Interface istatistikleri:**
```bash
$ netstat -i
Kernel Interface table
Iface   MTU Met   RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR
eth0    1500 0       137      0      4 0        12      0
lo      65536 0        18      0      0 0        18      0
```

**Açık portlar:**
```bash
$ netstat -tln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address
tcp        0      0 0.0.0.0:22              0.0.0.0:*     LISTEN
tcp        0      0 127.0.0.1:53            0.0.0.0:*     LISTEN
```

### 💡 Pratik Örnekler

```bash
# Routing tablosu
netstat -r

# Tüm bağlantılar
netstat -an

# TCP bağlantıları
netstat -tnp
```

</div>
<div class="compare-box">

### ⚠️ Deprecation Uyarısı

**netstat eskimektir!**
- Yerini `ss` komutu alıyor
- `netstat -r` → `ip route`
- `netstat -i` → `ip -s link`
- `netstat -g` → `ip maddr`

**Ancak:**
- Hâlâ yaygın olarak kullanılıyor
- Bazı sistemlerde hâlâ varsayılan

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# ss Komutu

---

<!-- _class: compact-top -->

![bg](../gorseller/3_normal_slayt.png)

# ss Komutu

<div class="two-columns">
<div>

### Socket İstatistikleri

**Tüm socket'ler:**
```bash
$ ss
Netid  State      Recv-Q Send-Q   Local Address:Port
u_str  ESTAB      0      0    * 104741               * 104740
tcp    ESTAB      0      0    192.168.1.2:22        10.0.0.5:54321
```

**Özet istatistikler:**
```bash
$ ss -s
Total: 1000
TCP:   7 (estab 1, time-wait 0)
UDP:   9
```

</div>
<div class="highlight-box">

### 🔍 ss vs netstat

**ss avantajları:**
- Daha hızlı ve verimli
- Daha fazla bilgi
- Daha gelişmiş filtreleme seçenekleri

</div>

</div>

---

<!-- _class: compact-top -->

![bg](../gorseller/3_normal_slayt.png)

# ss Komutu - Pratik Örnekler

<div class="highlight-box">

### 💡 Pratik Örnekler

```bash
# Tüm bağlantılar
ss -tuna

# Dinlenen portlar
ss -tlnp

# Process bilgileriyle
ss -tunp

# Socket istatistikleri
ss -s
```

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# DNS Sorgu Komutları

---

![bg](../gorseller/3_normal_slayt.png)

# DNS Sorgu Komutları

<div class="two-columns">
<div>

### dig Komutu

**Detaylı DNS sorgusu:**
```bash
$ dig example.com
; <<>> DiG 9.8.1-P1 <<>> example.com
;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            86400   IN      A   192.168.1.2
```

**Başarısız sorgu:**
```bash
$ dig sample.com
connection timed out; no servers could be reached
```

### host Komutu

<div class="highlight-box">

### 📌 Basit DNS sorgusu:

```bash
$ host example.com
example.com has address 192.168.1.2

$ host 192.168.1.2
2.1.168.192.in-addr.arpa domain name pointer example.com
```

</div>

### 💡 Pratik Örnekler

```bash
# DNS sorgusu
dig google.com

# Reverse DNS
host 8.8.8.8

# MX kayıtları
dig example.com MX

# NS kayıtları
dig example.com NS
```

<div class="compare-box">

### 📋 Komut Karşılaştırması

<table>
<tr>
<th style="background-color: #2D4A7C; color: white;">Özellik</th>
<th style="background-color: #2D4A7C; color: white;">dig</th>
<th style="background-color: #2D4A7C; color: white;">host</th>
</tr>
<tr>
<td style="background-color: white; color: #333;">Detay seviyesi</td>
<td style="background-color: white; color: #333;">Yüksek</td>
<td style="background-color: white; color: #333;">Orta</td>
</tr>
<tr>
<td style="background-color: white; color: #333;">Çıktı formatı</td>
<td style="background-color: white; color: #333;">Karmaşık</td>
<td style="background-color: white; color: #333;">Basit</td>
</tr>
<tr>
<td style="background-color: white; color: #333;">Kayıt türleri</td>
<td style="background-color: white; color: #333;">Tümü</td>
<td style="background-color: white; color: #333;">Temel</td>
</tr>
<tr>
<td style="background-color: white; color: #333;">Kullanım</td>
<td style="background-color: white; color: #333;">Detaylı analiz</td>
<td style="background-color: white; color: #333;">Hızlı sorgu</td>
</tr>
</table>

**💡 Tavsiye:**
- Günlük kullanım için `host`
- Sorun giderme için `dig`

</div>

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# ssh Komutu

---

![bg](../gorseller/3_normal_slayt.png)

# ssh Komutu

<div class="two-columns">
<div>

### Uzak Bağlantı

**Bağlantı sözdizimi:**
```bash
ssh username@hostname
```

**Örnek:**
```bash
$ ssh bob@testserver
The authenticity of host 'testserver' can't be established.
RSA key fingerprint is c2:0d:ff:27:4c:f8:69:a9:c6:3e:13:da:2f:47:e4:c9.
Are you sure you want to continue connection (yes/no)? yes
bob@testserver's password: ********
bob@testserver:~$ date
Fri Oct  4 16:14:43 CDT 2013
```

**Çıkış:**
```bash
bob@testserver:~$ exit
logout
Connection to testserver closed.
```

</div>
<div class="compare-box">

### ⚠️ RSA Key Fingerprint

**İlk bağlantıda:**
- Host'un RSA parmak izi gösterilir
- `yes` ile kabul edilir
- Sonraki bağlantılarda otomatik

**Key değişirse:**
- Uyarı mesajı gösterilir
- "REMOTE HOST IDENTIFICATION HAS CHANGED!"
- Man-in-the-middle saldırısı olabilir

</div>

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# ssh Komutu

<div class="highlight-box">

### 💡 Pratik Örnekler

```bash
# Kullanıcı adıyla bağlan
ssh user@192.168.1.100

# Farklı port kullan
ssh -p 2222 user@hostname

# Komut uzaktan çalıştır
ssh user@hostname 'ls -la /tmp'
```

**⚠️ RSA Key Sorunu Çözümü:**
```bash
# Eski key'i sil
rm ~/.ssh/known_hosts

# Tekrar bağlan
ssh user@hostname
```

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Pratik Uygulamalar

---

![bg](../gorseller/3_normal_slayt.png)

# Pratik Uygulamalar

<div class="two-columns">
<div>

### 1️⃣ Ağ Sorunlarını Giderme

**Adım adım:**
```bash
# 1. Kendi IP adresini görüntüle
ip addr show

# 2. Gateway'e ping test
ping -c 4 192.168.1.1

# 3. DNS test
ping -c 4 8.8.8.8

# 4. İnternet test
ping -c 4 google.com

# 5. DNS sorgusu
dig google.com
```

</div>
<div>

### 2️⃣ Ağ Arayüzünü Yapılandırma

```bash
# Mevcut yapılandırma görüntüle
cat /etc/sysconfig/network-scripts/ifcfg-eth0

# Geçici IP atama
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0 up

# Routing tablosunu görüntüle
ip route show
```

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Pratik Uygulamalar

<div class="highlight-box">

### 3️⃣ Bağlantı İzleme

**Aktif bağlantılar:**
```bash
ss -tunp
```

**Açık portlar:**
```bash
ss -tlnp
```

**Ağ trafiği:**
```bash
sudo tcpdump -i eth0
```

**Interface istatistikleri:**
```bash
ip -s link show eth0
```

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Pratik Uygulamalar

<div class="highlight-box">

### 4️⃣ DNS Sorun Giderme

**Name resolution test:**
```bash
# Hostname çözümleme
host example.com

# Detaylı DNS sorgusu
dig example.com ANY

# Reverse DNS
host 192.168.1.2
```

</div>

---

<!-- _class: final-slide -->

# Teşekkürler!

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü
