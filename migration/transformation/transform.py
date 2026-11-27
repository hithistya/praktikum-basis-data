"""Tahap 2 - Transformasi: ubah baris relasional menjadi struktur Redis.
Menghasilkan redis_payload.json (untuk load_to_redis.py) dan migrasi_data.redis"""
import calendar
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from keys import (BOBOT_KEPARAHAN, KEY_GEO, KEY_PRIORITAS, KEY_SEQ_RIWAYAT, KEY_STATS,  # noqa: E402
                  OUT_DIR, STATUSES, key_deteksi, key_laporan, key_pengguna, key_riwayat,
                  key_riwayat_list, key_status_idx)


def _dt(v):
    return datetime.fromisoformat(str(v).replace("T", " "))


def _fmt(v):
    return _dt(v).strftime("%Y-%m-%d %H:%M:%S")


def _unix(v):
    """Unix timestamp (detik). waktu_lapor diperlakukan sebagai UTC, sama seperti Modul 12."""
    return calendar.timegm(_dt(v).timetuple())


def _json(v):
    """Kolom JSON MySQL -> string JSON ringkas; NULL -> string kosong (Redis tidak punya NULL)."""
    if v is None:
        return ""
    obj = json.loads(v) if isinstance(v, str) else v
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def laporan_fields(r):
    return {
        "id_laporan": str(r["id_laporan"]), "id_pengguna": str(r["id_pengguna"]),
        "alamat": r["alamat"] or "", "status": r["status"] or "",
        "waktu_lapor": _fmt(r["waktu_lapor"]), "tingkat_keparahan": r["tingkat_keparahan"] or "",
        "foto": r["foto"] or "",
        "latitude": f"{float(r['latitude']):.7f}", "longitude": f"{float(r['longitude']):.7f}",
    }


def deteksi_fields(d):
    return {
        "id_deteksi": str(d["id_deteksi"]), "jenis_kerusakan": d["jenis_kerusakan"] or "",
        "tingkat_keyakinan": f"{float(d['tingkat_keyakinan']):.2f}",
        "kotak_batas": _json(d["kotak_batas"]), "detail_deteksi": _json(d["detail_deteksi"]),
    }


def priority_score(lap, det):
    """Skor = bobot keparahan x tingkat keyakinan (0-100). Hanya laporan belum selesai yang sudah punya deteksi."""
    if det is None or (lap["status"] or "").lower() == "selesai":
        return None
    w = BOBOT_KEPARAHAN.get((lap["tingkat_keparahan"] or "").lower(), 1)
    return round(w * float(det["tingkat_keyakinan"]), 2)


def build_payload(ex: dict) -> dict:
    det_by = {d["id_laporan"]: d for d in ex["hasil_deteksi"]}
    laporan, deteksi, status_index, prioritas, geo, skipped = [], [], {s: {} for s in STATUSES}, {}, [], []
    for r in ex["laporan"]:
        i = r["id_laporan"]
        if r["latitude"] is None or r["longitude"] is None or r["waktu_lapor"] is None:
            skipped.append({"id_laporan": i, "alasan": "koordinat/waktu kosong"})
            continue
        laporan.append({"id": i, "fields": laporan_fields(r)})
        status_index.setdefault((r["status"] or "").lower(), {})[str(i)] = _unix(r["waktu_lapor"])
        det = det_by.get(i)
        if det:
            deteksi.append({"id": i, "fields": deteksi_fields(det)})
        sc = priority_score(r, det)
        if sc is not None:
            prioritas[str(i)] = sc
        geo.append({"id": i, "lng": float(r["longitude"]), "lat": float(r["latitude"])})
    riwayat = [{"id": h["id_riwayat"], "fields": {
        "id_riwayat": str(h["id_riwayat"]), "id_laporan": str(h["id_laporan"]),
        "id_pengguna": str(h["id_pengguna"]), "waktu_perubahan": _fmt(h["waktu_perubahan"]),
        "status_baru": h["status_baru"] or "", "catatan": h["catatan"] or ""}} for h in ex["riwayat_status"]]
    riwayat_list = {}
    for h in ex["riwayat_status"]:
        riwayat_list.setdefault(str(h["id_laporan"]), []).append(h["id_riwayat"])
    pengguna = [{"id": p["id_pengguna"], "fields": {
        "id_pengguna": str(p["id_pengguna"]), "nama": p["nama"], "id_role": str(p["id_role"]),
        "nama_role": p["nama_role"]}} for p in ex["pengguna"]]
    stats = {s: len(status_index.get(s, {})) for s in STATUSES}
    for s, m in status_index.items():
        stats.setdefault(s, len(m))
    return {
        "laporan": laporan, "hasil_deteksi": deteksi, "pengguna": pengguna, "riwayat": riwayat,
        "riwayat_list": riwayat_list, "status_index": status_index, "stats": stats,
        "prioritas": prioritas, "geo": geo,
        "seq_riwayat": max([h["id_riwayat"] for h in ex["riwayat_status"]] or [0]),
        "summary": {
            "laporan": len(laporan), "hasil_deteksi": len(deteksi), "pengguna": len(pengguna),
            "riwayat": len(riwayat), "riwayat_list": len(riwayat_list), "prioritas": len(prioritas),
            "geo": len(geo), "skipped": skipped,
            "tanpa_deteksi": [r["id"] for r in laporan if r["id"] not in det_by],
        },
    }


def _q(v):
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def to_redis_commands(p: dict) -> list:
    """Perintah Redis setara dengan load_to_redis.py (untuk redis-cli / Redis Insight)."""
    c = []
    def hset(key, f):
        c.append(f"HSET {key} " + " ".join(f"{k} {_q(v)}" for k, v in f.items()))
    for x in p["laporan"]: hset(key_laporan(x["id"]), x["fields"])
    for x in p["hasil_deteksi"]: hset(key_deteksi(x["id"]), x["fields"])
    for x in p["pengguna"]: hset(key_pengguna(x["id"]), x["fields"])
    for x in p["riwayat"]: hset(key_riwayat(x["id"]), x["fields"])
    for lid, ids in p["riwayat_list"].items():
        c.append(f"RPUSH {key_riwayat_list(lid)} " + " ".join(str(i) for i in ids))
    for s, m in p["status_index"].items():
        if m:
            c.append(f"ZADD {key_status_idx(s)} " + " ".join(f"{sc} {i}" for i, sc in m.items()))
    c.append(f"HSET {KEY_STATS} " + " ".join(f"{s} {n}" for s, n in p["stats"].items()))
    if p["prioritas"]:
        c.append(f"ZADD {KEY_PRIORITAS} " + " ".join(f"{sc} {i}" for i, sc in p["prioritas"].items()))
    c.append(f"GEOADD {KEY_GEO} " + " ".join(f"{g['lng']:.7f} {g['lat']:.7f} {g['id']}" for g in p["geo"]))
    c.append(f"SET {KEY_SEQ_RIWAYAT} {p['seq_riwayat']}")
    return c


def main():
    ex = json.loads((OUT_DIR / "mysql_extract.json").read_text(encoding="utf-8"))
    p = build_payload(ex)
    (OUT_DIR / "redis_payload.json").write_text(json.dumps(p, indent=2, ensure_ascii=False), encoding="utf-8")
    cmds = to_redis_commands(p)
    (OUT_DIR / "migrasi_data.redis").write_text("\n".join(cmds) + "\n", encoding="utf-8")
    s = p["summary"]
    print(f"[transform] HASH laporan:{{id}}         : {s['laporan']}")
    print(f"[transform] HASH hasil_deteksi:{{id}}   : {s['hasil_deteksi']}")
    print(f"[transform] HASH pengguna:{{id}}        : {s['pengguna']}")
    print(f"[transform] HASH riwayat:{{id}}         : {s['riwayat']} (LIST riwayat:laporan:*: {s['riwayat_list']})")
    print(f"[transform] ZSET idx:status:*:laporan  : {p['stats']}")
    print(f"[transform] ZSET idx:prioritas:laporan : {s['prioritas']}")
    print(f"[transform] GEO  idx:lokasi:laporan    : {s['geo']}")
    print(f"[transform] seq:riwayat                : {p['seq_riwayat']}")
    print(f"[transform] laporan tanpa deteksi AI   : {s['tanpa_deteksi']}")
    print(f"[transform] dilewati                   : {s['skipped']}")
    print(f"[transform] file                       : redis_payload.json, migrasi_data.redis ({len(cmds)} perintah)")


if __name__ == "__main__":
    main()
