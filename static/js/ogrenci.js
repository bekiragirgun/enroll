// Öğrenci tarafı — mod değişimini 500ms'de bir kontrol eder (hızlı senkronizasyon)

const POLLING_ARALIK = 500;

function mevcutModu() {
  // LocalStorage'dan oku, yoksa 'bekleme'
  return localStorage.getItem('mod') || 'bekleme';
}

function modalGoster(mod, ekstra) {
  const bekleme = document.getElementById('bekleme-ekrani');
  const slayt = document.getElementById('slayt-ekrani');
  const terminal = document.getElementById('terminal-ekrani');

  // Hepsini gizle
  [bekleme, slayt, terminal].forEach(el => { if (el) el.style.display = 'none'; });

  if (mod === 'bekleme') {
    if (bekleme) bekleme.style.display = 'flex';
  } else if (mod === 'slayt') {
    if (slayt) {
      slayt.style.display = 'block';
      const iframe = document.getElementById('slayt-iframe');
      if (iframe && ekstra?.dosya) {
        // Hash ile birlikte URL oluştur
        const hash = ekstra?.slayt_hash || '';
        const yeniSrc = '/slayt/' + ekstra.dosya + hash;

        // Dataset ile karşılaştır (iframe.src tam URL döner, karışıklık olur)
        if (iframe.dataset.dosya !== ekstra.dosya || iframe.dataset.hash !== hash) {
          iframe.src = yeniSrc;
          iframe.dataset.dosya = ekstra.dosya;
          iframe.dataset.hash = hash;
        }
      }
    }
  } else if (mod === 'terminal') {
    if (terminal) {
      terminal.style.display = 'flex';
      const iframe = document.getElementById('terminal-iframe');
      const loading = document.getElementById('terminal-loading');
      console.log('Terminal modu aktif, ekstra:', ekstra);

      if (loading) loading.style.display = 'block';

      if (iframe) {
        if (ekstra?.terminal_url) {
          console.log('Terminal URL ayarlanıyor:', ekstra.terminal_url);
          const url = ekstra.terminal_url;

          if (iframe.dataset.url !== url) {
            iframe.src = url;
            iframe.dataset.url = url;

            // Loading'i gizle (iframe yüklenince veya timeout)
            iframe.onload = () => {
              console.log('Terminal yüklendi!');
              if (loading) loading.style.display = 'none';
            };

            iframe.onerror = () => {
              console.error('Terminal yüklenemedi!');
              if (loading) loading.style.display = 'none';
              alert('Terminal yüklenemedi. TTYD çalışmıyor olabilir.');
            };
          }
        } else {
          console.warn('Terminal URL bulunamadı! Ekstra veri:', ekstra);
          iframe.src = 'about:blank';
          if (loading) loading.style.display = 'none';
        }
      } else {
        console.error('Terminal iframe bulunamadı!');
        if (loading) loading.style.display = 'none';
      }

      // Timeout: 10 saniye sonra loading'i gizle
      setTimeout(() => {
        if (loading) loading.style.display = 'none';
      }, 10000);
    }
  }

  // Mod bilgisini localStorage'a kaydet
  localStorage.setItem('mod', mod);
  document.body.dataset.mod = mod;
}

async function durumKontrol() {
  try {
    // API URL'i config'den al (production için API proxy)
    const apiUrl = (window.API_BASE || '') + '/api/durum';

    // Cloudflare Access CORS sorunu için same-origin flag
    const yanit = await fetch(apiUrl, {
      credentials: 'same-origin',
      headers: {
        'Cache-Control': 'no-cache'
      }
    });

    if (!yanit.ok) {
      console.warn('API yanıtı başarısız:', yanit.status, yanit.statusText);
      return;
    }

    const veri = await yanit.json();
    const eskiMod = mevcutModu();
    const slaytIframe = document.getElementById('slayt-iframe');
    const eskiDosya = slaytIframe?.dataset.dosya || '';
    const eskiHash = slaytIframe?.dataset.hash || '';
    const terminalIframe = document.getElementById('terminal-iframe');
    const eskiTerminalUrl = terminalIframe?.dataset.url || '';

    // Terminal URL için trailing slash kontrolü yapalım (Nginx uyumu için)
    if (veri.mod === 'terminal' && veri.terminal_url && !veri.terminal_url.endsWith('/')) {
      veri.terminal_url += '/';
    }

    // Durum değişti mi kontrolü
    let degisti = false;
    if (veri.mod !== eskiMod) {
      console.log(`[Polling] Mod değişti: ${eskiMod} -> ${veri.mod}`);
      degisti = true;
    }
    if (veri.dosya !== eskiDosya) {
      console.log(`[Polling] Dosya değişti: ${eskiDosya} -> ${veri.dosya}`);
      degisti = true;
    }
    if (veri.mod === 'slayt' && veri.slayt_hash !== eskiHash) {
      console.log(`[Polling] Slayt hash değişti: ${eskiHash} -> ${veri.slayt_hash}`);
      degisti = true;
    }
    if (veri.mod === 'terminal' && veri.terminal_url !== eskiTerminalUrl) {
      console.log(`[Polling] Terminal URL değişti: ${eskiTerminalUrl} -> ${veri.terminal_url}`);
      degisti = true;
    }

    if (degisti) {
      console.log('[Polling] Yeni durum uygulanıyor:', veri);

      if (slaytIframe) {
        slaytIframe.dataset.dosya = veri.dosya || '';
        if (veri.mod === 'slayt') slaytIframe.dataset.hash = veri.slayt_hash || '';
      }

      modalGoster(veri.mod, veri);
    }
  } catch (e) {
    console.error('[Polling] Kritik hata:', e);
  }
}

// Sayfa yüklendikten sonra polling başlat
document.addEventListener('DOMContentLoaded', () => {
  setInterval(durumKontrol, POLLING_ARALIK);
});
