/* ===== Tombol WhatsApp melayang di pojok kanan bawah (semua halaman) =====
   Cara memasang: salin SELURUH isi file ini ke paling bawah js/prefs.js (setelah baris terakhir).
   Karena prefs.js sudah dipakai semua halaman (beranda, produk, detail produk, artikel, kontak), tombolnya otomatis muncul di semua halaman.
   Klik tombol = langsung membuka WhatsApp ke nomor di bawah dengan pesan awal yang sudah terisi. */
(function () {
  var NOMOR_WA = '628113301819';      // GANTI di sini: kode negara 62 + nomor tanpa 0 di depan, tanpa spasi, tanda + atau tanda hubung
  if (!NOMOR_WA || document.querySelector('.wa-fab')) return;

  var TEKS = {
    id: { label: 'Chat WhatsApp', aria: 'Chat dengan kami lewat WhatsApp', pesan: 'Halo CV Cahaya Mustika, saya ingin bertanya tentang lemari arsip.', halaman: 'Saya sedang melihat halaman: ' },
    en: { label: 'Chat on WhatsApp', aria: 'Chat with us on WhatsApp', pesan: 'Hello CV Cahaya Mustika, I would like to ask about filing cabinets.', halaman: 'I am viewing the page: ' }
  };

  // gaya tombol (disisipkan lewat skrip, tidak perlu mengubah CSS)
  var css = document.createElement('style');
  css.textContent =
    '.wa-fab{position:fixed;z-index:90;right:22px;bottom:calc(22px + env(safe-area-inset-bottom,0px));display:flex;align-items:center;gap:0;height:58px;min-width:58px;padding:0 16px;border-radius:999px;background:#25d366;color:#fff;text-decoration:none;font-family:"Poppins",sans-serif;font-size:.9rem;font-weight:500;box-shadow:0 12px 28px rgba(7,94,84,.38);transition:transform .25s,box-shadow .25s,background .25s}' +
    '.wa-fab:hover,.wa-fab:focus-visible{background:#1ebe5b;transform:translateY(-3px);box-shadow:0 18px 34px rgba(7,94,84,.45)}' +
    '.wa-fab:focus-visible{outline:3px solid #fff;outline-offset:3px;box-shadow:0 0 0 6px #25d366}' +
    '.wa-fab svg{width:28px;height:28px;flex:none;fill:#fff}' +
    '.wa-fab span{max-width:0;overflow:hidden;white-space:nowrap;opacity:0;transition:max-width .3s ease,opacity .25s,margin .3s}' +
    '.wa-fab:hover span,.wa-fab:focus-visible span{max-width:190px;opacity:1;margin-left:10px}' +
    '@media(prefers-reduced-motion:no-preference){.wa-fab::before{content:"";position:absolute;inset:0;border-radius:inherit;border:2px solid #25d366;animation:wa-ring 2.6s ease-out infinite;pointer-events:none}@keyframes wa-ring{0%{transform:scale(1);opacity:.7}70%,100%{transform:scale(1.5);opacity:0}}}' +
    '@media(max-width:600px){.wa-fab{right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));height:54px;min-width:54px;padding:0 13px}.wa-fab span{display:none}}' +
    '@media print{.wa-fab{display:none}}';
  document.head.appendChild(css);

  // tombolnya
  var a = document.createElement('a');
  a.className = 'wa-fab'; a.target = '_blank'; a.rel = 'noopener';
  a.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg><span></span>';
  document.body.appendChild(a);

  // teks dan tautan mengikuti bahasa yang dipilih (ID atau EN) dan judul halaman yang sedang dibuka
  function muat() {
    var t = TEKS[document.documentElement.lang === 'en' ? 'en' : 'id'];
    var judul = (document.title || '').split(' | ')[0];
    var pesan = t.pesan + (judul ? '\n' + t.halaman + judul : '');
    a.href = 'https://wa.me/628113301819?text=LAJ-MYID%0A%0AHalo%20Cahaya%20Mustika%20Internesia%2C%20saya%20tertarik%20dengan%20produk%20Lemari%20Arsip.';
    a.setAttribute('aria-label', t.aria);
    a.querySelector('span').textContent = t.label;
  }
  muat();
  document.querySelectorAll('[data-lang]').forEach(function (b) { b.addEventListener('click', function () { setTimeout(muat, 0); }); });
})();