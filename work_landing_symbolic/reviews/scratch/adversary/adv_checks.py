#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Adversary checks against work_landing_symbolic/THEOREM.md.

Only reads the repo; writes only under work_landing_symbolic/reviews/scratch/adversary/.
Run: python -B work_landing_symbolic/reviews/scratch/adversary/adv_checks.py
"""
import json
import pickle
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from work_global_calendar.calendar_oracle import Calendar  # noqa: E402

TAB = Path(r"D:/math_cc_astra/deep1/table_1000000.pkl")
OUT = Path(__file__).resolve().with_name("adv_checks.json")
RES = {}


def v2(x):
    if isinstance(x, F):
        if x == 0:
            return None
        a, b = abs(x.numerator), x.denominator
        return (a & -a).bit_length() - (b & -b).bit_length()
    x = abs(int(x))
    if x == 0:
        return None
    return (x & -x).bit_length() - 1


def read_cross(cal, n):
    r = cal.crossing(n)
    d = {"kind": r["kind"], "odd": bool(r["odd"]), "tau": r["time"],
         "eps": r["epsilon"], "omega": r.get("omega"), "cW": None, "lam": None}
    if d["odd"] and d["kind"] != "a":
        cw = (r["head_ratio"] + 2 * r["tail_ratio"]) * (1 << n)
        d["cW"] = int(cw)
        d["lam"] = r["head_lambda"] + 2 * r["tail_lambda"] + 3
        d["omega"] = v2(d["lam"])
    return d


def step(x, T, cr):
    j = v2(x)
    if cr["kind"] == "a":
        k = cr["tau"] // 2
        return 2 * T + 6 * k - x // 2, T + 3 + 3 * cr["tau"]
    return cr["cW"] * (x >> j) + cr["lam"], T + 3 + 3 * cr["tau"]


def main():
    cal = Calendar(512)

    # ---------------------------------------------------------------- #
    # 1. THEOREM 2.3 says: strong-descent a step has A'=A and ht'=ht,
    #    where ht=|C|/Q.  ht' = |3Q-C|/Q = |3-c|, ht=|c|.  Counterexample.
    # ---------------------------------------------------------------- #
    C, Q, b, j, k, u = 7, 1, 0, 5, 1, 1
    D = C  # class == exact defect
    x = (1 << j) * u
    T = x + D
    xn = 2 * T + 6 * k - x // 2
    jn = v2(xn)
    p = 1 + v2(3 * Q * k + C)
    ht = abs(F(C, Q))
    ht2 = abs(F(3 * Q - C, Q))
    RES["ht_preserved_counterexample"] = {
        "input": {"j": j, "Q": Q, "C": C, "b": b, "k": k, "u": u},
        "p": p, "strong_descent": p <= j - 2, "jn": jn,
        "ht": str(ht), "ht_after": str(ht2), "equal": ht == ht2,
        "A_before": str(abs(F(C, Q) - F(3, 2))),
        "A_after": str(abs(F(3 * Q - C, Q) - F(3, 2))),
        "note": "THEOREM 2.3 asserts ht'=ht on strong a descent; c'=3-c gives |3-c|, not |c|",
    }

    # a second, canonical-crossing instance
    C2, Q2 = 10, 1
    j = 5
    k = read_cross(cal, j - 1)["tau"] // 2
    p2 = 1 + v2(3 * Q2 * k + C2)
    RES["ht_preserved_counterexample_canon"] = {
        "j": j, "k": k, "C": C2, "Q": Q2, "p": p2,
        "strong": p2 <= j - 2, "ht": str(abs(F(C2, Q2))),
        "ht_after": str(abs(F(3 * Q2 - C2, Q2))),
    }

    # ---------------------------------------------------------------- #
    # 2. THEOREM 2.1 (A3): "x'=0 => Q=1 and 2(C+3kQ)+3*2^{j-1}uQ = 0".
    #    The equation is exact, but D is only a class.  Find a state with
    #    x'=0 whose representative C does NOT satisfy it.
    # ---------------------------------------------------------------- #
    j, u, k = 5, 1, 1
    Dx = -27            # exact defect that makes x'=0 for x=32
    x = 32
    T = x + Dx
    xn = 2 * T + 6 * k - x // 2
    cls = Dx % (1 << (j + 1))
    # representative C = 37 (== cls), Q = 1, b = 0
    C = 37
    lhs = 2 * (C + 3 * k * 1) + 3 * (1 << (j - 1)) * u * 1
    # also the symmetric representative
    Csym = cls - (1 << (j + 1)) if cls > (1 << j) else cls
    lhs_sym = 2 * (Csym + 3 * k * 1) + 3 * (1 << (j - 1)) * u * 1
    RES["A3_zero_formula"] = {
        "state": {"j": j, "u": u, "Theta": T, "D": Dx},
        "x_next": xn,
        "class_mod_2j1": cls,
        "C_used": C, "C_is_valid_rep": (C % (1 << (j + 1))) == cls % (1 << (j + 1)),
        "lhs": lhs, "formula_holds": lhs == 0,
        "symmetric_C": Csym, "lhs_symmetric": lhs_sym,
        "p": 1 + v2(3 * k + Dx),
        "conclusion": "x'=0 but the stated necessary equation fails for the valid representative C=37",
    }

    # ---------------------------------------------------------------- #
    # 3. THEOREM 2.2 (Theorem B): "x' = c'_W u + lambda'_W, j' = omega".
    #    Requires x' != 0.  Test whether lambda'_W > 0 for the canonical data,
    #    and whether c'_W | lambda'_W is possible (x'=0 for u = -lam/cW).
    # ---------------------------------------------------------------- #
    lam_min = None
    lam_neg = 0
    n_checked = 0
    ratio_ok = 0
    try:
        with open(TAB, "rb") as f:
            tab = pickle.load(f)
        N = len(tab["typ"])
        for n in range(4, N):
            if tab["typ"][n] == ord("a"):
                continue
            lam = int(tab["lA"][n]) + 2 * int(tab["lY"][n]) + 3
            n_checked += 1
            if lam < 0:
                lam_neg += 1
            if lam_min is None or lam < lam_min:
                lam_min = lam
            # c'_W = 3*2^(n-1) for type b, else c_A; |lam| < c'_W?
            if tab["typ"][n] == ord("b"):
                cw = 3 * (1 << (n - 1))
                if abs(lam) < cw:
                    ratio_ok += 1
        RES["B_lambda"] = {"n_checked": n_checked, "lam_neg": lam_neg,
                           "lam_min": lam_min, "type_b_abs_lam_lt_cW": ratio_ok,
                           "table_len": N}
    except Exception as exc:  # noqa: BLE001
        RES["B_lambda"] = {"error": str(exc)}

    # direct zero test on one canonical b crossing: can c'W*u+lam be 0 with odd u?
    zero_possible = []
    for n in (5, 8, 11, 12, 14, 17, 21, 23):
        cr = read_cross(cal, n)
        if not (cr["odd"] and cr["kind"] != "a"):
            continue
        cw, lam = cr["cW"], cr["lam"]
        # x'=0 <=> cw*u = -lam ; u must be odd integer
        ok = (lam % cw == 0) and (((-lam) // cw) % 2 == 1)
        zero_possible.append({"n": n, "kind": cr["kind"], "cW": cw, "lam": lam,
                              "zero_u_possible": ok})
    RES["B_zero_u"] = zero_possible

    # ---------------------------------------------------------------- #
    # 4. THEOREM 2.3 catapult height: claims ht' <= 3 + 2k + ht/3 + 32b/3.
    #    The correct term from C'=(9+6k)Q-C-bQ*2^j, Q'=3Q is b*2^j/3.
    # ---------------------------------------------------------------- #
    rows = []
    for j in (6, 10, 20, 40):
        for k in (1, 5):
            for b in (0, 1):
                Q, C = 1, 1
                Cp = (9 + 6 * k) * Q - C - b * Q * (1 << j)
                Qp = 3 * Q
                ht = abs(F(C, Q))
                lhs = abs(F(Cp, Qp))
                claim = 3 + 2 * k + ht / 3 + F(32 * b, 3)
                rows.append({"j": j, "k": k, "b": b, "ht'": str(lhs),
                             "claimed_bound": str(claim), "holds": lhs <= claim})
    RES["catapult_height"] = rows

    # ---------------------------------------------------------------- #
    # 5. Theorem D / L: "all records <= j_0".  Find a real fire walk with
    #    an interior entry (Gamma_0 > 0) and show records > j_0 there.
    # ---------------------------------------------------------------- #
    def first_fire(P):
        modulus = 1 << (P - 1)
        base = (-2 * pow(3, -1, modulus)) % modulus
        for t in range(8):
            k = base + t * modulus
            if k < 1:
                continue
            if 1 + v2(3 * k + 2) != P:
                continue
            fire = cal.preceding_fire_by_time(2 * k)
            if fire["k"] == k:
                return fire
        return None

    worst = None
    multi = []
    for P in range(5, 257):
        fire = first_fire(P)
        if fire is None:
            continue
        x = 6 * fire["k"] + 4
        T = 6 * fire["k"] + 5
        G = 0
        rows_ = []
        for _ in range(200):
            if x == 0 or x < 0:
                break
            j = v2(x)
            if j is None or j <= 4:
                rows_.append((j, G))
                break
            rows_.append((j, G))
            cr = read_cross(cal, j - 1)
            if not cr["odd"]:
                break
            x, T = step(x, T, cr)
            G += 1 + cr["eps"]
        if len(rows_) >= 3:
            multi.append((P, rows_))
            for (jj, GG) in rows_[1:]:
                if worst is None or (jj + GG) - jj > worst[4]:
                    worst = (P, jj, GG, jj + GG, GG, rows_)
    RES["gamma0_records"] = {
        "fires_with_ge3_chains": len(multi),
        "example": None if worst is None else {
            "P": worst[0], "interior_j0": worst[1], "Gamma0": worst[2],
            "record_at_entry": worst[3], "record_exceeds_j0": worst[3] > worst[1],
            "full_walk_rows": worst[5]},
    }
    # also list a couple of walks of length >= 3
    RES["gamma0_walks"] = [{"P": P, "rows": r} for (P, r) in multi[:5]]

    # ---------------------------------------------------------------- #
    # 6. O1 substitution: does the P=49 / eta_r source satisfy the
    #    theorem hypotheses?  Compute p_0, (S2*), (DEPTH).
    # ---------------------------------------------------------------- #
    fire = first_fire(49)
    sigma = fire["pointer"]
    kf = fire["k"]
    x0 = 5 << 49
    y = 2 * (x0 + 1) + 120 - x0 // 2
    A = (y - 10) // 16
    rows = []
    for r in (1, 2, 18, 19, 100):
        Q = 3 ** r
        C = -4 * Q + 8
        p0 = 1 + v2(3 * Q * 20 + C)
        # (S2*): 3Qk+C not= 0 mod 2^(j-2), j=49
        s2 = (3 * Q * 20 + C) % (1 << 47)
        # (DEPTH): Q*(kappa(49)+h) < 2^47, h = 4 (ht<=4)
        kappa49 = F(3, 2) * 48 * (2 * ((6 * 48 * 48 + 5 - 1).bit_length()) ** 2 + 1345)
        depth = Q * (kappa49 + 4) < (1 << 47)
        rows.append({"r": r, "p0": p0, "j_minus_2": 47, "S2star_holds": s2 != 0,
                     "DEPTH_holds": depth, "j": 49, "is_NT_gate": p0 == 48})
    RES["O1_substitution"] = {
        "P": 49, "k": kf, "sigma": str(sigma), "x0": str(x0), "A": str(A),
        "A_mod8": A % 8, "rows": rows,
        "reading": ("O1 is excluded by (S2*) because p_0 = 4 + v2(7*3^r+1) and the dangerous "
                    "region forces v2(7*3^r+1)=44, i.e. p_0=48=j-1; the theorem's (L1) is "
                    "exactly what fails. No refutation of THEOREM here."),
    }

    # ---------------------------------------------------------------- #
    # 7. O2 substitution: j=5, D=5, x=32u family.  It is a tie; the
    #    gateway record is m+1 while the entry record is 5.
    # ---------------------------------------------------------------- #
    rows = []
    for m in (6, 8, 12, 20, 100):
        u = ((1 << (m - 4)) - 1) // 3
        x = 32 * u
        T = x + 5
        xn = 2 * T + 6 - x // 2
        m_obs = v2(xn)
        rows.append({"m": m, "u_odd": u % 2 == 1, "x_next": str(xn),
                     "v2_x_next": m_obs, "entry_record": 5, "exit_record": m_obs + 1,
                     "record_rise": m_obs - 4, "theta5_mod16": 5 % 16,
                     "S3_m_plus_1_le_9": (m_obs + 1) <= 9})
    RES["O2_substitution"] = {
        "rows": rows,
        "reading": ("O2 states are ties with class 5 mod 16 and no predecessor; THEOREM only "
                    "claims block descent for A/B-type gateways, so O2 is not a counterexample "
                    "to a stated [A] claim, but it shows (S3) is not derivable from j=5 class data."),
    }

    # ---------------------------------------------------------------- #
    # 8. O3 sum, and the 2^64 comparison
    # ---------------------------------------------------------------- #
    S = 64
    tot = sum((2 * (S - 2 * r) + 1) * 3 ** r + 1 for r in range(0, S // 2 + 1))
    RES["O3_sum"] = {"S": S, "sum": str(tot), "below_2_64": tot < (1 << 64),
                     "exponent_of_2": (1 << 64)}

    # ---------------------------------------------------------------- #
    # 9. rational rank: r'=r+1 at j=5 gateway claims 3 does not divide C'
    #    for r>=1; check r=0 cases too (5,5) and (5,-11).
    # ---------------------------------------------------------------- #
    rr = []
    for (C, b) in ((5, 0), (-11, 0), (-27, 0), (21, 0)):
        Cp = 15 - C - 32 * b
        rr.append({"Q": 1, "C": C, "b": b, "C_prime": Cp, "div3": Cp % 3 == 0,
                   "rank_prime": 0 if Cp % 3 == 0 else 1})
    RES["gateway_rank_r0"] = rr

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps(RES, indent=1, default=str)[:12000])
    print("json:", OUT)


if __name__ == "__main__":
    main()
