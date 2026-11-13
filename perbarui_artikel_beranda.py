#!/usr/bin/env python3
"""Perbarui section "Artikel terbaru" di beranda (index.html) dari js/articles.js.
Jalankan setelah menambah atau mengubah artikel:  python perbarui_artikel_beranda.py
Hanya mengubah bagian di antara penanda ARTIKEL-TERBARU di index.html. Halaman artikel tidak disentuh.
Butuh Python 3 saja (tanpa library tambahan)."""
import re, json, html, os

JUMLAH = 3  # jumlah artikel terbaru yang tampil di beranda

R = os.path.dirname(os.path.abspath(__file__))
def rd(p): return open(os.path.join(R, p), encoding='utf-8').read()

# --- baca articles.js (cara yang sama dengan build_artikel.py) ---
src = rd('js/articles.js')
src = re.sub(r'^\s*//.*$', '', src, flags=re.M)
src = src[src.index('['):src.rindex(']') + 1]
src = re.sub(r'([{,]\s*)(title|slug|produk|iso|cat|date|read|excerpt|intro|sections|h|p|en)\s*:', r'\1"\2":', src)
src = re.sub(r',(\s*[}\]])', r'\1', src)
A = sorted(json.loads(src), key=lambda a: a['iso'], reverse=True)

# --- foto produk per kode (vf2, zs2, ...) dibaca dari kartu produk di halaman merek ---
PR = {m.group(1): m.group(2) for m in re.finditer(
    r'<article class="pcard" id="(\w+)">.*?<img src="([^"]+)"', rd('produk-vivorti.html') + rd('produk-zecco.html'), re.S)}

esc = lambda s: html.escape(s, quote=True)

dipakai = set()
def kartu(a):
    # pilih foto produk yang belum dipakai kartu sebelumnya, supaya foto tidak kembar
    foto = [PR[i] for i in a.get('produk', []) if i in PR]
    img = next((x for x in foto if x not in dipakai), foto[0] if foto else 'assets/images/bg-artikel.jpg')
    dipakai.add(img)
    return f'''    <a class="at-card" href="artikel/{a["slug"]}.html">
      <span class="at-foto"><img src="{img}" alt="" loading="lazy" decoding="async"><span class="at-cat">{esc(a["cat"])}</span></span>
      <div class="at-isi">
        <span class="at-meta">{esc(a["date"])} &middot; {esc(a["read"])}</span>
        <h3>{esc(a["title"])}</h3>
        <p class="at-desc">{esc(a["excerpt"])}</p>
        <span class="at-link">Baca artikel <i aria-hidden="true">&rarr;</i></span>
      </div>
    </a>'''

section = f'''<!-- ARTIKEL-TERBARU:MULAI (dibuat otomatis oleh perbarui_artikel_beranda.py dari js/articles.js, jangan diedit manual) -->
<section class="section cm-sec" id="artikel-terbaru" aria-labelledby="at-judul">
<div class="wrap">
  <div class="cm-head">
    <span class="eyebrow">Artikel</span>
    <h2 id="at-judul">Panduan terbaru seputar lemari arsip</h2>
    <p class="lead">Tips memilih, menata, dan merawat lemari arsip untuk kantor, sekolah, dan instansi.</p>
  </div>
  <div class="at-grid">
{chr(10).join(kartu(a) for a in A[:JUMLAH])}
  </div>
  <div class="at-semua"><a class="at-btn" href="artikel.html">Lihat semua artikel <i aria-hidden="true">&rarr;</i></a></div>
</div>
</section>
<!-- ARTIKEL-TERBARU:SELESAI -->'''

f = os.path.join(R, 'index.html')
s = open(f, encoding='utf-8').read()
pola = re.compile(r'<!-- ARTIKEL-TERBARU:MULAI.*?<!-- ARTIKEL-TERBARU:SELESAI -->', re.S)
if pola.search(s):
    s = pola.sub(lambda m: section, s, 1)
else:
    tanda = '<section class="section" id="premium-faq">'
    if tanda not in s:
        raise SystemExit('Tidak menemukan section FAQ di index.html untuk menaruh artikel terbaru.')
    s = s.replace(tanda, section + '\n\n' + tanda, 1)
open(f, 'w', encoding='utf-8').write(s)
print(f'Selesai: {min(JUMLAH, len(A))} artikel terbaru ditampilkan di beranda.')
