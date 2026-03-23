#!/bin/bash
#
# Master Deployment Script - CT 990 + CT 991
#

PROJECT_DIR="/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  Ders Takip Sistemi - Tam Deployment                          ║"
echo "║  CT 990: Flask App                                          ║"
echo "║  CT 991: Chroot Ortamları                                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Kullanıcıdan onay al
echo "Bu script şunları yapacak:"
echo "  1. CT 990 (ders-takip) → Flask uygulamasını kuracak"
echo "  2. CT 991 (ogrenci-vm) → Chroot ortamlarını kuracak"
echo ""
read -p "Devam etmek istiyor musunuz? (e/h): " confirm
if [ "$confirm" != "e" ]; then
    echo "İptal edildi."
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  1/2 CT 990 (ders-takip) Flask App Deployment"
echo "═══════════════════════════════════════════════════════════════"
echo ""

bash $PROJECT_DIR/deploy_app_container.sh

if [ $? -ne 0 ]; then
    echo "❌ CT 990 deployment başarısız!"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  2/2 CT 991 (ogrenci-vm) Chroot Deployment"
echo "═══════════════════════════════════════════════════════════════"
echo ""

bash $PROJECT_DIR/deploy_chroot_container.sh

if [ $? -ne 0 ]; then
    echo "❌ CT 991 deployment başarısız!"
    exit 1
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ TAM DEPLOYMENT BAŞARILI!                                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Sistem Durumu:"
echo ""
echo "CT 990 (Flask App):"
pct exec 990 -- bash -c "
    echo \"  IP: \$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1)\"
    echo \"  Port: 3333\"
    echo \"  Service: \$(systemctl is-active ders-takip.service)\"
    echo \"  URL: http://\$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1):3333\"
"
echo ""
echo "CT 991 (Chroot):"
pct exec 991 -- bash -c "
    echo \"  IP: \$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1)\"
    echo \"  SSH Port: 2222\"
    echo \"  Chroot Base: /home/chroot\"
    echo \"  Test: ssh -p 2222 ogrenci1@\$(ip addr show eth0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1)\"
"
echo ""
echo "Sonraki Adımlar:"
echo "  1. Tarayıcıdan test edin:"
echo "     http://<CT_990_IP>:3333"
echo ""
echo "  2. Öğretmen paneli:"
echo "     http://<CT_990_IP>:3333/teacher"
echo "     Şifre: linux2024"
echo ""
echo "  3. Öğrenci ekleyin (CT 991 içinde):"
echo "     pct exec 991 -- python3 /root/ders-takip/chroot_yonetici.py create ahmetyilmaz220001001"
echo "     pct exec 991 -- python3 /root/ders-takip/chroot_yonetici.py create ayseedemir220001002"
echo ""
echo "  4. Logları izleyin:"
echo "     pct exec 990 -- journalctl -u ders-takip -f"
echo ""
