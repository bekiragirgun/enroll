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
  const sinav = document.getElementById('sinav-ekrani');
  const overlay = document.getElementById('join-overlay');
  const cikisAlani = document.getElementById('cikis-talep-alani');

  // Hepsini gizle
  [bekleme, slayt, terminal, sinav].forEach(el => { if (el) el.style.display = 'none'; });
  if (cikisAlani) cikisAlani.style.display = 'none';

  // Eğer mod 'bekleme' DEĞİLSE ve tam ekran DEĞİLSE overlay göster
  if (mod !== 'bekleme' && !document.fullscreenElement) {
    if (overlay) overlay.style.display = 'flex';
    document.body.dataset.mod = mod;
    return; // İçeriği gösterme
  }

  // Overlay'i kapat (Eğer tam ekransa veya bekleme modundaysa)
  if (overlay) overlay.style.display = 'none';
  // Eğer bekleme modunda değilsek çıkış butonunu göster
  if (mod !== 'bekleme' && cikisAlani) {
    cikisAlani.style.display = 'block';
  }

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
  else if (mod === 'sinav') {
    if (sinav) {
      sinav.style.display = 'block';
      aktifSinaviGetir();
    }
  }

  document.body.dataset.mod = mod;
}

// Global olarak sınav değişkenleri
let mevcutSinavId = null;

async function aktifSinaviGetir() {
  try {
    const yanit = await fetch('/api/sinav/aktif');
    const veri = await yanit.json();

    if (!veri.aktif_sinav) return;

    mevcutSinavId = veri.aktif_sinav.id;
    document.getElementById('ogrenci-sinav-baslik').innerText = veri.aktif_sinav.baslik;

    const alan = document.getElementById('ogrenci-sorular-alani');
    const buton = document.getElementById('btn-sinav-gonder');
    const bitis = document.getElementById('sinav-bitis-mesaji');

    if (veri.aktif_sinav.zaten_cevapladi) {
      alan.style.display = 'none';
      buton.style.display = 'none';
      bitis.style.display = 'block';
      return;
    }

    alan.style.display = 'block';
    buton.style.display = 'block';
    bitis.style.display = 'none';

    let html = '';
    veri.aktif_sinav.sorular.forEach((soru, i) => {
      html += `<div class="sinav-soru" data-soru-id="${soru.id}" style="background:#2d3748; padding:1.5rem; border-radius:8px; margin-bottom:1.5rem; border:1px solid #4a5568;">
                <h3 style="margin-top:0; color:#e2e8f0; font-size:1.1rem; margin-bottom:1rem;">${i + 1}. ${soru.metin}</h3>
                <div style="display:flex; flex-direction:column; gap:0.75rem;">`;

      soru.secenekler.forEach(secenek => {
        html += `
                 <label style="display:flex; align-items:center; gap:0.5rem; cursor:pointer; background:#1a202c; padding:0.75rem; border-radius:6px; border:1px solid #4a5568; transition:all 0.2s;">
                    <input type="radio" name="soru_${soru.id}" value="${secenek.id}" style="width:18px;height:18px;">
                    <span style="font-size:1rem;">${secenek.metin}</span>
                 </label>
               `;
      });
      html += `</div></div>`;
    });

    alan.innerHTML = html;

  } catch (e) {
    console.error("Sınav çekilemedi", e);
  }
}

async function sinavCevaplariniGonder() {
  if (!mevcutSinavId) return;

  const sorular = document.querySelectorAll('.sinav-soru');
  let cevaplar = [];
  let eksikVar = false;

  sorular.forEach(soruDiv => {
    const soruId = soruDiv.dataset.soruId;
    const secili = document.querySelector(`input[name="soru_${soruId}"]:checked`);
    if (secili) {
      cevaplar.push({
        soru_id: parseInt(soruId),
        secenek_id: parseInt(secili.value)
      });
    } else {
      eksikVar = true;
    }
  });

  if (eksikVar) {
    alert("Lütfen tüm soruları işaretlediğinizden emin olun.");
    return;
  }

  try {
    const yanit = await fetch('/api/sinav/cevap_kaydet', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        sinav_id: mevcutSinavId,
        cevaplar: cevaplar
      })
    });

    if (yanit.ok) {
      document.getElementById('ogrenci-sorular-alani').style.display = 'none';
      document.getElementById('btn-sinav-gonder').style.display = 'none';
      document.getElementById('sinav-bitis-mesaji').style.display = 'block';
    }
  } catch (e) {
    alert("Bağlantı hatası, cevaplar gönderilemedi!");
  }
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

    if (veri.cikis_onaylandi) {
      document.body.innerHTML = '<h2 style="color:white; text-align:center; margin-top:50px;">Öğretmen çıkışınızı onayladı. Tarayıcı kapatılıyor...</h2>';
      window.location.href = '/seb-quit';
      return;
    }

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

async function yardimTalepEt() {
  const btn = document.getElementById('btn-yardim-talep');
  if (!btn) return;

  try {
    btn.innerHTML = '⏳ Gönderiliyor...';
    btn.disabled = true;
    btn.style.backgroundColor = '#718096';
    btn.style.transform = 'none';

    const res = await fetch('/api/yardim_talep', { method: 'POST' });
    const data = await res.json();

    if (data.durum === 'ok') {
      btn.innerHTML = '✅ Yardım Bekleniyor...';
      btn.style.backgroundColor = '#48bb78';
    } else {
      alert('Hata: ' + data.mesaj);
      btn.disabled = false;
      btn.innerHTML = '🙋‍♂️ Yardım İste';
      btn.style.backgroundColor = '#2b6cb0';
    }
  } catch (e) {
    alert("Hata oluştu.");
    btn.disabled = false;
    btn.innerHTML = '🙋‍♂️ Yardım İste';
    btn.style.backgroundColor = '#2b6cb0';
  }
}


async function cikisTalepEt() {
  const btn = document.getElementById('btn-cikis-talep');
  if (!btn) return;

  if (!confirm("Sınavı bitirmek ve Güvenli Tarayıcıdan çıkış yapmak istediğinize emin misiniz?")) return;

  try {
    btn.innerHTML = '⏳ Bekleniyor...';
    btn.disabled = true;
    btn.style.backgroundColor = '#718096';
    btn.style.transform = 'none';

    const res = await fetch('/api/seb_cikis_talep', { method: 'POST' });
    const data = await res.json();

    if (data.durum === 'ok') {
      btn.innerHTML = 'Öğretmen onayı bekleniyor...';
    } else {
      alert('Hata: ' + data.mesaj);
      btn.disabled = false;
      btn.innerHTML = '🚪 Çıkış Talep Et';
      btn.style.backgroundColor = '#c53030';
    }
  } catch (e) {
    alert("Hata oluştu.");
    btn.disabled = false;
    btn.innerHTML = '🚪 Çıkış Talep Et';
    btn.style.backgroundColor = '#c53030';
  }
}

// SEB kapandığında / Sayfa tazelendiğinde arka plana log at
window.addEventListener('beforeunload', function (e) {
  if (suAnkiDurum.mod === 'sinav' || suAnkiDurum.mod === 'terminal' || suAnkiDurum.mod === 'slayt') {
    navigator.sendBeacon('/api/seb_cikis');
  }
});
