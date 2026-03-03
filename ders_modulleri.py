"""
Ders Modülleri Konfigürasyonu
Kapadokya Üniversitesi - NDG Linux Essentials

Bu dosya ders modüllerini, slayt dosyalarını ve sınav sorularını yönetir.
"""

# Ders modülleri (18 bölüm)
DERS_MODULLERI = [
    {
        "id": 1,
        "ad": "Linux'a Giriş",
        "dosya": "bolum_01_linux_giris",
        "durum": "tamam",
        "aciklama": "Linux tarihçesi, dağıtımlar ve temel kavramlar",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 2,
        "ad": "İşletim Sistemleri & Açık Kaynak",
        "dosya": "bolum_02_04_isletim_sistemleri_acik_kaynak",
        "durum": "tamam",
        "aciklama": "İşletim sistemleri, açık kaynak yazılım felsefesi",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 3,
        "ad": "Linux'ta Çalışmak",
        "dosya": "bolum_03_linuxta_calismak",
        "durum": "tamam",
        "aciklama": "GUI, terminal ve temel işlemler",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 4,
        "ad": "Komut Satırı Becerileri",
        "dosya": "bolum_05_komut_satiri",
        "durum": "tamam",
        "aciklama": "Komut satırı kullanımı, temel komutlar",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 5,
        "ad": "Yardım Alma & Dosya Sisteminde Gezinme",
        "dosya": "bolum_06_07_yardim_dosya_sistemi",
        "durum": "tamam",
        "aciklama": "man pages, dosya sistemi hiyerarşisi, navigasyon",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 6,
        "ad": "Dosya Yönetimi & Arşivleme",
        "dosya": "bolum_08_09_dosya_arsivleme",
        "durum": "tamam",
        "aciklama": "Dosya işlemleri, arşivleme (tar, gzip)",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 7,
        "ad": "Metinlerle Çalışmak",
        "dosya": "bolum_10_metinlerle_calisma",
        "durum": "tamam",
        "aciklama": "Metin düzenleme, grep, sed, awk",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 8,
        "ad": "Temel Betik Yazımı",
        "dosya": "bolum_11_betik_yazimi",
        "durum": "tamam",
        "aciklama": "Shell script yazımı, değişkenler, döngüler",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 9,
        "ad": "Bilgisayar Donanımını Anlamak",
        "dosya": "bolum_12_bilgisayar_donanimi",
        "durum": "tamam",
        "aciklama": "CPU, RAM, disk, I/O aygıtları",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 10,
        "ad": "Verinin Depolandığı Yer",
        "dosya": "bolum_13_verinin_depolandigi_yer",
        "durum": "tamam",
        "aciklama": "Disk yönetimi, dosya sistemleri, mount",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 11,
        "ad": "Ağ Yapılandırması",
        "dosya": "014_ag_yapilandrma",
        "durum": "tamam",
        "aciklama": "IP adresleme, DNS, network komutları",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 12,
        "ad": "Sistem ve Kullanıcı Güvenliği",
        "dosya": "015_user_hesaplari",
        "durum": "tamam",
        "aciklama": "Kullanıcı yönetimi, yetkilendirme, güvenlik",
        "slayt_var": True,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 13,
        "ad": "Kullanıcı ve Grup Oluşturma",
        "dosya": None,
        "durum": "eksisik",
        "aciklama": "Kullanıcı ve grup yönetimi",
        "slayt_var": False,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 14,
        "ad": "Sahiplik ve İzinler",
        "dosya": None,
        "durum": "eksisik",
        "aciklama": "chmod, chown, izinler",
        "slayt_var": False,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
    {
        "id": 15,
        "ad": "Özel Dizinler ve Dosyalar",
        "dosya": None,
        "durum": "eksisik",
        "aciklama": "Özel dosyalar, sistem dosyaları",
        "slayt_var": False,
        "sinav_var": False,
        "kaynak": "NetAcad NDG Linux Essentials"
    },
]

# Slayt dizini konfigürasyonu
SLAYT_KAYNAK_DIR = "../01_SUNUMLAR/kaynak"
SLAYT_HTML_DIR = "../01_SUNUMLAR/html"
SLAYT_PDF_DIR = "../01_SUNUMLAR/pdf"

# Docker eğitim modülleri
DOCKER_MODULLERI = [
    {
        "id": "docker-01",
        "ad": "Docker'a Giriş",
        "dosya": "docker_ubuntu_kurulum",
        "durum": "tamam",
        "aciklama": "Docker kurulumu ve temel kavramlar",
        "slayt_var": True,
        "sinav_var": False
    },
    {
        "id": "docker-02",
        "ad": "Docker Özet",
        "dosya": "DOCKER_OZET",
        "durum": "tamam",
        "aciklama": "Docker komutları özeti",
        "slayt_var": True,
        "sinav_var": False
    },
]


def modul_getir(modul_id):
    """Modül ID'sine göre modül bilgisi döndürür."""
    for modul in DERS_MODULLERI:
        if modul["id"] == modul_id:
            return modul
    return None


def modul_listesi(durum=None):
    """Modül listesini döndürür. durum parametresi ile filtreleme yapılabilir."""
    if durum:
        return [m for m in DERS_MODULLERI if m["durum"] == durum]
    return DERS_MODULLERI


def tamamlanan_moduller():
    """Tamamlanan modülleri döndürür."""
    return [m for m in DERS_MODULLERI if m["durum"] == "tamam"]


def eksik_moduller():
    """Eksik modülleri döndürür."""
    return [m for m in DERS_MODULLERI if m["durum"] == "eksisik"]


def slayti_var_moduller():
    """Slaytı olan modülleri döndürür."""
    return [m for m in DERS_MODULLERI if m["slayt_var"]]


def modul_slayt_yolu(modul_id, format="html"):
    """Modülün slayt dosya yolunu döndürür."""
    modul = modul_getir(modul_id)
    if not modul or not modul["slayt_var"]:
        return None

    dosya_adi = modul["dosya"]

    if format == "html":
        return f"{SLAYT_HTML_DIR}/{dosya_adi}.html"
    elif format == "pdf":
        return f"{SLAYT_PDF_DIR}/{dosya_adi}.pdf"
    elif format == "kaynak":
        return f"{SLAYT_KAYNAK_DIR}/{dosya_adi}.md"
    else:
        return None


def modul_istatistik():
    """Modül istatistiklerini döndürür."""
    toplam = len(DERS_MODULLERI)
    tamam = len(tamamlanan_moduller())
    eksik = len(eksik_moduller())
    slayt_var = len(slayti_var_moduller())

    return {
        "toplam": toplam,
        "tamam": tamam,
        "eksik": eksik,
        "slayt_var": slayt_var,
        "yuzde_tamam": round((tamam / toplam) * 100, 1) if toplam > 0 else 0
    }


if __name__ == "__main__":
    # Test
    print("Ders Modülleri İstatistik:")
    stats = modul_istatistik()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nTamamlanan Modüller:")
    for modul in tamamlanan_moduller():
        print(f"  {modul['id']}. {modul['ad']}")

    print("\nEksik Modüller:")
    for modul in eksik_moduller():
        print(f"  {modul['id']}. {modul['ad']}")
