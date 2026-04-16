# Terminal Sistemleri Karşılaştırması

## Docker vs Chroot vs LXC

| Özellik | Docker (Per-Student) | Docker (Shared) | Chroot + PAM | LXC (Per-Student) |
|---------|---------------------|-----------------|--------------|-------------------|
| **Kaynak Kullanımı** | ⚠️ Yüksek | ✅ Orta | ✅✅ Çok Düşük | ⚠️ Yüksek |
| **RAM (45 öğrenci)** | ~23 GB | ~2 GB | ~1.5 GB | ~23 GB |
| **CPU (45 öğrenci)** | ~22 cores | ~2 cores | ~1 core | ~22 cores |
| **Disk Alanı** | ~90 GB | ~2 GB | ~15 GB | ~90 GB |
| **Başlangıç Süresi** | 5-10 sn | 1-2 sn | <1 sn | 5-10 sn |
| **Root Erişimi** | ✅ Var | ✅ Var | ✅✅ Güvenli | ✅ Var |
| **Sistem İzolasyonu** | ✅✅ Tam | ⚠️ Kısmi | ✅ Yeterli | ✅✅ Tam |
| **Yönetim Kolaylığı** | ⚠️ Orta | ✅ Kolay | ✅✅ Çok Kolay | ⚠️ Orta |
| **Backup** | ✅ Image | ⚠️ Manuel | ✅✅ Çok Kolay | ✅ Snapshot |
| **Proxmox Entegrasyonu** | ⚠️ Docker gerekir | ⚠️ Docker gerekir | ✅✅ Native | ✅✅ Native |
| **Öğrenme Eğrisi** | Orta | Kolay | Kolay | Orta |
| **Üretim Olabilirlik** | ✅ Evet | ⚠️ Sınırlı | ✅✅ Evet | ✅✅ Evet |

## Detaylı Karşılaştırma

### 1. Docker (Per-Student Container)
```bash
# Her öğrenci için ayrı container
docker run -d --name ogrenci1 --memory 512m --cpus 0.5 ubuntu
docker run -d --name ogrenci2 --memory 512m --cpus 0.5 ubuntu
# ... 45 tane
```

**Artıları:**
- ✅ Tam izolasyon
- ✅ Her öğrenci root olabilir
- ✅ Container kolay yönetim

**Eksileri:**
- ❌ Çok kaynak gerektirir (45 öğrenci = 23GB RAM)
- ❌ Yönetim zorluğu (45 container)
- ❌ Proxmox'ta Docker gerektirir

**Kullanım Durumu:** Büyük kuruluşlar, yeterli kaynak varsa

---

### 2. Docker (Shared Container)
```bash
# Tek container, çoklu kullanıcı
docker run -d --name linux-lab --memory 2g --cpus 2 ubuntu
# İçinde useradd ile kullanıcılar oluştur
```

**Artıları:**
- ✅ Düşük kaynak kullanımı
- ✅ Kolay yönetim (1 container)
- ✅ Hızlı başlangıç

**Eksileri:**
- ❌ Kısmi izolasyon (aynı process tree)
- ❌ Bir öğrenci sistemi çökürse herkes etkilenir
- ❌ Root ayrımı zor

**Kullanım Durumu:** Kaynak kısıtlı, küçük sınıflar (10-15 öğrenci)

---

### 3. Chroot + PAM ⭐ **RECOMMENDED**
```bash
# Her öğrenci için chroot ortamı
/home/chroot/ogrenci1/  → Öğrenci1 için "/"
/home/chroot/ogrenci2/  → Öğrenci2 için "/"
# SSH ile girince otomatik chroot içine düşer
```

**Artıları:**
- ✅✅ **En düşük** kaynak kullanımı
- ✅✅ Öğrenci kendi chroot'unda root olabilir (güvenli)
- ✅✅ Gerçek sistem korunur
- ✅✅ Proxmox LXC için **ideal**
- ✅✅ Yönetimi çok kolay
- ✅✅ Backup/restoration çok basit

**Eksileri:**
- ⚠️ Kullanıcı eğitimi gerektirir (chroot kavramı)
- ⚠️ Kernel'i paylaşır (daha az izolasyon)

**Kullanım Durumu:** ✅ **Eğitim için ideal!** 30-60 öğrenci

---

### 4. LXC (Per-Student Container)
```bash
# Her öğrenci için LXC container
pct create 100 template.tar.gz
pct create 101 template.tar.gz
# ... 45 tane
```

**Artıları:**
- ✅✅ Tam izolasyon (kernel level)
- ✅✅ Proxmox native
- ✅✅ Snapshot/backup kolay
- ✅ Her öğrenci root olabilir

**Eksileri:**
- ❌ Yüksek kaynak kullanımı
- ❌ Yönetim zor (45 LXC container)
- ❌ Disk alanı gerektirir

**Kullanım Durumu:** Çok büyük kuruluşlar, sınırsız kaynak

---

## 🎯 Tavsiye

### Kapadokya Üniversitesi için: **Chroot + PAM**

**Neden?**
1. **Kaynak Uygun**: 45 öğrenci için sadece ~1.5 GB RAM
2. **Güvenli Root**: Öğrenci kendi ortamında root olabilir
3. **Proxmox Dostu**: LXC container içinde çalışır
4. **Kolay Yönetim**: Python script ile otomasyon
5. **Hızlı**: <1 saniyede başlar
6. **Eğitim İçin Ideal**: Gerçek Linux deneyimi

### Alternatif: LXC (Per-Student)
Eğer kaynak yetersiyse:
- 30 öğrenci → Chroot + PAM
- 60+ öğrenci → Shared Docker veya daha büyük server

## 📊 Maliyet Karşılaştırması (45 Öğrenci)

| Sistem | RAM | CPU | Disk | Maliyet (yıllık) |
|--------|-----|-----|------|------------------|
| Docker Per-Student | 23 GB | 22 cores | 90 GB | $$ (Yüksek) |
| Docker Shared | 2 GB | 2 cores | 2 GB | $ (Düşük) |
| **Chroot + PAM** | **1.5 GB** | **1 core** | **15 GB** | **$ (Çok Düşük)** |
| LXC Per-Student | 23 GB | 22 cores | 90 GB | $$ (Yüksek) |

## 🔧 Karar Matrisi

```
┌─────────────────────┬──────────┬──────────┬──────────┐
│ Öğrenci Sayısı     │ < 20     │ 20-50    │ > 50     │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Sınırsız Kaynak    │ LXC      │ LXC      │ Docker   │
│                     │          │ Per-Std  │ Per-Std  │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Normal Kaynak      │ Docker   │ Chroot   │ Docker   │
│ (16GB / 8 cores)   │ Shared   │ + PAM    │ Shared   │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Kısıtlı Kaynak     │ Chroot   │ Chroot   │ Shared   │
│ (8GB / 4 cores)    │ + PAM    │ + PAM    │ Docker   │
└─────────────────────┴──────────┴──────────┴──────────┘
```

## 🚀 Hızlı Karar

**Chroot + PAM seçin EĞER:**
- ✅ 30-60 öğrenciniz var
- ✅ 8-16 GB RAMiniz var
- ✅ Proxmox kullanıyorsunuz
- ✅ Öğrencilere root erişimi vermek istiyorsunuz
- ✅ Düşük maliyetli çözüm istiyorsunuz

**Docker Shared seçin EĞER:**
- ✅ 10-20 öğrenciniz var
- ✅ 4-8 GB RAMiniz var
- ✅ Docker'a aşinasınız
- ✅ En basit çözümü istiyorsunuz

**LXC Per-Student seçin EĞER:**
- ✅ Sınırsız kaynağınız var
- ✅ Tam izolasyon şart
- ✅ Proxmox expertsiniz
- ✅ Enterprise seviye çözüm istiyorsunuz

## 📚 Sonuç

**Kapadokya Üniversitesi BGY106 için:**
```
🏆 Kazanan: Chroot + PAM

Neden?
+ En uygun kaynak kullanımı
+ Güvenli root erişimi
+ Proxmox uyumlu
+ Kolay yönetim
+ Eğitim için ideal
```
