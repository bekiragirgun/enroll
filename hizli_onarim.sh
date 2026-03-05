#!/bin/bash
# Kapadokya Ders Takip Sistemi - Hızlı Onarım ve Kalıcı Fix Scripti
# Kullanım: ./hizli_onarim.sh

echo "🛠️ Terminal onarımı başlatılıyor..."

# 1. Dosyaları senkronize et
python3 chroot_terminal.py sync

# 2. Kalıcı servis kurulumunu tetikle
# chroot_terminal.py içinde SSH kullanarak remote VM'de persist komutunu çalıştıracağız.
# Veya doğrudan bu script üzerinden SSH ile yapabiliriz.

# CT 991 bilgilerini chroot_terminal.py'den alalım (basitçe)
HOST="192.168.111.51"
USER="root"
PORT="22"
SCRIPT_PATH="/root/enroll/chroot_yonetici.py"

echo "📡 CT 991 ($HOST) üzerinde kalıcı onarım servisi kuruluyor..."
ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -p $PORT $USER@$HOST "python3 $SCRIPT_PATH persist"

if [ $? -eq 0 ]; then
    echo "✅ Onarım tamamlandı! Terminal artık stabil çalışmalı."
else
    echo "❌ Onarım sırasında hata oluştu. Lütfen bağlantıları kontrol edin."
fi
