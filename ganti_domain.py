#!/usr/bin/env python3
"""Ganti alamat website contoh dengan domain asli di semua file (semua halaman, robots.txt, sitemap.xml, halaman artikel).
Pemakaian:  python ganti_domain.py www.domainanda.com
Butuh Python 3 saja."""
import sys, os, re, subprocess
R = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    sys.exit('Pemakaian: python ganti_domain.py www.domainanda.com')
new = 'https://' + re.sub(r'^https?://', '', sys.argv[1].strip()).strip('/') + '/'
idx = os.path.join(R, 'index.html')
old = re.search(r'<link rel="canonical" href="([^"]+)"', open(idx, encoding='utf-8').read()).group(1)
import glob
for f in [os.path.basename(x) for x in glob.glob(os.path.join(R, '*.html'))] + ['robots.txt']:
    p = os.path.join(R, f); s = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(s.replace(old, new))
# halaman artikel dan sitemap dibuat ulang dari alamat baru
subprocess.run([sys.executable, os.path.join(R, 'build_artikel.py')], check=True)
print(f'Selesai: {old}  ->  {new}')
