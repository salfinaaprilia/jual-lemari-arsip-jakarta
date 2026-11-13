#!/usr/bin/env python3
"""Bangun halaman artikel (artikel/<slug>.html), sitemap.xml, dan data SEO artikel dari js/articles.js.
Jalankan setiap kali menambah atau mengubah artikel:  python build_artikel.py
Butuh Python 3 saja (tanpa library tambahan)."""
import re, json, html, os, glob
R = os.path.dirname(os.path.abspath(__file__))
def rd(p): return open(os.path.join(R, p), encoding='utf-8').read()
def wr(p, s):
    p = os.path.join(R, p); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(s)

# --- baca articles.js ---
src = rd('js/articles.js')
src = re.sub(r'^\s*//.*$', '', src, flags=re.M)
src = src[src.index('['):src.rindex(']') + 1]
src = re.sub(r'([{,]\s*)(title|slug|produk|iso|cat|date|read|excerpt|intro|sections|h|p|en)\s*:', r'\1"\2":', src)
src = re.sub(r',(\s*[}\]])', r'\1', src)
A = sorted(json.loads(src), key=lambda a: a['iso'], reverse=True)

# --- kamus terjemahan Inggris untuk artikel (dibuat dari blok en di js/articles.js) ---
kam = {}
for a in A:
    e = a.get('en')
    if not e: continue
    for k in ('title', 'cat', 'date', 'read', 'excerpt', 'intro'):
        if e.get(k): kam[a[k]] = e[k]
    for s, t in zip(a['sections'], e.get('sections', [])):
        kam[s['h']] = t['h']; kam[s['p']] = t['p']
wr('js/kamus-artikel-en.js', '// Dibuat otomatis oleh build_artikel.py dari blok en di js/articles.js. Jangan diedit manual.\nObject.assign(window.KAMUS_EN = window.KAMUS_EN || {}, ' + json.dumps(kam, ensure_ascii=False, indent=1) + ');\n')

index = rd('index.html')
DOMAIN = re.search(r'<link rel="canonical" href="([^"]+)"', index).group(1)
esc = lambda s: html.escape(s, quote=True)
def rel(block):
    block = re.sub(r'href="(?!https?:|mailto:|tel:|#|\.\./)', 'href="../', block)
    return block.replace('src="assets/', 'src="../assets/')

# --- header & footer disalin dari index.html supaya selalu sama ---
nav = re.search(r'<header class="navbar".*?</header>', index, re.S).group(0)
nav = rel(nav).replace('class="navbar"', 'class="navbar scrolled"', 1).replace(' aria-current="page"', '')
nav = nav.replace('<a href="../artikel.html">', '<a href="../artikel.html" aria-current="page">', 1)
# data produk (foto, nama, jenis) dibaca dari kartu produk di index.html
PR = {m.group(1): dict(img=m.group(2), type=m.group(3), name=m.group(4)) for m in re.finditer(
    r'<article class="pcard" id="(\w+)">.*?<img src="([^"]+)" alt="[^"]*".*?<span class="ptype">(.*?)</span><h2>(.*?)</h2>', rd('produk-vivorti.html') + rd('produk-zecco.html'), re.S)}
def prods(a): return [dict(PR[i], id=i) for i in a.get('produk', []) if i in PR]
foot = rel(re.search(r'<footer class="footer">.*?</footer>', index, re.S).group(0))

# Templat halaman artikel: desainnya diambil dari file templat-artikel.html (ubah desain di file itu).
TPL = re.sub(r'<!-- TEMPLAT HALAMAN ARTIKEL.*?-->\s*', '', rd('templat-artikel.html'), count=1, flags=re.S)

# Foto sampul artikel (lebar). Artikel baru tanpa entri di sini memakai SAMPUL_DEFAULT.
SAMPUL = {
    'filing-cabinet-atau-lemari-pintu-geser': 'assets/images/bg/hero-zeco.webp',
    'memilih-loker-untuk-sekolah-dan-pabrik': 'assets/images/bg/artikel-2.jpg',
    'cara-memilih-lemari-arsip': 'assets/images/bg/hero-vivorti.webp',
    'merawat-lemari-arsip-besi': 'assets/images/bg/artikel-1.jpg',
}
SAMPUL_DEFAULT = 'assets/images/bg/hero-beranda.webp'
def cover(a): return SAMPUL.get(a['slug'], SAMPUL_DEFAULT)
def slug(t): return re.sub(r'[^a-z0-9]+', '-', html.unescape(re.sub(r'<[^>]+>', '', t)).lower()).strip('-')

for f in glob.glob(os.path.join(R, 'artikel', '*.html')): os.remove(f)
for a in A:
    url = f'{DOMAIN}artikel/{a["slug"]}.html'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": a['title'], "description": a['excerpt'], "datePublished": a['iso'], "dateModified": a['iso'],
         "mainEntityOfPage": url, "url": url, "image": DOMAIN + cover(a), "inLanguage": "id",
         "author": {"@type": "Organization", "name": "Cahaya Mustika Internesia"},
         "publisher": {"@type": "Organization", "name": "Cahaya Mustika Internesia", "logo": {"@type": "ImageObject", "url": DOMAIN + "assets/images/logoCMI.webp"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Beranda", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": "Artikel", "item": DOMAIN + "artikel.html"},
            {"@type": "ListItem", "position": 3, "name": a['title'], "item": url}]}]}
    def card(o):
        return (f'<a class="ad-card" href="{o["slug"]}.html"><figure><img src="../{cover(o)}" alt="{esc(o["title"])}" loading="lazy"></figure>'
                f'<div class="ad-cbody"><div class="ad-meta"><span class="ad-cat">{o["cat"]}</span><time datetime="{o["iso"]}">{o["date"]}</time></div>'
                f'<h3>{o["title"]}</h3><p>{o["excerpt"]}</p><span class="ad-more">Baca artikel &rarr;</span></div></a>')
    more = ''.join(card(o) for o in [x for x in A if x['slug'] != a['slug']][:3])
    hid = [(slug(s['h']), s) for s in a['sections']]
    toc = ''.join(f'<li><a href="#{i}">{s["h"]}</a></li>' for i, s in hid)
    secs = '\n'.join(f'<h2 id="{i}">{s["h"]}</h2><p>{s["p"]}</p>' for i, s in hid)
    page = TPL
    ogimg = DOMAIN + cover(a)
    for k, v in {'@@OGIMG@@': ogimg, '@@TITLE@@': esc(a['title']), '@@DESC@@': esc(a['excerpt']), '@@URL@@': url, '@@DOMAIN@@': DOMAIN, '@@ISO@@': a['iso'],
                 '@@LD@@': json.dumps(ld, ensure_ascii=False), '@@NAV@@': nav, '@@FOOT@@': foot, '@@CAT@@': a['cat'], '@@DATE@@': a['date'],
                 '@@READ@@': a['read'], '@@INTRO@@': a['intro'], '@@MORE@@': more,
                 '@@COVER@@': cover(a), '@@TOC@@': toc, '@@SECTIONS@@': secs}.items():
        page = page.replace(k, v)
    wr(f'artikel/{a["slug"]}.html', page)

# --- data SEO artikel di beranda + sitemap ---
posts = [{"@type": "BlogPosting", "headline": a['title'], "description": a['excerpt'], "datePublished": a['iso'],
          "url": f'{DOMAIN}artikel/{a["slug"]}.html', "author": {"@type": "Organization", "name": "Cahaya Mustika Internesia"}} for a in A]
new_ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": posts}, ensure_ascii=False) + '</script>'
artikel_html = rd('artikel.html')
artikel_html = re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*"BlogPosting"(?:(?!</script>).)*</script>', lambda m: new_ld, artikel_html, count=1, flags=re.S)
wr('artikel.html', artikel_html)
urls = f'  <url><loc>{DOMAIN}</loc><lastmod>{A[0]["iso"]}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n' + ''.join(
    f'  <url><loc>{DOMAIN}{pg}</loc><lastmod>{A[0]["iso"]}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n' for pg in ('produk.html', 'produk-vivorti.html', 'produk-zecco.html', 'portofolio.html', 'artikel.html', 'kontak.html')) + ''.join(
    f'  <url><loc>{DOMAIN}artikel/{a["slug"]}.html</loc><lastmod>{a["iso"]}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n' for a in A)
wr('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
print(f'Selesai: {len(A)} halaman artikel dibuat di folder artikel/')