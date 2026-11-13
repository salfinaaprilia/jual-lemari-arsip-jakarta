// ===== Skrip semua halaman =====
const $ = s => document.querySelector(s);
const toggle = $('.menu-toggle'), menu = $('#menu'), nav = $('.navbar');

// Tombol menu (tiga garis) di HP: buka dan tutup menu
toggle.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  toggle.setAttribute('aria-expanded', open);
});
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  menu.classList.remove('open'); toggle.setAttribute('aria-expanded', false);
}));
// Header berubah jadi putih setelah halaman digulir sedikit
const gulir = () => nav.classList.toggle('scrolled', scrollY > 10);
addEventListener('scroll', gulir, {passive: true}); requestAnimationFrame(gulir);

// ===== Daftar artikel (halaman artikel.html) =====
// Sumber data: js/articles.js. Semua artikel tampil sebagai kartu seragam, urut dari yang terbaru. Tiap kartu menuju artikel/slug.html
if ($('#article-list')) {
  ARTICLES.sort((a, b) => b.iso.localeCompare(a.iso));
  const list = $('#article-list');
  // Tautan lama berbentuk #artikel/slug dialihkan ke halaman artikelnya
  const alihkan = () => { const m = location.hash.match(/^#artikel\/(.+)$/); if (m) location.replace(`artikel/${decodeURIComponent(m[1])}.html`); };
  alihkan(); addEventListener('hashchange', alihkan);
  // Foto produk untuk tiap kode produk (sama dengan gambar di produk.html)
  const FOTO = {vf2: 'VT-SL01', vf4: 'VT-SL02G', vp2: 'VT-SLCB', vl6: 'VT-SW01 (2)', vg2: 'VT-SWCB', zs2: 'zeco-filingcabinet', zk2: 'zeco-lemarisliding', zr3: 'zeco-lemarikaca', zf3: 'zeco-lemariayun'};
  const fotoProduk = id => FOTO[id] ? `assets/images/${FOTO[id]}.webp` : '';
  // Semua artikel tampil sebagai kartu yang seragam (tanpa kartu besar "Terbaru"), urut dari yang terbaru.
  const kartu = a => {
    const fotos = (a.produk || []).slice(0, 1).map(fotoProduk).filter(Boolean);
    return `<a class="art" href="artikel/${a.slug}.html">
    <div class="cover"><span>${a.cat}</span><div class="imgs">${fotos.map(f => `<img src="${f}" alt="Produk yang dibahas: ${a.title}" loading="lazy">`).join('')}</div></div>
    <div class="body"><h2>${a.title}</h2><p>${a.excerpt}</p>
    <div class="meta"><span>${a.date} &middot; ${a.read}</span></div>
    <span class="btn btn-primary btn-sm">Baca artikel &rarr;</span></div></a>`;
  };
  // Jumlah artikel yang tampil langsung. Sisanya muncul lewat tombol "Tampilkan artikel lainnya".
  const TAMPIL = 6;
  list.innerHTML = `<div class="older">${ARTICLES.map(kartu).join('')}</div>` +
    (ARTICLES.length > TAMPIL ? '<button class="btn btn-ghost" id="more-articles" type="button">Tampilkan artikel lainnya</button>' : '');
  document.querySelectorAll('.older .art').forEach((el, i) => { if (i >= TAMPIL) el.classList.add('extra'); });
  const more = $('#more-articles');
  if (more) more.addEventListener('click', () => { $('.older').classList.add('all'); more.remove(); });
}

// ===== Formulir kontak (halaman kontak.html), dikirim lewat WhatsApp =====
const form = $('#contact-form');
if (form) {
  const WA_NUMBER = '628113301819';   // nomor WhatsApp tujuan, tanpa tanda + atau spasi
  // Tombol "Tanya harga" di halaman produk membawa nama produk lewat alamat (?produk=...)
  const dipilih = new URLSearchParams(location.search).get('produk'), sel = $('#produk-select');
  if (dipilih && sel) sel.value = dipilih;
  form.addEventListener('submit', e => {
    e.preventDefault();
    const f = new FormData(form);
    const en = window.CM && CM.lang === 'en';
    const text = en
      ? `Hello Cahaya Mustika Internesia, I am ${f.get('nama')} (${f.get('wa')}).\nI am buying as ${f.get('peran')} and am interested in ${f.get('produk')}.\n${f.get('pesan')}`
      : `Halo Cahaya Mustika Internesia, saya ${f.get('nama')} (${f.get('wa')}).\nSaya membeli sebagai ${f.get('peran')} dan tertarik dengan ${f.get('produk')}.\n${f.get('pesan')}`;
    window.open(`https://wa.me/${WA_NUMBER}?text=${encodeURIComponent('LAJ-MYID\n\n' + text)}`, '_blank');
  });
}

// Terjemahkan ulang halaman setelah kartu artikel dibuat (bila pengunjung memilih bahasa Inggris)
if (window.CM) CM.apply();