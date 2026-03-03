#!/bin/bash
#
# Python Environment Kurulum Script'i
# CT 990 ve CT 991 için
#

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  Python Environment Kurulumu                                 ║"
echo "║  CT 990: Flask App (venv + pip)                             ║"
echo "║  CT 991: Chroot Yönetimi (sistem python)                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# CT 990 - Flask App Container
echo "═══════════════════════════════════════════════════════════════"
echo "  1/2 CT 990 (ders-takip) - Flask App Python Kurulumu"
echo "═══════════════════════════════════════════════════════════════"
echo ""

pct exec 990 -- bash -c "
echo 'Python 3 kontrol...'
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=\$(python3 --version)
    echo \"✅ Python 3 mevcut: \$PYTHON_VERSION\"
else
    echo '❌ Python 3 yok, kuruluyor...'
    apt update
    apt install -y python3 python3-pip python3-venv python3-dev
fi

echo ''
echo 'Virtual environment kontrol...'
if [ -f /root/ders-takip/venv/bin/activate ]; then
    echo '✅ Virtual environment mevcut'
else
    echo 'Virtual environment oluşturuluyor...'
    cd /root/ders-takip
    python3 -m venv venv
    echo '✅ Virtual environment oluşturuldu'
fi

echo ''
echo 'Pip paketleri kontrol...'
source /root/ders-takip/venv/bin/activate
pip list | grep -q 'Flask'
if [ \$? -eq 0 ]; then
    echo '✅ Flask paketleri mevcut'
else
    echo 'Pip paketleri kuruluyor...'
    pip install --upgrade pip
    pip install flask flask-socketio eventlet
    echo '✅ Pip paketleri kuruldu'
fi

echo ''
echo 'Son durum:'
echo \"  Python: \$(python3 --version)\"
    echo \"  Pip: \$(pip --version)\"
    echo \"  Flask: \$(pip show Flask | grep Version)\"
    echo \"  SocketIO: \$(pip show flask-socketio | grep Version)\"
"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  2/2 CT 991 (ogrenci-vm) - Chroot Python Kurulumu"
echo "═══════════════════════════════════════════════════════════════"
echo ""

pct exec 991 -- bash -c "
echo 'Python 3 kontrol...'
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=\$(python3 --version)
    echo \"✅ Python 3 mevcut: \$PYTHON_VERSION\"
else
    echo '❌ Python 3 yok, kuruluyor...'
    apt update
    apt install -y python3 python3-pip
fi

echo ''
echo 'Chroot yönetim script\'i kontrol...'
if [ -f /root/ders-takip/chroot_yonetici.py ]; then
    echo '✅ Chroot yönetim script\'i mevcut'
    chmod +x /root/ders-takip/chroot_yonetici.py
else
    echo '❌ Chroot yönetim script\'i yok!'
    echo 'Proje dosyalarını kopyalamanız gerekir.'
fi

echo ''
echo 'Son durum:'
echo \"  Python: \$(python3 --version)\"
    echo \"  Pip: \$(pip --version 2>/dev/null || echo 'yok')\"
    echo \"  Chroot script: \$(ls -la /root/ders-takip/chroot_yonetici.py 2>/dev/null || echo 'yok')\"
"

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ Python Environment Kurulumu Tamamlandı                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
