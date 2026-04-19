// XSS koruması — kullanıcı verisini HTML'e güvenli şekilde ekle
function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

// JS string literal'i HTML attribute içinde güvenli — inline onclick="fn(${escJsAttr(x)})" için.
// JSON.stringify hem escape hem quote sağlar; sonra HTML attribute için &quot; ile çift kapsama.
function escJsAttr(s) {
  return JSON.stringify(String(s == null ? '' : s))
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

const YOKLAMA_ARALIK = 5000;

// Centralized Fetch for Cloudflare Access Session Handling
async function safeFetch(url, options = {}) {
  try {
    // CSRF Token ekle
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    if (csrfToken) {
      if (!options.headers) options.headers = {};
      options.headers['X-CSRFToken'] = csrfToken;
    }

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
  const slaytKlasoru = document.getElementById('config-slayt-klasoru') ? document.getElementById('config-slayt-klasoru').value : '';
  
  const dbType = document.getElementById('config-db-type').value;
  const dbHost = document.getElementById('config-db-host').value;
  const dbPort = document.getElementById('config-db-port').value;
  const dbUser = document.getElementById('config-db-user').value;
  const dbPass = document.getElementById('config-db-pass').value;
  const dbName = document.getElementById('config-db-name').value;

  // Kiosk Modu Toggle
  const kioskModuSelect = document.getElementById('config-kiosk-modu');
  const kioskModu = kioskModuSelect ? kioskModuSelect.value : '1'; // Default: Açık

  // IP Kontrol Toggle
  const ipKontrolSelect = document.getElementById('config-ip-kontrol');
  const ipKontrol = ipKontrolSelect ? ipKontrolSelect.value : '1';

  // SEB Çıkış İzni
  const cikisIzniSelect = document.getElementById('config-cikis-izni');
  const cikisIzni = cikisIzniSelect ? cikisIzniSelect.value : '0';

  // Ders Günleri
  const dersGunleri = Array.from(document.querySelectorAll('.ders-gun-cb:checked')).map(cb => cb.value).join(',');

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
      slayt_klasoru: slaytKlasoru,
      db_type: dbType,
      db_host: dbHost,
      db_port: dbPort,
      db_user: dbUser,
      db_pass: dbPass,
      db_name: dbName,
      kiosk_modu: kioskModu,
      ip_kontrol: ipKontrol,
      cikis_izni: cikisIzni,
      ders_gunleri: dersGunleri
    })
  });

  const veri = await yanit.json();

  // Devamsizlik esigi kaydet
  const esikInput = document.getElementById('config-devamsizlik-esik');
  if (esikInput) {
    await safeFetch('/api/yoklama/devamsizlik_esik', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ esik: parseInt(esikInput.value) || 3 })
    });
  }

  if (veri.durum === 'ok') {
    alert('Ayarlar başarıyla kaydedildi!');
  } else {
    alert('Ayarlar kaydedilirken hata oluştu!');
  }
}

// ─── Ayarlar kart toggle (collapsible cards + localStorage) ───
function ayarKartToggle(kartAd) {
  var el = document.querySelector('.ayar-kart[data-kart="' + kartAd + '"]');
  if (!el) return;
  el.classList.toggle('kapali');
  ayarKartDurumKaydet();
}
function ayarKartlarHepsiAc() {
  document.querySelectorAll('.ayar-kart').forEach(function(k) { k.classList.remove('kapali'); });
  ayarKartDurumKaydet();
}
function ayarKartlarHepsiKapat() {
  document.querySelectorAll('.ayar-kart').forEach(function(k) { k.classList.add('kapali'); });
  ayarKartDurumKaydet();
}
function ayarKartDurumKaydet() {
  var durumlar = {};
  document.querySelectorAll('.ayar-kart').forEach(function(k) {
    durumlar[k.dataset.kart] = !k.classList.contains('kapali');
  });
  try { localStorage.setItem('ayar-kart-durum', JSON.stringify(durumlar)); } catch (e) {}
}
function ayarKartDurumYukle() {
  try {
    var durumlar = JSON.parse(localStorage.getItem('ayar-kart-durum') || '{}');
    document.querySelectorAll('.ayar-kart').forEach(function(k) {
      if (durumlar[k.dataset.kart] === false) k.classList.add('kapali');
    });
  } catch (e) {}
}
document.addEventListener('DOMContentLoaded', ayarKartDurumYukle);

// ─── Slayt klasör tarayıcı (inline gözat panel) ───
var _slaytGozatMevcutYol = null;

function slaytKlasorGozatAc() {
  var panel = document.getElementById('slayt-gozat-panel');
  if (!panel) return;
  panel.style.display = 'block';
  // İlk açılışta mevcut input'taki yoldan başla, yoksa kök
  var input = document.getElementById('config-slayt-klasoru');
  var baslangic = (input && input.value.trim()) || '';
  slaytKlasorTara(baslangic);
}

function slaytKlasorGozatKapat() {
  var panel = document.getElementById('slayt-gozat-panel');
  if (panel) panel.style.display = 'none';
}

async function slaytKlasorTara(yol) {
  var icerik = document.getElementById('slayt-gozat-icerik');
  var bc = document.getElementById('slayt-gozat-breadcrumb');
  var info = document.getElementById('slayt-gozat-info');
  if (!icerik) return;

  icerik.textContent = '';
  bc.textContent = 'Yükleniyor…';
  if (info) info.textContent = '';

  try {
    var url = '/api/klasor/gozat' + (yol ? '?yol=' + encodeURIComponent(yol) : '');
    var r = await safeFetch(url);
    var res = await r.json();
    if (res.durum !== 'ok') {
      bc.textContent = '';
      var err = document.createElement('div');
      err.style.cssText = 'color:#fc8181;font-size:0.8rem;padding:0.5rem;';
      err.textContent = '❌ ' + (res.mesaj || 'Hata');
      icerik.appendChild(err);
      return;
    }

    _slaytGozatMevcutYol = res.mevcut;
    if (info) info.textContent = res.mevcut_slayt_sayisi + ' slayt bu klasörde';

    // Breadcrumb
    bc.textContent = '';
    res.breadcrumb.forEach(function(b, i) {
      if (i > 0) {
        var sep = document.createElement('span');
        sep.textContent = ' › ';
        sep.style.color = '#4a5568';
        bc.appendChild(sep);
      }
      var link = document.createElement('a');
      link.href = '#';
      link.textContent = b.ad;
      link.style.cssText = 'color:#90cdf4;text-decoration:none;cursor:pointer;';
      link.onclick = function(e) { e.preventDefault(); slaytKlasorTara(b.yol); };
      bc.appendChild(link);
    });

    // Üst klasör
    if (res.ust_yol) {
      var ust = document.createElement('div');
      ust.style.cssText = 'padding:6px 10px;background:#2d3748;border-radius:4px;cursor:pointer;color:#a0aec0;font-size:0.82rem;';
      ust.textContent = '⬆️  .. (üst klasör)';
      ust.onclick = function() { slaytKlasorTara(res.ust_yol); };
      icerik.appendChild(ust);
    }

    // Alt klasörler
    if (res.alt_klasorler.length === 0) {
      var bos = document.createElement('div');
      bos.style.cssText = 'color:#718096;font-size:0.78rem;padding:0.5rem;text-align:center;';
      bos.textContent = '— Alt klasör yok —';
      icerik.appendChild(bos);
    } else {
      res.alt_klasorler.forEach(function(k) {
        var row = document.createElement('div');
        row.style.cssText = 'display:flex;justify-content:space-between;align-items:center;padding:6px 10px;background:#2d3748;border-radius:4px;cursor:pointer;font-size:0.82rem;';
        row.onmouseenter = function() { row.style.background = '#374151'; };
        row.onmouseleave = function() { row.style.background = '#2d3748'; };
        row.onclick = function() { slaytKlasorTara(k.yol); };

        var sol = document.createElement('span');
        sol.style.color = '#e2e8f0';
        sol.textContent = '📁 ' + k.ad;

        var sag = document.createElement('span');
        var sayi = k.slayt_sayisi;
        if (sayi < 0) {
          sag.textContent = '🔒 izin yok';
          sag.style.color = '#fc8181';
        } else if (sayi === 0) {
          sag.textContent = '— boş';
          sag.style.color = '#4a5568';
        } else {
          sag.textContent = sayi + ' slayt';
          sag.style.color = '#48bb78';
        }
        sag.style.fontSize = '0.74rem';

        row.appendChild(sol);
        row.appendChild(sag);
        icerik.appendChild(row);
      });
    }
  } catch (e) {
    bc.textContent = '';
    var err = document.createElement('div');
    err.style.color = '#fc8181';
    err.textContent = '❌ İstek başarısız: ' + (e.message || e);
    icerik.appendChild(err);
  }
}

function slaytKlasorMevcutSec() {
  if (!_slaytGozatMevcutYol) return;
  var input = document.getElementById('config-slayt-klasoru');
  if (input) {
    input.value = _slaytGozatMevcutYol;
    // Otomatik test
    slaytKlasoruTest();
  }
  slaytKlasorGozatKapat();
}

async function slaytKlasoruTest() {
  var input = document.getElementById('config-slayt-klasoru');
  var sonuc = document.getElementById('slayt-klasoru-sonuc');
  if (!input || !sonuc) return;
  var klasor = input.value.trim();
  sonuc.style.color = '#a0aec0';
  sonuc.textContent = 'Test ediliyor… ⏳';
  try {
    var r = await safeFetch('/api/slayt_klasoru/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ klasor: klasor })
    });
    var res = await r.json();
    if (res.durum === 'ok') {
      sonuc.style.color = '#48bb78';
      sonuc.textContent = '✅ ' + res.mesaj + (res.docker ? ' (Docker mount görünür)' : '');
    } else {
      sonuc.style.color = '#fc8181';
      sonuc.textContent = '❌ ' + res.mesaj;
    }
  } catch (e) {
    sonuc.style.color = '#fc8181';
    sonuc.textContent = '❌ İstek başarısız: ' + (e.message || e);
  }
}

async function baglantiTestEt() {
  const sonucSpan = document.getElementById('healthcheck-sonuc');
  sonucSpan.style.color = '#a0aec0';
  sonucSpan.textContent = 'Test ediliyor... ⏳';

  const data = {
    chroot_host: document.getElementById('config-chroot-ip').value.trim(),
    chroot_port: document.getElementById('config-chroot-port').value.trim(),
    chroot_user: document.getElementById('config-chroot-user').value.trim(),
    chroot_pass: document.getElementById('config-chroot-pass').value.trim()
  };

  try {
    const r = await safeFetch('/api/healthcheck', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const res = await r.json();

    if (res.durum === 'ok') {
      sonucSpan.style.color = '#48bb78';
      sonucSpan.textContent = res.mesaj || 'Bağlantı Başarılı ✅';
    } else {
      sonucSpan.style.color = '#e53e3e';
      sonucSpan.textContent = res.mesaj || 'Bağlantı Hatası ❌';
    }
  } catch (err) {
    sonucSpan.style.color = '#e53e3e';
    sonucSpan.textContent = 'İstek gönderilemedi ❌';
    console.error('Bağlantı test hatası:', err);
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

async function yoklamaPaketleriCek() {
  try {
    const tarih = document.getElementById('yoklama-tarih')?.value || '';
    const url = tarih ? '/api/yoklama/paketler?tarih=' + tarih : '/api/yoklama/paketler';
    const yanit = await safeFetch(url);
    const veri = await yanit.json();
    const select = document.getElementById('yoklama-paket-filtre');
    if (!select) return;
    const mevcut = select.value;
    select.textContent = '';
    const tumOpt = document.createElement('option');
    tumOpt.value = '';
    tumOpt.textContent = 'Tüm Paketler';
    select.appendChild(tumOpt);
    veri.paketler.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.paket;
      opt.textContent = p.paket + ' (' + p.sayi + ')';
      select.appendChild(opt);
    });
    if (mevcut) select.value = mevcut;
  } catch (e) { /* sessiz */ }
}

function yoklamaTarihDegisti() {
  yoklamaPaketleriCek();
  yoklamaCek();
}

// Geçmiş ders günleri dropdown'ını doldur (sadece ders günleri — default pazartesi)
async function yoklamaTarihlerYukle() {
  const sel = document.getElementById('yoklama-gecmis-tarihler');
  if (!sel) return;
  const testGoster = document.getElementById('yoklama-test-tarihleri-goster')?.checked || false;

  try {
    const r = await safeFetch('/api/yoklama/tarihler');
    const d = await r.json();
    const tarihler = d.tarihler || [];

    // Default: sadece ders günü; checkbox açıksa test günleri de
    const listele = testGoster ? tarihler : tarihler.filter(t => t.ders_gunu);

    sel.innerHTML = '<option value="">📅 Geçmiş ders günleri…</option>';
    listele.forEach(t => {
      const opt = document.createElement('option');
      opt.value = t.tarih;
      const isaret = t.ders_gunu ? '✓' : '•';
      const etiket = t.ders_gunu ? '' : ' (test)';
      opt.textContent = `${isaret} ${t.tarih} ${t.gun} — ${t.sayi} kayıt${etiket}`;
      sel.appendChild(opt);
    });

    if (listele.length === 0) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = testGoster ? '(hiç kayıt yok)' : '(pazartesi kaydı yok — "test günleri göster" ile kontrol et)';
      opt.disabled = true;
      sel.appendChild(opt);
    }
  } catch (e) {
    console.error('Tarihler yüklenemedi:', e);
  }
}

// Dropdown'dan geçmiş bir tarih seçildi → date input'a yaz + refresh
function yoklamaGecmisTarihSec() {
  const sel = document.getElementById('yoklama-gecmis-tarihler');
  const inp = document.getElementById('yoklama-tarih');
  if (!sel || !inp || !sel.value) return;
  inp.value = sel.value;
  yoklamaTarihDegisti();
  // Seçimi sıfırla ki aynı tarih tekrar seçilebilsin
  sel.value = '';
}

// Sayfa yüklendiğinde + yoklama sekmesine girilince dropdown'u doldur
document.addEventListener('DOMContentLoaded', () => {
  yoklamaTarihlerYukle();
});

async function yoklamaCek() {
  try {
    const paket = document.getElementById('yoklama-paket-filtre')?.value || '';
    const tarih = document.getElementById('yoklama-tarih')?.value || '';
    let url = '/api/yoklama?';
    if (paket) url += 'paket=' + encodeURIComponent(paket) + '&';
    if (tarih) url += 'tarih=' + tarih + '&';
    const yanit = await safeFetch(url);
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
        <div class="isim">${esc(o.ad_soyad)}</div>
        <div class="numara">${esc(o.numara)}</div>
        <div class="sinif-etiket" style="font-size:0.75rem;color:#90cdf4;margin-left:auto;">${esc(o.sinif || '')}</div>
        <div style="font-size:0.75rem;color:#a0aec0;margin-left:0.5rem;" title="Bağlantı IP Adresi">🌐 ${esc(o.ip || '')}</div>
        ${o.paket && o.paket !== '—' ? `<div class="paket-etiket" style="font-size:0.7rem;color:#68d391;background:#1a3a2a;border:1px solid #2d6a4a;border-radius:4px;padding:0.1rem 0.4rem;margin-left:0.4rem;">📦 ${esc(o.paket.split(' ')[0] + ' ' + o.paket.split(' ')[1])}</div>` : ''}
        ${o.kaynak === 'manuel' ? `<span title="Manuel giriş" style="font-size:0.7rem;color:#f6c90e;background:#2d2a00;border:1px solid #6b5900;border-radius:4px;padding:0.1rem 0.4rem;margin-left:0.4rem;">👨‍🏫 M</span>` : ''}
        <div class="saat">${esc(o.saat)}</div>
        <button
          onclick="tekSil(${escJsAttr(o.numara)}, ${escJsAttr(o.ad_soyad)})"
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
    let toplamGelen = 0;
    for (const sinif of siniflar.siniflar) {
      const detayYanit = await safeFetch(`/api/sinif_ogrencileri/${sinif.id}`);
      const veri = await detayYanit.json();

      const geldi = veri.ogrenciler.filter(o => o.geldi);
      const tamKatilim = geldi.length === sinif.kayitli && sinif.kayitli > 0;
      toplamGelen += sinif.bugun;

      html += `
        <div class="sinif-kart" data-sinif-id="${sinif.id}">
          <div class="sinif-kart-baslik" onclick="sinifKartToggle(${sinif.id})">
            <h4>
              ${esc(sinif.ad)}
              <span class="sinif-badge ${tamKatilim ? 'tam' : ''}">${sinif.bugun}/${sinif.kayitli}</span>
            </h4>
            <span class="kart-ok">▼</span>
          </div>
          <div class="sinif-kart-icerik">
            <div class="sinif-ozet">Bugün ${sinif.bugun} katıldı · ${sinif.kayitli - sinif.bugun} eksik</div>
            ${veri.ogrenciler.map(o => `
              <div class="ogrenci-mini ${o.geldi ? '' : 'devamsiz'}" id="ogrenci-${esc(o.numara)}">
                <div class="${o.geldi ? 'dot-geldi' : 'dot-gelmedi'}"></div>
                <span>${esc(o.ad_soyad)}</span>
                ${o.geldi && o.paket && o.paket !== '—' ? `<span style="font-size:0.65rem;color:#68d391;background:#1a3a2a;border-radius:3px;padding:0 0.3rem;margin-left:0.3rem;">${esc(o.paket.split(' ')[0] + ' ' + o.paket.split(' ')[1])}</span>` : ''}
                ${o.geldi && o.paket === 'manuel' ? `<span style="font-size:0.65rem;color:#f6c90e;margin-left:0.2rem;" title="Manuel giriş">👨‍🏫</span>` : ''}
                <span style="margin-left:auto;color:#718096;font-size:0.75rem;">${esc(o.numara)}</span>
                ${!o.geldi ? `<button
                  onclick="event.stopPropagation();manuelGiris(${sinif.id}, ${escJsAttr(o.numara)}, ${escJsAttr(o.ad_soyad)})"
                  style="margin-left:0.5rem;padding:0.15rem 0.5rem;font-size:0.7rem;background:#2d3a1a;border:1px solid #4a6a2a;border-radius:4px;color:#a0d070;cursor:pointer;"
                  title="Manuel giriş ekle">
                  + Giriş
                </button>` : ''}
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }
    grid.innerHTML = html;
    sinifKartDurumYukle();

    var bilgi = document.getElementById('sinif-durum-bilgi');
    if (bilgi) bilgi.textContent = siniflar.siniflar.length + ' sınıf · toplam ' + toplamGelen + '/' + toplamKayitli + ' öğrenci geldi';
  } catch (e) { console.error(e); }
}

// ─── Sınıf kart toggle (collapsible + localStorage) ───
function sinifKartToggle(sinifId) {
  var el = document.querySelector('.sinif-kart[data-sinif-id="' + sinifId + '"]');
  if (!el) return;
  el.classList.toggle('kapali');
  sinifKartDurumKaydet();
}
function sinifKartlarHepsiAc() {
  document.querySelectorAll('.sinif-kart').forEach(function(k) { k.classList.remove('kapali'); });
  sinifKartDurumKaydet();
}
function sinifKartlarHepsiKapat() {
  document.querySelectorAll('.sinif-kart').forEach(function(k) { k.classList.add('kapali'); });
  sinifKartDurumKaydet();
}
function sinifKartDurumKaydet() {
  var durumlar = {};
  document.querySelectorAll('.sinif-kart').forEach(function(k) {
    var id = k.dataset.sinifId;
    if (id) durumlar[id] = !k.classList.contains('kapali');
  });
  try { localStorage.setItem('sinif-kart-durum', JSON.stringify(durumlar)); } catch (e) {}
}
function sinifKartDurumYukle() {
  try {
    var durumlar = JSON.parse(localStorage.getItem('sinif-kart-durum') || '{}');
    document.querySelectorAll('.sinif-kart').forEach(function(k) {
      var id = k.dataset.sinifId;
      if (id && durumlar[id] === false) k.classList.add('kapali');
    });
  } catch (e) {}
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
              <span style="color:#718096;">${esc(k.tarih)} ${esc(k.saat.substring(0, 5))} · ${esc(k.sinif)}</span>
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
            <strong>${esc(k.gercek_ad)}</strong>
            <span style="color:#718096;">(#${esc(k.gercek_numara)})</span>
            &nbsp;—&nbsp;bu IP'den önceden giriş yapmıştı.
          </div>
          <div style="color:#e2e8f0;">
            <span style="color:#fbd38d;">🚫 Deneme:</span>
            <strong>${esc(k.denenen_ad)}</strong>
            <span style="color:#718096;">(#${esc(k.denenen_numara)})</span>
            &nbsp;aynı cihazdan giriş yapmaya çalıştı.
          </div>
          <div style="color:#718096;font-size:0.75rem;margin-top:0.2rem;">IP: ${esc(k.ip)}</div>
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

async function cikisLogCek() {
  const kutu = document.getElementById('cikis-log-kutu');
  if (!kutu) return;
  try {
    const yanit = await safeFetch('/api/ogrenci_cikis_log');
    const veri = await yanit.json();
    if (!veri.kayitlar || veri.kayitlar.length === 0) {
      kutu.innerHTML = '<div style="color:#718096;text-align:center;padding:1rem;">Bugün çıkış yok</div>';
      return;
    }
    let html = '<table style="width:100%;border-collapse:collapse;font-size:0.82rem;">';
    html += '<tr style="color:#a0aec0;border-bottom:1px solid #4a5568;"><th style="padding:6px;">Saat</th><th>Numara</th><th>Ad Soyad</th><th>Paket</th><th>Kaynak</th><th>İşlem</th></tr>';
    veri.kayitlar.forEach(k => {
      const kaynak_renk = k.kaynak === 'force' ? '#fc8181' : '#68d391';
      const kaynak_etiket = k.kaynak === 'force' ? '👨‍🏫 Force' : '🧑 Öğrenci';
      html += `<tr style="border-bottom:1px solid #2d3748;">
        <td style="padding:5px 8px;color:#a0aec0;">${esc(k.saat)}</td>
        <td style="padding:5px 8px;">${esc(k.numara)}</td>
        <td style="padding:5px 8px;">${esc(k.ad_soyad)}</td>
        <td style="padding:5px 8px;color:#90cdf4;">${esc(k.paket)}</td>
        <td style="padding:5px 8px;color:${kaynak_renk};">${kaynak_etiket}</td>
        <td style="padding:5px 8px;"></td>
      </tr>`;
    });
    html += '</table>';
    kutu.innerHTML = html;
  } catch(e) {
    kutu.innerHTML = '<div style="color:#e53e3e;padding:1rem;">Hata: ' + e.message + '</div>';
  }
}

async function ogrenciForceCikis(numara, adSoyad) {
  if (!confirm(`${adSoyad || numara} adlı öğrenciyi zorla çıkartmak istiyor musunuz?`)) return;
  try {
    const res = await safeFetch('/api/ogrenci_force_cikis', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ numara })
    });
    const veri = await res.json();
    if (veri.durum === 'ok') {
      alert(`✅ ${numara} çıkartıldı (5 saniye içinde etkili olacak).`);
      cikisLogCek();
    } else {
      alert('Hata: ' + (veri.mesaj || 'Bilinmeyen hata'));
    }
  } catch(e) {
    alert('Bağlantı hatası.');
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
            <span style="color:${renk};font-weight:600;">${ikon} ${esc(log.durum)}</span>
            <span style="color:#718096;">${esc(log.tarih)} ${esc(log.saat.substring(0, 5))}</span>
          </div>
          <div style="color:#e2e8f0;">
            <span style="color:#90cdf4;">${esc(log.session_ad)}</span>
            (${esc(log.session_numara)})
          </div>
          ${log.durum === 'GUVENLIK_IHLALI' ? `
            <div style="color:#fc8181;">
              Girmeye çalışan: <strong>${esc(log.girilen_numara)}</strong>
            </div>
          ` : ''}
          <div style="color:#718096;font-size:0.75rem;">IP: ${esc(log.ip)}</div>
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
            <td style="padding:0.5rem;color:#fc8181;">${esc(log.tarih)} ${esc(log.saat.substring(0, 5))}</td>
            <td style="padding:0.5rem;">${esc(log.numara)}</td>
            <td style="padding:0.5rem;">${esc(log.ad_soyad)}</td>
            <td style="padding:0.5rem;color:#a0aec0;font-size:0.85rem;">${esc(log.ip)}</td>
        </tr>`;
    });

    html += '</tbody></table>';
    div.innerHTML = html;
  } catch (e) {
    console.error('SEB çıkış log çekme hatası:', e);
  }
}

async function cikisTalepleriCek() {
  try {
    const yanit = await safeFetch('/api/seb_cikis_talepler');
    const veri = await yanit.json();

    const div = document.getElementById('seb-cikis-talepleri-kutu');
    if (!div) return;

    if (!veri.talepler || veri.talepler.length === 0) {
      div.innerHTML = '<div style="color:#718096;text-align:center;padding:1rem;">Bekleyen çıkış talebi yok.</div>';
      return;
    }

    let html = '<table class="veri-tablosu" style="width:100%; border-collapse:collapse;">';
    html += '<thead><tr style="border-bottom:1px solid #4a5568;"><th style="padding:0.5rem;text-align:left;">Zaman</th><th style="padding:0.5rem;text-align:left;">Öğrenci No</th><th style="padding:0.5rem;text-align:left;">Ad Soyad</th><th style="padding:0.5rem;text-align:right;">İşlem</th></tr></thead>';
    html += '<tbody>';

    veri.talepler.forEach(t => {
      html += `<tr style="border-bottom:1px solid #2d3748; background:rgba(237,137,54,0.1);">
            <td style="padding:0.5rem;color:#fbd38d;">${esc(t.tarih)} ${esc(t.saat.substring(0, 5))}</td>
            <td style="padding:0.5rem;">${esc(t.numara)}</td>
            <td style="padding:0.5rem;">${esc(t.ad_soyad)}</td>
            <td style="padding:0.5rem;text-align:right;">
              <button onclick="cikisOnayla(${t.id}, 'onaylandi')" style="background:#38a169; border:none; padding:4px 8px; border-radius:4px; color:white; cursor:pointer; margin-right:4px;">İzin Ver</button>
              <button onclick="cikisOnayla(${t.id}, 'reddedildi')" style="background:#c53030; border:none; padding:4px 8px; border-radius:4px; color:white; cursor:pointer;">Reddet</button>
            </td>
        </tr>`;
    });

    html += '</tbody></table>';
    div.innerHTML = html;
  } catch (e) {
    console.error('SEB çıkış talepleri çekme hatası:', e);
  }
}

async function cikisOnayla(id, durum) {
  try {
    const yanit = await safeFetch('/api/seb_cikis_onayla', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, durum })
    });
    const veri = await yanit.json();
    if (veri.durum === 'ok') {
      cikisTalepleriCek();
      sebCikisCek(); // Update the lower table if it's approved
    } else alert('Hata: ' + veri.mesaj);
  } catch (e) {
    alert('Bağlantı hatası: ' + e.message);
  }
}

async function cikisTopluOnayla() {
  if (!confirm("Bekleyen BÜTÜN taleplere izin vermek istiyor musunuz?")) return;
  try {
    const yanit = await safeFetch('/api/seb_cikis_toplu_onayla', { method: 'POST' });
    const veri = await yanit.json();
    if (veri.durum === 'ok') {
      cikisTalepleriCek();
      sebCikisCek();
    } else alert('Hata: ' + veri.mesaj);
  } catch (e) {
    alert('Bağlantı hatası: ' + e.message);
  }
}

// ── Yardım Talepleri ──────────────────────────────────────────────

async function yardimTalepleriCek() {
  try {
    const yanit = await safeFetch('/api/yardim_talepler');
    const veri = await yanit.json();

    const div = document.getElementById('yardim-talepleri-kutu');
    const rozet = document.getElementById('yardim-rozet');
    if (!div) return;

    if (!veri.talepler || veri.talepler.length === 0) {
      if (rozet) {
        rozet.style.display = 'none';
        rozet.innerText = '0';
      }
      div.innerHTML = '<div style="color:#718096;text-align:center;padding:1rem;">Bekleyen yardım talebi yok.</div>';
      return;
    }

    let bekleyenSayisi = 0;

    const kategoriMap = { komut: '\u{1F527} Komut', dosya: '\u{1F4C1} Dosya', terminal: '\u{1F4BB} Terminal', soru: '\u{2753} Soru', diger: '\u{1F4CB} Di\u011Fer' };

    const tablo = document.createElement('table');
    tablo.className = 'veri-tablosu';
    tablo.style.cssText = 'width:100%; border-collapse:collapse;';

    const thead = document.createElement('thead');
    const baslikSatir = document.createElement('tr');
    baslikSatir.style.borderBottom = '1px solid #4a5568';
    ['Zaman', '\u00D6\u011Frenci No', 'Ad Soyad', 'Kategori', 'Durum', '\u0130\u015Flem'].forEach((txt, i) => {
      const th = document.createElement('th');
      th.style.padding = '0.5rem';
      th.style.textAlign = (i === 5) ? 'right' : 'left';
      th.textContent = txt;
      baslikSatir.appendChild(th);
    });
    thead.appendChild(baslikSatir);
    tablo.appendChild(thead);

    const tbody = document.createElement('tbody');

    veri.talepler.forEach(t => {
      if (t.durum === 'bekliyor') bekleyenSayisi++;

      const tr = document.createElement('tr');
      tr.style.borderBottom = '1px solid #2d3748';
      tr.style.background = t.durum === 'bekliyor' ? 'rgba(43,108,176,0.1)' : 'rgba(72,187,120,0.1)';

      // Zaman
      const tdZaman = document.createElement('td');
      tdZaman.style.cssText = 'padding:0.5rem;color:#a0aec0;';
      tdZaman.textContent = t.tarih + ' ' + t.saat.substring(0, 5);
      tr.appendChild(tdZaman);

      // Numara
      const tdNumara = document.createElement('td');
      tdNumara.style.padding = '0.5rem';
      tdNumara.textContent = t.numara;
      tr.appendChild(tdNumara);

      // Ad Soyad
      const tdAd = document.createElement('td');
      tdAd.style.padding = '0.5rem';
      tdAd.textContent = t.ad_soyad;
      tr.appendChild(tdAd);

      // Kategori
      const tdKat = document.createElement('td');
      tdKat.style.padding = '0.5rem';
      tdKat.textContent = kategoriMap[t.kategori] || (t.kategori || '—');
      tr.appendChild(tdKat);

      // Durum
      const tdDurum = document.createElement('td');
      tdDurum.style.padding = '0.5rem';
      const durumSpan = document.createElement('span');
      durumSpan.style.fontWeight = 'bold';
      if (t.durum === 'bekliyor') {
        durumSpan.style.color = '#63b3ed';
        durumSpan.textContent = 'Bekliyor';
      } else {
        durumSpan.style.color = '#48bb78';
        durumSpan.textContent = 'Kabul Edildi';
      }
      tdDurum.appendChild(durumSpan);
      tr.appendChild(tdDurum);

      // İşlem
      const tdIslem = document.createElement('td');
      tdIslem.style.cssText = 'padding:0.5rem;text-align:right;';
      if (t.durum === 'bekliyor') {
        const btnKabul = document.createElement('button');
        btnKabul.textContent = 'Kabul Et (Ba\u011Flan)';
        btnKabul.style.cssText = 'background:#2b6cb0; border:none; padding:4px 8px; border-radius:4px; color:white; cursor:pointer; margin-right:4px;';
        btnKabul.addEventListener('click', () => yardimKabul(t.id, 'kabul_edildi'));
        tdIslem.appendChild(btnKabul);
      }
      const btnTamam = document.createElement('button');
      btnTamam.textContent = 'Tamamla';
      btnTamam.style.cssText = 'background:#48bb78; border:none; padding:4px 8px; border-radius:4px; color:white; cursor:pointer;';
      btnTamam.addEventListener('click', () => yardimKabul(t.id, 'tamamlandi'));
      tdIslem.appendChild(btnTamam);
      tr.appendChild(tdIslem);

      tbody.appendChild(tr);
    });

    tablo.appendChild(tbody);
    div.textContent = '';
    div.appendChild(tablo);

    if (rozet) {
      if (bekleyenSayisi > 0) {
        rozet.style.display = 'inline-block';
        rozet.innerText = bekleyenSayisi;
      } else {
        rozet.style.display = 'none';
        rozet.innerText = '0';
      }
    }
  } catch (e) {
    console.error('Yardım talepleri çekme hatası:', e);
  }
}

async function yardimKabul(id, durum) {
  try {
    const yanit = await safeFetch('/api/yardim_kabul', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, durum })
    });
    const veri = await yanit.json();
    if (veri.durum === 'ok') {
      yardimTalepleriCek();
      if (durum === 'kabul_edildi') {
        // İleride burada terminal devralma (bağlanma) penceresi fırlatılacak
        alert("Bağlantı kabul edildi. Terminal devralma özelliği bir sonraki aşamada eklenecektir.");
      }
    } else alert('Hata: ' + veri.mesaj);
  } catch (e) {
    alert('Bağlantı hatası: ' + e.message);
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

async function sifreDegistir() {
  const mevcut = document.getElementById('sifre-mevcut')?.value || '';
  const yeni = document.getElementById('sifre-yeni')?.value || '';
  const sonuc = document.getElementById('sifre-sonuc');

  if (!mevcut || !yeni) { alert('Mevcut ve yeni şifre gerekli'); return; }
  if (yeni.length < 4) { alert('Yeni şifre en az 4 karakter olmalı'); return; }

  try {
    const res = await safeFetch('/teacher/sifre_degistir', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mevcut, yeni })
    });
    const data = await res.json();
    if (data.durum === 'ok') {
      if (sonuc) { sonuc.style.color = '#48bb78'; sonuc.textContent = 'Şifre değiştirildi'; }
      document.getElementById('sifre-mevcut').value = '';
      document.getElementById('sifre-yeni').value = '';
    } else {
      if (sonuc) { sonuc.style.color = '#e53e3e'; sonuc.textContent = data.mesaj; }
    }
  } catch (e) {
    if (sonuc) { sonuc.style.color = '#e53e3e'; sonuc.textContent = 'Bağlantı hatası'; }
  }
}

// Chroot pre-warm — sınıfın tüm öğrenci chroot'larını önceden toplu yarat
async function chrootPreWarmSinifDoldur() {
  const sel = document.getElementById('chroot-prewarm-sinif');
  if (!sel || sel.options.length > 1) return;
  try {
    const r = await safeFetch('/api/siniflar');
    const d = await r.json();
    (d.siniflar || []).forEach(s => {
      const opt = document.createElement('option');
      opt.value = s.id;
      opt.textContent = `${s.ad} (${s.kayitli} öğr)`;
      sel.appendChild(opt);
    });
  } catch (e) {
    console.error('Sınıflar alınamadı:', e);
  }
}

async function chrootPreWarm() {
  const sel = document.getElementById('chroot-prewarm-sinif');
  const sonuc = document.getElementById('chroot-prewarm-sonuc');
  if (!sel || !sel.value) {
    if (sonuc) { sonuc.style.color = '#fc8181'; sonuc.textContent = 'Önce sınıf seç'; }
    return;
  }
  if (sonuc) { sonuc.style.color = '#a0aec0'; sonuc.textContent = 'Yaratılıyor...'; }
  try {
    const r = await safeFetch(`/api/chroot/pre_warm/${sel.value}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    const d = await r.json();
    if (d.durum === 'ok') {
      if (sonuc) {
        sonuc.style.color = '#48bb78';
        sonuc.textContent = `✅ ${d.mesaj} (var: ${d.zaten_var}, yaratılacak: ${d.yaratilacak})`;
      }
    } else {
      if (sonuc) { sonuc.style.color = '#fc8181'; sonuc.textContent = `❌ ${d.mesaj}`; }
    }
  } catch (e) {
    if (sonuc) { sonuc.style.color = '#fc8181'; sonuc.textContent = 'Bağlantı hatası'; }
  }
}

// Pre-warm dropdown'ını sayfa yüklendiğinde doldur
document.addEventListener('DOMContentLoaded', () => chrootPreWarmSinifDoldur());

async function chrootListele() {
  const sonuc = document.getElementById('chroot-tarama-sonuc');
  const liste = document.getElementById('chroot-fazla-liste');
  const btn = document.getElementById('chroot-temizle-btn');
  if (sonuc) sonuc.textContent = '⏳ Taranıyor...';
  if (liste) liste.innerHTML = '';
  if (btn) btn.style.display = 'none';
  try {
    const res = await safeFetch('/api/chroot/listele');
    const veri = await res.json();
    if (veri.hata) {
      if (sonuc) { sonuc.style.color = '#e53e3e'; sonuc.textContent = 'Hata: ' + veri.hata; }
      return;
    }
    if (veri.fazla_sayisi === 0) {
      if (sonuc) { sonuc.style.color = '#48bb78'; sonuc.textContent = `✅ Temiz — ${veri.toplam} VM, hepsi aktif.`; }
      return;
    }
    if (sonuc) {
      sonuc.style.color = '#f6ad55';
      sonuc.textContent = `⚠️ ${veri.fazla_sayisi} eski VM bulundu (toplam: ${veri.toplam})`;
    }
    if (btn) btn.style.display = 'inline-block';
    // Seçili silme butonu
    let btnSecili = document.getElementById('chroot-secili-sil-btn');
    if (!btnSecili) {
      btnSecili = document.createElement('button');
      btnSecili.id = 'chroot-secili-sil-btn';
      btnSecili.className = 'btn-kucuk';
      btnSecili.style.cssText = 'background:#c53030; margin-left:6px; display:none;';
      btnSecili.textContent = '🗑️ Seçilenleri Sil';
      btnSecili.onclick = chrootSeciliSil;
      btn.parentNode.insertBefore(btnSecili, btn.nextSibling);
    }
    if (liste) {
      liste.innerHTML = '<label style="display:block;margin-bottom:4px;cursor:pointer;font-size:0.78rem;color:#a0aec0;">' +
        '<input type="checkbox" id="chroot-hepsi-sec" style="margin-right:4px;" onchange="chrootHepsiSec(this.checked)"> Tümünü seç</label>' +
        veri.fazla.map(u =>
        `<label style="display:inline-flex;align-items:center;background:#742a2a;color:#feb2b2;border-radius:4px;padding:3px 8px;margin:2px;font-size:0.78rem;font-family:monospace;cursor:pointer;">` +
        `<input type="checkbox" class="chroot-sec" value="${u}" style="margin-right:4px;" onchange="chrootSecimGuncelle()"> ${u}</label>`
      ).join('');
    }
  } catch (e) {
    if (sonuc) { sonuc.style.color = '#e53e3e'; sonuc.textContent = 'Bağlantı hatası'; }
  }
}

function chrootHepsiSec(checked) {
  document.querySelectorAll('.chroot-sec').forEach(cb => { cb.checked = checked; });
  chrootSecimGuncelle();
}

function chrootSecimGuncelle() {
  const secili = document.querySelectorAll('.chroot-sec:checked').length;
  const btn = document.getElementById('chroot-secili-sil-btn');
  if (btn) {
    btn.style.display = secili > 0 ? 'inline-block' : 'none';
    btn.textContent = `🗑️ Seçilenleri Sil (${secili})`;
  }
}

async function chrootSeciliSil() {
  const checkboxlar = document.querySelectorAll('.chroot-sec:checked');
  const secili = Array.from(checkboxlar).map(cb => cb.value);
  if (secili.length === 0) return;
  if (!confirm(`${secili.length} VM silinecek:\n${secili.join(', ')}\n\nEmin misiniz?`)) return;

  const sonuc = document.getElementById('chroot-tarama-sonuc');
  const btn = document.getElementById('chroot-secili-sil-btn');
  if (btn) { btn.disabled = true; btn.textContent = '⏳ Siliniyor...'; }
  try {
    const res = await safeFetch('/api/chroot/sil', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ secili })
    });
    const veri = await res.json();
    if (veri.durum === 'ok') {
      if (sonuc) { sonuc.style.color = '#48bb78'; sonuc.textContent = `✅ ${veri.silinen} VM siliniyor (arka planda)`; }
      // Silinen checkbox'ları kaldır
      checkboxlar.forEach(cb => cb.closest('label').remove());
      chrootSecimGuncelle();
    } else {
      if (sonuc) { sonuc.style.color = '#e53e3e'; sonuc.textContent = 'Hata: ' + (veri.hata || 'Bilinmeyen'); }
    }
  } catch (e) {
    if (sonuc) { sonuc.style.color = '#e53e3e'; sonuc.textContent = 'Bağlantı hatası'; }
  }
  if (btn) { btn.disabled = false; chrootSecimGuncelle(); }
}

async function chrootTemizle() {
  const btn = document.getElementById('chroot-temizle-btn');
  const sonuc = document.getElementById('chroot-tarama-sonuc');
  if (!confirm('Bu eski VM\'ler kalıcı olarak silinecek. Emin misiniz?')) return;
  if (btn) { btn.disabled = true; btn.textContent = '⏳ Siliniyor...'; }
  try {
    const res = await safeFetch('/api/chroot/temizle', { method: 'POST' });
    const veri = await res.json();
    if (veri.hata) {
      if (sonuc) { sonuc.style.color = '#e53e3e'; sonuc.textContent = 'Hata: ' + veri.hata; }
    } else {
      if (sonuc) { sonuc.style.color = '#48bb78'; sonuc.textContent = `✅ ${veri.silinen} VM siliniyor (arka planda)`; }
      document.getElementById('chroot-fazla-liste').innerHTML = '';
    }
    if (btn) { btn.disabled = false; btn.textContent = '🗑️ Hepsini Sil'; btn.style.display = 'none'; }
  } catch (e) {
    if (btn) { btn.disabled = false; btn.textContent = '🗑️ Hepsini Sil'; }
    if (sonuc) { sonuc.style.color = '#e53e3e'; sonuc.textContent = 'Bağlantı hatası'; }
  }
}

async function paketSonu() {
  const onay = confirm(
    '📦 PAKET SONU\n\n' +
    'Bu işlem:\n' +
    '  1. Tüm öğrencilerin oturumunu kapatır\n' +
    '  2. Mevcut paketin öğrencilerinin VM\'lerini (chroot) siler\n\n' +
    'Öğrencilerin çalışmaları kaybolacak.\n' +
    'Devam etmek istiyor musunuz?'
  );
  if (!onay) return;

  try {
    const res = await safeFetch('/api/paket_sonu', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const data = await res.json();
    if (data.durum === 'ok') {
      alert(
        '✅ Paket Sonu işlemi başlatıldı.\n\n' +
        data.mesaj + '\n\n' +
        'Paket: ' + data.paket
      );
      yoklamaCek();
    } else {
      alert('Hata: ' + (data.mesaj || 'Bilinmeyen hata'));
    }
  } catch (e) {
    alert('Bağlantı hatası: ' + e.message);
  }
}

let _girisAcik = false;

async function girisToggle() {
  const yeniDurum = !_girisAcik;
  try {
    const res = await safeFetch('/api/giris_toggle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ acik: yeniDurum })
    });
    const veri = await res.json();
    if (veri.durum === 'ok') {
      _girisAcik = veri.giris_acik;
      girisButonGuncelle();
    }
  } catch (e) {
    alert('Bağlantı hatası');
  }
}

function girisButonGuncelle() {
  const btn = document.getElementById('btn-giris-toggle');
  if (!btn) return;
  if (_girisAcik) {
    btn.textContent = '🔓 Giriş Açık';
    btn.style.background = '#48bb78';
  } else {
    btn.textContent = '🔒 Giriş Aç';
    btn.style.background = '#2b6cb0';
  }
}

// Sayfa yüklendiğinde giriş durumunu kontrol et
fetch('/api/durum').then(r => r.json()).then(v => {
  _girisAcik = v.giris_acik || false;
  girisButonGuncelle();
}).catch(() => {});

async function topluCikis() {
  if (!confirm('Tüm öğrencilerin oturumunu kapatmak istediğinize emin misiniz?\n\nBu işlem tüm öğrencileri giriş sayfasına yönlendirecektir.')) return;
  try {
    const res = await safeFetch('/api/toplu_cikis', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
    const data = await res.json();
    if (data.durum === 'ok') {
      // Girişi de kapat
      _girisAcik = false;
      girisButonGuncelle();
      safeFetch('/api/giris_toggle', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ acik: false }) });
      alert('Tüm öğrenci oturumları kapatılıyor.');
      yoklamaCek();
    }
  } catch (e) {
    alert('Hata: ' + e.message);
  }
}

// ── Devam Raporu ─────────────────────────────────────────────────

let _devamRaporuVeri = null;

async function devamRaporuCek() {
  try {
    // Sinif dropdown'ini doldur (ilk sefer)
    var sinifSelect = document.getElementById('rapor-sinif');
    if (sinifSelect && sinifSelect.options.length <= 1) {
      var sRes = await safeFetch('/api/siniflar');
      var sVeri = await sRes.json();
      (sVeri.siniflar || []).forEach(function(s) {
        var opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = s.ad;
        sinifSelect.appendChild(opt);
      });
    }

    var sinifId = document.getElementById('rapor-sinif') ? document.getElementById('rapor-sinif').value : '';
    var baslangic = document.getElementById('rapor-baslangic') ? document.getElementById('rapor-baslangic').value : '';
    var bitis = document.getElementById('rapor-bitis') ? document.getElementById('rapor-bitis').value : '';

    var url = '/api/yoklama/rapor?';
    if (sinifId) url += 'sinif_id=' + encodeURIComponent(sinifId) + '&';
    if (baslangic) url += 'baslangic=' + encodeURIComponent(baslangic) + '&';
    if (bitis) url += 'bitis=' + encodeURIComponent(bitis) + '&';

    var yanit = await safeFetch(url);
    var veri = await yanit.json();
    _devamRaporuVeri = veri;

    var div = document.getElementById('devam-raporu-icerik');
    if (!div) return;

    if (!veri.rapor || veri.rapor.length === 0) {
      div.textContent = '';
      var bosMsg = document.createElement('div');
      bosMsg.style.cssText = 'color:#718096; text-align:center; padding:2rem;';
      bosMsg.textContent = 'Kayit bulunamadi.';
      div.appendChild(bosMsg);
      return;
    }

    // Tablo olustur
    var tablo = document.createElement('table');
    tablo.style.cssText = 'width:100%; border-collapse:collapse; font-size:0.8rem;';

    // Header
    var thead = document.createElement('tr');
    thead.style.borderBottom = '2px solid #4a5568';

    var basliklar = ['Ogrenci', '%'];
    veri.tarihler.forEach(function(t) {
      basliklar.push(t.substring(5));
    });

    basliklar.forEach(function(h) {
      var th = document.createElement('th');
      th.style.cssText = 'padding:4px 6px; text-align:center; color:#a0aec0; white-space:nowrap;';
      th.textContent = h;
      thead.appendChild(th);
    });
    tablo.appendChild(thead);

    // Rows
    veri.rapor.forEach(function(o) {
      var tr = document.createElement('tr');
      tr.style.borderBottom = '1px solid #2d3748';
      if (o.uyari) tr.style.background = 'rgba(229,62,62,0.15)';

      var tdAd = document.createElement('td');
      tdAd.style.cssText = 'padding:4px 6px; white-space:nowrap;';
      tdAd.textContent = o.ad_soyad;
      if (o.uyari) tdAd.style.color = '#fc8181';
      tr.appendChild(tdAd);

      var tdPct = document.createElement('td');
      tdPct.style.cssText = 'padding:4px 6px; text-align:center; font-weight:bold;';
      tdPct.textContent = '%' + o.yuzde;
      if (o.yuzde >= 70) {
        tdPct.style.color = '#48bb78';
      } else if (o.yuzde >= 50) {
        tdPct.style.color = '#ed8936';
      } else {
        tdPct.style.color = '#e53e3e';
      }
      tr.appendChild(tdPct);

      veri.tarihler.forEach(function(t) {
        var td = document.createElement('td');
        td.style.cssText = 'padding:4px 6px; text-align:center;';
        if (o.gunler[t] === 'geldi') {
          td.textContent = '\u2705';
        } else {
          td.textContent = '\u274C';
        }
        tr.appendChild(td);
      });

      tablo.appendChild(tr);
    });

    div.textContent = '';
    div.appendChild(tablo);
  } catch (e) {
    console.error('Devam raporu hatasi:', e);
  }
}

// ─────────────────────────────────────────────────────────
// Haftalık Devamlılık (öğrenci × hafta matrisi + override)
// ─────────────────────────────────────────────────────────

var _devamlilikVeri = null;

async function devamlilikCek() {
  try {
    var sinifSelect = document.getElementById('devamlilik-sinif');
    if (!sinifSelect) return;

    // Sınıf dropdown'ını doldur (ilk açılışta)
    if (sinifSelect.options.length <= 1) {
      // Özel "Tümü" seçeneği en başta
      var optTumu = document.createElement('option');
      optTumu.value = 'tumu';
      optTumu.textContent = '📋 Tümü (test hariç)';
      sinifSelect.appendChild(optTumu);

      var sRes = await safeFetch('/api/siniflar');
      var sVeri = await sRes.json();
      (sVeri.siniflar || []).forEach(function(s) {
        var opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = s.ad;
        sinifSelect.appendChild(opt);
      });
    }

    var sinifId = sinifSelect.value;
    var div = document.getElementById('devamlilik-icerik');
    var bilgi = document.getElementById('devamlilik-bilgi');

    if (!sinifId) {
      div.innerHTML = '<div style="color:#718096; text-align:center; padding:2rem;">Bir sınıf seçin.</div>';
      if (bilgi) bilgi.textContent = '';
      return;
    }

    var url = (sinifId === 'tumu')
      ? '/api/devamlilik/tumu'
      : '/api/devamlilik/' + encodeURIComponent(sinifId);
    var r = await safeFetch(url);
    var veri = await r.json();
    _devamlilikVeri = veri;

    if (veri.durum === 'hata') {
      div.innerHTML = '<div style="color:#fc8181; padding:1rem;">' + (veri.mesaj || 'Hata') + '</div>';
      return;
    }

    if (!veri.ogrenciler || veri.ogrenciler.length === 0) {
      div.innerHTML = '<div style="color:#718096; text-align:center; padding:2rem;">' + (veri.mesaj || 'Kayıt yok.') + '</div>';
      if (bilgi) bilgi.textContent = '';
      return;
    }

    if (bilgi) {
      bilgi.textContent = veri.sinif + ' · dönem başı: ' + veri.donem_baslangic + ' · ' + veri.max_hafta + ' hafta';
    }

    devamlilikRender(veri);
  } catch (e) {
    console.error('Devamlılık hatası:', e);
  }
}

function devamlilikRender(veri) {
  var div = document.getElementById('devamlilik-icerik');
  if (!div) return;

  var tumu = !!veri.tumu_modu;

  var tablo = document.createElement('table');
  tablo.style.cssText = 'width:100%;border-collapse:collapse;font-size:0.78rem;';

  // Header
  var thead = document.createElement('tr');
  thead.style.borderBottom = '2px solid #4a5568';
  var basliklar = ['Öğrenci'];
  if (tumu) basliklar.push('Sınıf');
  basliklar.push('Katıldı', 'Devamsız', '%');
  for (var i = 1; i <= veri.max_hafta; i++) basliklar.push('H' + i);
  basliklar.forEach(function(h) {
    var th = document.createElement('th');
    th.style.cssText = 'padding:6px 6px;text-align:center;color:#a0aec0;white-space:nowrap;';
    th.textContent = h;
    thead.appendChild(th);
  });
  tablo.appendChild(thead);

  // Satırlar
  veri.ogrenciler.forEach(function(o) {
    var tr = document.createElement('tr');
    tr.style.borderBottom = '1px solid #2d3748';

    var tdAd = document.createElement('td');
    tdAd.style.cssText = 'padding:4px 8px;white-space:nowrap;color:#e2e8f0;';
    tdAd.textContent = (o.ad + ' ' + o.soyad).trim() + '  (' + o.numara + ')';
    tr.appendChild(tdAd);

    if (tumu) {
      var tdSinif = document.createElement('td');
      tdSinif.style.cssText = 'padding:4px 8px;white-space:nowrap;color:#90cdf4;font-size:0.72rem;';
      tdSinif.textContent = o.sinif_ad || '';
      tr.appendChild(tdSinif);
    }

    var tdK = document.createElement('td');
    tdK.style.cssText = 'padding:4px 6px;text-align:center;color:#48bb78;font-weight:bold;';
    tdK.textContent = o.katildi;
    tr.appendChild(tdK);

    var tdD = document.createElement('td');
    tdD.style.cssText = 'padding:4px 6px;text-align:center;color:#fc8181;font-weight:bold;';
    tdD.textContent = o.devamsizlik;
    tr.appendChild(tdD);

    var tdP = document.createElement('td');
    tdP.style.cssText = 'padding:4px 6px;text-align:center;font-weight:bold;';
    tdP.textContent = '%' + o.yuzde;
    if (o.yuzde >= 70) tdP.style.color = '#48bb78';
    else if (o.yuzde >= 50) tdP.style.color = '#ed8936';
    else tdP.style.color = '#e53e3e';
    tr.appendChild(tdP);

    o.hucreler.forEach(function(h) {
      var td = document.createElement('td');
      td.style.cssText = 'padding:2px;text-align:center;';
      var hucre = document.createElement('div');
      hucre.style.cssText = 'width:22px;height:22px;margin:auto;border-radius:4px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.7rem;font-weight:bold;user-select:none;';
      hucre.style.background = h.durum === 'katildi' ? '#48bb78' : '#e53e3e';
      if (h.override) {
        hucre.style.border = '2px solid #f6e05e';
      }
      hucre.textContent = h.durum === 'katildi' ? '✓' : '✗';
      hucre.title = 'Hafta ' + h.hafta + (h.override ? ' (öğretmen override)' : '');
      hucre.dataset.numara = o.numara;
      hucre.dataset.hafta = h.hafta;
      hucre.dataset.durum = h.durum;
      hucre.dataset.override = h.override ? '1' : '0';
      hucre.dataset.otomatik = h.otomatik;
      hucre.addEventListener('click', devamlilikHucreClick);
      td.appendChild(hucre);
      tr.appendChild(td);
    });

    tablo.appendChild(tr);
  });

  div.textContent = '';
  div.appendChild(tablo);
}

async function devamlilikHucreClick(ev) {
  var el = ev.currentTarget;
  var numara = el.dataset.numara;
  var hafta = parseInt(el.dataset.hafta, 10);
  var mevcutDurum = el.dataset.durum;
  var isOverride = el.dataset.override === '1';
  var otomatik = el.dataset.otomatik;

  // 3-durumlu toggle:
  //   otomatik == 'katilmadi' (DB'de kayıt yok) →
  //     click 1: override 'katildi' (öğretmen ekler, yeşil + sarı çerçeve)
  //     click 2: sil (geri kırmızı otomatik)
  //   otomatik == 'katildi' (DB'de kayıt var) →
  //     click 1: override 'katilmadi' (öğretmen siler, kırmızı + sarı çerçeve)
  //     click 2: sil (geri yeşil otomatik)
  var yeniDurum;
  if (!isOverride) {
    // Override yok — otomatik durumun TERSİNE çevir
    yeniDurum = (otomatik === 'katildi') ? 'katilmadi' : 'katildi';
  } else {
    // Override var — sil (otomatik'e dön)
    yeniDurum = 'sil';
  }

  try {
    var r = await safeFetch('/api/devamlilik/override', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ numara: numara, hafta: hafta, durum: yeniDurum })
    });
    var res = await r.json();
    if (res.durum !== 'ok') {
      alert('Override hatası: ' + (res.mesaj || ''));
      return;
    }
    // Tabloyu tazele
    devamlilikCek();
  } catch (e) {
    console.error('Override hatası:', e);
    alert('Override başarısız.');
  }
}

function devamlilikCSV() {
  var sinifId = document.getElementById('devamlilik-sinif').value;
  if (!sinifId) {
    alert('Önce bir sınıf seçin.');
    return;
  }
  var url = (sinifId === 'tumu')
    ? '/api/devamlilik/tumu/csv'
    : '/api/devamlilik/' + encodeURIComponent(sinifId) + '/csv';
  window.location.href = url;
}

async function devamRaporuCSV() {
  try {
    var sinifId = document.getElementById('rapor-sinif') ? document.getElementById('rapor-sinif').value : '';
    var baslangic = document.getElementById('rapor-baslangic') ? document.getElementById('rapor-baslangic').value : '';
    var bitis = document.getElementById('rapor-bitis') ? document.getElementById('rapor-bitis').value : '';

    var veri = _devamRaporuVeri;

    // Eger veri yoksa tekrar cek
    if (!veri || !veri.rapor) {
      var url = '/api/yoklama/rapor?';
      if (sinifId) url += 'sinif_id=' + encodeURIComponent(sinifId) + '&';
      if (baslangic) url += 'baslangic=' + encodeURIComponent(baslangic) + '&';
      if (bitis) url += 'bitis=' + encodeURIComponent(bitis) + '&';

      var yanit = await safeFetch(url);
      veri = await yanit.json();
    }

    if (!veri || !veri.rapor || veri.rapor.length === 0) {
      alert('Disa aktarilacak veri yok.');
      return;
    }

    var csv = 'Ogrenci,Numara,Katilim,Devamsizlik,%,' + veri.tarihler.join(',') + '\n';
    veri.rapor.forEach(function(o) {
      var satir = '"' + o.ad_soyad + '",' + o.numara + ',' + o.katilim + ',' + o.devamsizlik + ',' + o.yuzde;
      veri.tarihler.forEach(function(t) {
        satir += ',' + (o.gunler[t] === 'geldi' ? '1' : '0');
      });
      csv += satir + '\n';
    });

    var blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'devam_raporu.csv';
    a.click();
  } catch (e) {
    console.error('CSV export hatasi:', e);
    alert('CSV indirme hatasi.');
  }
}

async function dersGunleriYukle() {
  try {
    const yanit = await safeFetch('/api/config');
    const veri = await yanit.json();
    const gunler = (veri.ders_gunleri || '1').split(',').map(g => g.trim());
    document.querySelectorAll('.ders-gun-cb').forEach(cb => {
      cb.checked = gunler.includes(cb.value);
    });
  } catch (e) {}
}

async function devamsizlikEsikYukle() {
  try {
    var yanit = await safeFetch('/api/yoklama/devamsizlik_esik');
    var veri = await yanit.json();
    var input = document.getElementById('config-devamsizlik-esik');
    if (input && veri.esik !== undefined) {
      input.value = veri.esik;
    }
  } catch (e) {
    console.error('Devamsizlik esik yukleme hatasi:', e);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  yoklamaPaketleriCek();
  yoklamaCek();
  sahteCek();
  sinifDurumCek();        // Kayıtlı öğrenci sayısını güncelle
  guvenlikSoketBaslat();  // Güvenlik uyarılarını dinle
  devamsizlikEsikYukle(); // Devamsizlik esigini yukle
  dersGunleriYukle();    // Ders günlerini yükle

  // Eski URL kontrolü ve otomatik düzeltme (Eskiden /terminal-yayin kullanılıyordu)
  const ttydUrlInput = document.getElementById('config-ttyd-url');
  if (ttydUrlInput && ttydUrlInput.value.includes('terminal-yayin')) {
    console.log('🔄 Eski terminal URL düzeltiliyor...');
    ttydUrlInput.value = '/terminal';
  }

  setInterval(yoklamaCek, YOKLAMA_ARALIK);
  setInterval(sahteCek, 30_000);   // 30 saniyede bir kontrol
  setInterval(yardimTalepleriCek, 5000); // 5 saniyede bir kontrol
  setInterval(sinavIhlalKontrol, 3000); // 3 saniyede bir ihlal kontrol
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
          <td style="padding:0.5rem;">${esc(s.baslik)}</td>
          <td style="padding:0.5rem;">${s.soru_sayisi} Soru</td>
          <td style="padding:0.5rem;">${durumBadge}</td>
          <td style="padding:0.5rem;text-align:right;">
             <button class="btn-kucuk" style="background:#3182ce;" onclick="soruYonetiminiAc(${s.id}, ${escJsAttr(s.baslik)})">📝 Sorular</button>
             <button class="btn-kucuk" style="background:#d69e2e;" onclick="rubrikFormuAc(${s.id}, ${escJsAttr(s.baslik)})">📋 Rubrik</button>
             <button class="btn-kucuk yeşil" onclick="sinavSonuclariniAc(${s.id}, ${escJsAttr(s.baslik)})">📊 Sonuçlar</button>
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

function sinavBaslatDialog() {
  return new Promise(function(resolve) {
    const overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:10001;display:flex;align-items:center;justify-content:center;';
    overlay.innerHTML = `
      <div style="background:#2d3748;border-radius:12px;padding:2rem;max-width:380px;width:90%;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,0.5);">
        <h3 style="color:#e2e8f0;margin:0 0 1rem;">Sınavı Başlat</h3>
        <p style="color:#a0aec0;font-size:0.9rem;margin:0 0 1.5rem;">Öğrenci ekranlarında bu sınav açılacaktır.</p>
        <label style="display:flex;align-items:center;gap:8px;color:#90cdf4;font-size:0.95rem;cursor:pointer;justify-content:center;margin-bottom:1.5rem;">
          <input type="checkbox" id="sinav-terminal-cb" style="width:18px;height:18px;cursor:pointer;">
          Terminal açık kalsın (bölünmüş ekran)
        </label>
        <div style="display:flex;gap:10px;justify-content:center;">
          <button id="sinav-basla-btn" style="background:#48bb78;color:white;border:none;padding:10px 24px;border-radius:8px;font-weight:bold;cursor:pointer;font-size:1rem;">Başlat</button>
          <button id="sinav-iptal-btn" style="background:#4a5568;color:white;border:none;padding:10px 24px;border-radius:8px;font-weight:bold;cursor:pointer;font-size:1rem;">İptal</button>
        </div>
      </div>`;
    document.body.appendChild(overlay);
    overlay.querySelector('#sinav-basla-btn').onclick = function() {
      const terminal = overlay.querySelector('#sinav-terminal-cb').checked;
      document.body.removeChild(overlay);
      resolve({ terminal: terminal });
    };
    overlay.querySelector('#sinav-iptal-btn').onclick = function() {
      document.body.removeChild(overlay);
      resolve(null);
    };
  });
}

async function sinavDurumDegistir(id, aktifYap) {
  let sinavTerminal = false;
  if (aktifYap) {
    // Terminal seçeneğiyle onay sor
    const sonuc = await sinavBaslatDialog();
    if (!sonuc) return;
    sinavTerminal = sonuc.terminal;
  } else {
    if (!confirm("Sınav yayından kaldırılsın mı?")) return;
  }

  const yanit = await safeFetch('/api/sinav/aktiflestir', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sinav_id: id, aktif: aktifYap, sinav_terminal: sinavTerminal })
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
  document.getElementById('rubrik-formu-alani').style.display = 'none';
  document.getElementById('aktif-sinav-baslik').innerText = `Soru Yönetimi: ${baslik}`;
  document.getElementById('soru-sinav-id').value = sinavId;
  document.getElementById('soru-tipi').value = 'cok_secmeli';
  document.getElementById('soru-bloom').value = '';
  document.getElementById('soru-zorluk').value = '';
  soruTipiDegistir();
  mevcutSorulariGetir(sinavId);
  ciktiListesiniGuncelle(sinavId);
}

function soruEklemeKapat() {
  document.getElementById('soru-yonetimi-alani').style.display = 'none';
}

function soruTipiDegistir() {
  const tip = document.getElementById('soru-tipi').value;
  document.getElementById('secenekler-alani').style.display = tip === 'cok_secmeli' ? 'block' : 'none';
  document.getElementById('dogru-yanlis-alani').style.display = tip === 'dogru_yanlis' ? 'block' : 'none';
  document.getElementById('bosluk-doldurma-alani').style.display = tip === 'bosluk_doldurma' ? 'block' : 'none';
  document.getElementById('acik-uclu-alani').style.display = tip === 'acik_uclu' ? 'block' : 'none';
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

  const tipEtiket = { cok_secmeli: '📋 Çoktan Seçmeli', dogru_yanlis: '✔️ Doğru/Yanlış', bosluk_doldurma: '✏️ Boşluk Doldurma', acik_uclu: '📝 Açık Uçlu' };
  const tipRenk = { cok_secmeli: '#90cdf4', dogru_yanlis: '#fbd38d', bosluk_doldurma: '#9ae6b4', acik_uclu: '#d6bcfa' };

  let html = '';
  veri.sorular.forEach((s, idx) => {
    const badge = `<span style="background:${tipRenk[s.tip] || '#718096'};color:#1a202c;padding:1px 8px;border-radius:10px;font-size:0.7rem;font-weight:bold;margin-left:0.5rem;">${tipEtiket[s.tip] || s.tip}</span>`;
    html += `<div style="background:#1a202c; padding:1rem; border-radius:6px; margin-bottom:1rem; border:1px solid #4a5568;">
          <div style="font-weight:bold; color:#e2e8f0; margin-bottom:0.5rem;">Soru ${idx + 1}: ${esc(s.metin)} ${badge} <span style="color:#a0aec0;font-size:0.8rem;font-weight:normal;">(${s.puan} Puan)</span></div>`;

    if (s.tip === 'cok_secmeli' || s.tip === 'dogru_yanlis') {
      s.secenekler.forEach((sec, sIdx) => {
        const color = sec.dogru_mu ? '#48bb78' : '#a0aec0';
        html += `<div style="color:${color}; font-size:0.9rem; margin-left:1rem; margin-bottom:0.25rem;">${String.fromCharCode(65 + sIdx)}) ${esc(sec.metin)} ${sec.dogru_mu ? '(Doğru Cevap)' : ''}</div>`;
      });
    } else if (s.tip === 'bosluk_doldurma') {
      const dogru = s.secenekler.find(x => x.dogru_mu);
      html += `<div style="color:#9ae6b4; font-size:0.9rem; margin-left:1rem;">Doğru cevap: <strong>${dogru ? esc(dogru.metin) : '?'}</strong></div>`;
    } else if (s.tip === 'acik_uclu') {
      html += `<div style="color:#d6bcfa; font-size:0.9rem; margin-left:1rem;">Öğrenci serbest metin yazacak (manuel puanlama)</div>`;
    }
    // Rubrik bilgileri
    const bloomEtiket = {bilgi:'Bilgi',kavrama:'Kavrama',uygulama:'Uygulama',analiz:'Analiz',degerlendirme:'Değerlendirme',yaratma:'Yaratma'};
    const zorlukEtiket = {cok_kolay:'Çok Kolay',kolay:'Kolay',orta:'Orta',zor:'Zor',cok_zor:'Çok Zor'};
    let rubrikInfo = [];
    if (s.bloom_seviyesi) rubrikInfo.push(`Bloom: ${bloomEtiket[s.bloom_seviyesi] || s.bloom_seviyesi}`);
    if (s.zorluk) rubrikInfo.push(`Zorluk: ${zorlukEtiket[s.zorluk] || s.zorluk}`);
    if (s.ciktilar && s.ciktilar.length > 0) rubrikInfo.push(`Çıktılar: ${s.ciktilar.map(c => c.numara).join(', ')}`);
    if (rubrikInfo.length > 0) {
      html += `<div style="color:#fbd38d;font-size:0.8rem;margin-left:1rem;margin-top:0.3rem;opacity:0.8;">${rubrikInfo.join(' | ')}</div>`;
    }
    html += `</div>`;
  });
  kutu.innerHTML = html;
}

async function soruKaydet() {
  const sinavId = document.getElementById('soru-sinav-id').value;
  const metin = document.getElementById('soru-metni').value;
  const tip = document.getElementById('soru-tipi').value;

  if (!metin.trim()) {
    alert("Soru metni boş olamaz!");
    return;
  }

  // Rubrik bilgileri
  const bloom = document.getElementById('soru-bloom').value;
  const zorluk = document.getElementById('soru-zorluk').value;
  const ciktiCheckboxes = document.querySelectorAll('#cikti-secim-listesi input[type="checkbox"]:checked');
  const ciktiIdler = Array.from(ciktiCheckboxes).map(cb => parseInt(cb.value));

  const payload = { sinav_id: sinavId, metin: metin, tip: tip, puan: 10, bloom_seviyesi: bloom, zorluk: zorluk, cikti_idler: ciktiIdler };

  if (tip === 'cok_secmeli') {
    let secenekler = [];
    let secilenDogruIndex = parseInt(document.querySelector('input[name="dogru_secenek"]:checked').value);
    for (let i = 0; i < 4; i++) {
      let optText = document.getElementById(`secenek-${i}`).value.trim();
      if (optText !== '') {
        secenekler.push({ metin: optText, dogru_mu: (secilenDogruIndex === i) });
      }
    }
    if (secenekler.length < 2) { alert("En az 2 seçenek girmelisiniz!"); return; }
    payload.secenekler = secenekler;

  } else if (tip === 'dogru_yanlis') {
    payload.dogru_cevap = document.querySelector('input[name="dy_cevap"]:checked').value;

  } else if (tip === 'bosluk_doldurma') {
    const cevap = document.getElementById('dogru-cevap-metin').value.trim();
    if (!cevap) { alert("Doğru cevap girilmeli!"); return; }
    payload.dogru_cevap = cevap;
  }
  // acik_uclu: ek veri gerekmez

  const yanit = await safeFetch('/api/sinav/soru_ekle', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (yanit.ok) {
    // Formu temizle
    document.getElementById('soru-metni').value = '';
    for (let i = 0; i < 4; i++) document.getElementById(`secenek-${i}`).value = '';
    document.querySelectorAll('input[name="dogru_secenek"]')[0].checked = true;
    document.getElementById('dogru-cevap-metin').value = '';
    document.getElementById('soru-bloom').value = '';
    document.getElementById('soru-zorluk').value = '';
    document.querySelectorAll('#cikti-secim-listesi input[type="checkbox"]').forEach(cb => cb.checked = false);

    mevcutSorulariGetir(sinavId);
    sinavListesiniGuncelle();
  } else {
    const v = await yanit.json();
    alert("Hata: " + (v.mesaj || 'Bilinmeyen hata'));
  }
}

// ── Öğrenci Yönetimi ──────────────────────────────────────────────

let _yonetimSiniflari = [];
let _yonetimOgrencileri = [];

async function ogrenciYonetimCek() {
  try {
    const yanit = await safeFetch('/api/siniflar');
    const veri = await yanit.json();
    _yonetimSiniflari = veri.siniflar || [];

    const ekleSinif = document.getElementById('ekle-sinif-id');
    const filtreSinif = document.getElementById('yonetim-sinif-filtre');

    if (ekleSinif) {
      ekleSinif.innerHTML = '<option value="">Sınıf seçin...</option>' +
        _yonetimSiniflari.map(s => '<option value="' + s.id + '">' + esc(s.ad) + ' (' + s.kayitli + ')</option>').join('');
    }
    if (filtreSinif) {
      const secili = filtreSinif.value;
      filtreSinif.innerHTML = '<option value="">Tüm sınıflar</option>' +
        _yonetimSiniflari.map(s => '<option value="' + s.id + '"' + (s.id == secili ? ' selected' : '') + '>' + esc(s.ad) + ' (' + s.kayitli + ')</option>').join('');
    }

    ogrenciYonetimListele(filtreSinif ? filtreSinif.value : '');
  } catch (e) { console.error('Öğrenci yönetimi yükleme hatası:', e); }
}

async function ogrenciYonetimListele(sinifId) {
  const kutu = document.getElementById('ogrenci-yonetim-listesi');
  if (!kutu) return;

  try {
    let tumOgrenciler = [];

    if (sinifId) {
      const yanit = await safeFetch('/api/sinif_ogrencileri/' + sinifId);
      const veri = await yanit.json();
      const sinifAdi = (_yonetimSiniflari.find(function (s) { return s.id == sinifId; }) || {}).ad || '';
      tumOgrenciler = veri.ogrenciler.map(function (o) { return Object.assign({}, o, { sinif_ad: sinifAdi, sinif_id: sinifId }); });
    } else {
      for (const sinif of _yonetimSiniflari) {
        const yanit = await safeFetch('/api/sinif_ogrencileri/' + sinif.id);
        const veri = await yanit.json();
        tumOgrenciler.push.apply(tumOgrenciler, veri.ogrenciler.map(function (o) { return Object.assign({}, o, { sinif_ad: sinif.ad, sinif_id: sinif.id }); }));
      }
    }

    _yonetimOgrencileri = tumOgrenciler;

    if (tumOgrenciler.length === 0) {
      kutu.textContent = 'Kayıtlı öğrenci yok.';
      kutu.style.color = '#718096';
      kutu.style.textAlign = 'center';
      kutu.style.padding = '1rem';
      return;
    }

    // Build DOM safely
    kutu.innerHTML = '';

    // Sınıf silme butonları
    if (!sinifId) {
      var sinifDiv = document.createElement('div');
      sinifDiv.style.cssText = 'margin-bottom:1rem;display:flex;flex-wrap:wrap;gap:0.3rem;';
      _yonetimSiniflari.forEach(function (s) {
        var span = document.createElement('span');
        span.style.cssText = 'display:inline-flex;align-items:center;gap:0.3rem;background:#2d3748;border:1px solid #4a5568;border-radius:6px;padding:0.2rem 0.5rem;font-size:0.8rem;';
        span.textContent = s.ad + ' (' + s.kayitli + ')';
        if (s.kayitli === 0) {
          var btn = document.createElement('button');
          btn.style.cssText = 'background:#742a2a;border:1px solid #9b2c2c;border-radius:3px;color:#feb2b2;cursor:pointer;font-size:0.7rem;padding:0 4px;';
          btn.textContent = 'x';
          btn.title = 'Sınıfı sil';
          btn.addEventListener('click', (function (id, ad) { return function () { sinifSil(id, ad); }; })(s.id, s.ad));
          span.appendChild(btn);
        }
        sinifDiv.appendChild(span);
      });
      kutu.appendChild(sinifDiv);
    }

    var toplamDiv = document.createElement('div');
    toplamDiv.style.cssText = 'color:#a0aec0;font-size:0.8rem;margin-bottom:0.5rem;';
    toplamDiv.textContent = 'Toplam: ' + tumOgrenciler.length + ' öğrenci';
    kutu.appendChild(toplamDiv);

    tumOgrenciler.forEach(function (o) {
      var row = document.createElement('div');
      row.className = 'ogrenci-mini';
      row.style.cssText = 'padding:6px 0;display:flex;align-items:center;gap:8px;';

      var sinifSpan = document.createElement('span');
      sinifSpan.style.cssText = 'color:#90cdf4;font-size:0.75rem;min-width:100px;';
      sinifSpan.textContent = o.sinif_ad || '';
      row.appendChild(sinifSpan);

      var numaraSpan = document.createElement('span');
      numaraSpan.style.cssText = 'min-width:90px;color:#a0aec0;font-size:0.8rem;';
      numaraSpan.textContent = o.numara;
      row.appendChild(numaraSpan);

      var adSpan = document.createElement('span');
      adSpan.style.cssText = 'flex:1;font-size:0.85rem;';
      adSpan.textContent = o.ad_soyad;
      row.appendChild(adSpan);

      var silBtn = document.createElement('button');
      silBtn.style.cssText = 'padding:0.15rem 0.5rem;font-size:0.7rem;background:#742a2a;border:1px solid #9b2c2c;border-radius:4px;color:#feb2b2;cursor:pointer;';
      silBtn.title = 'Öğrenciyi sil';
      silBtn.textContent = '🗑️';
      silBtn.addEventListener('click', (function (num, ad) { return function () { ogrenciSil(num, ad); }; })(o.numara, o.ad_soyad));
      row.appendChild(silBtn);

      kutu.appendChild(row);
    });
  } catch (e) { console.error('Liste yükleme hatası:', e); }
}

async function ogrenciEkle() {
  var sinifId = document.getElementById('ekle-sinif-id').value;
  var numara = document.getElementById('ekle-numara').value.trim();
  var ad = document.getElementById('ekle-ad').value.trim();
  var soyad = document.getElementById('ekle-soyad').value.trim();

  if (!sinifId || !numara || !ad || !soyad) {
    alert('Lütfen tüm alanları doldurun.');
    return;
  }

  try {
    var yanit = await safeFetch('/api/ogrenci_ekle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sinif_id: sinifId, numara: numara, ad: ad, soyad: soyad })
    });
    var veri = await yanit.json();
    if (veri.durum === 'ok') {
      document.getElementById('ekle-numara').value = '';
      document.getElementById('ekle-ad').value = '';
      document.getElementById('ekle-soyad').value = '';
      ogrenciYonetimCek();
      sinifDurumCek();
    } else {
      alert('Hata: ' + veri.mesaj);
    }
  } catch (e) { alert('Bağlantı hatası: ' + e.message); }
}

async function ogrenciSil(numara, adSoyad) {
  if (!confirm(adSoyad + ' (' + numara + ') silinecek. Emin misiniz?')) return;

  try {
    var yanit = await safeFetch('/api/ogrenci_sil', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ numara: numara })
    });
    var veri = await yanit.json();
    if (veri.durum === 'ok') {
      ogrenciYonetimCek();
      sinifDurumCek();
    } else {
      alert('Hata: ' + veri.mesaj);
    }
  } catch (e) { alert('Bağlantı hatası: ' + e.message); }
}

async function sinifEkle() {
  var ad = document.getElementById('yeni-sinif-adi').value.trim();
  if (!ad) {
    alert('Sınıf adı boş olamaz.');
    return;
  }

  try {
    var yanit = await safeFetch('/api/sinif_ekle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ad: ad })
    });
    var veri = await yanit.json();
    if (veri.durum === 'ok') {
      document.getElementById('yeni-sinif-adi').value = '';
      ogrenciYonetimCek();
      sinifDurumCek();
    } else {
      alert('Hata: ' + veri.mesaj);
    }
  } catch (e) { alert('Bağlantı hatası: ' + e.message); }
}

async function sinifSil(sinifId, sinifAdi) {
  if (!confirm('"' + sinifAdi + '" sınıfını silmek istediğinize emin misiniz?')) return;

  try {
    var yanit = await safeFetch('/api/sinif_sil', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sinif_id: sinifId })
    });
    var veri = await yanit.json();
    if (veri.durum === 'ok') {
      ogrenciYonetimCek();
      sinifDurumCek();
    } else {
      alert('Hata: ' + veri.mesaj);
    }
  } catch (e) { alert('Bağlantı hatası: ' + e.message); }
}

// ── Öğrenme Çıktıları CRUD ──────────────────────────────────────────

let _mevcutCiktilar = [];

async function ciktiListesiniGuncelle(sinavId) {
  if (!sinavId) sinavId = document.getElementById('soru-sinav-id').value;
  const yanit = await safeFetch(`/api/sinav/ciktilar/${sinavId}`);
  const veri = await yanit.json();
  _mevcutCiktilar = veri.ciktilar || [];

  // Çıktı listesi (yönetim)
  const kutu = document.getElementById('cikti-listesi-kutu');
  if (_mevcutCiktilar.length === 0) {
    kutu.innerHTML = '<div style="color:#718096;">Henüz öğrenme çıktısı eklenmemiş.</div>';
  } else {
    let html = '';
    _mevcutCiktilar.forEach(c => {
      html += `<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;background:#1a202c;padding:0.4rem 0.6rem;border-radius:6px;border:1px solid #4a5568;">
        <span style="color:#fbd38d;font-weight:bold;min-width:24px;">${esc(String(c.numara))}.</span>
        <span style="flex:1;color:#e2e8f0;">${esc(c.metin)}</span>
        <button class="btn-kucuk" style="background:#742a2a;font-size:0.7rem;padding:2px 6px;" onclick="ciktiSil(${c.id})">x</button>
      </div>`;
    });
    kutu.innerHTML = html;
  }

  // Soru formundaki checkbox listesi
  const secimKutu = document.getElementById('cikti-secim-listesi');
  if (_mevcutCiktilar.length === 0) {
    secimKutu.innerHTML = '<span style="color:#718096;font-size:0.8rem;">Önce öğrenme çıktısı ekleyin</span>';
  } else {
    let html = '';
    _mevcutCiktilar.forEach(c => {
      html += `<label style="display:flex;align-items:center;gap:4px;background:#1a202c;padding:3px 8px;border-radius:6px;border:1px solid #4a5568;cursor:pointer;font-size:0.8rem;color:#e2e8f0;">
        <input type="checkbox" value="${c.id}" style="width:14px;height:14px;">
        <span style="color:#fbd38d;font-weight:bold;">${esc(String(c.numara))}</span>- ${esc(c.metin.substring(0, 40))}${c.metin.length > 40 ? '...' : ''}
      </label>`;
    });
    secimKutu.innerHTML = html;
  }
}

async function ciktiEkle() {
  const sinavId = document.getElementById('soru-sinav-id').value;
  const metin = document.getElementById('yeni-cikti-metin').value.trim();
  if (!metin) { alert('Çıktı metni boş olamaz!'); return; }

  const yanit = await safeFetch('/api/sinav/cikti_ekle', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sinav_id: sinavId, metin: metin })
  });
  if (yanit.ok) {
    document.getElementById('yeni-cikti-metin').value = '';
    ciktiListesiniGuncelle(sinavId);
  }
}

async function ciktiSil(ciktiId) {
  if (!confirm('Bu öğrenme çıktısını silmek istediğinize emin misiniz?')) return;
  const yanit = await safeFetch('/api/sinav/cikti_sil', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cikti_id: ciktiId })
  });
  if (yanit.ok) ciktiListesiniGuncelle();
}

// ── Rubrik Formu ──────────────────────────────────────────────

async function rubrikFormuAc(sinavId, baslik) {
  document.getElementById('rubrik-formu-alani').style.display = 'block';
  document.getElementById('soru-yonetimi-alani').style.display = 'none';
  document.getElementById('sinav-sonuclari-alani').style.display = 'none';
  document.getElementById('rubrik-sinav-baslik').innerText = `Rubrik Formu: ${baslik}`;

  const icerik = document.getElementById('rubrik-formu-icerik');
  icerik.innerHTML = '<div style="color:#718096;text-align:center;">Yükleniyor...</div>';

  const yanit = await safeFetch(`/api/sinav/rubrik/${sinavId}`);
  const veri = await yanit.json();

  if (!veri.sorular || veri.sorular.length === 0) {
    icerik.innerHTML = '<div style="color:#718096;text-align:center;">Bu sınavda henüz soru yok.</div>';
    return;
  }

  const bloomEtiket = {bilgi:'Bilgi',kavrama:'Kavrama',uygulama:'Uygulama',analiz:'Analiz',degerlendirme:'Değerlendirme',yaratma:'Yaratma'};
  const zorlukEtiket = {cok_kolay:'Çok Kolay',kolay:'Kolay',orta:'Orta',zor:'Zor',cok_zor:'Çok Zor'};
  const tipEtiket = {cok_secmeli:'Çoktan Seçmeli',dogru_yanlis:'D/Y',bosluk_doldurma:'Boşluk Dold.',acik_uclu:'Açık Uçlu'};

  let html = '<div id="rubrik-yazdir-alani">';

  // Başlık
  html += `<div style="text-align:center;margin-bottom:1.5rem;">
    <div style="font-size:0.75rem;color:#a0aec0;">DKM.FR.033 SINAV RUBRİK FORMU</div>
    <h3 style="color:#e2e8f0;margin:0.25rem 0;">${esc(veri.sinav.baslik)}</h3>
  </div>`;

  // Öğrenme Çıktıları
  if (veri.ciktilar.length > 0) {
    html += `<div style="margin-bottom:1.5rem;background:#1a202c;padding:1rem;border-radius:8px;border:1px solid #4a5568;">
      <h4 style="color:#fbd38d;margin:0 0 0.5rem;">Dersin Öğrenme Çıktıları</h4>`;
    veri.ciktilar.forEach(c => {
      html += `<div style="color:#e2e8f0;font-size:0.85rem;margin-bottom:0.3rem;"><strong style="color:#fbd38d;">${esc(String(c.numara))}.</strong> ${esc(c.metin)}</div>`;
    });
    html += '</div>';
  }

  // Tablo-1: Soru-Çıktı İlişki Matrisi
  html += `<h4 style="color:#90cdf4;margin:0 0 0.5rem;">Tablo-1: Dereceli Puanlama Anahtarı</h4>`;
  html += `<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:0.8rem;color:#e2e8f0;border:1px solid #4a5568;">
    <thead><tr style="background:#2b6cb0;color:#fff;">
      <th style="padding:8px;border:1px solid #4a5568;width:40px;">Soru</th>
      <th style="padding:8px;border:1px solid #4a5568;">Tip</th>
      <th style="padding:8px;border:1px solid #4a5568;">Puan</th>
      <th style="padding:8px;border:1px solid #4a5568;">Kazanım No</th>
      <th style="padding:8px;border:1px solid #4a5568;">İlişkili Öğrenme Çıktısı</th>
    </tr></thead><tbody>`;

  let toplamPuan = 0;
  veri.sorular.forEach((s, idx) => {
    toplamPuan += s.puan;
    const kazanimNo = s.ciktilar.length > 0 ? s.ciktilar.map(c => c.numara).join(', ') : '-';
    const ciktiMetinleri = s.ciktilar.length > 0 ? s.ciktilar.map(c => esc(c.metin)).join('; ') : '-';
    html += `<tr style="border:1px solid #4a5568;">
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;font-weight:bold;">${idx + 1}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${tipEtiket[s.tip] || esc(s.tip)}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${s.puan}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;color:#fbd38d;">${esc(String(kazanimNo))}</td>
      <td style="padding:6px;border:1px solid #4a5568;font-size:0.75rem;">${ciktiMetinleri}</td>
    </tr>`;
  });
  html += `<tr style="background:#2d3748;font-weight:bold;">
    <td colspan="2" style="padding:6px;border:1px solid #4a5568;text-align:right;">TOPLAM</td>
    <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${toplamPuan}</td>
    <td colspan="2" style="padding:6px;border:1px solid #4a5568;"></td>
  </tr></tbody></table></div>`;

  // Tablo-2: Zorluk Düzeyi Dağılımı
  html += `<h4 style="color:#90cdf4;margin:1.5rem 0 0.5rem;">Tablo-2: Soru Zorluk Düzeyi Dağılımı</h4>`;
  html += `<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:0.8rem;color:#e2e8f0;border:1px solid #4a5568;">
    <thead><tr style="background:#2b6cb0;color:#fff;">
      <th style="padding:8px;border:1px solid #4a5568;">Soru</th>
      <th style="padding:8px;border:1px solid #4a5568;">Çok Kolay (1)</th>
      <th style="padding:8px;border:1px solid #4a5568;">Kolay (2)</th>
      <th style="padding:8px;border:1px solid #4a5568;">Orta (3)</th>
      <th style="padding:8px;border:1px solid #4a5568;">Zor (4)</th>
      <th style="padding:8px;border:1px solid #4a5568;">Çok Zor (5)</th>
    </tr></thead><tbody>`;
  veri.sorular.forEach((s, idx) => {
    const z = s.zorluk;
    html += `<tr style="border:1px solid #4a5568;">
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;font-weight:bold;">${idx + 1}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${z === 'cok_kolay' ? '●' : ''}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${z === 'kolay' ? '●' : ''}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${z === 'orta' ? '●' : ''}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${z === 'zor' ? '●' : ''}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${z === 'cok_zor' ? '●' : ''}</td>
    </tr>`;
  });
  html += '</tbody></table></div>';

  // Tablo-3: Bloom Taksonomisi Dağılımı
  html += `<h4 style="color:#90cdf4;margin:1.5rem 0 0.5rem;">Tablo-3: Bloom Taksonomisi Dağılımı</h4>`;
  html += `<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:0.8rem;color:#e2e8f0;border:1px solid #4a5568;">
    <thead><tr style="background:#2b6cb0;color:#fff;">
      <th style="padding:8px;border:1px solid #4a5568;">Soru</th>
      <th style="padding:8px;border:1px solid #4a5568;">Bilgi (1)</th>
      <th style="padding:8px;border:1px solid #4a5568;">Kavrama (2)</th>
      <th style="padding:8px;border:1px solid #4a5568;">Uygulama (3)</th>
      <th style="padding:8px;border:1px solid #4a5568;">Analiz (4)</th>
      <th style="padding:8px;border:1px solid #4a5568;">Değerlendirme (5)</th>
      <th style="padding:8px;border:1px solid #4a5568;">Yaratma (6)</th>
    </tr></thead><tbody>`;
  veri.sorular.forEach((s, idx) => {
    const b = s.bloom_seviyesi;
    html += `<tr style="border:1px solid #4a5568;">
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;font-weight:bold;">${idx + 1}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${b === 'bilgi' ? '●' : ''}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${b === 'kavrama' ? '●' : ''}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${b === 'uygulama' ? '●' : ''}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${b === 'analiz' ? '●' : ''}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${b === 'degerlendirme' ? '●' : ''}</td>
      <td style="padding:6px;border:1px solid #4a5568;text-align:center;">${b === 'yaratma' ? '●' : ''}</td>
    </tr>`;
  });
  html += '</tbody></table></div>';

  // Özet İstatistikler
  const bloomDagilim = {};
  const zorlukDagilim = {};
  veri.sorular.forEach(s => {
    if (s.bloom_seviyesi) bloomDagilim[s.bloom_seviyesi] = (bloomDagilim[s.bloom_seviyesi] || 0) + 1;
    if (s.zorluk) zorlukDagilim[s.zorluk] = (zorlukDagilim[s.zorluk] || 0) + 1;
  });

  html += `<div style="display:flex;gap:1rem;margin-top:1.5rem;">`;
  html += `<div style="flex:1;background:#1a202c;padding:0.75rem;border-radius:8px;border:1px solid #4a5568;">
    <h5 style="color:#90cdf4;margin:0 0 0.5rem;">Bloom Dağılımı</h5>`;
  Object.entries(bloomEtiket).forEach(([key, label]) => {
    const sayi = bloomDagilim[key] || 0;
    if (sayi > 0) html += `<div style="font-size:0.8rem;margin-bottom:2px;"><span style="color:#fbd38d;">${label}:</span> ${sayi} soru</div>`;
  });
  if (Object.keys(bloomDagilim).length === 0) html += '<div style="color:#718096;font-size:0.8rem;">Belirtilmemiş</div>';
  html += '</div>';

  html += `<div style="flex:1;background:#1a202c;padding:0.75rem;border-radius:8px;border:1px solid #4a5568;">
    <h5 style="color:#90cdf4;margin:0 0 0.5rem;">Zorluk Dağılımı</h5>`;
  Object.entries(zorlukEtiket).forEach(([key, label]) => {
    const sayi = zorlukDagilim[key] || 0;
    if (sayi > 0) html += `<div style="font-size:0.8rem;margin-bottom:2px;"><span style="color:#fbd38d;">${label}:</span> ${sayi} soru</div>`;
  });
  if (Object.keys(zorlukDagilim).length === 0) html += '<div style="color:#718096;font-size:0.8rem;">Belirtilmemiş</div>';
  html += '</div></div>';

  html += '</div>';
  icerik.innerHTML = html;
}

function rubrikYazdir() {
  const icerik = document.getElementById('rubrik-yazdir-alani');
  if (!icerik) return;
  const win = window.open('', '_blank');
  const doc = win.document;
  doc.open();
  doc.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>Rubrik Formu</title>');
  doc.write('<style>body{font-family:Arial,sans-serif;color:#1a202c;padding:2rem}table{width:100%;border-collapse:collapse;margin-bottom:1rem}th,td{border:1px solid #333;padding:6px 8px;font-size:0.8rem}th{background:#2b6cb0;color:#fff}h3,h4{margin:0.5rem 0}@media print{body{padding:0.5cm}}</style>');
  doc.write('</head><body>');
  doc.write(icerik.innerHTML);
  doc.write('</body></html>');
  doc.close();
  win.onload = function() { win.print(); };
}

// ── Sınav İhlal Kontrol (Öğretmen) ──────────────────────────────

let _gosterilmisIhlaller = new Set();

async function sinavIhlalKontrol() {
  // Aktif sınavı bul
  try {
    const yanit = await safeFetch('/api/sinav/liste');
    const veri = await yanit.json();
    const aktifSinav = (veri.sinavlar || []).find(s => s.aktif);
    if (!aktifSinav) return;

    const ihlalYanit = await safeFetch(`/api/sinav/ihlaller/${aktifSinav.id}`);
    const ihlalVeri = await ihlalYanit.json();

    (ihlalVeri.ihlaller || []).forEach(ihlal => {
      if (ihlal.durum === 'beklemede' && !_gosterilmisIhlaller.has(ihlal.id)) {
        _gosterilmisIhlaller.add(ihlal.id);
        _ihlalPopupGoster(ihlal);
      }
    });
  } catch(e) {}
}

function _ihlalPopupGoster(ihlal) {
  const adSoyad = (ihlal.ad && ihlal.soyad) ? (ihlal.ad + ' ' + ihlal.soyad) : ihlal.ogrenci_numara;
  const zaman = ihlal.zaman || '';

  const overlay = document.createElement('div');
  overlay.id = 'ihlal-popup-' + ihlal.id;
  overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:10002;display:flex;align-items:center;justify-content:center;';

  const popup = document.createElement('div');
  popup.style.cssText = 'background:#2d3748;border-radius:12px;padding:2rem;max-width:450px;width:90%;box-shadow:0 8px 32px rgba(0,0,0,0.5);border:2px solid #fc8181;';

  const baslik = document.createElement('div');
  baslik.style.cssText = 'display:flex;align-items:center;gap:0.5rem;margin-bottom:1rem;';
  baslik.innerHTML = '<span style="font-size:2rem;">⚠️</span><div><h3 style="color:#fc8181;margin:0;">Tam Ekran İhlali</h3><span style="color:#a0aec0;font-size:0.8rem;">' + zaman + '</span></div>';
  popup.appendChild(baslik);

  const bilgi = document.createElement('div');
  bilgi.style.cssText = 'background:#1a202c;padding:0.75rem;border-radius:8px;margin-bottom:1rem;';
  bilgi.innerHTML = '<div style="color:#e2e8f0;font-size:0.95rem;margin-bottom:0.3rem;"><strong>' + adSoyad + '</strong> <span style="color:#a0aec0;">(' + ihlal.ogrenci_numara + ')</span></div>';
  if (ihlal.aciklama) {
    bilgi.innerHTML += '<div style="color:#fbd38d;font-size:0.85rem;margin-top:0.5rem;"><strong>Sebep:</strong> ' + ihlal.aciklama + '</div>';
  } else {
    bilgi.innerHTML += '<div style="color:#718096;font-size:0.85rem;margin-top:0.5rem;">Henüz açıklama gönderilmedi</div>';
  }
  popup.appendChild(bilgi);

  const butonlar = document.createElement('div');
  butonlar.style.cssText = 'display:flex;gap:10px;';

  const devamBtn = document.createElement('button');
  devamBtn.style.cssText = 'flex:1;background:#48bb78;color:white;border:none;padding:10px;border-radius:8px;font-weight:bold;cursor:pointer;font-size:0.95rem;';
  devamBtn.textContent = 'Sınava Devam Ettir';
  devamBtn.addEventListener('click', function() { _ihlalKarariVer(ihlal.id, 'onayla', overlay); });

  const sonlandirBtn = document.createElement('button');
  sonlandirBtn.style.cssText = 'flex:1;background:#e53e3e;color:white;border:none;padding:10px;border-radius:8px;font-weight:bold;cursor:pointer;font-size:0.95rem;';
  sonlandirBtn.textContent = 'Sınavı Sonlandır';
  sonlandirBtn.addEventListener('click', function() { _ihlalKarariVer(ihlal.id, 'reddet', overlay); });

  butonlar.appendChild(devamBtn);
  butonlar.appendChild(sonlandirBtn);
  popup.appendChild(butonlar);

  overlay.appendChild(popup);
  document.body.appendChild(overlay);

  // Ses ile uyar
  try { new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2telebn/telebn/telebn/telebn').play(); } catch(e) {}
}

async function _ihlalKarariVer(ihlalId, karar, overlay) {
  try {
    await safeFetch('/api/sinav/ihlal_' + karar, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ihlal_id: ihlalId })
    });
  } catch(e) {}
  if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
  _gosterilmisIhlaller.delete(ihlalId);
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

// ── Sistem Logları (PG app_log tablosundan) ────────────────────
let _logVerisi = [];
let _logSonId = 0;
let _logOtomatikInterval = null;

const _seviyeRenk = {
  DEBUG:    '#718096',
  INFO:     '#68d391',
  WARNING:  '#f6ad55',
  ERROR:    '#fc8181',
  CRITICAL: '#fc8181',
};

function loglarRenderEt() {
  const kutu = document.getElementById('log-kutu');
  if (!kutu) return;

  if (_logVerisi.length === 0) {
    kutu.innerHTML = '<div style="color:#4a5568;text-align:center;padding:2rem;">Log bulunamadı.</div>';
    const s = document.getElementById('log-sayac');
    if (s) s.textContent = '';
    return;
  }

  const frag = document.createDocumentFragment();
  // Reverse — yenisi altta görünsün (DESC sorgu → ASC render)
  _logVerisi.slice().reverse().forEach(e => {
    const renk = _seviyeRenk[e.level] || '#a0aec0';
    const satir = document.createElement('div');
    satir.style.cssText = 'padding:3px 4px;border-bottom:1px solid #1a202c;white-space:pre-wrap;word-break:break-all;';

    const ts = document.createElement('span');
    ts.style.color = '#4a5568';
    ts.textContent = (e.ts || '').substring(11, 19) + ' ';

    const sev = document.createElement('span');
    sev.style.cssText = 'color:' + renk + ';font-weight:bold;min-width:5rem;display:inline-block;';
    sev.textContent = '[' + (e.level || '?') + '] ';

    const logger = document.createElement('span');
    logger.style.cssText = 'color:#90cdf4;font-size:0.72rem;margin-right:0.4rem;';
    logger.textContent = e.logger ? '(' + e.logger + ')' : '';

    const msg = document.createElement('span');
    msg.style.color = '#e2e8f0';
    msg.textContent = e.message;

    satir.appendChild(ts);
    satir.appendChild(sev);
    satir.appendChild(logger);
    satir.appendChild(msg);

    if (e.kullanici) {
      const u = document.createElement('span');
      u.style.cssText = 'color:#fbd38d;font-size:0.72rem;margin-left:0.5rem;';
      u.textContent = '· ' + e.kullanici;
      satir.appendChild(u);
    }
    if (e.ip) {
      const ip = document.createElement('span');
      ip.style.cssText = 'color:#4a5568;font-size:0.72rem;margin-left:0.4rem;';
      ip.textContent = '· ' + e.ip;
      satir.appendChild(ip);
    }

    frag.appendChild(satir);
  });

  kutu.innerHTML = '';
  kutu.appendChild(frag);
  kutu.scrollTop = kutu.scrollHeight;

  const sayac = document.getElementById('log-sayac');
  if (sayac) sayac.textContent = _logVerisi.length + ' kayıt';
}

async function loglarCek(tumu = false) {
  try {
    const level = document.getElementById('log-seviye-filtre')?.value || '';
    const q = document.getElementById('log-arama')?.value.trim() || '';
    const limit = document.getElementById('log-limit')?.value || '200';
    const since = (tumu || level || q) ? 0 : _logSonId;

    let url = '/api/loglar?limit=' + encodeURIComponent(limit);
    if (since > 0) url += '&since=' + since;
    if (level) url += '&level=' + encodeURIComponent(level);
    if (q) url += '&q=' + encodeURIComponent(q);

    const res = await safeFetch(url);
    const veri = await res.json();
    if (!veri.loglar) return;

    if (tumu || level || q) {
      _logVerisi = veri.loglar;
      _logSonId = veri.loglar.length > 0 ? veri.loglar[0].id : 0;
    } else {
      // Inkremental — yeni gelen log'ları başa ekle (DESC sıralama)
      if (veri.loglar.length > 0) {
        _logVerisi = veri.loglar.concat(_logVerisi);
        if (_logVerisi.length > parseInt(limit, 10)) {
          _logVerisi = _logVerisi.slice(0, parseInt(limit, 10));
        }
        _logSonId = veri.loglar[0].id;
      }
    }
    loglarRenderEt();
  } catch (e) {
    console.error('Log çekme hatası:', e);
  }
}

function logOtomatikToggle() {
  const aktif = document.getElementById('log-otomatik')?.checked;
  if (aktif) {
    _logOtomatikInterval = setInterval(() => loglarCek(false), 3000);
  } else {
    clearInterval(_logOtomatikInterval);
    _logOtomatikInterval = null;
  }
}

function logTemizleEkran() {
  _logVerisi = [];
  _logSonTs = 0;
  loglarRenderEt();
}

// Loglar tabına geçilince otomatik yenilemeyi başlat
document.addEventListener('DOMContentLoaded', () => {
  const orijTabGec = typeof tabGec === 'function' ? tabGec : null;
  if (!orijTabGec) return;
  window.tabGec = function(tab, btn) {
    if (tab === 'loglar') {
      if (!_logOtomatikInterval && document.getElementById('log-otomatik')?.checked) {
        _logOtomatikInterval = setInterval(() => loglarCek(false), 3000);
      }
    } else {
      clearInterval(_logOtomatikInterval);
      _logOtomatikInterval = null;
    }
    orijTabGec(tab, btn);
  };
});
