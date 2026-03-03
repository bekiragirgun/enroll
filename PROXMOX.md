# Proxmox Linux Eğitim Ortamı Kurulum Rehberi

Bu rehber, Kapadokya Linux eğitim ortamını Proxmox VE'ye taşımak için hazırlanmıştır.

## 🎯 Özet

Projenizi Proxmox'a aktararak:
- ✅ Tam Linux sistemi (systemd dahil)
- ✅ Tüm network ve sistem araçları
- ✅ Öğrenci hesabı ve eğitim materyalleri
- ✅ Kalıcı ve stabil çalışma ortamı

## 📋 Gereksinimler

- Proxmox VE kurulu bir sunucu
- VM için kaynaklar (2GB RAM, 2 CPU, 20GB disk yeterli)
- Debian 12 veya Ubuntu 22.04 ISO dosyası

## 🚀 Kurulum Adımları

### Adım 1: VM Oluştur

Proxmox web arayüzünde:

1. **VM Oluştur:**
   - Sol menüden "Create VM" tıklayın
   - **General:**
     - Name: `linux-egitim`
     - VM ID: Otomatik (boş bırakın)
     - BIOS Type: OVMF (UEFI) - ARM64 için gerekli

2. **OS:**
   - **Type:** Linux
   - **Version:** Debian 12 Bookworm (ARM64)
   - ISO: Yüklediğiniz Debian/Ubuntu ISO'yu seçin

3. **Hard Disk:**
   - **Bus/Device:** VirtIO
   - **Storage:** Local-lvm veya uygun storage
   - **Disk size:** 20G (veya daha fazla)
   - **SSD emulation:** İşaretleyin

4. **CPU:**
   - **Type:** ARM64 (Apple Silicon için)
   - **Cores:** 2 (veya daha fazla)
   - **Type:** Host

5. **Memory:**
   - **Memory:** 2048 MB (2GB)

6. **Network:**
   - **Device:** VirtIO (paravirtualized)
   - **Bridge:** vmbr0
   - **Firewall:** Off (sonra açabilirsiniz)
   - **VLAN ID:** Boş

7. **Confirm:** Review edip "Finish" tıklayın

### Adım 2: VM'i Başlat ve Kurulum Yap

1. VM'i seçin ve **Start** tıklayın
2. **Console** butonuna tıklayın
3. Debian/Ubuntu kurulumunu yapın:
   - Language: English (veya Turkish)
   - Location: Turkey
   - Keyboard: Turkish
   - Hostname: `linux-egitim`
   - Domain: (boş bırakın)
   - User: Sadece root kullanacağız (user oluşturmayın)
   - Partition: Guided - use entire disk
   - SSH: OpenSSH server kurun
   - Software: Standard system utilities

### Adım 3: İlk Kurulum

VM kurulduktan sonra console'da:

```bash
# Root girişi yapın (şifre belirlediyseniz)

# Sistem güncelle
apt update && apt upgrade -y

# Temel araçlar
apt install -y curl wget vim git sudo

# SSH erişimi için IP öğrenin
ip addr show
```

Bu IP adresini not alın.

### Adım 4: provision.sh'ı İçeri Aktarın

Yöntem 1 - SSH ile:

```bash
# Ana makinenizden Proxmox VM'e SSH ile bağlanın
ssh root@<VM_IP_ADRESI>

# provision.sh dosyasını oluşturun
cat > /root/provision.sh << 'EOFPROVISION'
[provision.sh dosyasının içeriğini buraya yapıştırın]
EOFPROVISION

# Çalıştırılabilir yapın
chmod +x /root/provision.sh

# Çalıştırın
bash /root/provision.sh
```

Yöntem 2 - Direct Console:

Proxmox console'dan direkt provision.sh içeriğini yapıştırın.

### Adım 5: provision.sh'ı Çalıştırın

```bash
# VM içinde
cd /root
bash provision.sh
```

Bu işlem 5-10 dakika sürecek, 100+ paket kuracak.

## 🎯 VM Hazır Olduğunda

```bash
# Öğrenci kullanıcısına geçin
su - ogrenci
# Şifre: ogrenci

# Test edin
sysinfo
which ip tcpdump nmap ufw systemctl
```

## 🌐 VM'e Erişim

### SSH ile Bağlanma

```bash
# Ana makineden
ssh root@<VM_IP_ADRESI>

# Öğrenci kullanıcısı ile
ssh ogrenci@<VM_IP_ADRESI>
```

### Web Arayüzü

Proxmox web arayüzünden:
- VM: Console butonu ile
- Network: 22 portuna erişim

## 📚 Eğitim Kullanımı

### Öğrenci Girişi

```bash
ssh ogrenci@<VM_IP_ADRESI>
# Şifre: ogrenci

cd ~/egitim/
ls -la
./network-egzersizleri.sh
./process-egzersizleri.sh
```

### Sistem Bilgisi

```bash
sysinfo  # Özel komut
ip addr
df -h
free -h
```

## 🔧 Otomasyon Seçenekleri

### Cloud-Init Kullanırsanız

Proxmox Cloud-Init ile otomatik kurulum:

1. **CICustom:** provision.sh'ı yükleyin
2. **First Boot:** Otomatik çalışır
3. **Network:** Otomatik IP alır

### Yedekleme

**VM Snapshot:**
```bash
# Proxmox web arayüzünde
1. VM seçin
2. Backup -> Snapshot
3. Adını girin (örn: "temel-kurulum")
4. Snapshot alın
```

**SSH Key:**
```bash
# SSH anahtarı oluştur
ssh-keygen -t rsa -b 4096

# Public key'i VM'e kopyala
ssh-copy-id root@<VM_IP_ADRESI>
```

## 🎓 Kullanım Senaryoları

### Ders İçin

1. **Öğrenci erişimi:** SSH ile bağlanma
2. **Eğitim materyalleri:** ~/egitim/
3. **Pratik:** ~/pratik/
4. **Test:** ~/testler/

### Eğitmen İçin

1. **VM yönetimi:** Proxmox web arayüzü
2. **Snapshot yönetimi:** Ders öncesi/sonrası
3. **Resource monitoring:** Proxmox dashboard
4. **Log erişimi:** ~/loglar/

## 📊 Kaynak Kullanımı

**Minimum:**
- RAM: 2GB
- CPU: 2 çekirdek
- Disk: 20GB

**Önerilen:**
- RAM: 4GB
- CPU: 4 çekirdek
- Disk: 40GB

## 🔐 Güvenlik

### Firewall

```bash
# VM içinde
ufw enable
ufw allow ssh
ufw allow from 192.168.1.0/24  # Yerel ağa izin ver
```

### SSH Güvenliği

```bash
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no

# Reload
systemctl restart sshd
```

## 🐛 Sorun Giderme

### VM Başlamıyor

- BIOS Type: OVMF (UEFI) kontrol edin
- ISO dosyası doğru seçilmiş mi?
- CPU Type: ARM64 kontrol edin

### Network Çalışmıyor

- Bridge: vmbr0 kontrol edin
- Firewall kapalı mı kontrol edin
- VLAN ID boş bırakın

### Provision Çalışmıyor

- Console'dan manuel çalıştırın
- Hata mesajını kontrol edin
- İnternet bağlantısını kontrol edin: `ping google.com`

## 📞 Destek

Eğer sorun yaşarsanız:
1. Proxmox loglarını kontrol edin
2. VM console çıktısını inceleyin
3. Network ayarlarını doğrulayın

## 🎉 Başarılar!

Artık Linux eğitim ortamınız Proxmox'ta çalışıyor!
