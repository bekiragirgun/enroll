---
marp: true
theme: default
paginate: true
lang: tr
backgroundColor: #F7F7F7
style: |
  section {
    font-family: 'Trebuchet MS', Arial, sans-serif;
    font-size: 85%;
    padding: 85px 50px 30px 50px;
    background-color: #F7F7F7;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    position: relative;
  }

  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
    position: absolute;
    bottom: 10px;
    right: 30px;
    color: #666;
    font-size: 12pt;
    pointer-events: none;
    z-index: 1;
  }

  h1 {
    color: #2D4A7C;
    font-size: 26pt;
    font-weight: bold;
    margin-bottom: 20px;
    margin-left: 350px;
    padding-bottom: 10px;
    border-bottom: none !important;
    text-align: left;
  }

  h2 {
    color: #2D4A7C;
    font-size: 18pt;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 10px;
  }

  h3 {
    color: #2D4A7C;
    font-size: 15pt;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 8px;
  }

  p, li {
    font-size: 13pt;
    line-height: 1.5;
    color: #333;
  }

  section.cover-slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
    padding-left: 80px;
    position: relative;
    background-color: #2D4A7C !important;
  }

  section.cover-slide h1 {
    color: white;
    font-size: 38pt;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    border-bottom: none;
  }

  section.cover-slide p {
    position: absolute;
    bottom: 40px;
    right: 60px;
    color: white;
    font-size: 20pt;
    font-weight: normal;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
  }

  section.cover-slide::after {
    content: none;
  }

  section.topic-slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
  }

  section.topic-slide h1 {
    color: white;
    font-size: 38pt;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    border-bottom: none;
    margin: 0;
  }

  section.topic-slide p {
    position: absolute;
    bottom: 40px;
    right: 60px;
    color: white;
    font-size: 20pt;
    font-weight: normal;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
  }

  section.topic-slide::after {
    content: none;
  }

  section.final-slide {
    background-color: #2D4A7C !important;
    color: white !important;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    position: relative;
  }

  section.final-slide::after {
    content: none;
  }

  section.final-slide h1,
  section.final-slide h2,
  section.final-slide h3,
  section.final-slide p,
  section.final-slide strong,
  section.final-slide li,
  section.final-slide div,
  section.final-slide a {
    color: white !important;
    border-bottom-color: white !important;
  }

  section.final-slide div *,
  section.final-slide a {
    color: white !important;
  }

  .two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-top: 20px;
  }

  .info-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .info-box h3 {
    color: white;
    margin-top: 0;
  }

  .info-box th, .info-box td {
    color: white !important;
    background-color: transparent !important;
    border-color: rgba(255,255,255,0.3) !important;
  }

  .info-box th {
    background-color: rgba(0,0,0,0.2) !important;
  }

  .highlight-box {
    background: linear-gradient(135deg, #6B9FE8 0%, #4A7FB8 100%);
    color: white;
    padding: 18px;
    border-radius: 12px;
    margin: 15px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .highlight-box h3 {
    color: white;
    margin-top: 0;
  }

  .highlight-box th, .highlight-box td {
    color: white !important;
    background-color: transparent !important;
    border-color: rgba(255,255,255,0.3) !important;
  }

  .highlight-box th {
    background-color: rgba(0,0,0,0.2) !important;
  }

  .compare-box {
    background: #dce4ec;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #6B9FE8;
  }

  .compare-box th {
    background-color: #2D4A7C;
    color: white;
  }

  .compare-box td {
    color: #333 !important;
    background-color: white !important;
  }

  td {
    color: #333 !important;
    background-color: white !important;
  }

  th {
    background-color: #2D4A7C;
    color: white;
  }

  code {
    background-color: #1a1a1a;
    color: #e0e0e0;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12pt;
  }

  pre {
    background-color: #1a1a1a;
    color: #e0e0e0;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  }

  pre code {
    background: none;
    padding: 0;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12pt;
    line-height: 1.5;
  }

  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
  }
---

<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# Kullanıcı Hesap Yönetimi

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Giriş

---

![bg](../gorseller/3_normal_slayt.png)

# Giriş

### 🔐 Kullanıcı Hesaplarının Amacı

Kullanıcı hesapları Linux işletim sisteminde güvenliği sağlamak için tasarlanmıştır:

- **Dosya Erişim Kontrolü:** Her kullanıcı belirli dosyalara ve dizinlere erişebilir
- **İzin Yönetimi:** Root kullanıcısı izinleri düzenleyebilir
- **Grup Üyeliği:** Kullanıcılar gruplara ait olarak veri paylaşımı yapabilir

### 📚 Veri Tabanları

Kullanıcı ve grup bilgileri veritabanı dosyalarında saklanır:

- `/etc/passwd` - Kullanıcı hesap bilgileri
- `/etc/shadow` - Şifre ve güvenlik bilgileri
- `/etc/group` - Grup hesap bilgileri

### 💡 Komutlar

Sistemdeki kullanıcıları görüntüleme ve hesaplar arasında geçiş için komutlar mevcuttur.

---

![bg](../gorseller/3_normal_slayt.png)

# Giriş

<div class="two-columns">
<div>

### 🎯 Temel Kavramlar

**Kullanıcı Hesapları:**
- Her kişi sisteme kendi hesabı ile giriş yapar
- Dosya izinleri kullanıcı, grup ve diğerleri (others) için tanımlanır
- Root kullanıcısı tüm izinleri düzenleyebilir

**Grup Hesapları:**
- Kullanıcılar bir veya daha fazla gruba üye olabilir
- Gruplar dosya erişimını kolaylaştırır
- Birincil ve ikincil grup üyeliği vardır

</div>

<div class="info-box">

### ⚠️ Güvenlik Bilgisi

Kullanıcı ve grup veritabanı dosyaları sistem güvenliği için kritiktir:

- **Giriş Kontrolü:** Kimlerin sisteme erişebileceğini belirler
- **İzin Yönetimi:** Dosya ve dizin erişimlerini kontrol eder
- **Güvenlik İzleme:** Yetkisiz erişim tespit edilir

</div>
</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Yönetici Hesapları

---

![bg](../gorseller/3_normal_slayt.png)

# Yönetici Hesapları

### ⚠️ Root Hesabı Riskleri

Root kullanıcısı olarak doğrudan giriş yapmak tehlikelidir:

<div class="highlight-box">

### 🚨 Tehlikeler

- **Unutma Riski:** Root'ta olduğunu unutup hatalı komut çalıştırabilirsiniz
- **Geniş Erişim:** Grafik ortamda root ile giriş tüm programlara tam yetki verir
- **Güvenlik Açığı:** Tarayıcı ve e-posta istemcileri gibi programlar kısıtsız çalışır

</div>

### ✅ Önerilen Yöntem

**Ubuntu'da Root Hesabı:**
- Root hesabı varsayılan olarak devre dışıdır
- Yönetici komutları `sudo` ile çalıştırılır
- Güvenlik ve hesap verilebilirliği sağlanır

---

![bg](../gorseller/3_normal_slayt.png)

# Kullanıcı Değiştirme (su)

### 🔄 su Komutu

Farklı kullanıcı ile kabuk çalıştırır:

```bash
su [options] [username]
```

### 📋 Ana Seçenekler

- **`su -`** / **`su -l`** → Login shell (tam giriş)
- **`su`** → Sadece shell değiştirir
- **`su --login`** → Açık form

**💡 Login shell** tüm ortam değişkenlerini yükler

---

![bg](../gorseller/3_normal_slayt.png)

# Kullanıcı Değiştirme (su) - Örnek

### 💡 Pratik Kullanım

<div class="info-box">

### Örnek: Root Kullanıcısına Geçiş

```bash
# Root kullanıcısına geçiş
sysadmin@localhost:~$ su -
Password: netlab123

# Kimlik kontrolü
root@localhost:~# id
uid=0(root) gid=0(root) groups=0(root)

# Çıkış
root@localhost:~# exit
logout
```

**Not:** `exit` komutu ile oturumdan çıkabilirsiniz

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Yetkili Komut Çalıştırma (sudo)

### 🎯 sudo Komutu

Kullanıcıların başka bir kullanıcı adına komut çalıştırmasını sağlar:

```bash
sudo [options] command
```

<div class="two-columns">
<div>

### 🔒 Güvenlik Özellikleri

- **Kendi Şifresi:** Root şifresi değil, kullanıcının kendi şifresi
- **Oturum Süresi:** 5 dakika içinde tekrar sudo kullanırsa şifre sormaz
- **Loglama:** Tüm sudo komutları log dosyasına kaydedilir
- **Hesap Verilebilirliği:** Kimin hangi komutu çalıştırdığı bilinir

</div>
<div class="info-box">

### ✅ Avantajları

- **Güvenlik:** Root şifresi paylaşılmasına gerek yok
- **Denetim:** Her yönetici işlemi kaydedilir
- **Hata Önleme:** Yanlışlıkla root komutu çalıştırma riski azalır
- **Niyet Belirliği:** Sadece sudo ile başlayan komutlar root yetkisinde çalışır

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# sudo Komutu - Örnekler

### 💡 Pratik Kullanım

```bash
# Izinsiz dosya okuma denemesi
sysadmin@localhost:~$ head /etc/shadow
head: cannot open '/etc/shadow' for reading: Permission denied

# sudo ile yetkili erişim
sysadmin@localhost:~$ sudo head /etc/shadow
[sudo] password for sysadmin: netlab123
root:$6$4Yga95H9$8HbxqsMEIBTZ0YomlMffYCV9VE1SQ4T2H3SHXw41M02SQtfAdDVE9mqGp2hr20q
daemon:*:16463:0:99999:7:::
bin:*:16463:0:99999:7:::
```

---

![bg](../gorseller/3_normal_slayt.png)

# sudo vs su Karşılaştırma

<div class="compare-box">

### 📊 sudo vs su

| Özellik | su | sudo |
|---------|-----|------|
| Şifre | Hedef kullanıcının şifresi | Kendi şifreniz |
| Oturum | Tam yeni shell | Tek komut |
| Loglama | Sınırlı | Detaylı log |
| Güvenlik | Root şifresi paylaşımı | Kullanıcı bazlı |

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Kullanıcı Hesapları

---

![bg](../gorseller/3_normal_slayt.png)

# /etc/passwd Dosyası

### 📄 Kullanıcı Hesap Bilgileri

`/etc/passwd` dosyası sistemdeki tüm kullanıcı hesaplarını tanımlar:

```bash
sysadmin@localhost:~$ tail -5 /etc/passwd
syslog:x:101:103::/home/syslog:/bin/false
bind:x:102:105::/var/cache/bind:/bin/false
sshd:x:103:65534::/var/run/sshd:/usr/sbin/nologin
operator:x:1000:37::/root:/bin/sh
sysadmin:x:1001:1001:System Administrator...:/home/sysadmin:/bin/bash
```

### 🔍 Alan Açıklamaları (1-3)

**sysadmin:x:1001:1001:System Administrator,,,,:/home/sysadmin:/bin/bash**

1. **Kullanıcı Adı:** `sysadmin` - Giriş için kullanılır
2. **Şifre Yer Tutucusu:** `x` - Şifre `/etc/shadow` dosyasındadır
3. **User ID (UID):** `1001` - Dosya sahipliği UID ile tanımlanır

---

![bg](../gorseller/3_normal_slayt.png)

# /etc/passwd Dosyası (devam)

### 🔍 Alan Açıklamaları (4-7)

**sysadmin:x:1001:1001:System Administrator,,,,:/home/sysadmin:/bin/bash**

4. **Birincil Grup ID (GID):** `1001` - Kullanıcının birincil grubu
5. **Açıklama:** `System Administrator,,,,` - Kullanıcı hakkında bilgi
6. **Home Dizin:** `/home/sysadmin` - Kullanıcının kişisel klasörü
7. **Shell:** `/bin/bash` - Varsayılan kabuk programı

---

![bg](../gorseller/3_normal_slayt.png)

# /etc/passwd - Arama (grep)

### 🔍 grep ile Arama

Belirli bir kullanıcının bilgilerini görüntüleme:

```bash
sysadmin@localhost:~$ grep sysadmin /etc/passwd
sysadmin:x:1001:1001:System Admin...:/home/sysadmin:/bin/bash
```

<div class="info-box">

### 💡 grep Avantajları

- **Hızlı:** Doğrudan dosya araması
- **Basit:** Standart regex desteği

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# /etc/passwd - Arama (getent)

### 🔍 getent Komutu

Daha gelişmiş kullanıcı sorgusu:

```bash
sysadmin@localhost:~$ getent passwd sysadmin
sysadmin:x:1001:1001:System Admin...:/home/sysadmin:/bin/bash
```

<div class="info-box">

### 💡 getent Avantajları

- **Çok Kaynak:** Yerel + LDAP, AD, NIS
- **Tutarlı:** Farklı kaynaklar için aynı arayüz
- **Güçlü:** Name Service Switch ile entegre

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# /etc/shadow Dosyası

### 🔐 Şifre Güvenlik Dosyası

`/etc/shadow` dosyası kullanıcı şifrelerini ve yaşlandırma bilgilerini içerir:

```bash
root@localhost:~# tail -5 /etc/shadow
syslog:*:16874:0:99999:7:::
bind:*:16874:0:99999:7:::
sshd:*:16874:0:99999:7:::
operator:!:16874:0:99999:7:::
sysadmin:$6$c75ekQWF$...:16874:5:30:7:60:15050::
```

### 📊 Alan Açıklamaları (1-4)

**sysadmin:$6$c75ekQWF$...:16874:5:30:7:60:15050::**

1. **Kullanıcı Adı:** `sysadmin`
2. **Şifre:** `$6$c75ekQWF$...` - Tek yönlü şifreleme
3. **Son Değişiklik:** `16874` - Epoch'dan gün sayısı
4. **Minimum:** `5` - Şifre değişiklikleri arası minimum gün

---

![bg](../gorseller/3_normal_slayt.png)

# /etc/shadow Dosyası (devam)

### 📊 Alan Açıklamaları (5-9)

**sysadmin:$6$c75ekQWF$...:16874:5:30:7:60:15050::**

5. **Maksimum:** `30` - Şifrenin geçerlilik süresi (gün)
6. **Uyarı:** `7` - Bitişten 7 gün önce uyarı
7. **Pasif:** `60` - Bitişten sonra grace period (gün)
8. **Bitiş Tarihi:** `15050` - Hesap geçerlilik bitiş tarihi (Epoch)
9. **Rezerve:** Boş alan

---

![bg](../gorseller/3_normal_slayt.png)

# Şifre Yaşlandırma Politikaları

### ⏰ Zaman Bazlı Şifre Politikaları

**Politika Ayarları:** Minimum: 5 gün | Maksimum: 30 gün | Uyarı: 7 gün | Pasif: 60 gün

**Kullanıcı Kuralları:**
1. Her 30 günde şifre değiştirmek zorundadır
2. Değişiklikten sonra 5 gün beklemelidir
3. Bitiş tarihine 7 gün kala uyarılır
4. 60 gün grace period içinde şifre değiştirebilir

### 💡 Önemli Bilgiler

- **99999 = ~274 yıl:** Pratikte sonsuza kadar geçerli
- **Sistem Hesapları:** Genelde `*` karakteri içerir
- **Epoch:** 1 Ocak 1970 tarihinden gün sayısı
- **Hesap Kilidi:** Bitmiş hesap silinmez, yönetici açar

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Sistem Hesapları

---

![bg](../gorseller/3_normal_slayt.png)

# Sistem Hesapları

### 🖥️ Sistem Hesapları

Sistem hesapları kullanıcı girişi için tasarlanmamıştır, hizmetler için kullanılır:

<div class="two-columns">
<div>

### 🔍 Sistem Hesap Özellikleri

- **UID Aralığı:** 1-499 (veya 1000'den küçük)
- **Root UID:** 0 (özel yetkiler)
- **Regular Users:** UID > 500 (veya 1000+)
- **Home Dizin:** Genelde yok (dosya oluşturmazlar)

**Örnek:**
```bash
sshd:x:103:65534::/var/run/sshd:/usr/sbin/nologin
```

</div>
<div class="compare-box">

### ⚠️ Kullanıcı vs Sistem Hesabı

| Özellik | Sistem Hesabı | Kullanıcı Hesabı |
|---------|---------------|------------------|
| UID | 1-499 | 500+ (1000+) |
| Home | Yok veya özel | /home/kullanıcı |
| Shell | /usr/sbin/nologin | /bin/bash |
| Giriş | İmkansız | Mümkün |
| Amaç | Hesapları çalıştırır | Dosya oluşturur |

</div>
</div>

---

![bg](../gorseller/3_normal_slayt.png)

# Sistem Hesapları - /etc/passwd

### 📋 /etc/passwd - Sistem Hesabı

```bash
sshd:x:103:65534::/var/run/sshd:/usr/sbin/nologin
```

**Analiz:**
- Kullanıcı: sshd, UID: 103, GID: 65534
- Home: /var/run/sshd
- Shell: /usr/sbin/nologin (giriş yok)

---

![bg](../gorseller/3_normal_slayt.png)

# Sistem Hesapları - /etc/shadow

### 📋 /etc/shadow - Sistem Hesabı

```bash
sshd:*:16874:0:99999:7:::
```

### 💡 Önemli Gözlemler

- **Şifre Alanı:** `*` karakteri (şifre yok, giriş yok)
- **Çoğu Sistem Hesabı:** Gerekli olduğu için var olmalıdır
- **Silme:** Yöneticiler sistem hesaplarını silmemelidir (sorun yaratabilir)
- **Güvenlik:** Sistem hesaplarının güvenliğini sağlamak yöneticinin görevidir

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Grup Hesapları

---

![bg](../gorseller/3_normal_slayt.png)

# /etc/group Dosyası

### 👥 Grup Hesap Bilgileri

Her kullanıcı bir veya daha fazla gruba üye olabilir:

```bash
sysadmin@localhost:~$ cat /etc/group | grep mail
mail:x:12:mail,postfix
```

### 🔍 Alan Açıklamaları

**mail:x:12:mail,postfix**

1. **Grup Adı:** `mail` - Grubu tanımlayan benzersiz isim
2. **Şifre Yer Tutucusu:** `x` - Grup şifresi `/etc/gshadow` dosyasındadır
3. **Group ID (GID):** `12` - Benzersiz tanımlayıcı
4. **Üye Listesi:** `mail,postfix` - İkincil grup üyeleri (virgülle ayrılır)

---

![bg](../gorseller/3_normal_slayt.png)

# /etc/group Dosyası (devam)

### 💡 Birincil vs İkincil Grup Üyeliği

- **Birincil Grup:** /etc/passwd dosyasında tanımlı
- **İkincil Gruplar:** /etc/group dosyasında listelenir
- **Maksimum Grup:** 16 (eski UNIX) → 65000+ (yeni Linux)

---

![bg](../gorseller/3_normal_slayt.png)

# Grup Bilgisi Görüntüleme

### 🔍 Grup Arama Komutları

```bash
# grep ile arama
sysadmin@localhost:~$ grep sudo /etc/group
sudo:x:27:sysadmin

# getent ile görüntüleme
sysadmin@localhost:~$ getent group sudo
sudo:x:27:sysadmin
```

---

![bg](../gorseller/3_normal_slayt.png)

# Grup Bilgisi Görüntüleme (devam)

### 📊 Kullanıcı Grupları

```bash
sysadmin@localhost:~$ cat /etc/group | grep sysadmin
adm:x:4:syslog,sysadmin
sudo:x:27:sysadmin
sysadmin:x:1001:
```

<div class="highlight-box">

### 💡 Analiz

**sysadmin kullanıcının grupları:**
- **sysadmin (GID: 1001)** - Birincil grup
- **adm (GID: 4)** - İkincil grup
- **sudo (GID: 27)** - İkincil grup (yönetici yetkileri)

</div>

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Kullanıcı Bilgisi Görüntüleme

---

![bg](../gorseller/3_normal_slayt.png)

# id Komutu

### 🔍 Kullanıcı Bilgisi Görüntüleme

`id` komutu belirtilen kullanıcı için kullanıcı ve grup bilgilerini gösterir:

```bash
id [options] username
```

### 💡 Mevcut Kullanıcı Bilgisi

```bash
sysadmin@localhost:~$ id
uid=1001(sysadmin) gid=1001(sysadmin) groups=1001(sysadmin),4(adm),27(sudo)
```

### 📊 Çıktı Analizi

- **uid (User ID):** 1001(sysadmin) - Kullanıcının benzersiz kimlik numarası ve adı
- **gid (Group ID):** 1001(sysadmin) - Birincil grup ID'si ve grup adı
- **groups:** 1001,4,27 - Kullanıcının üye olduğu tüm grup ID'leri ve adları

---

![bg](../gorseller/3_normal_slayt.png)

# id Komutu - Seçenekler

### 🎯 Özellikler

**Belirli Kullanıcı:**
```bash
sysadmin@localhost:~$ id root
uid=0(root) gid=0(root) groups=0(root)
```

**Sadece Birincil Grup:**
```bash
sysadmin@localhost:~$ id -g
1001
```

**Tüm Gruplar:**
```bash
sysadmin@localhost:~$ id -G
1001 4 27
```

---

![bg](../gorseller/3_normal_slayt.png)

# id Komutu - Seçenekler (Tablo)

<div class="compare-box">

### 💡 Seçenekler

| Seçenek | Açıklama |
|---------|-----------|
| `-u` | User ID (varsayılan) |
| `-g` | Sadece birincil grup ID |
| `-G` | Tüm grup ID'leri |
| `-n` | Isimler yerine numeric ID'ler |
| `-r` | Real ID ve effective ID |

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# id Komutu - Doğrulama

### ✅ Grup Bilgisi Doğrulama

`id -G` çıktısı ile `/etc/group` dosyası karşılaştırması:

```bash
sysadmin@localhost:~$ id -G
1001 4 27

sysadmin@localhost:~$ cat /etc/group | grep sysadmin
adm:x:4:syslog,sysadmin
sudo:x:27:sysadmin
sysadmin:x:1001:
```

### 📊 Eşleştirme Sonucu

- **Grup ID 1001** → sysadmin (birincil grup)
- **Grup ID 4** → adm
- **Grup ID 27** → sudo

Tüm gruplar doğrulanmış ve `/etc/group` dosyasındaki bilgilerle tutarlı ✅

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Mevcut Kullanıcıları Görüntüleme

---

![bg](../gorseller/3_normal_slayt.png)

# who Komutu

### 👥 Sisteme Giriş Yapmış Kullanıcılar

`who` komutu sisteme giriş yapmış kullanıcıları, giriş yerlerini ve zamanlarını gösterir:

```bash
sysadmin@localhost:~$ who
root     	tty2        2013-10-11 10:00
sysadmin	tty1        2013-10-11 09:58 (:0)
sysadmin 	pts/0       2013-10-11 09:59 (:0.0)
sysadmin 	pts/1       2013-10-11 10:00 (example.com)
```

<div class="compare-box">

### 📊 Çıktı Alanları

| Alan | Açıklama |
|------|-----------|
| Username | Giriş yapmış kullanıcı adı |
| Terminal | Çalışılan terminal (tty = lokal, pts = pseudo) |
| Date | Giriş zamanı |
| Host | Giriş yeri (hostname = uzak, :0 = lokal grafik) |

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# who Komutu - Sistem Durumu

### 💡 Sistem Durum Bilgisi

```bash
sysadmin@localhost:~$ who -b -r
         system boot  	2013-10-11 09:54
         run-level 5    2013-10-11 09:54
```

### 🔍 Seçenekler

| Seçenek | Açıklama |
|---------|-----------|
| `-b` | Son boot zamanı |
| `-r` | Mevcut runlevel |
| `-a` | Tüm giriş bilgileri |
| `-H` | Column başlıkları |

---

![bg](../gorseller/3_normal_slayt.png)

# who Komutu - Terminal Tipleri

<div class="highlight-box">

### 📌 Terminal Tipleri

- **tty2 → Lokal Komut Satır** - Doğrudan konsol erişimi
- **:0 → Lokal Grafik** - Grafik arabirim üzerinden giriş
- **pts/0 → Pseudo Terminal** - SSH, terminal emulator vb.
- **(example.com) → Uzak Giriş** - Ağ üzerinden uzak sunucudan giriş

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# w Komutu

### 📊 Detaylı Kullanıcı Bilgisi

`w` komutu `who` komutundan daha detaylı bilgi sağlar:

```bash
sysadmin@localhost:~$ w
 10:44:03 up 50 min,  4 users,  load average: 0.78, 0.44, 0.19
USER     TTY      FROM      LOGIN@   IDLE   JCPU    PCPU   WHAT
root     tty2     -         10:00    43:44  0.01s   0.01s  -bash
sysadmin tty1     :0        09:58    50:02  5.68s   0.16s  pam: gdm
sysadmin pts/0    :0.0      09:59    0.00s  0.14s   0.13s  ssh 192.168.1.2
```

---

![bg](../gorseller/3_normal_slayt.png)

# w Komutu - Sistem Yükü

<div class="compare-box">

### 📊 Sistem Yükü (Load Average)

| Değer | Anlamı |
|-------|--------|
| 0.78 | Son 1 dakika |
| 0.44 | Son 5 dakika |
| 0.19 | Son 15 dakika |

**Tek Core:** 1.0 = %100 CPU | **Çok Core:** 1.0 / (core sayısı) = % kullanım

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# w Komutu - Alan Açıklamaları

### 🔍 Kullanıcı Aktivite Bilgileri

<div class="compare-box">

| Alan | Açıklama |
|------|-----------|
| USER | Kullanıcı adı |
| TTY | Terminal |
| FROM | Giriş yeri |
| LOGIN@ | Giriş zamanı |
| IDLE | Son komuttan beri boşta zamanı |
| JCPU | Toplam CPU zamanı (tüm processler) |
| PCPU | Mevcut process CPU zamanı |
| WHAT | Çalıştırılan komut/process |

</div>

### 💡 Önemli Kısaltmalar

- **s:** Saniye, **up 50 min:** Sistem 50 dk aktif
- **JCPU vs PCPU:** JCPU = toplam, PCPU = mevcut process

---

<!-- _class: topic-slide -->

![bg](../gorseller/2_Konu_baslik.png)

# Giriş Geçmişi

---

![bg](../gorseller/3_normal_slayt.png)

# last Komutu

### 📜 Tüm Giriş Geçmişi

`last` komutu `/var/log/wtmp` dosyasından tüm giriş geçmişini okur:

```bash
sysadmin@localhost:~$ last
sysadmin console Tue Sep 18 02:31   still logged in
sysadmin console                    Tue Sep 18 02:31 - 02:31  (00:00)
wtmp begins Tue Sep 18 02:31:57 2018
```

---

![bg](../gorseller/3_normal_slayt.png)

# last Komutu - Çıktı Analizi

### 🔍 Çıktı Alanları

- **Username:** Giriş yapmış kullanıcı
- **Terminal:** Kullanılan terminal
- **Date/Time:** Giriş tarihi ve saati
- **still logged in:** Hala aktif | **(00:00):** Oturum süresi

---

![bg](../gorseller/3_normal_slayt.png)

# last Komutu - Log Dosyaları

<div class="info-box">

### 💡 Log Dosyaları

- **who** → `/var/log/utmp` (Mevcut kullanıcılar)
- **last** → `/var/log/wtmp` (Tüm geçmiş)
- **lastb** → `/var/log/btmp` (Başarısız girişler)

Bu dosyalar sistem aktivitesi ve güvenlik izlemesi için kritiktir.

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# last Komutu - Özellikler

### 🎯 Kullanım Senaryoları

<div class="highlight-box">

### 💡 Pratik Kullanımlar - 1

**Son 10 Giriş:**
```bash
last | head -10
```

**Belirli Kullanıcı:**
```bash
last sysadmin
```

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# last Komutu - Özellikler

### 🎯 Kullanım Senaryoları

<div class="highlight-box">

### 💡 Pratik Kullanımlar - 2

**Reboot Kayıtları:**
```bash
last reboot
```

**Başarısız Girişler:**
```bash
lastb
```

</div>

---

![bg](../gorseller/3_normal_slayt.png)

# last Komutu - Karşılaştırma

### 🔍 who vs w vs last

| Komut | Odak | Kaynak | Zaman |
|-------|------|--------|-------|
| **who** | Mevcut oturumlar | /var/log/utmp | Anlık |
| **w** | Mevcut + detay | /var/log/utmp | Anlık |
| **last** | Tüm geçmiş | /var/log/wtmp | Geçmiş |

---

<!-- _class: final-slide -->

# Teşekkürler!

**Kapadokya Üniversitesi**
Yönetim Bilişim Sistemleri Bölümü
