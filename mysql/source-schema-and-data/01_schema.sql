CREATE DATABASE IF NOT EXISTS db_kerusakan_jalan CHARACTER SET utf8mb4;
USE db_kerusakan_jalan;

CREATE TABLE role (
  id_role   INT AUTO_INCREMENT PRIMARY KEY,
  nama_role VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE pengguna (
  id_pengguna INT AUTO_INCREMENT PRIMARY KEY,
  id_role     INT NOT NULL,
  nama        VARCHAR(100) NOT NULL,
  email       VARCHAR(100) NOT NULL UNIQUE,
  password    VARCHAR(255) NOT NULL,
  FOREIGN KEY (id_role) REFERENCES role(id_role)
) ENGINE=InnoDB;

CREATE TABLE laporan (
  id_laporan       INT AUTO_INCREMENT PRIMARY KEY,
  id_pengguna      INT NOT NULL,
  tingkat_keparahan VARCHAR(50),
  foto             VARCHAR(255),
  latitude         DECIMAL(10,7),
  longitude        DECIMAL(10,7),
  alamat           TEXT,
  keterangan       TEXT,
  waktu_lapor      DATETIME DEFAULT CURRENT_TIMESTAMP,
  status           VARCHAR(50),
  FOREIGN KEY (id_pengguna) REFERENCES pengguna(id_pengguna)
) ENGINE=InnoDB;

CREATE TABLE hasil_deteksi (
  id_deteksi       INT AUTO_INCREMENT PRIMARY KEY,
  id_laporan       INT NOT NULL,
  jenis_kerusakan  VARCHAR(100),
  kotak_batas      JSON,
  tingkat_keyakinan DECIMAL(5,2),
  detail_deteksi   JSON,
  FOREIGN KEY (id_laporan) REFERENCES laporan(id_laporan)
) ENGINE=InnoDB;

CREATE TABLE riwayat_status (
  id_riwayat       INT AUTO_INCREMENT PRIMARY KEY,
  id_laporan       INT NOT NULL,
  id_pengguna      INT NOT NULL,
  waktu_perubahan  DATETIME DEFAULT CURRENT_TIMESTAMP,
  status_baru      VARCHAR(50),
  catatan          TEXT,
  FOREIGN KEY (id_laporan)  REFERENCES laporan(id_laporan),
  FOREIGN KEY (id_pengguna) REFERENCES pengguna(id_pengguna)
) ENGINE=InnoDB;

CREATE INDEX idx_status ON laporan(status);
