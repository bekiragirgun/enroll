# Ders Takip Sistemi Guvenlik Inceleme Raporu

Tarih: 2026-04-13

Kapsam:
- Kod incelemesi `app.py`, `routes/*`, `core/*`, `templates/*`, `static/js/*`, `docker-compose.yml`, `README.md`
- Inceleme mevcut calisma agaci uzerinde yapildi
- Dinamik exploit dogrulamasi yapilmadi; bulgular kod akisina ve konfigurasyona dayali

## Ozet

Toplam bulgu:
- `1` kritik
- `3` yuksek
- `3` orta

En kritik risk, WebSocket terminal olaylarinda yetki kontrollerinin eksik olmasi. Mevcut haliyle giris yapmis bir ogrenci, ogretmen terminaline komut yazabilir ve kendi oturumunu baska bir ogrencinin chroot'una baglayabilir. Buna ek olarak sinav ihlal aciklamasi uzerinden ogretmen panelinde stored XSS zinciri mevcut.

## Pozitif Gozlemler

- SQL sorgularinin buyuk cogunlugu parametreli yazilmis; belirgin bir klasik SQL injection yuzeyi goremedim.
- Slayt dosyasi servisinde path traversal icin ek kontroller mevcut: [app.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/app.py:110) ve [routes/api.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/api.py:80).
- `.env` dosyasi `.gitignore` icinde; depo duzeyinde dogrudan commit edilmis bir `.env` gormedim: [.gitignore](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/.gitignore:41).

## Bulgular

### C1 - WebSocket uzerinden ogretmen terminaline yetkisiz komut enjeksiyonu

Kanit:
- `ogretmen_baglan` ogretmen PTY'sini aciyor: [app.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/app.py:283)
- Ancak `ogretmen_girdi` olayi hicbir `session` veya `request.sid` kontrolu yapmadan global `ogretmen_pty_fd`'ye yazi yaziyor: [app.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/app.py:346)
- `ogretmen_temizle` de benzer sekilde yetkisiz broadcast yapiyor: [app.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/app.py:365)
- Ogrenci istemcisi de ayni `/terminal` namespace'ine baglaniyor: [templates/terminal_workspace.html](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/templates/terminal_workspace.html:189)

Etki:
- Giris yapmis herhangi bir ogrenci, tarayici konsolundan `socket.emit('ogretmen_girdi', {data: '...'} )` gondererek ogretmen terminaline komut enjekte edebilir.
- Ogretmen PTY'si uzak SSH/chroot zinciri uzerinden acildigi icin etki yalnizca UI bozma degil, fiili komut calistirma seviyesindedir.

Oneri:
- `ogretmen_girdi` ve `ogretmen_temizle` icin `request.sid == ogretmen_sid` zorunlu olsun.
- Ek olarak `session.get('ogretmen')` ikinci savunma hatti olarak kontrol edilsin.
- Ogretmen terminali icin ayri namespace veya ayri Socket.IO room kullanin; ogrenci istemcilerini bu kanaldan tamamen ayirin.

### H1 - Ogrenci terminal oturumu, istemcinin gonderdigi kullanici adina guveniyor

Kanit:
- WebSocket tarafinda tek kontrol `session.get('numara')` var; daha sonra istemciden gelen `username` dogrudan kullaniliyor: [app.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/app.py:429)
- Sunucu `username` degerine gore chroot olusturuyor ve baglanti aciyor: [app.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/app.py:447)
- HTTP tarafinda terminal dogrulama icin `terminal_numara` oturuma yaziliyor: [routes/terminal.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/terminal.py:19) fakat WebSocket akisi bunu hic dogrulamiyor.

Etki:
- Giris yapmis bir ogrenci, kendi numarasi yerine baska bir kullanici adiyla `ogrenci_baglan` gonderebilir.
- Bu, terminal dogrulama adimini by-pass eder ve baska bir ogrencinin chroot'una erisim veya o ogrenci adina yeni chroot olusturma riski dogurur.

Oneri:
- `username` parametresini istemciden kabul etmeyin; sunucu sadece `session['terminal_numara']` veya `session['numara']` uzerinden karar versin.
- `ogrenci_sidleri[sid]` degerini istemci verisinden degil, server-side session'dan turetin.
- `terminal_workspace` icin kullanilan ikinci faktor benzeri kontrol WebSocket tarafinda da zorunlu olsun.

### H2 - Sinav ihlal aciklamasi uzerinden ogretmen panelinde stored XSS

Kanit:
- Ogrenci tarafi `aciklama` degerini oldugu gibi veritabanina yazabiliyor: [routes/exam.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/exam.py:484)
- Ogretmen paneli bu veriyi `innerHTML` ile kacissiz basiyor: [static/js/ogretmen.js](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/static/js/ogretmen.js:2700)

Etki:
- Ogrenci, ihlal aciklamasina HTML/JS payload koyup ogretmen ekrani popup'i actiginda JS calistirabilir.
- Bu, ogretmen oturumundan `/api/config`, `/api/chroot/sil`, `/api/toplu_cikis` gibi kritik endpoint'lere istek atmak icin kullanilabilir.

Oneri:
- Bu popup tamamen `textContent`/`createElement` ile uretilsin.
- `innerHTML` kullanilacaksa tum degisken alanlar `esc(...)` benzeri kacislamadan gecsin.
- Tarayici tarafi duzeltmenin yanina sunucu tarafinda da `aciklama` icin HTML sanitize veya encoding ekleyin.

### H3 - Ogretmen kimlik dogrulamasi varsayilan parola ve duz metin saklama uzerine kurulu

Kanit:
- Varsayilan parola kod icinde sabit: [routes/teacher.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/teacher.py:6)
- Parola duz string karsilastirmasi ile kontrol ediliyor: [routes/teacher.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/teacher.py:12)
- Parola README icinde de yayinlanmis: [README.md](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/README.md:124)
- Sifre degistirme akisi yeni sifreyi hash'siz kaydediyor: [routes/teacher.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/teacher.py:41)

Etki:
- Parola degistirilmemis sistemlerde yonetici paneli fiilen varsayilan kimlik bilgileriyle acik.
- Veritabani sizmasi veya log/backup erisimi durumunda ogretmen sifresi acik metin olarak ele gecirilebilir.
- Kod tabaninda brute-force veya rate limit mekanizmasina dair bir iz goremedim; bu da riski buyutuyor.

Oneri:
- `werkzeug.security.generate_password_hash` ve `check_password_hash` kullanin.
- Ilk kurulumda zorunlu parola rotasyonu uygulayin; README'den varsayilan sifreyi kaldirin.
- `/teacher/login` icin rate limiting ekleyin.

### M1 - DB ve chroot sirlari uygulama veritabanisinda duz metin tutuluyor

Kanit:
- `api/config` gelen `chroot_pass` ve `db_pass` degerlerini dogrudan `ayar_kaydet` ile sakliyor: [routes/api.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/api.py:248)
- Bu sirlar `ders_durumu` icinde bellege yukleniyor: [core/config.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/core/config.py:11)
- Zayif varsayilan DB sifresi de mevcut: [core/db.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/core/db.py:190), [docker-compose.yml](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/docker-compose.yml:7)

Etki:
- Uygulama veritabanina erisen kisi sadece uygulama verisini degil, uzak chroot host ve veritabani erisim bilgilerini de topluca elde eder.
- Bu bilgi, H2 gibi bir XSS veya H3 gibi ogretmen paneli ele gecirme bulgulari ile zincirlenebilir.

Oneri:
- Bu tip sirlarin uygulama veritabanisina yazilmasini kaldirin; ortam degiskeni, secret manager veya dosya tabanli protected secret store kullanin.
- Zorunlu ise en azindan uygulama seviyesinde sifreleme ve anahtar ayristirma uygulayin.
- `postgres_pass` gibi varsayilanlari kaldirin.

### M2 - SEB/policy konfigurasyonu sinav guvenligini zayiflatiyor

Kanit:
- `allowThirdPartyCookies = true`: [routes/student.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/student.py:240)
- `URLFilterEnable = false`: [routes/student.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/student.py:254)
- `allowVirtualMachine = true`: [routes/student.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/student.py:258)
- `quitPassword = linux2024`: [routes/student.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/routes/student.py:275)

Etki:
- Sistem kendini SEB/kiosk modlu sinav ortami olarak konumlarken, sanal makine ve tum URL'lere izin vererek bu modeli zayiflatiyor.
- Quit parolasinin sabit olmasi, istemci tarafinda sinavdan cikisin dolasli olarak kolaylastirilmasi anlamina geliyor.

Oneri:
- SEB profilini "minimum yetki" mantigiyla yeniden olusturun.
- Quit parolasini sabit string yerine kurulum bazli benzersiz bir sir haline getirin veya bu ozelligi kapatin.
- VM izni ve URL filtresi egitim ihtiyacina gore yeniden degerlendirilsin.

### M3 - Oturumlar HTTP'ye gore ayarlanmis; transport hardening eksik

Kanit:
- `SESSION_COOKIE_SECURE = False`: [app.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/app.py:68)
- Sadece temel iki header var; CSP, HSTS, Referrer-Policy gibi korumalar tanimli degil: [app.py](/Users/bekiragirgun/Projects/KAPADOKYA_SLAYT/ders_takip/app.py:82)

Etki:
- Sistem localhost/LAN disinda kullaniliyorsa ogretmen parolasi, session cookie'leri ve terminal trafigi agir sekilde riske girer.
- H2 gibi XSS bulgulari, CSP olmadigi icin daha rahat istismar edilir.

Oneri:
- Uygulamayi ters proxy arkasinda HTTPS ile calistirin; `SESSION_COOKIE_SECURE = True` yapin.
- HSTS, CSP, Referrer-Policy ve benzeri header'lari ekleyin.
- HTTP modunu yalnizca lokal gelistirme moduna sinirlayin.

## Oncelikli Duzeltme Sirasi

1. `app.py` icindeki WebSocket olaylarini sert sekilde yetkilendirin.
2. `static/js/ogretmen.js` icindeki XSS yuzeylerini `innerHTML` yerine guvenli DOM API ile yeniden yazin.
3. Ogretmen kimlik dogrulamasini hash'li parola, rate limit ve zorunlu parola rotasyonu ile degistirin.
4. `api/config` uzerinden altyapi sirlari tutmayi birakin; secret'lari uygulama DB'sinden cikarin.
5. SEB ve transport ayarlarini sertlestirin.

## Sonuc

Kod tabaninda iyi niyetli bazi guvenlik onlemleri var; fakat terminal ve sinav akislarindaki guven sinirlari istemci tarafina fazla dayanmis. Mevcut haliyle en ciddi riskler, oturum acmis ogrencinin ogretmen terminaline komut yazabilmesi ve stored XSS ile ogretmen panelini ele gecirebilmesidir. Uretim ortamina alinmadan once en az C1, H1 ve H2 kapatilmis olmalidir.
