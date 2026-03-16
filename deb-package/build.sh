#!/bin/bash
# Chroot Terminal DEB paketi oluştur
set -e

cd "$(dirname "$0")"

# chroot_yonetici.py'yi güncelle
cp ../chroot_yonetici.py chroot-terminal_1.0/usr/local/bin/chroot-yonetici
chmod 755 chroot-terminal_1.0/usr/local/bin/chroot-yonetici

# Dosya izinlerini düzelt
chmod 755 chroot-terminal_1.0/DEBIAN/postinst
chmod 755 chroot-terminal_1.0/DEBIAN/prerm
chmod 644 chroot-terminal_1.0/etc/sysctl.d/99-pty-limits.conf
chmod 644 chroot-terminal_1.0/etc/ssh/sshd_config.d/chroot-terminal.conf
chmod 644 chroot-terminal_1.0/etc/systemd/system/*.service
chmod 644 chroot-terminal_1.0/etc/systemd/system/*.timer

# DEB oluştur
dpkg-deb --build chroot-terminal_1.0

echo ""
echo "✅ Paket oluşturuldu: chroot-terminal_1.0.deb"
echo ""
echo "Kurulum: sudo dpkg -i chroot-terminal_1.0.deb"
echo "Kaldırma: sudo dpkg -r chroot-terminal"
