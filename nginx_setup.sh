#!/bin/bash

# Nginx Kurulum ve Yapılandırma Betiği (PCT 990 için)
# Bu betik root yetkisi ile çalıştırılmalıdır.

set -e

# Renkler
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Nginx kurulumu ve yapılandırması başlatılıyor...${NC}"

# 1. Nginx Kurulumu
if ! command -v nginx >/dev/null 2>&1; then
    echo -e "${YELLOW}📦 Nginx kuruluyor...${NC}"
    apt-get update
    apt-get install -y nginx
else
    echo -e "${GREEN}✅ Nginx zaten kurulu.${NC}"
fi

# 2. Yapılandırma Dosyası Oluşturma
DOMAIN="enroll.bekiragi.org"
CONF_FILE="/etc/nginx/sites-available/enroll"

echo -e "${YELLOW}📝 Nginx yapılandırması oluşturuluyor: $CONF_FILE${NC}"

cat > "$CONF_FILE" <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    # Tipik Flask Uygulaması
    location / {
        proxy_pass http://127.0.0.1:3333;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # TTYD Terminal Yayını
    location /terminal-yayin {
        # Trailing slash redirect
        rewrite ^/terminal-yayin$ /terminal-yayin/ permanent;
    }

    location /terminal-yayin/ {
        proxy_pass http://127.0.0.1:7681/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket için gerekli timeout'lar
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
        
        # Buffer kapatma (terminal hızı için)
        proxy_buffering off;
    }
}
EOF

# 3. Dosyayı aktifleştir
echo -e "${YELLOW}🔗 Yapılandırma aktifleştiriliyor...${NC}"
ln -sf "$CONF_FILE" /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 4. Nginx Test ve Restart
echo -e "${YELLOW}🔄 Nginx test ediliyor ve yeniden başlatılıyor...${NC}"
nginx -t
systemctl restart nginx

echo -e "${GREEN}✨ Nginx başarıyla yapılandırıldı!${NC}"
echo -e "Şu an şuradan erişebilirsiniz: http://$DOMAIN"
echo -e "Terminal yayını: http://$DOMAIN/terminal-yayin/"
