// Menu HP + tombol salin tautan pada halaman artikel
const t = document.querySelector('.menu-toggle'), m = document.querySelector('#menu');
t.addEventListener('click', () => { const o = m.classList.toggle('open'); t.setAttribute('aria-expanded', o); });
m.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { m.classList.remove('open'); t.setAttribute('aria-expanded', false); }));
const tt = s => (window.CM ? CM.t(s) : s);   // terjemahan sesuai bahasa yang dipilih
const c = document.querySelector('#copy-link');
if (c) c.addEventListener('click', async () => {
  const file = location.protocol === 'file:';
  const url = file ? c.dataset.url : location.href.split('#')[0];
  let ok = true;
  try { await navigator.clipboard.writeText(url); } catch { ok = false; prompt(tt('Salin tautan artikel:'), url); }
  if (ok) {
    c.textContent = tt(file ? 'Tautan disalin (aktif setelah website online)' : 'Tautan disalin');
    setTimeout(() => { c.textContent = tt('Salin tautan'); }, 2600);
  }
});
