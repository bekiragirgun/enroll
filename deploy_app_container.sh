#!/bin/bash
#
# CT 990 (ders-takip) Flask App Deployment
#

CT_ID=990
PROJECT_DIR="/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  CT 990 (ders-takip) Flask App Deployment                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Container durumunu kontrol et
echo "[1/6] Container durumu kontrol ediliyor..."
pct status $CT_ID | grep -q "status: running"
if [ $? -ne 0 ]; then
    echo "❌ Container çalışmıyor! Başlatılıyor..."
    pct start $CT_ID
    sleep 5
fi
echo "✅ Container çalışıyor"

# 2. Temel paketleri kur
echo ""
echo "[2/6] Paketler kuruluyor..."
pct exec $CT_ID -- bash -c "
    apt update
    apt install -y python3 python3-pip python3-venv \
                   python3-dev build-essential \
                   git curl wget \
                   sqlite3 \
                   libffi-dev libssl-dev
"
echo "✅ Paketler kuruldu"

# 3. Proje dosyalarını kopyala
echo ""
echo "[3/6] Proje dosyaları kopyalanıyor..."
pct push $CT_ID $PROJECT_DIR /root/ders-takip
echo "✅ Dosyalar kopyalandı"

# 4. Python sanal ortam oluştur
echo ""
echo "[4/6] Python virtual environment oluşturuluyor..."
pct exec $CT_ID -- bash -c "
    cd /root/ders-takip
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install flask flask-socketio eventlet
"
echo "✅ Virtual environment hazır"

# 5. Veritabanını başlat
echo ""
echo "[5/6] Veritabanı başlatılıyor..."
pct exec $CT_ID -- bash -c "
    cd /root/ders-takip
    source venv/bin/activate
    python3 -c 'from app import app, db_baglanti, init_db; init_db()'
"
echo "✅ Veritabanı hazır"

# 6. Systemd service oluştur
echo ""
echo "[6/6] Systemd service oluşturuluyor..."
pct exec $CT_ID -- bash -c "
cat > /etc/systemd/system/ders-takip.service <<'EEOF'
[Unit]
Description=Ders Takip Sistemi - Flask App
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/ders-takip
Environment=\"PATH=/root/ders-takip/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"
ExecStart=/root/ders-takip/venv/bin/python /root/ders-takip/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EEOF

systemctl daemon-reload
systemctl enable ders-takip.service
systemctl start ders-takip.service
"
echo "✅ Service oluşturuldu"

# Bilgileri göster
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ CT 990 Deployment Tamamlandı!                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Bilgiler:"
pct exec $CT_ID -- bash -c "
    echo \"  Container: $CT_ID\"
    echo \"  Hostname: \$(hostname)\"
    echo \"  IP: \$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1)\"
    echo \"  Port: 3333\"
    echo \"  Durum: \$(systemctl is-active ders-takip.service)\"
    echo \"\"
    echo \"Erişim:\"
    echo \"  Öğrenciler: http://\$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1):3333\"
    echo \"  Öğretmen: http://\$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1):3333/teacher\"
    echo \"  Şifre: linux2024\"
"
echo ""
echo "Logları görüntülemek için:"
echo "  pct exec $CT_ID -- journalctl -u ders-takip -f"
echo ""
