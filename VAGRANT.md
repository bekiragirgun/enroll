# Linux Eğitim Ortamı - Vagrant Kurulum Kılavuzu

Bu ortam, Linux sistem yönetimi eğitimi için tam özellikli bir Debian 12 sanal makinesi sağlar.

## 🔑 Gereksinimler

### VirtualBox Kurulumu

Vagrant çalışmak için VirtualBox gerektirir:

```bash
# macOS (Homebrew ile)
brew install --cask virtualbox

# Veya indir: https://www.virtualbox.org/wiki/Downloads
```

### Vagrant Kurulumu

```bash
# macOS (Homebrew ile)
brew install vagrant

# Veya indir: https://developer.hashicorp.com/vagrant/downloads
```

Kurulumu kontrol edin:

```bash
vagrant --version
vboxmanage --version
```

## 🚀 Hızlı Başlangıç

### 1. VM'i Başlatma

```bash
# VM'i oluşturun ve başlatın
vagrant up

# İlk başlatma 5-10 dakika sürebilir (indirme + kurulum)
```

### 2. VM'e Bağlanma

```bash
# SSH ile bağlanın
vagrant ssh

# Öğrenci kullanıcısına geçin
su - ogrenci
# Şifre: ogrenci
```

### 3. VM'i Durdurma

```bash
# VM'i durdur (ayarları korur)
vagrant halt

# VM'i sil (tüm veriler silinir)
vagrant destroy
```

## 📚 Eğitim İçerikleri

VM hazırlandığında `/home/ogrenci/egitim/` dizininde şu egzersiz script'leri bulacaksınız:

| Script | Konu |
|--------|------|
| `network-egzersizleri.sh` | Network komutları ve araçları |
| `process-egzersizleri.sh` | Process yönetimi ve monitoring |
| `kullanici-egzersizleri.sh` | Kullanıcı ve grup yönetimi |
| `servis-egzersizleri.sh` | Systemd ve servis yönetimi |
| `disk-egzersizleri.sh` | Disk ve dosya sistemi yönetimi |

## 🎯 Öğrenci Hesabı

```
Kullanıcı: ogrenci
Şifre: ogrenci
Sudo: Şifresiz
Home: /home/ogrenci
Shell: /bin/bash
```

## 🌐 Network Erişimi

VM'de iki network arayüzü vardır:

1. **NAT** - İnternet erişimi için (otomatik)
2. **Private Network** - Host'tan erişim için (DHCP)

Host'tan VM'e erişmek için:

```bash
# VM IP adresini bulun
vagrant ssh
ip addr show eth1
```

## 📂 Paylaşılan Dizin

Host sisteminizdeki `./shared` dizini VM içinde `/home/ogrenci/shared` olarak erişilebilir:

```bash
# Host tarafında
echo "Test dosyası" > shared/test.txt

# VM içinde (ogrenci kullanıcısı ile)
cat ~/shared/test.txt
```

## 🛠️ Yaygın Vagrant Komutları

```bash
vagrant up          # VM'i başlat
vagrant ssh         # VM'e bağlan
vagrant halt        # VM'i durdur
vagrant reload      # VM'i yeniden başlat
vagrant status      # VM durumunu göster
vagrant destroy     # VM'i sil
vagrant suspend     # VM'i askıya al (save state)
vagrant resume      # Askıya alınan VM'i devam ettir
```

## 🔧 VM Yapılandırması

VM şu özelliklerle oluşturulur:

- **OS:** Debian 12 Bookworm (64-bit)
- **RAM:** 2GB
- **CPU:** 2 çekirdek
- **Disk:** Dinamik (varsayılan 10GB)
- **Network:** NAT + Private Network (DHCP)

Yapılandırmayı değiştirmek için `Vagrantfile` dosyasını düzenleyin, sonra:

```bash
vagrant reload
```

## 📦 Yüklü Araçlar

### Temel Sistem Araçları
- `vim`, `nano`, `mcedit` - Editörler
- `htop`, `btop`, `iotop` - Monitoring
- `tmux`, `screen` - Terminal multiplexer'ler
- `tree`, `file`, `less` - Dosya araçları

### Network Araçları
- `iproute2`, `net-tools` - Network komutları
- `nmap`, `tcpdump` - Network analizi
- `traceroute`, `whois` - Network teşhisi
- `iptables`, `nftables` - Firewall
- `bind9-dnsutils` - DNS araçları

### Sistem Yönetimi
- `systemd` - Init system ve servis yönetimi
- `cron` - Zamanlanmış görevler
- `rsyslog` - Log yönetimi
- `logrotate` - Log rotasyonu

### Geliştirme Araçları
- `build-essential` - Derleme araçları
- `git`, `subversion` - Versiyon kontrol
- `python3`, `perl`, `php` - Script dilleri
- `nodejs`, `npm` - JavaScript runtime
- `golang`, `rust` - Derleme dilleri

### Web Sunucular
- `apache2` - Apache HTTP Server
- `nginx-light` - Nginx
- `lighttpd` - Hafif web sunucu

### Veritabanı Client'leri
- `sqlite3` - SQLite
- `postgresql-client` - PostgreSQL
- `mysql-client` - MySQL/MariaDB
- `redis-tools` - Redis

### Güvenlik Araçları
- `ufw` - Uncomplicated Firewall
- `fail2ban` - Intrusion prevention
- `rkhunter`, `chkrootkit` - Rootkit detection
- `auditd` - Audit daemon

## 🎓 Öğrenme Yol Haritası

### 1. Temel Komutlar (1. Hafta)
```bash
ls, cd, pwd, mkdir, rmdir, rm, cp, mv
cat, less, tail, head, grep
find, locate
man, --help
```

### 2. Kullanıcı Yönetimi (2. Hafta)
```bash
useradd, usermod, userdel
groupadd, gpasswd
/etc/passwd, /etc/shadow, /etc/group
sudo, visudo
```

### 3. Process Yönetimi (3. Hafta)
```bash
ps, top, htop, kill, killall
bg, fg, jobs, nohup
/proc filesystem
```

### 4. Network Temelleri (4. Hafta)
```bash
ip addr, ip route, ip link
ping, traceroute, mtr
ss, netstat
iptables
```

### 5. Servis Yönetimi (5. Hafta)
```bash
systemctl
journalctl
service unit dosyaları
cron
```

### 6. Disk ve Dosya Sistemleri (6. Hafta)
```bash
df, du, lsblk, mount
fdisk, parted
ext4, xfs, btrfs
LVM, RAID
```

### 7. Log Yönetimi (7. Hafta)
```bash
/var/log/
rsyslog
journalctl
logrotate
```

### 8. Güvenlik (8. Hafta)
```bash
ufw, fail2ban
ssh anahtarlar
sudo yapılandırması
permissions
```

## 🐛 Sorun Giderme

### VM başlamıyor

```bash
# VirtualBox'ın çalıştığından emin olun
vboxmanage --version

# Vagrant loglarını kontrol edin
vagrant up --debug 2>&1 | tee vagrant.log
```

### Network çalışmıyor

```bash
# VM içinde network ayarlarını kontrol edin
vagrant ssh
ip addr show
ip route show

# Network servisini yeniden başlatın
sudo systemctl restart networking
```

### Yetersiz RAM/CPU

`Vagrantfile` dosyasını düzenleyin:

```ruby
vb.memory = 4096  # 4GB RAM
vb.cpus = 4        # 4 CPU
```

Sonra yeniden başlatın:

```bash
vagrant reload
```

### Disk yetersiz

VirtualBox'ta disk boyutunu artırın:

```bash
vagrant halt
vboxmanage modifyhd disk.vdi --resize 20480  # 20GB
vagrant up
```

## 📞 Yardım

Eğer sorun yaşarsanız:

1. `vagrant up` çıktısını dikkatlice okuyun
2. `Vagrantfile` sözdizimini kontrol edin
3. VirtualBox ve Vagrant sürümlerini güncelleyin
4. [Vagrant dokümantasyonu](https://developer.hashicorp.com/vagrant/docs)
5. [VirtualBox forumları](https://forums.virtualbox.org/)

## 🎉 Başarılar!

Bu eğitim ortamı Linux sistem yönetimi için güvenli ve esnek bir ortam sağlar. Öğrenme yolculuğunuzda iyi şanslar!

---
**Not:** Bu VM sadece eğitim amaçlıdır. Production ortamlarında kullanmayın.
