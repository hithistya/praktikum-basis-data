"""Tahap 2 - Transformasi: data relasional (MySQL) -> perintah Redis.

Aturan mengikuti tabel pemetaan (Bagian C laporan). Fungsi build_commands()
murni (tanpa koneksi), hasilnya daftar tuple perintah Redis, mis.
("HSET", "laporan:1", "id_laporan", "1", ...).
"""
import json
from datetime import datetime, timezone
from decimal import Decimal

LAPORAN_FIELDS = [  
    "id_laporan", "id_pengguna", "tingkat_keparahan", "foto",
    "latitude", "longitude", "alamat", "waktu_lapor", "status",
]
DETEKSI_FIELDS = [
    "id_deteksi", "id_laporan", "jenis_kerusakan", "kotak_batas",
    "tingkat_keyakinan", "detail_deteksi",
]
PENGGUNA_FIELDS = ["id_pengguna", "id_role", "nama_role", "nama"]  
RIWAYAT_FIELDS = [
    "id_riwayat", "id_laporan", "id_pengguna",
    "waktu_perubahan", "status_baru", "catatan",
]
BOBOT = {"rendah": 1, "sedang": 2, "tinggi": 3}


def s(v):
    """Semua nilai disimpan sebagai string; NULL menjadi string kosong."""
    if v is None:
        return ""
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(v, (dict, list)):
        return json.dumps(v, separators=(", ", ": "))
    return str(v)


def unix_utc(v):
    dt = v if isinstance(v, datetime) else datetime.strptime(s(v), "%Y-%m-%d %H:%M:%S")
    return int(dt.replace(tzinfo=timezone.utc).timestamp())


def hset(key, row, fields):
    args = []
    for f in fields:
        args += [f, s(row.get(f))]
    return ("HSET", key, *args)


def skor_prioritas(tingkat, keyakinan):
    d = Decimal(s(keyakinan)) * BOBOT[s(tingkat).lower()]
    return format(d.normalize(), "f")


def build_commands(data):
    cmds = []
    for r in data["laporan"]:
        cmds.append(hset(f"laporan:{r['id_laporan']}", r, LAPORAN_FIELDS))
    for r in data["hasil_deteksi"]:
        cmds.append(hset(f"hasil_deteksi:{r['id_laporan']}", r, DETEKSI_FIELDS))
    for r in data["pengguna"]:
        cmds.append(hset(f"pengguna:{r['id_pengguna']}", r, PENGGUNA_FIELDS))

    # indeks status + counter
    counter = {}
    for r in data["laporan"]:
        st = s(r["status"]).lower()
        counter[st] = counter.get(st, 0) + 1
        cmds.append(("ZADD", f"idx:status:{st}:laporan", str(unix_utc(r["waktu_lapor"])), s(r["id_laporan"])))
    for st, n in counter.items():
        cmds.append(("HSET", "stats:status", st, str(n)))

    # antrean prioritas: belum Selesai DAN sudah punya deteksi
    deteksi = {d["id_laporan"]: d for d in data["hasil_deteksi"]}
    for r in data["laporan"]:
        d = deteksi.get(r["id_laporan"])
        if d and s(r["status"]).lower() != "selesai":
            cmds.append(("ZADD", "idx:prioritas:laporan",
                         skor_prioritas(r["tingkat_keparahan"], d["tingkat_keyakinan"]),
                         s(r["id_laporan"])))

    # indeks lokasi (GEOADD: longitude dulu, lalu latitude)
    for r in data["laporan"]:
        cmds.append(("GEOADD", "idx:lokasi:laporan", s(r["longitude"]), s(r["latitude"]), s(r["id_laporan"])))

    # riwayat (data sudah terurut menurut waktu_perubahan)
    max_id = 0
    for r in data["riwayat_status"]:
        cmds.append(hset(f"riwayat:{r['id_riwayat']}", r, RIWAYAT_FIELDS))
        cmds.append(("RPUSH", f"riwayat:laporan:{r['id_laporan']}", s(r["id_riwayat"])))
        max_id = max(max_id, int(r["id_riwayat"]))
    cmds.append(("SET", "seq:riwayat", str(max_id)))
    return cmds


def ringkasan(cmds):
    """Jumlah objek yang akan dibuat; dipakai untuk dry-run dan validasi."""
    hset_keys = [c[1] for c in cmds if c[0] == "HSET"]
    return {
        "hash laporan": sum(k.startswith("laporan:") for k in hset_keys),
        "hash hasil_deteksi": sum(k.startswith("hasil_deteksi:") for k in hset_keys),
        "hash pengguna": sum(k.startswith("pengguna:") for k in hset_keys),
        "hash riwayat": sum(k.startswith("riwayat:") for k in hset_keys),
        "list riwayat:laporan": len({c[1] for c in cmds if c[0] == "RPUSH"}),
        "anggota zset status": sum(c[0] == "ZADD" and c[1].startswith("idx:status:") for c in cmds),
        "anggota zset prioritas": sum(c[0] == "ZADD" and c[1] == "idx:prioritas:laporan" for c in cmds),
        "anggota geo lokasi": sum(c[0] == "GEOADD" for c in cmds),
        "seq:riwayat": int(next(c[2] for c in cmds if c[0] == "SET")),
    }
