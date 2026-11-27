"""Tahap 3 - Loading: masukkan payload hasil transformasi ke Redis.
Pemakaian: python migration/loading/load_to_redis.py [--flush]
--flush menghapus key milik aplikasi (laporan:*, hasil_deteksi:*, pengguna:*, riwayat:*, idx:*, stats:*, seq:*)
sebelum memuat, sehingga aman dijalankan ulang. Key session:* tidak disentuh."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from keys import (KEY_GEO, KEY_PRIORITAS, KEY_SEQ_RIWAYAT, KEY_STATS, NAMESPACE_PATTERNS,  # noqa: E402
                  OUT_DIR, key_deteksi, key_laporan, key_pengguna, key_riwayat, key_riwayat_list,
                  key_status_idx, redis_client)


def load(r, p: dict, flush: bool = False) -> dict:
    if flush:
        for pattern in NAMESPACE_PATTERNS:
            keys = list(r.scan_iter(match=pattern, count=500))
            if keys:
                r.delete(*keys)
    pipe = r.pipeline(transaction=False)

    def put_hash(key, fields):
        pipe.delete(key)
        pipe.hset(key, mapping=fields)

    for x in p["laporan"]: put_hash(key_laporan(x["id"]), x["fields"])
    for x in p["hasil_deteksi"]: put_hash(key_deteksi(x["id"]), x["fields"])
    for x in p["pengguna"]: put_hash(key_pengguna(x["id"]), x["fields"])
    for x in p["riwayat"]: put_hash(key_riwayat(x["id"]), x["fields"])
    for lid, ids in p["riwayat_list"].items():
        pipe.delete(key_riwayat_list(lid))
        pipe.rpush(key_riwayat_list(lid), *ids)
    for status, members in p["status_index"].items():
        pipe.delete(key_status_idx(status))
        if members:
            pipe.zadd(key_status_idx(status), members)
    put_hash(KEY_STATS, p["stats"])
    pipe.delete(KEY_PRIORITAS)
    if p["prioritas"]:
        pipe.zadd(KEY_PRIORITAS, p["prioritas"])
    pipe.delete(KEY_GEO)
    for g in p["geo"]:
        pipe.geoadd(KEY_GEO, (g["lng"], g["lat"], str(g["id"])))
    pipe.set(KEY_SEQ_RIWAYAT, p["seq_riwayat"])
    pipe.execute()
    return {
        "laporan": len(p["laporan"]), "hasil_deteksi": len(p["hasil_deteksi"]),
        "pengguna": len(p["pengguna"]), "riwayat": len(p["riwayat"]),
        "prioritas": r.zcard(KEY_PRIORITAS), "geo": r.zcard(KEY_GEO),
    }


def main():
    p = json.loads((OUT_DIR / "redis_payload.json").read_text(encoding="utf-8"))
    r = redis_client()
    r.ping()
    res = load(r, p, flush="--flush" in sys.argv)
    print(f"[load] HASH laporan:*         : {res['laporan']}")
    print(f"[load] HASH hasil_deteksi:*   : {res['hasil_deteksi']}")
    print(f"[load] HASH pengguna:*        : {res['pengguna']}")
    print(f"[load] HASH riwayat:*         : {res['riwayat']}")
    print(f"[load] ZSET idx:prioritas     : {res['prioritas']}")
    print(f"[load] GEO  idx:lokasi        : {res['geo']}")
    print(f"[load] stats:status           : {r.hgetall(KEY_STATS)}")


if __name__ == "__main__":
    main()
