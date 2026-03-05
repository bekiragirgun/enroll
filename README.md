# Kapadokya Üniversitesi - Linux Laboratuvarı Ders Takip Sistemi

Kapadokya Üniversitesi Linux dersleri için geliştirilmiş, gerçek zamanlı yoklama, slayt senkronizasyonu ve izole terminal ortamı sağlayan kapsamlı bir eğitim platformudur.

## 🚀 Öne Çıkan Özellikler

- **İzole Chroot Terminalleri**: Her öğrenci için PCT 991 üzerinde çalışan, tamamen izole ve güvenli Linux ortamı.
- **PTY Fix & Persistence (V14)**: unprivileged LXC/Proxmox ortamları ile tam uyumlu, kalıcı ve kendi kendini onaran terminal bağlantısı.
- **Tam Linux Deneyimi**: `build-essential`, `python3`, `git`, `gcc` gibi araçlar ve genişletilmiş Ubuntu depoları (universe, multiverse) ön yüklü.
- **Zorunlu Tam Ekran**: Öğrenciler ders başladığında tam ekrana geçmeye zorlanır; tam ekrandan çıkıldığında içerik otomatik gizlenir.
- **Öğretmen Monitörü**: Öğretmenin kendi terminalinde yazdığı komutları anlık olarak öğrencilerin ekranında görüntüleme.
- **Cloudflare Access Entegrasyonu**: Güvenli erişim ve oturum süresi dolduğunda otomatik yenileme desteği.

## 🛠 Kurulum ve Dağıtım

### 1. Backend Kurulumu (Master Node)

```bash
pip3 install -r requirements.txt
python3 app.py
```

### 2. Öğrenci Node Yapılandırması (CT 991)

Öğrenci node'u üzerinde chroot şablonunu ve depoları hazırlamak için:

```bash
sudo python3 chroot_yonetici.py init
```

## 🔧 Sorun Giderme (Troubleshooting)

### Terminal Bağlantı Hatası (PTY Allocation Failed)

Eğer snapshot sonrası veya beklenmedik bir durumda terminale bağlanamazsanız, tek komutla her şeyi düzeltebilir ve kalıcı hale getirebilirsiniz:

```bash
chmod +x hizli_onarim.sh && ./hizli_onarim.sh
```

Bu komut:

- Tüm scriptleri CT 991'e senkronize eder.
- PTY ayarlarını onarır.
- Her reboot sonrası fixin kalıcı olması için systemd servisini kurar.

## 📂 Klasör Yapısı

- `app.py`: Ana Flask ve Socket.IO sunucusu.
- `chroot_yonetici.py`: Chroot ortamlarını, mount işlemlerini ve kalıcı onarımı yöneten ana modül (V14).
- `chroot_terminal.py`: Terminal bağlantılarını ve SSH tünellerini koordine eden servis.
- `hizli_onarim.sh`: Snapshot sonrası veya hata durumunda tek tuşla onarım sağlayan script.
- `templates/`: Dinamik HTML arayüzleri.
- `static/js/ogrenci.js`: Tam ekran ve polling mantığını yöneten öğrenci arayüzü.

## 🏁 Kullanım

1. **Öğretmen**: `http://sunucu-ip:3333/teacher` adresinden (Şifre: `linux2024`) dersi başlatır.
2. **Öğrenci**: Ana sayfadan giriş yapar ve "Derse Katıl" butonu ile tam ekranda dersi takip eder.
3. **Terminal**: Öğretmen terminal moduna geçtiğinde öğrencilere SSH üzerinden izole bash kabukları atanır.

---
*Kapadokya Üniversitesi - Advanced Agentic Coding Ekibi tarafından geliştirilmiştir.*
