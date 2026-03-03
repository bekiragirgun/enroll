#!/bin/bash
set -e

echo "🐧 Linux eğitim ortamı hazırlanıyor..."

# Değişkenler
STUDENT_USER="ogrenci"
STUDENT_PASS="ogrenci"

# Sistem güncellemesi
echo "📦 Sistem güncelleniyor..."
apt-get update
apt-get upgrade -y

# Temel sistem araçları
echo "🔧 Temel sistem araçları kuruluyor..."
apt-get install -y \
    bash-completion \
    ca-certificates \
    curl \
    wget \
    gnupg \
    lsb-release \
    software-properties-common \
    apt-transport-https \
    man-db \
    manpages \
    manpages-tr \
    vim \
    nano \
    joe \
    mcedit \
    tmux \
    screen \
    htop \
    btop \
    iotop \
    iftop \
    nethogs \
    tree \
    file \
    less \
    most \
    zile \
    pinfo

# Network araçları
echo "🌐 Network araçları kuruluyor..."
apt-get install -y \
    iproute2 \
    iputils-ping \
    iputils-tracepath \
    traceroute \
    net-tools \
    dnsutils \
    whois \
    netcat \
    nmap \
    tcpdump \
    wireshark-common \
    curl \
    wget \
    ssh \
    openssh-server \
    openssh-client \
    telnet \
    ftp \
    lftp \
    rsync \
    scp \
    socat \
    iptables \
    nftables \
    ipset \
    conntrack \
    ethtool \
    mtr-tiny \
    bind9-dnsutils \
    bind9-host \
    nslookup

# Sistem yönetim araçları
echo "⚙️  Sistem yönetim araçları kuruluyor..."
apt-get install -y \
    systemd \
    systemd-sysv \
    systemd-coredump \
    cron \
    rsyslog \
    logrotate \
    syslog-ng-core \
    acl \
    attr \
    quota \
    xfsprogs \
    e2fsprogs \
    btrfs-progs \
    lvm2 \
    mdadm \
    parted \
    fdisk \
    gdisk \
    util-linux \
    mount \
    umount \
    losetup \
    cryptsetup \
    smartmontools \
    hdparm \
    sdparm \
    lsscsi \
    sg3-utils \
    usbutils \
    pciutils \
    dmidecode \
    lshw \
    lm-sensors \
    fancontrol \
    cpufrequtils \
    numactl \
    schedtool

# Process yönetim ve monitoring
echo "📊 Process yönetim araçları kuruluyor..."
apt-get install -y \
    procps \
    psmisc \
    psutils \
    lsof \
    strace \
    ltrace \
    sysstat \
    dstat \
    glances \
    iotop \
    htop \
    btop \
    atop \
    perf-tools-unstable

# Geliştirme araçları
echo "👨‍💻 Geliştirme araçları kuruluyor..."
apt-get install -y \
    build-essential \
    gcc \
    g++ \
    clang \
    make \
    cmake \
    autoconf \
    automake \
    libtool \
    pkg-config \
    git \
    subversion \
    mercurial \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    python3-full \
    python3-setuptools \
    python3-wheel \
    perl \
    perl-doc \
    php \
    php-cli \
    ruby \
    ruby-dev \
    nodejs \
    npm \
    golang \
    rustc \
    cargo

# Web sunucu ve veritabanı (eğitim amaçlı)
echo "🌍 Web sunucu ve veritabanı kuruluyor..."
apt-get install -y \
    apache2 \
    nginx-light \
    lighttpd \
    sqlite3 \
    postgresql-client \
    mysql-client \
    redis-tools \
    mongodb-client

# Güvenlik araçları
echo "🔒 Güvenlik araçları kuruluyor..."
apt-get install -y \
    ufw \
    fail2ban \
    rkhunter \
    chkrootkit \
    auditd \
    libpam-modules \
    apparmor \
    apparmor-utils \
    selinux-basics \
    openssl \
    gnutls-bin \
    stunnel4

# Dosya sistemleri ve depolama
echo "💾 Dosya sistemi araçları kuruluyor..."
apt-get install -y \
    xfsprogs \
    btrfs-progs \
    reiserfsprogs \
    jfsutils \
    reiser4progs \
    zfsutils-linux

# Diğer faydalı araçlar
echo "🛠️  Diğer araçlar kuruluyor..."
apt-get install -y \
    zip \
    unzip \
    tar \
    gzip \
    bzip2 \
    xz-utils \
    p7zip \
    p7zip-full \
    arj \
    rar \
    unrar \
    cpio \
    faac \
    faad \
    flac \
    lame \
    vorbis-tools \
    imagemagick \
    ffmpeg \
    sox \
    mpg123 \
    vlc \
    poppler-utils \
    antiword \
    catdoc \
    xls2csv \
    odt2txt \
    pandoc

# Servislerin otomatik başlaması (eğitim için)
echo "🎯 Servisler yapılandırılıyor..."
systemctl enable ssh
systemctl enable cron
systemctl enable rsyslog

# Öğrenci kullanıcısı oluşturma
echo "👤 Öğrenci kullanıcısı oluşturuluyor..."
if id "$STUDENT_USER" &>/dev/null; then
    echo "Kullanıcı zaten mevcut"
else
    useradd -m -s /bin/bash -G sudo,dialout,cdrom,floppy,audio,dip,video,plugdev,netdev $STUDENT_USER
    echo "$STUDENT_USER:$STUDENT_PASS" | chpasswd
    echo "$STUDENT_USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$STUDENT_USER
    chmod 440 /etc/sudoers.d/$STUDENT_USER
fi

# Öğrenci kullanıcısı için bash yapılandırması
echo "📝 Bash yapılandırması ayarlanıyor..."
cat >> /home/$STUDENT_USER/.bashrc << 'EOF'

# Linux eğitim ortamı özelleştirmeleri
export EDITOR=vim
export VISUAL=vim
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTTIMEFORMAT="%F %T "
export HISTCONTROL=ignoredups:erasedups
shopt -s histappend
shopt -s cmdhist

# Renkli prompt
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

# Aliaslar
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias df='df -h'
alias du='du -h'
alias free='free -h'
alias tree='tree -a'
alias ip='ip -color=auto'
alias journalctl='journalctl --no-pager'
alias systemctl='systemctl --no-pager'
alias ss='ss -tulw'

# Eğitim amaçlı fonksiyonlar
# Sistem durumu özeti
sysinfo() {
    echo "=== Sistem Bilgileri ==="
    echo "Kernel: $(uname -r)"
    echo "Uptime: $(uptime -p)"
    echo "CPU: $(nproc) çekirdek"
    echo "Memory: $(free -h | grep Mem | awk '{print $2}')"
    echo "Disk: $(df -h / | tail -1 | awk '{print $2}')"
    echo "IP: $(ip -4 addr show | grep inet | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1)"
    echo ""
    echo "=== Servisler ==="
    systemctl list-units --type=service --state=running --no-pager -q
    echo ""
    echo "=== Dinlenen Portlar ==="
    ss -tulwn | grep LISTEN
}

# Process ağacı
pstree() {
    ps auxf
}

# Hızlı disk kullanımı
diskhogs() {
    du -h /* 2>/dev/null | sort -rh | head -20
}

EOF

chown $STUDENT_USER:$STUDENT_USER /home/$STUDENT_USER/.bashrc

# Pratik eğitim dosyaları oluşturma
echo "📚 Pratik eğitim dosyaları oluşturuluyor..."
mkdir -p /home/$STUDENT_USER/{egitim,pratik,testler,loglar}

# Network egzersiz dosyaları
cat > /home/$STUDENT_USER/egitim/network-egzersizleri.sh << 'EOF'
#!/bin/bash
# Network egzersizleri için yardımcı script

echo "1. IP adresini görüntüle:"
echo "   ip addr show"
echo "   ip a"
echo ""

echo "2. Network istatistikleri:"
echo "   ip -s link"
echo "   ip -s addr"
echo ""

echo "3. Routing tablosu:"
echo "   ip route"
echo "   ip r"
echo ""

echo "4. ARP tablosu:"
echo "   ip neigh"
echo "   arp -n"
echo ""

echo "5. Bağlantı testleri:"
echo "   ping -c 4 google.com"
echo "   traceroute google.com"
echo "   tracepath google.com"
echo ""

echo "6. DNS sorguları:"
echo "   nslookup google.com"
echo "   dig google.com"
echo "   host google.com"
echo ""

echo "7. Port taraması:"
echo "   nmap -sT localhost"
echo "   ss -tulwn"
echo ""

echo "8. Network trafiği izleme:"
echo "   tcpdump -i any -c 10"
echo "   sudo tcpdump -i eth0 port 80"
echo ""

echo "9. İnternet hız testi:"
echo "   curl -o /dev/null http://speedtest.tele2.net/100MB.zip"
echo ""

echo "10. Network gecikmesi:"
echo "   ping -c 10 -i 0.2 google.com"
EOF
chmod +x /home/$STUDENT_USER/egitim/network-egzersizleri.sh
chown $STUDENT_USER:$STUDENT_USER /home/$STUDENT_USER/egitim/network-egzersizleri.sh

# Process yönetimi egzersizleri
cat > /home/$STUDENT_USER/egitim/process-egzersizleri.sh << 'EOF'
#!/bin/bash
# Process yönetimi egzersizleri

echo "1. Tüm processleri listele:"
echo "   ps aux"
echo "   ps -ef"
echo ""

echo "2. Process ağacı:"
echo "   pstree"
echo "   ps auxf"
echo ""

echo "3. CPU kullanımı (sıralı):"
echo "   ps aux --sort=-%cpu | head -20"
echo "   top"
echo "   htop"
echo ""

echo "4. Memory kullanımı (sıralı):"
echo "   ps aux --sort=-%mem | head -20"
echo ""

echo "5. Process detayları:"
echo "   ps -p \$\$ -f"
echo "   cat /proc/\$\$/status"
echo ""

echo "6. Process öldürme:"
echo "   kill <PID>"
echo "   kill -9 <PID>"
echo "   killall <isim>"
echo "   pkill <pattern>"
echo ""

echo "7. Background/Foreground:"
echo "   komut &  # Background"
echo "   jobs    # Job listesi"
echo "   fg %1   # Foreground"
echo "   bg %1   # Background'a devam"
echo ""

echo "8. Process izleme:"
echo "   strace -p <PID>"
echo "   ltrace -p <PID>"
echo "   watch -n 1 'ps aux | grep nginx'"
echo ""

echo "9. Servis yönetimi:"
echo "   systemctl status <servis>"
echo "   systemctl start <servis>"
echo "   systemctl stop <servis>"
echo "   systemctl restart <servis>"
echo "   journalctl -u <servis> -f"
echo ""

echo "10. Sistem kaynakları:"
echo "   free -h        # Memory"
echo "   df -h          # Disk"
echo "   uptime         # Uptime/load"
echo "   vmstat 1 5     # VM istatistikleri"
echo "   iostat 1 5     # I/O istatistikleri"
EOF
chmod +x /home/$STUDENT_USER/egitim/process-egzersizleri.sh
chown $STUDENT_USER:$STUDENT_USER /home/$STUDENT_USER/egitim/process-egzersizleri.sh

# Kullanıcı yönetimi egzersizleri
cat > /home/$STUDENT_USER/egitim/kullanici-egzersizleri.sh << 'EOF'
#!/bin/bash
# Kullanıcı yönetimi egzersizleri

echo "1. Kullanıcı bilgilerini görüntüle:"
echo "   id"
echo "   whoami"
echo "   w"
echo "   who"
echo ""

echo "2. Tüm kullanıcıları listele:"
echo "   cat /etc/passwd"
echo "   getent passwd"
echo "   cut -d: -f1 /etc/passwd"
echo ""

echo "3. Grup bilgileri:"
echo "   groups"
echo "   groups ogrenci"
echo "   cat /etc/group"
echo "   getent group"
echo ""

echo "4. Kullanıcı ekleme:"
echo "   sudo useradd -m -s /bin/bash yeniuser"
echo "   sudo usermod -aG sudo yeniuser"
echo "   echo 'yeniuser:pass' | sudo chpasswd"
echo ""

echo "5. Kullanıcı silme:"
echo "   sudo userdel -r yeniuser  # -r: home diziniyle birlikte sil"
echo ""

echo "6. Grup işlemleri:"
echo "   sudo groupadd yenigrup"
echo "   sudo gpasswd -a user yenigrup"
echo "   sudo groupdel yenigrup"
echo ""

echo "7. Sudo yapılandırması:"
echo "   sudo visudo"
echo "   sudo -l  # Kullanıcı sudo haklarını görüntüle"
echo "   sudo -i  # Root olarak shell"
echo ""

echo "8. Login geçmişi:"
echo "   last"
echo "   lastlog"
echo "   w"
echo "   who"
echo ""

echo "9. Parola yönetimi:"
echo "   passwd          # Kendi parolanı değiştir"
echo "   sudo passwd <user>  # Başka kullanıcının parolasını değiştir"
echo "   sudo chage -l <user>  # Parola yaş bilgisi"
echo ""

echo "10. Permission işlemleri:"
echo "   ls -l           # Dosya izinleri"
echo "   chmod 755 dosya # İzinleri değiştir"
echo "   chown user:grp dosya  # Sahipliği değiştir"
echo "   umask           # Varsayılan umask değeri"
EOF
chmod +x /home/$STUDENT_USER/egitim/kullanici-egzersizleri.sh
chown $STUDENT_USER:$STUDENT_USER /home/$STUDENT_USER/egitim/kullanici-egzersizleri.sh

# Servis yönetimi egzersizleri
cat > /home/$STUDENT_USER/egitim/servis-egzersizleri.sh << 'EOF'
#!/bin/bash
# Servis yönetimi egzersizleri

echo "1. Tüm servisleri listele:"
echo "   systemctl list-units --type=service"
echo "   systemctl list-units --type=service --all"
echo ""

echo "2. Servis durumu:"
echo "   systemctl status <servis-adı>"
echo "   systemctl is-active <servis-adı>"
echo "   systemctl is-enabled <servis-adı>"
echo ""

echo "3. Servis başlatma/durdurma:"
echo "   sudo systemctl start <servis-adı>"
echo "   sudo systemctl stop <servis-adı>"
echo "   sudo systemctl restart <servis-adı>"
echo "   sudo systemctl reload <servis-adı>"
echo ""

echo "4. Servisleri otomatik başlatma:"
echo "   sudo systemctl enable <servis-adı>"
echo "   sudo systemctl disable <servis-adı>"
echo ""

echo "5. Servis logları:"
echo "   journalctl -u <servis-adı>"
echo "   journalctl -u <servis-adı> -f  # Follow mode"
echo "   journalctl -u <servis-adı> --since today"
echo "   journalctl -u <servis-adı> -p err  # Sadece hatalar"
echo ""

echo "6. Servis dosyalarını bulma:"
echo "   systemctl show <servis-adı> -p FragmentPath"
echo "   systemctl cat <servis-adı>"
echo "   systemctl status <servis-adı> | grep loaded"
echo ""

echo "7. Servis bağımlılıkları:"
echo "   systemctl list-dependencies <servis-adı>"
echo "   systemctl list-dependencies --all <servis-adı>"
echo ""

echo "8. Başarısız servisleri görüntüle:"
echo "   systemctl --failed"
echo "   journalctl -p err -b"
echo ""

echo "9. Servis yeniden yükleme:"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl reset-failed"
echo ""

echo "10. Mevcut önemli servisler:"
echo "   sshd        - SSH sunucu"
echo "   cron        - Zamanlanmış görevler"
echo "   rsyslog     - Sistem logları"
echo "   systemd     - Init system"
echo "   network     - Ağ bağlantısı"
echo "   ufw         - Firewall"
echo ""

echo "Pratik örnekler:"
echo "   sudo systemctl start ssh"
echo "   sudo systemctl enable ssh"
echo "   sudo systemctl status ssh"
echo "   journalctl -u ssh -f"
EOF
chmod +x /home/$STUDENT_USER/egitim/servis-egzersizleri.sh
chown $STUDENT_USER:$STUDENT_USER /home/$STUDENT_USER/egitim/servis-egzersizleri.sh

# Disk ve dosya sistemi egzersizleri
cat > /home/$STUDENT_USER/egitim/disk-egzersizleri.sh << 'EOF'
#!/bin/bash
# Disk ve dosya sistemi egzersizleri

echo "1. Disk kullanımı:"
echo "   df -h"
echo "   df -i        # Inode kullanımı"
echo "   df -T        # Dosya sistemi tipleri"
echo ""

echo "2. Disk kullanımını sırala:"
echo "   du -sh * | sort -rh | head -20"
echo "   du -h --max-depth=1 /"
echo ""

echo "3. Disk bilgileri:"
echo "   fdisk -l"
echo "   lsblk"
echo "   blkid"
echo "   parted -l"
echo ""

echo "4. Mount noktaları:"
echo "   mount"
echo "   findmnt"
echo "   cat /etc/fstab"
echo ""

echo "5. Dosya sistemi tipleri:"
echo "   mount | grep ext4"
echo "   mount | grep xfs"
echo "   mount | grep btrfs"
echo ""

echo "6. Inode kullanımı:"
echo "   df -i"
echo "   find / -xdev -printf '%h\n' | sort | uniq -c | sort -k 1 -n"
echo ""

echo "7. Disk I/O monitoring:"
echo "   iotop"
echo "   iostat -x 1"
echo "   dstat -d"
echo ""

echo "8. Disk performans testi:"
echo "   dd if=/dev/zero of=test.img bs=1G count=1 oflag=direct"
echo "   dd if=test.img of=/dev/null bs=1M"
echo "   rm test.img"
echo ""

echo "9. LVM işlemleri (eğer LVM varsa):"
echo "   sudo pvdisplay"
echo "   sudo vgdisplay"
echo "   sudo lvdisplay"
echo ""

echo "10. RAID durumu (eğer RAID varsa):"
echo "   cat /proc/mdstat"
echo "   sudo mdadm --detail /dev/md0"
echo ""

echo "Pratik komutlar:"
echo "   Disk temizleme: sudo apt clean"
echo "   Eski kerneller: sudo apt autoremove --purge"
echo "   Log temizleme: sudo journalctl --vacuum-time=7d"
EOF
chmod +x /home/$STUDENT_USER/egitim/disk-egzersizleri.sh
chown $STUDENT_USER:$STUDENT_USER /home/$STUDENT_USER/egitim/disk-egzersizleri.sh

# Test dosyaları oluşturma
echo "📝 Test dosyaları oluşturuluyor..."

# Büyük dosya testi için
dd if=/dev/zero of=/home/$STUDENT_USER/testler/test-100mb.img bs=1M count=100 2>/dev/null
chown $STUDENT_USER:$STUDENT_USER /home/$STUDENT_USER/testler/test-100mb.img

# Script test dosyası
cat > /home/$STUDENT_USER/testler/test-servis.sh << 'EOF'
#!/bin/bash
# Basit servis test script'i
while true; do
    echo "$(date): Servis çalışıyor..."
    sleep 5
done
EOF
chmod +x /home/$STUDENT_USER/testler/test-servis.sh
chown $STUDENT_USER:$STUDENT_USER /home/$STUDENT_USER/testler/test-servis.sh

# Servis dosyası oluşturma (systemd)
cat > /etc/systemd/system/test-servis.service << 'EOF'
[Unit]
Description=Test Servisi
After=network.target

[Service]
Type=simple
User=ogrenci
WorkingDirectory=/home/ogrenci/testler
ExecStart=/home/ogrenci/testler/test-servis.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload

# README dosyası
cat > /home/$STUDENT_USER/README.md << 'EOF'
# Linux Eğitim Ortamı

Bu ortam, Linux sistem yönetimi eğitimi için hazırlanmıştır.

## Öğrenci Hesabı

- **Kullanıcı:** ogrenci
- **Şifre:** ogrenci
- **Sudo:** Şifresiz

## Temel Komutlar

### Sistem Bilgileri
```bash
sysinfo          # Sistem özeti
uname -a         # Kernel bilgisi
hostname         # Sistem adı
uptime           # Çalışma süresi
```

### Kullanıcı Yönetimi
```bash
id               # Kullanıcı bilgisi
groups           # Gruplar
w                # Bağlı kullanıcılar
last             # Login geçmişi
```

### Process Yönetimi
```bash
ps aux           # Process listesi
top              # İnteraktif monitoring
htop             # Gelişmiş monitoring
pstree           # Process ağacı
```

### Network
```bash
ip addr          # IP adresi
ip route         # Routing tablosu
ss -tulwn        # Açık portlar
ping host        # Bağlantı testi
```

### Disk Yönetimi
```bash
df -h            # Disk kullanımı
du -sh *         # Dizin boyutları
lsblk            # Block cihazlar
mount            # Mount noktaları
```

### Servis Yönetimi
```bash
systemctl status <servis>
systemctl start <servis>
systemctl stop <servis>
systemctl restart <servis>
journalctl -u <servis>
```

## Eğitim Dizinleri

- `~/egitim/` - Eğitim materyalleri ve egzersizler
- `~/pratik/` - Pratik çalışmalarınız
- `~/testler/` - Test dosyaları
- `~/loglar/` - Log dosyaları
- `~/shared/` - Host ile paylaşılan dizin

## Eğzersiz Scriptleri

Egzersiz script'leri `~/egitim/` dizininde bulunabilir:

```bash
./egitim/network-egzersizleri.sh
./egitim/process-egzersizleri.sh
./egitim/kullanici-egzersizleri.sh
./egitim/servis-egzersizleri.sh
./egitim/disk-egzersizleri.sh
```

## Önemli Dosyalar

- `/etc/passwd` - Kullanıcı bilgileri
- `/etc/shadow` - Kullanıcı parolaları
- `/etc/group` - Grup bilgileri
- `/etc/fstab` - Mount ayarları
- `/etc/sudoers` - Sudo yapılandırması
- `/var/log/` - Log dosyaları
- `/proc/` - Kernel bilgileri
- `/sys/` - Sistem parametreleri

## Faydalı İpuçları

1. **Tab tuşu** ile komut tamamlama kullanın
2. **Ctrl+R** ile komut geçmişinde arama yapın
3. **history** komutu ile komut geçmişini görün
4. **man <komut>** ile yardım alın
5. **<komut> --help** ile kısa yardım alın
6. **Ctrl+C** ile çalışan işlemi durdurun
7. **Ctrl+Z** ile işlemi arka plana alın
8. **bg/fg** ile arka plan/ön plan arasında geçin
9. **jobs** ile arka plan işlerini görün
10. **nohup** ile SSH kapanınca çalışmaya devam eden işlem başlatın

## Güvenli Örnekler

```bash
# Sistem yedeği almadan önce test edin
# Önce test kullanıcısı oluşturun
sudo useradd -m testuser
sudo userdel -r testuser  # İşimiz bitince silin
```

EOF
chown $STUDENT_USER:$STUDENT_USER /home/$STUDENT_USER/README.md

# Temizlik
echo "🧹 Temizlik yapılıyor..."
apt-get clean
apt-get autoclean
apt-get autoremove -y

# Önbelleği temizle
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/*
rm -rf /var/tmp/*

echo "✅ Linux eğitim ortamı hazır!"
echo ""
echo "🎓 Öğrenci kullanıcısı: $STUDENT_USER"
echo "🔑 Şifre: $STUDENT_PASS"
echo ""
echo "📚 Eğitim materyalleri: /home/$STUDENT_USER/egitim/"
echo "📖 README: /home/$STUDENT_USER/README.md"
echo ""
echo "🚀 Başlatmak için: vagrant ssh"
echo "👤 Kullanıcıya geçiş için: su - $STUDENT_USER"
