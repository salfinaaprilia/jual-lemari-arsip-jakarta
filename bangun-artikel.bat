@echo off
rem Klik dua kali file ini setelah menambah atau mengubah artikel di js/articles.js, atau setelah mengubah produk.html, css/style.css, atau css/home.css.
rem Halaman artikel, halaman detail produk, sitemap, dan data SEO dibuat ulang otomatis (butuh Python 3).
cd /d "%~dp0"
python build_artikel.py || py build_artikel.py
python build_produk.py || py build_produk.py
python perbarui_artikel_beranda.py || py perbarui_artikel_beranda.py
python sisipkan_css_beranda.py || py sisipkan_css_beranda.py
echo.
pause