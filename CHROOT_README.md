# Chroot + PAM Terminal Sistemi

## 🎯 Özellikler

Her öğrenci için **izole chroot ortamı**:
- ✅ Öğrenci kendi ortamında `sudo su -` ile root olabilir
- ✅ Gerçek sistem korunur, öğrenci sadece kendi chroot'unu bozabilir
- ✅ DNS filtering (sosyal medya, haber siteleri engelli)
- ✅ Hafif ve performanslı (Docker'a göre daha az kaynak)
- ✅ Proxmox LXC için ideal

## 🔒 Güvenlik Modeli

```
┌─────────────────────────────────────────────────────┐
│ Host Sistem (Proxmox LXC)                          │
│ ├─ /home/chroot/ogrenci1/  (Öğrenci1 için "/")     │
│ ├─ /home/chroot/ogrenci2/  (Öğrenci2 için "/")     │
│ └─ /home/chroot/ogrenci3/  (Öğrenci3 için "/")     │
└─────────────────────────────────────────────────────┘

Öğrenci1: ssh ogrenci1@server
  → chroot(/home/chroot/ogrenci1)
  → sudo su -  # Sadece kendi chroot'unda root
  → rm -rf /  # Sadece kendi ortamını siler
```

## 📦 Kurulum (Proxmox LXC)

### 1. Proxmox'ta LXC Container Oluştur

```bash
# Debian 11 template ile LXC container
pct create 100 local:vztmpl/debian-11-standard_11.3-1_amd64.tar.zst \
  --storage local-lvm \
  --cores 8 \
  --memory 32768 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.100/24,gw=192.168.1.1

# Container'ı başlat
pct start 100

# Container'a gir
pct enter 100
```

### 2. Deploy Script'i Çalıştır

```bash
# Proxmox LXC container içinde
cd /root
wget https://github.com/.../proxmox-chroot-deploy.sh  # Veya manuel kopyala
chmod +x proxmox-chroot-deploy.sh
./proxmox-chroot-deploy.sh
```

### 3. Öğrenci Ekle

```bash
python3 chroot_yonetici.py create ahmetyilmaz220001001
python3 chroot_yonetici.py create ayseedemir220001002
python3 chroot_yonetici.py create mehmetkaya220001003
```

### 4. Öğrenci SSH ile Bağlanır

```bash
# Öğrenci kendi bilgisayarından:
ssh -p 2222 ahmetyilmaz220001001@<server_ip>
# Şifre: ahmetyilmaz220001001

# İçinde root olabilir:
[ahmetyilmaz220001001@linux1]$ sudo su -
[root@linux1]#
```

## 🚀 Özellikler

### İçerik Filtreleme
- **DNS Level**: CleanBrowsing Family Shield (185.228.168.168)
- **Hosts Dosyası**: Sosyal medya ve haber siteleri doğrudan engelli
- Engelli siteler: Facebook, Twitter, Instagram, TikTok, YouTube, Reddit, CNN, BBC, NYT, Hürriyet, Milliyet, Sözcü, vs.

### Öğrenci Yetkileri
| Yetki | Açıklama |
|-------|----------|
| Normal kullanıcı | Kendi dosyalarını yönetebilir |
| `sudo su -` | Kendi chroot'unda **root** olur |
| Host sistemi | ❌ Erişim yok |
| Diğer öğrenciler | ❌ Erişim yok |

## 🔧 Yönetim Komutları

```bash
# Tüm öğrencileri listele
python3 chroot_yonetici.py list

# Yeni öğrenci ekle
python3 chroot_yonetici.py create <kullanıcı_adı>

# Öğrenci chroot'unu mount et
python3 chroot_yonetici.py mount <kullanıcı_adı>

# Öğrenci sil
python3 chroot_yonetici.py delete <kullanıcı_adı>

# Öğrenci sayısı
ls -1 /home/chroot/ | grep -v template | wc -l
```

## 📊 Kaynak Kullanımı

| Öğrenci Sayısı | RAM (MB/öğrenci) | Toplam RAM | CPU (core/öğrenci) | Toplam CPU |
|---------------|------------------|------------|-------------------|------------|
| 30            | 256              | 7.7 GB     | 0.2               | 6 cores    |
| 45            | 256              | 11.5 GB    | 0.2               | 9 cores    |
| 60            | 256              | 15.4 GB    | 0.2               | 12 cores   |

*Chroot çok hafiftir, Docker container'a göre ~50% daha az kaynak kullanır*

## 🔄 Backup ve Restore

```bash
# Tüm chroot ortamlarını yedekle
tar czf chroot_backup_$(date +%Y%m%d).tar.gz /home/chroot/

# Tek öğrenciyi yedekle
tar czf ogrenci1_backup.tar.gz /home/chroot/ogrenci1/

# Geri yükle
tar xzf chroot_backup_20260303.tar.gz -C /
```

## 🐛 Troubleshooting

### Öğrenci chroot'tan çıkamaz
```bash
# Mount'ları kontrol et
mount | grep ogrenci1

# Elle mount et
python3 chroot_yonetici.py mount ogrenci1
```

### SSH bağlantısı başarısız
```bash
# SSH loglarını kontrol et
tail -f /var/log/auth.log

# Chroot dizinini kontrol et
ls -la /home/chroot/ogrenci1/
```

### Öğrenci sudo yapamıyor
```bash
# Chroot içinde sudoers dosyasını kontrol et
cat /home/chroot/ogrenci1/etc/sudoers

# Doğru içerik:
# ogrenci1 ALL=(ALL:ALL) NOPASSWD:ALL
```

## 📚 Dokümantasyon

- Chroot nedir: `man chroot`
- PAM authentication: `man pam_chroot`
- SSH ForceCommand: `man sshd_config`

## 🎓 Eğitim İçin Ideal

- ✅ Gerçek Linux deneyimi
- ✅ Root erişimi (güvenli ortamda)
- ✅ Sistemi bozma özgürlüğü
- ✅ Diğer öğrencileri etkileme riski yok
- ✅ Öğretmen kolayca reset yapabilir
- ✅ Ders sonunda tüm ortamı silip baştan başlayabilir

## 🔐 Güvenlik Notları

1. **Chroot Escape**: Öğrenci host sistemde root yetkisi olmadığı için chroot'tan çıkamaz
2. **Sudo Kısıtlama**: Öğrenci sadece kendi chroot'unda sudo kullanabilir
3. **Network İzolasyonu**: İsteğe bağlı olarak her öğrenci için network namespace
4. **Resource Limits**: `ulimit` ile kaynak kısıtlaması yapılabilir

## 📧 İletişim

Sorularınız için: bpg106@kapadokya.edu.tr
