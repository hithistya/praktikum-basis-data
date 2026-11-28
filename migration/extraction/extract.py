"""Tahap 1 - Ekstraksi: membaca data sumber dari MySQL.

Dua mode:
  * mysql : membaca langsung dari server MySQL (dipakai di praktikum).
  * dump  : membaca dari file .sql hasil ekspor phpMyAdmin (untuk uji tanpa server).

Keempat query sama persis dengan Bagian D.1 laporan.
"""
import os
import re
from pathlib import Path

QUERIES = {
    "laporan": "SELECT * FROM laporan",
    "hasil_deteksi": (
        "SELECT h.* FROM hasil_deteksi h "
        "WHERE h.id_deteksi = (SELECT MAX(id_deteksi) FROM hasil_deteksi "
        "WHERE id_laporan = h.id_laporan)"
    ),
    "pengguna": (
        "SELECT p.*, r.nama_role FROM pengguna p "
        "JOIN role r ON r.id_role = p.id_role"
    ),
    "riwayat_status": "SELECT * FROM riwayat_status ORDER BY waktu_perubahan, id_riwayat",
}


def extract_from_mysql():
    import mysql.connector  # pip install mysql-connector-python

    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "db_laporan_kerusakan_jalan"),
    )
    try:
        cur = conn.cursor(dictionary=True)
        data = {}
        for name, sql in QUERIES.items():
            cur.execute(sql)
            data[name] = cur.fetchall()
        return data
    finally:
        conn.close()


# ---------------------------------------------------------------- mode dump
_INSERT = re.compile(
    r"INSERT INTO `(\w+)` \(([^)]*)\) VALUES\s*(.*?);\s*\n", re.DOTALL
)
_ESC = {"n": "\n", "r": "\r", "t": "\t", "0": "\0", "Z": "\x1a"}


def _parse_values(text):
    rows, row, i, n = [], None, 0, len(text)
    while i < n:
        c = text[i]
        if row is None:
            if c == "(":
                row = []
            i += 1
        elif c in " \r\n\t,":
            i += 1
        elif c == ")":
            rows.append(row)
            row = None
            i += 1
        elif c == "'":
            i += 1
            buf = []
            while True:
                ch = text[i]
                if ch == "\\":
                    nxt = text[i + 1]
                    buf.append(_ESC.get(nxt, nxt))
                    i += 2
                elif ch == "'":
                    if text[i + 1:i + 2] == "'":
                        buf.append("'")
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    buf.append(ch)
                    i += 1
            row.append("".join(buf))
        else:
            j = i
            while text[j] not in ",)":
                j += 1
            tok = text[i:j].strip()
            row.append(None if tok.upper() == "NULL" else int(tok) if re.fullmatch(r"-?\d+", tok) else tok)
            i = j
    return rows


def read_dump(path):
    sql = Path(path).read_text(encoding="utf-8")
    tables = {}
    for table, cols, values in _INSERT.findall(sql):
        names = [c.strip(" `") for c in cols.split(",")]
        tables.setdefault(table, []).extend(
            dict(zip(names, r)) for r in _parse_values(values)
        )
    return tables


def extract_from_dump(path):
    t = read_dump(path)
    latest = {}
    for h in t["hasil_deteksi"]:
        cur = latest.get(h["id_laporan"])
        if cur is None or h["id_deteksi"] > cur["id_deteksi"]:
            latest[h["id_laporan"]] = h
    roles = {r["id_role"]: r["nama_role"] for r in t["role"]}
    return {
        "laporan": t["laporan"],
        "hasil_deteksi": sorted(latest.values(), key=lambda h: h["id_laporan"]),
        "pengguna": [dict(p, nama_role=roles[p["id_role"]]) for p in t["pengguna"]],
        "riwayat_status": sorted(
            t["riwayat_status"], key=lambda r: (r["waktu_perubahan"], r["id_riwayat"])
        ),
    }
