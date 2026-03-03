# 🚀 Proxmox Deployment Talimatları

## Adım 1: Proxmox LXC Container Oluştur

Proxmox web panelinde veya SSH ile:

```bash
# Proxmox host SSH
ssh root@<proxmox-ip>

# Debian 11 template indir (yoksa)
pveam update
pveam download local debian-11-standard_11.3-1_amd64.tar.zst

# LXC Container oluştur (CT ID: 100)
pct create 100 local:vztmpl/debian-11-standard_11.3-1_amd64.tar.zst \
  --storage local-lvm \
  --cores 8 \
  --memory 16384 \
  --swap 2048 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.100/24,gw=192.168.1.1 \
  --hostname ders-takip \
  --rootfs local-lvm:50 \
  --onboot 1 \
  --unprivileged 0 \
  --features nesting=1

# Container'ı başlat
pct start 100

# Container'a gir
pct enter 100
```

## Adım 2: Container İçinde Hazırlık

```bash
# Container içinde (pct enter 100 sonrası)

# Sistem güncelle
apt update && apt upgrade -y

# Zaman dilimi ayarla
timedatectl set-timezone Europe/Istanbul
echo 'TZ="Europe/Istanbul"' >> /etc/environment

# Gerekli paketler
apt install -y \
  git \
  python3 \
  python3-pip \
  python3-venv \
  debootstrap \
  openssh-server \
  sudo \
  openssl \
  curl \
  wget

# Proje dizini oluştur
mkdir -p /root/ders_takip
cd /root/ders_takip

# Git'ten projeyi çek
git clone https://github.com/bekiragirgun/enroll.git .

# Veya manuel kopyalama (yukarıdaki komut çalışmazsa)
# exit
# scp -r /Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/* root@<proxmox-ip>:/root/ders_takip/
# pct enter 100

# Script'lere çalıştırma izni ver
chmod +x proxmox-chroot-deploy.sh
chmod +x chroot_login.sh
chmod +x chroot_yonetici.py

# Python virtual environment oluştur
python3 -m venv venv
source venv/bin/activate

# Paketleri yükle
pip install flask flask-socketio eventlet
```

## Adım 3: Chroot Template Kur

```bash
# Deploy script'ini çalıştır
./proxmox-chroot-deploy.sh

# Bu script:
# - Paketleri kurar
# - Chroot template oluşturur (Ubuntu 22.04)
# - DNS filtering ayarlar
# - Sosyal medya engelleme
# - Test öğrencisi oluşturur
```

## Adım 4: Flask Uygulamasını Başlat

```bash
# Uygulamayı başlat
cd /root/ders_takip
source venv/bin/activate

# Test modunda başlat
python3 app.py

# Çıktı:
# =======================================================
#   🐧 Ders Takip Sistemi başlatıldı!
# =======================================================
#   Öğrenciler için    : http://192.168.1.100:3333
#   Öğretmen paneli    : http://localhost:3333/teacher
#   Öğretmen terminal  : http://localhost:3333/teacher/terminal
#   Şifre              : linux2024
#   Docker imaj durumu : ✅ Hazır
# =======================================================
```

## Adım 5: Test Et

### Öğrenci Girişi
```
1. Tarayıcıdan: http://192.168.1.100:3333
2. Numara: 220001001
3. Ad: Ahmet
4. Soyad: Yılmaz
5. Sınıf: 101
```

### Öğretmen Paneli
```
1. Tarayıcıdan: http://192.168.1.100:3333/teacher
2. Şifre: linux2024
```

### Terminal Test
```bash
# Öğretmen: "💻 Terminal" butonuna tıkla
# Öğrenci: http://192.168.1.100:3333/terminal
# Giriş: 220001001 (session numarası ile aynı olmalı)

# SSH ile test (container IP'si)
ssh -p 2222 ogrenci1@192.168.1.100
# Şifre: ogrenci1

# İçinde root olabilir
sudo su -
```

## Adım 6: Systemd Service (Opsiyonel - Otomatik Başlatma)

```bash
# Systemd service dosyası oluştur
cat > /etc/systemd/system/ders-takip.service <<'EOF'
[Unit]
Description=Ders Takip Sistemi
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/ders_takip
Environment="PATH=/root/ders_takip/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/root/ders_takip/venv/bin/python /root/ders_takip/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Service'i etkinleştir
systemctl daemon-reload
systemctl enable ders-takip.service
systemctl start ders-takip.service

# Durum kontrol
systemctl status ders-takip.service
```

## Adım 7: Firewall (Gerekirse)

```bash
# Proxmox host'ta (container'da değil)
pct exec 100 -- apt install -y ufw

# Container içinde
ufw allow 22/tcp      # SSH
ufw allow 3333/tcp    # Flask
ufw allow 2222/tcp    # Chroot SSH
ufw enable
```

## Adım 8: Backup

### Proxmox Backup
```bash
# Container snapshot
pct snapshot 100 "ilk-kurulum"

# Manuel backup
vzdump 100 --dumpdir /var/lib/vz/dump --mode snapshot --compress zstd

# Otomatik backup (Proxmox scheduler)
# Proxmox web panel → Datacenter → Backup → Add
```

### Uygulama Backup
```bash
# Container içinde
cd /root
tar czf ders-takip-backup-$(date +%Y%m%d).tar.gz ders_takip/
```

## 🔧 Sorun Giderme

### Container Başlamıyor
```bash
# Logları kontrol et
journalctl -xe
pct status 100
pct log 100

# Container'ı yeniden başlat
pct stop 100
pct start 100
```

### Port 3333 Kullanımda
```bash
# Port'u kullanmayan process'i bul
lsof -i :3333

# Process'i öldür
kill -9 <PID>

# Veya farklı port kullan
python3 app.py --port 3334
```

### Chroot Ortamı Hatası
```bash
# Chroot dizinini kontrol et
ls -la /home/chroot/

# İzinleri düzelt
chmod +x chroot_yonetici.py
python3 chroot_yonetici.py init
```

## 📊 Kaynak Kullanımı

```bash
# Container kaynak kullanımı
pct status 100

# CPU kullanımı
pct exec 100 -- top -bn1 | head -20

# RAM kullanımı
pct exec 100 -- free -h

# Disk kullanımı
pct exec 100 -- df -h

# Chroot disk kullanımı
du -sh /home/chroot/*
```

## 🎯 Sonraki Adımlar

1. **Öğrencileri Ekle**
   ```bash
   python3 chroot_yonetici.py create ahmetyilmaz220001001
   python3 chroot_yonetici.py create ayseedemir220001002
   # ... 45 öğrenci
   ```

2. **Öğretmen Hesabı Oluştur**
   ```bash
   # Zaten mevcut (linux2024)
   ```

3. **Test Et**
   - Öğrenci girişi
   - Yoklama
   - Slayt gösterimi
   - Terminal erişimi
   - Güvenlik ihlali testi

4. **Production'a Al**
   ```bash
   # DNS ayarla
   # SSL sertifikası kur (Let's Encrypt)
   # Monitoring kur
   # Backup planı hazırla
   ```

## 📞 İletişim

Sorun yaşarsanız:
- Proxmox logları: `/var/log/pve/tasks/`
- Container logları: `journalctl -u pve-firewall`
- Uygulama logları: `/root/ders_takip/server.log`

---
**Not**: Bu doküman container IP'si olarak `192.168.1.100` kullanıyor.
Kendi IP adresinizi ayarlamayı unutmayın!
