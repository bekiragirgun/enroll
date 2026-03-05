#!/bin/bash
# Kapadokya Ders Takip - Debian Paketleyici
# Bu script, chroot_yonetici.py ve gerekli bağımlılıkları içeren bir .deb paketi oluşturur.

set -e

VERSION="1.0"
PKG_DIR="ders-takip-chroot_${VERSION}_all"

echo "📦 '$PKG_DIR' için paket yapısı oluşturuluyor..."
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/root/enroll"
mkdir -p "$PKG_DIR/usr/local/bin"

echo "📄 Dosyalar kopyalanıyor..."
# Ana scripti kopyala
cp chroot_yonetici.py "$PKG_DIR/root/enroll/"
chmod +x "$PKG_DIR/root/enroll/chroot_yonetici.py"
cp chroot_login.sh "$PKG_DIR/root/enroll/" 2>/dev/null || true
chmod +x "$PKG_DIR/root/enroll/chroot_login.sh" 2>/dev/null || true

# Kısa komut için symlink (kurulum aşamasında kök dizine symlinklenecek)
ln -s /root/enroll/chroot_yonetici.py "$PKG_DIR/usr/local/bin/chroot-yonetici"

echo "📝 Kontrol dosyası (metadata) oluşturuluyor..."
cat <<EOF > "$PKG_DIR/DEBIAN/control"
Package: ders-takip-chroot
Version: $VERSION
Architecture: all
Maintainer: Kapadokya Universitesi AAC
Depends: python3, debootstrap, rsync, sudo, openssh-server, vim, curl, wget
Section: education
Priority: optional
Description: Kapadokya Ders Takip Sistemi - Chroot Terminal Yöneticisi
 Bu paket, ogrenci sanal makinelerinde (CT 991, 992 vb.) chroot 
 ortamini kurmak, PTY onarimini yapmak (V14) ve ogrenci oturumlarini 
 yonetmek icin gerekli Python betiklerini icerir. Bagimliliklari
 ve servisleri otomatik kurar.
EOF

echo "⚙️ Kurulum sonrası (postinst) scripti oluşturuluyor..."
cat <<EOF > "$PKG_DIR/DEBIAN/postinst"
#!/bin/bash
set -e

echo "🔧 ders-takip-chroot yapilandiriliyor..."

# 1. Gerekli izinler
chmod +x /root/enroll/chroot_yonetici.py

# 2. Kalici PTY onarim servisini tetikle (chroot_yonetici icinde persist komutu)
echo "🛠️ Kalici PTY onarim servisi kurulumu..."
if [ -f "/root/enroll/chroot_yonetici.py" ]; then
    /root/enroll/chroot_yonetici.py persist || true
fi

# 3. SSH baglantisi icin hazirlik
mkdir -p /home/chroot

echo "================================================================"
echo "🎯 Kurulum bashariyla tamamlandi!"
echo ""
echo "Terminal sablonunu indirmek ve hazirlamak icin uzerinde"
echo "su komutu calistirin:"
echo ""
echo "    sudo chroot-yonetici init"
echo ""
echo "================================================================"

exit 0
EOF
chmod 755 "$PKG_DIR/DEBIAN/postinst"

echo "🔨 Paket insa ediliyor..."

if command -v dpkg-deb &> /dev/null; then
    dpkg-deb --build "$PKG_DIR"
elif command -v docker &> /dev/null; then
    echo "⚠️ dpkg-deb bulunamadi (macOS/Windows ortami). Docker kullaniliyor..."
    docker run --rm -v "$(pwd):/work" -w /work debian:bookworm-slim dpkg-deb --build "$PKG_DIR"
elif command -v limactl &> /dev/null; then
    echo "⚠️ dpkg-deb ve Docker bulunamadi. Lima kullaniliyor..."
    # 'linux-egitim' veya 'default' instance'ini dene
    if limactl list -q | grep -q linux-egitim; then
        limactl start linux-egitim 2>/dev/null || true
        limactl shell linux-egitim dpkg-deb --build "$PKG_DIR"
    else
        lima dpkg-deb --build "$PKG_DIR"
    fi
else
    echo "❌ HATA: dpkg-deb, Docker veya Lima bulunamadi."
    echo "Bu dizini bir Linux makinesine kopyalayip 'dpkg-deb --build $PKG_DIR' calistirin."
    exit 1
fi

echo "🎉 Islem tamam! Varlik: ${PKG_DIR}.deb"
echo "Paketi CT (Proxmox Container) icine gonderip su komutla kurabilirsiniz:"
echo "sudo dpkg -i ${PKG_DIR}.deb || sudo apt-get install -f"
