-- Empat query ekstraksi (Bagian D.1 laporan)
-- Database: db_laporan_kerusakan_jalan

    SELECT * FROM laporan;

    SELECT h.* FROM hasil_deteksi h
    WHERE h.id_deteksi = (SELECT MAX(id_deteksi) FROM hasil_deteksi WHERE id_laporan = h.id_laporan);

    SELECT p.*, r.nama_role FROM pengguna p JOIN role r ON r.id_role = p.id_role;

    SELECT * FROM riwayat_status ORDER BY waktu_perubahan;
