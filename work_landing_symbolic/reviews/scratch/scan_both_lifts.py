"""Reviewer scratch check for work_c3_drift/RATIONAL_MODE.md.

The doc's representation is D = C/3 + b*2^j (mod 2^(j+1)), b in {0,1}.
verify_rational_mode.py only scans the b=0 representative
d = C*3^{-1} mod 2^(j+1).  This script scans BOTH lifts for the same
32-numerator closure and j=5..128, and separately the actual gateway
classes (10-2^j)/3 and (26-2^j)/3.

Run: python -B work_landing_symbolic/reviews/scratch/scan_both_lifts.py
"""
import sys, json
from collections import Counter
from pathlib import Path

REPO = Path(r"D:/math_cc")
sys.path.insert(0, str(REPO / "work_c3_drift"))
from verify_shift_transport import Calendar, bounded_walk, val  # noqa: E402


def closure():
    allc = set()
    for c0 in (10, 26):
        states = {c0}
        for t in range(5):
            allc |= states
            states = {z for c in states for z in (9 - c, c - 3, c, c + 3)}
    return sorted(allc)


def status_of(cal, j, delta, prec):
    st, rows = bounded_walk(cal, 1 << j, (1 << j) + delta, prec, signed=True)
    return st, len(rows)


def main():
    cal = Calendar(256)
    allc = closure()
    out = {"numerators": allc, "n": len(allc)}
    for lift in (0, 1):
        cnt = Counter()
        fails = []
        per_j = Counter()
        for j in range(5, 129):
            mod = 1 << (j + 1)
            for c in allc:
                d = (c * pow(3, -1, mod)) % mod
                dd = (d + lift * (1 << j)) % mod
                st, nrows = status_of(cal, j, dd, j + 1)
                cnt[st] += 1
                if st != "end":
                    fails.append({"j": j, "C": c, "lift": lift, "delta": str(dd),
                                  "status": st, "chains": nrows})
                    per_j[j] += 1
        out["lift_%d" % lift] = {"status": dict(cnt), "nfail": len(fails),
                                 "fails": fails[:50],
                                 "fail_j_hist": dict(sorted(per_j.items()))}

    # Actual gateway classes (10-2^j)/3 and (26-2^j)/3, entered at b=1
    # in the doc's convention.  delta = (C - 2^j)/3 reduced mod 2^(j+1).
    gw = {}
    for C in (10, 26):
        cnt = Counter()
        fails = []
        for j in range(5, 129):
            mod = 1 << (j + 1)
            delta = ((C - (1 << j)) * pow(3, -1, mod)) % mod
            st, nrows = status_of(cal, j, delta, j + 1)
            cnt[st] += 1
            if st != "end":
                fails.append({"j": j, "C": C, "delta": str(delta),
                              "status": st, "chains": nrows})
        gw[str(C)] = {"status": dict(cnt), "fails": fails[:20]}
    out["gateway_classes"] = gw

    p = Path(__file__).with_name("scan_both_lifts.json")
    p.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("numerators:", len(allc))
    for lift in (0, 1):
        r = out["lift_%d" % lift]
        print("lift %d: %s nfail=%d hist=%s" % (lift, r["status"], r["nfail"],
                                                r["fail_j_hist"]))
        for f in r["fails"][:6]:
            print("   ", f)
    for C, r in gw.items():
        print("gateway C=%s: %s fails=%s" % (C, r["status"], r["fails"][:4]))
    print("json:", p)


if __name__ == "__main__":
    main()
