# TTYD Güvenli Kurulum Rehberi

## 🎯 Güvenli Kullanım İçin 3 Seçenek

### Seçenek 1: Pure Readonly (En Güvenli - Önerilen)

```bash
# Öğretmen terminalinde:
ttyd --port 7681 bash

# Varsayılan olarak READONLY!
# Öğrenci sadece izler, yazamaz.
# Öğretmen de bu terminalde gösteri yapar.
```

**Kullanım:**
- Öğretmen TTYD'de demonstrasyon yapar
- Öğrenciler izler
- Pratik için öğrenciler KENDİ terminalini kullanır

---

### Seçenek 2: Credential Protected (Korumalı Erişim)

```bash
# Öğretmen terminalinde:
ttyd --port 7681 --credential ogretmen:sifre123 bash
```

**Kullanım:**
- TTYD'ye erişmek için şifre gerekir
- Şifreyi sadece ÖĞRETMEN bilir
- Öğrenciler şifreyi bilmezse TTYD'yi göremez
- Şifreyi asla öğrencilerle paylaşma!

**Not:** Şifreyi bilen herkes yazabilir. READONLY kalmaz.

---

### Seçenek 3: İki Ayrı TTYD (Gelişmiş)

```bash
# Terminal 1: Öğrenciler için (readonly)
ttyd --port 7681 bash

# Terminal 2: Öğretmen için (writable, farklı port)
ttyd --port 7682 --writable --credential admin:secret bash
```

**Kullanım:**
- Port 7681: Öğrenciler için (readonly)
- Port 7682: Öğretmen için (writable)
- Öğretmen panelinde sadece 7681 gösterilir

---

## 🚀 Hızlı Başlangıç

### En Basit Güvenli Kurulum:

```bash
# 1. TTYD'yi başlat
ttyd --port 7681 bash

# 2. Flask'i başlat
python3 app.py

# 3. Öğretmen paneli
http://localhost:3333/teacher
→ Terminal URL: http://localhost:7681
→ "💻 Terminal" butonuna tıkla

# 4. Öğrenci
http://localhost:3333
→ Giriş yap
→ TTYD'yi görür (sadece izler)
```

---

## ⚠️ Güvenlik Kuralları

1. **ASLA `--writable` flag kullanma** (öğrenci varsa)
2. **ASLA credential şifresini öğrencilerle paylaşma**
3. **Varsayılan readonly mod her zaman için yeterli**
4. **Pratik için öğrenciler kendi terminalini kullansın**

---

## 🎓 Ders Akışı Örneği

1. **Teori (15 dk)**
   - Öğretmen: Slaytları gösterir (`📽 Slayt` modu)
   - Öğrenci: Not alır

2. **Demonstrasyon (10 dk)**
   - Öğretmen: TTYD'de komutları gösterir (`💻 Terminal` modu)
   - Öğrenci: İzler (readonly, yazamaz)

3. **Pratik (25 dk)**
   - Öğretmen: `⏸ Beklet` moduna geçer
   - Öğrenci: KENDİ terminalinde uygulama yapar
   - Öğretmen: Dolaşır, yardımcı olur

4. **Yoklama**
   - Sistem otomatik kaydeder

---

**Özet:** TTYD credential kullanabilirsin ama şifreyi asla öğrencilerle paylaşma! Varsayılan readonly mod yeterli.
