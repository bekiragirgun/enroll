# Güvenlik Denetim Raporu

Bu rapor, projenin kaynak kodu üzerinde yapılan manuel güvenlik incelemesi sonucunda tespit edilen zafiyetleri içermektedir.

**Durum:** ✅ Tüm zafiyetler 13 Nisan 2026 tarihinde kapatıldı.

## Tespit Edilen Zafiyetler

### 1. Path Traversal (Dizin Gezintisi) — ✅ ÇÖZÜLDÜ
*   **Dosya:** `app.py` (Satır 126)
*   **Kod:** `yol = Path(klasor) / filename`
*   **Tür:** Güvenlik (Security)
*   **Önem Derecesi:** Yüksek (High)
*   **Açıklama:** `/slayt/<path:filename>` rotası, kullanıcının `../` gibi dizin gezintisi karakterlerini kullanarak sistemdeki herhangi bir `.html` dosyasına erişmesine izin verebilir. Sadece `.html` dosyalarıyla sınırlı olsa da, sunucudaki diğer hassas HTML dosyalarının ifşasına yol açabilir.
*   **Öneri:** `flask.safe_join` kullanarak veya çözümlenen yolun `klasor` dizini içinde kaldığını doğrulayarak bu zafiyeti engelleyin. `send_from_directory` fonksiyonu bu korumayı otomatik olarak sağlar.
*   **Uygulanan Çözüm:** `serve_slayt` fonksiyonunda HTML dalı için `Path.resolve()` + `relative_to(klasor_resolved)` kombinasyonu eklendi. `..` ve symlink ile dışarı çıkma denemeleri `ValueError` fırlatır ve `403` döner. `OSError` da yakalanır (kötü dosya adları için). Test: `..%2f..%2fetc/hosts.html` → 403 ✅

### 2. onclick İşleyicilerinde DOM XSS — ✅ ÇÖZÜLDÜ
*   **Dosya:** `static/js/ogretmen.js` (Satır 541, 593, 1990-1992)
*   **Kod:** `onclick="tekSil('${esc(o.numara)}', '${esc(o.ad_soyad).replace(/'/g, "\\'")}')"`
*   **Tür:** Güvenlik (Security)
*   **Önem Derecesi:** Orta (Medium)
*   **Açıklama:** Öğrenci isimleri veya sınav başlıkları gibi kullanıcı kontrollü veriler, satır içi `onclick` özniteliklerine yerleştirilmektedir. Mevcut kaçış mekanizması (`esc()` ve tırnak değiştirme), veride ters eğik çizgi veya JS dize bağlamını kırabilecek karakterler bulunması durumunda XSS saldırılarını önlemek için yetersizdir.
*   **Öneri:** Dinamik veriler için satır içi `onclick` kullanmaktan kaçının. Bunun yerine `addEventListener` kullanın veya verileri `data-*` özniteliklerinde saklayıp işleyici içinden okuyun.
*   **Uygulanan Çözüm:** Yeni `escJsAttr(s)` helper fonksiyonu eklendi (`static/js/ogretmen.js:5-12`). `JSON.stringify` ile JS string literal escape ve ardından HTML attribute için `&quot;`/`&#39;`/`&lt;`/`&gt;`/`&amp;` çevrimi yapılır. Çift katmanlı koruma sağlar — kullanıcı ad'ı `'); alert(1); //` gibi payload içerse bile JSON.stringify quote'lar ve HTML escape attribute kontekstini korur. Tüm 5 risk satırı (`tekSil`, `manuelGiris`, `soruYonetiminiAc`, `rubrikFormuAc`, `sinavSonuclariniAc`) bu helper'a geçirildi. Saf integer ID alan onclick'ler (`sinifKartToggle(${sinif.id})` vb.) doğal olarak güvenli olduğu için dokunulmadı.

### 3. HTML İçerisinde Hassas Bilgi İfşası — ✅ ÇÖZÜLDÜ
*   **Dosya:** `templates/ogretmen.html` (Satır 458, 504)
*   **Kod:** `<input type="password" id="config-chroot-pass" value="{{ config.chroot_pass }}">`
*   **Tür:** Güvenlik (Security)
*   **Önem Derecesi:** Düşük (Low)
*   **Açıklama:** SSH ve Veritabanı şifreleri, doğrudan HTML kaynak koduna `value` özniteliği içinde yazdırılmaktadır. Giriş tipi `password` olsa bile, öğretmen paneline erişimi olan herkes "Sayfa Kaynağını Görüntüle" diyerek ham şifreleri görebilir.
*   **Öneri:** Mevcut şifreleri istemciye geri göndermeyin. UI'daki şifre alanlarını boş bırakın ve sunucu tarafında sadece yeni bir değer girildiyse güncelleyin.
*   **Uygulanan Çözüm:** Hem `config-chroot-pass` hem `config-db-pass` input'larında `value=""` (boş) ve `autocomplete="new-password"` ayarlandı. Mevcut bir şifre varsa placeholder `••••• (değiştirmemek için boş bırak)` ve açıklama "Mevcut şifre saklı. Yeni değer girilirse güncellenir." gösterir. Backend tarafında `routes/api.py` POST `/api/config` handler'ında `chroot_pass` ve `db_pass` için "boş gönderilirse mevcut değeri koru" mantığı eklendi. Test: `view-source` ile sayfa kaynağında ham şifre artık yok ✅

---
*Rapor Tarihi: 13 Nisan 2026*
*Düzeltme Tarihi: 13 Nisan 2026*
