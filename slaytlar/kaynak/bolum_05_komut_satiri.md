---
marp: true
theme: default
paginate: true
lang: tr
backgroundColor: #F7F7F7
style: |
  @import url('https://fonts.googleapis.com/css2?family=Trebuchet+MS:wght@400;700&display=swap');

  section {
    font-family: 'Trebuchet MS', Arial, sans-serif;
    font-size: 90%;
    padding: 30px 50px;
    background-color: #F7F7F7;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  /* Logo kaldırıldı - sol üst köşede logo görünmeyecek */

  h1 {
    color: #2D4A7C;
    font-size: 24pt;
    font-weight: bold;
    margin-bottom: 20px;
    border-bottom: 3px solid #6B9FE8;
    padding-bottom: 10px;
  }

  h2 {
    color: #2D4A7C;
    font-size: 16pt;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 15px;
  }

  h3 {
    color: #2D4A7C;
    font-size: 13pt;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 10px;
  }

  p, li {
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
  }

  ul, ol {
    margin-left: 20px;
    max-height: 500px;
    overflow: hidden;
  }

  strong {
    color: #2D4A7C;
    font-weight: bold;
  }

  code {
    background-color: #1a1a1a;
    color: #e0e0e0;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 10pt;
  }

  pre {
    background-color: #1a1a1a;
    color: #e0e0e0;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    overflow: hidden;
    overflow: hidden;
    max-height: 400px;
  }

  pre code {
    background: none;
    padding: 0;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 10pt;
    line-height: 1.5;
  }

  .two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-top: 20px;
  }

  .subtitle-box {
    background-color: #E6EAF3;
    padding: 15px 18px;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    margin-top: 20px;
  }

  .info-box {
    background-color: #FFFFFF;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    margin-top: 15px;
  }

  .highlight-box {
    background-color: #6B9FE8;
    color: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 3px solid #4A90E2;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
    margin-top: 15px;
  }

  .highlight-box h1,
  .highlight-box h2,
  .highlight-box h3,
  .highlight-box p,
  .highlight-box strong,
  .highlight-box li {
    color: white !important;
  }

  .compare-box {
    background-color: #F5F5F5;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  }

  /* 1. SLAYT: Ders Başlığı */
  section.cover-slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
    padding-left: 80px;
    background: linear-gradient(135deg, #F7F7F7 0%, #E6EAF3 100%);
    position: relative;
  }

  section.cover-slide h1 {
    color: white;
    font-size: 36pt;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    border-bottom: none;
  }

  section.cover-slide p {
    position: absolute;
    bottom: 40px;
    right: 60px;
    color: white;
    font-size: 18pt;
    font-weight: normal;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
  }

  /* 2. SLAYT: Haftalık Konu */
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
    font-size: 36pt;
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
    font-size: 18pt;
    font-weight: normal;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
  }

  /* SON SLAYT: Kapanış */
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
    content: '';
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 150px;
    height: 75px;
    background-image: url('../gorseller/1_ana_slayt.png');
    background-size: contain;
    background-repeat: no-repeat;
    filter: brightness(0) invert(1);
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

  img {
    max-width: 100%;
    max-height: 400px;
    object-fit: contain;
  }

---

<!-- 1. SLAYT: DERS BAŞLIĞI -->
<!-- _class: cover-slide -->
<!-- _paginate: false -->

![bg](../gorseller/1_ana_slayt.png)

# İşletim Sistemleri

Dr. Bekir Ağırgün

---

<!-- 2. SLAYT: HAFTALIK KONU -->
<!-- _class: topic-slide -->
<!-- _paginate: false -->

![bg](../gorseller/2_Konu_baslik.png)

# The Linux Command Line

Dr. Bekir Ağırgün

---

# 1️⃣ CLI'ya Giriş (Introduction to CLI)

<div class="two-columns">

<div>

## 💡 Neden CLI?

- **Güç ve Hız:** Tek komutla karmaşık işlemler
- **Otomasyon:** Script ile otomatik görevler
- **Evrensellik:** Tüm Linux dağıtımlarında aynı
- **Verimlilik:** GUI'den daha hızlı çalışma

</div>

<div class="highlight-box">

### 🎯 Önemli Nokta

CLI öğrenmek başta zor görünse de, komut yapısını ve dosya sistemini öğrendikten sonra **inanılmaz üretken** olabilirsiniz.

</div>

</div>

<div class="info-box">

**Avantajlar:**
- Daha kesin kontrol
- Daha yüksek hız
- Script ile otomasyon kolaylığı
- Farklı Linux dağıtımlarında anında verimli çalışma

</div>

---

# 2️⃣ Shell Nedir?

<div class="two-columns">

<div class="info-box">

### 🐚 Shell Tanımı

**Shell**, kullanıcının girdiği komutları işletim sistemine çeviren **komut satırı yorumlayıcısıdır**.

**İş Akışı:**
1. Kullanıcı komutu yazar
2. Terminal komutu shell'e iletir
3. Shell komutu yorumlar
4. İşletim sistemi işlemi gerçekleştirir

</div>

<div>

### 🔷 Bash Shell Özellikleri

- **Scripting:** Komutları dosyaya kaydetme
- **Aliases:** Kısa komut takma adları
- **Variables:** Bilgi saklama
- **Command History:** Geçmiş komutları hatırlama
- **Inline Editing:** Komutları düzenleme

</div>

</div>

<div class="highlight-box">

**En Yaygın Shell:** Linux dağıtımlarında **Bash (Bourne Again Shell)** kullanılır.

</div>

---

# 3️⃣ Prompt Yapısı

<div class="info-box">

### 📟 Prompt Nedir?

**Prompt**, komut girebileceğinizi gösteren işarettir ve kullanışlı bilgiler içerir.

</div>

<div class="two-columns">

<div>

### Tipik Prompt Yapısı

```
sysadmin@localhost:~$
```

**Bileşenler:**
- `sysadmin` → Kullanıcı adı
- `@` → Ayırıcı
- `localhost` → Sistem adı
- `:` → Ayırıcı
- `~` → Mevcut dizin (home)
- `$` → Normal kullanıcı işareti

</div>

<div class="compare-box">

### 💡 Özel Semboller

**`~` Sembolü:**
- Kullanıcının home dizinini temsil eder
- Genellikle `/home/kullaniciadi` şeklindedir
- Örnek: `/home/sysadmin`

**`$` vs `#`:**
- `$` → Normal kullanıcı
- `#` → Root (süper kullanıcı)

</div>

</div>

---

# 4️⃣ Komutların Temel Yapısı

<div class="info-box">

### 📝 Komut Formatı

```
komut [seçenekler] [argümanlar]
```

</div>

<div class="two-columns">

<div>

### Komut Örnekleri

```
# Basit komut
ls

# Seçenekli komut
ls -l

# Argümanlı komut
ls /etc

# Tam format
ls -l /etc/ppp
```

</div>

<div class="highlight-box">

### ⚠️ Önemli Kurallar

- Linux **büyük/küçük harf duyarlıdır**
- Seçenekler ve argümanlar **boşlukla** ayrılır
- Seçenekler genellikle **birleştirilebilir**
- `-l -r` = `-lr` = `-rl`

</div>

</div>

---

# 5️⃣ Argümanlar (Arguments)

<div class="two-columns">

<div>

### 🎯 Argüman Nedir?

Komutun **üzerinde işlem yapacağı hedefi** belirtir.

### Tek Argüman

```
ls /etc/ppp
```

**Çıktı:**
```
ip-down.d  ip-up.d
```

</div>

<div>

### Çoklu Argüman

```
ls /etc/ppp /etc/ssh
```

**Çıktı:**
```
/etc/ppp:
ip-down.d  ip-up.d

/etc/ssh:
moduli               ssh_host_dsa_key.pub
ssh_config           ssh_host_rsa_key
ssh_host_ecdsa_key   sshd_config
```

</div>

</div>

---

# 6️⃣ Seçenekler (Options)

<div class="two-columns">

<div>

### ⚙️ Seçenek Nedir?

Komutun **davranışını değiştirir** veya **genişletir**.

### `-l` Seçeneği (Long Listing)

```
ls -l
```

**Çıktı:**
```
drwxr-xr-x 1 sysadmin sysadmin 0 Desktop
drwxr-xr-x 1 sysadmin sysadmin 0 Documents
drwxr-xr-x 1 sysadmin sysadmin 0 Downloads
```

</div>

<div>

### Seçenekleri Birleştirme

```
# Ayrı seçenekler
ls -l -r

# Birleştirilmiş seçenekler
ls -lr
ls -rl  # Sıra önemli değil
```

<div class="highlight-box">

### 💡 Mnemonic (Hatırlatıcı)

- `-l` → **l**ong (uzun liste)
- `-r` → **r**everse (ters sıra)
- `-h` → **h**uman-readable (okunabilir)

</div>

</div>

</div>

---

# 7️⃣ Kısa ve Uzun Seçenekler

<div class="two-columns">

<div class="info-box">

### 📏 Kısa Seçenekler

**Format:** Tek tire `-` + tek harf

```
ls -l
ls -h
ls -r
ls -lhr  # Birleştirilebilir
```

**Özellikler:**
- Genellikle eski komutlarda
- Tek karakter
- Birleştirilebilir

</div>

<div class="info-box">

### 📐 Uzun Seçenekler

**Format:** İki tire `--` + kelime

```
ls --human-readable
ls --reverse
ls --all
```

**Özellikler:**
- Yeni komutlarda yaygın
- Daha açıklayıcı
- Birleştirilemez

</div>

</div>

<div class="compare-box">

### 🔄 Eşdeğer Seçenekler

```
ls -h        # Kısa format
ls --human-readable   # Uzun format (aynı işlev)
```

</div>

---

# 8️⃣ Komut Geçmişi (History)

<div class="two-columns">

<div>

### 📜 History Özellikleri

- Her komut **otomatik kaydedilir**
- **↑** (Yukarı ok): Önceki komut
- **↓** (Aşağı ok): Sonraki komut
- **←** **→**: Düzenleme için
- **Enter**: Komutu çalıştır

### Klavye Kısayolları

- **Home**: Satır başı
- **End**: Satır sonu
- **Backspace**: Sil (geri)
- **Delete**: Sil (ileri)

</div>

<div>

### `history` Komutu

```
history
```

**Çıktı:**
```
1  date
2  ls
3  cal 5 2030
4  history
```

### Geçmişten Çalıştırma

```
!3        # 3. komutu çalıştır
!!        # Son komutu çalıştır
!-3       # Sondan 3. komutu çalıştır
!ls       # Son ls komutunu çalıştır
```

</div>

</div>

---

# 9️⃣ Değişkenler (Variables) - Giriş

<div class="info-box">

### 🔢 Değişken Nedir?

Kullanıcının veya shell'in **veri saklamasını** sağlayan özelliktir. Sistem bilgisi sağlar veya komut davranışını değiştirir.

</div>

<div class="two-columns">

<div>

### 📌 İki Tür Değişken

**1. Yerel (Local) Değişkenler**
- Sadece mevcut shell'de geçerli
- Küçük harfle yazılır (convention)
- Shell kapanınca kaybolur

**2. Çevre (Environment) Değişkenleri**
- Tüm sistem genelinde geçerli
- Büyük harfle yazılır
- Sistem otomatik oluşturur

</div>

<div class="highlight-box">

### 💡 Önemli Nokta

Değişkenler geçici bellekte saklanır. Shell kapandığında yerel değişkenler kaybolur, ancak çevre değişkenleri yeni shell'de yeniden oluşturulur.

</div>

</div>

---

# 🔟 Yerel Değişkenler (Local Variables)

<div class="two-columns">

<div>

### 📝 Yerel Değişken Oluşturma

```
# Değişken tanımlama
variable1='Something'

# Değişken değerini gösterme
echo $variable1
```

**Çıktı:**
```
Something
```

</div>

<div class="info-box">

### ⚙️ Özellikler

- Sadece **mevcut shell'de** geçerli
- Diğer komutları **etkilemez**
- Shell **kapatılınca kaybolur**
- Genellikle **küçük harfle** yazılır

### Sözdizimi

```
degisken_adi=deger
```

**⚠️ Dikkat:** `=` işaretinin **etrafında boşluk yok!**

</div>

</div>

---

# 1️⃣1️⃣ Çevre Değişkenleri (Environment Variables)

<div class="two-columns">

<div>

### 🌍 Çevre Değişkenleri

```
# Değişken değerini göster
echo $HISTSIZE
```

**Çıktı:**
```
1000
```

### Değeri Değiştirme

```
# HISTSIZE değişkenini değiştir
HISTSIZE=500

# Kontrol et
echo $HISTSIZE
```

**Çıktı:**
```
500
```

</div>

<div class="highlight-box">

### 💡 Önemli Örnekler

- **`PATH`**: Komutların arandığı dizinler
- **`HOME`**: Kullanıcı home dizini
- **`HISTSIZE`**: Geçmiş listesi boyutu
- **`USER`**: Mevcut kullanıcı adı
- **`SHELL`**: Kullanılan shell

</div>

</div>

<div class="info-box">

**Özellikler:**
- **Sistem genelinde** geçerli
- **Büyük harfle** yazılır
- Yeni shell'de **otomatik oluşturulur**

</div>

---

# 1️⃣2️⃣ `export` Komutu

<div class="two-columns">

<div>

### 📤 Yerel → Çevre Değişkeni

```
# Yerel değişken oluştur
variable1='Something'

# Çevre değişkenine çevir
export variable1

# Kontrol et
env | grep variable1
```

**Çıktı:**
```
variable1=Something
```

</div>

<div>

### Doğrudan Export

```
# Oluştururken export et
export variable2='Else'

# Kontrol et
env | grep variable2
```

**Çıktı:**
```
variable2=Else
```

### Değişkeni Kaldırma

```
unset variable2
```

</div>

</div>

---

# 1️⃣3️⃣ PATH Değişkeni

<div class="info-box">

### 🛤️ PATH Nedir?

Shell'in **komutları aradığı dizinlerin listesidir**. Komut bulunamazsa "command not found" hatası verir.

</div>

<div class="two-columns">

<div>

### PATH'i Görüntüleme

```
echo $PATH
```

**Çıktı:**
```
/home/sysadmin/bin:/usr/local/sbin:
/usr/local/bin:/usr/sbin:/usr/bin:
/sbin:/bin:/usr/games
```

</div>

<div class="compare-box">

### 📂 Dizin Listesi

1. `/home/sysadmin/bin`
2. `/usr/local/sbin`
3. `/usr/local/bin`
4. `/usr/sbin`
5. `/usr/bin`
6. `/sbin`
7. `/bin`
8. `/usr/games`

**Not:** Dizinler **`:`** ile ayrılır

</div>

</div>

---

# 1️⃣4️⃣ PATH Değişkenini Güncelleme

<div class="two-columns">

<div>

### ➕ Yeni Dizin Ekleme

```
# PATH'e yeni dizin ekle
PATH=/usr/bin/custom:$PATH

# Kontrol et
echo $PATH
```

**Çıktı:**
```
/usr/bin/custom:/home/sysadmin/bin:
/usr/local/sbin:/usr/local/bin:
/usr/sbin:/usr/bin:/sbin:/bin
```

</div>

<div class="highlight-box">

### ⚠️ Kritik Uyarı

PATH'i güncellerken **mutlaka mevcut PATH'i dahil edin** (`$PATH`). Aksi halde diğer dizinlerdeki komutlara erişimi kaybedersiniz!

**Doğru:**
```
PATH=/new/dir:$PATH
```

**Yanlış:**
```
PATH=/new/dir  # Eski PATH kaybolur!
```

</div>

</div>

---

# 1️⃣5️⃣ Komut Türleri (Command Types)

<div class="info-box">

### 🔍 `type` Komutu

Komutun **kaynağını** ve **türünü** öğrenmek için kullanılır.

```
type komut_adi
```

</div>

<div class="two-columns">

<div class="compare-box">

### 🔧 Komut Türleri

1. **Internal (Built-in)**: Shell'e gömülü
2. **External**: Ayrı çalıştırılabilir dosyalar
3. **Alias**: Kısa takma adlar
4. **Function**: Komut grupları

</div>

<div>

### Örnekler

```
type cd
# cd is a shell builtin

type ls
# ls is /bin/ls

type ll
# ll is aliased to `ls -alF'
```

</div>

</div>

---

# 1️⃣6️⃣ Dahili Komutlar (Internal Commands)

<div class="two-columns">

<div class="info-box">

### 🏠 Built-in Commands

Shell'in **içine gömülü** komutlardır. Ek program başlatmaya gerek yoktur.

### Örnek: `cd` Komutu

```
type cd
```

**Çıktı:**
```
cd is a shell builtin
```

**Özellikler:**
- Shell'e entegre
- Daha hızlı çalışır
- Ek dosya gerektirmez

</div>

<div class="highlight-box">

### 💡 Yaygın Built-in Komutlar

- `cd` - Dizin değiştirme
- `echo` - Metin yazdırma
- `export` - Değişken export etme
- `alias` - Takma ad oluşturma
- `history` - Komut geçmişi
- `pwd` - Mevcut dizin
- `exit` - Shell'den çıkış

</div>

</div>

---

# 1️⃣7️⃣ Harici Komutlar (External Commands)

<div class="two-columns">

<div>

### 🗂️ External Commands

PATH dizinlerinde bulunan **ayrı çalıştırılabilir dosyalardır**.

### `which` Komutu

```
which ls
```

**Çıktı:**
```
/bin/ls
```

```
which cal
```

**Çıktı:**
```
/usr/bin/cal
```

</div>

<div>

### Tam Yol ile Çalıştırma

```
/bin/ls
```

**Çıktı:**
```
Desktop  Documents  Downloads
Music    Pictures   Public
```

<div class="info-box">

### `type` ile Kontrol

```
type cal
```

**Çıktı:**
```
cal is /usr/bin/cal
```

</div>

</div>

</div>

---

# 1️⃣8️⃣ `type -a` Komutu

<div class="two-columns">

<div>

### 🔍 Tüm Konumları Gösterme

Bazı komutlar hem **built-in** hem de **external** olabilir.

### Örnek: `echo`

```
type echo
```

**Çıktı:**
```
echo is a shell builtin
```

```
which echo
```

**Çıktı:**
```
/bin/echo
```

</div>

<div class="highlight-box">

### `-a` Seçeneği

```
type -a echo
```

**Çıktı:**
```
echo is a shell builtin
echo is /bin/echo
```

**Açıklama:**
- İlk satır: Built-in versiyonu
- İkinci satır: External versiyonu
- Shell **önce built-in'i** kullanır

</div>

</div>

---

# 1️⃣9️⃣ Takma Adlar (Aliases)

<div class="two-columns">

<div class="info-box">

### 🏷️ Alias Nedir?

Uzun komutları **kısa tuş dizilerine** eşleme. Daha hızlı çalışma imkanı.

### Mevcut Aliasları Görme

```
alias
```

**Çıktı:**
```
alias egrep='egrep --color=auto'
alias grep='grep --color=auto'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'
```

</div>

<div>

### Yeni Alias Oluşturma

```
# Format
alias isim=komut

# Örnek
alias mycal="cal 2019"

# Kullanım
mycal
```

**Çıktı:**
```
     2019
January  February  March
...
```

</div>

</div>

---

# 2️⃣0️⃣ Alias Özellikleri

<div class="two-columns">

<div>

### ⏱️ Geçicilik

**Aliaslar geçicidir:**
- Shell açıkken geçerli
- Shell kapanınca kaybolur
- Her shell'in kendi aliasları var

### `type` ile Kontrol

```
type ll
```

**Çıktı:**
```
ll is aliased to `ls -alF'
```

```
type -a ls
```

**Çıktı:**
```
ls is aliased to `ls --color=auto'
ls is /bin/ls
```

</div>

<div class="highlight-box">

### 💡 Kalıcı Alias

Aliasları **kalıcı** yapmak için initialization dosyalarına eklemelisiniz:

- `~/.bashrc`
- `~/.bash_aliases`
- `~/.profile`

**Örnek:**
```
# .bashrc dosyasına ekle
alias ll='ls -alF'
alias la='ls -A'
alias mycal='cal 2025'
```

</div>

</div>

---

# 2️⃣1️⃣ Fonksiyonlar (Functions)

<div class="two-columns">

<div>

### 🔧 Function Syntax

```
function_name () {
   commands
}
```

### Örnek Function

```
my_report () {
  ls Documents
  date
  echo "Document directory report"
}
```

</div>

<div>

### Function Çalıştırma

```
my_report
```

**Çıktı:**
```
School  Work  adjectives.txt
alpha-first.txt  animals.txt
Wed Oct 13 06:54:04 UTC 2021
Document directory report
```

<div class="info-box">

**Özellikler:**
- Birden fazla komut çalıştırır
- Alias'tan daha gelişmiş
- Script'lerde yaygın kullanılır

</div>

</div>

</div>

---

# 2️⃣2️⃣ Alıntılama (Quoting) - Çift Tırnak

<div class="two-columns">

<div class="info-box">

### 📝 Üç Tür Tırnak

1. **Çift tırnak** `"`
2. **Tek tırnak** `'`
3. **Ters tırnak** `` ` ``

Her birinin **özel anlamı** vardır.

</div>

<div>

### "" Çift Tırnak

**Bazı özel karakterleri** durdurur (**glob karakterleri**), ama **değişkenlere izin verir**.

```
echo "The glob characters are *, ? and [ ]"
```

**Çıktı:**
```
The glob characters are *, ? and [ ]
```

```
echo "The path is $PATH"
```

**Çıktı:**
```
The path is /usr/bin:/usr/local/bin:...
```

</div>

</div>

---

# 2️⃣3️⃣ Tek Tırnak (Single Quotes)

<div class="two-columns">

<div>

### '' Tek Tırnak

**Tüm özel karakterleri** durdurur. Değişkenler dahil **hiçbir şey yorumlanmaz**.

### Hatalı Kullanım

```
echo The car costs $100
```

**Çıktı:**
```
The car costs 00
```

**Problem:** `$1` ve `$00` değişken olarak algılandı.

</div>

<div class="highlight-box">

### ✅ Doğru Kullanım

```
echo 'The car costs $100'
```

**Çıktı:**
```
The car costs $100
```

**Açıklama:** Tek tırnak içinde `$` sadece bir karakterdir, değişken değildir.

</div>

</div>

---

# 2️⃣4️⃣ Backslash Karakteri

<div class="two-columns">

<div>

### \\ Backslash

**Tek bir karakteri** özel anlamından çıkarır.

### Problem

```
echo "The service costs $1 and path is $PATH"
```

**Çıktı:**
```
The service costs  and path is /usr/bin:...
```

</div>

<div class="highlight-box">

### ✅ Çözüm

```
echo The service costs \$1 and path is $PATH
```

**Çıktı:**
```
The service costs $1 and path is /usr/bin:...
```

**Açıklama:**
- `\$1` → `$1` olarak yazdırılır (değişken değil)
- `$PATH` → Değişken olarak yorumlanır

</div>

</div>

---

# 2️⃣5️⃣ Ters Tırnak (Backquotes)

<div class="two-columns">

<div class="info-box">

### `` ` `` Ters Tırnak (Backticks)

**Komut ikamesi** (command substitution) için kullanılır. Bir komutun çıktısını başka bir komuta gömme.

</div>

<div>

### Örnek 1

```
date
```

**Çıktı:**
```
Mon Nov 4 03:35:50 UTC 2018
```

```
echo Today is date
```

**Çıktı:**
```
Today is date
```

</div>

</div>

<div class="highlight-box">

### ✅ Doğru Kullanım

```
echo Today is `date`
```

**Çıktı:**
```
Today is Mon Nov 4 03:40:04 UTC 2018
```

</div>

---

# 2️⃣6️⃣ Kontrol İfadeleri - Noktalı Virgül

<div class="two-columns">

<div class="info-box">

### ; Noktalı Virgül

Birden fazla komutu **sırayla** çalıştırır. Her komut **bağımsız** çalışır.

```
komut1; komut2; komut3
```

</div>

<div>

### Örnek

```
cal 1 2030; cal 2 2030; cal 3 2030
```

**Çıktı:**
```
   January 2030
Su Mo Tu We Th Fr Sa
      1  2  3  4  5
 6  7  8  9 10 11 12
...

  February 2030
Su Mo Tu We Th Fr Sa
               1  2
 3  4  5  6  7  8  9
...

    March 2030
Su Mo Tu We Th Fr Sa
               1  2
 3  4  5  6  7  8  9
...
```

</div>

</div>

---

# 2️⃣7️⃣ Çift Ampersand (&&)

<div class="two-columns">

<div class="info-box">

### && Mantıksal "VE"

**İlk komut başarılıysa** ikinci komutu çalıştırır. İlk komut **başarısızsa** ikinci komut **çalışmaz**.

```
komut1 && komut2
```

</div>

<div>

### Başarılı Örnek

```
ls /etc/ppp && echo success
```

**Çıktı:**
```
ip-down.d  ip-up.d
success
```

### Başarısız Örnek

```
ls /etc/junk && echo success
```

**Çıktı:**
```
ls: cannot access /etc/junk: No such file or directory
```

**Not:** `echo` çalışmadı.

</div>

</div>

---

# 2️⃣8️⃣ Çift Pipe (||)

<div class="two-columns">

<div class="info-box">

### || Mantıksal "VEYA"

**İlk komut başarılıysa** ikinci komut **atlanır**. İlk komut **başarısızsa** ikinci komut **çalışır**.

```
komut1 || komut2
```

"Ya ilk komutu çalıştır **ya da** ikinci komutu"

</div>

<div>

### Başarılı Örnek

```
ls /etc/ppp || echo failed
```

**Çıktı:**
```
ip-down.d  ip-up.d
```

**Not:** `echo` çalışmadı.

### Başarısız Örnek

```
ls /etc/junk || echo failed
```

**Çıktı:**
```
ls: cannot access /etc/junk: No such file or directory
failed
```

</div>

</div>

---

# 2️⃣9️⃣ 💡 Pratik Örnek: `ls` Komutları

<div class="two-columns">

<div>

### Temel Kullanım

```
# Basit liste
ls

# Uzun format
ls -l

# Gizli dosyaları göster
ls -a

# Tümünü birlikte
ls -la
```

</div>

<div>

### İleri Seviye

```
# İnsan okunabilir boyutlar
ls -lh

# Ters sıralama (tarihe göre)
ls -lt

# Boyuta göre sırala
ls -lS

# Rekürsif liste
ls -R
```

</div>

</div>

<div class="highlight-box">

### 🎯 Best Practice Kombinasyon

```
ls -lhSr    # Uzun, okunabilir, boyuta göre, ters sıralı
```

</div>

---

# 3️⃣0️⃣ 💡 Pratik Örnek: `echo` ile Çalışma

<div class="two-columns">

<div>

### Basit Kullanım

```
# Metin yazdır
echo "Hello World"

# Değişken göster
echo $HOME

# Çoklu değişken
echo "User: $USER, Home: $HOME"
```

</div>

<div>

### İleri Kullanım

```
# Yeni satır ekle
echo -e "Line 1\nLine 2"

# Yeni satır ekleme
echo -n "No newline"

# Renkli çıktı
echo -e "\033[31mRed Text\033[0m"
```

</div>

</div>

<div class="info-box">

### Gerçek Dünya Senaryosu

```
# Sistem bilgisi raporu
echo "=== System Report ==="
echo "User: $USER"
echo "Date: `date`"
echo "Uptime: `uptime -p`"
```

</div>

---

# 3️⃣1️⃣ 💡 PATH Manipülasyonu Senaryoları

<div class="two-columns">

<div>

### Senaryo 1: Özel Script Dizini

```
# Scripts klasörünü PATH'e ekle
mkdir -p ~/scripts
PATH=$HOME/scripts:$PATH

# Script oluştur
cat > ~/scripts/backup.sh << 'EOF'
#!/bin/bash
echo "Backup başladı..."
tar -czf backup.tar.gz Documents/
echo "Backup tamamlandı!"
EOF

# Çalıştırılabilir yap
chmod +x ~/scripts/backup.sh

# Artık her yerden çalışır
backup.sh
```

</div>

<div class="highlight-box">

### 🎯 Önemli Notlar

**PATH sırası önemlidir:**
```
# Önce custom, sonra sistem
PATH=/custom:$PATH

# Önce sistem, sonra custom
PATH=$PATH:/custom
```

**Kalıcı yapmak için:**
```
# ~/.bashrc dosyasına ekle
echo 'export PATH=$HOME/scripts:$PATH' >> ~/.bashrc
source ~/.bashrc
```

</div>

</div>

---

# 3️⃣2️⃣ 💡 Gerçek Dünya Alias Örnekleri

<div class="two-columns">

<div>

### Sistem Yöneticisi Aliasları

```
# Güvenli silme (onay iste)
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Disk kullanımı
alias duh='du -h --max-depth=1'
alias dfh='df -h'

# Ağ kontrolü
alias ports='netstat -tulanp'
```

</div>

<div>

### Geliştirici Aliasları

```
# Git kısayolları
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'

# Python virtual env
alias venv='python3 -m venv'
alias activate='source venv/bin/activate'
```

</div>

</div>

<div class="info-box">

### ~/.bashrc'ye Ekle

```
# ~/.bashrc dosyasının sonuna ekle
source ~/.bashrc  # Değişiklikleri yükle
```

</div>

---

# 3️⃣3️⃣ 💡 Pratik Function Örnekleri

<div class="two-columns">

<div>

### Sistem Bilgisi Fonksiyonu

```
sysinfo() {
  echo "=== System Information ==="
  echo "Hostname: $(hostname)"
  echo "OS: $(uname -s)"
  echo "Kernel: $(uname -r)"
  echo "Uptime: $(uptime -p)"
  echo "Memory: $(free -h | grep Mem | awk '{print $3"/"$2}')"
  echo "Disk: $(df -h / | tail -1 | awk '{print $3"/"$2" ("$5")"}')"
}
```

</div>

<div>

### Backup Fonksiyonu

```
backup() {
  local source=$1
  local dest=$2

  if [ -z "$source" ] || [ -z "$dest" ]; then
    echo "Usage: backup <source> <dest>"
    return 1
  fi

  echo "Backing up $source to $dest..."
  tar -czf "$dest/backup-$(date +%Y%m%d-%H%M%S).tar.gz" "$source"
  echo "Backup complete!"
}

# Kullanım
backup ~/Documents ~/Backups
```

</div>

</div>

---

# 3️⃣4️⃣ 💡 Komut Zinciri Best Practices

<div class="two-columns">

<div>

### Güvenli Komut Zincirleri

```
# Dizin oluştur VE içine gir
mkdir myproject && cd myproject

# Dosya varsa yedekle
[ -f file.txt ] && cp file.txt file.txt.bak

# İndirme başarılıysa aç
wget file.zip && unzip file.zip
```

</div>

<div>

### Hata Yönetimi

```
# Başarısızsa hata mesajı
ls /invalid || echo "Directory not found!"

# Başarılıysa devam et, değilse dur
cd /project && make && make install

# Karmaşık kontrol
cd /project && \
  make clean && \
  make && \
  make test && \
  sudo make install || \
  echo "Build failed!"
```

</div>

</div>

---

# 3️⃣5️⃣ 💡 Değişken Kullanım Senaryoları

<div class="two-columns">

<div>

### Script'te Konfigürasyon

```
#!/bin/bash

# Konfigürasyon değişkenleri
BACKUP_DIR="/var/backups"
LOG_FILE="/var/log/backup.log"
DATE=$(date +%Y%m%d)

# Kullanım
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/backup-$DATE.tar.gz" /home
echo "Backup completed: $DATE" >> "$LOG_FILE"
```

</div>

<div>

### Dinamik Dosya Adları

```
# Tarih damgalı dosyalar
today=$(date +%Y-%m-%d)
logfile="app-${today}.log"
echo "Log started" > $logfile

# Rastgele isimler
tmpfile="/tmp/myapp-$$.tmp"
echo "Processing..." > $tmpfile

# Kullanıcı özel
config="$HOME/.myapp/config-$USER.conf"
```

</div>

</div>

---

# 3️⃣6️⃣ 💡 Script Yazma Temelleri

<div class="two-columns">

<div>

### Basit Backup Script

```
#!/bin/bash
# backup.sh - Basit backup scripti

SOURCE_DIR="$HOME/Documents"
BACKUP_DIR="$HOME/Backups"
DATE=$(date +%Y%m%d-%H%M%S)

# Backup dizinini oluştur
mkdir -p "$BACKUP_DIR"

# Backup yap
tar -czf "$BACKUP_DIR/docs-$DATE.tar.gz" "$SOURCE_DIR"

echo "Backup tamamlandı: docs-$DATE.tar.gz"
```

</div>

<div>

### Kullanım ve İzinler

```
# Script'i oluştur
nano backup.sh

# Çalıştırılabilir yap
chmod +x backup.sh

# Çalıştır
./backup.sh

# PATH'e ekle
mv backup.sh ~/scripts/
backup.sh  # Artık her yerden çalışır
```

</div>

</div>

<div class="highlight-box">

### 🎯 Script Best Practices
- Her zaman `#!/bin/bash` ile başla
- Değişkenleri BÜYÜK_HARF ile yaz
- Hata kontrolü ekle
- Yorum satırları kullan

</div>

---

# 3️⃣7️⃣ 💡 Hata Ayıklama Teknikleri

<div class="two-columns">

<div>

### Debug Mode

```
# Script'i debug modda çalıştır
bash -x script.sh

# Script içinde debug aç
#!/bin/bash
set -x  # Debug açık
ls /etc
set +x  # Debug kapalı
```

### Verbose Output

```
#!/bin/bash
set -v  # Her satırı göster
echo "Starting..."
ls /etc
echo "Done"
```

</div>

<div>

### Hata Yakalama

```
#!/bin/bash
set -e  # Hata durumunda dur

# Hata fonksiyonu
error_exit() {
  echo "ERROR: $1" >&2
  exit 1
}

# Kullanım
cd /invalid/path || error_exit "Directory not found"
```

</div>

</div>

<div class="info-box">

### Faydalı Debug Komutları

```
echo "Debug: Variable is $VAR"
echo "Current directory: $(pwd)"
echo "Script name: $0"
```

</div>

---

# 3️⃣8️⃣ 💡 Performans İpuçları

<div class="two-columns">

<div>

### Komut Optimizasyonu

```
# Yavaş (her seferinde process oluştur)
for file in *.txt; do
  cat $file | grep "pattern"
done

# Hızlı (tek process)
grep "pattern" *.txt
```

### Built-in Kullan

```
# Yavaş (external command)
dirname=$(dirname /path/to/file)

# Hızlı (parameter expansion)
dirname=${file%/*}
```

</div>

<div class="highlight-box">

### 🚀 Hız Artırıcı İpuçları

1. **Built-in komutları** tercih et
2. **Pipe zincirlerini** minimize et
3. **Gereksiz sub-shell** oluşturma
4. **Glob yerine find** kullan (büyük dizinler)
5. **awk/sed** yerine bash built-in (küçük işler)

</div>

</div>

---

# 3️⃣9️⃣ 💡 Güvenlik Best Practices

<div class="two-columns">

<div>

### Güvenli Scripting

```
#!/bin/bash

# Tanımsız değişkenlerde dur
set -u

# Hatalarda dur
set -e

# Pipe hatalarını yakala
set -o pipefail

# Güvenli temp dosyası
TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT
```

</div>

<div>

### Input Validation

```
#!/bin/bash

# Kullanıcı inputunu kontrol et
read -p "Enter filename: " filename

# Güvenli kontrol
if [[ ! "$filename" =~ ^[a-zA-Z0-9._-]+$ ]]; then
  echo "Invalid filename!"
  exit 1
fi

# Güvenli kullanım
touch "$filename"
```

</div>

</div>

<div class="info-box">

### ⚠️ Güvenlik Kuralları
- Asla `eval` kullanma
- User input'u her zaman validate et
- Tam path kullan (`/bin/ls` vs `ls`)
- Sensitive datayı environment variable'da tutma

</div>

---

# 4️⃣0️⃣ 💡 Dosya İşlemleri Örnekleri

<div class="two-columns">

<div>

### Toplu Dosya İşlemleri

```
# Tüm .txt dosyalarını yedekle
for f in *.txt; do
  cp "$f" "$f.bak"
done

# Dosya uzantısı değiştir
for f in *.jpeg; do
  mv "$f" "${f%.jpeg}.jpg"
done

# Boşlukları alt çizgiye çevir
for f in *\ *; do
  mv "$f" "${f// /_}"
done
```

</div>

<div>

### Dosya Bulma ve İşleme

```
# 30 günden eski logları sil
find /var/log -name "*.log" -mtime +30 -delete

# Büyük dosyaları listele
find . -type f -size +100M -exec ls -lh {} \;

# İzinleri toplu değiştir
find . -type f -name "*.sh" -exec chmod +x {} \;
```

</div>

</div>

---

# 4️⃣1️⃣ 💡 Text İşleme Örnekleri

<div class="two-columns">

<div>

### grep ile Arama

```
# Dosyalarda kelime ara
grep "error" *.log

# Case-insensitive arama
grep -i "warning" system.log

# Satır numarasıyla göster
grep -n "failed" app.log

# Rekürsif arama
grep -r "TODO" /project/src/
```

</div>

<div>

### sed ile Değiştirme

```
# Basit değiştirme
sed 's/old/new/' file.txt

# Tüm oluşumları değiştir
sed 's/old/new/g' file.txt

# Dosyayı güncelle
sed -i 's/old/new/g' file.txt

# Satır sil
sed '/pattern/d' file.txt
```

</div>

</div>

---

# 4️⃣2️⃣ 💡 Sistem Bakımı Komutları

<div class="two-columns">

<div>

### Disk ve Bellek

```
# Disk kullanımı
df -h

# Dizin boyutları
du -sh */

# Bellek durumu
free -h

# En büyük dosyalar
du -ah | sort -rh | head -20
```

</div>

<div>

### Sistem İzleme

```
# CPU kullanımı
top

# Process listesi
ps aux

# Aktif bağlantılar
netstat -tulpn

# Sistem logu
tail -f /var/log/syslog
```

</div>

</div>

<div class="highlight-box">

### 🔧 Otomatik Temizlik Script
```
#!/bin/bash
# cleanup.sh - Sistem temizliği
find /tmp -type f -mtime +7 -delete
find ~/Downloads -type f -mtime +30 -delete
```

</div>

---

# 4️⃣3️⃣ 💡 Network Komutları Temelleri

<div class="two-columns">

<div>

### Bağlantı Testleri

```
# Ping testi
ping -c 4 google.com

# Port kontrolü
nc -zv hostname 80

# DNS lookup
nslookup google.com

# Route izleme
traceroute google.com
```

</div>

<div>

### Network Bilgisi

```
# IP adresi
ip addr show

# Aktif bağlantılar
ss -tuln

# Network interface
ifconfig

# Download hızı testi
curl -o /dev/null http://speedtest.com/test
```

</div>

</div>

---

# 4️⃣4️⃣ 💡 Process Yönetimi

<div class="two-columns">

<div>

### Process Kontrolü

```
# Process listele
ps aux | grep nginx

# Process durumu
pgrep -l firefox

# Process öldür
kill PID
killall firefox

# Zorla öldür
kill -9 PID
```

</div>

<div>

### Background İşlemler

```
# Arka planda çalıştır
command &

# Suspended işi arka plana at
bg

# Arka plan işlerini listele
jobs

# Ön plana getir
fg %1
```

</div>

</div>

<div class="info-box">

### Uzun İşlem Örneği
```
# Arka planda çalıştır ve log tut
nohup long_running_script.sh > output.log 2>&1 &
```

</div>

---

# 4️⃣5️⃣ 💡 Pipe ve Redirection Örnekleri

<div class="two-columns">

<div>

### Redirection

```
# Output'u dosyaya yaz
ls > files.txt

# Append et
echo "new line" >> files.txt

# Error'ları yaz
command 2> error.log

# Her ikisini de yaz
command > output.log 2>&1
```

</div>

<div>

### Pipe Kullanımı

```
# Komut zincirleme
cat file.txt | grep "error" | wc -l

# Sıralama ve unique
cat file.txt | sort | uniq

# Column işleme
ps aux | awk '{print $1, $11}'

# Sayfa sayfa göster
ls -la | less
```

</div>

</div>

---

# 4️⃣6️⃣ 💡 Shortcuts ve Produktivite

<div class="two-columns">

<div class="info-box">

### Klavye Kısayolları

**Düzenleme:**
- `Ctrl+A` - Satır başı
- `Ctrl+E` - Satır sonu
- `Ctrl+U` - Satırı sil
- `Ctrl+K` - Sağı sil
- `Ctrl+W` - Kelime sil
- `Alt+D` - İleri kelime sil

</div>

<div class="info-box">

### History Kısayolları

**Geçmiş:**
- `Ctrl+R` - History'de ara
- `Ctrl+G` - Aramadan çık
- `!!` - Son komutu tekrarla
- `!$` - Son argüman
- `!^` - İlk argüman
- `!*` - Tüm argümanlar

</div>

</div>

<div class="highlight-box">

### 🚀 Pro Tip
`Ctrl+R` ile history'de arama yapın. Tekrar `Ctrl+R` ile sonraki eşleşmeye geçin!

</div>

---

# 4️⃣7️⃣ 💡 Troubleshooting Senaryoları

<div class="two-columns">

<div>

### Senaryo 1: Komut Bulunamadı

```
# Problem
mycommand
-bash: mycommand: command not found

# Çözüm Adımları
# 1. Komutu bul
which mycommand
find / -name mycommand 2>/dev/null

# 2. PATH'i kontrol et
echo $PATH

# 3. PATH'e ekle
export PATH=$PATH:/custom/path
```

</div>

<div>

### Senaryo 2: İzin Hatası

```
# Problem
./script.sh
-bash: ./script.sh: Permission denied

# Çözüm
# 1. İzinleri kontrol et
ls -l script.sh

# 2. Çalıştırma izni ver
chmod +x script.sh

# 3. Tekrar dene
./script.sh
```

</div>

</div>

---

# 4️⃣8️⃣ 💡 Lab Egzersiz 1: Alias ve Function

<div class="info-box">

### 🎯 Görev: Kişisel Produktivite Araçları Oluştur

**Adımlar:**

1. `.bashrc` dosyanıza şu aliasları ekleyin:
```
alias ll='ls -alF'
alias update='sudo apt update && sudo apt upgrade'
alias myip='curl ifconfig.me'
```

2. Sistem bilgisi fonksiyonu oluşturun:
```
syscheck() {
  echo "=== Quick System Check ==="
  echo "Disk: $(df -h / | tail -1 | awk '{print $5}')"
  echo "Memory: $(free | grep Mem | awk '{printf "%.0f%%", $3/$2 * 100}')"
  echo "Uptime: $(uptime -p)"
}
```

3. Değişiklikleri yükleyin ve test edin:
```
source ~/.bashrc
ll
syscheck
```

</div>

---

# 4️⃣9️⃣ 💡 Lab Egzersiz 2: Script Yazma

<div class="info-box">

### 🎯 Görev: Otomatik Backup Script

**backup_my_docs.sh:**
```
#!/bin/bash

# Konfigürasyon
SOURCE="$HOME/Documents"
DEST="$HOME/Backups"
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="docs-backup-$DATE.tar.gz"

# Backup dizini oluştur
mkdir -p "$DEST"

# Backup yap
echo "Backup başlıyor..."
tar -czf "$DEST/$BACKUP_FILE" "$SOURCE" 2>/dev/null

# Kontrol et
if [ $? -eq 0 ]; then
  SIZE=$(du -h "$DEST/$BACKUP_FILE" | cut -f1)
  echo "✓ Backup başarılı: $BACKUP_FILE ($SIZE)"
else
  echo "✗ Backup başarısız!"
  exit 1
fi
```

**Test:**
```
chmod +x backup_my_docs.sh
./backup_my_docs.sh
```

</div>

---

<!-- _class: final-slide -->
<!-- _paginate: false -->

# 📚 Teşekkürler!

<div>

📧 **Email:** info@kapadokya.edu.tr
🌐 **Website:** www.kapadokya.edu.tr
💼 **LinkedIn:** Kapadokya Üniversitesi

</div>
