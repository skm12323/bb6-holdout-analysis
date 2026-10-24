#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""train_checks.py -- Task (B): gateway trains / denominator-rank growth.

Coordinator implementation (the (B) subagent could not be launched: concurrency
limit). Canonical data: work_global_calendar Calendar(512) and the read-only
table D:/math_cc_astra/deep1/table_1000000.pkl. Table semantics (verified in T1):
typ/tau/eps/odd as in the calendar; lY[n] = lambda_Y = lambda'_W - 3*tau - 4 for
odd b/c n (all n < 10^6); lA[n] = lambda'_W - 3 only for type b (NOT for c).

Checks (statements and tags in B_RANK.md):
  T1  table/calendar consistency (n < 5000; lY for all odd b/c, lA for b only).
  T2  canonical kernel scan (exact walks from the S(J) anchor rep (2^J, 2^J+1),
      J <= 512): every parameter-5 chain has class 13 mod 16 and output 4
      (the theta=13 catapult-to-4 branch); no tie class, no gateway output
      (m >= 6) from a 5-chain, no (5, m>=6, 5) pattern anywhere.
  T3  label scan [B]: odd-a labels m in [7, 10^6) with k = tau(m-1)/2 == 6
      mod 16 (necessary for an internal A-return of a train, Prop B1); odd b/c
      labels with omega = 5 and lambda_Y == 8 mod 16 (internal B-return,
      Prop B1b); labels 5..16 in detail; mod-32 split (6 vs 22).
  T4  36 bad-class representative walks (exact): words, tie classes mod 64,
      strict trains (ties at gap 2), m distribution, rank tripling check
      Q_{t+1} = 3 Q_t, class recursion D'Q' - C' - 2^m Q' == 0 mod 2^(m+1).
  T5  tie->tie witness (73515, 98094) (non-canonical): same checks; tie-class
      alternation 21 -> 5 (mod 32) on its strict train; internal label 17 has
      k == 6 mod 16.
  T6  (S2*) on every non-gate a-chain of all T4/T5 walks (3Qk + C != 0 mod
      2^(j-2)); DEPTH size test split by "post-gate" (lift-bit height) vs other.
  T7  dangerous-residue structure (Prop B3) at j = 25: classes C mod 2^(j-2)
      that are NT-dangerous for some rank form exactly the coset -3k*<3>, each
      hit by exactly one r mod ord(3).
  T8  m is not a class function at (5,5): fixed class D=5 mod 64, vary u;
      m = 4 + v2(3u+1) is unbounded; also fixed u=1, vary D by 64t gives m=6.

Writes train_checks.json; exit 0 iff all hard checks pass.
No global EXT claim; K_clock unchanged.
"""
import json
import pickle
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from work_global_calendar.calendar_oracle import Calendar  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "train_checks.json"
TABPATH = Path(r"D:/math_cc_astra/deep1/table_1000000.pkl")

RES = {"status": "PASS", "failures": [], "counts": {}, "data": {},
       "scope": ("Task (B) gateway-train / rank-growth checks. Canonical: Calendar(512) "
                 "+ table_1000000.pkl (n<10^6). The (73515,98094) witness and lift "
                 "variants are synthetic (non-canonical). No global EXT claim; "
                 "K_clock unchanged.")}


def v2(x):
    if x == 0:
        return None
    x = abs(int(x))
    return (x & -x).bit_length() - 1


def sym(e, bits):
    M = 1 << bits
    r = e % M
    return r - M if r > M // 2 else r


def read_cross(cal, n):
    r = cal.crossing(n)
    d = {"kind": r["kind"], "odd": bool(r["odd"]), "tau": r["time"],
         "eps": r["epsilon"], "omega": r["omega"], "cW": None, "lam": None}
    if d["odd"] and d["kind"] != "a":
        cw = (r["head_ratio"] + 2 * r["tail_ratio"]) * (1 << n)
        assert cw.denominator == 1
        d["cW"] = int(cw)
        d["lam"] = r["head_lambda"] + 2 * r["tail_lambda"] + 3
        d["omega"] = v2(d["lam"])
    return d


def walk(cal, x, T, ceiling, limit=100000):
    """Exact walk with rational-description tracking (Q = 3^r)."""
    G = 0
    rows = []
    Q, C, H = 1, None, None
    prev_gate = False
    for _ in range(limit):
        if x == 0 or x < 0:
            break
        j = v2(x)
        if j is None or j + G >= ceiling:
            break
        D = T - x
        if C is None:
            C, H = sym(D, j + 1), j + 1
        b = ((D * Q - C) >> j) & 1
        rows.append(dict(j=j, G=G, R=j + G, D=D, Q=Q, C=C, b=b, H=H,
                         tie=(j == 5 and (D % 16) == 5), post_gate=prev_gate))
        prev_gate = False
        if j <= 4:
            break
        cr = read_cross(cal, j - 1)
        if not cr["odd"]:
            break
        if cr["kind"] == "a":
            k = cr["tau"] // 2
            xn = 2 * T + 6 * k - x // 2
            eps = 0
        else:
            xn = cr["cW"] * (x >> j) + cr["lam"]
            eps = cr["eps"]
        Tn = T + 3 + 3 * cr["tau"]
        jn = v2(xn)
        Gn = G + 1 + eps
        if jn is None:
            rows[-1]["zero"] = True
            break
        rows[-1]["out"] = jn
        if cr["kind"] == "a" and jn >= j:
            Qn = 3 * Q
            Cn = (9 + 6 * k) * Q - C - b * Q * (1 << j)
            while Qn > 1 and Cn % 3 == 0:
                Cn //= 3
                Qn //= 3
            rows[-1]["gate"] = True
            prev_gate = True
            Hn = min(H, jn + 1)
        elif cr["kind"] == "a":
            Cn, Qn = 3 * Q - C, Q
            Hn = min(H, jn + 1)
        else:
            lY = cr["lam"] - 3 * cr["tau"] - 4
            s = -1 - lY          # integer for canonical crossings read here
            Cn, Qn = C + Q * s, Q
            Hn = min(H, jn + 1)
        x, T, G, Q, C, H = xn, Tn, Gn, Qn, sym(Cn, jn + 1), Hn
    return rows


def analyze(rows, label, canonical):
    ties = [i for i, r in enumerate(rows) if r["tie"]]
    trains = []
    cur = []
    for a, b_ in zip(ties, ties[1:]):
        if b_ - a == 2:
            if not cur:
                cur = [a, b_]
            else:
                cur.append(b_)
        else:
            if cur:
                trains.append(cur)
            cur = []
    if cur:
        trains.append(cur)
    # rank law along strict trains: r' = r+1, except r=0 with 3 | C+2b gives r'=0
    def rank_law(a, b_):
        ra, rb = rows[a], rows[b_]
        Qa, Qb, Ca, ba = ra["Q"], rb["Q"], ra["C"], ra["b"]
        if Qa * 3 == Qb:
            return True
        return Qa == 1 and Qb == 1 and (Ca + 2 * ba) % 3 == 0
    rank_ok = all(rank_law(t0, t1) for t in trains for t0, t1 in zip(t, t[1:]))
    return dict(label=label, canonical=canonical, word=[r["j"] for r in rows],
                n_ties=len(ties), tie_idx=ties,
                tie_classes_mod64=[rows[i]["D"] % 64 for i in ties],
                max_train=max((len(t) for t in trains), default=0),
                trains=[len(t) for t in trains],
                tie_gaps=[b_ - a for a, b_ in zip(ties, ties[1:])],
                ms=[rows[i + 1]["j"] for i in ties if i + 1 < len(rows)],
                rank_tripling_ok=rank_ok,
                zero=any(r.get("zero") for r in rows))


def check_class_recursion(rows, label):
    """Across each tie step: D'Q' - C' - 2^m Q' == 0 mod 2^(m+1)."""
    ok, bad = 0, []
    for i, r in enumerate(rows):
        if not r.get("gate") or i + 1 >= len(rows) or r["j"] != 5 or not r["tie"]:
            continue
        m = rows[i + 1]["j"]
        Dp = rows[i + 1]["D"]
        Q, C, b, H = r["Q"], r["C"], r["b"], r["H"]
        Cn, Qn = 15 * Q - C - 32 * b * Q, 3 * Q
        Mmod = 1 << min(m + 1, H)
        val = (Dp * Qn - Cn - (1 << m) * Qn)
        if val % Mmod != 0:
            bad.append((label, m, H, val % Mmod))
        else:
            ok += 1
    return ok, bad


def main():
    t0 = time.time()
    cal = Calendar(512)
    tab = pickle.load(open(TABPATH, "rb"))
    F = RES["failures"]

    # T1: table consistency
    n_ok = lam_ok = 0
    for n in range(0, 5000):
        r = cal.crossing(n)
        if not (chr(tab["typ"][n]) == r["kind"] and bool(tab["odd"][n]) == bool(r["odd"])
                and int(tab["tau"][n]) == r["time"] and int(tab["eps"][n]) == r["epsilon"]):
            F.append(("T1 table", n))
            break
        n_ok += 1
    for n in range(4, 5000):
        r = cal.crossing(n)
        if not r["odd"] or r["kind"] == "a":
            continue
        lam = r["head_lambda"] + 2 * r["tail_lambda"] + 3
        lY_ok = int(tab["lY"][n]) == lam - 3 * r["time"] - 4
        lA_ok = (r["kind"] != "b") or (int(tab["lA"][n]) == lam - 3)
        if lY_ok and lA_ok:
            lam_ok += 1
        else:
            F.append(("T1 lam", n))
            break
    RES["counts"]["T1_table_consistent_n"] = n_ok
    RES["counts"]["T1_lambda_consistent_n"] = lam_ok

    # T2: canonical kernel scan via exact walks
    n5 = tie5 = gw5 = pattern = 0
    cls5 = Counter()
    for J in range(1, 513):
        x0 = 1 << J
        rows = walk(cal, x0, x0 + 1, J + 2, limit=80)
        w = [r["j"] for r in rows]
        for a in range(len(w) - 2):
            if w[a] == 5 and w[a + 1] >= 6 and w[a + 2] == 5:
                pattern += 1
        for i, r in enumerate(rows):
            if r["j"] != 5:
                continue
            if i == 0 and J <= 5:
                cls5["start"] += 1
                continue
            n5 += 1
            cls5[r["D"] % 16] += 1
            if r["tie"]:
                tie5 += 1
            if r.get("out") is not None and r["out"] >= 6:
                gw5 += 1
                F.append(("T2 gateway from 5", J, r["D"] % 64, r["out"]))
    RES["counts"]["T2_kernels_scanned"] = 512
    RES["counts"]["T2_parameter5_chains"] = n5
    RES["data"]["T2_five_class_mod16"] = dict(cls5)
    RES["counts"]["T2_ties"] = tie5
    RES["counts"]["T2_gateway_patterns"] = pattern

    # T3: label scan
    a_int = []
    a_all = 0
    a_mod32 = Counter()
    bc_ret = []
    bc_om5 = 0
    for m in range(7, 1000000):
        n = m - 1
        if not tab["odd"][n]:
            continue
        kch = chr(tab["typ"][n])
        if kch == "a":
            a_all += 1
            k = int(tab["tau"][n]) // 2
            if k % 16 == 6:
                a_int.append(m)
                a_mod32[k % 32] += 1
        else:
            lam = int(tab["lY"][n]) + 3 * int(tab["tau"][n]) + 4
            if v2(lam) == 5:
                bc_om5 += 1
                if int(tab["lY"][n]) % 16 == 8:
                    bc_ret.append(m)
    RES["counts"]["T3_odd_a_labels"] = a_all
    RES["counts"]["T3_A_internal_labels"] = len(a_int)
    RES["data"]["T3_A_internal_first20"] = a_int[:20]
    RES["data"]["T3_A_internal_mod32"] = dict(a_mod32)
    RES["counts"]["T3_omega5_labels"] = bc_om5
    RES["counts"]["T3_B_internal_labels"] = len(bc_ret)
    RES["data"]["T3_B_internal_first20"] = bc_ret[:20]
    small = []
    for m in range(5, 17):
        n = m - 1
        if tab["odd"][n]:
            kch = chr(tab["typ"][n])
            k = int(tab["tau"][n]) // 2 if kch == "a" else None
            lam = None if kch == "a" else int(tab["lY"][n]) + 3 * int(tab["tau"][n]) + 4
            small.append(dict(m=m, kind=kch, k=k, k_mod32=None if k is None else k % 32,
                              omega=None if lam is None else v2(lam),
                              lY_mod16=None if kch == "a" else int(tab["lY"][n]) % 16))
        else:
            small.append(dict(m=m, kind="even"))
    RES["data"]["T3_labels_5_16"] = small

    # T4 + T5: walks
    bad = {5: [5, 21, -27, -11], 8: [58, 186, -198, -70],
           12: [1012, 3060, -3084, -1036], 14: [4081, 12273, -12303, -4111],
           17: [32702, 32750, 98238, 98286, -98370, -98322, -32834, -32786],
           22: [1048552, 3145704, 5242856, 7340008],
           24: [4194277, 12582885, 20971493, 29360101],
           27: [33554402, 100663266, 167772130, 234880994]}
    allrows = {}
    stats = []
    rec_ok = 0
    rec_bad = []
    for j in sorted(bad):
        for delta in bad[j]:
            x = 1 << j
            rows = walk(cal, x, x + delta, j + 60)
            lbl = "bad_%d_%d" % (j, delta)
            allrows[lbl] = rows
            stats.append(analyze(rows, lbl, True))
            ok, bads = check_class_recursion(rows, lbl)
            rec_ok += ok
            rec_bad += bads
    j0, D0 = 73515, 98094
    x = 1 << j0
    rows = walk(cal, x, x + D0, j0 + 60)
    allrows["witness"] = rows
    stw = analyze(rows, "witness_73515_98094", False)
    ok, bads = check_class_recursion(rows, "witness")
    rec_ok += ok
    rec_bad += bads
    RES["data"]["T4_walks"] = stats
    RES["data"]["T5_witness"] = stw
    RES["counts"]["T4_walks"] = len(stats)
    RES["counts"]["T4_total_ties"] = sum(s["n_ties"] for s in stats) + stw["n_ties"]
    RES["counts"]["T4_max_train"] = max(max(s["max_train"] for s in stats), stw["max_train"])
    RES["counts"]["T4_max_m"] = max(max((max(s["ms"]) if s["ms"] else 0) for s in stats),
                                    max(stw["ms"]) if stw["ms"] else 0)
    RES["counts"]["T4T5_class_recursion_ok"] = rec_ok
    if rec_bad:
        F.append(("T4T5 class recursion", rec_bad[:5]))
    if not all(s["rank_tripling_ok"] for s in stats + [stw]):
        F.append(("T4T5 rank tripling",))
    # alternation on the witness strict train: tie classes mod 32
    wit = stw["tie_classes_mod64"]
    RES["data"]["T5_witness_ties_mod32"] = [c % 32 for c in wit]
    # internal label k congruence on the witness train (label 17)
    k17 = int(tab["tau"][16]) // 2
    RES["data"]["T5_label17_k_mod32"] = k17 % 32
    if chr(tab["typ"][16]) != "a" or k17 % 16 != 6:
        F.append(("T5 label17 k", k17))

    # T6: (S2*) and DEPTH
    s2 = s2_tot = 0
    dep = Counter()
    worst_depth = []
    for lbl, rows in allrows.items():
        for r in rows:
            if r["j"] <= 4 or r.get("gate") or r.get("zero") or r["tie"]:
                continue
            j, Q, C = r["j"], r["Q"], r["C"]
            cr = read_cross(cal, j - 1)
            if not cr["odd"] or cr["kind"] != "a":
                continue
            k = cr["tau"] // 2
            s2_tot += 1
            if (3 * Q * k + C) % (1 << (j - 2)) != 0:
                s2 += 1
            else:
                F.append(("T6 S2* failed", lbl, j, Q, C))
            if j >= 19:
                Pn = 2 * (6 * (j - 1) ** 2 + 5).bit_length() ** 2 + 1345
                # DEPTH: Q*(kappa + h) < 2^(j-2), kappa = 1.5*(j-1)*P, h = |C|/Q
                lhs2 = 3 * (j - 1) * Pn * Q + 2 * abs(C)   # = 2*Q*(kappa+h)
                okd = lhs2 < (1 << (j - 1))
                key = "post_gate" if r["post_gate"] else "other"
                dep[(key, okd)] += 1
                worst_depth.append((lbl, j, key, round(lhs2 / (1 << (j - 1)), 3)))
    RES["counts"]["T6_a_chains"] = s2_tot
    RES["counts"]["T6_S2_ok"] = s2
    RES["data"]["T6_DEPTH"] = {str(k_): v for k_, v in dep.items()}
    RES["data"]["T6_DEPTH_worst"] = sorted(worst_depth, key=lambda z: -z[3])[:8]

    # T7: dangerous-residue structure at the first odd-a j >= 19
    j = next(jj for jj in range(19, 200)
             if tab["odd"][jj - 1] and chr(tab["typ"][jj - 1]) == "a")
    k = int(tab["tau"][j - 1]) // 2
    n = j - 2
    M = 1 << n
    target = (-3 * k) % M
    order = (1 << (n - 2))                    # order of 3 mod 2^n
    orb = set()
    p = target
    while p not in orb:
        orb.add(p)
        p = (p * 3) % M
    hits = Counter()
    for r in range(order):
        hits[(target * pow(3, r, M)) % M] += 1
    mult = order // len(orb)
    if not (set(hits) == orb and all(c == mult for c in hits.values())):
        F.append(("T7 coset structure", j, order, len(orb)))
    dang = orb
    RES["counts"]["T7_j"] = j
    RES["counts"]["T7_k"] = k
    RES["counts"]["T7_order_of_3"] = order
    RES["counts"]["T7_dangerous_classes"] = len(dang)
    RES["counts"]["T7_v2_of_3k"] = v2(3 * k)
    RES["counts"]["T7_total_classes"] = M

    # T8: m not a class function at (5,5)
    mu = Counter()
    for u in range(1, 512, 2):
        x = 32 * u
        y = 2 * (x + 5) + 6 - x // 2     # D = 5, k = 1
        mu[v2(y)] += 1
    md = Counter()
    for t in range(64):
        D = 5 + 64 * t
        x = 32
        y = 2 * (x + D) + 6 - x // 2
        md[v2(y)] += 1
    RES["data"]["T8_m_vs_u_at_class5"] = {str(k_): v for k_, v in mu.items()}
    RES["data"]["T8_m_vs_lift_D_at_u1"] = {str(k_): v for k_, v in md.items()}
    RES["counts"]["T8_distinct_m_vs_u"] = len(mu)
    RES["counts"]["T8_max_m_vs_u"] = max(mu)
    RES["counts"]["T8_m_fixed_when_u1"] = len(md)

    # T9: synthetic alternation test (non-canonical): tie class 5 mod 32 with
    # output 54 (k53 = 22 mod 32) returns to a tie of class 21 mod 32 (Prop B1),
    # and the train then stops at the non-internal label 7 (X(6) even).
    u9 = ((1 << 50) - 1) // 3
    x9 = 32 * u9
    T9a = x9 + 5
    y9 = 2 * T9a + 6 - x9 // 2
    m9 = v2(y9)
    k53 = int(tab["tau"][53]) // 2
    x9b, T9b = y9, T9a + 9
    x9c = 2 * T9b + 6 * k53 - x9b // 2
    T9c = T9b + 3 + 6 * k53
    cls9 = (T9c - x9c) % 32
    y9b = 2 * T9c + 6 - x9c // 2
    ok9 = (m9 == 54 and k53 % 32 == 22 and v2(x9c) == 5 and cls9 == 21
           and (T9c - x9c) % 16 == 5 and v2(y9b) == 7 and not tab["odd"][6])
    if not ok9:
        F.append(("T9 alternation", m9, k53 % 32, v2(x9c), cls9, v2(y9b)))
    RES["data"]["T9_synthetic_54"] = dict(m=m9, k53_mod32=k53 % 32,
                                          returned=v2(x9c), next_class_mod32=cls9,
                                          next_out=v2(y9b), X6_even=not bool(tab["odd"][6]))

    RES["timing"] = round(time.time() - t0, 1)
    RES["status"] = "PASS" if not F else "FAIL"
    OUT.write_text(json.dumps(RES, indent=1, default=str) + "\n", encoding="utf-8")
    print(json.dumps({k: RES[k] for k in ("status", "counts", "timing")}, indent=1,
                     default=str))
    print("failures:", F[:10])
    return 0 if not F else 1


if __name__ == "__main__":
    sys.exit(main())
