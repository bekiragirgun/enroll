# 🔐 Terminal Güvenlik Sistemi

## Akış

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ÖĞRENCİ ANA SAYFADAN GİRİŞ YAPAR                        │
│    POST /api/giris                                         │
│    { numara: "220001001", ad: "Ahmet", soyad: "Yılmaz" }   │
│    → session['numara'] = '220001001'                        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. ÖĞRENCİ SLAYTLARI İZLER                                  │
│    WebSocket ile aktif mod'u takip eder                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. ÖĞRETMEN "TERMINAL" BUTONUNA BASAR                      │
│    POST /api/mod → { mod: 'terminal' }                     │
│    → Tüm öğrenciler /terminal'e yönlendirilir              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. ÖĞRENCİ /terminal SAYFASINA GELİR                       │
│    GET /terminal                                           │
│    → terminal_guvenlik.html gösterilir                     │
│    → Session numarası ekranda yazılı                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. ÖĞRENCİ NUMARASINI DOĞRULAR                             │
│    POST /terminal/login                                    │
│    { numara_dogrulama: "220001001" }                       │
│                                                             │
│    ┌─────────────────────┬─────────────────────┐          │
│    │ AYNI NUMARA         │ FARKLI NUMARA       │          │
│    ├─────────────────────┼─────────────────────┤          │
│    │ ✅ Chroot'a giriş   │ ❌ ALARM!           │          │
│    │ ✅ Loglanır (BASARILI)│ ❌ Loglanır (GUVENLIK_IHLALI)│  │
│    │ ✅ /terminal/workspace│ ❌ Uyarı gösterilir│          │
│    │                     │ ❌ Öğretmene bildirim│          │
│    └─────────────────────┴─────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Güvenlik Kontrolleri

### 1. Session Doğrulama
```python
# Ana oturumda numara var mı?
if not session.get('numara'):
    return "Önce giriş yapmalısınız"
```

### 2. Numara Eşleşme Kontrolü
```python
# Session numarası ile girilen numara aynı mı?
if girilen_numara == session_numara:
    # ✅ BAŞARILI
    durum = 'BASARILI'
else:
    # ❌ GÜVENLİK İHLALİ
    durum = 'GUVENLIK_IHLALI'
```

### 3. Veritabanı Loglama
```sql
INSERT INTO terminal_guvenlik_log
(tarih, saat, ip, session_numara, session_ad, girilen_numara, durum)
VALUES ('2026-03-03', '14:30:00', '192.168.1.100',
        '220001001', 'Ahmet Yılmaz', '220001002', 'GUVENLIK_IHLALI')
```

### 4. Öğretmen Bildirimi (WebSocket)
```javascript
// Öğretmen panelinde anlık bildirim
socket.on('guvenlik_uyari', (mesaj) => {
    alert('⚠️ GÜVENLİK UYARISI!\n' + mesaj);
    // Sesli uyarı
    new Audio('/static/sounds/alert.mp3').play();
});
```

## Veritabanı Yapısı

### terminal_guvenlik_log Tablosu

| Kolon | Tip | Açıklama |
|-------|-----|----------|
| id | INTEGER | Primary Key |
| tarih | TEXT | YYYY-MM-DD |
| saat | TEXT | HH:MM:SS |
| ip | TEXT | İstemci IP adresi |
| session_numara | TEXT | Oturum açan öğrenci numarası |
| session_ad | TEXT | Oturum açan öğrenci adı |
| girilen_numara | TEXT | Terminal'e girmeye çalışan numara |
| durum | TEXT | 'BASARILI' veya 'GUVENLIK_IHLALI' |
| uyari_gonderildi | INTEGER | E-posta gönderildi mi? (0/1) |

## Örnek Senaryolar

### ✅ Başarılı Erişim
```
1. Ahmet (220001001) ana sayfadan giriş yapar
   → session['numara'] = '220001001'

2. Öğretmen terminal moduna geçer
   → Ahmet /terminal'e yönlendirilir

3. Ahmet terminal_guvenlik.html'de "220001001" girer
   → AYNI NUMARA ✅
   → Chroot ortamına giriş
   → Log: BASARILI
```

### ❌ Güvenlik İhlali
```
1. Ahmet (220001001) ana sayfadan giriş yapar
   → session['numara'] = '220001001'

2. Öğretmen terminal moduna geçer
   → Ahmet /terminal'e yönlendirilir

3. Ahmet "220001002" numarasını dener (arkadaşının numarası)
   → FARKLI NUMARA ❌
   → Uyarı: "Bu terminal 220001001 içindir!"
   → Log: GUVENLIK_IHLALI
   → Öğretmene anlık bildirim
   → Ahmet'e uyarı e-postası
```

## Güvenlik Önlemleri

### Frontend (Tarayıcı)
- ✅ Session numarası otomatik doldurulur
- ✅ Yanlış girmeyi deneyen kullanıcıya JavaScript onay sorusu
- ✅ Uyarı mesajı gösterilir

### Backend (Sunucu)
- ✅ Session numarası ile girilen numara karşılaştırılır
- ✅ Tüm erişim denemeleri loglanır
- ✅ Farklı numara girişi anında öğretmene bildirim

### Veritabanı
- ✅ Tüm loglar kalıcı olarak saklanır
- ✅ IP adresi, tarih, saat kaydedilir
- ✅ İleriye dönük analiz mümkün

## Öğretmen Paneli

### Güvenlik Log Tab'ı
```
🔐 Güvenlik Log

✅ 220001001 (Ahmet Yılmaz) → 220001001
   2026-03-03 14:30 | IP: 192.168.1.100

⚠️  220001001 (Ahmet Yılmaz) → 220001002
   2026-03-03 14:35 | IP: 192.168.1.100
   GUVENLIK IHLALI!
```

### Anlık Bildirimler
- 🔔 Sesli uyarı (alert.mp3)
- 📧 Tarayıcı bildirimi (alert())
- 📊 Güvenlik log rozet güncellenir

## Log Sorgulama

### Son 50 Güvenlik Logu
```bash
sqlite3 data/yoklama.db "SELECT * FROM terminal_guvenlik_log ORDER BY id DESC LIMIT 50"
```

### Güvenlik İhlalleri
```bash
sqlite3 data/yoklama.db "SELECT * FROM terminal_guvenlik_log WHERE durum='GUVENLIK_IHLALI'"
```

### Bugünün Logları
```bash
sqlite3 data/yoklama.db "SELECT * FROM terminal_guvenlik_log WHERE tarih=date('now')"
```

## Öğrenciye Gönderilecek Uyarı E-postası

```python
def uyari_eposta_gonder(session_numara, session_ad, girilen_numara):
    konu = "⚠️ Terminal Güvenlik İhlali Bildirimi"
    icerik = f"""
    Sayın {session_ad},

    {bugun()} {simdi()} tarihinde terminal erişiminde
    güvenlik ihlali tespit edilmiştir.

    Oturum numaranız: {session_numara}
    Girmeye çalıştığınız numara: {girilen_numara}

    Bu erişim girişimi loglanmıştır ve öğretmeninize
    bildirilmiştir.

    Lütfen terminali sadece kendi numaranızla kullanınız.

    Saygılarla,
    Kapadokya Üniversitesi BGY106
    """
    # E-posta gönderme kodu...
```

## Gelecek Özellikler

- [ ] Otomatik e-posta bildirimi
- [ ] Çoklu başarısız denemede hesap kilidi
- [ ] Ebeveyn bilgilendirme
- [ ] Detaylı güvenlik raporları (PDF)
- [ ] IP bazlı kara liste
