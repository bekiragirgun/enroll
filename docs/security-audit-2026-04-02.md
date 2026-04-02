# Güvenlik Denetim Raporu — Ders Takip Sistemi

**Tarih:** 2026-04-02
**Araç:** Manuel kod analizi + Trivy v0.69.3
**Kapsam:** Tüm .py, .js, .html, .sh, .yml, .env dosyaları

---

## Özet

| Seviye | Sayı |
|--------|------|
| CRITICAL | 2 |
| HIGH | 9 |
| MEDIUM | 12 |
| LOW | 9 |
| **TOPLAM** | **32** |

---

## CRITICAL

### C1 — Hardcoded SECRET_KEY (Session Forgery)
- **Dosya:** `app.py:41`, `.env:1`
- **Açıklama:** `SECRET_KEY = 'kapadokya-linux-2024'` hardcoded. Bu anahtarı bilen herkes Flask session cookie'si forge edebilir, öğretmen yetkisi alabilir.
- **Düzeltme:** Kriptografik random key üret (`python -c "import secrets; print(secrets.token_hex(32))"`), sadece environment variable'dan oku, fallback kaldır. `.env`'yi git history'den temizle.

### C2 — SQL Injection (migrate_to_pg.py)
- **Dosya:** `migrate_to_pg.py:25,30,43`
- **Açıklama:** f-string ile SQL sorgusu oluşturuluyor. Migration scripti olduğu için risk düşük ama pattern tehlikeli.
- **Düzeltme:** Tablo/kolon isimlerini allowlist ile doğrula.

---

## HIGH

### H1 — SocketIO Terminal — Kimlik Doğrulama Yok
- **Dosya:** `app.py:216-220, 361-365`
- **Açıklama:** `ogretmen_baglan` ve `ogrenci_baglan` SocketIO eventleri session kontrolü yapmıyor. Herhangi bir WebSocket client öğretmen terminali açabilir.
- **Düzeltme:** `session.get('ogretmen')` ve `session.get('numara')` kontrolü ekle.

### H2 — CSRF Koruması Yok
- **Dosya:** Tüm route dosyaları
- **Açıklama:** Hiçbir form veya API endpoint'inde CSRF token yok. Kötü niyetli bir sayfa, aktif session'ı olan öğretmenin tarayıcısından yoklama silme, ayar değiştirme gibi işlemler yapabilir.
- **Düzeltme:** `flask-wtf` kur, `CSRFProtect(app)` aktifleştir, formlara `{{ csrf_token() }}` ekle.

### H3 — DEBUG Print ile Şifre Sızıntısı
- **Dosya:** `routes/teacher.py:18`
- **Açıklama:** `print(f"DEBUG: Login attempt - Input: '{pw_input}', Expected: '{pw_expected}'")` — her login denemesinde öğretmen şifresi stdout'a yazılıyor.
- **Düzeltme:** Bu satırı tamamen sil.

### H4 — Şifreler Düz Metin Olarak Saklanıyor
- **Dosya:** `routes/teacher.py`, `core/config.py`
- **Açıklama:** Öğretmen ve öğrenci şifreleri hash'lenmeden DB'ye yazılıyor.
- **Düzeltme:** `werkzeug.security.generate_password_hash()` / `check_password_hash()` kullan.

### H5 — Hardcoded Varsayılan Şifreler
- **Dosyalar:** `routes/teacher.py:6` (`linux2024`), `core/db.py:31` (`postgres_pass`), `docker-compose.yml:7`
- **Düzeltme:** Varsayılan fallback kaldır, env var zorunlu yap, yoksa hata ver.

### H6 — .env Dosyası Git'te
- **Dosya:** `.env`
- **Açıklama:** `.gitignore`'da olmasına rağmen daha önce commit edilmiş, history'de mevcut.
- **Düzeltme:** `git rm --cached .env`, tüm secret'ları rotate et.

### H7 — Teacher Login'de Brute-Force Koruması Yok
- **Dosya:** `routes/teacher.py:13-22`
- **Düzeltme:** `flask-limiter` ile rate limiting ekle.

### H8 — Stored XSS (innerHTML ile Sınav Verisi)
- **Dosya:** `static/js/ogrenci.js:208-230`
- **Açıklama:** Sınav soru metni ve seçenekler `innerHTML` ile render ediliyor. `<img src=x onerror="alert(1)">` gibi bir soru metni tüm öğrencilerde JS çalıştırır.
- **Düzeltme:** `textContent` kullan veya HTML entity escape fonksiyonu ekle.

### H9 — Chroot İçinde NOPASSWD sudo ALL
- **Dosya:** `chroot_yonetici.py:428`
- **Açıklama:** Chroot escape zafiyeti varsa öğrenci host'ta root olabilir.
- **Düzeltme:** sudo yetkisini sadece gereken komutlara kısıtla.

---

## MEDIUM

### M1 — Öğrenci Numarası = Şifre
- **Dosya:** `routes/student.py:91-107`
- **Düzeltme:** Ayrı şifre alanı + hash.

### M2 — SSH Şifresi Komut Satırında (`sshpass -p`)
- **Dosya:** `chroot_terminal.py:145,249,292,362`
- **Düzeltme:** `sshpass -e` (env var) veya SSH key kullan.

### M3 — Öğrenci Listesi API'si Kimliksiz Erişilebilir
- **Dosya:** `routes/api.py:263-267`
- **Düzeltme:** Auth decorator ekle.

### M4 — Chroot Şifresi = Kullanıcı Adı
- **Dosya:** `chroot_terminal.py:628`
- **Düzeltme:** Random şifre veya SSH key.

### M5 — /api/durum Kimliksiz State Değişikliği
- **Dosya:** `routes/api.py:15-19`
- **Düzeltme:** Hash parametresini kaldır veya auth ekle.

### M6 — innerHTML Kullanımı (Öğretmen Paneli)
- **Dosya:** `static/js/ogretmen.js` (çok sayıda yer)
- **Düzeltme:** textContent veya escape fonksiyonu.

### M7 — Shell String Concatenation (Command Injection Riski)
- **Dosya:** `app.py:248-258`, `chroot_terminal.py:487-494`
- **Düzeltme:** `subprocess.run()` ile liste argümanları kullan, `shell=True` kaldır.

### M8 — SocketIO CORS Açık (`*`)
- **Dosya:** `app.py:74`
- **Düzeltme:** Gerçek origin ile kısıtla.

### M9 — Docker Container Root Olarak Çalışıyor
- **Dosya:** `Dockerfile`
- **Düzeltme:** `USER appuser` ekle.

### M10 — Tüm Proje Dizini Container'a Mount
- **Dosya:** `docker-compose.yml:30`
- **Düzeltme:** Sadece gerekli dizinleri mount et.

### M11 — PostgreSQL Tüm Arayüzlere Açık
- **Dosya:** `docker-compose.yml:10`
- **Düzeltme:** `127.0.0.1:5432:5432` yap.

### M12 — StrictHostKeyChecking=no
- **Dosya:** `chroot_terminal.py:132,235,282`
- **Düzeltme:** `accept-new` kullan.

---

## LOW

| # | Dosya | Açıklama |
|---|-------|----------|
| L1 | `core/db.py:100-106` | `_kolon_ekle` identifier validation yok |
| L2 | `routes/student.py:142-158` | Session regeneration yok |
| L3 | `chroot_login.sh:47,64` | $USERNAME format doğrulaması yok |
| L4 | `app.py:80-89` | Slayt dizini base path doğrulaması yok |
| L5 | `app.py:64` | SESSION_COOKIE_SECURE = False |
| L6 | Templates | Content Security Policy yok |
| L7 | `core/utils.py:12-16` | X-Forwarded-For doğrulamasız trust |
| L8 | `requirements.txt` | Pinlenmemiş dependency versiyonları |
| L9 | `chroot_yonetici.py:298` | SUID su binary chroot'ta |

---

## Düzeltme Öncelik Sırası

### Acil (Bu hafta)
1. SECRET_KEY random üret, .env'yi git'ten kaldır
2. SocketIO eventlerine session kontrolü ekle
3. DEBUG print satırını sil (teacher.py:18)
4. CSRF koruması ekle (flask-wtf)
5. innerHTML → textContent (XSS fix)

### Kısa Vadeli (Bu ay)
6. Şifre hashing (werkzeug)
7. Rate limiting (flask-limiter)
8. Öğrenci listesi API'sine auth ekle
9. SSH key-based auth'a geç
10. Docker güvenlik düzeltmeleri

### Uzun Vadeli
11. CSP headers
12. Chroot sudo kısıtlama
13. Dependency pinning
14. ProxyFix middleware
