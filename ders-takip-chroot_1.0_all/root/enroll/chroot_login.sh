#!/bin/bash
#
# Chroot Login Script
# Öğrenci SSH ile bağlandığında otomatik chroot ortamına girer
#

USERNAME="$1"
CHROOT_BASE="/home/chroot"
CHROOT_PATH="$CHROOT_BASE/$USERNAME"

# Chroot yoksa hata ver
if [ ! -d "$CHROOT_PATH" ]; then
    echo "Hata: Chroot ortamı bulunamadı"
    echo "Lütfen öğretmeninizle iletişime geçin"
    exit 1
fi

# Gerekli filesystem'leri mount et
mount_dev() {
    if ! mountpoint -q "$CHROOT_PATH/dev"; then
        mount -o bind /dev "$CHROOT_PATH/dev"
    fi
}

mount_proc() {
    if ! mountpoint -q "$CHROOT_PATH/proc"; then
        mount -t proc proc "$CHROOT_PATH/proc"
    fi
}

mount_sys() {
    if ! mountpoint -q "$CHROOT_PATH/sys"; then
        mount -o bind /sys "$CHROOT_PATH/sys"
    fi
}

# Mount işlemleri
mount_dev
mount_proc
mount_sys

# Chroot içine gir ve login
echo "┌────────────────────────────────────────────────────┐"
echo "│  Kapadokya Üniversitesi - Linux Laboratuvarı      │"
echo "│  Özel Chroot Ortamı                               │"
echo "│                                                    │"
echo "│  Kullanıcı: $USERNAME"
echo "│  Komut: 'sudo su -' ile root olabilirsiniz        │"
echo "└────────────────────────────────────────────────────┘"
echo ""

# Chroot içindeki /bin/su dosyasını kontrol et (Sonsuz döngüyü önlemek için)
if [ ! -x "$CHROOT_PATH/bin/su" ]; then
    echo "❌ HATA: Chroot ortamı bozuk veya eksik yüklenmiş!"
    echo "Sistem yöneticisinin ortamınızı onarması gerekiyor."
    echo "(/bin/su çalıştırılamadı)"
    
    # 5 saniye bekle ve çıkış yap, SSH bağlantısı kopsun ki loop'a girmesin
    sleep 5
    exit 1
fi

# Chroot içine giriş
exec chroot "$CHROOT_PATH" /bin/su - "$USERNAME"
