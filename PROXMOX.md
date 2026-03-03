# Proxmox CT Deployment Rehberi

Bu rehber, Kapadokya Ders Takip Sistemi'nin Proxmox CT (LXC Container) üzerinde çalıştırılması için hazırlanmıştır.

## 🎯 Mimari

Sistem iki ayrı CT olarak çalışır:

| CT | ID | Hostname | Amaç |
|----|----|----------|------|
| **Web** | 9001 | ders-takip-web | Flask web uygulaması, öğrenci/öğretmen arayüzü |
| **Terminal** | 9002 | linux-egitim | Öğrenciler için Linux eğitim ortamı, web terminal |

## 📋 Gereksinimler

- **Proxmox VE** kurulu bir sunucu (v7.x+ önerilir)
- **Kaynaklar:**
  - Web CT: 2GB RAM, 2 CPU, 20GB disk
  - Terminal CT: 2GB RAM, 2 CPU, 20GB disk
- **Network:** Bridge (vmbr0) varsayılan
- **Depolama:** local-lvm veya benzeri

## 🚀 Hızlı Kurulum

### 1. Scripti İndirin

```bash
# Proxmox host üzerinde
cd /root
# Scripti projenizden kopyalayın veya buraya upload edin
```

### 2. Scripti Çalıştırın

```bash
# Her iki container'ı da oluştur (varsayılan)
./proxmox-deploy.sh

# Sadece web container oluştur
./proxmox-deploy.sh --web-only

# Sadece terminal container oluştur
./proxmox-deploy.sh --term-only

# Kurulumu test et (gerçek işlem yok)
./proxmox-deploy.sh --dry-run
```

### 3. Tamamlandı

Script otomatik olarak:
- ✅ Debian 12 template indirir
- ✅ İki CT oluşturur ve yapılandırır
- ✅ Sistem güncellemelerini yapar
- ✅ Gerekli paketleri yükler
- ✅ Servisleri başlatır

## 📝 Detaylı Kullanım

### Script Seçenekleri

```
KULLANIM:
    ./proxmox-deploy.sh [SEÇENEKLER]

SEÇENEKLER:
    -h, --help              Bu yardım mesajını göster
    -w, --web-only          Sadece web container oluştur
    -t, --term-only         Sadece terminal container oluştur
    -b, --both              Her iki container'ı da oluştur (varsayılan)
    -c, --config <dosya>    Konfigürasyon dosyası kullan
    -s, --skip-template     Template indirmeyi atla
    --dry-run               Kurulum simülasyonu yap (gerçek işlem yok)

ÖRNEKLER:
    # İki container'ı da oluştur (varsayılan)
    ./proxmox-deploy.sh

    # Sadece web container oluştur
    ./proxmox-deploy.sh --web-only

    # Özel konfigürasyon ile
    ./proxmox-deploy.sh --config my-config.sh

    # Kurulumu test et (gerçek işlem yok)
    ./proxmox-deploy.sh --dry-run
```

### Özel Konfigürasyon

Varsayılan ayarları değiştirmek için bir konfigürasyon dosyası oluşturun:

```bash
# config.sh
CTID_WEB=9010
CTID_TERM=9011
MEMORY=4096
CORES=4
DISK_SIZE=40
STORAGE="local-zfs"
BRIDGE="vmbr0"
```

Kullanımı:

```bash
./proxmox-deploy.sh --config config.sh
```

## 🌐 Erişim Bilgileri

### Web Container (9001)

```
Web Paneli:    http://<CT_IP>
Öğretmen:      http://<CT_IP>/teacher
Şifre:         linux2024

Yönetim:
pct enter 9001
systemctl status ders-takip
journalctl -u ders-takip -f
```

### Terminal Container (9002)

```
Web Terminal:  http://<CT_IP>:7681

SSH Erişimi:
ssh root@<CT_IP>
ssh ogrenci@<CT_IP>  (Şifre: ogrenci)

Yönetim:
pct enter 9002
systemctl status ttyd
```

## 🔧 CT Yönetimi

### Temel Komutlar

```bash
# Tüm CT'leri listele
pct list

# CT başlat/durdur
pct start <CT_ID>
pct stop <CT_ID>
pct restart <CT_ID>

# CT içine gir
pct enter <CT_ID>

# CT içinde komut çalıştır
pct exec <CT_ID> -- bash -c "komut"

# CT sil
pct destroy <CT_ID>

# Snapshot al
pct snapshot <CT_ID> <snapshot-adı>

# Snapshot'tan dön
pct rollback <CT_ID> <snapshot-adı>
```

### Log Görüntüleme

```bash
# Web CT logları
pct exec 9001 -- journalctl -u ders-takip -f
pct exec 9001 -- journalctl -u nginx -f

# Terminal CT logları
pct exec 9002 -- journalctl -u ttyd -f
```

## 🔄 Servis Yönetimi

### Web Container (9001)

```bash
pct exec 9001 -- systemctl status ders-takip
pct exec 9001 -- systemctl restart ders-takip
pct exec 9001 -- systemctl status nginx
```

### Terminal Container (9002)

```bash
pct exec 9002 -- systemctl status ttyd
pct exec 9002 -- systemctl restart ttyd
```

## 📊 Kaynak Kullanımı

### Minimum Kaynaklar

| CT | RAM | CPU | Disk |
|----|-----|-----|------|
| Web | 2GB | 2 | 20GB |
| Terminal | 2GB | 2 | 20GB |
| **Toplam** | **4GB** | **4** | **40GB** |

### Önerilen Kaynaklar

| CT | RAM | CPU | Disk |
|----|-----|-----|------|
| Web | 4GB | 4 | 40GB |
| Terminal | 4GB | 4 | 40GB |
| **Toplam** | **8GB** | **8** | **80GB** |

## 🔐 Güvenlik

### Firewall

```bash
# Web CT - Nginx için
pct exec 9001 -- ufw allow 80/tcp
pct exec 9001 -- ufw allow 443/tcp

# Terminal CT - SSH ve TTYD için
pct exec 9002 -- ufw allow 22/tcp
pct exec 9002 -- ufw allow 7681/tcp

# Firewall'ı etkinleştir
pct exec 9001 -- ufw enable
pct exec 9002 -- ufw enable
```

### SSH Güvenliği

```bash
# Root girişini kapat
pct exec 9002 -- sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
pct exec 9002 -- systemctl restart sshd

# Sadece anahtar tabanlı kimlik doğrulama
pct exec 9002 -- sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
pct exec 9002 -- systemctl restart sshd
```

## 🐛 Sorun Giderme

### CT Başlamıyor

```bash
# Logları kontrol et
journalctl -xe
pct status <CT_ID>

# CT loglarını görüntüle
pct exec <CT_ID -- journalctl -n 50
```

### Network Çalışmıyor

```bash
# Network konfigürasyonunu kontrol et
pct exec <CT_ID> -- ip addr
pct exec <CT_ID> -- ip route

# Bridge kontrol et
cat /etc/network/interfaces
```

### Template İndirilemiyor

```bash
# Manuel olarak indirin
wget https://download.proxmox.com/images/system/debian-12-standard_12.2-1_amd64.tar.zst \
  -O /var/lib/vz/template/cache/debian-12-standard_12.2-1_amd64.tar.zst

# Scripti --skip-template ile çalıştırın
./proxmox-deploy.sh --skip-template
```

### Servis Başlamıyor

```bash
# Web CT
pct exec 9001 -- systemctl status ders-takip
pct exec 9001 -- journalctl -u ders-takip -n 50

# Terminal CT
pct exec 9002 -- systemctl status ttyd
pct exec 9002 -- journalctl -u ttyd -n 50
```

## 📦 Backup ve Restore

### Backup

```bash
# Proxmox web arayüzünde
1. CT seçin
2. Backup -> Backup
3. Bekleyin

# Vzdump ile
vzdump 9001 --storage local --mode snapshot
vzdump 9002 --storage local --mode snapshot
```

### Restore

```bash
# Proxmox web arayüzünde
1. Backup listesinden seçin
2. Restore -> CT ID belirtin
3. Onaylayın

# CLI ile
pctrestore <backup-file> <new-ctid>
```

### Snapshot

```bash
# Ders öncesi snapshot
pct snapshot 9001 "ders-basi"
pct snapshot 9002 "ders-basi"

# Snapshot listele
pct snapshot-list 9001

# Snapshot'tan dön
pct rollback 9001 "ders-basi"
```

## 🎓 Kullanım Senaryoları

### Ders Öncesi Hazırlık

```bash
# 1. Snapshot al
pct snapshot 9001 "ders-basi-$(date +%Y%m%d)"
pct snapshot 9002 "ders-basi-$(date +%Y%m%d)"

# 2. Servisleri kontrol et
pct exec 9001 -- systemctl status ders-takip
pct exec 9002 -- systemctl status ttyd

# 3. IP adreslerini öğren
pct exec 9001 -- hostname -I
pct exec 9002 -- hostname -I
```

### Ders Sonrası Temizlik

```bash
# 1. Öğrenci oturumlarını kapat
pct exec 9002 -- pkill -u ogrenci

# 2. Logları temizle
pct exec 9001 -- journalctl --vacuum-time=1d
pct exec 9002 -- journalctl --vacuum-time=1d

# 3. İsteğe bağlı: Ders sonrası snapshot
pct snapshot 9001 "ders-sonu-$(date +%Y%m%d)"
```

### Öğrenci Erişimi

```bash
# SSH
ssh ogrenci@<TERM_IP>

# Web Terminal
http://<TERM_IP>:7681

# Web Paneli
http://<WEB_IP>
```

## 🔗 Faydalı Linkler

- [Proxmox VE Dokümantasyonu](https://pve.proxmox.com/wiki/Main_Page)
- [LXC Container Dokümantasyonu](https://pve.proxmox.com/wiki/Linux_Container)
- [TTYD Web Terminal](https://github.com/tsl0922/ttyd)

## 📞 Destek

Sorun yaşarsanız:
1. Script loglarını kontrol edin
2. CT loglarını inceleyin: `journalctl -xe`
3. Proxmox loglarını kontrol edin
4. Network ayarlarını doğrulayın

## 🎉 Başarılar!

Artık Kapadokya Ders Takip Sistemi Proxmox CT'lerde çalışıyor!
