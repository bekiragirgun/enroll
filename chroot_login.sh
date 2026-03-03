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

# Chroot içine giriş
exec chroot "$CHROOT_PATH" /bin/su - "$USERNAME"
