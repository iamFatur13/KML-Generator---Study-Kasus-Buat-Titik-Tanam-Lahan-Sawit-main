# KML-Generator---Study-Kasus-Buat-Titik-Tanam-Lahan-Sawit
Aplikasi yang lahir dari kebutuhan pribadi , mempunyai lahan sawit yang luas dan akan ditanami bibit, namun jika menggunakan penanaman manual titik tanam tidak presisi.



# 🌴Generator KML penentuan titik tanam bibit sawit (Metode Mata Lima)
Program Python interaktif untuk merencanakan tata letak penanaman kelapa sawit secara presisi menggunakan metode Mata Lima (Segitiga Sama Sisi). Program ini menghasilkan file KML yang siap digunakan di Google Earth, GPS Handheld, maupun aplikasi navigasi lapangan lainnya.

# 🚀 Fitur Utama
- Metode Mata Lima Otomatis: Menghitung posisi titik tanam dengan pola segitiga yang mengoptimalkan ruang tajuk dan penyerapan cahaya matahari.
- Input Jarak Tanam Dinamis: Mendukung berbagai ukuran (misal: 8x9, 9x9, dll) melalui input teks sederhana.
- Sempadan (Buffer) Kustom: Fitur untuk mengosongkan area dari batas lahan (dalam meter) guna memberikan ruang manuver alat berat atau akses jalan.
- Boundary & Ruas Marker: * Membuat poligon area lahan secara visual.
- Otomatis membuat titik bantu (Waypoint) di sepanjang garis batas setiap 10 meter untuk memudahkan pematokan (staking out) di lapangan.
- Visualisasi Hierarki KML: Output KML terbagi dalam folder yang rapi dengan ikon yang berbeda antara titik batas utama, titik ruas, dan titik tanam.
- Analisis Lahan: Memberikan laporan otomatis mengenai total luas lahan (dalam Hektar) dan estimasi jumlah bibit yang dibutuhkan.

# 🛠️ Prasyarat (Dependencies)
Sebelum menjalankan program, pastikan Anda telah menginstal library Python berikut:

Bash
<pre>pip install simplekml shapely numpy</pre>

## 📖 Cara Penggunaan
Jalankan Program:

Bash
<pre>python generator_sawit.py</pre>

Input Parameter:

- Masukkan jarak tanam (contoh: 8x9).
- Masukkan jarak buffer/sempadan dari batas luar (contoh: 2 untuk 2 meter).
- Masukkan jumlah titik koordinat batas lahan yang Anda miliki.
- Input Koordinat: Masukkan koordinat batas dalam format longitude, latitude (Contoh: 103.64423, -3.86290).
- Pilih Titik Awal: Pilih salah satu titik batas sebagai acuan (Anchor) dimulainya baris pertama penanaman.
- Selesai: Program akan menghasilkan file .kml di folder yang sama.

# 📂 Struktur Output KML

- Folder Batas Lahan: Berisi poligon area dan pin merah pada setiap sudut batas.
- Folder Ruas: Berisi titik penanda setiap 10m di sepanjang garis batas.
- Folder Titik Tanam: Berisi semua titik koordinat lubang tanam dengan ikon hijau.

# 📊 Contoh Laporan Output
<pre>
Plaintext
========================================
HASIL ANALISIS & GENERASI:
Total Luas Lahan     : 1.25 Hektar
Jarak Tanam          : 8.0m x 9.0m
Sempadan (Buffer)    : 2.0 meter
Total Kebutuhan Bibit: 168 Pokok
File Berhasil Dibuat : Rencana_Tanam_8x9_Lengkap.kml
========================================
</pre>


# ⚖️ Lisensi
Proyek ini dikembangkan untuk membantu manajemen perkebunan rakyat maupun industri agar lebih presisi dalam perencanaan lahan.
