#!/usr/bin/env python3
"""Bangun halaman detail tiap produk (produk/<nama>.html, contoh produk/v-SL01.html; nama file mengikuti tautan di kartu produk) dan tambahkan ke sitemap.xml.
Sumber data: kartu produk dan blok UKURAN di produk-vivorti.html dan produk-zecco.html; header dan footer disalin dari index.html.
Jalankan setiap kali produk-vivorti.html, produk-zecco.html, atau header/footer index.html berubah:  python build_produk.py
Butuh Python 3 saja (tanpa library tambahan).

AMAN: halaman produk/<nama>.html yang SUDAH ADA tidak ditimpa dan tidak dihapus (foto yang sudah kamu pasang tetap utuh).
Skrip hanya membuat halaman yang belum ada. Untuk membangun ulang SEMUA halaman (misalnya header/footer berubah):  python build_produk.py --timpa
Saat --timpa, halaman lama dicadangkan dulu ke folder produk_cadangan/."""
import re, json, html, os, glob, datetime, sys, shutil
R = os.path.dirname(os.path.abspath(__file__))
def rd(p): return open(os.path.join(R, p), encoding='utf-8').read()
def wr(p, s):
    p = os.path.join(R, p); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(s)
esc = lambda s: html.escape(s, quote=True)

# ====== PENGATURAN ======
FOTO_DETAIL = 'assets/images/detail/{id}-{n}.jpg'   # 4 foto detail tiap produk: vf2-1.jpg, vf2-2.jpg, vf2-3.jpg, vf2-4.jpg
LABEL_FOTO = {                                       # nama tiap foto detail (urutan sama dengan nomor foto)
    'vf2': ['Kunci', 'Handle pintu', 'Pintu kaca', 'Rak dalam'],
    # tambah atau ubah per produk, contoh:  'vf4': ['Kunci sentral', 'Handle laci', 'Rel laci', 'Isi laci'],
}
LABEL_JENIS = [                                      # nama foto bawaan menurut jenis produk (kata kunci di jenis produk)
    ('laci', ['Kunci sentral', 'Handle laci', 'Rel laci', 'Isi laci']),
    ('loker', ['Kunci', 'Ventilasi', 'Pintu', 'Rak dalam']),
    ('rolling', ['Kunci', 'Pintu rolling', 'Rak dalam', 'Rangka']),
    ('geser', ['Kunci', 'Handle pintu', 'Rel pintu', 'Rak dalam']),
]
LABEL_BAWAAN = ['Kunci', 'Handle pintu', 'Pintu', 'Rak dalam']
# Kartu produk di produk-vivorti.html dan produk-zecco.html sekarang tidak memuat kotak Ukuran / Kunci / Cocok untuk,
# jadi isinya diambil dari sini. Isi per produk (kode: (kunci, cocok untuk)). Produk yang belum diisi memakai nilai bawaan.
SPEK = {
    'vf2': ('Kunci sentral', 'Meja kerja, ruang kecil'),
    # 'vf4': ('Kunci sentral', 'Ruang arsip kantor'),
}
KUNCI_BAWAAN, COCOK_BAWAAN = 'Kunci sentral', 'Kantor dan ruang arsip'
UKURAN_AWAL = 3                                      # ukuran yang terpilih saat halaman dibuka (0 = pertama, 3 = keempat)
KEUNGGULAN = ['Harga distributor untuk satuan dan partai besar', 'Garansi atas cacat produksi', 'Dikirim aman ke seluruh Indonesia']
# ========================

index = rd('index.html'); prod = rd('produk-vivorti.html') + rd('produk-zecco.html')   # Vivorti dulu, lalu Zecco
DOMAIN = re.search(r'<link rel="canonical" href="([^"]+)"', index).group(1)

# --- 10 ukuran tiap model dari blok UKURAN di produk-vivorti.html dan produk-zecco.html ---
UK = {}
for mm in re.finditer(r'const UKURAN = \{(.*?)\n  \};', prod, re.S):
    UK.update({k: json.loads(v) for k, v in re.findall(r'(\w+):\s*(\[.*?\])', mm.group(1), re.S)})

# --- data produk dari kartu (foto, jenis, nama, deskripsi). Kotak dl Ukuran/Kunci/Cocok untuk boleh tidak ada ---
batas = prod.index('id="zecco"')
P = []
for m in re.finditer(r'<article class="pcard" id="(\w+)">.*?<img src="([^"]+)".*?<span class="ptype">(.*?)</span><h4>(.*?)</h4><p>(.*?)</p>'
                     r'(?:\s*<dl><div><dt>Ukuran</dt><dd>(.*?)</dd></div><div><dt>Kunci</dt><dd>(.*?)</dd></div>'
                     r'<div class="full"><dt>Cocok untuk</dt><dd>(.*?)</dd></div></dl>)?', prod, re.S):
    i, img, tipe, nama, desc, uk, kunci, cocok = m.groups()
    kk, cc = SPEK.get(i, (KUNCI_BAWAAN, COCOK_BAWAAN))
    # nama file halaman detail diambil dari tautan "Lihat ukuran & detail" di kartu (contoh produk/v-SL01.html); kalau tidak ada, pakai id kartu
    sl = re.search(r'class="(?:sz-open|aksi-detail)" href="produk/([^"?#]+)\.html', prod[m.start():prod.index('</article>', m.start())])
    P.append(dict(id=i, slug=sl.group(1) if sl else i, img=img, type=tipe, name=nama, desc=desc, ukuran=uk or (UK[i][UKURAN_AWAL] + ' cm'), kunci=kunci or kk, cocok=cocok or cc,
                  brand='Vivorti' if m.start() < batas else 'Zecco', bid='vivorti' if m.start() < batas else 'zecco'))
if not P:
    raise SystemExit('GAGAL: tidak ada kartu produk yang terbaca di produk-vivorti.html / produk-zecco.html. Folder produk/ tidak diubah.')

# --- header & footer disalin dari index.html, alamatnya disesuaikan untuk folder produk/ ---
def rel(block):
    block = re.sub(r'href="(?!https?:|mailto:|tel:|#|\.\./)', 'href="../', block)
    return block.replace('src="assets/', 'src="../assets/')
nav = rel(re.search(r'<header class="navbar".*?</header>', index, re.S).group(0)).replace(' aria-current="page"', '')
nav = nav.replace('class="dropdown-btn" href="../produk.html"', 'class="dropdown-btn" href="../produk.html" aria-current="page"', 1)
foot = rel(re.search(r'<footer class="footer">.*?</footer>', index, re.S).group(0))

TPL = '''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.dataset.theme="light"</script>
<script>function fb(i,n){var e=(i.dataset.ext||"").split(",").filter(Boolean);if(e.length){var x=e.shift();i.dataset.ext=e.join(",");i.src=i.src.replace(/\\.\\w+$/,"."+x);return}i.onerror=null;i.src=i.dataset.main;i.classList.add("fb","fb"+n)}</script>
<title>@@NAMA@@ @@TIPE@@ | Cahaya Mustika Internesia</title>
<meta name="description" content="@@DESC@@">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b1f4a">
<link rel="canonical" href="@@URL@@">
<meta property="og:type" content="product"><meta property="og:locale" content="id_ID"><meta property="og:site_name" content="Cahaya Mustika Internesia">
<meta property="og:title" content="@@NAMA@@ @@TIPE@@"><meta property="og:description" content="@@DESC@@"><meta property="og:url" content="@@URL@@">
<meta property="og:image" content="@@IMGABS@@"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">@@LD@@</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="../assets/images/logo.svg"><link rel="stylesheet" href="../css/style.css"><link rel="stylesheet" href="../css/produk-detail.css?v=4">
</head>
<body>
@@NAV@@
<main>
<section class="d-top"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Beranda</a><span>/</span><a href="../produk.html">Produk</a><span>/</span><a href="../produk-@@BID@@.html">@@BRAND@@</a><span>/</span>@@MODEL@@</nav></div></section>

<section class="d-main"><div class="wrap d-grid">
<div class="d-gal">
<div class="d-thumbs" role="group" aria-label="Foto detail produk">@@THUMBS@@</div>
<div class="d-stage"><div class="d-view"><img id="d-big" class="is-detail" src="../@@IMG@@" alt="@@NAMA@@ @@TIPE@@ - lemari arsip besi merek @@BRAND@@" width="420" height="520"></div><button type="button" class="d-zoom" id="d-zoom">Perbesar foto</button></div>
</div>
<div class="d-info">
<span class="ptype">@@TIPE@@</span><h1>@@NAMA@@</h1><p>@@DESC@@</p>
<dl class="d-spec"><div><dt>Ukuran</dt><dd id="d-uk">@@UKDEF@@ cm</dd></div><div><dt>Kunci</dt><dd>@@KUNCI@@</dd></div><div><dt>Cocok untuk</dt><dd>@@COCOK@@</dd></div></dl>
<div class="d-act"><a id="d-tanya" class="btn btn-primary" href="@@TANYA@@">Tanya harga</a><a class="btn btn-ghost" href="../produk-@@BID@@.html">Semua produk @@BRAND@@</a></div>
<ul class="d-ok">@@OK@@</ul>
</div>
</div></section>

<section class="d-more"><div class="wrap d-cols">
<div><h2 class="d-h" id="detail">Detail produk</h2>
<dl class="d-table"><div><dt>Merek</dt><dd>@@BRAND@@</dd></div><div><dt>Jenis</dt><dd>@@TIPE@@</dd></div><div><dt>Lebar</dt><dd id="d-w"></dd></div><div><dt>Dalam</dt><dd id="d-d"></dd></div><div><dt>Tinggi</dt><dd id="d-t"></dd></div><div><dt>Kunci</dt><dd>@@KUNCI@@</dd></div><div><dt>Cocok untuk</dt><dd>@@COCOK@@</dd></div></dl></div>
<div><h2 class="d-h">Pilih ukuran</h2><p class="d-note">@@JML@@ ukuran tersedia. Pilih salah satu untuk melihat rinciannya, lalu tanyakan harganya.</p>
<div class="d-sizes" role="group" aria-label="Pilihan ukuran">@@SIZES@@</div></div>
</div></section>

<section class="d-other"><div class="wrap"><h2 class="d-h">Produk @@BRAND@@ lainnya</h2><div class="d-ogrid">@@OTHER@@</div></div></section>
</main>
<dialog id="d-lb" class="lb" aria-label="Foto produk diperbesar"><button type="button" class="lb-x" id="d-lbx" aria-label="Tutup">&times;</button><img id="d-lbimg" src="" alt=""></dialog>
@@FOOT@@
<script src="../js/kamus-en.js"></script><script src="../js/prefs.js"></script><script src="../js/script.js"></script>
<script>
(function () {
  var U = @@UJSON@@, DEF = @@DEF@@, NAMA = @@NAMAJSON@@;
  var $ = function (s) { return document.querySelector(s); }, cur = DEF;
  var q = new URLSearchParams(location.search).get('u'); if (q !== null && U[+q]) cur = +q;
  function pilih(i) {
    cur = i; var p = U[i].split('x').map(function (n) { return +n.trim(); });
    document.querySelectorAll('.d-sz').forEach(function (b, k) { b.setAttribute('aria-pressed', k === i); });
    $('#d-uk').textContent = U[i] + ' cm'; $('#d-w').textContent = p[0] + ' cm'; $('#d-d').textContent = p[1] + ' cm'; $('#d-t').textContent = p[2] + ' cm';
    $('#d-tanya').href = '../kontak.html?produk=' + encodeURIComponent(NAMA).replace(/%20/g, '+') + '&ukuran=' + encodeURIComponent(U[i] + ' cm');
    try { history.replaceState(null, '', location.pathname + '?u=' + i + location.hash); } catch (e) {}
  }
  document.querySelectorAll('.d-sz').forEach(function (b, k) { b.addEventListener('click', function () { pilih(k); }); });
  pilih(cur);
  // Galeri: klik foto kecil untuk menampilkannya di foto besar, klik lagi untuk kembali ke foto produk
  var big = $('#d-big'), awal = big.getAttribute('src'), altAwal = big.alt;
  var ths = document.querySelectorAll('.d-th');
  function kembali() { big.src = awal; big.alt = altAwal; big.className = 'is-detail'; ths.forEach(function (t) { t.setAttribute('aria-pressed', false); }); }
  ths.forEach(function (t) {
    t.addEventListener('click', function () {
      if (t.getAttribute('aria-pressed') === 'true') return kembali();
      var im = t.querySelector('img');
      ths.forEach(function (x) { x.setAttribute('aria-pressed', x === t); });
      big.src = im.getAttribute('src'); big.alt = im.alt;
      big.className = 'is-detail' + (im.classList.contains('fb') ? ' ' + [].filter.call(im.classList, function (c) { return c.indexOf('fb') === 0; }).join(' ') : '');
    });
  });
  // Perbesar foto
  var lb = $('#d-lb');
  $('#d-zoom').addEventListener('click', function () { $('#d-lbimg').src = big.getAttribute('src'); $('#d-lbimg').alt = big.alt; if (lb.showModal) lb.showModal(); });
  $('#d-lbx').addEventListener('click', function () { lb.close(); });
  lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
})();
</script>
</body></html>'''

def labels(p):
    if p['id'] in LABEL_FOTO: return LABEL_FOTO[p['id']]
    for kata, lb in LABEL_JENIS:
        if kata in p['type'].lower(): return lb
    return LABEL_BAWAAN

TIMPA = '--timpa' in sys.argv
if TIMPA:
    cad = os.path.join(R, 'produk_cadangan', datetime.datetime.now().strftime('%Y%m%d-%H%M%S')); os.makedirs(cad, exist_ok=True)
    for f in glob.glob(os.path.join(R, 'produk', '*.html')): shutil.copy2(f, cad); os.remove(f)
    print('Halaman lama dicadangkan ke', os.path.relpath(cad, R))
dibuat, dilewati = [], []
for p in P:
    uk = UK[p['id']]; maxT = max(int(s.split('x')[2]) for s in uk)
    awal = next((k for k, s in enumerate(uk) if s + ' cm' == p['ukuran']), 0)
    model = p['name'].replace(p['brand'] + ' ', '', 1)
    url = f'{DOMAIN}produk/{p["slug"]}.html'
    imgabs = DOMAIN + p['img'].replace(' ', '%20')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": p['name'], "brand": {"@type": "Brand", "name": p['brand']}, "category": p['type'], "image": imgabs,
         "description": p['desc'], "url": url, "seller": {"@id": DOMAIN + "#bisnis"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Beranda", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": "Produk", "item": DOMAIN + "produk.html"},
            {"@type": "ListItem", "position": 3, "name": p['brand'], "item": f'{DOMAIN}produk-{p["bid"]}.html'},
            {"@type": "ListItem", "position": 4, "name": p['name'], "item": url}]}]}
    thumbs = ''.join(
        f'<button type="button" class="d-th" aria-pressed="false" aria-label="Foto detail: {esc(lb)}"><img src="../{FOTO_DETAIL.format(id=p["id"], n=n)}" '
        f'data-ext="webp,png,jpeg" data-main="../{p["img"]}" alt="{esc(p["name"])} - {esc(lb)}" loading="lazy" onerror="fb(this,{n})"><span>{lb}</span></button>'
        for n, lb in enumerate(labels(p), 1))
    sizes = ''.join(
        f'<button type="button" class="d-sz" aria-pressed="false"><span class="d-szi"><img src="../{p["img"]}" alt="" loading="lazy" '
        f'style="height:{round(int(s.split("x")[2]) / maxT * 100)}%"></span><span class="d-szl">{s} cm</span></button>' for s in uk)
    other = ''.join(
        f'<a class="d-oc" href="{o["slug"]}.html"><span class="o-img"><img src="../{o["img"]}" alt="{esc(o["name"])} - {esc(o["type"])}" loading="lazy"></span><b>{o["name"]}</b><small>{o["type"]}</small></a>'
        for o in P if o['brand'] == p['brand'] and o['id'] != p['id'])
    page = TPL
    for k, v in {'@@NAMAJSON@@': json.dumps(p['name']), '@@UJSON@@': json.dumps(uk), '@@DEF@@': str(awal), '@@LD@@': json.dumps(ld, ensure_ascii=False),
                 '@@NAMA@@': esc(p['name']), '@@TIPE@@': p['type'], '@@DESC@@': esc(p['desc']), '@@URL@@': url, '@@IMGABS@@': imgabs,
                 '@@NAV@@': nav, '@@FOOT@@': foot, '@@BID@@': p['bid'], '@@BRAND@@': p['brand'], '@@MODEL@@': model, '@@IMG@@': p['img'],
                 '@@THUMBS@@': thumbs, '@@UKDEF@@': uk[awal], '@@KUNCI@@': p['kunci'], '@@COCOK@@': p['cocok'],
                 '@@TANYA@@': f'../kontak.html?produk={p["name"].replace(" ", "+")}&ukuran={uk[awal].replace(" ", "+")}+cm',
                 '@@OK@@': ''.join(f'<li>{k}</li>' for k in KEUNGGULAN), '@@SIZES@@': sizes, '@@JML@@': str(len(uk)), '@@OTHER@@': other}.items():
        page = page.replace(k, v)
    if os.path.exists(os.path.join(R, 'produk', p['slug'] + '.html')):
        dilewati.append(p['slug']); continue
    wr(f'produk/{p["slug"]}.html', page); dibuat.append(p['slug'])

# --- sitemap: tambahkan halaman produk (entri lama /produk/ diganti) ---
sm = os.path.join(R, 'sitemap.xml')
if os.path.exists(sm):
    s = re.sub(r'  <url><loc>[^<]*/produk/[^<]*</loc>.*?</url>\n', '', open(sm, encoding='utf-8').read())
    hari = datetime.date.today().isoformat()
    baru = ''.join(f'  <url><loc>{DOMAIN}produk/{p["slug"]}.html</loc><lastmod>{hari}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n' for p in P)
    open(sm, 'w', encoding='utf-8').write(s.replace('</urlset>', baru + '</urlset>'))
print(f'Selesai. Dibuat baru: {len(dibuat)} {dibuat}. Dilewati karena sudah ada (tidak diubah): {len(dilewati)} {dilewati}')