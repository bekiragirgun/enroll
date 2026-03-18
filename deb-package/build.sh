#!/bin/bash
# Chroot Terminal DEB paketi oluştur
set -e

cd "$(dirname "$0")"

PKG="chroot-terminal_1.2"

# Kaynak: varsa ../chroot_yonetici.py, yoksa paketin kendi kopyasını kullan
if [ -f "../chroot_yonetici.py" ]; then
    echo "→ chroot_yonetici.py kaynaktan kopyalanıyor..."
    cp ../chroot_yonetici.py ${PKG}/usr/local/bin/chroot-yonetici
fi
chmod 755 ${PKG}/usr/local/bin/chroot-yonetici

# Dosya izinlerini düzelt
chmod 755 ${PKG}/DEBIAN/postinst
chmod 755 ${PKG}/DEBIAN/prerm
chmod 644 ${PKG}/etc/sysctl.d/99-pty-limits.conf
chmod 644 ${PKG}/etc/ssh/sshd_config.d/chroot-terminal.conf
chmod 644 ${PKG}/etc/security/limits.d/99-chroot-terminal.conf
chmod 644 ${PKG}/etc/systemd/timesyncd.conf.d/chroot-terminal.conf
chmod 644 ${PKG}/etc/systemd/system/*.service
chmod 644 ${PKG}/etc/systemd/system/*.timer

# DEB oluştur
dpkg-deb --build ${PKG}

echo ""
echo "✅ Paket oluşturuldu: ${PKG}.deb"
echo ""
echo "Kurulum (bağımlılıklar otomatik indirilir):"
echo "  sudo apt install ./${PKG}.deb"
echo ""
echo "Kaldırma:"
echo "  sudo dpkg -r chroot-terminal"
