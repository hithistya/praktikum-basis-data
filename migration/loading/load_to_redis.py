"""Tahap 3 - Loading: ekstraksi -> transformasi -> tulis ke Redis.

Contoh:
  python migration/loading/load_to_redis.py                      # MySQL -> Redis
  python migration/loading/load_to_redis.py --source dump        # dari file .sql
  python migration/loading/load_to_redis.py --source dump --dry-run   # hanya cetak perintah
"""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "migration" / "extraction"), str(ROOT / "migration" / "transformation")]

from extract import extract_from_dump, extract_from_mysql  
from transform import build_commands, ringkasan  

DEFAULT_DUMP = ROOT / "mysql" / "source-schema-and-data" / "db_laporan_kerusakan_jalan.sql"
MANAGED = ["laporan:*", "hasil_deteksi:*", "pengguna:*", "riwayat:*", "idx:*", "stats:status", "seq:riwayat"]


def quote(a):
    return f'"{a}"' if (" " in a or not a) else a


def verify(r, exp):
    def n(pattern, skip=None):
        return sum(1 for k in r.scan_iter(match=pattern) if not (skip and k.startswith(skip)))

    status_total = sum(r.zcard(k) for k in r.scan_iter(match="idx:status:*"))
    got = {
        "hash laporan": n("laporan:*"),
        "hash hasil_deteksi": n("hasil_deteksi:*"),
        "hash pengguna": n("pengguna:*"),
        "hash riwayat": n("riwayat:*", skip="riwayat:laporan:"),
        "list riwayat:laporan": n("riwayat:laporan:*"),
        "anggota zset status": status_total,
        "anggota zset prioritas": r.zcard("idx:prioritas:laporan"),
        "anggota geo lokasi": r.zcard("idx:lokasi:laporan"),
        "seq:riwayat": int(r.get("seq:riwayat") or 0),
    }
    ok = True
    print(f"\n{'Pemeriksaan':28}{'Diharapkan':>12}{'Di Redis':>10}")
    for k, v in exp.items():
        flag = "" if got[k] == v else "  <-- BEDA"
        ok &= got[k] == v
        print(f"{k:28}{v:>12}{got[k]:>10}{flag}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["mysql", "dump"], default="mysql")
    ap.add_argument("--dump", default=str(DEFAULT_DUMP))
    ap.add_argument("--dry-run", action="store_true", help="cetak perintah, tidak menulis ke Redis")
    ap.add_argument("--no-reset", action="store_true", help="jangan hapus key migrasi lama dulu")
    a = ap.parse_args()

    data = extract_from_dump(a.dump) if a.source == "dump" else extract_from_mysql()
    cmds = build_commands(data)
    exp = ringkasan(cmds)
    print(f"Ekstraksi: {len(data['laporan'])} laporan, {len(data['hasil_deteksi'])} hasil_deteksi (terbaru), "
          f"{len(data['pengguna'])} pengguna, {len(data['riwayat_status'])} riwayat")

    if a.dry_run:
        for c in cmds:
            print(" ".join(quote(x) for x in c))
        print("\nRingkasan yang akan dibuat:")
        for k, v in exp.items():
            print(f"  {k:28}{v}")
        return 0

    import redis  # pip install redis

    r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", "6379")),
                    db=int(os.getenv("REDIS_DB", "0")), password=os.getenv("REDIS_PASSWORD") or None,
                    decode_responses=True)
    r.ping()
    if not a.no_reset:
        for p in MANAGED:
            for k in r.scan_iter(match=p):
                r.delete(k)
    pipe = r.pipeline(transaction=False)
    for c in cmds:
        pipe.execute_command(*c)
    pipe.execute()
    print(f"Memuat {len(cmds)} perintah ke Redis selesai.")
    return 0 if verify(r, exp) else 1


if __name__ == "__main__":
    sys.exit(main())
