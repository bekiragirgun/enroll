# SEB (Safe Exam Browser) Entegrasyonu

## Nasil Calisir

1. Ogretmen panelinden **Kiosk Modu: Acik** yap
2. Ogrenci normal tarayicidan gelince `/seb-gerekli` sayfasina yonlendirilir
3. Sayfadan SEB indirilir ve kurulur
4. `.seb` config dosyasi indirilip acilir
5. SEB otomatik olarak sisteme baglanir

## SEB Indirme Linkleri

| Platform | Link |
|----------|------|
| Windows | [GitHub Release v3.10.1](https://github.com/SafeExamBrowser/seb-win-refactoring/releases/tag/v3.10.1) |
| macOS | [GitHub Release 3.6.1](https://github.com/SafeExamBrowser/seb-mac/releases/tag/3.6.1) |
| Yedek | [safeexambrowser.org](https://safeexambrowser.org/download_en.html) |

## SEB Config

`/seb-config` endpoint'i `.seb` dosyasi uretir. Icerigi:

- `startURL`: Sistem IP + port (orn: `http://10.211.55.2:3333/`)
- `quitURL`: `/seb-quit`
- `quitPassword`: `linux2024`
- `allowThirdPartyCookies`: true (Flask session icin)
- `URLFilterEnable`: false
- `showTaskBar`: false (sunum sirasinda gizli)

!!! warning "Config Degisikliginde"
    `system_host` veya port degistiginde `.seb` dosyasini **tekrar indirin**.
    Eski dosya yanlis URL'ye baglanmaya calisir.

## SEB User-Agent

SEB Windows: `SEB/3.10.1 (x64)`
SEB macOS: `SafeExamBrowser/3.x`

Tespit: `'SEB/' in user_agent` (her iki platform icin calisir)

## Cikis Yonetimi

| Yontem | Akis |
|--------|------|
| Ogrenci "Cikis Yap" | `/api/ogrenci_cikis` → `/seb-quit` → SEB kapanir |
| Ogrenci "SEB Cikis Talep" | Ogretmen onaylar → polling algila → `/seb-quit` |
| Ogretmen "Toplu Cikis" | Polling algila → `/seb-quit` |
| Sinav sonrasi | "Sinavi Bitir ve Cik" → `/seb-quit` |

## Ogretmen Kontrolleri

- **SEB Cikis Izni**: Acik/Kapali — ogrenci cikis butonlarini kontrol eder
- **Kiosk Modu**: SEB zorunlulugunu ac/kapat (3sn polling ile ogrenciye yansiyor)
- **Guvenlik Log**: SEB cikis talepleri onayla/reddet
