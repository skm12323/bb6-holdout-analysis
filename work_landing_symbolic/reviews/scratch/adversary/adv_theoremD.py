#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Adversary check 4: direct test of the central class-determined claim
(THEOREM 2.4 / 5.2, Theorem L):
  (S2*) at every a-chain  =>  only strong descents and b/c steps, termination in
  <= j0-4 chains, all records <= j0+Gamma0, and the class mod 2^{j0+1} determines
  the parameter/type word.

Run: python -B work_landing_symbolic/reviews/scratch/adversary/adv_theoremD.py
"""
import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from work_global_calendar.calendar_oracle import Calendar  # noqa: E402

OUT = Path(__file__).resolve().with_name("adv_theoremD.json")


def v2(x):
    if isinstance(x, F):
        if x == 0:
            return None
        a, b = abs(x.numerator), x.denominator
        return (a & -a).bit_length() - (b & -b).bit_length()
    a = abs(int(x))
    return None if a == 0 else (a & -a).bit_length() - 1


def read_cross(cal, n):
    r = cal.crossing(n)
    d = {"kind": r["kind"], "odd": bool(r["odd"]), "tau": r["time"],
         "eps": r["epsilon"], "omega": r.get("omega"), "cW": None, "lam": None}
    if d["odd"] and d["kind"] != "a":
        d["cW"] = int((r["head_ratio"] + 2 * r["tail_ratio"]) * (1 << n))
        d["lam"] = r["head_lambda"] + 2 * r["tail_lambda"] + 3
        d["omega"] = v2(d["lam"])
    return d


def reduce3(C, Q):
    while Q > 1 and C % 3 == 0:
        C //= 3
        Q //= 3
    return C, Q


def class_walk(cal, j0, C, Q, b, maxsteps=400):
    """Class-driven walk with rational bookkeeping (canonical b/c shifts are integers)."""
    j, G = j0, 0
    rows = []
    status = "limit"
    for _ in range(maxsteps):
        if j <= 4:
            status = "end_small"
            break
        cr = read_cross(cal, j - 1)
        if not cr["odd"]:
            status = "end_even"
            break
        rows.append({"j": j, "G": G, "rec": j + G, "kind": cr["kind"]})
        if cr["kind"] == "a":
            k = cr["tau"] // 2
            z = 3 * Q * k + C
            p = None if z == 0 else 1 + v2(z)
            if p is not None and p <= j - 2:
                C, Q, b = 3 * Q - C, Q, 0
                j, G = p, G + 1
            else:
                return {"status": "s2_violated", "at_j": j, "p": p, "rows": rows}
        else:
            s = 3 * cr["tau"] + 5 - cr["lam"] - 2   # Phi - 2, an integer here
            C = C + Q * s
            b = 0
            C, Q = reduce3(C, Q)
            j, G = cr["omega"], G + 1 + cr["eps"]
    return {"status": status, "rows": rows, "final_j": j, "final_G": G}


def exact_word(cal, j0, delta, u, lift, limit=400):
    """Exact integer walk from x=2^j0 u, D = delta + lift*2^(j0+1)."""
    D = delta + lift * (1 << (j0 + 1))
    x = (1 << j0) * u
    T = x + D
    G = 0
    word = []
    for _ in range(limit):
        j = v2(x)
        if j is None:
            word.append(("zero", G))
            return word
        if j <= 4:
            word.append(("e", j, G))
            return word
        cr = read_cross(cal, j - 1)
        word.append((cr["kind"] if cr["odd"] else "e", j, G))
        if not cr["odd"]:
            return word
        tau = cr["tau"]
        if cr["kind"] == "a":
            k = tau // 2
            x, T = 2 * T + 6 * k - x // 2, T + 3 + 3 * tau
        else:
            x, T = cr["cW"] * (x >> j) + cr["lam"], T + 3 + 3 * tau
        G += 1 + cr["eps"]
    return word


def main():
    cal = Calendar(512)
    rng = random.Random(77123)
    RES = {"tests": 0, "violations": [], "s2_violated": 0}

    ok_claims = 0
    tested = 0
    for _ in range(4000):
        j0 = rng.randrange(5, 81)
        r = rng.randrange(0, 6)
        Q = 3 ** r
        C = rng.randrange(-(1 << 12), 1 << 12)
        if Q > 1 and C % 3 == 0:
            continue
        if C == 0:
            continue
        b = rng.randrange(0, 2)
        out = class_walk(cal, j0, C, Q, b)
        tested += 1
        if out["status"] == "s2_violated":
            RES["s2_violated"] += 1
            continue
        rows = out["rows"]
        steps_ok = all(rows[i + 1]["j"] <= rows[i]["j"] - 2 for i in range(len(rows) - 1))
        rec_ok = all(rows[i + 1]["rec"] <= rows[i]["rec"] - 1 for i in range(len(rows) - 1))
        len_ok = len(rows) <= max(j0 - 4, 1)
        if steps_ok and rec_ok and len_ok:
            ok_claims += 1
        elif len(RES["violations"]) < 10:
            RES["violations"].append({"j0": j0, "Q": Q, "C": C, "b": b,
                                      "status": out["status"], "rows": rows,
                                      "steps_ok": steps_ok, "rec_ok": rec_ok,
                                      "len_ok": len_ok})
    RES["tests"] = tested
    RES["theoremD_ok"] = ok_claims
    RES["theoremD_violations"] = len(RES["violations"])

    # same class, different u / lift: HP spot check
    same = 0
    diff = 0
    examples = []
    for _ in range(300):
        j0 = rng.randrange(5, 31)
        delta = rng.randrange(0, 1 << (j0 + 1))
        w1 = exact_word(cal, j0, delta, 1, 0)
        w2 = exact_word(cal, j0, delta, 3, 1)
        w3 = exact_word(cal, j0, delta, 5, 2)
        if w1 == w2 == w3:
            same += 1
        else:
            diff += 1
            if len(examples) < 6:
                examples.append({"j0": j0, "delta": delta,
                                 "w1": w1[:10], "w2": w2[:10], "w3": w3[:10]})
    RES["hp_same_class"] = {"same": same, "different": diff, "examples": examples}

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps(RES, indent=1, default=str)[:6000])
    print("json:", OUT)


if __name__ == "__main__":
    main()
