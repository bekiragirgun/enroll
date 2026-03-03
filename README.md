# Ders Takip Sistemi

Kapadokya Üniversitesi Linux Dersleri için yoklama ve slayt kontrol sistemi.

## Kurulum (Tek seferlik)

```bash
pip3 install -r requirements.txt
```

## Kullanım

```bash
# 1. IP adresini öğren
ipconfig getifaddr en0

# 2. Sunucuyu başlat
python3 app.py

# 3. Öğrencilere söyle:
#    Tarayıcıda: http://<IP_ADRESI>:3333

# 4. Öğretmen paneli:
#    http://localhost:3333/teacher
#    Şifre: linux2024
```

## Klasör Yapısı

```
ders_takip/
├── app.py              # Ana Flask uygulaması
├── requirements.txt    # Bağımlılıklar
├── README.md           # Bu dosya
├── PROXMOX.md          # Proxmox deployment dokümantasyonu
├── templates/          # HTML şablonları
│   ├── ogrenci_giris.html
│   ├── ogrenci_ana.html
│   └── ogretmen.html
├── static/
│   ├── css/stil.css
│   └── js/
│       ├── ogrenci.js
│       └── ogretmen.js
├── data/               # SQLite DB (otomatik oluşur)
├── slaytlar/           # Marp HTML sunumlar
└── sanalmakine/        # Proxmox VM/CT yapılandırmaları
```

## Aşamalar

- [x] Faz 1: Yoklama sistemi
- [ ] Faz 2: Slayt kontrolü
- [ ] Faz 3: Ödev teslimi
