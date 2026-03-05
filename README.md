# Kapadokya Üniversitesi - Linux Laboratuvarı Ders Takip Sistemi

Kapadokya Üniversitesi Linux dersleri için geliştirilmiş, gerçek zamanlı yoklama, slayt senkronizasyonu ve izole terminal ortamı sağlayan kapsamlı bir eğitim platformudur.

## 🚀 Öne Çıkan Özellikler

- **İzole Chroot Terminalleri**: Her öğrenci için PCT 991 üzerinde çalışan, tamamen izole ve güvenli Linux ortamı.
- **PTY Fix (V7)**: unprivileged LXC/Proxmox ortamları ile tam uyumlu, kalıcı terminal bağlantısı.
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

## 📂 Klasör Yapısı

- `app.py`: Ana Flask ve Socket.IO sunucusu.
- `chroot_yonetici.py`: Chroot ortamlarını, mount işlemlerini ve kullanıcı izinlerini yöneten ana modül (V7).
- `chroot_terminal.py`: Terminal bağlantılarını ve SSH tünellerini koordine eden servis.
- `templates/`: Dinamik HTML arayüzleri.
- `static/js/ogrenci.js`: Tam ekran ve polling mantığını yöneten öğrenci arayüzü.

## 🏁 Kullanım

1. **Öğretmen**: `http://sunucu-ip:3333/teacher` adresinden (Şifre: `linux2024`) dersi başlatır.
2. **Öğrenci**: Ana sayfadan giriş yapar ve "Derse Katıl" butonu ile tam ekranda dersi takip eder.
3. **Terminal**: Öğretmen terminal moduna geçtiğinde öğrencilere SSH üzerinden izole bash kabukları atanır.

---
*Kapadokya Üniversitesi - Advanced Agentic Coding Ekibi tarafından geliştirilmiştir.*
