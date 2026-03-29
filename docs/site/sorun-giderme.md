# Sorun Giderme

## Chroot / Terminal

### `/bin/su` veya `/usr/bin/su` bulunamiyor

```
chroot: failed to run command '/bin/su': No such file or directory
```

**Cozum:** Chroot icerisine `su` binary'sini kopyalayin:
```bash
sudo cp /usr/bin/su /home/chroot/template/usr/bin/su
sudo chmod 4755 /home/chroot/template/usr/bin/su

# Mevcut chroot'lar icin:
for d in /home/chroot/*/; do
    if [ -d "${d}usr/bin" ]; then
        sudo rm -f "${d}usr/bin/su"
        sudo cp /usr/bin/su "${d}usr/bin/su"
        sudo chmod 4755 "${d}usr/bin/su"
    fi
done
```

### Sembolik bag seviyesi cok fazla

```
chroot: Too many levels of symbolic links
```

**Neden:** Symlink ile kopyalanmis. Chroot icindeki symlink host dosyasina isaret ediyor.
**Cozum:** `cp` kullanin, `ln -s` degil:
```bash
sudo rm -f /home/chroot/template/usr/bin/su
sudo cp /usr/bin/su /home/chroot/template/usr/bin/su
sudo chmod 4755 /home/chroot/template/usr/bin/su
```

### PTY allocation failed

```bash
sudo chroot-yonetici cleanup
sudo chroot-yonetici repair
```

### sudo-rs PTY hatasi (Ubuntu 25.10)

```
sudo-rs: cannot execute: unable to open pty
```

**Cozum:** Geleneksel sudo kurun:
```bash
echo "SIFRE" | sudo -S apt install -y sudo
```

## SSH

### Connection reset by peer

**Neden:** SSH pool socket stale kalmis.
**Cozum:** Otomatik duzeltilir (v1.9+). Manuel:
```bash
rm /tmp/ssh_pool_*
```

### SSH servisi Debian 12

Servis adi `ssh` (not `sshd`):
```bash
sudo systemctl restart ssh
```

## SEB

### SEB baglanmiyor (connection refused)

**Neden:** `.seb` config'deki URL'de port eksik.
**Cozum:** `system_host` ayarini port ile yazin (orn: `http://IP:3333`) ve `.seb` dosyasini tekrar indirin.

### SEB cikis butonu gorunmuyor

**Kontrol:**
1. Ogretmen paneli → Ayarlar → SEB Cikis Izni: Acik
2. SEB User-Agent tespiti: `SEB/` kontrolu (v679c872+)

### Kiosk kapali ama ogrenci hala SEB gerekli goruyor

Sayfa 3sn polling yaparak otomatik yonlendirir. Tarayiciyi yenileyin.

## Veritabani

### `unable to open database file`

**Neden:** `data/` dizini yok veya yazma izni yok.
**Cozum:**
```bash
mkdir -p data
chmod 755 data
```

### Test modu production DB'yi mi siler?

**Hayir** (v1.9+). Test modu sadece `test_yoklama.db` kullanir. Guvenlik kontrolu:
DB yolunda "test" yoksa islem iptal edilir.

### Backup nereden alinir?

Her baslatmada otomatik: `data/backups/yoklama_TIMESTAMP.db` (son 10 tane saklanir).

## Parallels VM

### RLIMIT hatasi

```
Failed to adjust resource limit RLIMIT_NOFILE: Operation not permitted
```

v1.8+ dusuk limitler kullanir. Eski surumde:
```bash
sudo sed -i 's/65536/4096/g; s/131072/8192/g' /etc/security/limits.d/99-chroot-terminal.conf
```

### Boot sonrasi sistem acilmiyor

**Neden:** Container tespiti yanlis — VM servisleri mask'lenmis.
**Cozum (recovery mode):**
```bash
systemctl unmask systemd-udevd.service systemd-resolved.service
systemctl enable systemd-udevd.service
rm -f /etc/systemd/system.conf.d/lxc-timeout.conf
reboot
```
v1.8+ bu sorunu duzeltmistir.
