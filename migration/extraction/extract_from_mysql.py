"""Tahap 1 - Ekstraksi: ambil data terpilih dari db_kerusakan_jalan (MySQL) dan simpan sebagai JSON.
Kolom sensitif (email, password) sengaja TIDAK diambil."""
import json
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from keys import MYSQL_CFG, OUT_DIR  # noqa: E402

LAPORAN_SQL = """
SELECT id_laporan, id_pengguna, tingkat_keparahan, foto, latitude, longitude,
       alamat, waktu_lapor, status
FROM laporan ORDER BY id_laporan"""

# Satu hasil deteksi TERBARU (id_deteksi terbesar) per laporan.
DETEKSI_SQL = """
SELECT h.id_deteksi, h.id_laporan, h.jenis_kerusakan, h.kotak_batas,
       h.tingkat_keyakinan, h.detail_deteksi
FROM hasil_deteksi h
WHERE h.id_deteksi = (SELECT MAX(h2.id_deteksi) FROM hasil_deteksi h2
                      WHERE h2.id_laporan = h.id_laporan)
ORDER BY h.id_laporan"""

PENGGUNA_SQL = """
SELECT p.id_pengguna, p.nama, p.id_role, r.nama_role
FROM pengguna p JOIN role r ON r.id_role = p.id_role
ORDER BY p.id_pengguna"""

RIWAYAT_SQL = """
SELECT id_riwayat, id_laporan, id_pengguna, waktu_perubahan, status_baru, catatan
FROM riwayat_status ORDER BY id_laporan, waktu_perubahan, id_riwayat"""


def _jsonable(v):
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, datetime):
        return v.isoformat(timespec="seconds")
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, (bytes, bytearray)):
        return v.decode("utf-8")
    return v


def _fetch_all(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    cols = [c[0] for c in cur.description]
    rows = [{c: _jsonable(v) for c, v in zip(cols, row)} for row in cur.fetchall()]
    cur.close()
    return rows


def extract(conn) -> dict:
    data = {
        "laporan": _fetch_all(conn, LAPORAN_SQL),
        "hasil_deteksi": _fetch_all(conn, DETEKSI_SQL),
        "pengguna": _fetch_all(conn, PENGGUNA_SQL),
        "riwayat_status": _fetch_all(conn, RIWAYAT_SQL),
    }
    data["source_counts"] = {
        t: _fetch_all(conn, f"SELECT COUNT(*) AS n FROM {t}")[0]["n"]
        for t in ("role", "pengguna", "laporan", "hasil_deteksi", "riwayat_status")
    }
    return data


def main():
    import mysql.connector  # pip install mysql-connector-python

    conn = mysql.connector.connect(**MYSQL_CFG)
    try:
        data = extract(conn)
    finally:
        conn.close()
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / "mysql_extract.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[extract] jumlah baris sumber    : {data['source_counts']}")
    print(f"[extract] laporan diambil        : {len(data['laporan'])}")
    print(f"[extract] deteksi terbaru        : {len(data['hasil_deteksi'])}")
    print(f"[extract] pengguna / riwayat     : {len(data['pengguna'])} / {len(data['riwayat_status'])}")
    print(f"[extract] disimpan ke            : {out}")


if __name__ == "__main__":
    main()
