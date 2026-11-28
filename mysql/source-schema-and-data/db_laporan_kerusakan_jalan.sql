-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 28, 2026 at 01:45 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_laporan_kerusakan_jalan`
--

-- --------------------------------------------------------

--
-- Table structure for table `hasil_deteksi`
--

CREATE TABLE `hasil_deteksi` (
  `id_deteksi` int NOT NULL,
  `id_laporan` int NOT NULL,
  `jenis_kerusakan` varchar(100) DEFAULT NULL,
  `kotak_batas` json DEFAULT NULL,
  `tingkat_keyakinan` decimal(5,2) DEFAULT NULL,
  `detail_deteksi` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `hasil_deteksi`
--

INSERT INTO `hasil_deteksi` (`id_deteksi`, `id_laporan`, `jenis_kerusakan`, `kotak_batas`, `tingkat_keyakinan`, `detail_deteksi`) VALUES
(1, 1, 'Lubang Jalan', '{\"x\": 120, \"y\": 80, \"width\": 200, \"height\": 150}', '95.50', '{\"diameter_cm\": 45, \"kedalaman_cm\": 8}'),
(2, 2, 'Retakan Jalan', '{\"x\": 50, \"y\": 60, \"width\": 180, \"height\": 90}', '89.75', '{\"panjang_m\": 1.2, \"lebar_retak_mm\": 2}'),
(3, 3, 'Lubang Jalan', '{\"x\": 100, \"y\": 100, \"width\": 250, \"height\": 180}', '97.20', '{\"diameter_cm\": 60, \"kedalaman_cm\": 12}'),
(4, 4, 'Retakan Jalan', '{\"x\": 70, \"y\": 40, \"width\": 120, \"height\": 60}', '85.30', '{\"panjang_m\": 1.5, \"lebar_retak_mm\": 3}'),
(5, 5, 'Lubang Jalan', '{\"x\": 120, \"y\": 80, \"width\": 200, \"height\": 150}', '93.10', '{\"diameter_cm\": 40, \"kedalaman_cm\": 7}'),
(6, 6, 'Retakan Jalan', '{\"x\": 50, \"y\": 60, \"width\": 180, \"height\": 90}', '88.40', '{\"panjang_m\": 2.0, \"lebar_retak_mm\": 4}'),
(7, 7, 'Lubang Jalan', '{\"x\": 100, \"y\": 100, \"width\": 250, \"height\": 180}', '96.00', '{\"diameter_cm\": 55, \"kedalaman_cm\": 11}'),
(8, 8, 'Retakan Jalan', '{\"x\": 70, \"y\": 40, \"width\": 120, \"height\": 60}', '80.20', '{\"panjang_m\": 0.8, \"lebar_retak_mm\": 1}'),
(9, 9, 'Lubang Jalan', '{\"x\": 120, \"y\": 80, \"width\": 200, \"height\": 150}', '86.70', '{\"diameter_cm\": 30, \"kedalaman_cm\": 5}'),
(10, 10, 'Lubang Jalan', '{\"x\": 100, \"y\": 100, \"width\": 250, \"height\": 180}', '94.80', '{\"diameter_cm\": 58, \"kedalaman_cm\": 10}'),
(11, 11, 'Retakan Jalan', '{\"x\": 50, \"y\": 60, \"width\": 180, \"height\": 90}', '90.50', '{\"panjang_m\": 2.5, \"lebar_retak_mm\": 5}'),
(13, 2, 'Retakan Jalan', '{\"x\": 50, \"y\": 60, \"width\": 180, \"height\": 90}', '91.30', '{\"panjang_m\": 1.6, \"lebar_retak_mm\": 3}');

-- --------------------------------------------------------

--
-- Table structure for table `laporan`
--

CREATE TABLE `laporan` (
  `id_laporan` int NOT NULL,
  `id_pengguna` int NOT NULL,
  `tingkat_keparahan` varchar(50) DEFAULT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `alamat` text,
  `keterangan` text,
  `waktu_lapor` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `laporan`
--

INSERT INTO `laporan` (`id_laporan`, `id_pengguna`, `tingkat_keparahan`, `foto`, `latitude`, `longitude`, `alamat`, `keterangan`, `waktu_lapor`, `status`) VALUES
(1, 1, 'Tinggi', 'jalan_rusak1.jpg', '-7.4700000', '112.4400000', 'Jl. Raya Mojokerto', 'Terdapat lubang besar pada jalan', '2026-11-01 08:30:00', 'Diproses'),
(2, 1, 'Sedang', 'jalan_rusak2.jpg', '-7.4750000', '112.4450000', 'Jl. Gajah Mada', 'Permukaan jalan mengalami retakan', '2026-11-02 10:15:00', 'Menunggu'),
(3, 2, 'Tinggi', 'jalan_rusak3.jpg', '-7.4800000', '112.4500000', 'Jl. Majapahit', 'Kerusakan jalan cukup parah', '2026-11-03 13:20:00', 'Selesai'),
(4, 3, 'Rendah', 'jalan_rusak4.jpg', '-7.4850000', '112.4550000', 'Jl. Pahlawan', 'Terdapat retakan kecil pada jalan', '2026-11-04 09:00:00', 'Diproses'),
(5, 2, 'Tinggi', 'jalan_rusak5.jpg', '-7.4700500', '112.4400500', 'Jl. Raya Mojokerto', 'Lubang dekat laporan sebelumnya', '2026-11-05 07:40:00', 'Menunggu'),
(6, 3, 'Sedang', 'jalan_rusak6.jpg', '-7.4760000', '112.4460000', 'Jl. Gajah Mada', 'Retakan memanjang di sisi kiri', '2026-11-06 15:10:00', 'Menunggu'),
(7, 1, 'Tinggi', 'jalan_rusak7.jpg', '-7.4900000', '112.4600000', 'Jl. Empunala', 'Lubang besar di tikungan', '2026-11-07 06:50:00', 'Diproses'),
(8, 2, 'Rendah', 'jalan_rusak8.jpg', '-7.4950000', '112.4650000', 'Jl. Mayjen Sungkono', 'Retakan halus', '2026-11-08 11:25:00', 'Selesai'),
(9, 3, 'Sedang', 'jalan_rusak9.jpg', '-7.4600000', '112.4300000', 'Jl. Raya Gedeg', 'Lubang sedang di dekat pasar', '2026-11-09 16:05:00', 'Menunggu'),
(10, 1, 'Tinggi', 'jalan_rusak10.jpg', '-7.4650000', '112.4350000', 'Jl. Bypass Mojokerto', 'Lubang besar di tepi jalan', '2026-11-10 07:15:00', 'Diproses'),
(11, 2, 'Sedang', 'jalan_rusak11.jpg', '-7.4720000', '112.4420000', 'Jl. Pahlawan', 'Retakan kulit buaya', '2026-11-11 08:00:00', 'Diproses'),
(12, 3, 'Rendah', 'jalan_rusak12.jpg', '-7.4880000', '112.4580000', 'Jl. Majapahit', 'Foto buram, menunggu analisis AI', '2026-11-12 09:30:00', 'Menunggu');

-- --------------------------------------------------------

--
-- Table structure for table `pengguna`
--

CREATE TABLE `pengguna` (
  `id_pengguna` int NOT NULL,
  `id_role` int NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pengguna`
--

INSERT INTO `pengguna` (`id_pengguna`, `id_role`, `nama`, `email`, `password`) VALUES
(1, 3, 'Andi', 'andi@gmail.com', '12345678'),
(2, 3, 'Budi', 'budi@gmail.com', '12345678'),
(3, 3, 'Citra', 'citra@gmail.com', '12345678'),
(4, 2, 'Petugas Lapangan', 'petugas@gmail.com', '12345678'),
(5, 1, 'Admin Sistem', 'admin@gmail.com', '12345678');

-- --------------------------------------------------------

--
-- Table structure for table `riwayat_status`
--

CREATE TABLE `riwayat_status` (
  `id_riwayat` int NOT NULL,
  `id_laporan` int NOT NULL,
  `id_pengguna` int NOT NULL,
  `waktu_perubahan` datetime DEFAULT CURRENT_TIMESTAMP,
  `status_baru` varchar(50) DEFAULT NULL,
  `catatan` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `riwayat_status`
--

INSERT INTO `riwayat_status` (`id_riwayat`, `id_laporan`, `id_pengguna`, `waktu_perubahan`, `status_baru`, `catatan`) VALUES
(1, 1, 1, '2026-11-01 08:30:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(2, 1, 4, '2026-11-02 08:30:00', 'Diproses', 'Laporan diverifikasi petugas'),
(3, 2, 1, '2026-11-02 10:15:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(4, 3, 2, '2026-11-03 13:20:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(5, 3, 4, '2026-11-04 13:20:00', 'Diproses', 'Laporan diverifikasi petugas'),
(6, 3, 4, '2026-11-06 13:20:00', 'Selesai', 'Perbaikan selesai'),
(7, 4, 3, '2026-11-04 09:00:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(8, 4, 4, '2026-11-05 09:00:00', 'Diproses', 'Laporan diverifikasi petugas'),
(9, 5, 2, '2026-11-05 07:40:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(10, 6, 3, '2026-11-06 15:10:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(11, 7, 1, '2026-11-07 06:50:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(12, 7, 4, '2026-11-08 06:50:00', 'Diproses', 'Laporan diverifikasi petugas'),
(13, 8, 2, '2026-11-08 11:25:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(14, 8, 4, '2026-11-09 11:25:00', 'Diproses', 'Laporan diverifikasi petugas'),
(15, 8, 4, '2026-11-11 11:25:00', 'Selesai', 'Perbaikan selesai'),
(16, 9, 3, '2026-11-09 16:05:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(17, 10, 1, '2026-11-10 07:15:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(18, 10, 4, '2026-11-11 07:15:00', 'Diproses', 'Laporan diverifikasi petugas'),
(19, 11, 2, '2026-11-11 08:00:00', 'Menunggu', 'Laporan dibuat oleh pelapor'),
(20, 11, 4, '2026-11-12 08:00:00', 'Diproses', 'Laporan diverifikasi petugas'),
(21, 12, 3, '2026-11-12 09:30:00', 'Menunggu', 'Laporan dibuat oleh pelapor');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `id_role` int NOT NULL,
  `nama_role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`id_role`, `nama_role`) VALUES
(1, 'Admin'),
(3, 'Pelapor'),
(2, 'Petugas');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `hasil_deteksi`
--
ALTER TABLE `hasil_deteksi`
  ADD PRIMARY KEY (`id_deteksi`),
  ADD KEY `id_laporan` (`id_laporan`);

--
-- Indexes for table `laporan`
--
ALTER TABLE `laporan`
  ADD PRIMARY KEY (`id_laporan`),
  ADD KEY `id_pengguna` (`id_pengguna`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`id_pengguna`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `id_role` (`id_role`);

--
-- Indexes for table `riwayat_status`
--
ALTER TABLE `riwayat_status`
  ADD PRIMARY KEY (`id_riwayat`),
  ADD KEY `id_laporan` (`id_laporan`),
  ADD KEY `id_pengguna` (`id_pengguna`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id_role`),
  ADD UNIQUE KEY `nama_role` (`nama_role`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `hasil_deteksi`
--
ALTER TABLE `hasil_deteksi`
  MODIFY `id_deteksi` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `laporan`
--
ALTER TABLE `laporan`
  MODIFY `id_laporan` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `pengguna`
--
ALTER TABLE `pengguna`
  MODIFY `id_pengguna` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `riwayat_status`
--
ALTER TABLE `riwayat_status`
  MODIFY `id_riwayat` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `id_role` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `hasil_deteksi`
--
ALTER TABLE `hasil_deteksi`
  ADD CONSTRAINT `hasil_deteksi_ibfk_1` FOREIGN KEY (`id_laporan`) REFERENCES `laporan` (`id_laporan`);

--
-- Constraints for table `laporan`
--
ALTER TABLE `laporan`
  ADD CONSTRAINT `laporan_ibfk_1` FOREIGN KEY (`id_pengguna`) REFERENCES `pengguna` (`id_pengguna`);

--
-- Constraints for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD CONSTRAINT `pengguna_ibfk_1` FOREIGN KEY (`id_role`) REFERENCES `role` (`id_role`);

--
-- Constraints for table `riwayat_status`
--
ALTER TABLE `riwayat_status`
  ADD CONSTRAINT `riwayat_status_ibfk_1` FOREIGN KEY (`id_laporan`) REFERENCES `laporan` (`id_laporan`),
  ADD CONSTRAINT `riwayat_status_ibfk_2` FOREIGN KEY (`id_pengguna`) REFERENCES `pengguna` (`id_pengguna`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
