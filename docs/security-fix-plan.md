# Güvenlik Düzeltme Planı

**Referans:** docs/security-audit-2026-04-02.md
**Toplam:** 32 zafiyet (2 CRITICAL, 9 HIGH, 12 MEDIUM, 9 LOW)

---

## Faz 1 — Acil (CRITICAL + HIGH) — Tahmini: 1-2 gün

### 1.1 SECRET_KEY Düzeltmesi [C1]
```python
# app.py — mevcut:
app.secret_key = os.environ.get('SECRET_KEY', 'kapadokya-linux-2024')

# düzeltme:
app.secret_key = os.environ['SECRET_KEY']  # fallback yok, yoksa crash
```
```bash
# .env'yi git'ten kaldır
git rm --cached .env
echo "SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(32))')" > .env
```

### 1.2 SocketIO Auth [H1]
```python
# app.py — ogretmen_baglan_event içine:
if not session.get('ogretmen'):
    emit('error', {'mesaj': 'Yetkisiz'})
    return

# ogrenci_baglan_event içine:
if not session.get('numara'):
    emit('error', {'mesaj': 'Yetkisiz'})
    return
```

### 1.3 DEBUG Print Kaldır [H3]
```python
# routes/teacher.py:18 — SİL:
print(f"DEBUG: Login attempt - Input: '{pw_input}', Expected: '{pw_expected}'")
```

### 1.4 CSRF Koruması [H2]
```bash
pip install flask-wtf
```
```python
# app.py:
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# AJAX için exempt (JSON Content-Type yeterli):
@csrf.exempt
@exam_bp.route('/cevap_kaydet', methods=['POST'])
```
```html
<!-- formlara ekle: -->
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

### 1.5 XSS Fix [H8]
```javascript
// static/js/ogrenci.js — escape fonksiyonu ekle:
function esc(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

// Kullanım — innerHTML içinde:
// ${soru.metin}  →  ${esc(soru.metin)}
// ${secenek.metin}  →  ${esc(secenek.metin)}
```

### 1.6 Şifre Hashing [H4]
```python
# routes/teacher.py:
from werkzeug.security import generate_password_hash, check_password_hash

# Login kontrolü:
if check_password_hash(pw_expected_hash, pw_input):

# Şifre kaydetme:
ayar_kaydet('ogretmen_sifre', generate_password_hash(yeni))
```

### 1.7 Brute-Force Koruması [H7]
```bash
pip install flask-limiter
```
```python
# app.py:
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["100/hour"])

# routes/teacher.py:
@teacher_bp.route('/login', methods=['POST'])
@limiter.limit("5/minute")
def ogretmen_giris():
```

### 1.8 .env Git'ten Kaldır [H6]
```bash
git rm --cached .env
# .gitignore'da zaten var, tekrar kontrol et
echo ".env" >> .gitignore
```

### 1.9 Chroot sudo Kısıtlama [H9]
```bash
# Mevcut (tehlikeli):
%ogrenciler ALL=(ALL) NOPASSWD: ALL

# Düzeltme:
%ogrenciler ALL=(ALL) NOPASSWD: /bin/su
```

---

## Faz 2 — Kısa Vadeli (MEDIUM) — Tahmini: 3-5 gün

### 2.1 SSH Key Auth [M2, M4]
- sshpass kaldır, SSH key pair oluştur
- Host'tan chroot'a key-based bağlantı

### 2.2 API Auth [M3, M5]
```python
# routes/api.py — kimliksiz endpointlere decorator ekle:
@api_bp.route('/ogrenci_listesi/<sinif_id>')
@seb_gerekli  # veya @ogretmen_giris_gerekli
def api_sinif_ogrencileri(sinif_id):
```

### 2.3 innerHTML Temizleme [M6]
- ogretmen.js'deki tüm innerHTML kullanımlarında esc() fonksiyonu

### 2.4 Command Injection Fix [M7]
```python
# Mevcut (tehlikeli):
cmd = f"bash -c 'sudo {PYTHON_PATH} {SCRIPT} create \'{slug}\' \'{safe_ad}\''"

# Düzeltme — liste argümanları:
subprocess.run(["sudo", PYTHON_PATH, SCRIPT, "create", slug, safe_ad])
```

### 2.5 SocketIO CORS [M8]
```python
# app.py:
SocketIO(app, cors_allowed_origins=["http://localhost:3333", "https://yourdomain.com"])
```

### 2.6 Docker Güvenlik [M9, M10, M11]
```dockerfile
# Dockerfile:
RUN useradd -m appuser
USER appuser
```
```yaml
# docker-compose.yml:
ports:
  - "127.0.0.1:5432:5432"  # localhost only
volumes:
  - ./data:/app/data        # sadece data dizini
```

### 2.7 SSH StrictHostKeyChecking [M12]
```python
# chroot_terminal.py — tüm SSH komutlarında:
"-o", "StrictHostKeyChecking=accept-new"  # "no" yerine
```

---

## Faz 3 — Uzun Vadeli (LOW) — Tahmini: 1-2 gün

### 3.1 CSP Headers [L6]
```python
@app.after_request
def security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response
```

### 3.2 Dependency Pinning [L8]
```bash
pip freeze > requirements.txt
# veya
pip install pip-audit
pip-audit
```

### 3.3 ProxyFix [L7]
```python
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
```

### 3.4 Session Regeneration [L2]
```python
# routes/student.py — login sonrası:
session.clear()
session['numara'] = numara
# yeni session ID otomatik oluşur
```

---

## Yeni Dependency'ler

```
flask-wtf>=1.2.0      # CSRF koruması
flask-limiter>=3.5.0   # Rate limiting
```

## Test Planı

Her fix sonrası:
1. `python3 app.py --test` ile çalıştır
2. Öğretmen login → sınav oluştur → başlat
3. Öğrenci login → sınav cevapla
4. Terminal SSH bağlantısı
5. trivy fs . ile tekrar tara
