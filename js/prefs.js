// ===== HAPUS BAGIAN CTA BIRU "Bingung memilih merek, model, atau jumlah?" DI SEMUA HALAMAN =====
(function () {
  document.querySelectorAll('section.cta').forEach(function (e) { e.remove(); });
})();

// ===== GAYA HERO SEMUA HALAMAN =====
// Gerak zoom halus dan gaya teks hero. Foto hero tiap halaman diatur lewat atribut data-bg di HTML:
// Beranda = bg/hero-beranda.webp, Produk = bg/produk-1.jpg, Vivorti = bg/hero-vivorti.webp, Zeco = bg/hero-zeco.webp.
(function () {

  const css = document.createElement('style');
  css.textContent = `
html .hero[data-bg] .bg-slides,html .a-hero[data-bg] .bg-slides{background:#e8f1ff}
html .hero[data-bg] .bg-slides span,html .a-hero[data-bg] .bg-slides span{
  background-size:cover;background-position:right center;
  filter:brightness(1.35) saturate(1.1) contrast(.95);transform:scale(1.02);
  animation:cmHeroZoom 22s ease-in-out infinite alternate}
@keyframes cmHeroZoom{from{transform:scale(1.02)}to{transform:scale(1.08)}}
@media(prefers-reduced-motion:reduce){html .hero[data-bg] .bg-slides span,html .a-hero[data-bg] .bg-slides span{animation:none}}
html .hero[data-bg]::before,html .hero.home[data-bg]::before,html .a-hero[data-bg]::before{
  background:
    linear-gradient(90deg,rgba(54,124,230,.80) 0%,rgba(84,148,240,.58) 42%,rgba(150,195,250,.10) 100%),
    linear-gradient(0deg,rgba(235,244,255,.55) 0%,transparent 38%)}
html .hero[data-bg] h1,html .a-hero[data-bg] h1{color:#fff;text-shadow:0 2px 16px rgba(25,70,160,.35)}
html .hero[data-bg] p,html .a-hero[data-bg] .meta{color:#fff;text-shadow:0 1px 12px rgba(25,70,160,.35)}
html .hero[data-bg] .btn-ghost{background:rgba(255,255,255,.14);box-shadow:inset 0 0 0 1px rgba(255,255,255,.7)}
html .hero[data-bg] .btn-ghost:hover{background:#fff;color:#367ce6}
html .a-hero[data-bg]{border-bottom:2px solid #c8a96a}
html .a-hero[data-bg] .crumbs,html .a-hero[data-bg] .crumbs a{color:#fff}
html .a-hero[data-bg] .crumbs span{opacity:.8}
html .a-hero[data-bg] .tag{color:#fff;border-color:rgba(255,255,255,.8);background:rgba(255,255,255,.14)}
@media(max-width:900px){
  html .hero[data-bg] .bg-slides span,html .a-hero[data-bg] .bg-slides span{background-position:78% center}
  html .hero[data-bg]::before,html .hero.home[data-bg]::before,html .a-hero[data-bg]::before{
    background:linear-gradient(180deg,rgba(54,124,230,.78),rgba(110,166,244,.60))}
}`;
  document.head.appendChild(css);
  // Foto hero TIDAK lagi diseragamkan: tiap halaman memakai fotonya sendiri dari atribut data-bg di HTML.
})();

// ===== FOOTER SEMUA HALAMAN =====
// Tiga kolom: perusahaan (logo + deskripsi), Informasi Perusahaan, Kontak Kami.
// Kolom "Informasi Perusahaan" DIAMBIL OTOMATIS dari menu di header halaman yang sama,
// jadi kalau menu header diubah, footer ikut berubah. Nomor WhatsApp dan alamat diubah di DATA KONTAK.
(function () {
  const f = document.querySelector('footer.footer');
  if (!f) return;

  // ---- DATA KONTAK (ubah di sini) ----
  const WA_TAMPIL = '0811-330-1819', WA_URL = 'https://wa.me/628113301819?text=LAJ-MYID%0A%0AHalo%20Cahaya%20Mustika%20Internesia%2C%20saya%20tertarik%20dengan%20produk%20Lemari%20Arsip.';
  const ALAMAT = 'Jl. Penjernihan II No.7, RT.11/RW.6, Bend. Hilir, Kecamatan Tanah Abang, Kota Jakarta Pusat, Daerah Khusus Ibukota Jakarta 10210';
  const ALAMAT_SINGKAT = 'Jl. Penjernihan II No.7, Bend. Hilir, Tanah Abang, Jakarta Pusat 10210';
  // ------------------------------------

  const home = f.querySelector('a.brand, a[href$="index.html"]');
  const p = (home && /^\.\.\//.test(home.getAttribute('href'))) ? '../' : '';
  const maps = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(ALAMAT);
  const esc = t => t.replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const tautan = a => '<a href="' + esc(a.getAttribute('href')) + '">' + esc(a.textContent.trim()) + '</a>';

  // menu dari header: tautan utama (tanpa tombol)
  const menu = document.querySelector('header .nav-menu');
  let infoLinks = '';
  if (menu) {
    [].forEach.call(menu.children, el => {
      if (el.matches('a:not(.btn)')) infoLinks += tautan(el);
      else if (el.classList.contains('dropdown')) {
        const btn = el.querySelector('.dropdown-btn');
        if (btn) infoLinks += tautan(btn);
      }
    });
  }
  if (!infoLinks) infoLinks = `<a href="${p}index.html">Beranda</a><a href="${p}produk.html">Produk</a><a href="${p}portofolio.html">Portofolio</a><a href="${p}artikel.html">Artikel</a><a href="${p}kontak.html">Kontak Kami</a>`;

  const css = document.createElement('style');
  css.textContent = `
footer.footer.ft{background:#fff;color:#5f6f88;padding:0;border-top:1px solid #e3eaf4;font-size:15px;line-height:1.6}
footer.footer.ft .ft-main{padding-top:clamp(48px,6vw,72px);padding-bottom:clamp(36px,4vw,52px)}
footer.footer.ft .ft-grid{display:grid;grid-template-columns:1.5fr 1fr 1.3fr;gap:clamp(28px,4vw,56px);align-items:start}
footer.footer.ft .ft-logo{display:inline-block}
footer.footer.ft .ft-logo img{height:56px;width:auto;display:block}
footer.footer.ft .ft-brand p{margin:16px 0 0;max-width:320px;color:#5f6f88;line-height:1.75}
footer.footer.ft h2{margin:0 0 16px;color:#0b1f4a;font:700 13px/1.3 Poppins,sans-serif;letter-spacing:.14em;text-transform:uppercase}
footer.footer.ft .ft-list a{display:block;padding:5px 0;color:#5f6f88;text-decoration:none;transition:color .2s ease}
footer.footer.ft .ft-list a:hover{color:#2f6fd6}
footer.footer.ft .ft-alamat{margin:0 0 10px;color:#5f6f88;line-height:1.7}
footer.footer.ft .ft-kontak a{color:#2f6fd6;text-decoration:none;font-weight:500}
footer.footer.ft .ft-kontak a:hover{color:#0b1f4a}
footer.footer.ft .ft-kontak .ft-telp{display:block;margin-bottom:12px;color:#0b1f4a;font:700 17px/1.3 'Manrope','Poppins',sans-serif}
footer.footer.ft .ft-bar{border-top:1px solid #e3eaf4;padding:18px 0}
footer.footer.ft .ft-bar .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 20px;color:#8a97ad;font-size:14px}
footer.footer.ft .ft-bar a{color:#5f6f88;text-decoration:none}
footer.footer.ft .ft-bar a:hover{color:#2f6fd6}
@media(max-width:900px){
  footer.footer.ft .ft-grid{grid-template-columns:1fr 1fr}
  footer.footer.ft .ft-brand{grid-column:1/-1}
}
@media(max-width:520px){
  footer.footer.ft .ft-grid{grid-template-columns:1fr;gap:32px}
  footer.footer.ft .ft-bar .wrap{justify-content:center;text-align:center}
}
`;
  document.head.appendChild(css);

  f.className = 'footer ft';
  f.innerHTML = `
<div class="wrap ft-main">
  <div class="ft-grid">
    <div class="ft-brand">
      <a class="ft-logo" href="${p}index.html" aria-label="Cahaya Mustika Internesia, beranda"><img src="${p}assets/images/LOGO CMI (1).webp" alt="Cahaya Mustika Internesia" width="219" height="56"></a>
      <p>Distributor lemari arsip merek Vivorti dan Zeco di Jakarta, melayani pengiriman ke seluruh Indonesia.</p>
    </div>
    <nav class="ft-list" aria-label="Informasi perusahaan"><h2>Informasi Perusahaan</h2>${infoLinks}</nav>
    <div class="ft-kontak"><h2>Kontak Kami</h2>
      <a class="ft-telp" href="${WA_URL}" target="_blank" rel="noopener">${WA_TAMPIL}</a>
      <p class="ft-alamat">${ALAMAT_SINGKAT}</p>
      <a href="${maps}" target="_blank" rel="noopener">Buka di Google Maps &rarr;</a>
    </div>
  </div>
</div>
<div class="ft-bar"><div class="wrap"><span>&copy; 2026 Cahaya Mustika Internesia. Semua hak dilindungi.</span><a href="#top">Kembali ke atas &uarr;</a></div></div>`;
})();

// ===== Pengaturan pengunjung: bahasa (Indonesia / Inggris) dan mode gelap / terang =====
// Dipakai di beranda dan semua halaman artikel. Pilihan pengunjung disimpan di browser (localStorage).
// Teks Indonesia di halaman dicocokkan dengan kamus (js/kamus-en.js dan js/kamus-artikel-en.js), lalu diganti.
(function () {
  const root = document.documentElement;
  const store = {
    get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  // Tombol bahasa dan mode gelap/terang sudah dihapus: website selalu berbahasa Indonesia dan bertema terang.
  try { localStorage.removeItem('cm-lang'); localStorage.removeItem('cm-theme'); } catch (e) {}
  let lang = 'id';
  const dict = () => window.KAMUS_EN || {};

  // Terjemahkan satu teks. Spasi di awal dan akhir dipertahankan. Teks gabungan ("tanggal · durasi", "judul | nama") ikut diterjemahkan per bagian.
  function tr(s) {
    const k = s.trim(), d = dict();
    if (!k) return s;
    let out = d[k], m;
    if (out == null) {
      if ((m = k.match(/^(.*?)(\s*\u2192)$/)) && d[m[1]] != null) out = d[m[1]] + m[2];
      else for (const sep of [' \u00b7 ', ' | ', ' - ']) {
        if (k.includes(sep)) {
          const p = k.split(sep);
          if (p.some(x => d[x] != null)) { out = p.map(x => (d[x] != null ? d[x] : x)).join(sep); break; }
        }
      }
    }
    return out == null ? s : s.replace(k, out);
  }
  const PREFIX = 'Produk yang dibahas: ';
  const trAttr = v => (v.startsWith(PREFIX) ? 'Products discussed: ' + tr(v.slice(PREFIX.length)) : tr(v));

  const head = { title: null, desc: null };
  function apply() {
    const en = lang === 'en';
    root.lang = en ? 'en' : 'id';
    // teks di halaman
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: n => (n.parentNode && /^(SCRIPT|STYLE|NOSCRIPT)$/.test(n.parentNode.nodeName) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT)
    });
    let n;
    while ((n = w.nextNode())) {
      if (n.__id === undefined) {
        if (!en) continue;
        const t = tr(n.nodeValue);
        if (t !== n.nodeValue) { n.__id = n.nodeValue; n.nodeValue = t; }
      } else n.nodeValue = en ? tr(n.__id) : n.__id;
    }
    // gambar (alt), kolom isian (placeholder), dan label tombol (aria-label)
    document.querySelectorAll('[alt],[placeholder],[aria-label]').forEach(el => {
      el.__a = el.__a || {};
      for (const a of ['alt', 'placeholder', 'aria-label']) {
        if (!el.hasAttribute(a)) continue;
        if (el.__a[a] === undefined) {
          if (!en) continue;
          const v = el.getAttribute(a), t = trAttr(v);
          if (t !== v) { el.__a[a] = v; el.setAttribute(a, t); }
        } else el.setAttribute(a, en ? trAttr(el.__a[a]) : el.__a[a]);
      }
    });
    // judul tab dan deskripsi
    const md = document.querySelector('meta[name="description"]');
    if (head.title === null) { head.title = document.title; head.desc = md ? md.content : ''; }
    document.title = en ? tr(head.title) : head.title;
    if (md) md.content = en ? tr(head.desc) : head.desc;
    // tombol bahasa
    document.querySelectorAll('[data-lang]').forEach(b => {
      const on = b.dataset.lang === lang;
      b.classList.toggle('on', on); b.setAttribute('aria-pressed', on);
    });
  }

  function setLang(l) { lang = l === 'en' ? 'en' : 'id'; store.set('cm-lang', lang); apply(); }

  const tcolor = () => document.querySelector('meta[name="theme-color"]');
  function setTheme(t, save) {
    root.classList.add('tswap'); setTimeout(() => root.classList.remove('tswap'), 450);
    root.dataset.theme = t;
    if (save !== false) store.set('cm-theme', t);
    const m = tcolor(); if (m) m.content = t === 'dark' ? '#050d1f' : '#0b1f4a';
    document.querySelectorAll('.theme-btn').forEach(b => b.setAttribute('aria-pressed', t === 'dark'));
  }

  document.querySelectorAll('[data-lang]').forEach(b => b.addEventListener('click', () => setLang(b.dataset.lang)));
  document.querySelectorAll('.theme-btn').forEach(b => b.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark')));
  setTheme('light', false);
  apply();
  // CM.t('teks') = terjemahan teks untuk skrip lain; CM.apply() = jalankan ulang setelah halaman diubah oleh skrip
  window.CM = { get lang() { return lang; }, t: s => (lang === 'en' ? tr(s) : s), apply };
})();