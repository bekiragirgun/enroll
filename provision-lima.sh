#!/bin/bash
set -e

echo "🐧 Lima Linux eğitim ortamı hazırlanıyor..."

# Sistem güncellemesi
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade -y

# Network araçları
echo "🌐 Network araçları kuruluyor..."
apt-get install -y \
    iproute2 \
    iputils-ping \
    traceroute \
    net-tools \
    dnsutils \
    netcat \
    nmap \
    tcpdump \
    curl \
    wget \
    openssh-server \
    openssh-client \
    telnet \
    rsync \
    iptables \
    nftables \
    ethtool \
    mtr-tiny \
    bind9-dnsutils \
    conntrack

# Sistem yönetimi
echo "⚙️  Sistem yönetimi araçları kuruluyor..."
apt-get install -y \
    systemd \
    cron \
    rsyslog \
    logrotate \
    acl \
    fdisk \
    gdisk \
    parted \
    lvm2 \
    util-linux \
    smartmontools \
    lshw \
    pciutils \
    usbutils

# Process monitoring
echo "📊 Process monitoring araçları kuruluyor..."
apt-get install -y \
    procps \
    lsof \
    strace \
    sysstat \
    htop \
    btop \
    iotop \
    glances

# Geliştirme araçları
echo "👨‍💻 Geliştirme araçları kuruluyor..."
apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    git \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv

# Web sunucu
echo "🌍 Web sunucu kuruluyor..."
apt-get install -y \
    apache2 \
    nginx-light \
    sqlite3

# Güvenlik
echo "🔒 Güvenlik araçları kuruluyor..."
apt-get install -y \
    ufw \
    fail2ban \
    rkhunter \
    openssl

# Diğer araçlar
echo "🛠️  Diğer araçlar kuruluyor..."
apt-get install -y \
    zip \
    unzip \
    tar \
    gzip \
    bzip2 \
    tree \
    vim \
    nano \
    tmux \
    screen \
    man-db \
    less

# Servisleri başlat
echo "🎯 Servisler başlatılıyor..."
systemctl enable ssh
systemctl enable cron
systemctl enable rsyslog
systemctl start ufw || true

# Öğrenci kullanıcısı
echo "👤 Öğrenci kullanıcısı oluşturuluyor..."
if ! id ogrenci &>/dev/null; then
    useradd -m -s /bin/bash -G sudo,diallog,cdrom,floppy,audio,dip,video,plugdev,netdev adm ogrenci
    echo "ogrenci:ogrenci" | chpasswd
    echo "ogrenci ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/ogrenci
    chmod 440 /etc/sudoers.d/ogrenci
fi

# Bash yapılandırması
echo "📝 Bash yapılandırması ayarlanıyor..."
cat >> /home/ogrenci/.bashrc << 'EOF'

# Linux eğitim ortamı
export EDITOR=vim
export VISUAL=vim
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTTIMEFORMAT="%F %T "
shopt -s histappend
shopt -s cmdhist

# Renkli prompt
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

# Aliaslar
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias grep='grep --color=auto'
alias df='df -h'
alias du='du -h'
alias free='free -h'
alias ip='ip -color=auto'
alias journalctl='journalctl --no-pager'
alias systemctl='systemctl --no-pager'

# Sistem bilgisi
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

EOF

chown ogrenci:ogrenci /home/ogrenci/.bashrc

# Dizinler oluşturma
echo "📁 Dizinler oluşturuluyor..."
mkdir -p /home/ogrenci/{egitim,pratik,testler,loglar,shared}
chown -R ogrenci:ogrenci /home/ogrenci

# Temizlik
echo "🧹 Temizlik yapılıyor..."
apt-get clean
rm -rf /var/lib/apt/lists/*

echo "✅ Lima Linux eğitim ortamı hazır!"
echo ""
echo "🎓 Öğrenci: ogrenci / ogrenci"
echo "📚 Eğitim: /home/ogrenci/egitim/"
