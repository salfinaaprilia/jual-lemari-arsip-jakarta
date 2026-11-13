#!/usr/bin/env python3
"""Sisipkan isi css/style.css dan css/home.css langsung ke index.html (di dalam <style id="css-beranda">).
Tujuannya agar beranda tidak menunggu 2 file CSS sebelum tampil (PageSpeed: "Permintaan pemblokiran render").
File CSS aslinya tetap dipakai halaman lain dan tetap menjadi tempat mengedit gaya.
Jalankan lagi setiap kali mengubah css/style.css atau css/home.css:  python sisipkan_css_beranda.py
(bangun-artikel.bat juga menjalankannya)."""
import os, re
R = os.path.dirname(os.path.abspath(__file__))
def rd(p): return open(os.path.join(R, p), encoding='utf-8').read()

def ringkas(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)        # buang komentar
    css = re.sub(r'\s+', ' ', css)                          # rapatkan spasi dan baris
    css = re.sub(r'\s*([{};])\s*', r'\1', css)              # spasi di sekitar { } ;
    return css.replace(';}', '}').strip()

css = ''.join(ringkas(rd(f'css/{n}.css')) for n in ('style', 'home'))
css = css.replace("url('../assets/", "url('assets/").replace('url("../assets/', 'url("assets/').replace('url(../assets/', 'url(assets/')
blok = '<style id="css-beranda">' + css + '</style>'

f = os.path.join(R, 'index.html'); s = open(f, encoding='utf-8').read()
lama = '<link rel="stylesheet" href="css/style.css"><link rel="stylesheet" href="css/home.css">'
if lama in s:
    s = s.replace(lama, blok, 1)
else:
    s, n = re.subn(r'<style id="css-beranda">.*?</style>', lambda m: blok, s, count=1, flags=re.S)
    if not n: raise SystemExit('Tempat CSS beranda tidak ditemukan di index.html')
open(f, 'w', encoding='utf-8').write(s)
print(f'Selesai: CSS beranda ({len(css) // 1024} KB) disisipkan ke index.html')
