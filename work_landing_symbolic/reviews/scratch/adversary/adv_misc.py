#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Adversary check 3: small-range test of the inherited [B] window certificate,
the relation of the 24 exceptions to the window, the RAT-C family heights, and a
few quoted constants.

Run: python -B work_landing_symbolic/reviews/scratch/adversary/adv_misc.py
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from work_global_calendar.calendar_oracle import Calendar  # noqa: E402

OUT = Path(__file__).resolve().with_name("adv_misc.json")


def v2(x):
    x = abs(int(x))
    if x == 0:
        return None
    return (x & -x).bit_length() - 1


def read_cross(cal, n):
    r = cal.crossing(n)
    d = {"kind": r["kind"], "odd": bool(r["odd"]), "tau": r["time"],
         "eps": r["epsilon"], "omega": r.get("omega"), "cW": None, "lam": None}
    if d["odd"] and d["kind"] != "a":
        d["cW"] = int((r["head_ratio"] + 2 * r["tail_ratio"]) * (1 << n))
        d["lam"] = r["head_lambda"] + 2 * r["tail_lambda"] + 3
        d["omega"] = v2(d["lam"])
    return d


def exact_walk(cal, x, T, P, limit=20000):
    G = 0
    maxrec = -1
    for _ in range(limit):
        if x == 0:
            return {"status": "zero", "maxrec": maxrec}
        if x < 0:
            return {"status": "nonpositive", "maxrec": maxrec}
        j = v2(x)
        if j is None:
            return {"status": "bad", "maxrec": maxrec}
        if j + G >= P:
            return {"status": "ceiling", "maxrec": maxrec}
        maxrec = max(maxrec, j + G)
        if j <= 4:
            return {"status": "end", "maxrec": maxrec}
        cr = read_cross(cal, j - 1)
        if not cr["odd"]:
            return {"status": "end", "maxrec": maxrec}
        if cr["kind"] == "a":
            k = cr["tau"] // 2
            x, T = 2 * T + 6 * k - x // 2, T + 3 + 3 * cr["tau"]
        else:
            x, T = cr["cW"] * (x >> j) + cr["lam"], T + 3 + 3 * cr["tau"]
        G += 1 + cr["eps"]
    return {"status": "limit", "maxrec": maxrec}


def certify(cal, j, delta):
    r = exact_walk(cal, 1 << j, (1 << j) + delta, j + 1)
    return r["status"] == "end" and r["maxrec"] <= j


def main():
    cal = Calendar(512)
    RES = {}

    # 1. window certificate in the accessible range 6..200, delta in [-12,15]
    fails = []
    nwin = 0
    for j in range(5, 201):
        for d in range(-12, 16):
            nwin += 1
            if not certify(cal, j, d):
                fails.append([j, d])
    RES["window_check"] = {"range": "5<=j<=200, -12<=d<=15", "checked": nwin,
                           "failures": fails,
                           "matches_claim": fails == [] or
                           [f for f in fails if f[0] > 5] == []}

    # 2. the 24 exceptions: is any of them inside the window (mod 2^(j+1))?
    exc = {
        5: [5, 21, -27, -11],
        8: [58, 186, -198, -70],
        12: [1012, 3060, -3084, -1036],
        14: [4081, 12273, -12303, -4111],
        17: [32702, 32750, 98238, 98286, -98370, -98322, -32834, -32786],
    }
    rows = []
    for j, ds in exc.items():
        M = 1 << (j + 1)
        for d in ds:
            reps = [d + t * M for t in range(-3, 4)]
            inwin = [r for r in reps if -12 <= r <= 15]
            rows.append({"j": j, "delta": d, "in_window_rep": inwin,
                         "certified": certify(cal, j, d % M)})
    RES["exceptions"] = {"rows": rows,
                         "any_in_window": any(r["in_window_rep"] for r in rows),
                         "all_bad": all(not r["certified"] for r in rows)}

    # 3. RAT-C families: max A_t and h_t (three families, m<=1000)
    def class_walk_A(j, C, Q, b):
        C = F(C)
        Q = F(Q)
        G = 0
        As = []
        steps = 0
        for _ in range(20):
            row = read_cross(cal, j - 1)
            if not row["odd"]:
                return {"status": "end", "steps": steps, "maxA": max(As) if As else F(0)}
            tau = row["tau"]
            As.append(abs(C / Q - F(3, 2)))
            if row["kind"] == "a":
                k = tau // 2
                val = v2(3 * Q * k + C)
                p = None if val is None else 1 + val
                if p is not None and p <= j - 2:
                    C, Q, b, j2 = 3 * Q - C, Q, 0, p
                    G += 1
                elif p is None or p >= j:
                    C2 = (9 + 6 * k) * Q - C - b * Q * (1 << j)
                    Q2 = F(3) * Q
                    while C2 % 3 == 0 and Q2 > 1:
                        C2 = C2 / 3
                        Q2 = Q2 / 3
                    C, Q, b, j2 = C2, Q2, 1, j - 1
                    G += 1
                else:
                    return {"status": "gateway" if j == 5 else "nt", "steps": steps,
                            "maxA": max(As)}
            else:
                phi = 3 * tau + 5 - row["lam"]
                s = F(phi - 2)
                C = C + Q * s
                # reduce by 3
                while C.denominator > 1:
                    break
                Q2 = Q
                # keep denom normal form 3^r
                b = 0
                j2 = row["omega"]
                G += 1 + row["eps"]
            j = j2
            steps += 1
        return {"status": "limit", "steps": steps, "maxA": max(As)}

    fam = {"(10-2^m)/3": [], "(26-2^m)/3": [], "BBBAA C/3": []}
    for m in range(19, 1001):
        fam["(10-2^m)/3"].append(class_walk_A(m, 10, 3, 1))
        fam["(26-2^m)/3"].append(class_walk_A(m, 26, 3, 1))
        for old in (-2, 1, 4, 7, 10, 13, 16):
            if (m - 19) % 7 == old % 7:
                fam["BBBAA C/3"].append(class_walk_A(m, 3 * old + 4, 3, 0))
    summ = {}
    for k, v in fam.items():
        st = {}
        for d in v:
            st[d["status"]] = st.get(d["status"], 0) + 1
        summ[k] = {"counts": st, "maxA": str(max((d["maxA"] for d in v), default=0)),
                   "maxsteps": max((d["steps"] for d in v), default=0)}
    RES["ratc_families"] = summ
    RES["ratc_note"] = "max A_t quoted in THEOREM 2.8 is 95/6 = %.6f" % (95 / 6)

    # 4. quoted constants
    def ceil_log2(m):
        return (m - 1).bit_length()

    def P(n):
        return 2 * ceil_log2(6 * n * n + 5) ** 2 + 1345

    def kappa(j):
        return F(3, 2) * (j - 1) * P(j - 1)

    RES["constants"] = {
        "kappa19": str(kappa(19)), "kappa18": str(kappa(18)), "kappa49": str(kappa(49)),
        "3(k19+31)": str(3 * (kappa(19) + 31)), "2^17": 1 << 17,
        "k18+31": str(kappa(18) + 31), "2^16": 1 << 16,
        "3(k19+841)": str(3 * (kappa(19) + 841)),
        "3(k19+842)": str(3 * (kappa(19) + 842)),
    }

    # 5. a few crossings used in quotes
    RES["crossings"] = {}
    for n in (4, 5, 27, 28, 29, 6132):
        try:
            r = read_cross(cal, n)
            RES["crossings"][str(n)] = {"kind": r["kind"], "odd": r["odd"],
                                        "tau": r["tau"], "eps": r["eps"],
                                        "omega": r["omega"]}
        except Exception as exc:  # noqa: BLE001
            RES["crossings"][str(n)] = {"error": str(exc)}

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps(RES, indent=1, default=str)[:9000])
    print("json:", OUT)


if __name__ == "__main__":
    main()
