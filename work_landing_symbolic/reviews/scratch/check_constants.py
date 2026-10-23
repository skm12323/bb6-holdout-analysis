"""Reviewer scratch: constants and counts for RATIONAL_MODE.md sections 2 and 4.

Checks, with exact integer arithmetic where feasible:
  * count of (j,C,lift) pairs actually exercised by verify_rational_mode.py;
  * SIZE3: 3*(kappa(j)+B) < 2^(j-2) at j = N0, and the two-term bound on L3(j);
  * L3(j) <= max(2*log2 j + 5, N0/2+4) at sample j >= N0;
  * h3(q) for q = N0 and q = 1e8, and the height condition (C0+3h3)/3 <= B;
  * the tower inequality q < U_r => L3(q) < U_{r-1} at symbolic level is not
    executable (U_1 = 2^(1e7)); we instead check the two algebraic premises
    2*log2(U_r)+5 < U_{r-1} and N0/2+4 < U_{r-1} for r=1,2 by log2 algebra.

Run: python -B work_landing_symbolic/reviews/scratch\check_constants.py
"""
import sys, math
from pathlib import Path

REPO = Path(r"D:/math_cc")
sys.path.insert(0, str(REPO / "work_c3_drift"))
from verify_shift_transport import Calendar, val  # noqa: E402

N0 = 2 * 10**7
BLOG = 10**7  # B = 2^BLOG


def P(n):
    g = (6 * n * n + 5 - 1).bit_length()  # ceil(log2(6n^2+5))
    assert (1 << (g - 1)) < 6 * n * n + 5 <= (1 << g), (n, g)
    return 2 * g * g + 1345


def kappa(j):
    return (3 * (j - 1) * P(j - 1)) // 2


def log2_int(n):
    return math.log2(n) if n < 10**300 else n.bit_length() - 1 + math.log2(
        n / (1 << (n.bit_length() - 1)))


def L3_log2(j):
    """log2 of the two L3 arguments (floats; both are astronomically large)."""
    a = 3 * (kappa(j) + (1 << BLOG)) if BLOG < 1000 else None
    return a


def main():
    out = {}
    # --- 1. count of tested a-pairs (mirrors the verifier's loop condition) ---
    cal = Calendar(256)
    allc = set()
    for c0 in (10, 26):
        states = {c0}
        for t in range(5):
            allc |= states
            states = {z for c in states for z in (9 - c, c - 3, c, c + 3)}
    allc = sorted(allc)
    checks = 0
    odd_a_j = []
    skipped = 0
    for j in range(5, 129):
        r = cal.crossing(j - 1)
        if not (r["odd"] and r["kind"] == "a"):
            continue
        odd_a_j.append(j)
        k = r["time"] // 2
        for c in allc:
            z = 9 * k + c
            q = 1 + val(z)
            if q > j - 2:
                skipped += 2
                continue
            checks += 2
    out["a_checks_reproduced"] = checks
    out["a_skipped_pairs"] = skipped
    out["odd_a_j_in_5_128"] = odd_a_j

    # --- 2. SIZE3 and L3 at j = N0 ---
    j = N0
    kap = kappa(j)
    # 3*(kappa+B) < 2^(j-2)?
    # compare logs: log2(3*kappa+3*2^BLOG) vs j-2
    # use exact-ish bounds: 3*kappa < 2^(j-2) is obvious; check with bit lengths
    bl_k = (3 * kap).bit_length()
    out["j_N0"] = {"kappa": str(kap), "bitlen(3kappa)": bl_k,
                   "j_minus_2": j - 2,
                   "SIZE3_ok": bl_k <= j - 2 and (3 * kap) < (1 << (j - 2)),
                   "3B_bitlen": (3 << BLOG).bit_length()}
    # use bit lengths to bound 3*(kappa+B) < 2^(j-2)
    tot = 3 * kap + 3 * (1 << BLOG)
    out["j_N0"]["bitlen(3(kappa+B))"] = tot.bit_length()
    out["j_N0"]["SIZE3_exact"] = tot < (1 << (j - 2))

    # --- 3. L3(j) <= max(2log2 j + 5, N0/2+4) ---
    # count bits instead of floats
    def L3_parts(j):
        t1 = 1 + (3 * (kappa(j) + (1 << BLOG))).bit_length() - 1
        # floor(log2 x) = bitlen(x)-1
        x = 6 * (j - 1) * P(j - 1) + 5
        t2 = x.bit_length() - 1
        return t1, t2

    rows = []
    for j in (N0, N0 + 1, 10**8, 10**20, 2**100):
        t1, t2 = L3_parts(j)
        bound = max(2 * math.log2(j) + 5, N0 / 2 + 4)
        rows.append({"j": str(j), "term1": t1, "term2": t2,
                     "L3": max(t1, t2), "claimed_bound": bound,
                     "ok": max(t1, t2) <= bound})
    out["L3_rows"] = rows

    # --- 4. h3 at two starts ---
    def h3(q, cap=64):
        t = 0
        while q >= N0 and t < cap:
            t1, t2 = L3_parts(q)
            q = max(t1, t2)
            t += 1
        return t, q

    h1 = h3(N0)
    h2 = h3(10**8)
    out["h3"] = {"q=N0": h1, "q=1e8": h2,
                 "height_ok_N0": (10 + 3 * h1[0]) / 3 <= 2**BLOG,
                 "height_ok_1e8": (26 + 3 * h2[0]) / 3 <= 2**BLOG}

    p = Path(__file__).with_name("check_constants.json")
    import json
    p.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))
    print("json:", p)


if __name__ == "__main__":
    main()
