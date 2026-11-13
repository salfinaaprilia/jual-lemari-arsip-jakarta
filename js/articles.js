// CARA MENAMBAH ARTIKEL
// 1. Salin satu blok {...} di bawah, lalu ganti isinya.
// 2. slug  = nama halaman (huruf kecil, pakai tanda hubung). iso = tanggal (tahun-bulan-hari).
// 2b. en = terjemahan Inggris (title, cat, date, read, excerpt, intro, sections). Isi agar artikel ikut berganti bahasa.
// 3. produk = kode produk yang fotonya ditampilkan di artikel: vf2 vf4 vp2 vl6 (Vivorti) atau zs2 zk2 zr3 zf3 (Zecco).
// 4. Jalankan bangun-artikel.bat (Windows) atau: python build_artikel.py  -> halaman artikelnya dibuat otomatis.
// Urutan tidak perlu diatur: artikel dengan tanggal terbaru otomatis jadi kartu besar di beranda,
// artikel sebelumnya turun ke bagian bawahnya.
const ARTICLES = [
  {
    title: "Filing cabinet atau lemari pintu geser: mana yang cocok untuk kantor Anda?",
    slug: "filing-cabinet-atau-lemari-pintu-geser", produk: ["vf4", "zs2"], iso: "2026-09-27",
    cat: "Perbandingan", date: "27 September 2026", read: "4 menit baca",
    en: {
      title: "Filing cabinet or sliding-door cabinet: which suits your office?",
      cat: "Comparison", date: "September 27, 2026", read: "4 min read",
      excerpt: "Compare how they store files, the space they need, and how easy they are to access, so you choose right.",
      intro: "Both are steel filing cabinets, but they work differently. Understanding the difference helps you choose the model you will actually use every day.",
      sections: [
        {h: "How files are stored", p: "A filing cabinet keeps documents in hanging folders lined up in drawers, so files are easy to find from above. A sliding-door cabinet uses shelves, suited to box files, thick folders, and ledgers."},
        {h: "Space requirements", p: "Drawers must be pulled out fully, so leave room in front of the cabinet. Sliding doors need no door-swing area, which suits narrow rooms and busy walkways."},
        {h: "How often files are opened", p: "For documents opened every day, a filing cabinet is more practical. For large archives that are rarely opened, a sliding-door cabinet saves more space."},
        {h: "A middle path", p: "Many offices use both: filing cabinets near workstations for active files, and sliding-door cabinets in the archive room for older records. Our team can help work out the right combination."}
      ]
    },
    excerpt: "Bandingkan cara menyimpan, kebutuhan ruang, dan kemudahan akses agar pilihan Anda tidak salah.",
    intro: "Keduanya sama-sama lemari arsip besi, tetapi cara kerjanya berbeda. Memahami perbedaannya membantu Anda memilih model yang benar-benar terpakai setiap hari.",
    sections: [
      {h: "Cara menyimpan berkas", p: "Filing cabinet menyimpan dokumen dalam folder gantung yang berjajar di laci, sehingga berkas mudah dicari dari atas. Lemari pintu geser memakai rak, cocok untuk box file, map tebal, dan buku besar."},
      {h: "Kebutuhan ruang", p: "Laci harus ditarik penuh, jadi sisakan ruang di depan lemari. Pintu geser tidak memakan area buka pintu sehingga cocok untuk ruangan sempit atau jalur yang ramai."},
      {h: "Seberapa sering berkas dibuka", p: "Untuk dokumen yang dibuka setiap hari, filing cabinet lebih praktis. Untuk arsip yang jarang dibuka tetapi jumlahnya besar, lemari pintu geser lebih hemat tempat."},
      {h: "Jalan tengah", p: "Banyak kantor memakai keduanya: filing cabinet dekat meja kerja untuk berkas aktif, dan lemari pintu geser di ruang arsip untuk berkas lama. Tim kami bisa membantu menghitung kombinasi yang pas."}
    ]
  },
  {
    title: "Memilih loker untuk sekolah, pabrik, dan kantor",
    slug: "memilih-loker-untuk-sekolah-dan-pabrik", produk: ["vl6"], iso: "2026-09-22",
    cat: "Panduan", date: "22 September 2026", read: "3 menit baca",
    en: {
      title: "Choosing lockers for schools, factories, and offices",
      cat: "Guide", date: "September 22, 2026", read: "3 min read",
      excerpt: "The right number of doors, ventilation, and locks keep lockers durable and comfortable to use.",
      intro: "Lockers are used by many people every day, so choosing one differs from choosing an ordinary filing cabinet. Keep these four points in mind.",
      sections: [
        {h: "Count your users", p: "Plan one door per person, then add spare capacity for new users. Too few lockers force people to share."},
        {h: "Choose the right lock", p: "A lock on every door keeps each person's belongings separate. Store spare keys somewhere safe and record who holds them."},
        {h: "Mind the ventilation", p: "Ventilation holes keep air circulating and reduce odor and dampness. This matters for uniforms, work clothes, and sports gear."},
        {h: "Plan the placement", p: "Place lockers where they are easy to reach, clear of exit routes, and away from direct water."}
      ]
    },
    excerpt: "Jumlah pintu, ventilasi, dan kunci yang tepat membuat loker awet dan nyaman dipakai.",
    intro: "Loker dipakai banyak orang setiap hari, jadi pemilihannya berbeda dari lemari arsip biasa. Empat hal berikut perlu Anda perhatikan.",
    sections: [
      {h: "Hitung jumlah pengguna", p: "Siapkan satu pintu untuk satu orang, lalu tambahkan cadangan untuk pengguna baru. Loker yang kurang membuat penggunanya terpaksa berbagi."},
      {h: "Pilih kunci yang sesuai", p: "Kunci di setiap pintu menjaga barang tiap orang tetap terpisah. Simpan kunci cadangan di tempat yang aman dan catat pemegangnya."},
      {h: "Perhatikan ventilasi", p: "Lubang ventilasi menjaga sirkulasi udara, mengurangi bau dan lembap. Ini penting untuk seragam, pakaian kerja, atau perlengkapan olahraga."},
      {h: "Atur penempatan", p: "Tempatkan loker di area yang mudah dijangkau, tidak menghalangi jalur keluar, dan tidak terkena air secara langsung."}
    ]
  },
  {
    title: "Cara memilih lemari arsip sesuai ruangan dan jumlah berkas",
    slug: "cara-memilih-lemari-arsip", produk: ["vf4", "zs2", "vp2"], iso: "2026-09-12",
    cat: "Panduan", date: "12 September 2026", read: "4 menit baca",
    en: {
      title: "How to choose a filing cabinet for your room and file volume",
      cat: "Guide", date: "September 12, 2026", read: "4 min read",
      excerpt: "Four simple steps so the cabinet you buy fits the room and does not fill up too quickly.",
      intro: "A cabinet that is too big crowds the room, while one that is too small fills up fast. These four steps help you choose correctly before you buy.",
      sections: [
        {h: "Measure the room first", p: "Note the length and width of the area, and leave a walkway of at least 80 cm. For drawer cabinets, also leave space in front so drawers can be pulled out fully."},
        {h: "Estimate your file volume", p: "Estimate the number of folders or box files you have now, then add about 30 percent for a year of document growth."},
        {h: "Choose the door type", p: "Drawers suit frequently opened documents kept in hanging folders. Sliding doors suit narrow rooms because they need no door-swing area, and give more freedom for box files and ledgers."},
        {h: "Check the build quality", p: "Look at the steel thickness, the paint finish, and the strength of the rails or hinges. A central lock makes it easy to secure all drawers at once."}
      ]
    },
    excerpt: "Empat langkah sederhana agar lemari yang dibeli pas dengan ruangan dan tidak cepat penuh.",
    intro: "Lemari arsip yang terlalu besar menyesakkan ruangan, sedangkan yang terlalu kecil cepat penuh. Empat langkah berikut membantu Anda memilih dengan tepat sebelum membeli.",
    sections: [
      {h: "Ukur ruangan lebih dulu", p: "Catat panjang dan lebar area yang akan dipakai, lalu sisakan jalur jalan minimal 80 cm. Untuk lemari laci, sisakan juga ruang di depan lemari agar laci bisa ditarik penuh."},
      {h: "Hitung kebutuhan berkas", p: "Perkirakan jumlah map atau box file saat ini, lalu tambahkan cadangan sekitar 30 persen untuk pertumbuhan dokumen setahun ke depan."},
      {h: "Pilih jenis pintu", p: "Laci cocok untuk dokumen yang sering dibuka dan disusun dengan folder gantung. Pintu geser cocok untuk ruang sempit karena tidak butuh area buka pintu, serta lebih leluasa untuk box file dan buku besar."},
      {h: "Periksa kualitas bahan", p: "Perhatikan ketebalan besi, hasil pengecatan, dan kekuatan rel atau engsel. Kunci sentral memudahkan pengamanan semua laci sekaligus."}
    ]
  },
  {
    title: "Merawat lemari arsip besi agar awet dan tidak berkarat",
    slug: "merawat-lemari-arsip-besi", produk: ["vp2", "zr3"], iso: "2026-09-03",
    cat: "Perawatan", date: "3 September 2026", read: "3 menit baca",
    en: {
      title: "Maintaining steel filing cabinets so they last and do not rust",
      cat: "Maintenance", date: "September 3, 2026", read: "3 min read",
      excerpt: "Small habits that keep steel cabinets smooth and their drawers gliding for years.",
      intro: "Steel filing cabinets can last for years when cared for properly. The care is simple and takes little time.",
      sections: [
        {h: "Clean regularly", p: "Wipe the surface with a clean damp cloth, then dry it. Avoid harsh cleaners or rough sponges that can scratch the paint."},
        {h: "Keep away from damp areas", p: "Place the cabinet slightly away from damp walls or leaky areas. High humidity is the main cause of rust and moldy files."},
        {h: "Look after rails and locks", p: "Apply a light lubricant to drawer or sliding-door rails every few months. For locks, just clear away dust and never force them when they feel stiff."},
        {h: "Spread the load evenly", p: "Do not pile all the heavy files into one drawer or shelf. Spread the weight evenly so the frame and rails do not wear out quickly."}
      ]
    },
    excerpt: "Kebiasaan kecil yang menjaga lemari besi tetap mulus dan lacinya lancar bertahun-tahun.",
    intro: "Lemari arsip besi bisa bertahan bertahun-tahun bila dirawat dengan benar. Perawatannya sederhana dan tidak memakan waktu.",
    sections: [
      {h: "Bersihkan secara rutin", p: "Lap permukaan dengan kain lembap yang bersih, lalu keringkan. Hindari cairan pembersih keras atau spons kasar yang bisa menggores lapisan cat."},
      {h: "Jauhkan dari area lembap", p: "Letakkan lemari agak menjauh dari dinding yang lembap atau area bocor. Kelembapan tinggi adalah penyebab utama karat dan berkas yang berjamur."},
      {h: "Rawat rel dan kunci", p: "Beri pelumas ringan pada rel laci atau rel pintu geser setiap beberapa bulan. Untuk kunci, cukup dibersihkan dari debu dan jangan dipaksa saat terasa seret."},
      {h: "Atur beban dengan merata", p: "Jangan menumpuk semua berkas berat di satu laci atau satu rak. Bagi beban secara merata agar rangka dan rel tidak cepat aus."}
    ]
  },
];
