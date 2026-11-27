# Desain key Redis 

|Pola key|Tipe|Isi|Sumber MySQL|
|-|-|-|-|
|`laporan:{id\_laporan}`|HASH|id\_laporan, id\_pengguna, alamat, status, waktu\_lapor, tingkat\_keparahan, foto, latitude, longitude|laporan|
|`hasil\_deteksi:{id\_laporan}`|HASH|id\_deteksi, jenis\_kerusakan, tingkat\_keyakinan, kotak\_batas (JSON string), detail\_deteksi (JSON string)|hasil\_deteksi (id\_deteksi terbesar per laporan)|
|`pengguna:{id\_pengguna}`|HASH|id\_pengguna, nama, id\_role, nama\_role|pengguna JOIN role (tanpa email/password)|
|`idx:status:{status}:laporan`|ZSET|member = id\_laporan, score = waktu\_lapor (Unix UTC)|laporan.status, waktu\_lapor|
|`stats:status`|HASH|jumlah laporan per status|COUNT GROUP BY status|
|`idx:prioritas:laporan`|ZSET|score = bobot keparahan x tingkat\_keyakinan|laporan.tingkat\_keparahan + hasil\_deteksi (status bukan Selesai)|
|`idx:lokasi:laporan`|GEO|koordinat laporan|laporan.latitude, longitude|
|`riwayat:laporan:{id\_laporan}`|LIST|id\_riwayat berurutan waktu|riwayat\_status|
|`riwayat:{id\_riwayat}`|HASH|id\_riwayat, id\_laporan, id\_pengguna, waktu\_perubahan, status\_baru, catatan|riwayat\_status|
|`seq:riwayat`|STRING|id\_riwayat terakhir (INCR untuk id baru)|MAX(id\_riwayat)|
|`session:{token}`|STRING (JSON)|id\_pengguna, role; TTL 30 menit|dibuat saat login|



