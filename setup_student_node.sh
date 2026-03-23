#!/bin/bash
# PCT Setup Script for Student Workspace (Student Node)
# Run this on the NEW PCT (e.g., PCT 992) as root.

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🚀 PCT Öğrenci Sunucusu Kurulumu Başlatılıyor...${NC}"

# 1. Gerekli Paketleri Kur
echo -e "${YELLOW}📦 Paketler kuruluyor...${NC}"
apt-get update
apt-get install -y rsync debootstrap python3 python3-pip sudo bash vim curl wget

# 2. Çalışma Dizinlerini Oluştur
echo -e "${YELLOW}📁 Dizinler hazırlanıyor...${NC}"
mkdir -p /root/enroll
mkdir -p /home/chroot

# 3. SSH Yapılandırması (Giriş hızını ve sayısını artır)
echo -e "${YELLOW}🔒 SSH yapılandırılıyor...${NC}"
sed -i 's/#MaxStartups.*/MaxStartups 100:30:200/' /etc/ssh/sshd_config
sed -i 's/#MaxSessions.*/MaxSessions 100/' /etc/ssh/sshd_config
systemctl restart ssh

# 4. Chroot Manager'ı Hazırla
# Not: chroot_yonetici.py dosyasını PCT 990 üzerinden buraya kopyalamanız gerekecek.
# Bu script mevcut varsayıyor.

if [ -f "/root/enroll/chroot_yonetici.py" ]; then
    chmod +x /root/enroll/chroot_yonetici.py
    echo -e "${YELLOW}🎓 Chroot şablonu oluşturuluyor (Bu birkaç dakika sürebilir)...${NC}"
    python3 /root/enroll/chroot_yonetici.py init
else
    echo -e "${YELLOW}⚠️ /root/enroll/chroot_yonetici.py bulunamadı! Lütfen dosyayı kopyalayın.${NC}"
fi

echo -e "${GREEN}✨ Kurulum tamamlandı!${NC}"
echo -e "Lütfen PCT 990 (app.py) üzerindeki CT_991_HOST değerini bu sunucunun IP'si ile güncelleyin."
