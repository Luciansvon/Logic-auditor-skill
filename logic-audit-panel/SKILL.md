---
name: logic-audit-panel
description: Audit lintas aspek dengan subagent terpisah untuk mencari cacat logika saat ini, skenario gagal di masa depan, dan prioritas risiko pada rancangan, produk fisik, software, workflow, atau rencana. Gunakan saat diminta audit menyeluruh, cari blind spot, analisis mode kegagalan, atau premortem. Untuk satu bug atau pemeriksaan sempit, gunakan review langsung.
---

# Logic Audit Panel

Cari kombinasi penyebab yang bisa membuat tujuan gagal, termasuk saat setiap bagian tampak berfungsi sendiri. Moderator mengatur cakupan, memeriksa bukti, dan menyimpulkan. Auditor mengerjakan penilaian awal secara terpisah. Audit hanya membaca dan memeriksa dalam lingkup yang diizinkan. Sampaikan perubahan sebagai rekomendasi kecuali implementasi juga diminta.

## 1. Petakan objek dan pilih auditor

- Catat tujuan, ukuran keberhasilan, pengguna atau pihak terdampak, kondisi pemakaian, batas, dan horizon yang relevan. Petakan alur atau bagian utama beserta hubungan dan asumsi yang dibutuhkan agar semuanya berfungsi. Jika data belum lengkap, lanjutkan dengan asumsi yang disebutkan. Ajukan satu pertanyaan jika jawabannya menentukan apakah audit bisa dilakukan dengan bermakna.
- Pilih 2–3 auditor dengan tugas yang berbeda sesuai objek. Untuk sepatu, contoh pembagiannya adalah struktur dan material, pemakaian dan lingkungan, serta produksi dan variasi antarunit. Untuk software, contoh pembagiannya adalah aturan bisnis dan state, interaksi pengguna dan dependensi, serta perubahan versi dan pemulihan. Sesuaikan dengan keputusan yang mau diambil dan tunjuk siapa memeriksa hubungan yang berisiko di antara lensa. Catat aspek penting yang luput dari cakupan.

## 2. Jalankan penilaian terpisah

- Luncurkan 2–3 subagent sungguhan bila tersedia dan diizinkan. Pakai konteks baru tanpa riwayat diskusi jika tool mendukungnya. Beri semua auditor brief fakta dan akses bukti yang sama, dengan mandat dan pertanyaan khusus sesuai lensa masing-masing. Tahan dugaan moderator dan hasil auditor lain sampai penilaian awal masuk. Kerjakan paralel jika memungkinkan.
- Minta tiap auditor menguji dua hal. Untuk **saat ini**, bandingkan perilaku atau desain yang terlihat dengan aturan atau tujuan yang seharusnya. Untuk **ke depan**, bayangkan tujuan gagal pada horizon yang relevan, lalu telusuri pemicu dan mekanismenya. Uji juga satu interaksi lintas bagian atau lensa. Gunakan kondisi normal, batas pemakaian, perubahan, atau pemulihan yang relevan. Auditor boleh melaporkan bahwa buktinya belum cukup atau tidak menemukan risiko material pada lensa tersebut.
- Minta paling banyak tiga temuan material per auditor. Tiap temuan memuat kondisi/pemicu → mekanisme → dampak, status, rujukan bukti atau asumsi, serta cara menguji atau membantahnya. Catat konflik jika perbaikan menggeser risiko ke bagian lain. Bila memakai uji yang tersedia di proyek atau infrastruktur bersama, tautkan hasil aktual. Tandai setiap usulan uji yang belum dijalankan.
- Jika auditor gagal atau kapasitas penuh, coba sekali dengan konteks lebih kecil atau jalankan secara berurutan. Jika tetap kurang dari dua subagent yang mengembalikan penilaian awal, lanjutkan dengan lensa yang masih berguna dan laporkan jumlah auditor yang benar-benar selesai. Jika semuanya dikerjakan satu agen, sebut hasilnya **audit satu agen, beberapa sudut pandang**. Catat lensa yang belum terliput.

## 3. Uji silang dan urutkan risiko

- Bedakan **terkonfirmasi** (bukti langsung menunjukkan temuan), **indikasi** (ada sinyal saat ini, mekanisme belum teruji), dan **skenario** (risiko ke depan yang bersyarat). Pecah gejala dan dugaan penyebab bila status buktinya berbeda. Cantumkan keyakinan tinggi/sedang/rendah beserta alasannya jika memengaruhi keputusan.
- Satukan temuan yang mempunyai mekanisme dan dampak sama. Periksa rantai yang melintasi beberapa lensa dan efek samping solusi. Untuk temuan teratas atau yang diperdebatkan, minta satu auditor lain menantang asumsi, menelusuri sumber, atau mengusulkan uji pembeda setelah penilaian awal terkumpul. Jika auditor lain tidak tersedia, moderator memeriksa langsung dan menyebut bahwa pemeriksaan dilakukan sendiri. Utamakan bukti terkuat. Pertahankan temuan minoritas yang masih masuk akal dan tulis bukti yang bisa menyelesaikan selisihnya. Persetujuan beberapa auditor yang memakai bukti sama dihitung sebagai satu dasar bukti.

Tentukan tier dari dampak, peluang atau frekuensi paparan, dan kapan keputusan harus dibuat. Untuk kejadian yang sudah terjadi, nilai peluang terulang jika relevan. Gunakan label kualitatif. Jika data peluang belum ada, isi **belum diketahui** dan sebutkan efeknya pada tier.

| Tier | Kapan dipakai | Tindakan yang disarankan |
| --- | --- | --- |
| P0 Kritis | Dampak berat dan tidak mudah dipulihkan, seperti bahaya serius atau hilangnya fungsi utama, dengan bukti kejadian atau jalur paparan yang kuat dan mendesak | Tahan atau batasi paparan sekarang, lalu verifikasi mitigasi |
| P1 Tinggi | Dampak besar dengan jalur yang masuk akal, atau skenario berat dengan pemicu yang belum terverifikasi dan paparan dalam waktu dekat | Uji atau tangani sebelum keputusan atau paparan berikutnya. Tandai **sementara** bila fakta penentu masih hilang |
| P2 Sedang | Gangguan nyata dengan dampak terbatas, dapat dipulihkan, atau paparan rendah yang didukung bukti | Jadwalkan perbaikan atau uji. Tetapkan pemicu untuk menaikkan prioritas |
| P3 Rendah | Dampak kecil dan mudah ditangani | Pantau atau perbaiki saat relevan |

Jelaskan penentu tier untuk temuan penting. Keyakinan pada bukti dan tier risiko menjawab dua pertanyaan berbeda. Jika fakta yang hilang dapat menggeser tier, tulis kondisi yang menaikkan atau menurunkannya. Jangan isi tier yang kosong demi meratakan laporan.

## 4. Serahkan hasil yang bisa dipakai

Mulai dengan temuan paling mendesak dan tindakan berikutnya. Tampilkan jumlah auditor yang selesai dan lensa yang diperiksa. Gunakan format ringkas berikut dan lanjutkan dengan perbedaan pendapat atau kekurangan bukti yang bisa mengubah keputusan.

| Tier dan status | Pemicu → kegagalan → dampak | Bukti atau asumsi | Uji atau tindakan |
| --- | --- | --- | --- |

Untuk skenario masa depan, tambahkan horizon atau kondisi pemicu yang dapat diamati. Untuk tindakan teratas, beri kriteria lolos/gagal yang dapat diperiksa, atau sebutkan data yang diperlukan untuk menetapkan ambangnya. Jika perlu mengecek klaim teknis di luar materi audit, utamakan sumber primer atau hasil uji. Pakai laporan pengguna dan diskusi praktisi untuk menemukan pola pemakaian yang perlu diuji.
