#!/usr/bin/env python3
"""Ganti lokasi/alamat website di semua file sekaligus (footer, kontak, peta, SEO, data terstruktur, terjemahan Inggris).
Pemakaian: taruh file ini di folder utama website (sejajar index.html), lalu jalankan:  python ganti_alamat.py
Butuh Python 3 saja. Aman dijalankan ulang. Untuk alamat lain, ubah bagian PENGATURAN di bawah."""
import os, re, glob, json

# ===== PENGATURAN: ubah di sini kalau alamat berubah lagi =====
ALAMAT  = "Jl. Penjernihan II No.7, RT.11/RW.6, Bend. Hilir, Kecamatan Tanah Abang, Kota Jakarta Pusat, Daerah Khusus Ibukota Jakarta 10210"
JALAN   = "Jl. Penjernihan II No.7, RT.11/RW.6, Bend. Hilir, Kecamatan Tanah Abang"
KOTA    = "Jakarta Pusat"        # untuk data terstruktur (SEO)
PROVINSI= "DKI Jakarta"
KODEPOS = "10210"
KOTA_UMUM = "Jakarta"            # dipakai di kalimat: "... Zecco di Jakarta, melayani ..."
KOTA_LAMA = "Malang"             # kota lama yang diganti (kalimat "di Malang")
# ===============================================================

R = os.path.dirname(os.path.abspath(__file__))
files = [f for pat in ('*.html', 'produk/*.html', 'artikel/*.html', 'js/*.js', 'README.md') for f in glob.glob(os.path.join(R, pat))]
esc = lambda s: s.replace('\\', '\\\\').replace('"', '\\"')
addr_ld = ('"address": {"@type": "PostalAddress", "streetAddress": %s, "addressLocality": %s, "addressRegion": %s, "postalCode": %s, "addressCountry": "ID"}'
           % tuple(json.dumps(x, ensure_ascii=False) for x in (JALAN, KOTA, PROVINSI, KODEPOS)))
n_files = 0
for f in files:
    s = open(f, encoding='utf-8').read(); o = s
    # 1) kalimat "di Malang" / "in Malang" (footer, deskripsi SEO, terjemahan)
    s = s.replace('di %s' % KOTA_LAMA, 'di %s' % KOTA_UMUM).replace('in %s' % KOTA_LAMA, 'in %s' % KOTA_UMUM)
    s = s.replace('lemari arsip %s' % KOTA_LAMA, 'lemari arsip %s' % KOTA_UMUM)   # kata kunci SEO
    # 2) data terstruktur (alamat bisnis untuk Google)
    s = re.sub(r'"address":\s*\{[^{}]*\}', lambda m: addr_ld, s)
    # 3) halaman kontak: tulisan Alamat dan alamat untuk peta Google Maps
    s = re.sub(r'(<b>Alamat</b><span>)[^<]*(</span>)', lambda m: m.group(1) + ALAMAT + m.group(2), s)
    s = re.sub(r'(data-alamat=")[^"]*(")', lambda m: m.group(1) + ALAMAT + m.group(2), s)
    s = s.replace('Jl. Contoh No. 12, Malang, Jawa Timur', ALAMAT)
    # 4) kamus Inggris: alamat tidak perlu diterjemahkan
    if f.endswith('kamus-en.js'):
        s = re.sub(r'\n "Malang, Jawa Timur": "[^"]*",', '', s)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); n_files += 1
# halaman artikel dan sitemap dibuat ulang bila ada build_artikel.py (footer ikut sama)
print('Selesai: %d file diperbarui. Alamat sekarang: %s' % (n_files, ALAMAT))
left = [os.path.relpath(f, R) for f in files if KOTA_LAMA.lower() in open(f, encoding='utf-8').read().lower()]
if left: print('Masih ada kata "%s" di: %s' % (KOTA_LAMA, ', '.join(left)))