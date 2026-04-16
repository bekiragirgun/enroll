# Proxmox Kurulum Planları - Ders Modüllerine Göre

## 📋 Seçenekler

### Seçenek 1: Modül Bazlı CT (Container) Oluşturma

Her ders modülü için özel CT oluşturulur.

**Avantajları:**
- Her modül için izole çalışma ortamı
- Öğrenci hatası diğer modülleri etkilemez
- Snapshot ile kolay geri dönme

**Dezavantajları:**
- Daha fazla kaynak kullanımı (15 CT × 2GB = 30GB RAM)
- Yönetim zorluğu

**Kurulum:**
```bash
# Her modül için CT oluştur
./proxmox-modul-kur.sh --modul 1  # Linux'a Giriş
./proxmox-modul-kur.sh --modul 2  # İşletim Sistemleri
# ...
```

---

### Seçenek 2: Tema Bazlı Gruplama (ÖNERİLEN)

Modülleri konularına göre 4-5 grupta toplarız.

**Gruplandırma:**

| Grup | Modüller | Konu | CT ID | Kaynak |
|------|----------|------|-------|--------|
| **Temel** | 1-5 | Linux giriş, komut satırı | 9010 | 2GB RAM, 2 CPU |
| **Dosya** | 6-8 | Dosya yönetimi, script | 9011 | 2GB RAM, 2 CPU |
| **Sistem** | 9-12 | Donanım, ağ, güvenlik | 9012 | 4GB RAM, 4 CPU |
| **İzinler** | 13-15 | Kullanıcı, izinler | 9013 | 2GB RAM, 2 CPU |

**Avantajları:**
- Dengeli kaynak kullanımı (toplam 10GB RAM)
- Yönetim kolaylığı
- Her tema için özel araçlar

**Kurulum:**
```bash
# Tüm temaları kur
./proxmox-tema-kur.sh --all

# Sadece belirli tema
./proxmox-tema-kur.sh --tema dosya
```

---

### Seçenek 3: Dinamik Provisioning (ESNEK)

Tek bir "master" CT oluşturulur, her dersten önce snapshot'tan clone alınır.

**Akış:**
1. Master template CT oluştur (9000)
2. Her dersten önce: Clone al (9010, 9011, ...)
3. Ders sonrası: CT'yi sil veya snapshot'tan dön

**Avantajları:**
- Minimum kaynak kullanımı
- Hızlı kurulum
- Esnek kullanım

**Kurulum:**
```bash
# Master template oluştur (tek seferlik)
./proxmox-master-kur.sh

# Her ders için clone oluştur
./proxmox-clone-olustur.sh --modul 1 --ogrenci sayisi=30
```

---

### Seçenek 4: Docker Container (HIZLI)

Her modül için Docker container, Proxmox içinde çalışır.

**Avantajları:**
- Çok hızlı başlatma (saniyeler)
- Minimum kaynak kullanımı
- Kolay yönetim

**Dezavantajları:**
- Sistem kısıtlamaları (privileged mode gerekli)
- Network complexity

**Kurulum:**
```bash
# Docker engine yüklü CT içinde
./proxmox-docker-kur.sh

# Her modül için container
docker run -d --name modul-1 linux-egitim:modul-1
```

---

## 🎯 Önerilen Kurulum: Seçenek 2 (Tema Bazlı)

### Neden?

1. **Dengeli Kaynak Kullanımı**: 4 CT × 2-4GB = 10GB RAM
2. **Yönetim Kolaylığı**: Sadece 4 CT yönetmek
3. **Konu Odaklı**: Her tema için özel araçlar
4. **Öğrenci Deneyimi**: Her öğrenci tüm temalarda çalışabilir

### Tema Detayları

#### Tema 1: Temel (Modül 1-5)
**Konu:** Linux'a giriş, komut satırı, dosya sistemi

**Gerekli Araçlar:**
```bash
# Temel komutlar
coreutils, grep, sed, awk, find, locate

# Yardım
man-db, man-pages

# Navigasyon
tree, ncdu

# Network (basit)
iproute2, iputils-ping
```

**Öğrenci Pratik:**
- Linux tarihçesi araştırması
- Temel komutlar (ls, cd, pwd, mkdir, vb.)
- Dosya sistemi navigasyonu
- man pages kullanımı

---

#### Tema 2: Dosya (Modül 6-8)
**Konu:** Dosya yönetimi, arşivleme, betik yazımı

**Gerekli Araçlar:**
```bash
# Arşivleme
tar, gzip, bzip2, xz, zip, unzip

# Metin işleme
grep, sed, awk, sort, uniq, cut

# Editörler
vim, nano

# Scripting
bash-completion
```

**Öğrenci Pratik:**
- Dosya arşivleme ve çıkarma
- Log dosyası analizi (grep, awk)
- Basit shell script yazımı
- Crontab ile otomasyon

---

#### Tema 3: Sistem (Modül 9-12)
**Konu:** Donanım, ağ, güvenlik

**Gerekli Araçlar:**
```bash>
# Donanım bilgisi
lshw, lscpu, lsblk, free, df, htop, iotop

# Network
net-tools, iproute2, curl, wget, dnsutils, nmap

# Güvenlik
ufw, fail2ban, auditd

# Kullanıcı yönetimi
adduser, usermod, sudo
```

**Öğrenci Pratik:**
- Sistem kaynaklarını izleme
- Network yapılandırması ve troubleshooting
- Kullanıcı ve grup yönetimi
- Firewall kuralları

---

#### Tema 4: İzinler (Modül 13-15)
**Konu:** Kullanıcı, grup, izinler

**Gerekli Araçlar:**
```bash
# İzin yönetimi
acl, attr

# Kullanıcı yönetimi
adduser, deluser, groupadd

# Sistem güvenliği
sudo, logrotate

# Özel dosyalar
sshd, systemd
```

**Öğrenci Pratik:**
- Kullanıcı ve grup oluşturma
- Dosya izinleri (chmod, chown)
- ACL kullanımı
- sudo yapılandırması
- SSH anahtar yönetimi

---

## 🚀 Hızlı Başlangıç

### 1. Tüm Temaları Kur

```bash
# 4 CT'yi de oluştur
./proxmox-deploy.sh --tema-all
```

### 2. Ders Öncesi Hazırlık

```bash
# Tema 1 için snapshot
pct snapshot 9010 "ders-basi-$(date +%Y%m%d)"

# Servisleri kontrol et
pct exec 9010 -- systemctl status
```

### 3. Ders Sırasında

```bash
# Öğrenci erişimi
ssh ogrenci@<CT_IP>        # Tema 1: 9010
ssh ogrenci@<CT_IP>        # Tema 2: 9011
# ...

# Web terminal
http://<CT_IP>:7681
```

### 4. Ders Sonrası

```bash
# Logları temizle
pct exec 9010 -- journalctl --vacuum-time=1d

# Snapshot al (isteğe bağlı)
pct snapshot 9010 "ders-sonu-$(date +%Y%m%d)"
```

---

## 📊 Kaynak Karşılaştırması

| Seçenek | CT Sayısı | RAM | CPU | Disk | Yönetim |
|---------|-----------|-----|-----|------|---------|
| Modül Bazlı | 15 | 30GB | 30 | 300GB | Zor |
| Tema Bazlı ⭐ | 4 | 10GB | 10 | 80GB | Kolay |
| Dinamik | 1+ | 2GB* | 2* | 20GB* | Orta |
| Docker | 1 | 4GB | 4 | 40GB | Kolay |

*Clone sayısına bağlı artar

---

## 🔧 Script'ler

### 1. Tema Bazlı Kurulum Scripti

```bash
#!/bin/bash
# proxmox-tema-kur.sh

TEMALAR=(
    "temel:9010:2:2"
    "dosya:9011:2:2"
    "sistem:9012:4:4"
    "izinler:9013:2:2"
)

for tema in "${TEMALAR[@]}"; do
    IFS=':' read -r ad ctid ram cores <<< "$tema"
    echo "Kuruluyor: $ad (CT: $ctid)"
    # CT oluştur ve konfigüre et
done
```

### 2. Clone Scripti

```bash
#!/bin/bash
# proxmox-clone-olustur.sh

MASTER_CT=9000
MODUL=$1
OGRENCI_SAYISI=${2:-30}

for i in $(seq 1 $OGRENCI_SAYISI); do
    pct clone $MASTER_CT ${MODUL}${i} --hostname "ogrenci-${i}"
done
```

---

## 🎯 Sonraki Adım

Hangi seçeneği uygulamak istersiniz?

1. **Tema Bazlı (Önerilen)** - Şimdi uygulayalım
2. **Modül Bazlı** - Detaylı planlama yapalım
3. **Dinamik Provisioning** - Master template oluşturalım
4. **Docker** - Container yaklaşımı

Seçiminizi söyleyin, hemen uygulayalım! 🚀
