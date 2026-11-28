# Desain Struktur Data Redis

| Key | Tipe | Isi | Sumber MySQL |
|---|---|---|---|
| `laporan:{id_laporan}` | HASH | id_laporan, id_pengguna, tingkat_keparahan, foto, latitude, longitude, alamat, waktu_lapor, status | `laporan` (tanpa `keterangan`) |
| `hasil_deteksi:{id_laporan}` | HASH | id_deteksi, id_laporan, jenis_kerusakan, kotak_batas, tingkat_keyakinan, detail_deteksi | `hasil_deteksi` (id_deteksi terbesar per laporan) |
| `pengguna:{id_pengguna}` | HASH | id_pengguna, id_role, nama_role, nama | `pengguna` JOIN `role` (tanpa email, password) |
| `idx:status:{status}:laporan` | ZSET | member id_laporan, skor = waktu_lapor (Unix UTC) | `laporan.status`, `waktu_lapor` |
| `stats:status` | HASH | menunggu, diproses, selesai (counter) | jumlah anggota tiap ZSET status |
| `idx:prioritas:laporan` | ZSET | skor = bobot keparahan x tingkat_keyakinan | laporan belum Selesai yang punya deteksi |
| `idx:lokasi:laporan` | GEO | member id_laporan | `latitude`, `longitude` |
| `riwayat:{id_riwayat}` | HASH | semua kolom riwayat | `riwayat_status` |
| `riwayat:laporan:{id_laporan}` | LIST | id_riwayat berurutan menurut waktu | `riwayat_status` |
| `seq:riwayat` | STRING | id riwayat terakhir (untuk INCR) | MAX(`id_riwayat`) |
| `sesi:{token}` | STRING + TTL | sesi login (dibuat aplikasi, tidak dimigrasi) | - |

Bobot keparahan: Rendah = 1, Sedang = 2, Tinggi = 3. Nama status pada key memakai huruf kecil,
nilai field `status` tetap seperti di MySQL (Menunggu / Diproses / Selesai).

## Tidak dimigrasikan
email dan password (sensitif), `keterangan` (teks panjang), hasil deteksi lama (id_deteksi 2),
tabel `role` (cukup `nama_role`), file foto.

## Aturan konsistensi
MySQL adalah sumber utama. Aplikasi menulis ke MySQL dulu, lalu memperbarui Redis dalam satu
`MULTI/EXEC`. Bila berbeda, jalankan ulang `migration/loading/load_to_redis.py`.
