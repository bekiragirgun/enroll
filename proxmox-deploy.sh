#!/bin/bash
#############################################
# Proxmox CT Deployment Script
# Kapadokya Ders Takip Sistemi
# Versiyon: 2.0
#############################################

set -e

# Renkli çıktı
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logo
print_logo() {
    echo -e "${BLUE}"
    cat << "EOF"
╔═════════════════════════════════════════╗
║   Proxmox CT Deployment Script v2.0    ║
║   Kapadokya Ders Takip Sistemi         ║
╚═════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Yardım mesajı
show_help() {
    cat << EOF

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

ÇEVRE DEĞİŞKENLERİ:
    PROXMOX_HOST           Proxmox host adresi (varsayılan: localhost)
    PROXMOX_USER           Proxmox kullanıcı adı (varsayılan: root@pam)
    PROXMOX_PASS           Proxmox şifresi
    PM_API_URL             Tam API URL (diğerleri geçersiz kılar)

EOF
}

# Log fonksiyonları
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Varsayılan konfigürasyon
DEFAULT_CTID_WEB=9001
DEFAULT_CTID_TERM=9002
DEFAULT_HOSTNAME_WEB="ders-takip-web"
DEFAULT_HOSTNAME_TERM="linux-egitim"
DEFAULT_MEMORY=2048
DEFAULT_CORES=2
DEFAULT_DISK=20
DEFAULT_STORAGE="local-lvm"
DEFAULT_BRIDGE="vmbr0"
DEFAULT_TEMPLATE="debian-12-standard_12.2-1_amd64.tar.zst"
DEFAULT_TEMPLATE_URL="https://download.proxmox.com/images/system/debian-12-standard_12.2-1_amd64.tar.zst"

# Konfigürasyon değişkenleri
CTID_WEB=$DEFAULT_CTID_WEB
CTID_TERM=$DEFAULT_CTID_TERM
HOSTNAME_WEB=$DEFAULT_HOSTNAME_WEB
HOSTNAME_TERM=$DEFAULT_HOSTNAME_TERM
MEMORY=$DEFAULT_MEMORY
CORES=$DEFAULT_CORES
DISK_SIZE=$DEFAULT_DISK
STORAGE=$DEFAULT_STORAGE
BRIDGE=$DEFAULT_BRIDGE
TEMPLATE=$DEFAULT_TEMPLATE
TEMPLATE_URL=$DEFAULT_TEMPLATE_URL

# Çalışma modu
MODE="both"
DRY_RUN=false
SKIP_TEMPLATE=false

# Parametreleri işle
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -w|--web-only)
            MODE="web"
            shift
            ;;
        -t|--term-only)
            MODE="term"
            shift
            ;;
        -b|--both)
            MODE="both"
            shift
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            if [[ -f "$CONFIG_FILE" ]]; then
                source "$CONFIG_FILE"
                log_info "Konfigürasyon dosyası yüklendi: $CONFIG_FILE"
            else
                log_error "Konfigürasyon dosyası bulunamadı: $CONFIG_FILE"
                exit 1
            fi
            shift 2
            ;;
        -s|--skip-template)
            SKIP_TEMPLATE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            log_error "Bilinmeyen seçenek: $1"
            show_help
            exit 1
            ;;
    esac
done

# Proxmox kontrolü
check_proxmox() {
    log_info "Proxmox bağlantısı kontrol ediliyor..."

    if ! command -v pct &> /dev/null; then
        log_error "pct komutu bulunamadı. Bu script Proxmox host üzerinde çalışmalı."
        exit 1
    fi

    if [[ $DRY_RUN == false ]]; then
        if ! pct status &> /dev/null; then
            log_error "Proxmox'e erişilemedi. Lütfen Proxmox host üzerinde çalıştırdığınızdan emin olun."
            exit 1
        fi
    fi

    log_success "Proxmox bağlantısı OK"
}

# CT kontrolü
check_ct_exists() {
    local ctid=$1
    if pct status $ctid &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Template kontrolü ve indirme
download_template() {
    if [[ $SKIP_TEMPLATE == true ]]; then
        log_warning "Template indirme atlandı"
        return
    fi

    log_info "Template kontrol ediliyor: $TEMPLATE"

    local template_path="/var/lib/vz/template/cache/$TEMPLATE"

    if [[ -f "$template_path" ]]; then
        log_success "Template zaten mevcut"
        return
    fi

    log_info "Template indiriliyor..."
    log_info "URL: $TEMPLATE_URL"

    if [[ $DRY_RUN == true ]]; then
        log_warning "[DRY-RUN] Template indirilecek: $TEMPLATE_URL"
        return
    fi

    # Template dizinini kontrol et
    if [[ ! -d "/var/lib/vz/template/cache" ]]; then
        log_info "Template dizini oluşturuluyor..."
        mkdir -p /var/lib/vz/template/cache
    fi

    # Template indir
    if command -v wget &> /dev/null; then
        wget -O "$template_path" "$TEMPLATE_URL" --show-progress
    elif command -v curl &> /dev/null; then
        curl -o "$template_path" "$TEMPLATE_URL" --progress-bar
    else
        log_error "wget veya curl bulunamadı"
        exit 1
    fi

    log_success "Template indirildi: $template_path"
}

# CT oluştur
create_ct() {
    local ctid=$1
    local hostname=$2
    local description=$3

    log_info "CT oluşturuluyor: $hostname (ID: $ctid)"

    # CT zaten var mı?
    if check_ct_exists $ctid; then
        log_warning "CT $ctid zaten mevcut, atlanıyor"
        return
    fi

    if [[ $DRY_RUN == true ]]; then
        log_warning "[DRY-RUN] CT oluşturulacak: $hostname (ID: $ctid)"
        log_warning "[DRY-RUN]   Memory: ${MEMORY}MB, Cores: $CORES, Disk: ${DISK_SIZE}GB"
        return
    fi

    # CT oluştur
    pct create $ctid \
        ${STORAGE}:vztmpl/${TEMPLATE} \
        --hostname $hostname \
        --memory $MEMORY \
        --cores $CORES \
        --rootfs ${STORAGE}:${DISK_SIZE} \
        --net0 name=eth0,bridge=${BRIDGE},ip=dhcp \
        --features nesting=1,keyctl=1 \
        --onboot 1 \
        --description "$description" \
        --unprivileged 0

    log_success "CT oluşturuldu: $hostname"
}

# CT başlat
start_ct() {
    local ctid=$1
    local hostname=$2

    log_info "CT başlatılıyor: $hostname"

    if [[ $DRY_RUN == true ]]; then
        log_warning "[DRY-RUN] CT başlatılacak: $hostname"
        return
    fi

    pct start $ctid

    # CT'nin başlamasını bekle
    log_info "CT'nin başlaması bekleniyor..."
    local max_wait=30
    local waited=0
    while [ $waited -lt $max_wait ]; do
        if pct status $ctid | grep -q "running"; then
            log_success "CT başlatıldı: $hostname"
            return
        fi
        sleep 1
        waited=$((waited + 1))
    done

    log_error "CT başlatılamadı: $hostname"
    exit 1
}

# Sistem güncelleme
update_system() {
    local ctid=$1
    local hostname=$2

    log_info "Sistem güncelleniyor: $hostname"

    if [[ $DRY_RUN == true ]]; then
        log_warning "[DRY-RUN] Sistem güncellenecek: $hostname"
        return
    fi

    pct exec $ctid -- bash -c "apt-get update && apt-get upgrade -y"

    log_success "Sistem güncellendi: $hostname"
}

# Paket kur
install_packages() {
    local ctid=$1
    local hostname=$2
    shift 2
    local packages="$@"

    log_info "Paketler yükleniyor: $hostname"

    if [[ $DRY_RUN == true ]]; then
        log_warning "[DRY-RUN] Paketler yüklenecek: $packages"
        return
    fi

    pct exec $ctid -- bash -c "apt-get install -y $packages"

    log_success "Paketler yüklendi: $hostname"
}

# Web container kurulumu
setup_web_ct() {
    log_info "=========================================="
    log_info "Web Container Kurulumu Başlıyor"
    log_info "=========================================="

    create_ct $CTID_WEB $HOSTNAME_WEB "Kapadokya Ders Takip Sistemi - Web"
    start_ct $CTID_WEB $HOSTNAME_WEB
    update_system $CTID_WEB $HOSTNAME_WEB

    # Python ve araçlar
    log_info "Python ve araçlar yükleniyor..."
    install_packages $CTID_WEB $HOSTNAME_WEB "python3 python3-pip python3-venv git vim curl wget sqlite3 nginx"

    # Proje dosyalarını kopyala
    log_info "Proje dosyaları kopyalanıyor..."
    if [[ $DRY_RUN == false ]]; then
        # Scriptin çalıştığı dizini bul
        SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

        # CT içine proje dizinini oluştur
        pct exec $CTID_WEB -- bash -c "mkdir -p /root/ders_takip"

        # Dosyaları kopyala (pct push kullanımı)
        log_info "Dosyalar kopyalanıyor (bu biraz zaman alabilir)..."
        rsync -av --exclude='venv' --exclude='__pycache__' --exclude='.git' \
            --exclude='data' --exclude='boxes' --exclude='.vagrant' \
            "$SCRIPT_DIR/" "root@${HOSTNAME_WEB}:/root/ders_takip/" 2>/dev/null || \
            pct push $CTID_WEB "$SCRIPT_DIR" /tmp/ders_takip-upload
    fi

    # Python ortamı kur
    log_info "Python sanal ortam kuruluyor..."
    if [[ $DRY_RUN == false ]]; then
        pct exec $CTID_WEB -- bash -c "cd /root/ders_takip && python3 -m venv venv"
        pct exec $CTID_WEB -- bash -c "cd /root/ders_takip && source venv/bin/activate && pip install --upgrade pip"
        pct exec $CTID_WEB -- bash -c "cd /root/ders_takip && source venv/bin/activate && pip install -r requirements.txt"
    fi

    # Systemd servisi oluştur
    log_info "Systemd servisi oluşturuluyor..."
    if [[ $DRY_RUN == false ]]; then
        pct exec $CTID_WEB -- bash -c "cat > /etc/systemd/system/ders-takip.service << 'EOFSERVICE'
[Unit]
Description=Ders Takip Sistemi
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/ders_takip
Environment=\"PATH=/root/ders_takip/venv/bin\"
ExecStart=/root/ders_takip/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOFSERVICE
"

        # Servisi aktifleştir
        pct exec $CTID_WEB -- bash -c "systemctl daemon-reload && systemctl enable ders-takip.service && systemctl start ders-takip.service"
    fi

    # Nginx reverse proxy
    log_info "Nginx yapılandırılıyor..."
    if [[ $DRY_RUN == false ]]; then
        pct exec $CTID_WEB -- bash -c "cat > /etc/nginx/sites-available/ders-takip << 'EOFNGINX'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOFNGINX
"

        pct exec $CTID_WEB -- bash -c "ln -sf /etc/nginx/sites-available/ders-takip /etc/nginx/sites-enabled/"
        pct exec $CTID_WEB -- bash -c "rm -f /etc/nginx/sites-enabled/default"
        pct exec $CTID_WEB -- bash -c "nginx -t && systemctl restart nginx"
    fi

    log_success "Web container kurulumu tamamlandı!"
}

# Terminal container kurulumu
setup_term_ct() {
    log_info "=========================================="
    log_info "Terminal Container Kurulumu Başlıyor"
    log_info "=========================================="

    create_ct $CTID_TERM $HOSTNAME_TERM "Kapadokya Linux Eğitim Ortamı"
    start_ct $CTID_TERM $HOSTNAME_TERM
    update_system $CTID_TERM $HOSTNAME_TERM

    # Linux eğitim araçları
    log_info "Linux eğitim araçları yükleniyor..."
    install_packages $CTID_TERM $HOSTNAME_TERM "build-essential man-db man-pages vim nano tmux htop iotop net-tools iproute2 iputils-ping traceroute nmap telnet curl wget git tree jq sudo ufw fail2ban"

    # Öğrenci kullanıcısı oluştur
    log_info "Öğrenci kullanıcısı oluşturuluyor..."
    if [[ $DRY_RUN == false ]]; then
        pct exec $CTID_TERM -- bash -c "useradd -m -s /bin/bash -p \$(openssl passwd -1 ogrenci) ogrenci"
        pct exec $CTID_TERM -- bash -c "usermod -aG sudo ogrenci"
    fi

    # Eğitim dizinleri oluştur
    log_info "Eğitim dizinleri oluşturuluyor..."
    if [[ $DRY_RUN == false ]]; then
        pct exec $CTID_TERM -- bash -c "mkdir -p /home/ogrenci/{egitim,pratik,testler,loglar}"
        pct exec $CTID_TERM -- bash -c "chown -R ogrenci:ogrenci /home/ogrenci/*"
    fi

    # TTYD kurulumu (web terminal)
    log_info "TTYD (web terminal) yükleniyor..."
    if [[ $DRY_RUN == false ]]; then
        pct exec $CTID_TERM -- bash -c "apt-get install -y build-essential cmake git libwebsockets-dev"
        pct exec $CTID_TERM -- bash -c "cd /tmp && git clone https://github.com/tsl0922/ttyd.git && cd ttyd && mkdir build && cd build && cmake .. && make && make install"
    fi

    # TTYD servisi
    log_info "TTYD servisi yapılandırılıyor..."
    if [[ $DRY_RUN == false ]]; then
        pct exec $CTID_TERM -- bash -c "cat > /etc/systemd/system/ttyd.service << 'EOFSERVICE'
[Unit]
Description=TTYD Web Terminal
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/ttyd -p 7681 bash
Restart=always

[Install]
WantedBy=multi-user.target
EOFSERVICE
"

        pct exec $CTID_TERM -- bash -c "systemctl daemon-reload && systemctl enable ttyd.service && systemctl start ttyd.service"
    fi

    log_success "Terminal container kurulumu tamamlandı!"
}

# Özet bilgiler göster
show_summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     Kurulum Başarıyla Tamamlandı!        ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}📦 Container Bilgileri:${NC}"
    echo ""

    if [[ $MODE == "web" || $MODE == "both" ]]; then
        echo -e "  ${GREEN}✓${NC} Web Container"
        echo -e "     CT ID: ${YELLOW}$CTID_WEB${NC}"
        echo -e "     Hostname: ${YELLOW}$HOSTNAME_WEB${NC}"
        if [[ $DRY_RUN == false ]]; then
            local ip=$(pct exec $CTID_WEB -- hostname -I 2>/dev/null | awk '{print $1}')
            echo -e "     IP: ${YELLOW}$ip${NC}"
        fi
        echo ""
    fi

    if [[ $MODE == "term" || $MODE == "both" ]]; then
        echo -e "  ${GREEN}✓${NC} Terminal Container"
        echo -e "     CT ID: ${YELLOW}$CTID_TERM${NC}"
        echo -e "     Hostname: ${YELLOW}$HOSTNAME_TERM${NC}"
        if [[ $DRY_RUN == false ]]; then
            local ip=$(pct exec $CTID_TERM -- hostname -I 2>/dev/null | awk '{print $1}')
            echo -e "     IP: ${YELLOW}$ip${NC}"
        fi
        echo ""
    fi

    echo -e "${BLUE}🌐 Erişim Bilgileri:${NC}"
    echo ""
    echo -e "  Web Paneli: ${YELLOW}http://<WEB_IP>${NC}"
    echo -e "  Öğretmen:   ${YELLOW}http://<WEB_IP>/teacher${NC}"
    echo -e "             Şifre: ${YELLOW}linux2024${NC}"
    echo ""
    echo -e "  Web Terminal: ${YELLOW}http://<TERM_IP>:7681${NC}"
    echo ""
    echo -e "  SSH Erişimi:"
    echo -e "     ${YELLOW}ssh root@<TERM_IP>${NC}"
    echo -e "     ${YELLOW}ssh ogrenci@<TERM_IP>${NC} (Şifre: ogrenci)"
    echo ""
    echo -e "${BLUE}🔧 Yönetim Komutları:${NC}"
    echo ""
    echo -e "  CT listesi:     ${YELLOW}pct list${NC}"
    echo -e "  Console:        ${YELLOW}pct enter <CT_ID>${NC}"
    echo -e "  Başlat/Durdur:  ${YELLOW}pct start/stop <CT_ID>${NC}"
    echo -e "  Log görüntüle: ${YELLOW}pct exec <CT_ID> -- journalctl -u ders-takip${NC}"
    echo ""

    if [[ $DRY_RUN == true ]]; then
        echo -e "${YELLOW}[!] DRY-RUN modu: Gerçek bir işlem yapılmadı${NC}"
        echo ""
    fi
}

# Ana akış
main() {
    print_logo

    if [[ $DRY_RUN == true ]]; then
        log_warning "DRY-RUN modu aktif - Gerçek işlem yapılmayacak"
    fi

    check_proxmox
    download_template

    if [[ $MODE == "web" || $MODE == "both" ]]; then
        setup_web_ct
    fi

    if [[ $MODE == "term" || $MODE == "both" ]]; then
        setup_term_ct
    fi

    show_summary
}

# Scripti çalıştır
main "$@"
