#!/bin/bash
# Proxmox Storage Bulucu ve Deployment Script

echo "🔍 Proxmox Storage Analizi..."
echo "=============================="

# Mevcut storage'ları listele
echo "📦 Mevcut Storage Listesi:"
pvesm list

echo ""
echo "🔍 Detaylı Storage Bilgileri:"
pvesm status

echo ""
echo "💾 LVM Storage var mı?"
if pvesm list | grep -q "lvm"; then
    echo "✅ LVM storage bulundu"
    pvesm list | grep lvm
else
    echo "❌ LVM storage yok"
fi

echo ""
echo "📁 Directory Storage var mı?"
if pvesm list | grep -q "dir"; then
    echo "✅ Directory storage bulundu"
    pvesm list | grep dir
else
    echo "❌ Directory storage yok"
fi

echo ""
echo "🔄 ZFS Storage var mı?"
if pvesm list | grep -q "zfs"; then
    echo "✅ ZFS storage bulundu"
    pvesm list | grep zfs
else
    echo "❌ ZFS storage yok"
fi

echo ""
echo "🎯 Uygun Storage Seçimi:"
STORAGE=$(pvesm list | grep -E "local|dir|lvm|zfs" | head -1 | awk '{print $1}')
if [ -n "$STORAGE" ]; then
    echo "📌 Otomatik seçilen storage: $STORAGE"

    # Deployment script'i güncelle
    cat > proxmox-deploy-fixed.sh << EOF
#!/bin/bash
# Proxmox Deployment Script (Storage Düzeltmeli)

set -e

# Konfigürasyon
STORAGE="$STORAGE"
CTID_WEB=9001
CTID_TERM=9002
HOSTNAME_WEB="ders-takip-web"
HOSTNAME_TERM="linux-egitim"
MEMORY=2048
CORES=2
BRIDGE="vmbr0"

echo "🚀 Proxmox Deployment Başlıyor..."
echo "Kullanılan Storage: $STORAGE"
echo "================================"

if ! pvesm list | grep -q "\$STORAGE"; then
    echo "❌ HATA: Storage '\$STORAGE' bulunamadı!"
    echo ""
    echo "Mevcut storage'lar:"
    pvesm list
    exit 1
fi

echo "✅ Storage kontrolü geçti: \$STORAGE"

echo "📦 1. Web Container Oluşturuluyor..."
pct create \$STORAGE:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst \\
  --hostname \$HOSTNAME_WEB \\
  --memory \$MEMORY \\
  --cores \$CORES \\
  --net0 name=eth0,bridge=\$BRIDGE,ip=dhcp \\
  --features nesting=1,keyctl=1 \\
  --onboot 1

echo "⏳ Web Container başlatılıyor..."
pct start \$CTID_WEB

echo "📦 Sistem güncelleniyor..."
pct exec \$CTID_WEB -- bash -c "apt-get update && apt-get upgrade -y"

echo "🐍 Python ve araçlar yükleniyor..."
pct exec \$CTID_WEB -- bash -c "apt-get install -y python3 python3-pip python3-venv git vim curl wget sqlite3"

echo "📂 Proje dosyaları kopyalanıyor..."
# Proje dosyalarının olduğu dizini buraya güncelleyin
PROJECT_DIR="/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip"

echo "📂 Mevcut dizin: \$PROJECT_DIR"

# Container içine dosya kopyalama
pct push \$CTID_WEB \$PROJECT_DIR /root/ders_takip

echo "🔧 Python ortamı kuruluyor..."
pct exec \$CTID_WEB -- bash -c "cd /root/ders_takip && python3 -m venv venv && source venv/bin/activate && pip install flask gunicorn"

echo "📄 Servis dosyası oluşturuluyor..."
pct exec \$CTID_WEB -- bash -c "cat > /etc/systemd/system/ders-takip.service << 'EOFSERVICE'
[Unit]
Description=Ders Takip Sistemi
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/ders_takip
Environment=\"PATH=/root/venv/bin\"
ExecStart=/root/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOFSERVICE
"

echo "🎯 Servis aktifleştiriliyor..."
pct exec \$CTID_WEB -- bash -c "systemctl daemon-reload && systemctl enable ders-takip.service && systemctl start ders-takip.service"

echo "📦 2. Terminal Container Oluşturuluyor..."
pct create \$STORAGE:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst \\
  --hostname \$HOSTNAME_TERM \\
  --memory \$MEMORY \\
  --cores \$CORES \\
  --net0 name=eth0,bridge=\$BRIDGE,ip=dhcp \\
  --features nesting=1,keyctl=1 \\
  --onboot 1

echo "⏳ Terminal Container başlatılıyor..."
pct start \$CTID_TERM

echo "📦 Sistem güncelleniyor..."
pct exec \$CTID_TERM -- bash -c "apt-get update && apt-get upgrade -y"

echo "📂 Proje dosyaları kopyalanıyor..."
pct push \$CTID_TERM \$PROJECT_DIR/provision.sh /root/

echo "🔧 Linux eğitim araçları kuruluyor..."
pct exec \$CTID_TERM -- bash /root/provision.sh

echo "✅ Kurulum Tamamlandı!"
echo ""
echo "🌐 Erişim Bilgileri:"
pct exec \$CTID_WEB -- hostname -I | awk '{print "   Web Container IP: " \$2}'
pct exec \$CTID_TERM -- hostname -I | awk '{print "   Terminal Container IP: " \$2}'
echo ""
echo "🎓 Öğrenci Girişi:"
echo "   SSH: ssh ogrenci@<TERMINAL_IP>"
echo "   Şifre: ogrenci"
echo ""
echo "🔗 Web Erişimi:"
echo "   http://<WEB_IP>:5000"
EOF

    chmod +x proxmox-deploy-fixed.sh
    echo "✅ Deployment script'i oluşturuldu: proxmox-deploy-fixed.sh"

else
    echo "❌ Uygun storage bulunamadı!"
    echo ""
    echo "Lütfen önce Proxmox'te storage oluşturun:"
    echo "1. ZFS: pvesm create zfs <disk> <name>"
    echo "2. LVM: pvesm create lvm <disk> <name>"
    echo "3. Directory: pvesm create dir <path> <name>"
fi
