// Öğrenci tarafı — mod değişimini 500ms'de bir kontrol eder
const POLLING_ARALIK = 1000; // 1 saniyeye düşürelim (sunucu yükü için)

// Mevcut durumu bellekte tut (Loop'u engellemek için en güvenli yol)
let suAnkiDurum = {
  mod: '',
  dosya: '',
  slayt_hash: '',
  terminal_url: ''
};

function modalGoster(mod, ekstra) {
  const bekleme = document.getElementById('bekleme-ekrani');
  const slayt = document.getElementById('slayt-ekrani');
  const terminal = document.getElementById('terminal-ekrani');

  // Hepsini gizle
  [bekleme, slayt, terminal].forEach(el => { if (el) el.style.display = 'none'; });

  if (mod === 'bekleme') {
    if (bekleme) bekleme.style.display = 'flex';
  }
  else if (mod === 'slayt') {
    if (slayt) {
      slayt.style.display = 'block';
      const iframe = document.getElementById('slayt-iframe');
      if (iframe && ekstra?.dosya) {
        const hash = ekstra?.slayt_hash || '';
        const yeniSrc = '/slayt/' + ekstra.dosya + hash;

        // Iframe URL'i gerçekten farklıysa yükle
        if (iframe.dataset.lastSrc !== yeniSrc) {
          iframe.src = yeniSrc;
          iframe.dataset.lastSrc = yeniSrc;
        }
      }
    }
  }
  else if (mod === 'terminal') {
    if (terminal) {
      terminal.style.display = 'flex';
      const iframe = document.getElementById('terminal-iframe');
      const loading = document.getElementById('terminal-loading');

      if (iframe && ekstra?.terminal_url) {
        let url = ekstra.terminal_url;
        // Nginx uyumu için trailing slash ekle (404'ü önlemek için)
        if (!url.endsWith('/')) url += '/';

        if (iframe.dataset.lastUrl !== url) {
          console.log('[Terminal] URL yükleniyor:', url);
          if (loading) loading.style.display = 'block';
          iframe.src = url;
          iframe.dataset.lastUrl = url;

          iframe.onload = () => { if (loading) loading.style.display = 'none'; };
          iframe.onerror = () => {
            if (loading) loading.style.display = 'none';
            alert('Terminal yüklenemedi. TTYD çalışmıyor olabilir.');
          };
        }
      }
    }
  }

  document.body.dataset.mod = mod;
}

async function durumKontrol() {
  try {
    const apiUrl = '/api/durum';
    const yanit = await fetch(apiUrl, {
      credentials: 'same-origin',
      headers: { 'Cache-Control': 'no-cache' }
    });

    if (!yanit.ok) return;

    // Cloudflare Access redirect kontrolü (CORS hatasını önlemek için)
    if (yanit.redirected) {
      console.warn('[Polling] Session süresi dolmuş olabilir, yönlendirildi.');
      return;
    }

    const veri = await yanit.json();

    // Derin karşılaştırma (Loop'u durduran asıl yer)
    const degisti =
      veri.mod !== suAnkiDurum.mod ||
      veri.dosya !== suAnkiDurum.dosya ||
      veri.slayt_hash !== suAnkiDurum.slayt_hash ||
      veri.terminal_url !== suAnkiDurum.terminal_url;

    if (degisti) {
      console.log('[Polling] Durum değişti:', suAnkiDurum, '->', veri);

      // Bellekteki durumu güncelle
      suAnkiDurum = { ...veri };

      // Arayüzü güncelle
      modalGoster(veri.mod, veri);
    }
  } catch (e) {
    console.error('[Polling] Hata:', e);
  }
}

// Polling başlat
document.addEventListener('DOMContentLoaded', () => {
  // İlk yüklemede çalıştır
  durumKontrol();
  // Sonra periyodik
  setInterval(durumKontrol, POLLING_ARALIK);
});
