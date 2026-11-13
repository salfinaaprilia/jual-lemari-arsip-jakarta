// ===== Latar foto yang berganti =====
// Elemen dengan atribut data-bg="foto1.jpg,foto2.jpg,..." mendapat foto sebagai latar di belakang tulisannya.
// Foto pertama sudah dipasang di HTML (supaya langsung tampil); foto lainnya ditambahkan di sini lalu berganti
// secara bertahap. data-interval = jeda dalam milidetik (bawaan 7000). Cukup satu foto = tidak berganti.
(function () {
  const diam = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-bg]').forEach(el => {
    const files = el.dataset.bg.split(',').map(s => s.trim()).filter(Boolean);
    let box = el.querySelector(':scope > .bg-slides');
    if (!box) { box = document.createElement('div'); box.className = 'bg-slides'; el.prepend(box); }
    box.setAttribute('aria-hidden', 'true');
    const slides = [...box.children];
    files.slice(slides.length).forEach(f => {
      const s = document.createElement('span'); s.style.backgroundImage = `url("${f}")`; box.appendChild(s); slides.push(s);
    });
    if (slides.length < 2 || diam) return;
    let i = 0;
    setInterval(() => {
      if (document.hidden) return;
      slides[i].classList.remove('on'); i = (i + 1) % slides.length; slides[i].classList.add('on');
    }, +el.dataset.interval || 7000);
  });
})();
