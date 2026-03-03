#!/bin/bash
#
# CT 991 (ogrenci-vm) Chroot Deployment
#

CT_ID=991
PROJECT_DIR="/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  CT 991 (ogrenci-vm) Chroot Deployment                       ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Container durumunu kontrol et
echo "[1/7] Container durumu kontrol ediliyor..."
pct status $CT_ID | grep -q "status: running"
if [ $? -ne 0 ]; then
    echo "❌ Container çalışmıyor! Başlatılıyor..."
    pct start $CT_ID
    sleep 5
fi
echo "✅ Container çalışıyor"

# 2. Temel paketleri kur (debootstrap + SSH)
echo ""
echo "[2/7] Chroot için gerekli paketler kuruluyor..."
pct exec $CT_ID -- bash -c "
    apt update
    apt install -y debootstrap openssh-server python3 openssl sudo

    # Chroot base dizini oluştur
    mkdir -p /home/chroot
"
echo "✅ Paketler kuruldu"

# 3. Proje dosyalarını kopyala (chroot yönetim script'leri)
echo ""
echo "[3/7] Proje dosyaları kopyalanıyor..."
pct push $CT_ID $PROJECT_DIR /root/ders-takip
pct exec $CT_ID -- bash -c "
    chmod +x /root/ders-takip/chroot_yonetici.py
    chmod +x /root/ders-takip/chroot_login.sh
"
echo "✅ Dosyalar kopyalandı"

# 4. Chroot template oluştur (Ubuntu 22.04)
echo ""
echo "[4/7] Chroot template oluşturuluyor..."
echo "Bu işlem 5-10 dakika sürebilir..."
pct exec $CT_ID -- bash -c "
    cd /root/ders-takip
    python3 chroot_yonetici.py init
"
echo "✅ Template hazır"

# 5. SSH yapılandırması
echo ""
echo "[5/7] SSH yapılandırılıyor..."
pct exec $CT_ID -- bash -c "
    # SSH portunu değiştir (ana sistemle çakışmasın)
    sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

    # Chroot login script'ini kopyala
    cp /root/ders-takip/chroot_login.sh /usr/local/bin/chroot-login
    chmod +x /usr/local/bin/chroot-login

    # Öğrenci grubu oluştur
    groupadd -f ogrenciler

    # SSH config'e chroot support ekle
    cat >> /etc/ssh/sshd_config <<'EOF'

# Chroot terminal için
Match Group ogrenciler
    ForceCommand /usr/local/bin/chroot-login %u
    PermitRootLogin no
    X11Forwarding no
    AllowTcpForwarding no
EOF

    # SSH'yi restart et
    systemctl restart sshd
"
echo "✅ SSH hazır"

# 6. Test öğrencisi oluştur
echo ""
echo "[6/7] Test öğrencisi oluşturuluyor..."
pct exec $CT_ID -- bash -c "
    cd /root/ders-takip
    python3 chroot_yonetici.py create ogrenci1
"
echo "✅ Test öğrencisi oluşturuldu"

# 7. Network ve IP bilgileri
echo ""
echo "[7/7] Network konfigürasyonu..."
echo "Container IP bilgileri:"
pct exec $CT_ID -- bash -c "
    echo \"  IP: \$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1)\"
    echo \"  SSH Port: 2222\"
    echo \"\"
    echo \"Test bağlantısı:\"
    echo \"  ssh -p 2222 ogrenci1@\$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1)\"
    echo \"  Şifre: ogrenci1\"
"
echo "✅ Network hazır"

# Bilgileri göster
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ CT 991 Deployment Tamamlandı!                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Bilgiler:"
pct exec $CT_ID -- bash -c "
    echo \"  Container: $CT_ID\"
    echo \"  Hostname: \$(hostname)\"
    echo \"  IP: \$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1)\"
    echo \"  SSH Port: 2222\"
    echo \"  Chroot Base: /home/chroot\"
    echo \"\"
    echo \"Öğrenci eklemek için:\"
    echo \"  pct exec $CT_ID -- python3 /root/ders-takip/chroot_yonetici.py create <numara>\"
    echo \"\"
    echo \"Tüm öğrencileri listelemek için:\"
    echo \"  pct exec $CT_ID -- python3 /root/ders-takip/chroot_yonetici.py list\"
"
echo ""
echo "Test:"
pct exec $CT_ID -- bash -c "
    if command -v ogrenci1 &> /dev/null; then
        echo \"  ✅ Test öğrencisi var\"
        echo \"  SSH: ssh -p 2222 ogrenci1@\$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1)\"
    else
        echo \"  ⚠️  Test öğrencisi oluşturulamadı\"
    fi
"
echo ""
