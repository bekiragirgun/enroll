#!/bin/bash
# Kapadokya Ders Takip Sistemi - İnteraktif Hızlı Onarım Scripti
# Kullanım: ./hizli_onarim.sh

clear
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🛠️  Kapadokya Ders Takip Sistemi - Terminal Onarımı         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Varsayılan değerler
DEFAULT_IP="192.168.111.51"
DEFAULT_PORT="2222"
DEFAULT_USER="root"

# Kullanıcıdan bilgileri al
read -p "🌐 Terminal VM IP Adresi [$DEFAULT_IP]: " HOST
HOST=${HOST:-$DEFAULT_IP}

read -p "🔢 SSH Portu [$DEFAULT_PORT]: " PORT
PORT=${PORT:-$DEFAULT_PORT}

read -p "👤 SSH Kullanıcı Adı [$DEFAULT_USER]: " USER
USER=${USER:-$DEFAULT_USER}

echo ""
echo "⚙️  Yapılandırma:"
echo "   IP: $HOST"
echo "   Port: $PORT"
echo "   Kullanıcı: $USER"
echo ""

# 1. chroot_terminal.py dosyasındaki ayarları geçici olarak güncellemek yerine 
# script içinden doğrudan SSH ile işlemleri yapalım.

# Önce dosyaları senkronize etmek için chroot_terminal'i kullanalım (ama IP/Port uyuşmazlığı olabilir)
echo "📡 Dosyalar senkronize ediliyor..."
# chroot_terminal.py içinde de ayarların doğru olması gerekebilir. 
# Kullanıcıya bir hatırlatma yapalım.
echo "⚠️  Not: chroot_terminal.py içindeki CT_991_HOST ve CT_991_REAL_SSH_PORT 
     değerlerinin de bu bilgilerle eşleştiğinden emin olun."

# 2. Kalıcı onarımı doğrudan SSH ile tetikle
echo "🚀 Onarım komutu gönderiliyor..."
SCRIPT_PATH="/root/enroll/chroot_yonetici.py"

# Önce dizini oluştur ve chroot_yonetici.py'yi gönder
ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -p $PORT $USER@$HOST "mkdir -p /root/enroll"
scp -P $PORT chroot_yonetici.py $USER@$HOST:$SCRIPT_PATH

# Komutları çalıştır
ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -p $PORT $USER@$HOST "chmod +x $SCRIPT_PATH && python3 $SCRIPT_PATH repair && python3 $SCRIPT_PATH persist"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Onarım tamamlandı! Terminal artık stabil çalışmalı."
    echo "   VM her açıldığında onarım otomatik olarak yapılacaktır."
else
    echo ""
    echo "❌ Onarım sırasında hata oluştu. Lütfen şunları kontrol edin:"
    echo "   1. IP ve Port doğru mu?"
    echo "   2. SSH şifresiz giriş veya doğru anahtar tanımlı mı?"
    echo "   3. Hedef sunucuda Python3 kurulu mu?"
fi
