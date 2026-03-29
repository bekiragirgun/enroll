# Ders Takip Sistemi

**Kapadokya Universitesi Linux Laboratuvari** icin gelistirilmis, gercek zamanli yoklama, slayt senkronizasyonu, sinav modulu ve izole terminal ortami saglayan kapsamli bir egitim platformudur.

## Ozellikler

- **Yoklama** — Gercek zamanli giris takibi, devam raporu, CSV export
- **Slayt Yayini** — Ogretmen slaytlarini ogrenci ekranlarinda senkronize gosterme
- **Terminal** — Chroot tabanli izole Linux ortami (her ogrenci ayri)
- **Sinav** — Coktan secmeli + terminalli (split screen) sinav
- **SEB** — Safe Exam Browser zorunlulugu ve cikis yonetimi
- **Guvenlik** — IP kontrol, sahte giris tespiti, ogrenci izleme/mudahale

## Hizli Baslangic

```bash
# Production (Docker + PostgreSQL)
docker compose up -d

# Test (SQLite)
DB_TYPE=sqlite python app.py --test --host CHROOT_IP
```

## Mimari

```
[Ogretmen Mac/PC]              [Ogrenci Tarayici/SEB]
        |                              |
        v                              v
+------------------+        +------------------+
|  Flask + SocketIO |<----->|  Polling (3s)    |
|  (app.py :3333)   |       |  ogrenci.js      |
+------------------+        +------------------+
        |
        | SSH (ControlMaster pool)
        v
+------------------+
|  Debian 12 VM    |
|  chroot-terminal |
|  deb v1.9        |
+------------------+
```

## Baglantilar

| Sayfa | URL |
|-------|-----|
| Ogrenci girisi | `http://SUNUCU_IP:3333` |
| Ogretmen paneli | `http://localhost:3333/teacher` |
| Terminal izleme | `http://localhost:3333/teacher/terminal` |
