USE db_kerusakan_jalan;

INSERT INTO role (id_role, nama_role) VALUES
(1,'Admin'),
(2,'Petugas'),
(3,'Pelapor');

INSERT INTO pengguna (id_pengguna, id_role, nama, email, password) VALUES
(1,3,'Andi','andi@gmail.com','12345678'),
(2,3,'Budi','budi@gmail.com','12345678'),
(3,3,'Citra','citra@gmail.com','12345678'),
(4,2,'Petugas Lapangan','petugas@gmail.com','12345678'),
(5,1,'Admin Sistem','admin@gmail.com','12345678');

INSERT INTO laporan (id_laporan, id_pengguna, tingkat_keparahan, foto, latitude, longitude, alamat, keterangan, waktu_lapor, status) VALUES
(1,1,'Tinggi','jalan_rusak1.jpg',-7.4700000,112.4400000,'Jl. Raya Mojokerto','Terdapat lubang besar pada jalan','2026-11-01 08:30:00','Diproses'),
(2,1,'Sedang','jalan_rusak2.jpg',-7.4750000,112.4450000,'Jl. Gajah Mada','Permukaan jalan mengalami retakan','2026-11-02 10:15:00','Menunggu'),
(3,2,'Tinggi','jalan_rusak3.jpg',-7.4800000,112.4500000,'Jl. Majapahit','Kerusakan jalan cukup parah','2026-11-03 13:20:00','Selesai'),
(4,3,'Rendah','jalan_rusak4.jpg',-7.4850000,112.4550000,'Jl. Pahlawan','Terdapat retakan kecil pada jalan','2026-11-04 09:00:00','Diproses'),
(5,2,'Tinggi','jalan_rusak5.jpg',-7.4700500,112.4400500,'Jl. Raya Mojokerto','Lubang dekat laporan sebelumnya','2026-11-05 07:40:00','Menunggu'),
(6,3,'Sedang','jalan_rusak6.jpg',-7.4760000,112.4460000,'Jl. Gajah Mada','Retakan memanjang di sisi kiri','2026-11-06 15:10:00','Menunggu'),
(7,1,'Tinggi','jalan_rusak7.jpg',-7.4900000,112.4600000,'Jl. Empunala','Lubang besar di tikungan','2026-11-07 06:50:00','Diproses'),
(8,2,'Rendah','jalan_rusak8.jpg',-7.4950000,112.4650000,'Jl. Mayjen Sungkono','Retakan halus','2026-11-08 11:25:00','Selesai'),
(9,3,'Sedang','jalan_rusak9.jpg',-7.4600000,112.4300000,'Jl. Raya Gedeg','Lubang sedang di dekat pasar','2026-11-09 16:05:00','Menunggu'),
(10,1,'Tinggi','jalan_rusak10.jpg',-7.4650000,112.4350000,'Jl. Bypass Mojokerto','Lubang besar di tepi jalan','2026-11-10 07:15:00','Diproses'),
(11,2,'Sedang','jalan_rusak11.jpg',-7.4720000,112.4420000,'Jl. Pahlawan','Retakan kulit buaya','2026-11-11 08:00:00','Diproses'),
(12,3,'Rendah','jalan_rusak12.jpg',-7.4880000,112.4580000,'Jl. Majapahit','Foto buram, menunggu analisis AI','2026-11-12 09:30:00','Menunggu');

INSERT INTO hasil_deteksi (id_deteksi, id_laporan, jenis_kerusakan, kotak_batas, tingkat_keyakinan, detail_deteksi) VALUES
(1,1,'Lubang Jalan','{"x":120,"y":80,"width":200,"height":150}',95.50,'{"diameter_cm":45,"kedalaman_cm":8}'),
(2,2,'Retakan Jalan','{"x":50,"y":60,"width":180,"height":90}',89.75,'{"panjang_m":1.2,"lebar_retak_mm":2}'),
(3,3,'Lubang Jalan','{"x":100,"y":100,"width":250,"height":180}',97.20,'{"diameter_cm":60,"kedalaman_cm":12}'),
(4,4,'Retakan Jalan','{"x":70,"y":40,"width":120,"height":60}',85.30,'{"panjang_m":1.5,"lebar_retak_mm":3}'),
(5,5,'Lubang Jalan','{"x":120,"y":80,"width":200,"height":150}',93.10,'{"diameter_cm":40,"kedalaman_cm":7}'),
(6,6,'Retakan Jalan','{"x":50,"y":60,"width":180,"height":90}',88.40,'{"panjang_m":2.0,"lebar_retak_mm":4}'),
(7,7,'Lubang Jalan','{"x":100,"y":100,"width":250,"height":180}',96.00,'{"diameter_cm":55,"kedalaman_cm":11}'),
(8,8,'Retakan Jalan','{"x":70,"y":40,"width":120,"height":60}',80.20,'{"panjang_m":0.8,"lebar_retak_mm":1}'),
(9,9,'Lubang Jalan','{"x":120,"y":80,"width":200,"height":150}',86.70,'{"diameter_cm":30,"kedalaman_cm":5}'),
(10,10,'Lubang Jalan','{"x":100,"y":100,"width":250,"height":180}',94.80,'{"diameter_cm":58,"kedalaman_cm":10}'),
(11,11,'Retakan Jalan','{"x":50,"y":60,"width":180,"height":90}',90.50,'{"panjang_m":2.5,"lebar_retak_mm":5}'),
(13,2,'Retakan Jalan','{"x":50,"y":60,"width":180,"height":90}',91.30,'{"panjang_m":1.6,"lebar_retak_mm":3}');

INSERT INTO riwayat_status (id_riwayat, id_laporan, id_pengguna, waktu_perubahan, status_baru, catatan) VALUES
(1,1,1,'2026-11-01 08:30:00','Menunggu','Laporan dibuat oleh pelapor'),
(2,1,4,'2026-11-02 08:30:00','Diproses','Laporan diverifikasi petugas'),
(3,2,1,'2026-11-02 10:15:00','Menunggu','Laporan dibuat oleh pelapor'),
(4,3,2,'2026-11-03 13:20:00','Menunggu','Laporan dibuat oleh pelapor'),
(5,3,4,'2026-11-04 13:20:00','Diproses','Laporan diverifikasi petugas'),
(6,3,4,'2026-11-06 13:20:00','Selesai','Perbaikan selesai'),
(7,4,3,'2026-11-04 09:00:00','Menunggu','Laporan dibuat oleh pelapor'),
(8,4,4,'2026-11-05 09:00:00','Diproses','Laporan diverifikasi petugas'),
(9,5,2,'2026-11-05 07:40:00','Menunggu','Laporan dibuat oleh pelapor'),
(10,6,3,'2026-11-06 15:10:00','Menunggu','Laporan dibuat oleh pelapor'),
(11,7,1,'2026-11-07 06:50:00','Menunggu','Laporan dibuat oleh pelapor'),
(12,7,4,'2026-11-08 06:50:00','Diproses','Laporan diverifikasi petugas'),
(13,8,2,'2026-11-08 11:25:00','Menunggu','Laporan dibuat oleh pelapor'),
(14,8,4,'2026-11-09 11:25:00','Diproses','Laporan diverifikasi petugas'),
(15,8,4,'2026-11-11 11:25:00','Selesai','Perbaikan selesai'),
(16,9,3,'2026-11-09 16:05:00','Menunggu','Laporan dibuat oleh pelapor'),
(17,10,1,'2026-11-10 07:15:00','Menunggu','Laporan dibuat oleh pelapor'),
(18,10,4,'2026-11-11 07:15:00','Diproses','Laporan diverifikasi petugas'),
(19,11,2,'2026-11-11 08:00:00','Menunggu','Laporan dibuat oleh pelapor'),
(20,11,4,'2026-11-12 08:00:00','Diproses','Laporan diverifikasi petugas'),
(21,12,3,'2026-11-12 09:30:00','Menunggu','Laporan dibuat oleh pelapor');
