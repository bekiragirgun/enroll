// Öğrenci tarafı — mod değişimini 3 sn'de bir kontrol eder

const POLLING_ARALIK = 3000;

function mevcutModu() {
  return document.body.dataset.mod || 'bekleme';
}

function modalGoster(mod, ekstra) {
  const bekleme = document.getElementById('bekleme-ekrani');
  const slayt   = document.getElementById('slayt-ekrani');
  const terminal = document.getElementById('terminal-ekrani');

  // Hepsini gizle
  [bekleme, slayt, terminal].forEach(el => { if(el) el.style.display = 'none'; });

  if (mod === 'bekleme') {
    if (bekleme) bekleme.style.display = 'flex';
  } else if (mod === 'slayt') {
    if (slayt) {
      slayt.style.display = 'block';
      const iframe = document.getElementById('slayt-iframe');
      if (iframe && ekstra?.dosya) {
        // dataset ile karşılaştır (iframe.src tam URL döner, karışıklık olur)
        if (iframe.dataset.dosya !== ekstra.dosya) {
          iframe.src = '/slayt/' + ekstra.dosya;
          iframe.dataset.dosya = ekstra.dosya;
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

  document.body.dataset.mod = mod;
}

async function durumKontrol() {
  try {
    const yanit = await fetch('/api/durum');
    const veri = await yanit.json();
    const eskiMod = mevcutModu();
    const eskiDosya = document.getElementById('slayt-iframe')?.dataset.dosya || '';

    if (veri.mod !== eskiMod || veri.dosya !== eskiDosya) {
      modalGoster(veri.mod, veri);
    }
  } catch (e) {
    // Bağlantı hatası — sessizce geç
  }
}

// Sayfa yüklendikten sonra polling başlat
document.addEventListener('DOMContentLoaded', () => {
  setInterval(durumKontrol, POLLING_ARALIK);
});
