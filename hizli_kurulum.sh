#!/bin/bash
#
# Hızlı Proxmox Deploy Script
# Kapadokya Üniversitesi - BGY106
#

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  Proxmox LXC Container Hızlı Kurulum Sihirbazı               ║"
echo "║  Ders Takip Sistemi - Chroot Terminal                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Varsayılan değerler
CT_ID=${CT_ID:-100}
HOSTNAME="ders-takip"
MEMORY=${MEMORY:-16384}  # 16 GB
CORES=${CORES:-8}
STORAGE=${STORAGE:-local-lvm}
DISK_SIZE=${DISK_SIZE:-50}
BRIDGE=${BRIDGE:-vmbr0}
IP=${IP:-192.168.1.100/24}
GATEWAY=${GATEWAY:-192.168.1.1}

echo -e "${BLUE}[1/6] Proxmox LXC Container Oluşturma${NC}"
echo "├─ CT ID: $CT_ID"
echo "├─ Hostname: $HOSTNAME"
echo "├─ Memory: ${MEMORY} MB"
echo "├─ CPU Cores: $CORES"
echo "├─ Disk: ${DISK_SIZE} GB ($STORAGE)"
echo "├─ Bridge: $BRIDGE"
echo "├─ IP: $IP"
echo "└─ Gateway: $GATEWAY"
echo ""

read -p "Devam etmek istiyor musunuz? (e/h): " confirm
if [ "$confirm" != "e" ]; then
    echo -e "${RED}İptal edildi${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[2/6] Container Oluşturuluyor...${NC}"

# Debian 11 template kontrolü
if ! pveam list local | grep -q "debian-11"; then
    echo "Debian 11 template indiriliyor..."
    pveam update
    pveam download local debian-11-standard_11.3-1_amd64.tar.zst
fi

# Container oluştur
echo "LXC container oluşturuluyor..."
pct create $CT_ID local:vztmpl/debian-11-standard_11.3-1_amd64.tar.zst \
  --storage $STORAGE \
  --cores $CORES \
  --memory $MEMORY \
  --swap 2048 \
  --net0 name=eth0,bridge=$BRIDGE,ip=$IP,gw=$GATEWAY \
  --hostname $HOSTNAME \
  --rootfs ${STORAGE}:${DISK_SIZE} \
  --onboot 1 \
  --unprivileged 0 \
  --features nesting=1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Container oluşturuldu${NC}"
else
    echo -e "${RED}❌ Container oluşturulamadı${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[3/6] Container Başlatılıyor...${NC}"

# Container'ı başlat
pct start $CT_ID

# Başlatılmasını bekle
echo "Container başlatılıyor..."
sleep 5

# Container çalışıyor mu?
if pct status $CT_ID | grep -q "status: running"; then
    echo -e "${GREEN}✅ Container çalışıyor${NC}"
else
    echo -e "${RED}❌ Container başlatılamadı${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[4/6] İçeriden Kurulum Script'i İndiriliyor...${NC}"

# Container'a proje dosyalarını kopyala
echo "Proje dosyaları kopyalanıyor..."

# Proje dizinini al
PROJECT_DIR="/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip"

if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Proje dizini bulunamadı: $PROJECT_DIR${NC}"
    exit 1
fi

# Container'a kopyala
pct push $CT_ID $PROJECT_DIR /root/ders-takip

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dosyalar kopyalandı${NC}"
else
    echo -e "${YELLOW}⚠️  Dosyalar kopyalanamadı, manuel kopyalayın${NC}"
    echo "scp -r $PROJECT_DIR root@<proxmox-ip>:/root/ders-takip/"
fi

echo ""
echo -e "${BLUE}[5/6] İçeriden Hazırlık Script'i Çalıştırılıyor...${NC}"

# Container içinde hazırlık
pct exec $CT_ID -- bash -c "
    apt update && apt upgrade -y
    apt install -y git python3 python3-pip python3-venv debootstrap openssh-server sudo openssl curl wget
    cd /root/ders-takip
    chmod +x proxmox-chroot-deploy.sh chroot_login.sh chroot_yonetici.py
    python3 -m venv venv
    source venv/bin/activate
    pip install flask flask-socketio eventlet
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Hazırlık tamamlandı${NC}"
else
    echo -e "${RED}❌ Hazırlık başarısız${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[6/6] Chroot Deploy Script'i Çalıştırılıyor...${NC}"
echo "Bu işlem 5-10 dakika sürebilir..."
echo ""

# Deploy script'ini çalıştır
pct exec $CT_ID -- bash -c "
    cd /root/ders-takip
    ./proxmox-chroot-deploy.sh
"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ KURULUM TAMAMLANDI!                                          ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Bilgiler:"
echo "  Container ID: $CT_ID"
echo "  IP Adresi: ${IP%/*}"
echo "  Öğrenciler: http://${IP%/*}:3333"
echo "  Öğretmen: http://${IP%/*}:3333/teacher"
echo "  Şifre: linux2024"
echo ""
echo "Sonraki adımlar:"
echo "  1. Container'a gir: pct enter $CT_ID"
echo "  2. Uygulamayı başlat: cd /root/ders-takip && python3 app.py"
echo "  3. Tarayıcıdan test et"
echo ""
echo "Öğrenci eklemek için:"
echo "  pct exec $CT_ID -- python3 /root/ders-takip/chroot_yonetici.py create <numara>"
echo ""
