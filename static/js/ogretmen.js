const YOKLAMA_ARALIK = 5000;

// Centralized Fetch for Cloudflare Access Session Handling
async function safeFetch(url, options = {}) {
  try {
    const res = await fetch(url, options);
    // Cloudflare Access check: If redirected to login page or 401/403
    if (res.url && res.url.includes('cloudflareaccess.com')) {
      alert("Oturum süreniz dolmuş olabilir. Sayfa yenileniyor...");
      window.location.reload();
      return new Promise(() => { }); // Never resolve
    }
    return res;
  } catch (e) {
    // If it's a "Failed to fetch" error, it's very likely a CORS block from Cloudflare redirect
    if (e.name === 'TypeError' && e.message === 'Failed to fetch') {
      console.warn("Fetch failed, possibly Cloudflare session timeout. Reloading...");
      window.location.reload();
    }
    throw e;
  }
}

function tabGec(tab, btn) {
  document.querySelectorAll('.panel-bolum').forEach(el => el.classList.remove('goster'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('aktif'));
  document.getElementById('tab-' + tab).classList.add('goster');
  btn.classList.add('aktif');
  if (tab === 'siniflar') sinifDurumCek();
}

async function modDegistir(mod) {
  const slaytSecici = document.getElementById('slayt-secici');
  const dosya = slaytSecici ? slaytSecici.value : '';

  const veri = { mod, dosya };

  // Terminal modu için URL'i ekle
  if (mod === 'terminal') {
    const configTtyd = document.getElementById('config-ttyd-url');
    if (configTtyd) {
      veri.terminal_url = configTtyd.value;
    }
  }

  // Slayt moduna geçiliyorsa hash'i sıfırla
  if (mod === 'slayt') {
    veri.slayt_hash = '';
    sonHash = ''; // Frontend'de de sıfırla
    console.log('🔄 Slayt modu, hash sıfırlandı');
  }

  await safeFetch('/api/mod', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(veri)
  });

  document.querySelectorAll('.btn-mod').forEach(btn => {
    btn.classList.toggle('aktif', btn.dataset.mod === mod);
  });
}

async function ayarlariKaydet() {
  const chrootIp = document.getElementById('config-chroot-ip').value;
  const chrootPort = document.getElementById('config-chroot-port').value;
  const chrootUser = document.getElementById('config-chroot-user').value;
  const chrootPass = document.getElementById('config-chroot-pass').value;
  const systemHost = document.getElementById('config-system-host').value;
  const ttydUrl = document.getElementById('config-ttyd-url').value;

  // Kiosk Modu Toggle
  const kioskModuSelect = document.getElementById('config-kiosk-modu');
  const kioskModu = kioskModuSelect ? kioskModuSelect.value : '1'; // Default: Açık

  const yanit = await safeFetch('/api/config', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chroot_host: chrootIp,
      chroot_port: chrootPort,
      chroot_user: chrootUser,
      chroot_pass: chrootPass,
      system_host: systemHost,
      ttyd_url: ttydUrl,
      kiosk_modu: kioskModu
    })
  });

  const veri = await yanit.json();
  if (veri.durum === 'ok') {
    alert('Ayarlar başarıyla kaydedildi!');
  } else {
    alert('Ayarlar kaydedilirken hata oluştu!');
  }
}

async function terminalUrlAyarla() {
  const terminalInput = document.getElementById('terminal-url');
  const userInput = document.getElementById('terminal-user');
  const passInput = document.getElementById('terminal-pass');

  if (!terminalInput) return;

  let url = terminalInput.value.trim();
  if (!url) {
    alert('Lütfen bir URL girin');
    return;
  }

  // Credential varsa URL'e ekle
  if (userInput && userInput.value && passInput && passInput.value) {
    const user = userInput.value.trim();
    const pass = passInput.value.trim();

    // URL'de protocol varsa ayır
    if (url.includes('://')) {
      const [protocol, rest] = url.split('://');
      url = `${protocol}://${user}:${pass}@${rest}`;
    } else {
      url = `http://${user}:${pass}@${url}`;
    }
  }

  // Terminal moduna geç
  await modDegistir('terminal');
  alert(`TTYD URL ayarlandı!\n\nÖğrenciler bu terminali görebilecek.`);
}

async function slaytDegistir() {
  const secici = document.getElementById('slayt-secici');
  if (!secici) return;
  await modDegistir('slayt');
}

function slaytOnizlemeAc() {
  const secici = document.getElementById('slayt-secici');
  if (!secici) return;

  const dosya = secici.value;
  if (!dosya) {
    alert('Lütfen bir slayt seçin.');
    return;
  }

  const modal = document.getElementById('slayt-onizleme-modal');
  const iframe = document.getElementById('slayt-onizleme-iframe');

  if (modal && iframe) {
    iframe.src = '/slayt/' + dosya;
    modal.style.display = 'flex';

    // İlk yükleme için hash'i gönder
    iframe.onload = function () {
      try {
        const hash = iframe.contentWindow.location.hash;
        if (hash) slaytHashGonder(hash);
      } catch (e) {
        // Cross-origin hatası yok say
      }
    };
  }
}

function slaytOnizlemeKapat() {
  const modal = document.getElementById('slayt-onizleme-modal');
  if (modal) {
    modal.style.display = 'none';
  }
}

function hashGonder() {
  // Manuel hash gönderme - debug için
  const iframe = document.getElementById('slayt-onizleme-iframe');
  if (!iframe) {
    alert('❌ iframe bulunamadı!');
    return;
  }

  try {
    const hash = iframe.contentWindow.location.hash;
    console.log('🔧 Manuel hash gönderme:', hash);
    alert(`📤 Mevcut hash: ${hash || '(yok)'}\n\nConsole detayları için F12'`);

    if (hash) {
      slaytHashGonder(hash);
    } else {
      alert('⚠️ Hash yok! Slaytta ileri/geri gitmeyi deneyin.');
    }
  } catch (e) {
    console.error('❌ Cross-origin hatası:', e);
    alert('❌ Cross-Origin hatası!\n\niframe içeriği okunamıyor.\n\nConsolu kontrol et (F12)');
  }
}

function slaytOnizleme(dosya) {
  // Slayt değiştiğinde otomatik önizleme güncelle (modal açıksa)
  const modal = document.getElementById('slayt-onizleme-modal');
  const iframe = document.getElementById('slayt-onizleme-iframe');

  if (modal && modal.style.display === 'flex' && iframe && dosya) {
    iframe.src = '/slayt/' + dosya;
  }
}

async function yoklamaCek() {
  try {
    const yanit = await safeFetch('/api/yoklama');
    const veri = await yanit.json();

    const sayac = document.getElementById('ogrenci-sayisi');
    if (sayac) sayac.textContent = veri.ogrenciler.length;

    const liste = document.getElementById('ogrenci-listesi');
    if (!liste) return;

    if (veri.ogrenciler.length === 0) {
      liste.innerHTML = '<div class="bos-liste">Henüz kimse bağlanmadı...</div>';
      return;
    }

    liste.innerHTML = veri.ogrenciler.map(o => `
      <div class="ogrenci-satir">
        <div class="badge"></div>
        <div class="isim">${o.ad_soyad}</div>
        <div class="numara">${o.numara}</div>
        <div class="sinif-etiket" style="font-size:0.75rem;color:#90cdf4;margin-left:auto;">${o.sinif || ''}</div>
        <div style="font-size:0.75rem;color:#a0aec0;margin-left:0.5rem;" title="Bağlantı IP Adresi">🌐 ${o.ip || ''}</div>
        ${o.paket && o.paket !== '—' ? `<div class="paket-etiket" style="font-size:0.7rem;color:#68d391;background:#1a3a2a;border:1px solid #2d6a4a;border-radius:4px;padding:0.1rem 0.4rem;margin-left:0.4rem;">📦 ${o.paket.split(' ')[0] + ' ' + o.paket.split(' ')[1]}</div>` : ''}
        ${o.kaynak === 'manuel' ? `<span title="Manuel giriş" style="font-size:0.7rem;color:#f6c90e;background:#2d2a00;border:1px solid #6b5900;border-radius:4px;padding:0.1rem 0.4rem;margin-left:0.4rem;">👨‍🏫 M</span>` : ''}
        <div class="saat">${o.saat}</div>
        <button
          onclick="tekSil('${o.numara}', '${o.ad_soyad.replace(/'/g, "\\'")}')"
          style="margin-left:0.5rem;padding:0.15rem 0.5rem;font-size:0.7rem;background:#742a2a;border:1px solid #9b2c2c;border-radius:4px;color:#feb2b2;cursor:pointer;"
          title="Kaydı sil">
          🗑️
        </button>
      </div>
    `).join('');
  } catch (e) { /* sessiz */ }
}

async function sinifDurumCek() {
  try {
    const sinifYanit = await safeFetch('/api/siniflar');
    const siniflar = await sinifYanit.json();
    const grid = document.getElementById('sinif-grid');
    if (!grid) return;

    // Toplam kayıtlı sayısını güncelle
    const toplamKayitli = siniflar.siniflar.reduce((t, s) => t + s.kayitli, 0);
    const el = document.getElementById('kayitli-sayisi');
    if (el) el.textContent = toplamKayitli;

    // Her sınıf için detay çek
    let html = '';
    for (const sinif of siniflar.siniflar) {
      const detayYanit = await safeFetch(`/api/sinif_ogrencileri/${sinif.id}`);
      const veri = await detayYanit.json();

      const geldi = veri.ogrenciler.filter(o => o.geldi);
      const gelmedi = veri.ogrenciler.filter(o => !o.geldi);
      const tamKatilim = geldi.length === sinif.kayitli && sinif.kayitli > 0;

      html += `
        <div class="sinif-kart">
          <h4>
            ${sinif.ad}
            <span class="sinif-badge ${tamKatilim ? 'tam' : ''}">${sinif.bugun}/${sinif.kayitli}</span>
          </h4>
          <div class="sinif-ozet">Bugün ${sinif.bugun} katıldı · ${sinif.kayitli - sinif.bugun} eksik</div>
          ${veri.ogrenciler.map(o => `
            <div class="ogrenci-mini ${o.geldi ? '' : 'devamsiz'}" id="ogrenci-${o.numara}">
              <div class="${o.geldi ? 'dot-geldi' : 'dot-gelmedi'}"></div>
              <span>${o.ad_soyad}</span>
              ${o.geldi && o.paket && o.paket !== '—' ? `<span style="font-size:0.65rem;color:#68d391;background:#1a3a2a;border-radius:3px;padding:0 0.3rem;margin-left:0.3rem;">${o.paket.split(' ')[0] + ' ' + o.paket.split(' ')[1]}</span>` : ''}
              ${o.geldi && o.paket === 'manuel' ? `<span style="font-size:0.65rem;color:#f6c90e;margin-left:0.2rem;" title="Manuel giriş">👨‍🏫</span>` : ''}
              <span style="margin-left:auto;color:#718096;font-size:0.75rem;">${o.numara}</span>
              ${!o.geldi ? `<button
                onclick="manuelGiris(${sinif.id}, '${o.numara}', '${o.ad_soyad.replace(/'/g, '\\\'')}')"
                style="margin-left:0.5rem;padding:0.15rem 0.5rem;font-size:0.7rem;background:#2d3a1a;border:1px solid #4a6a2a;border-radius:4px;color:#a0d070;cursor:pointer;"
                title="Manuel giriş ekle">
                + Giriş
              </button>` : ''}
            </div>
          `).join('')}
        </div>
      `;
    }
    grid.innerHTML = html;
  } catch (e) { console.error(e); }
}

async function manuelGiris(sinifId, numara, adSoyad) {
  // Kullanıcı isteği: Onay sormadan direkt işlem yap

  try {
    const yanit = await safeFetch('/api/manuel_giris', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sinif_id: sinifId, numara, ad_soyad: adSoyad })
    });
    const veri = await yanit.json();

    if (veri.durum === 'ok') {
      // Sayfayı yenile (liste + sınıf kartı)
      await Promise.all([sinifDurumCek(), yoklamaCek()]);
    } else {
      alert('Hata: ' + veri.mesaj);
    }
  } catch (e) {
    alert('Bağlantı hatası: ' + e.message);
  }
}

async function csvIndir() {
  window.location.href = '/api/yoklama/csv';
}

async function arsivCSVIndir() {
  const tarihInput = document.getElementById('tarih-secici');
  if (!tarihInput || !tarihInput.value) {
    alert('Lütfen bir tarih seçin.');
    return;
  }

  const tarih = tarihInput.value; // YYYY-MM-DD formatında

  try {
    const yanit = await safeFetch('/api/yoklama/tarih_csv?tarih=' + encodeURIComponent(tarih));
    if (yanit.ok) {
      const dosyaAdi = yanit.headers.get('Content-Disposition') || 'yoklama.csv';

      // Blob oluştur
      const blob = await yanit.blob();
      const url = window.URL.createObjectURL(blob);

      // İndir
      const a = document.createElement('a');
      a.href = url;
      a.download = dosyaAdi.match(/filename="(.+)"/)[1];
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } else {
      // Handle non-200 responses, e.g., 404
      if (yanit.status === 404) {
        alert('Bu tarihte kayıt bulunamadı.');
      } else {
        const errorText = await yanit.text();
        alert('Hata: ' + errorText);
      }
    }
  } catch (e) {
    alert('Bağlantı hatası: ' + e.message);
  }
}

async function yoklamaTemizle() {
  const sayi = document.getElementById('ogrenci-sayisi').textContent;
  if (sayi === '0') {
    alert('Silinecek kayıt yok.');
    return;
  }

  // Kullanıcı isteği: Onay sormadan direkt sil

  try {
    const yanit = await safeFetch('/api/yoklama/sil', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ onay: true })
    });
    const veri = await yanit.json();

    if (veri.durum === 'ok') {
      console.log(`✅ ${veri.silinen} kayıt silindi.`);
      await yoklamaCek();
      await sinifDurumCek();
    } else {
      alert('Hata: ' + veri.mesaj);
    }
  } catch (e) {
    alert('Bağlantı hatası: ' + e.message);
  }
}

async function tekSil(numara, adSoyad) {
  // Kullanıcı isteği: Onay sormadan direkt sil

  try {
    const yanit = await safeFetch('/api/yoklama/sil_tek', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ numara })
    });
    const veri = await yanit.json();

    if (veri.durum === 'ok') {
      await yoklamaCek();
      await sinifDurumCek();
    } else {
      alert('Hata: ' + veri.mesaj);
    }
  } catch (e) {
    alert('Bağlantı hatası: ' + e.message);
  }
}

async function sahteLogSil(kayitId) {
  // Kullanıcı isteği: Onay sormadan direkt sil

  try {
    const yanit = await safeFetch('/api/sahte_log/sil_tek', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: kayitId })
    });
    const veri = await yanit.json();

    if (veri.durum === 'ok') {
      await sahteCek();
    } else {
      alert('Hata: ' + veri.mesaj);
    }
  } catch (e) {
    alert('Bağlantı hatası: ' + e.message);
  }
}

// ── Şüpheli Giriş Logu ───────────────────────────────────────
async function sahteCek() {
  const kutu = document.getElementById('sahte-kutu');
  if (!kutu) return;

  try {
    const yanit = await safeFetch('/api/sahte_log');
    const veri = await yanit.json();
    const kayitlar = veri.kayitlar || [];

    // Rozet güncelle
    const rozet = document.getElementById('sahte-rozet');
    if (rozet) {
      rozet.textContent = kayitlar.length;
      rozet.style.display = kayitlar.length ? 'inline-block' : 'none';
    }

    if (kayitlar.length === 0) {
      kutu.innerHTML = '<div style="color:#718096;text-align:center;padding:1rem;">Şüpheli giriş girişimi yok 🎉</div>';
      return;
    }

    let html = '';
    for (const k of kayitlar) {
      html += `
        <div style="
          background:#1a1008;
          border:1px solid #744210;
          border-left:4px solid #dd6b20;
          border-radius:6px;
          padding:0.75rem 1rem;
          margin-bottom:0.5rem;
          font-size:0.82rem;
          line-height:1.7;
          position:relative;
        ">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
            <span style="color:#f6ad55;font-weight:600;">⚠️ Sahte Giriş Girişimi</span>
            <div style="display:flex;align-items:center;gap:0.5rem;">
              <span style="color:#718096;">${k.tarih} ${k.saat.substring(0, 5)} · ${k.sinif}</span>
              <button
                onclick="sahteLogSil(${k.id})"
                style="padding:0.15rem 0.5rem;font-size:0.7rem;background:#742a2a;border:1px solid #9b2c2c;border-radius:4px;color:#feb2b2;cursor:pointer;"
                title="Log kaydını sil">
                🗑️ Sil
              </button>
            </div>
          </div>
          <div style="color:#e2e8f0;">
            <span style="color:#fc8181;">🔒 Gerçek:</span>
            <strong>${k.gercek_ad}</strong>
            <span style="color:#718096;">(#${k.gercek_numara})</span>
            &nbsp;—&nbsp;bu IP'den önceden giriş yapmıştı.
          </div>
          <div style="color:#e2e8f0;">
            <span style="color:#fbd38d;">🚫 Deneme:</span>
            <strong>${k.denenen_ad}</strong>
            <span style="color:#718096;">(#${k.denenen_numara})</span>
            &nbsp;aynı cihazdan giriş yapmaya çalıştı.
          </div>
          <div style="color:#718096;font-size:0.75rem;margin-top:0.2rem;">IP: ${k.ip}</div>
        </div>`;
    }
    kutu.innerHTML = html;
  } catch (e) { console.error('sahte log hatası:', e); }
}

// ── Güvenlik Uyarıları ───────────────────────────────────────────
let guvenlikSoketi = null;

function guvenlikSoketBaslat() {
  if (typeof io === 'undefined') {
    console.warn('⚠️ Socket.IO yüklenemedi, güvenlik uyarıları pasif.');
    return;
  }
  try {
    // Terminal namespace'ine bağlan
    guvenlikSoketi = io('/terminal', {
      transports: ['websocket', 'polling']
    });

    guvenlikSoketi.on('connect', () => {
      console.log('Güvenlik soketi bağlandı');
      // Öğretmen olarak kayıt ol
      guvenlikSoketi.emit('ogretmen_baglan', { ogretmen: true });
    });

    guvenlikSoketi.on('guvenlik_uyari', (mesaj) => {
      // Sesli uyarı
      try {
        const audio = new Audio('/static/sounds/alert.mp3');
        audio.play().catch(e => console.log('Ses çalınamadı:', e));
      } catch (e) { }

      // Ekran uyarısı
      alert('⚠️ GÜVENLİK UYARISI ⚠️\n\n' + mesaj);

      // Logları yenile
      guvenlikLogCek();
    });

    guvenlikSoketi.on('disconnect', () => {
      console.log('Güvenlik soketi kesildi');
    });

  } catch (e) {
    console.error('Güvenlik soketi hatası:', e);
  }
}

async function guvenlikLogCek() {
  try {
    const yanit = await safeFetch('/api/terminal/guvenlik_log');
    const veri = await yanit.json();

    const logDiv = document.getElementById('guvenlik-log-kutu');
    if (!logDiv) return;

    if (veri.loglar.length === 0) {
      logDiv.innerHTML = '<div style="color:#718096;text-align:center;padding:1rem;">Güvenlik logu yok</div>';
      return;
    }

    let html = '';
    for (const log of veri.loglar) {
      const renk = log.durum === 'BASARILI' ? '#48bb78' : '#e53e3e';
      const ikon = log.durum === 'BASARILI' ? '✅' : '⚠️';

      html += `
        <div style="
          background: ${log.durum === 'BASARILI' ? 'rgba(72,187,120,0.1)' : 'rgba(229,62,62,0.1)'};
          border: 1px solid ${renk};
          border-left: 4px solid ${renk};
          border-radius: 6px;
          padding: 0.75rem 1rem;
          margin-bottom: 0.5rem;
          font-size: 0.82rem;
        ">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
            <span style="color:${renk};font-weight:600;">${ikon} ${log.durum}</span>
            <span style="color:#718096;">${log.tarih} ${log.saat.substring(0, 5)}</span>
          </div>
          <div style="color:#e2e8f0;">
            <span style="color:#90cdf4;">${log.session_ad}</span>
            (${log.session_numara})
          </div>
          ${log.durum === 'GUVENLIK_IHLALI' ? `
            <div style="color:#fc8181;">
              Girmeye çalışan: <strong>${log.girilen_numara}</strong>
            </div>
          ` : ''}
          <div style="color:#718096;font-size:0.75rem;">IP: ${log.ip}</div>
        </div>
      `;
    }

    logDiv.innerHTML = html;
  } catch (e) {
    console.error('Güvenlik log hatası:', e);
  }
}

async function sebCikisCek() {
  try {
    const yanit = await safeFetch('/api/seb_cikis_log');
    const veri = await yanit.json();

    const div = document.getElementById('seb-cikis-kutu');
    if (!div) return;

    if (!veri.loglar || veri.loglar.length === 0) {
      div.innerHTML = '<div style="color:#718096;text-align:center;padding:1rem;">Bugün sayfadan ayrılan/kapatan öğrenci kaydı yok.</div>';
      return;
    }

    let html = '<table class="veri-tablosu" style="width:100%; border-collapse:collapse;">';
    html += '<thead><tr style="border-bottom:1px solid #4a5568;"><th style="padding:0.5rem;text-align:left;">Zaman</th><th style="padding:0.5rem;text-align:left;">Öğrenci No</th><th style="padding:0.5rem;text-align:left;">Ad Soyad</th><th style="padding:0.5rem;text-align:left;">IP Adresi</th></tr></thead>';
    html += '<tbody>';

    veri.loglar.forEach(log => {
      html += `<tr style="border-bottom:1px solid #2d3748; background:rgba(229,62,62,0.1);">
            <td style="padding:0.5rem;color:#fc8181;">${log.tarih} ${log.saat.substring(0, 5)}</td>
            <td style="padding:0.5rem;">${log.numara}</td>
            <td style="padding:0.5rem;">${log.ad_soyad}</td>
            <td style="padding:0.5rem;color:#a0aec0;font-size:0.85rem;">${log.ip}</td>
        </tr>`;
    });

    html += '</tbody></table>';
    div.innerHTML = html;
  } catch (e) {
    console.error('SEB çıkış log çekme hatası:', e);
  }
}

// ── Slayt Hash Takibi ─────────────────────────────────────────────
let sonHash = '';

function slaytHashGonder(hash) {
  const takipCheckbox = document.getElementById('ogrenci-takip');
  if (!takipCheckbox || !takipCheckbox.checked) {
    console.log('⏸️ Senkronizasyon kapalı, hash gönderilmiyor');
    return;
  }

  if (hash === sonHash) {
    console.log('⏭️ Aynı hash, atlanıyor:', hash);
    return; // Aynı hash'i tekrar gönderme
  }

  console.log('📤 Hash gönderiliyor:', hash);
  sonHash = hash;

  // API URL'i config'den al (production için API proxy)
  const apiUrl = (window.API_BASE || '') + '/api/durum?hash=' + encodeURIComponent(hash);

  // GET request ile query parametresi olarak gönder (Cloudflare Access CORS sorunu için)
  safeFetch(apiUrl)
    .then(res => {
      console.log('✅ Hash gönderildi:', hash);
      return res.json();
    })
    .then(data => {
      console.log('📊 Sunucu yanıtı:', data);
    })
    .catch(e => console.error('❌ Hash gönderme hatası:', e));
}

function slaytHashKontrol() {
  const iframe = document.getElementById('slayt-onizleme-iframe');
  const modal = document.getElementById('slayt-onizleme-modal');
  const takipCheckbox = document.getElementById('ogrenci-takip');

  if (!iframe || !modal || modal.style.display !== 'flex' || !takipCheckbox.checked) return;

  try {
    const currentHash = iframe.contentWindow.location.hash;
    console.log('🔍 Hash kontrolü:', { currentHash, sonHash, iframeSrc: iframe.src });

    if (currentHash && currentHash !== sonHash) {
      slaytHashGonder(currentHash);
    }
  } catch (e) {
    console.error('⚠️ Cross-origin hash okuma hatası:', e);
    // Cross-origin hatası yok say
  }
}

// Her 500ms'de bir hash kontrol et
setInterval(slaytHashKontrol, 500);

// ── Mod değiştirme yardımcı fonksiyonları ───────────────────────────
function terminalModu() {
  modDegistir('terminal').then(() => {
    window.location.href = '/teacher/terminal';
  });
}

function terminalOnizlemeKapat() {
  const modal = document.getElementById('terminal-onizleme-modal');
  const iframe = document.getElementById('terminal-onizleme-iframe');
  if (modal) modal.style.display = 'none';
  if (iframe) iframe.src = 'about:blank';
}

function bekletModu() {
  modDegistir('bekleme');
}

function slaytModu() {
  modDegistir('slayt');
}

document.addEventListener('DOMContentLoaded', () => {
  yoklamaCek();
  sahteCek();
  guvenlikSoketBaslat();  // Güvenlik uyarılarını dinle

  // Eski URL kontrolü ve otomatik düzeltme (Eskiden /terminal-yayin kullanılıyordu)
  const ttydUrlInput = document.getElementById('config-ttyd-url');
  if (ttydUrlInput && ttydUrlInput.value.includes('terminal-yayin')) {
    console.log('🔄 Eski terminal URL düzeltiliyor...');
    ttydUrlInput.value = '/terminal';
  }

  setInterval(yoklamaCek, YOKLAMA_ARALIK);
  setInterval(sahteCek, 30_000);   // 30 saniyede bir kontrol
});

// ── Sınav / Quiz Yönetimi ──

async function sinavListesiniGuncelle() {
  const yanit = await safeFetch('/api/sinav/liste');
  const veri = await yanit.json();
  const kutu = document.getElementById('sinav-listesi-kutu');

  if (!veri.sinavlar || veri.sinavlar.length === 0) {
    kutu.innerHTML = '<div style="color:#718096;text-align:center;">Henüz sınav oluşturulmamış.</div>';
    return;
  }

  let html = '<table style="width:100%; border-collapse:collapse; margin-top:1rem; color:#e2e8f0; font-size:0.9rem;">';
  html += '<tr style="border-bottom:1px solid #4a5568; color:#a0aec0; text-align:left;">';
  html += '<th style="padding:0.5rem;">Sınav Adı</th>';
  html += '<th style="padding:0.5rem;">Soru Sayısı</th>';
  html += '<th style="padding:0.5rem;">Durum</th>';
  html += '<th style="padding:0.5rem;text-align:right;">İşlemler</th>';
  html += '</tr>';

  veri.sinavlar.forEach(s => {
    const durumBadge = s.aktif ?
      '<span style="background:#48bb78;color:#fff;padding:2px 8px;border-radius:12px;font-size:0.75rem;">Aktif (Yayında)</span>' :
      '<span style="background:#718096;color:#fff;padding:2px 8px;border-radius:12px;font-size:0.75rem;">Beklemede</span>';

    html += `<tr style="border-bottom:1px solid #2d3748;">
          <td style="padding:0.5rem;">${s.baslik}</td>
          <td style="padding:0.5rem;">${s.soru_sayisi} Soru</td>
          <td style="padding:0.5rem;">${durumBadge}</td>
          <td style="padding:0.5rem;text-align:right;">
             <button class="btn-kucuk" style="background:#3182ce;" onclick="soruYonetiminiAc(${s.id}, '${s.baslik}')">📝 Sorular</button>
             <button class="btn-kucuk yeşil" onclick="sinavSonuclariniAc(${s.id}, '${s.baslik}')">📊 Sonuçlar</button>
             <button class="btn-kucuk" style="background:${s.aktif ? '#e53e3e' : '#48bb78'};" onclick="sinavDurumDegistir(${s.id}, ${!s.aktif})">
                ${s.aktif ? '⏹ Yayını Durdur' : '▶ Sınavı Başlat'}
             </button>
          </td>
      </tr>`;
  });

  html += '</table>';
  kutu.innerHTML = html;
}

async function sinavOlustur() {
  const baslik = document.getElementById('yeni-sinav-baslik').value;
  if (!baslik.trim()) {
    alert("Sınav başlığı boş olamaz!");
    return;
  }

  const yanit = await safeFetch('/api/sinav/olustur', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ baslik })
  });

  if (yanit.ok) {
    document.getElementById('yeni-sinav-baslik').value = '';
    sinavListesiniGuncelle();
  } else {
    alert("Hata oluştu.");
  }
}

async function sinavDurumDegistir(id, aktifYap) {
  if (aktifYap && !confirm("Bu sınavı başlatmak istediğinize emin misiniz? Öğrenci ekranlarında otomatik olarak bu sınav açılacaktır.")) return;
  if (!aktifYap && !confirm("Sınav yayından kaldırılsın mı?")) return;

  const yanit = await safeFetch('/api/sinav/aktiflestir', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sinav_id: id, aktif: aktifYap })
  });

  if (yanit.ok) {
    sinavListesiniGuncelle();
    if (aktifYap) {
      document.querySelectorAll('.btn-mod').forEach(btn => btn.classList.remove('aktif'));
    }
  }
}

async function soruYonetiminiAc(sinavId, baslik) {
  document.getElementById('soru-yonetimi-alani').style.display = 'block';
  document.getElementById('sinav-sonuclari-alani').style.display = 'none';
  document.getElementById('aktif-sinav-baslik').innerText = `Soru Yönetimi: ${baslik}`;
  document.getElementById('soru-sinav-id').value = sinavId;

  // Mevcut soruları çek
  mevcutSorulariGetir(sinavId);
}

function soruEklemeKapat() {
  document.getElementById('soru-yonetimi-alani').style.display = 'none';
}

async function mevcutSorulariGetir(sinavId) {
  const yanit = await safeFetch(`/api/sinav/sorular/${sinavId}`);
  const veri = await yanit.json();

  document.getElementById('mevcut-soru-sayisi').innerText = veri.sorular.length;

  const kutu = document.getElementById('mevcut-sorular-listesi');
  if (veri.sorular.length === 0) {
    kutu.innerHTML = '<div style="color:#718096;">Soru eklenmemiş.</div>';
    return;
  }

  let html = '';
  veri.sorular.forEach((s, idx) => {
    html += `<div style="background:#1a202c; padding:1rem; border-radius:6px; margin-bottom:1rem; border:1px solid #4a5568;">
          <div style="font-weight:bold; color:#e2e8f0; margin-bottom:0.5rem;">Soru ${idx + 1}: ${s.metin} <span style="color:#a0aec0;font-size:0.8rem;font-weight:normal;">(${s.puan} Puan)</span></div>`;

    s.secenekler.forEach((sec, sIdx) => {
      const isCorrect = sec.dogru_mu ? '✅' : '❌';
      const color = sec.dogru_mu ? '#48bb78' : '#a0aec0';
      html += `<div style="color:${color}; font-size:0.9rem; margin-left:1rem; margin-bottom:0.25rem;">${String.fromCharCode(65 + sIdx)}) ${sec.metin} ${sec.dogru_mu ? '(Doğru Cevap)' : ''}</div>`;
    });
    html += `</div>`;
  });
  kutu.innerHTML = html;
}

async function soruKaydet() {
  const sinavId = document.getElementById('soru-sinav-id').value;
  const metin = document.getElementById('soru-metni').value;

  let secenekler = [];
  let secilenDogruIndex = parseInt(document.querySelector('input[name="dogru_secenek"]:checked').value);

  for (let i = 0; i < 4; i++) {
    let optText = document.getElementById(`secenek-${i}`).value.trim();
    if (optText !== '') {
      secenekler.push({
        metin: optText,
        dogru_mu: (secilenDogruIndex === i)
      });
    }
  }

  if (secenekler.length < 2) {
    alert("En az 2 seçenek girmelisiniz!");
    return;
  }
  if (!metin.trim()) {
    alert("Soru metni boş olamaz!");
    return;
  }

  const yanit = await safeFetch('/api/sinav/soru_ekle', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sinav_id: sinavId, metin: metin, secenekler: secenekler, puan: 10 })
  });

  if (yanit.ok) {
    // Formu temizle
    document.getElementById('soru-metni').value = '';
    for (let i = 0; i < 4; i++) document.getElementById(`secenek-${i}`).value = '';
    document.querySelectorAll('input[name="dogru_secenek"]')[0].checked = true;

    mevcutSorulariGetir(sinavId);
    sinavListesiniGuncelle(); // Listede soru sayısını güncelle
  } else {
    const v = await yanit.json();
    alert("Hata: " + (v.mesaj || 'Bilinmeyen hata'));
  }
}

async function sinavSonuclariniAc(sinavId, baslik) {
  document.getElementById('sinav-sonuclari-alani').style.display = 'block';
  document.getElementById('soru-yonetimi-alani').style.display = 'none';
  document.getElementById('sonuc-sinav-baslik').innerText = `Sınav Sonuçları: ${baslik}`;

  const tablo = document.getElementById('sinav-sonuclari-tablo');
  tablo.innerHTML = '<div style="color:#718096;text-align:center;">Sonuçlar yükleniyor...</div>';

  const yanit = await safeFetch(`/api/sinav/sonuclar/${sinavId}`);
  const veri = await yanit.json();

  if (!veri.sonuclar || veri.sonuclar.length === 0) {
    tablo.innerHTML = '<div style="color:#718096;text-align:center;">Henüz bu sınavı çözen öğrenci yok.</div>';
    return;
  }

  let html = '<table style="width:100%; border-collapse:collapse; margin-top:1rem; color:#e2e8f0; font-size:0.9rem;">';
  html += '<tr style="border-bottom:1px solid #4a5568; color:#a0aec0; text-align:left;">';
  html += '<th style="padding:0.5rem;">Öğrenci No</th>';
  html += '<th style="padding:0.5rem;">Ad Soyad</th>';
  html += '<th style="padding:0.5rem;">Puanı</th>';
  html += '</tr>';

  veri.sonuclar.sort((a, b) => b.toplam_puan - a.toplam_puan).forEach(s => {
    html += `<tr style="border-bottom:1px solid #2d3748;">
          <td style="padding:0.5rem;">${s.numara}</td>
          <td style="padding:0.5rem;">${s.ad_soyad}</td>
          <td style="padding:0.5rem;font-weight:bold;color:#48bb78;">${s.toplam_puan} Puan</td>
       </tr>`;
  });
  html += '</table>';
  tablo.innerHTML = html;
}
