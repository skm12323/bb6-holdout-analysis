#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Adversary check 2: the claimed Z[1/3] extension of work_deep Lemma 2.2
(used by THEOREM.md (A4): j>=N0+1 and |theta|<=B-3 implies no tie).

Construction: for a chain parameter j with calendar half-time k, choose r with
3^r <= 2^(j-2)/(3k) < 3^(r+1) and set theta = 2^(j-2)/3^r - 3k.
Then |theta| <= 6k, theta in Z[1/3], and v2(3k+theta) = j-2 exactly: a tie.
Also checks the full affine ledger (beta'=0 etc.) and the resulting record J+e.

Run: python -B work_landing_symbolic/reviews/scratch/adversary/adv_z13.py
"""
import json
import sys
from fractions import Fraction as F
from math import log2
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from work_global_calendar.calendar_oracle import Calendar  # noqa: E402

OUT = Path(__file__).resolve().with_name("adv_z13.json")


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


def construct(j, k):
    """theta = 2^(j-2)/3^r - 3k, with r maximal s.t. 3^r <= 2^(j-2)/(3k)."""
    num = 1 << (j - 2)
    den = 3 * k
    r = int((j - 2) * 0.6309297535714574) - 4  # log3(2) * (j-2), generous start
    if r < 0:
        r = 0
    while 3 ** (r + 1) * den <= num:
        r += 1
    while 3 ** r * den > num:
        r -= 1
    theta = F(num, 3 ** r) - 3 * k
    return r, theta


def main():
    cal = Calendar(512)
    rows = []
    # small j with the canonical calendar k
    for j in (20, 40, 61, 100, 200, 400):
        cr = cal.crossing(j - 1)
        if not (cr["odd"] and cr["kind"] == "a"):
            rows.append({"j": j, "skipped": "crossing not odd a"})
            continue
        k = cr["time"] // 2
        r, theta = construct(j, k)
        z = 3 * k + theta
        # affine data: beta=0, d=(theta-1)/3, U=1, J=j (Gamma=0)
        d = (theta - 1) / 3
        U = 1
        X = 1 << j
        T = X + theta  # Theta = 2^j U + 3d + 1 = 2^j + theta
        beta = F(0)
        alpha = F(1)
        J = j
        G = 0
        # a step
        beta2 = 6 * d + 2 + 6 * k - beta / 2
        alpha2 = 2 - alpha / 2
        d2 = d + 1 + 2 * k
        x2 = alpha2 * (1 << J) * U + beta2
        ell = j - 1
        e = v2(F(alpha2 * (1 << J), 1 << ell) * U + beta2 / (1 << ell))
        jn = v2(x2)
        rec = jn + G + 1
        rows.append({
            "j": j, "k": k, "r": r,
            "theta": str(theta), "theta_abs_float": float(abs(theta)),
            "v2_3k_theta": v2(z), "j_minus_2": j - 2,
            "tie": v2(z) == j - 2,
            "d_in_Z13": True, "beta": "0",
            "beta2": str(beta2), "v2_beta2": v2(beta2), "ell": ell,
            "e": e, "j_next": jn, "record_next": rec, "J": J,
            "record_exceeds_J": rec > J,
            "theta_within_B_minus_3": float(abs(theta)) < 2 ** (10 ** 7) - 3,
        })
    # deep instance: stated algebraically (no giant powers computed).
    # For any deep j with calendar half-time k>=1, choose r maximal with
    # 3^r <= 2^(j-2)/(3k); then theta = 2^(j-2)/3^r - 3k satisfies
    #   3k + theta = 2^(j-2)/3^r,  so v2(3k+theta) = j-2  (a tie),
    #   0 < 3k+theta <= 3k, so |theta| <= 6k <= 2*kappa(j) << B-3.
    # Only the value of r (a log_3) is needed; no big integer is formed.
    rows.append({
        "j": "any j >= N0+1 with calendar k>=1",
        "identity": "3k+theta = 2^(j-2)/3^r with r=max{r: 3^r <= 2^(j-2)/(3k)}",
        "v2_3k_theta_proved": "j-2 (exact, since 3k+theta = 2^(j-2)/3^r)",
        "tie": True,
        "abs_theta_bound": "|theta| <= 6k <= 2*kappa(j) << B-3 for j >= N0",
        "computed": False,
        "note": ("algebraic; the same identity is verified exactly below at j<=400 "
                 "with the true calendar half-time k"),
    })

    RES = {
        "claim_attacked": ("THEOREM.md 2.7 (A4) / affine/RESULT.md A4: j>=N0+1, |theta|<=B-3 "
                           "implies no tie, via a 'Z[1/3] extension' of work_deep Lemma 2.2"),
        "mechanism": ("work_deep Lemma 2.2 uses |z|>=2^v2(z) for INTEGER z. For theta=C/3^r, "
                      "z=(3^(r+1)k+C)/3^r has v2(z)=v2(3^(r+1)k+C) which can be j-2 while "
                      "|z|<2^(j-2); the family below realizes exactly that at every j."),
        "rows": rows,
        "all_ties": all(r.get("tie", True) for r in rows),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(RES, f, indent=1)
    print(json.dumps(RES, indent=1)[:9000])
    print("json:", OUT)


if __name__ == "__main__":
    main()
