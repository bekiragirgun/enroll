// Öğrenci tarafı — mod değişimini 500ms'de bir kontrol eder
const POLLING_ARALIK = 1000; // 1 saniyeye düşürelim (sunucu yükü için)

// Mevcut durumu bellekte tut
let suAnkiDurum = {
  mod: '',
  dosya: '',
  slayt_hash: '',
  terminal_url: ''
};

// Tam ekran durumu
let tamEkranModu = false;

function toggleFullScreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(err => {
      console.error(`Tam ekran hatası: ${err.message}`);
    });
  } else {
    document.exitFullscreen();
  }
}

function startLessonFullscreen() {
  // Tam ekrana geç
  document.documentElement.requestFullscreen().then(() => {
    // Overlay'i gizle
    document.getElementById('join-overlay').style.display = 'none';
    tamEkranModu = true;
    // Mevcut modu göster
    modalGoster(suAnkiDurum.mod, suAnkiDurum);
  }).catch(err => {
    console.error(`Derse katılma hatası: ${err.message}`);
    // Hata olsa bile overlay'i gizle ki ders görünsün
    document.getElementById('join-overlay').style.display = 'none';
    modalGoster(suAnkiDurum.mod, suAnkiDurum);
  });
}

function modalGoster(mod, ekstra) {
  const bekleme = document.getElementById('bekleme-ekrani');
  const slayt = document.getElementById('slayt-ekrani');
  const terminal = document.getElementById('terminal-ekrani');
  const overlay = document.getElementById('join-overlay');

  // Hepsini gizle
  [bekleme, slayt, terminal].forEach(el => { if (el) el.style.display = 'none'; });

  // Eğer mod 'bekleme' DEĞİLSE ve tam ekran DEĞİLSE overlay göster
  if (mod !== 'bekleme' && !document.fullscreenElement) {
    if (overlay) overlay.style.display = 'flex';
    document.body.dataset.mod = mod;
    return; // İçeriği gösterme
  }

  // Overlay'i kapat (Eğer tam ekransa veya bekleme modundaysa)
  if (overlay) overlay.style.display = 'none';

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
        // Backend artık hem /terminal hem /terminal/ destekliyor, zorlamaya gerek yok

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

    // Cloudflare Access check
    if (yanit.url && yanit.url.includes('cloudflareaccess.com')) {
      window.location.reload();
      return;
    }

    if (!yanit.ok) return;

    const veri = await yanit.json();

    const degisti =
      veri.mod !== suAnkiDurum.mod ||
      veri.dosya !== suAnkiDurum.dosya ||
      veri.slayt_hash !== suAnkiDurum.slayt_hash ||
      veri.terminal_url !== suAnkiDurum.terminal_url;

    if (degisti) {
      console.log('[Polling] Durum değişti:', suAnkiDurum, '->', veri);
      suAnkiDurum = { ...veri };
      modalGoster(veri.mod, veri);
    }
  } catch (e) {
    console.error('[Polling] Hata:', e);
  }
}

// Tam ekran değişimini izle (Kaldıysa veya ESC ile çıkıldıysa)
document.addEventListener('fullscreenchange', () => {
  if (!document.fullscreenElement && suAnkiDurum.mod !== 'bekleme') {
    // Tam ekrandan çıkıldı ve ders aktif, overlay göster
    modalGoster(suAnkiDurum.mod, suAnkiDurum);
  }
});

// Polling başlat
document.addEventListener('DOMContentLoaded', () => {
  durumKontrol();
  setInterval(durumKontrol, POLLING_ARALIK);
});
