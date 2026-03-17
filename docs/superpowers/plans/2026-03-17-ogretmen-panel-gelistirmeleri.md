# Ogretmen Panel Gelistirmeleri - Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add attendance reporting, student attendance view, categorized help requests, and terminal monitoring/intervention to the Ders Takip Sistemi.

**Architecture:** Flask backend with SQLite, server-rendered HTML templates, vanilla JS frontend. Socket.IO for real-time terminal communication. All new features build on existing patterns — REST API endpoints in `routes/api.py`, UI in `templates/ogretmen.html` and `static/js/ogretmen.js`.

**Tech Stack:** Python/Flask, SQLite, Socket.IO, xterm.js, vanilla JS, existing dark-theme CSS

**Spec:** `docs/superpowers/specs/2026-03-17-ogretmen-panel-gelistirmeleri-design.md`

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `core/db.py` | Modify | Add `kategori` column migration for `yardim_talepleri` |
| `routes/api.py` | Modify | Add 4 new endpoints: `/api/ogrenci/devam`, `/api/yoklama/rapor`, `/api/terminal/aktif_oturumlar`, update `/api/yardim_talep` |
| `routes/student.py` | No change | Existing login flow unchanged |
| `static/js/ogrenci.js` | Modify | Add help category modal, attendance display on waiting screen |
| `static/js/ogretmen.js` | Modify | Add attendance report tab logic, category display in help list, terminal monitoring UI |
| `templates/ogrenci_ana.html` | Modify | Add attendance summary section, help category modal |
| `templates/ogretmen.html` | Modify | Add "Devam Raporu" tab, terminal monitoring panel, category filter in help tab |
| `templates/ogretmen_terminal.html` | Modify | Add student terminal list panel with monitoring xterm |
| `app.py` | Modify | Add Socket.IO events: `ogretmen_izle`, `ogretmen_izle_girdi`, `ogretmen_izle_birak` |

---

## Chunk 1: Kategorili Yardim Sistemi

### Task 1: Database migration — add kategori column

**Files:**
- Modify: `core/db.py:170-172` (after yardim_talepleri CREATE TABLE)

- [ ] **Step 1: Add migration in `core/db.py`**

After the `yardim_talepleri` CREATE TABLE block (line ~172), add:

```python
try: db.execute("ALTER TABLE yardim_talepleri ADD COLUMN kategori TEXT DEFAULT ''")
except: pass
```

- [ ] **Step 2: Verify migration runs**

Run: `python -c "from core.db import db_olustur; db_olustur()"`
Then: `sqlite3 data/yoklama.db ".schema yardim_talepleri"` — should show `kategori` column.

- [ ] **Step 3: Commit**

```bash
git add core/db.py
git commit -m "feat(db): add kategori column to yardim_talepleri"
```

### Task 2: Update help request API to accept and return kategori

**Files:**
- Modify: `routes/api.py:465-503`

- [ ] **Step 1: Update `api_yardim_talep` to accept kategori**

In `routes/api.py`, modify the `/yardim_talep` POST handler. After `ad_soyad` line, add kategori extraction. Update the INSERT to include kategori:

```python
@api_bp.route('/yardim_talep', methods=['POST'])
def api_yardim_talep():
    from flask import session
    numara = session.get('numara')
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Oturum yok'})

    ad_soyad = f"{session.get('ad', '')} {session.get('soyad', '')}".strip()

    veri = request.get_json(silent=True) or {}
    kategori = veri.get('kategori', '')
    gecerli_kategoriler = ['komut', 'dosya', 'terminal', 'soru', 'diger']
    if kategori and kategori not in gecerli_kategoriler:
        kategori = 'diger'

    with db_baglantisi() as db:
        mevcut = db.execute("SELECT id, durum FROM yardim_talepleri WHERE numara=? AND tarih=? AND durum != 'tamamlandi'", (numara, bugun())).fetchone()
        if mevcut:
            return jsonify({'durum': 'ok', 'mesaj': 'Zaten aktif bir yardım talebiniz var.'})

        db.execute(
            'INSERT INTO yardim_talepleri (tarih, saat, numara, ad_soyad, durum, kategori) VALUES (?, ?, ?, ?, ?, ?)',
            (bugun(), simdi(), numara, ad_soyad, 'bekliyor', kategori)
        )
        db.commit()
    return jsonify({'durum': 'ok'})
```

- [ ] **Step 2: Verify `/api/yardim_talepler` already returns all columns**

The existing code uses `SELECT *` and `dict(l)`, so `kategori` will automatically appear in the response. No change needed.

- [ ] **Step 3: Commit**

```bash
git add routes/api.py
git commit -m "feat(api): accept kategori param in yardim_talep endpoint"
```

### Task 3: Student UI — help category modal

**Files:**
- Modify: `templates/ogrenci_ana.html` (add modal HTML)
- Modify: `static/js/ogrenci.js` (update yardimTalepEt function)

- [ ] **Step 1: Add category modal HTML to `ogrenci_ana.html`**

Before the closing `</body>` tag (before `<script src="/static/js/ogrenci.js">`), add:

```html
<!-- Yardım Kategori Modal -->
<div id="yardim-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:10000; justify-content:center; align-items:center;">
  <div style="background:#2d3748; border-radius:12px; padding:1.5rem; max-width:360px; width:90%;">
    <h3 style="color:#90cdf4; margin:0 0 1rem; text-align:center;">Yardım Kategorisi Seçin</h3>
    <div style="display:flex; flex-direction:column; gap:0.5rem;">
      <button class="yardim-kat-btn" onclick="yardimGonder('komut')" style="background:#1a202c; border:1px solid #4a5568; color:#e2e8f0; padding:0.75rem; border-radius:8px; cursor:pointer; text-align:left; font-size:0.95rem;">
        🔧 Komut çalışmıyor
      </button>
      <button class="yardim-kat-btn" onclick="yardimGonder('dosya')" style="background:#1a202c; border:1px solid #4a5568; color:#e2e8f0; padding:0.75rem; border-radius:8px; cursor:pointer; text-align:left; font-size:0.95rem;">
        📁 Dosya bulamıyorum
      </button>
      <button class="yardim-kat-btn" onclick="yardimGonder('terminal')" style="background:#1a202c; border:1px solid #4a5568; color:#e2e8f0; padding:0.75rem; border-radius:8px; cursor:pointer; text-align:left; font-size:0.95rem;">
        💻 Terminal dondu
      </button>
      <button class="yardim-kat-btn" onclick="yardimGonder('soru')" style="background:#1a202c; border:1px solid #4a5568; color:#e2e8f0; padding:0.75rem; border-radius:8px; cursor:pointer; text-align:left; font-size:0.95rem;">
        ❓ Soru sormak istiyorum
      </button>
      <button class="yardim-kat-btn" onclick="yardimGonder('diger')" style="background:#1a202c; border:1px solid #4a5568; color:#e2e8f0; padding:0.75rem; border-radius:8px; cursor:pointer; text-align:left; font-size:0.95rem;">
        📋 Diğer
      </button>
    </div>
    <button onclick="document.getElementById('yardim-modal').style.display='none'" style="margin-top:1rem; width:100%; background:#4a5568; border:none; color:#a0aec0; padding:0.5rem; border-radius:6px; cursor:pointer;">
      İptal
    </button>
  </div>
</div>
```

- [ ] **Step 2: Update `yardimTalepEt()` in `ogrenci.js` to show modal instead of sending directly**

Replace the existing `yardimTalepEt()` function with:

```javascript
async function yardimTalepEt() {
  // Modal göster, kategori seçilince yardimGonder() çağrılır
  document.getElementById('yardim-modal').style.display = 'flex';
}

async function yardimGonder(kategori) {
  const modal = document.getElementById('yardim-modal');
  modal.style.display = 'none';

  const btn = document.getElementById('btn-yardim-talep');
  if (!btn) return;

  try {
    btn.textContent = '⏳ Gönderiliyor...';
    btn.disabled = true;
    btn.style.backgroundColor = '#718096';

    const res = await fetch('/api/yardim_talep', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ kategori: kategori })
    });
    const data = await res.json();

    if (data.durum === 'ok') {
      btn.textContent = '✅ Yardım Bekleniyor...';
      btn.style.backgroundColor = '#48bb78';
    } else {
      alert('Hata: ' + data.mesaj);
      btn.disabled = false;
      btn.textContent = '🙋‍♂️ Yardım İste';
      btn.style.backgroundColor = '#2b6cb0';
    }
  } catch (e) {
    alert("Hata oluştu.");
    btn.disabled = false;
    btn.textContent = '🙋‍♂️ Yardım İste';
    btn.style.backgroundColor = '#2b6cb0';
  }
}
```

- [ ] **Step 3: Test manually**

Start server, login as student, click "Yardım İste" → category modal should appear. Select a category → request sent. Check DB: `sqlite3 data/yoklama.db "SELECT * FROM yardim_talepleri ORDER BY id DESC LIMIT 1;"` — should show `kategori` value.

- [ ] **Step 4: Commit**

```bash
git add templates/ogrenci_ana.html static/js/ogrenci.js
git commit -m "feat(student): add help category selection modal"
```

### Task 4: Teacher UI — show category in help requests list

**Files:**
- Modify: `static/js/ogretmen.js:769-826` (yardimTalepleriCek function)

- [ ] **Step 1: Add category icons map and update table in `yardimTalepleriCek()`**

At the top of `yardimTalepleriCek()`, add category icon mapping. Update the table header to include "Kategori" column. Update each row to show category:

In the table header row, add after "Ad Soyad" column:
```
<th style="padding:0.5rem;text-align:left;">Kategori</th>
```

Add category icon mapping inside the function:
```javascript
const katIkon = {
  'komut': '🔧',
  'dosya': '📁',
  'terminal': '💻',
  'soru': '❓',
  'diger': '📋'
};
```

In each row, add after `ad_soyad` cell:
```javascript
<td style="padding:0.5rem;">
  <span style="background:#1a202c; padding:2px 8px; border-radius:4px; font-size:0.8rem;">
    ${katIkon[t.kategori] || '📋'} ${t.kategori || 'belirsiz'}
  </span>
</td>
```

- [ ] **Step 2: Test manually**

Login as teacher, go to Yardım tab. Create a help request from student side with a category. Verify the category icon/label appears in the teacher's list.

- [ ] **Step 3: Commit**

```bash
git add static/js/ogretmen.js
git commit -m "feat(teacher): show help request categories in yardim tab"
```

---

## Chunk 2: Ogrenci Devam Goruntuleleme

### Task 5: Add student attendance API endpoint

**Files:**
- Modify: `routes/api.py` (add new endpoint)

- [ ] **Step 1: Add `/api/ogrenci/devam` endpoint**

Add after the existing student-facing endpoints (near `/api/ogrenci_listesi`):

```python
@api_bp.route('/ogrenci/devam')
def api_ogrenci_devam():
    """Öğrencinin kendi devam durumunu görmesi."""
    from flask import session
    numara = session.get('numara')
    if not numara:
        return jsonify({'durum': 'hata', 'mesaj': 'Oturum yok'}), 401

    with db_baglantisi() as db:
        # Bu öğrencinin tüm yoklama kayıtları
        katilimlar = db.execute(
            'SELECT DISTINCT tarih, paket FROM yoklama WHERE numara=? ORDER BY tarih DESC',
            (numara,)
        ).fetchall()

        # Tüm ders günleri (herhangi birinin yoklaması olan günler)
        tum_gunler = db.execute(
            'SELECT DISTINCT tarih FROM yoklama ORDER BY tarih DESC'
        ).fetchall()

    katilim_set = {(r['tarih'], r['paket']) for r in katilimlar}
    katilim_tarihleri = {r['tarih'] for r in katilimlar}
    tum_tarihler = [r['tarih'] for r in tum_gunler]

    gecmis = []
    for tarih in tum_tarihler:
        if tarih in katilim_tarihleri:
            for k in katilimlar:
                if k['tarih'] == tarih:
                    gecmis.append({'tarih': tarih, 'paket': k['paket'], 'durum': 'geldi'})
        else:
            gecmis.append({'tarih': tarih, 'paket': '-', 'durum': 'gelmedi'})

    toplam = len(tum_tarihler)
    katilim = len(katilim_tarihleri)
    devamsizlik = toplam - katilim
    yuzde = round((katilim / toplam * 100)) if toplam > 0 else 0

    return jsonify({
        'ozet': {
            'toplam_ders': toplam,
            'katilim': katilim,
            'devamsizlik': devamsizlik,
            'yuzde': yuzde
        },
        'gecmis': gecmis
    })
```

- [ ] **Step 2: Test endpoint**

Start server, login as student, then: `curl -b <cookie> http://localhost:3333/api/ogrenci/devam` — should return JSON with ozet and gecmis.

- [ ] **Step 3: Commit**

```bash
git add routes/api.py
git commit -m "feat(api): add student attendance history endpoint"
```

### Task 6: Student UI — attendance display on waiting screen

**Files:**
- Modify: `templates/ogrenci_ana.html` (add attendance section)
- Modify: `static/js/ogrenci.js` (add attendance fetch and render)

- [ ] **Step 1: Add attendance section to `ogrenci_ana.html`**

In the `bekleme-ekrani` div (after the "Öğretmen girişini bekleyiniz..." paragraph), add:

```html
<!-- Devam Durumu -->
<div id="devam-ozet" style="margin-top:1.5rem; background:#2d3748; border-radius:8px; padding:1rem; display:none;">
  <div id="devam-ozet-metin" style="font-size:1.1rem; font-weight:bold; text-align:center;"></div>
  <button onclick="devamDetayToggle()" style="margin-top:0.75rem; background:transparent; border:1px solid #4a5568; color:#90cdf4; padding:0.4rem 1rem; border-radius:6px; cursor:pointer; width:100%; font-size:0.85rem;">
    📋 Devam Detaylarım
  </button>
  <div id="devam-detay" style="display:none; margin-top:0.75rem; max-height:200px; overflow-y:auto;">
    <table id="devam-tablo" style="width:100%; font-size:0.8rem; border-collapse:collapse;">
    </table>
  </div>
</div>
```

- [ ] **Step 2: Add attendance fetch and render in `ogrenci.js`**

Add before the `durumKontrol()` function:

```javascript
async function devamBilgisiCek() {
  try {
    const yanit = await fetch('/api/ogrenci/devam', { credentials: 'same-origin' });
    if (!yanit.ok) return;
    const veri = await yanit.json();

    const ozet = document.getElementById('devam-ozet');
    const metin = document.getElementById('devam-ozet-metin');
    const tablo = document.getElementById('devam-tablo');
    if (!ozet || !metin) return;

    // Özet göster
    const y = veri.ozet.yuzde;
    let renk = '#48bb78'; // yeşil
    if (y < 50) renk = '#e53e3e'; // kırmızı
    else if (y < 70) renk = '#ed8936'; // turuncu

    metin.style.color = renk;
    metin.textContent = veri.ozet.katilim + '/' + veri.ozet.toplam_ders + ' derse katıldınız (%' + veri.ozet.yuzde + ')';
    ozet.style.display = 'block';

    // Tablo oluştur
    if (tablo && veri.gecmis) {
      tablo.textContent = '';
      const thead = document.createElement('tr');
      thead.style.borderBottom = '1px solid #4a5568';
      ['Tarih', 'Paket', 'Durum'].forEach(function(baslik) {
        const th = document.createElement('th');
        th.style.padding = '4px 8px';
        th.style.textAlign = 'left';
        th.style.color = '#a0aec0';
        th.textContent = baslik;
        thead.appendChild(th);
      });
      tablo.appendChild(thead);

      veri.gecmis.forEach(function(g) {
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid #2d3748';

        const tdTarih = document.createElement('td');
        tdTarih.style.padding = '4px 8px';
        tdTarih.textContent = g.tarih;
        tr.appendChild(tdTarih);

        const tdPaket = document.createElement('td');
        tdPaket.style.padding = '4px 8px';
        tdPaket.textContent = g.paket;
        tr.appendChild(tdPaket);

        const tdDurum = document.createElement('td');
        tdDurum.style.padding = '4px 8px';
        tdDurum.textContent = g.durum === 'geldi' ? '✅ Geldi' : '❌ Gelmedi';
        tdDurum.style.color = g.durum === 'geldi' ? '#48bb78' : '#e53e3e';
        tr.appendChild(tdDurum);

        tablo.appendChild(tr);
      });
    }
  } catch (e) {
    console.error('[Devam] Hata:', e);
  }
}

function devamDetayToggle() {
  const detay = document.getElementById('devam-detay');
  if (detay) {
    detay.style.display = detay.style.display === 'none' ? 'block' : 'none';
  }
}
```

In the `DOMContentLoaded` block, add `devamBilgisiCek();` call.

- [ ] **Step 3: Test manually**

Login as student with attendance history. Waiting screen should show "X/Y derse katıldınız (%Z)". Click "Devam Detaylarım" to toggle the history table.

- [ ] **Step 4: Commit**

```bash
git add templates/ogrenci_ana.html static/js/ogrenci.js routes/api.py
git commit -m "feat(student): add attendance summary and history on waiting screen"
```

---

## Chunk 3: Yoklama Raporlama (Ogretmen)

### Task 7: Add attendance report API endpoint

**Files:**
- Modify: `routes/api.py` (add new endpoint)

- [ ] **Step 1: Add `/api/yoklama/rapor` endpoint**

```python
@api_bp.route('/yoklama/rapor')
@ogretmen_giris_gerekli
def api_yoklama_rapor():
    """Öğrenci bazında devam raporu matrisi."""
    sinif_id = request.args.get('sinif_id', '')
    baslangic = request.args.get('baslangic', '')
    bitis = request.args.get('bitis', '')
    paket = request.args.get('paket', '')

    with db_baglantisi() as db:
        # Tarih filtrelemeli ders günleri
        tarih_sql = 'SELECT DISTINCT tarih FROM yoklama WHERE 1=1'
        tarih_params = []
        if baslangic:
            tarih_sql += ' AND tarih >= ?'
            tarih_params.append(baslangic)
        if bitis:
            tarih_sql += ' AND tarih <= ?'
            tarih_params.append(bitis)
        if paket:
            tarih_sql += ' AND paket = ?'
            tarih_params.append(paket)
        tarih_sql += ' ORDER BY tarih'
        ders_gunleri = [r['tarih'] for r in db.execute(tarih_sql, tarih_params).fetchall()]

        # Öğrenci listesi (sınıf filtreli)
        if sinif_id:
            ogrenciler = db.execute(
                'SELECT numara, ad, soyad FROM ogrenciler WHERE sinif_id=? ORDER BY soyad, ad',
                (sinif_id,)
            ).fetchall()
        else:
            ogrenciler = db.execute(
                'SELECT numara, ad, soyad FROM ogrenciler ORDER BY soyad, ad'
            ).fetchall()

        # Yoklama verileri — hangi öğrenci hangi gün gelmiş
        yoklama_sql = 'SELECT DISTINCT numara, tarih FROM yoklama WHERE 1=1'
        yoklama_params = []
        if baslangic:
            yoklama_sql += ' AND tarih >= ?'
            yoklama_params.append(baslangic)
        if bitis:
            yoklama_sql += ' AND tarih <= ?'
            yoklama_params.append(bitis)
        if paket:
            yoklama_sql += ' AND paket = ?'
            yoklama_params.append(paket)
        yoklama_kayitlari = db.execute(yoklama_sql, yoklama_params).fetchall()

        # Devamsızlık eşiği
        esik = int(db.execute("SELECT deger FROM ayarlar WHERE anahtar='devamsizlik_esik'").fetchone()['deger']) if db.execute("SELECT deger FROM ayarlar WHERE anahtar='devamsizlik_esik'").fetchone() else 3

    # Set oluştur: {(numara, tarih)}
    katilim_set = {(r['numara'], r['tarih']) for r in yoklama_kayitlari}
    toplam_ders = len(ders_gunleri)

    rapor = []
    for o in ogrenciler:
        katilim = sum(1 for t in ders_gunleri if (o['numara'], t) in katilim_set)
        devamsizlik = toplam_ders - katilim
        yuzde = round((katilim / toplam_ders * 100)) if toplam_ders > 0 else 0
        gunler = {}
        for t in ders_gunleri:
            gunler[t] = 'geldi' if (o['numara'], t) in katilim_set else 'gelmedi'

        rapor.append({
            'numara': o['numara'],
            'ad_soyad': o['ad'] + ' ' + o['soyad'],
            'katilim': katilim,
            'devamsizlik': devamsizlik,
            'yuzde': yuzde,
            'uyari': devamsizlik >= esik,
            'gunler': gunler
        })

    return jsonify({
        'tarihler': ders_gunleri,
        'toplam_ders': toplam_ders,
        'esik': esik,
        'rapor': rapor
    })
```

- [ ] **Step 2: Add devamsizlik_esik endpoints**

```python
@api_bp.route('/yoklama/devamsizlik_esik', methods=['GET'])
@ogretmen_giris_gerekli
def api_devamsizlik_esik_getir():
    from core.config import ayar_getir
    esik = ayar_getir('devamsizlik_esik', '3')
    return jsonify({'esik': int(esik)})

@api_bp.route('/yoklama/devamsizlik_esik', methods=['POST'])
@ogretmen_giris_gerekli
def api_devamsizlik_esik_kaydet():
    veri = request.get_json()
    esik = veri.get('esik', 3)
    from core.config import ayar_kaydet
    ayar_kaydet('devamsizlik_esik', str(esik))
    return jsonify({'durum': 'ok', 'esik': int(esik)})
```

- [ ] **Step 3: Commit**

```bash
git add routes/api.py
git commit -m "feat(api): add attendance report and absence threshold endpoints"
```

### Task 8: Teacher UI — attendance report tab

**Files:**
- Modify: `templates/ogretmen.html` (add tab button + tab content)
- Modify: `static/js/ogretmen.js` (add report fetch and render logic)

- [ ] **Step 1: Add "Devam Raporu" tab button in `ogretmen.html`**

In the tab menu (after the "Arşiv" button, before "Sınavlar"), add:

```html
<button class="tab-btn" onclick="tabGec('devam_raporu', this); devamRaporuCek();">📊 Devam Raporu</button>
```

- [ ] **Step 2: Add tab content HTML**

After the "Arşiv" tab content div, add:

```html
<!-- Devam Raporu -->
<div id="tab-devam_raporu" class="panel-bolum">
  <div class="kutu-baslik">
    <h3>📊 Devam Raporu</h3>
  </div>
  <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1rem;">
    <select id="rapor-sinif" style="padding:0.3rem 0.5rem;background:#2d3748;color:#e2e8f0;border:1px solid #4a5568;border-radius:6px;font-size:0.85rem;">
      <option value="">Tüm Sınıflar</option>
    </select>
    <input type="date" id="rapor-baslangic" style="padding:0.3rem 0.5rem;background:#2d3748;color:#e2e8f0;border:1px solid #4a5568;border-radius:6px;font-size:0.85rem;">
    <input type="date" id="rapor-bitis" style="padding:0.3rem 0.5rem;background:#2d3748;color:#e2e8f0;border:1px solid #4a5568;border-radius:6px;font-size:0.85rem;">
    <button onclick="devamRaporuCek()" class="btn-kucuk" style="background:#2b6cb0;">Filtrele</button>
    <button onclick="devamRaporuCSV()" class="btn-kucuk yeşil">📥 CSV</button>
  </div>
  <div id="devam-raporu-icerik" style="overflow-x:auto;">
    <div style="color:#718096; text-align:center; padding:2rem;">Yükleniyor...</div>
  </div>
</div>
```

- [ ] **Step 3: Add devamRaporuCek() in `ogretmen.js`**

```javascript
async function devamRaporuCek() {
  try {
    // Sınıf dropdown'ını doldur (ilk sefer)
    const sinifSelect = document.getElementById('rapor-sinif');
    if (sinifSelect && sinifSelect.options.length <= 1) {
      const sRes = await safeFetch('/api/siniflar');
      const sVeri = await sRes.json();
      sVeri.siniflar.forEach(function(s) {
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = s.ad;
        sinifSelect.appendChild(opt);
      });
    }

    const sinifId = document.getElementById('rapor-sinif')?.value || '';
    const baslangic = document.getElementById('rapor-baslangic')?.value || '';
    const bitis = document.getElementById('rapor-bitis')?.value || '';

    let url = '/api/yoklama/rapor?';
    if (sinifId) url += 'sinif_id=' + sinifId + '&';
    if (baslangic) url += 'baslangic=' + baslangic + '&';
    if (bitis) url += 'bitis=' + bitis + '&';

    const yanit = await safeFetch(url);
    const veri = await yanit.json();
    const div = document.getElementById('devam-raporu-icerik');
    if (!div) return;

    if (!veri.rapor || veri.rapor.length === 0) {
      div.textContent = 'Kayıt bulunamadı.';
      return;
    }

    // Tablo oluştur
    const tablo = document.createElement('table');
    tablo.style.cssText = 'width:100%; border-collapse:collapse; font-size:0.8rem;';

    // Header
    const thead = document.createElement('tr');
    thead.style.borderBottom = '2px solid #4a5568';
    ['Öğrenci', '%'].concat(veri.tarihler.map(function(t) { return t.substring(5); })).forEach(function(h) {
      const th = document.createElement('th');
      th.style.cssText = 'padding:4px 6px; text-align:center; color:#a0aec0; white-space:nowrap;';
      th.textContent = h;
      thead.appendChild(th);
    });
    tablo.appendChild(thead);

    // Rows
    veri.rapor.forEach(function(o) {
      const tr = document.createElement('tr');
      tr.style.borderBottom = '1px solid #2d3748';
      if (o.uyari) tr.style.background = 'rgba(229,62,62,0.15)';

      const tdAd = document.createElement('td');
      tdAd.style.cssText = 'padding:4px 6px; white-space:nowrap;';
      tdAd.textContent = o.ad_soyad;
      if (o.uyari) tdAd.style.color = '#fc8181';
      tr.appendChild(tdAd);

      const tdPct = document.createElement('td');
      tdPct.style.cssText = 'padding:4px 6px; text-align:center; font-weight:bold;';
      tdPct.textContent = '%' + o.yuzde;
      tdPct.style.color = o.yuzde >= 70 ? '#48bb78' : (o.yuzde >= 50 ? '#ed8936' : '#e53e3e');
      tr.appendChild(tdPct);

      veri.tarihler.forEach(function(t) {
        const td = document.createElement('td');
        td.style.cssText = 'padding:4px 6px; text-align:center;';
        if (o.gunler[t] === 'geldi') {
          td.textContent = '✅';
        } else {
          td.textContent = '❌';
        }
        tr.appendChild(td);
      });

      tablo.appendChild(tr);
    });

    div.textContent = '';
    div.appendChild(tablo);
  } catch (e) {
    console.error('Devam raporu hatası:', e);
  }
}

async function devamRaporuCSV() {
  const sinifId = document.getElementById('rapor-sinif')?.value || '';
  const baslangic = document.getElementById('rapor-baslangic')?.value || '';
  const bitis = document.getElementById('rapor-bitis')?.value || '';
  let url = '/api/yoklama/rapor?';
  if (sinifId) url += 'sinif_id=' + sinifId + '&';
  if (baslangic) url += 'baslangic=' + baslangic + '&';
  if (bitis) url += 'bitis=' + bitis + '&';

  const yanit = await safeFetch(url);
  const veri = await yanit.json();
  if (!veri.rapor) return;

  let csv = 'Öğrenci,Numara,Katılım,Devamsızlık,%,' + veri.tarihler.join(',') + '\n';
  veri.rapor.forEach(function(o) {
    let satir = '"' + o.ad_soyad + '",' + o.numara + ',' + o.katilim + ',' + o.devamsizlik + ',' + o.yuzde;
    veri.tarihler.forEach(function(t) {
      satir += ',' + (o.gunler[t] === 'geldi' ? '1' : '0');
    });
    csv += satir + '\n';
  });

  const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'devam_raporu.csv';
  a.click();
}
```

- [ ] **Step 4: Add devamsizlik_esik input to Ayarlar tab**

In the Ayarlar section of `ogretmen.html`, add:

```html
<div class="form-grup">
  <label>Devamsızlık Uyarı Eşiği</label>
  <input type="number" id="config-devamsizlik-esik" min="1" max="30" value="3"
    style="width:80px; padding:0.5rem; background:#2d3748; color:#e2e8f0; border:1px solid #4a5568; border-radius:6px;">
  <span style="color:#718096; font-size:0.8rem; margin-left:0.5rem;">ders (bu kadar veya daha fazla gelmeyenler uyarılır)</span>
</div>
```

Add loading and saving of this value in `ayarlariKaydet()` and the config loading function in `ogretmen.js`.

- [ ] **Step 5: Test manually**

Go to teacher panel → "Devam Raporu" tab. Filter by class, date range. Verify the matrix table shows correctly. Export CSV.

- [ ] **Step 6: Commit**

```bash
git add templates/ogretmen.html static/js/ogretmen.js routes/api.py
git commit -m "feat(teacher): add attendance report tab with matrix view and CSV export"
```

---

## Chunk 4: Terminal Izleme ve Mudahale

### Task 9: Add active terminal sessions API

**Files:**
- Modify: `routes/api.py` (add new endpoint)
- Modify: `app.py` (expose ogrenci_sidleri and ogrenci_surecleri for API)

- [ ] **Step 1: Add `/api/terminal/aktif_oturumlar` endpoint in `routes/api.py`**

```python
@api_bp.route('/terminal/aktif_oturumlar')
@ogretmen_giris_gerekli
def api_terminal_aktif_oturumlar():
    """Aktif terminal oturumlarının listesi."""
    try:
        from app import ogrenci_sidleri, ogrenci_surecleri
        import time
        oturumlar = []
        for sid, username in ogrenci_sidleri.items():
            oturumlar.append({
                'sid': sid,
                'username': username,
                'aktif': sid in ogrenci_surecleri
            })
        return jsonify({'oturumlar': oturumlar})
    except Exception as e:
        return jsonify({'oturumlar': [], 'hata': str(e)})
```

- [ ] **Step 2: Commit**

```bash
git add routes/api.py
git commit -m "feat(api): add active terminal sessions endpoint"
```

### Task 10: Add Socket.IO events for terminal monitoring

**Files:**
- Modify: `app.py` (add 3 new socket events + monitoring relay)

- [ ] **Step 1: Add monitoring state variables in `app.py`**

After the existing `ogretmen_komut_tampon` variable, add:

```python
ogretmen_izlenen_sid = None  # Öğretmenin şu an izlediği öğrenci SID'i
ogretmen_mudahale = False     # Müdahale modu açık mı
```

- [ ] **Step 2: Add `ogretmen_izle` event**

```python
@socketio.on('ogretmen_izle', namespace='/terminal')
def ogretmen_izle_event(veri):
    global ogretmen_izlenen_sid, ogretmen_mudahale
    if request.sid != ogretmen_sid:
        return

    username = veri.get('username', '')
    # SID'i bul
    hedef_sid = None
    for sid, uname in ogrenci_sidleri.items():
        if uname == username:
            hedef_sid = sid
            break

    if not hedef_sid or hedef_sid not in ogrenci_surecleri:
        emit('izleme_hata', 'Bu öğrencinin aktif terminali yok')
        return

    ogretmen_izlenen_sid = hedef_sid
    ogretmen_mudahale = False
    emit('izleme_basladi', {'username': username, 'sid': hedef_sid})
    log.info(f"Öğretmen izleme başladı: {username}")
```

- [ ] **Step 3: Add `ogretmen_izle_girdi` event**

```python
@socketio.on('ogretmen_izle_girdi', namespace='/terminal')
def ogretmen_izle_girdi_event(veri):
    global ogretmen_mudahale
    if request.sid != ogretmen_sid or not ogretmen_izlenen_sid:
        return
    if not ogretmen_mudahale:
        return  # Read-only modda yazma yok

    if ogretmen_izlenen_sid in ogrenci_surecleri:
        _, fd = ogrenci_surecleri[ogretmen_izlenen_sid]
        lock = ogrenci_pty_locks.get(fd)
        data = veri.get('data', '')
        if lock:
            with lock:
                try: os.write(fd, data.encode('utf-8'))
                except OSError: pass
        else:
            try: os.write(fd, data.encode('utf-8'))
            except OSError: pass
```

- [ ] **Step 4: Add `ogretmen_izle_birak` and `ogretmen_mudahale_toggle` events**

```python
@socketio.on('ogretmen_izle_birak', namespace='/terminal')
def ogretmen_izle_birak_event():
    global ogretmen_izlenen_sid, ogretmen_mudahale
    if request.sid != ogretmen_sid:
        return
    log.info(f"Öğretmen izleme bıraktı")
    ogretmen_izlenen_sid = None
    ogretmen_mudahale = False

@socketio.on('ogretmen_mudahale_toggle', namespace='/terminal')
def ogretmen_mudahale_toggle_event(veri):
    global ogretmen_mudahale
    if request.sid != ogretmen_sid:
        return
    ogretmen_mudahale = veri.get('aktif', False)
    log.info(f"Öğretmen müdahale modu: {'açık' if ogretmen_mudahale else 'kapalı'}")
```

- [ ] **Step 5: Modify `_pty_oku_ve_yayinla` to also relay to monitoring teacher**

In the existing `_pty_oku_ve_yayinla` function, after the existing emit logic, add a check to relay to the monitoring teacher:

```python
# İzleme relay: Eğer bu fd izlenen öğrenciye aitse, öğretmene de gönder
if ogretmen_izlenen_sid and hedef_room == ogretmen_izlenen_sid and ogretmen_sid:
    socketio.emit('izleme_cikti', text, room=ogretmen_sid, namespace='/terminal')
```

This needs to be added inside the `elif hedef_room:` block, after the student emit.

- [ ] **Step 6: Commit**

```bash
git add app.py
git commit -m "feat(terminal): add teacher monitoring and intervention socket events"
```

### Task 11: Teacher terminal UI — monitoring panel

**Files:**
- Modify: `templates/ogretmen_terminal.html` (add monitoring panel)

- [ ] **Step 1: Add monitoring panel to teacher terminal page**

Add after the existing terminal container, a side panel with:
- Active sessions list (fetched from `/api/terminal/aktif_oturumlar`)
- An xterm.js instance for monitoring (read-only by default)
- "Müdahale Et" toggle button
- "Bırak" button to stop monitoring
- Color-coded border: blue=monitoring, orange=intervention

The monitoring xterm listens for `izleme_cikti` events and displays them. When `ogretmen_mudahale` is toggled on, keystrokes from the monitoring xterm are sent via `ogretmen_izle_girdi`.

- [ ] **Step 2: Add JS logic for monitoring**

```javascript
let izlemeTerminal = null;
let izlemeAktif = false;
let mudahaleAktif = false;

function ogrenciListesiGuncelle() {
  fetch('/api/terminal/aktif_oturumlar')
    .then(r => r.json())
    .then(veri => {
      const liste = document.getElementById('izleme-ogrenci-listesi');
      if (!liste) return;
      liste.textContent = '';
      veri.oturumlar.forEach(function(o) {
        const btn = document.createElement('button');
        btn.textContent = o.username;
        btn.style.cssText = 'display:block; width:100%; text-align:left; padding:6px 10px; margin-bottom:4px; background:#1a202c; border:1px solid #4a5568; color:#e2e8f0; border-radius:6px; cursor:pointer;';
        btn.onclick = function() { izlemeBaslat(o.username); };
        liste.appendChild(btn);
      });
    });
}

function izlemeBaslat(username) {
  if (izlemeTerminal) izlemeTerminal.clear();
  socket.emit('ogretmen_izle', { username: username });
  izlemeAktif = true;
  document.getElementById('izleme-durum').textContent = 'İzleniyor: ' + username;
  document.getElementById('izleme-panel').style.borderColor = '#3182ce';
}

function izlemeBirak() {
  socket.emit('ogretmen_izle_birak');
  izlemeAktif = false;
  mudahaleAktif = false;
  document.getElementById('izleme-durum').textContent = 'İzleme kapalı';
  document.getElementById('izleme-panel').style.borderColor = '#4a5568';
}

function mudahaleToggle() {
  mudahaleAktif = !mudahaleAktif;
  socket.emit('ogretmen_mudahale_toggle', { aktif: mudahaleAktif });
  document.getElementById('izleme-panel').style.borderColor = mudahaleAktif ? '#ed8936' : '#3182ce';
  document.getElementById('mudahale-btn').textContent = mudahaleAktif ? '🔴 Müdahale Kapat' : '🟢 Müdahale Et';
}

// Socket events
socket.on('izleme_cikti', function(data) {
  if (izlemeTerminal) izlemeTerminal.write(data);
});

socket.on('izleme_hata', function(msg) {
  alert('İzleme hatası: ' + msg);
});
```

- [ ] **Step 3: Test manually**

1. Login as student, connect to terminal
2. Login as teacher, go to terminal page
3. See student in active sessions list
4. Click student → monitoring xterm shows their terminal
5. Toggle "Müdahale Et" → type commands that execute in student's terminal
6. Click "Bırak" → monitoring stops

- [ ] **Step 4: Commit**

```bash
git add templates/ogretmen_terminal.html static/js/ogretmen.js app.py
git commit -m "feat(teacher): add terminal monitoring and intervention UI"
```

---

## Final Verification

- [ ] **Step 1: Full integration test**

1. Start server: `python app.py`
2. Login as student → verify attendance summary shows on waiting screen
3. Click "Yardım İste" → verify category modal appears → select category → verify sent
4. Login as teacher → Yardım tab → verify category shown
5. Devam Raporu tab → verify matrix, filter by class, export CSV
6. Terminal page → verify student monitoring and intervention works

- [ ] **Step 2: Final commit**

```bash
git add -A
git commit -m "feat: complete teacher panel improvements (attendance, help categories, terminal monitoring)"
git push origin main
```
