#!/bin/bash
#
# Proxmox Chroot Terminal Deployment
# Kapadokya Üniversitesi Linux Laboratuvarı
#

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  Proxmox Chroot Terminal Sistemi Kurulumu                     ║"
echo "║  Her öğrenci izole chroot ortamında root olabilir              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Yapılandırma
PROJECT_DIR="/root/ders_takip"
CHROOT_BASE="/home/chroot"
SSH_PORT=2222

check_proxmox() {
    echo -e "${YELLOW}[1/7] Proxmox LXC kontrol ediliyor...${NC}"

    if [ ! -f /etc/debian_version ]; then
        echo -e "${RED}Hata: Bu bir Debian/Ubuntu tabanlı sistem değil${NC}"
        echo "Bu script sadece Proxmox LXC container içinde çalışmalı"
        exit 1
    fi

    # LXC içinde miyiz?
    if [ -d /proc/vz ]; then
        echo -e "${GREEN}✅ Proxmox LXC container tespit edildi${NC}"
    else
        echo -e "${YELLOW}⚠️  LXC container değil, fiziksel sistem VM olabilir${NC}"
        read -p "Devam etmek istiyor musunuz? (e/h): " confirm
        if [ "$confirm" != "e" ]; then
            exit 1
        fi
    fi
}

install_dependencies() {
    echo -e "${YELLOW}[2/7] Paketler kuruluyor...${NC}"

    apt-get update

    # Temel paketler
    apt-get install -y \
        debootstrap \
        openssh-server \
        python3 \
        python3-pip \
        sudo \
        openssl

    echo -e "${GREEN}✅ Paketler kuruldu${NC}"
}

setup_chroot_template() {
    echo -e "${YELLOW}[3/7] Şablon chroot ortamı kuruluyor...${NC}"
    echo "Bu işlem 5-10 dakika sürebilir..."

    mkdir -p "$CHROOT_BASE"

    # Ubuntu 22.04 chroot şablonu
    if [ ! -d "$CHROOT_BASE/template" ]; then
        debootstrap --arch=amd64 jammy "$CHROOT_BASE/template" http://archive.ubuntu.com/ubuntu/

        # DNS filtering
        cat > "$CHROOT_BASE/template/etc/resolv.conf" <<EOF
nameserver 185.228.168.168
nameserver 185.228.169.168
EOF

        # Sosyal medya engelleme (hosts)
        cat >> "$CHROOT_BASE/template/etc/hosts" <<EOF
127.0.0.1 www.facebook.com facebook.com
127.0.0.1 www.twitter.com twitter.com x.com
127.0.0.1 www.instagram.com instagram.com
127.0.0.1 www.tiktok.com tiktok.com
127.0.0.1 www.youtube.com youtube.com
127.0.0.1 www.linkedin.com linkedin.com
127.0.0.1 www.reddit.com reddit.com
127.0.0.1 www.cnn.com cnn.com
127.0.0.1 www.bbc.com bbc.com
127.0.0.1 www.nytimes.com nytimes.com
127.0.0.1 www.hurriyet.com.tr hurriyet.com.tr
127.0.0.1 www.milliyet.com.tr milliyet.com.tr
127.0.0.1 www.sozcu.com.tr sozcu.com.tr
EOF

        echo -e "${GREEN}✅ Şablon chroot hazır${NC}"
    else
        echo -e "${GREEN}✅ Şablon chroot zaten var${NC}"
    fi
}

install_flask_app() {
    echo -e "${YELLOW}[4/7] Flask uygulaması kuruluyor...${NC}"

    # Proje dizini oluştur
    mkdir -p "$PROJECT_DIR"

    # Eğer proje dosyaları yoksa, kullanıcıya söyle
    if [ ! -f "$PROJECT_DIR/app.py" ]; then
        echo -e "${YELLOW}⚠️  Proje dosyaları bulunamadı${NC}"
        echo "Proje dosyalarını buraya kopyalayın:"
        echo "  $PROJECT_DIR"
        echo ""
        read -p "Şimdi kopyalamak istiyor musunuz? (e/h): " copy_confirm

        if [ "$copy_confirm" = "e" ]; then
            echo "Proje dosyalarını şu anda kopyalayın..."
            echo "Enter'a basınca devam edeceğim"
            read
        fi
    fi

    cd "$PROJECT_DIR"
    
    # Virtual Environment (venv) oluştur
    echo "Virtual environment oluşturuluyor..."
    apt-get install -y python3-venv
    python3 -m venv venv
    
    # Python paketlerini venv içine kur
    ./venv/bin/pip install flask flask-socketio eventlet requests

    echo -e "${GREEN}✅ Flask uygulaması ve venv hazır${NC}"
}

setup_ssh_config() {
    echo -e "${YELLOW}[5/7] SSH yapılandırması...${NC}"

    # SSH portunu değiştir (ana sistemle çakışmasın)
    sed -i "s/#Port 22/Port $SSH_PORT/" /etc/ssh/sshd_config

    # Chroot login script'ini kopyala
    cp chroot_login.sh /usr/local/bin/chroot-login
    chmod +x /usr/local/bin/chroot-login

    # SSH config'e chroot support ekle
    cat >> /etc/ssh/sshd_config <<EOF

# Chroot terminal için
Match Group ogrenciler
    ForceCommand /usr/local/bin/chroot-login %u
    PermitRootLogin no
    X11Forwarding no
    AllowTcpForwarding no
EOF

    # Öğrenci grubu
    groupadd -f ogrenciler

    systemctl restart sshd

    echo -e "${GREEN}✅ SSH yapılandırması tamam${NC}"
}

create_test_student() {
    echo -e "${YELLOW}[6/7] Test öğrencisi oluşturuluyor...${NC}"

    python3 "$PROJECT_DIR/chroot_yonetici.py" create ogrenci1 || {
        echo -e "${RED}Hata: Test öğrencisi oluşturulamadı${NC}"
        return 1
    }

    echo -e "${GREEN}✅ Test öğrencisi oluşturuldu${NC}"
}

print_info() {
    echo -e "${YELLOW}[7/7] Kurulum tamamlandı!${NC}"
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  Bilgiler                                                      ║"
    echo "╠═══════════════════════════════════════════════════════════════╣"
    echo "║  Chroot Dizini  : $CHROOT_BASE"
    echo "║  SSH Portu      : $SSH_PORT"
    echo "║  Test Kullanıcı : ogrenci1 / ogrenci1"
    echo "║                                                                  ║"
    echo "║  Yeni öğrenci eklemek için:                                    ║"
    echo "║  python3 $PROJECT_DIR/chroot_yonetici.py create <kullanici>   ║"
    echo "║                                                                  ║"
    echo "║  SSH ile bağlanmak:                                            ║"
    echo "║  ssh -p $SSH_PORT ogrenci1@<container_ip>                     ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
}

# Ana akış
main() {
    check_proxmox
    install_dependencies
    setup_chroot_template
    install_flask_app
    setup_ssh_config
    create_test_student
    print_info

    echo -e "${GREEN}✅ Kurulum tamamlandı!${NC}"
    echo ""
    echo "Flask uygulamasını başlatmak için:"
    echo "  cd $PROJECT_DIR"
    echo "  python3 app.py"
}

main
