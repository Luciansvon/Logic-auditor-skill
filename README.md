# Logic Audit Panel

Skill Codex untuk mengaudit rancangan, produk fisik, software, dan workflow dari beberapa sudut pandang. Panel mencari masalah yang sudah terlihat dan skenario kegagalan yang baru muncul saat kondisi berubah. [Buka instruksi skill](logic-audit-panel/SKILL.md)

```text
Tujuan + bukti yang tersedia
            ↓
  2–3 auditor menilai sendiri
            ↓
  Uji silang temuan penting
            ↓
  Tier risiko + tindakan + cara menguji
```

## Pasang di Codex

Jalankan di PowerShell.

```powershell
git clone https://github.com/Luciansvon/Logic-auditor-skill.git
$skillTarget = Join-Path $env:USERPROFILE '.agents\skills\logic-audit-panel'
New-Item -ItemType Directory -Path $skillTarget -Force | Out-Null
Copy-Item -LiteralPath '.\Logic-auditor-skill\logic-audit-panel\SKILL.md' -Destination $skillTarget
```

Panggil `$logic-audit-panel` di chat Codex. Jika skill belum muncul di pemilih, buka ulang Codex. [Dokumentasi skill Codex](https://learn.chatgpt.com/docs/build-skills)

## Coba satu audit

```text
$logic-audit-panel Audit desain sepatu prototipe ini sebelum uji lapangan
kurir motor. Cari masalah yang terlihat sekarang dan skenario gagal saat
dipakai hujan selama tujuh hari. Bedakan bukti dari dugaan dan sarankan
uji yang paling penting sebelum hari pertama.
```

Auditor dipilih sesuai konteks. Untuk sepatu kurir, panel bisa memeriksa struktur dan sambungan, gerakan pemakai di permukaan basah, dan variasi antarunit. Untuk software, panel bisa menelusuri aturan bisnis, data, dependensi, dan perubahan versi. Kirim gambar, data uji, log, atau kode yang bisa dijadikan bukti.

Setiap auditor membuat penilaian awal di konteks terpisah. Moderator kemudian menguji temuan yang paling berpengaruh terhadap keputusan. Jika hanya satu agen yang tersedia, laporan mencantumkan mode satu agen dan sudut pandang yang diperiksa.

## Tier risiko

| Tier | Arti praktis |
| --- | --- |
| P0 · Kritis | Batasi paparan sekarang bila dampaknya berat dan jalur paparan didukung bukti kuat. |
| P1 · Tinggi | Uji atau tangani sebelum keputusan atau paparan berikutnya. Tier dapat bersifat sementara jika bukti penentu belum lengkap. |
| P2 · Sedang | Jadwalkan perbaikan atau uji, lalu tentukan kapan perlu menaikkan prioritas. |
| P3 · Rendah | Pantau atau tangani saat relevan. |

Laporan menunjukkan status bukti tiap temuan, pemicu dan dampaknya, serta tindakan atau uji pembeda. Untuk risiko ke depan, laporan juga menyebut kapan atau pada kondisi apa risiko muncul.

## Bukti validasi

| Pemeriksaan | Hasil yang diamati |
| --- | --- |
| Validator bawaan Codex | `Skill is valid!` |
| Discovery di app-server Codex | `skills/list: logic-audit-panel` tercatat dengan `scope=user` dan `enabled=True`. |
| Kasus sintetis sepatu kurir | Dua subagent menyelesaikan penilaian awal terpisah dan dua uji silang. Tumit naik-turun pada satu pasang dilaporkan sebagai temuan terkonfirmasi. Traksi di keramik basah menjadi P1 sementara karena paparan sudah dijadwalkan dan bukti uji masih kurang. |
| Kasus sintetis preorder, mode satu agen | Laporan menyatakan `0 subagent`. Dua pencatatan reserve sukses untuk satu event diklasifikasikan sebagai kejadian terkonfirmasi. Pembayaran yang masuk setelah auto-cancel diklasifikasikan sebagai skenario P1 sementara. |

Validasi ini mengecek perilaku skill pada brief dan log sintetis. Uji fisik sepatu dan uji staging yang muncul di laporan merupakan usulan verifikasi.

Cara kerja skill mengadaptasi analisis mode kegagalan, premortem, dan penilaian berbasis bukti saat auditor berbeda pendapat. [Panduan FMECA NASA](https://standards.nasa.gov/standard/GSFC/GSFC-HDBK-8004) · [Gary Klein, Performing a Project Premortem](https://hbr.org/2007/09/performing-a-project-premortem) · [Studi tentang pengaruh persuasi dalam debat multiagen](https://www.nature.com/articles/s41598-026-42705-7)
