# Website CV Cahaya Mustika (merek Vivorti dan Zecco)
Buka index.html di browser.
- css/style.css     : gaya dan animasi
- js/articles.js    : isi artikel (tambah atau ubah di sini)
- artikel/          : halaman tiap artikel (dibuat otomatis oleh build_artikel.py atau bangun-artikel.bat)
- Font              : Manrope untuk semua judul (h1-h6), Poppins untuk teks isi (dimuat dari Google Fonts di index.html)
- js/script.js      : menu, gerak gambar, pembaca artikel, form WhatsApp (ganti WA_NUMBER)
- assets/images/    : logo CV (logo.svg, logo-cv.svg, logo-cv-light.svg), logo merek (vivorti-logo, zecco-logo), 8 gambar produk, hero-cabinet, og-image
- robots.txt, sitemap.xml : SEO. Ganti https://www.cahayamustika.com/ dengan domain asli (index.html, robots.txt, sitemap.xml)

Yang perlu diganti dengan data asli: nama CV, nomor WhatsApp, email, alamat, ukuran/spesifikasi tiap model (saat ini contoh), dan gambar produk (ganti file SVG dengan foto asli, nama file dipertahankan).
Menambah produk: salin satu blok <article class="pcard"> di index.html dan ubah isinya (nama file gambar di assets/images/).
Menambah artikel: (1) buka js/articles.js, salin satu blok artikel, ganti isinya, isi slug, iso (tahun-bulan-tanggal), dan produk (kode produk yang fotonya tampil: vf2 vf4 vp2 vl6 zs2 zk2 zr3 zf3); (2) klik dua kali bangun-artikel.bat (Windows) atau jalankan `python build_artikel.py`. Artikel terbaru otomatis jadi kartu besar di beranda dan artikel sebelumnya turun ke bagian bawahnya. Halaman artikel, sitemap, dan data SEO dibuat otomatis.
Tautan tiap artikel: https://domainanda.com/artikel/slug-artikel.html
Setelah mengubah header atau footer di index.html, jalankan build_artikel.py lagi supaya halaman artikel ikut diperbarui.
Ganti domain contoh: jalankan `python ganti_domain.py www.domainanda.com`. Ini mengganti alamat di semua file (beranda, robots.txt, sitemap.xml, halaman artikel) sekaligus. Tautan yang disalin dari website hanya bisa dibuka orang lain setelah website di-upload ke hosting dengan domain tersebut.

Bahasa dan mode gelap/terang: tombol ID/EN dan tombol gelap/terang sudah dihapus dari header. Website selalu tampil dalam bahasa Indonesia dengan tema terang (diatur di js/prefs.js). Kamus Inggris dan CSS mode gelap masih ada di file, tetapi tidak dipakai.
- js/prefs.js              : mesin bahasa dan tema.
- js/kamus-en.js           : kamus Indonesia -> Inggris untuk teks di beranda. Menambah atau mengubah teks di index.html? Tambahkan atau ubah pasangannya di sini (teks Indonesia harus persis sama).
- Terjemahan artikel       : isi blok `en` pada tiap artikel di js/articles.js, lalu jalankan bangun-artikel.bat. File js/kamus-artikel-en.js dibuat otomatis (jangan diedit).
- Tampilan gelap           : bagian "Mode gelap" di akhir css/style.css.
Catatan SEO: teks Inggris diganti lewat JavaScript, sedangkan mesin pencari membaca versi Indonesia (bahasa utama website).

Latar foto halaman artikel: assets/images/bg-artikel.jpg. Ganti dengan foto Anda sendiri (nama file sama, ukuran sekitar 2000 x 1100 px, di bawah 300 KB). Kekuatan foto diatur di bagian paling bawah css/style.css lewat --fade-left, --fade-mid, --fade-right (makin kecil angkanya, makin jelas fotonya). Berlaku otomatis untuk semua halaman artikel, termasuk artikel baru.

## Halaman terpisah dan latar foto (v15)
Website kini terdiri dari lima halaman sendiri-sendiri: index.html (Beranda), produk.html, portofolio.html, artikel.html, kontak.html, ditambah halaman tiap artikel di folder artikel/.
- Latar foto di belakang tulisan: atribut data-bg pada bagian paling atas tiap halaman (dan pita ajakan di bawahnya). Contoh: data-bg="assets/images/bg/beranda-1.jpg,assets/images/bg/beranda-2.jpg". Pisahkan dengan koma; lebih dari satu foto berganti otomatis (jeda di data-interval, milidetik). Foto pertama juga ditulis di dalam <span style="background-image:..."> tepat di bawahnya, ubah keduanya bila mengganti foto pertama.
- Foto latar ada di assets/images/bg/ (1920 x 1080). Ganti dengan foto Anda sendiri dengan nama file yang sama, ukuran sebaiknya di bawah 250 KB. Gelap-terangnya diatur di css/style.css bagian "Halaman terpisah dan latar foto" (angka rgba pada [data-bg]::before).
- js/latar.js : mesin pengganti latar foto.
- Tombol "Tanya harga" di produk.html membawa nama produk ke formulir di kontak.html (lewat ?produk=...).
- Artikel baru: tetap lewat js/articles.js + bangun-artikel.bat. Header dan footer halaman artikel disalin dari index.html, produk.html dipakai sebagai sumber foto produk.
- Mengubah menu header atau footer: ubah di kelima halaman utama, lalu jalankan bangun-artikel.bat supaya halaman artikel ikut sama.
- Nomor WhatsApp formulir ada di js/script.js (WA_NUMBER).


## Foto latar dikurangi (v15c)
Tampilan, gerak, dan pergantian foto latar sama persis dengan v15. Yang berubah hanya isi fotonya: tiap foto di assets/images/bg/ kini berisi 3 lemari (sebelumnya 5-6) yang berdiri di sisi kanan, jadi tidak ramai di belakang tulisan. Nama file tidak berubah, jadi HTML dan CSS tidak perlu diubah. Untuk foto sendiri: ganti file di folder itu dengan nama yang sama (1920 x 1080 px).

## Halaman produk dipisah per merek (v17)
- produk.html          : halaman pemilih merek (dua kartu besar menuju halaman merek)
- produk-vivorti.html  : semua model Vivorti (kartu produk + blok UKURAN milik Vivorti)
- produk-zecco.html    : semua model Zecco (kartu produk + blok UKURAN milik Zecco)
- css/produk-tema.css  : warna biru halaman produk, disamakan dengan beranda (ubah warna di bagian :root paling atas)
- Menambah produk: salin satu blok <article class="pcard"> di halaman mereknya, tambahkan ukurannya di blok UKURAN halaman yang sama, lalu jalankan bangun-artikel.bat.