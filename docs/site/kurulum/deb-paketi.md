# DEB Paketi Kurulumu (Chroot Sunucusu)

## Desteklenen Isletim Sistemleri

| OS | Durum | Not |
|----|-------|-----|
| Debian 12 (Bookworm) | Tam destek | Onerilen |
| Ubuntu 24.04 LTS | Tam destek | Alternatif |
| Ubuntu 25.10 | Sorunlu | sudo-rs PTY bug'i |

## Kurulum

```bash
git clone https://github.com/bekiragirgun/enroll.git
cd enroll/deb-package

# Paketi olustur
bash build.sh

# Kur (bagimliliklar otomatik indirilir)
sudo apt install ./chroot-terminal_1.9.deb
```

## Ilk Kurulum Sonrasi

```bash
# Chroot sablonu olustur (ilk sefer, ~10dk)
sudo chroot-yonetici init

# Saglik kontrolu
sudo chroot-yonetici health
```

## Paket Icerigi (v1.9)

| Dosya | Aciklama |
|-------|----------|
| `/usr/local/bin/chroot-yonetici` | Ana yonetim scripti |
| `/etc/sysctl.d/99-pty-limits.conf` | Kernel optimizasyonu (PTY, fd, TCP) |
| `/etc/security/limits.d/99-chroot-terminal.conf` | ulimit ayarlari |
| `/etc/ssh/sshd_config.d/chroot-terminal.conf` | SSH optimizasyonu |
| `/etc/systemd/system/chroot-pty-fix.service` | Boot'ta PTY onarimi |
| `/etc/systemd/system/chroot-cleanup.timer` | 10dk'da temizlik |

## chroot-yonetici Komutlari

```bash
chroot-yonetici init           # Sablon olustur
chroot-yonetici create <user>  # Ogrenci chroot olustur
chroot-yonetici list           # Listele
chroot-yonetici mount <user>   # Mount et
chroot-yonetici delete <user>  # Sil
chroot-yonetici repair         # PTY onar
chroot-yonetici cleanup        # Zombie/stale temizligi
chroot-yonetici health         # Saglik raporu
```

## Bilinen Sorunlar

!!! danger "Debian 12: /usr/bin/su"
    Debian 12'de `su` komutu `/usr/bin/su` konumundadir (Ubuntu: `/bin/su`).
    v1.9'da otomatik olarak chroot'a kopyalanir.
    Eski surumlerde manual kopyalama gerekir:
    ```bash
    sudo cp /usr/bin/su /home/chroot/template/usr/bin/su
    sudo chmod 4755 /home/chroot/template/usr/bin/su
    ```

!!! warning "Parallels VM"
    Parallels VM'de yuksek RLIMIT degerler reddedilir.
    v1.8+ dusuk degerler kullanir (nofile 4096/8192).
    Container tespiti v1.8+'da duzeltildi — VM'ler korunur.
