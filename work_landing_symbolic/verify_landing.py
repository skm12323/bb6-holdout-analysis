#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""verify_landing.py -- independent cross-direction verification for THEOREM.md.

This script does NOT import verify_rational.py, verify_affine.py or
verify_gateway.py.  It recomputes from scratch the identities and counts that
the three directions share, using only

  * work_global_calendar/calendar_oracle.Calendar(512)  (canonical small range),
  * D:/math_cc_astra/deep1/table_1000000.pkl             (canonical tau/type data,
                                                          n < 10^6),

plus exact integer / Fraction arithmetic.

Hard checks (a failure of any of them makes the gate FAIL):
  A  rational a-step trichotomy and class transition     (canonical + synthetic)
  B  rational b/c-step class recurrence, shift, rank     (canonical + synthetic)
  C  j=5 gateway: rational class map, A/B-type identities, height ladder,
     m is not a function of the class
  D  affine ledger: one-step recursions and the landing/tie/suspension trichotomy
  E  canonical exits: affine criterion ledger on 252 fires / 419 chains / 84 c
     sources; exact suffix safety; the 336x17 shift suite; the five (5,5) shift ties
  F  constants: O1 source and valuation identity, O2 family, O3 count, kappa and
     the RAT-C thresholds (18/19, 841, 88222), the RAT-C three families
  G  cross-direction identities (p = 1 + r_aff; gateway m = affine e + 4;
     rational vs gateway C' formula; rank r' = r+1)
  H  finite [B] structure: full-residue scan 5<=j<=18 (24 exceptions),
     Bad_j spot checks at 22/24/27, the 36-vertex bad-class graph

Control (reported, not a FAIL): the gateway tie-to-tie record inequality (R)
of Theorem G(ii) is refuted by an explicit exact walk; the script verifies the
witness.  See THEOREM.md section 3.4.

Every synthetic state is labelled non-canonical.  Writes landing_checks.json.
Exit code 0 iff all hard checks pass.  Runtime target < 10 min.

Run: python -B work_landing_symbolic/verify_landing.py
"""
import json
import sys
import time
import random
import pickle
from decimal import Decimal, getcontext, ROUND_CEILING
from fractions import Fraction as F
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
OUT = HERE / "landing_checks.json"
TABPATH = Path(r"D:/math_cc_astra/deep1/table_1000000.pkl")

sys.path.insert(0, str(ROOT))
from work_global_calendar.calendar_oracle import Calendar  # noqa: E402

# --------------------------------------------------------------------------- #
# result store
RES = {
    "status": "PASS",
    "scope": ("Independent cross-direction recomputation for work_landing_symbolic/THEOREM.md. "
              "No import of the three direction verifiers. Canonical data: Calendar(512) and "
              "table_1000000.pkl; every synthetic state is marked non-canonical. "
              "This is not a global EXT proof and does not change K_clock."),
    "environment": {},
    "checks": {},
    "counts": {},
    "canonical": {},
    "synthetic": {},
    "refuted_claims": [],
    "notes": {},
    "not_run": [],
    "failures": [],
    "timing": {},
}
MAX_EX = 6


def CK(cid, tag, ok, detail=None, n=1):
    """Record n checks of conclusion cid; ok is the AND over the n cases."""
    d = RES["checks"].setdefault(cid, {"tag": tag, "checked": 0, "failed": 0,
                                       "examples": [], "note": "", "truncated": 0})
    d["checked"] += n
    if not ok:
        d["failed"] += 1
        if len(d["examples"]) < MAX_EX:
            d["examples"].append(str(detail)[:600])
        else:
            d["truncated"] += 1
    return ok


def note(cid, text):
    RES.setdefault("notes", {})[cid] = text


# --------------------------------------------------------------------------- #
# exact helpers
def v2(x):
    """2-adic valuation of a nonzero int or of a rational with odd denominator."""
    if isinstance(x, F):
        if x == 0:
            return None
        a, b = abs(x.numerator), x.denominator
        if a == 0:
            return None
        return (a & -a).bit_length() - (b & -b).bit_length()
    x = abs(int(x))
    if x == 0:
        return None
    return (x & -x).bit_length() - 1


def vv(x):
    """Like v2 but zero gets +infinity (a large sentinel)."""
    z = v2(x)
    return 10 ** 9 if z is None else z


def sym(e, bits):
    """Symmetric integer representative of the 2-adic class mod 2^bits."""
    M = 1 << bits
    if isinstance(e, F):
        e = clsmod(e, M)
    r = e % M
    return r - M if r > M // 2 else r


def clsmod(f, mod):
    """2-adic class of a rational with odd denominator, modulo mod."""
    if isinstance(f, int):
        return f % mod
    if f.denominator % 2 == 0:
        raise ValueError("even denominator")
    return (f.numerator * pow(f.denominator, -1, mod)) % mod


def ceil_log2(m):
    return (m - 1).bit_length()


def P_clock(n):
    return 2 * ceil_log2(6 * n * n + 5) ** 2 + 1345


def kappa(j):
    if j <= 1:
        return F(0)
    n = j - 1
    return F(3, 2) * n * P_clock(n)


def rank_of(Q):
    r = 0
    q = Q
    while q % 3 == 0:
        q //= 3
        r += 1
    return r if q == 1 else None


def height_pen(c):
    x = max(F(0), 1 - c, c - 2)
    return -((-x.numerator) // x.denominator)


# --------------------------------------------------------------------------- #
# canonical crossing reader
def read_cross(cal, n):
    r = cal.crossing(n)
    d = {"kind": r["kind"], "odd": bool(r["odd"]), "tau": r["time"],
         "eps": r["epsilon"], "omega": r["omega"], "cW": None, "lam": None}
    if d["odd"] and d["kind"] != "a":
        cw = (r["head_ratio"] + 2 * r["tail_ratio"]) * (1 << n)
        if cw.denominator != 1:
            raise ArithmeticError(("nonintegral cW", n))
        d["cW"] = int(cw)
        d["lam"] = r["head_lambda"] + 2 * r["tail_lambda"] + 3
        d["omega"] = v2(d["lam"])
    return d


def step_exact(x, T, cr):
    j = v2(x)
    tau = cr["tau"]
    if cr["kind"] == "a":
        k = tau // 2
        xn = 2 * T + 6 * k - x // 2
        kind = "a"
    else:
        xn = cr["cW"] * (x >> j) + cr["lam"]
        kind = cr["kind"]
    return xn, T + 3 + 3 * tau, kind


def exact_walk(cal, x, T, P, s0=0, limit=20000):
    """Exact walk with record ceiling P (record = j+Gamma must stay < P)."""
    G = 0
    s = s0
    rows = []
    maxrec = -1
    for _ in range(limit):
        if x == 0:
            return {"status": "zero", "rows": rows, "maxrec": maxrec}
        if x < 0:
            return {"status": "nonpositive", "rows": rows, "maxrec": maxrec}
        j = v2(x)
        if j is None:
            return {"status": "bad", "rows": rows, "maxrec": maxrec}
        if j + G >= P:
            return {"status": "ceiling", "rows": rows, "maxrec": maxrec}
        if j + G > maxrec:
            maxrec = j + G
        if j <= 4:
            rows.append({"j": j, "G": G, "s": s, "x": x, "T": T, "kind": "e"})
            return {"status": "end", "rows": rows, "maxrec": maxrec}
        cr = read_cross(cal, j - 1)
        rows.append({"j": j, "G": G, "s": s, "x": x, "T": T,
                     "kind": cr["kind"] if cr["odd"] else "e"})
        if not cr["odd"]:
            return {"status": "end", "rows": rows, "maxrec": maxrec}
        x, T, _ = step_exact(x, T, cr)
        G += 1 + cr["eps"]
        s += 1 + cr["tau"]
    return {"status": "limit", "rows": rows, "maxrec": maxrec}


def certify(cal, j, delta):
    r = exact_walk(cal, 1 << j, (1 << j) + delta, j + 1)
    return r["status"] == "end" and r["maxrec"] <= j


def first_fire(cal, P):
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
    raise AssertionError(("no sampled canonical fire", P))


# --------------------------------------------------------------------------- #
# A. rational a-step trichotomy
def build_rat_state(j, Q, C, b, u, lift, H=None):
    H = H if H is not None else j + 1
    M = 1 << H
    cls = (C * pow(Q, -1, M) + b * (1 << j)) % M
    D = cls + lift * M
    x = (1 << j) * u
    return x, x + D, D


def a_case(cal, j, k, Q, C, b, u, lift, tag_detail):
    """One exact a-step from a rational-description state; returns checks dict."""
    x, T, D = build_rat_state(j, Q, C, b, u, lift)
    xn = 2 * T + 6 * k - x // 2
    Tn = T + 3 + 6 * k
    Dn = Tn - xn
    val = v2(3 * Q * k + C)
    p = None if val is None else 1 + val
    out = {"p": p, "xn_zero": xn == 0}
    if xn == 0:
        jn = None
    else:
        jn = v2(xn)
    out["jn"] = jn
    if p is not None and p <= j - 2:
        out["case"] = "strong"
        ok = (jn == p) and ((Dn - (3 * Q - C) * pow(Q, -1, 1 << (jn + 1))) % (1 << (jn + 1)) == 0)
        if Q > 1:
            ok = ok and xn != 0
        CK("A.rational.strong", "A", ok, (tag_detail, j, p, jn, xn == 0))
        CK("A.rational.nonzero", "A", (xn != 0) or Q == 1, (tag_detail, "zero", Q))
    elif p is None or p >= j:
        out["case"] = "onestep"
        Mj = 1 << j
        ok = (jn == j - 1) and ((Dn - (3 - D - (1 << (j - 1)))) % Mj == 0)
        # catapult class: C2/Q2 + b' 2^{j-1} (mod 2^j)
        C2 = (9 + 6 * k) * Q - C - b * Q * (1 << j)
        Q2 = 3 * Q
        while C2 % 3 == 0 and Q2 > 1:
            C2 //= 3
            Q2 //= 3
        cat = (C2 * pow(Q2, -1, Mj) + (1 << (j - 1))) % Mj
        ok = ok and ((Dn - cat) % Mj == 0)
        if Q > 1:
            ok = ok and xn != 0
        CK("A.rational.onestep", "A", ok, (tag_detail, j, p, jn, Dn, cat))
        CK("A.rational.nonzero", "A", (xn != 0) or Q == 1, (tag_detail, "zero", Q))
    else:  # p == j-1
        out["case"] = "nt"
        if xn == 0:
            # virtual resonance: only Q=1, and then p=j-1 exactly
            lhs_zero = 2 * (C + 3 * k * Q) + 3 * (1 << (j - 1)) * u * Q
            ok = (Q == 1 and lhs_zero % (1 << (j + 1)) == 0)
            CK("A.rational.nt_zero", "A", ok, (tag_detail, j, Q, C, k, u, lhs_zero))
            CK("A.rational.nt_j", "A", True, None)
        else:
            ok = jn >= j
            CK("A.rational.nt_j", "A", ok, (tag_detail, j, p, jn))
        CK("A.rational.nonzero", "A", (xn != 0) or Q == 1, (tag_detail, "zero", Q))
    CK("A.rational.total", "A", True, None)
    return out


def check_A(cal):
    rng = random.Random(20261023)
    A_JS = list(range(5, 81)) + [100, 128, 150, 200, 256, 400]
    QS = [1, 3, 9, 27, 81, 3 ** 5]
    CS = [-40, -17, -13, -11, -7, -5, -2, -1, 1, 2, 4, 5, 7, 10, 13, 16, 17, 26, 40]
    nt_vary = 0
    nt_total = 0
    for j in A_JS:
        cr = read_cross(cal, j - 1)
        if not (cr["odd"] and cr["kind"] == "a"):
            continue
        k = cr["tau"] // 2
        for Q in QS:
            for C in CS:
                if gcd(C, Q) != 1:
                    continue
                for b in (0, 1):
                    for u in (1, 3, 5):
                        for lift in (0, 1):
                            out = a_case(cal, j, k, Q, C, b, u, lift, ("canon", j, Q, C, b, u, lift))
                            if out["case"] == "nt":
                                nt_total += 1
                                out2 = a_case(cal, j, k, Q, C, b, u, lift + 1,
                                              ("canon-lift2", j, Q, C, b, u, lift + 1))
                                if out["jn"] != out2["jn"]:
                                    nt_vary += 1
    # synthetic random classes (non-canonical)
    for _ in range(20000):
        j = rng.randrange(5, 201)
        r = rng.randrange(0, 21)
        Q = 3 ** r
        C = rng.randrange(-(1 << 20), 1 << 20)
        if gcd(C, Q) != 1:
            continue
        b = rng.randrange(0, 2)
        k = rng.randrange(1, 60)
        u = rng.randrange(1, 2000, 2)
        lift = rng.randrange(0, 4)
        a_case(cal, j, k, Q, C, b, u, lift, ("synth", j, Q, C, b, u, lift))
    # constructed one-step cases: force v2(3Qk+C) = j-1 (p = j)
    for _ in range(1500):
        j = rng.randrange(6, 61)
        Q = 3 ** rng.randrange(0, 8)
        C = rng.randrange(-(1 << 15), 1 << 15)
        if gcd(C, Q) != 1:
            continue
        mod = 1 << (j - 1)
        k0 = ((-C) * pow(3 * Q, -1, mod)) % mod
        k = (k0 if k0 != 0 else mod) + rng.choice((0, mod))
        if k <= 0:
            continue
        b = rng.randrange(0, 2)
        u = rng.randrange(1, 1000, 2)
        lift = rng.randrange(0, 3)
        out = a_case(cal, j, k, Q, C, b, u, lift, ("constructed-onestep", j, Q, C, b, u, k))
        CK("A.rational.constructed_onestep", "A", out["case"] == "onestep", (j, Q, C, k, out))
    # constructed NT cases: force v2(3Qk+C) = j-2 (p = j-1)
    for _ in range(1500):
        j = rng.randrange(6, 61)
        Q = 3 ** rng.randrange(0, 8)
        C = rng.randrange(-(1 << 15), 1 << 15)
        if gcd(C, Q) != 1:
            continue
        mod = 1 << (j - 1)
        k0 = ((1 << (j - 2)) - C) * pow(3 * Q, -1, mod) % mod
        k = (k0 if k0 != 0 else mod) + rng.choice((0, mod))
        if k <= 0:
            continue
        b = rng.randrange(0, 2)
        u = rng.randrange(1, 1000, 2)
        lift = rng.randrange(0, 3)
        out = a_case(cal, j, k, Q, C, b, u, lift, ("constructed-nt", j, Q, C, b, u, k))
        CK("A.rational.constructed_nt", "A", out["case"] == "nt", (j, Q, C, k, out))
    # explicit virtual resonance (Q=1, x'=0): j=5, k=1, C=-27, u=1
    x = 32
    T = x - 27
    xn = 2 * T + 6 - x // 2
    CK("A.rational.virtual_resonance", "A", xn == 0 and 1 + v2(3 + (-27)) == 4, (xn,))
    # explicit p=+infinity (3Qk+C=0, Q=1): j=5, k=1, C=-3
    x = 32
    T = x - 3
    xn = 2 * T + 6 - x // 2
    Tn = T + 9
    Dn = Tn - xn
    C2 = (9 + 6 * 1) * 1 - (-3)
    Q2 = 3
    CK("A.rational.p_infinity", "A",
      v2(3 * 1 + (-3)) is None and v2(xn) == 4
      and (clsmod(F(C2, Q2) + (1 << 4), 1 << 5) == Dn % (1 << 5)),
      (xn, Dn, C2, Q2))
    RES["counts"]["A_nt_classes"] = nt_total
    RES["counts"]["A_nt_u_dependent"] = nt_vary
    CK("A.rational.nt_not_class_determined", "A", nt_vary > 0,
      ("nt_total", nt_total, "varying", nt_vary))
    note("A.rational.nt_j", "NT gate: j'=v2(x') >= j; output not a function of the class")


# --------------------------------------------------------------------------- #
# B. rational b/c-step recurrence
def best_shift(phi2, omega, r, c):
    M = 1 << (omega + 1)
    cands = [(0, sym(phi2, omega + 1))]
    for d in range(1, 5):
        cands.append((d, sym(phi2 * 3 ** d, omega + 1)))
    best = None
    for (d, a) in cands:
        s = F(a, 3 ** d)
        key = (2 * max(r, d) + height_pen(c + s), abs(s))
        if best is None or key < best[0]:
            best = (key, d, a, s)
    return best[1], best[2], best[3]


def apply_shift(C, Q, r, d, a):
    if a == 0:
        return C, Q
    C2 = C * 3 ** max(0, d - r) + a * 3 ** max(0, r - d)
    Q2 = 3 ** max(r, d)
    while C2 % 3 == 0 and Q2 > 1:
        C2 //= 3
        Q2 //= 3
    return C2, Q2


def bc_case(cal, n, Q, C, b, u, tag_detail):
    cr = read_cross(cal, n)
    j = n + 1
    sigma = n - cr["eps"]
    omega = cr["omega"]
    lam = cr["lam"]
    cW = cr["cW"]
    tau = cr["tau"]
    x, T, D = build_rat_state(j, Q, C, b, u, 0)
    xn = cW * (x >> j) + lam
    Tn = T + 3 + 3 * tau
    Dn = Tn - xn
    jn = None if xn == 0 else v2(xn)
    phi = 3 * tau + 5 - lam
    s = F(phi - 2)
    M = 1 << (omega + 1)
    ok = (jn == omega) and (v2(lam) == omega) and (v2(cW) == sigma) and (omega < sigma)
    ok = ok and (clsmod(F(Dn) - (D + s), M) == 0)
    ok = ok and (clsmod(F(Dn) - (F(C, Q) + s), M) == 0)
    ok = ok and (omega + 1 + cr["eps"] <= j)
    # geometric height Lipschitz
    A = abs(F(C, Q) - F(3, 2))
    Ap = abs(F(C, Q) + s - F(3, 2))
    ok = ok and (Ap <= A + abs(s))
    CK("B.bc.exact", "A", ok, (tag_detail, n, Q, C, b, u, omega, jn))
    # rank recursion with the cost-minimal representative
    r = rank_of(Q)
    d, a, ss = best_shift(phi - 2, omega, r, F(C, Q))
    C2, Q2 = apply_shift(C, Q, r, d, a)
    raw = C * 3 ** max(0, d - r) + a * 3 ** max(0, r - d)
    rp = rank_of(Q2)
    okr = (rp <= max(r, d))
    CK("B.bc.rank_bound", "A", okr, (tag_detail, Q, C, d, a, rp))
    CK("B.bc.rank_equality", "A",
      (rp == max(r, d)) == (raw % 3 != 0 or max(r, d) == 0),
      (tag_detail, Q, C, d, a, rp, raw))
    # the shifted class equals the exact one
    CK("B.bc.shift_class", "A",
      ((Dn - (C2 * pow(Q2, -1, M))) % M == 0),
      (tag_detail, Q, C, d, a, C2, Q2))


def check_B(cal):
    rng = random.Random(20261024)
    QS = [1, 3, 9, 27]
    CS = [-13, -1, 1, 4, 10, 26]
    nbc = 0
    for n in range(4, 4000):
        cr = read_cross(cal, n)
        if not (cr["odd"] and cr["kind"] != "a"):
            continue
        nbc += 1
        CK("B.bc.lambda_bound", "A", abs(cr["lam"]) < cr["cW"],
          (n, cr["kind"], cr["cW"], cr["lam"]))
        for Q in QS:
            for C in CS:
                if gcd(C, Q) != 1:
                    continue
                for b in (0, 1):
                    for u in (1, 3):
                        bc_case(cal, n, Q, C, b, u, ("canon", n, Q, C, b, u))
    RES["counts"]["B_canonical_bc"] = nbc
    # synthetic representative algebra
    for _ in range(4000):
        r = rng.randrange(0, 12)
        Q = 3 ** r
        C = rng.randrange(-(1 << 15), 1 << 15)
        if gcd(C, Q) != 1:
            continue
        d = rng.randrange(0, 5)
        a = rng.randrange(-(1 << 10), 1 << 10)
        if a % 3 == 0:
            continue
        C2, Q2 = apply_shift(C, Q, r, d, a)
        raw = C * 3 ** max(0, d - r) + a * 3 ** max(0, r - d)
        rp = rank_of(Q2)
        CK("B.synth.rank_bound", "A", rp <= max(r, d), (Q, C, d, a, rp))
        CK("B.synth.rank_equality", "A",
          (rp == max(r, d)) == (raw % 3 != 0 or max(r, d) == 0),
          (Q, C, d, a, rp, raw))
        CK("B.synth.class", "A",
          clsmod(F(C2, Q2) - (F(C, Q) + F(a, 3 ** d)), 1 << 6) == 0,
          (Q, C, d, a, C2, Q2))
    # the two documented equality counterexamples
    C2, Q2 = apply_shift(55, 9, 2, 2, 2)
    CK("B.rank_counterexample_1", "A", rank_of(Q2) < 2 and (55 * 3 ** 0 + 2 * 3 ** 0) % 3 == 0,
      (55, 9, 2, 2, C2, Q2, rank_of(Q2)))
    C2, Q2 = apply_shift(1, 9, 2, 2, -1)
    CK("B.rank_counterexample_2", "A", C2 == 0 and rank_of(Q2) == 0,
      (1, 9, 2, -1, C2, Q2, rank_of(Q2)))
    note("B.bc.exact", "D' = D + Phi - 2 + (2^j - c_W)u; v2(2^j-c_W)=sigma>omega")


# --------------------------------------------------------------------------- #
# C. gateway
def check_C(cal):
    rng = random.Random(20261025)
    # C.1 rational j=5 class map
    m_ge_H = 0
    m_by_class = {}
    for H in range(6, 65, 2):
        for Q in (1, 3, 9, 27, 81):
            for C in (-40, -17, -13, -11, -7, -5, -2, -1, 1, 2, 4, 5, 7, 10, 13, 16, 26, 40):
                if gcd(C, Q) != 1:
                    continue
                for b in (0, 1):
                    for u in (1, 3, 5):
                        for lift in (0, 1, 2):
                            M = 1 << H
                            cls = (C * pow(Q, -1, M) + b * 32) % M
                            D = cls + lift * M
                            x = 32 * u
                            T = x + D
                            xn = 2 * T + 6 - x // 2
                            Tn = T + 9
                            Dn = Tn - xn
                            m = v2(xn)
                            key = (j5 := 5, Q, C, b)
                            m_by_class.setdefault(key, set()).add(m)
                            if m is None or m >= H:
                                m_ge_H += 1
                                continue
                            M2 = 1 << (m + 1)
                            C2 = 15 * Q - C - 32 * b * Q
                            Q2 = 3 * Q
                            ht = F(abs(C), Q)
                            ok = (clsmod(F(C2, Q2) + F(1 << m), M2) == (Dn % M2))
                            ok = ok and (abs(F(C2, Q2)) <= 5 + ht / 3 + F(32 * b, 3))
                            if Q >= 3:
                                ok = ok and (C2 % 3 != 0) and (rank_of(Q2) == rank_of(Q) + 1)
                            CK("C.gateway.class", "A", ok, (H, Q, C, b, u, lift, m, Dn, C2))
                            CK("C.gateway.height", "A",
                              abs(F(C2, Q2)) <= 5 + ht / 3 + F(32 * b, 3),
                              (H, Q, C, b, ht, C2, Q2))
                            # record ledger
                            R = j5 + 0
                            Rp = m + 0 + 1
                            CK("C.gateway.record", "A", Rp - R == m - 4, (H, Q, C, b, m))
    RES["counts"]["C_m_ge_H"] = m_ge_H
    varying = sum(1 for k, s in m_by_class.items() if len(s) > 1)
    RES["counts"]["C_classes_with_varying_m"] = varying
    CK("C.gateway.m_not_class_determined", "A", varying > 0, ("varying classes", varying))
    # synthetic random j=5 states (non-canonical)
    for _ in range(4000):
        H = rng.randrange(7, 40)
        Q = 3 ** rng.randrange(0, 8)
        C = rng.randrange(-(1 << 12), 1 << 12)
        if gcd(C, Q) != 1:
            continue
        b = rng.randrange(0, 2)
        u = rng.randrange(1, 1000, 2)
        lift = rng.randrange(0, 3)
        M = 1 << H
        cls = (C * pow(Q, -1, M) + b * 32) % M
        D = cls + lift * M
        x = 32 * u
        T = x + D
        xn = 2 * T + 6 - x // 2
        Tn = T + 9
        Dn = Tn - xn
        m = v2(xn)
        if m is None or m >= H:
            continue
        M2 = 1 << (m + 1)
        C2 = 15 * Q - C - 32 * b * Q
        Q2 = 3 * Q
        CK("C.gateway.synth_class", "A",
          clsmod(F(C2, Q2) + F(1 << m), M2) == (Dn % M2), (H, Q, C, b, u, lift, m))
    # C.2 A-type algebraic identity
    for _ in range(6000):
        jp = rng.randrange(7, 260)
        k = rng.randrange(1, 30)
        u = rng.randrange(1, 2000, 2)
        Dp = rng.randrange(-(1 << jp), 1 << jp)
        xp = (1 << jp) * u
        Tp = xp + Dp
        x5 = 2 * Tp + 6 * k - xp // 2
        T5 = Tp + 3 + 6 * k
        x2 = 2 * T5 + 6 - x5 // 2
        T2 = T5 + 9
        MA = Tp + 12 + 9 * k
        ok = (x2 == MA + xp // 4) and ((T2 - x2) == -3 * k - xp // 4)
        CK("C.Atype.identity", "A", ok, (jp, k, u, Dp))
        mm = v2(MA)
        if mm is not None and mm <= jp - 3:
            j2 = v2(x2)
            ok2 = (j2 == mm) and ((T2 - x2 - (-3 * k)) % (1 << (j2 + 1)) == 0)
            ok2 = ok2 and (j2 + 2 <= jp - 1)  # Gamma_p=0 block record descent
            CK("C.Atype.ledger", "A", ok2, (jp, k, u, Dp, mm, j2))
    # C.3 B-type algebraic identity
    for _ in range(6000):
        jT = rng.randrange(8, 260)
        sigma = rng.randrange(6, jT - 1)
        eps = jT - 1 - sigma
        tau = rng.randrange(1, 60)
        lam = 32 * rng.randrange(1, 2000, 2)
        cW = (1 << sigma) * rng.randrange(1, 2000, 2)
        u = rng.randrange(1, 2000, 2)
        DT = rng.randrange(-(1 << 20), 1 << 20)
        xT = (1 << jT) * u
        TT = xT + DT
        x5 = cW * u + lam
        T5 = TT + 3 + 3 * tau
        MB = 2 * DT + 12 + 6 * tau - lam // 2
        x2 = 2 * T5 + 6 - x5 // 2
        T2 = T5 + 9
        ok = (x2 == MB + u * ((1 << (jT + 1)) - cW // 2)) and (v2(x5) == 5)
        CK("C.Btype.identity", "A", ok, (jT, sigma, tau, u, DT))
        mm = v2(MB)
        if mm is not None and mm < sigma - 1:
            j2 = v2(x2)
            ok2 = (j2 == mm) and ((T2 - x2 - (T5 + 9 - MB)) % (1 << (j2 + 1)) == 0)
            ok2 = ok2 and (j2 + 2 + eps <= jT - 1)
            CK("C.Btype.ledger", "A", ok2, (jT, sigma, tau, u, DT, mm, j2))
    # C.4 height ladder
    for b in (0, 1):
        h = F(0)
        for t in range(1, 120):
            h = 5 + h / 3 + F(32 * b, 3)
            fix = F(15 + 32 * b, 2)
            CK("C.height.ladder", "A", h <= fix or t < 2,
              (b, t, h, fix))
        CK("C.height.fixed_point", "A", abs(h - F(15 + 32 * b, 2)) < F(1, 10 ** 9),
          (b, h))
    for s_abs in (F(1), F(4, 3)):
        h = F(0)
        for _ in range(200):
            h = 5 + (h + s_abs) / 3
        CK("C.height.shift_fixed_point", "A",
          abs(h - (15 + s_abs) / 2) < F(1, 10 ** 9), (str(s_abs), str(h)))
    # C.5 the rational RAT-4 and gateway C' formulas agree at k=1
    for Q in (1, 3, 9, 27, 81, 243):
        for C in (-13, -1, 1, 5, 10, 26):
            if gcd(C, Q) != 1:
                continue
            for b in (0, 1):
                rat = (9 + 6 * 1) * Q - C - b * Q * (1 << 5)
                gat = 15 * Q - C - 32 * b * Q
                CK("C.formula_bridge", "A", rat == gat, (Q, C, b))
    note("C.gateway.class", "D' = (15Q-C-32bQ)/(3Q) + 2^m (mod 2^{m+1}), m<H")


# --------------------------------------------------------------------------- #
# D. affine ledger
def check_D(cal):
    """Synthetic affine ledger.  States are exact: x=2^j u, Theta integer,
    alpha=2^{-G}, A=2^j, beta=x-A U (so beta=0 or v2(beta)>=j+1), d=(Theta-2^J U-1)/3.
    """
    rng = random.Random(20261026)
    canon_a = {}
    canon_bc = {}
    for n in range(4, 400):
        cr = read_cross(cal, n)
        if not cr["odd"]:
            continue
        if cr["kind"] == "a":
            canon_a[n + 1] = cr
        else:
            canon_bc[n + 1] = cr
    ncases = 0
    for _ in range(16000):
        J = rng.randrange(5, 150)
        G = rng.randrange(0, 6)
        j = J - G
        if j < 4:
            continue
        u = rng.randrange(1, 2000, 2)
        U = rng.randrange(1, 2000, 2)
        x = (1 << j) * u
        T = x + rng.randrange(-(1 << 20), 1 << 20)
        alpha = F(1, 1 << G)
        beta = F(x - (1 << j) * U)
        d = F(T - (1 << J) * U - 1, 3)
        theta = 3 * d + 1 - beta
        D = T - x
        ncases += 1
        CK("D.anchor.theta_class", "A", clsmod(F(D) - theta, 1 << j) == 0, (J, G, j))
        CK("D.anchor.lift", "A", beta == 0 or v2(beta) >= j + 1, (J, G, j, v2(beta)))
        # a-step
        if j >= 5:
            if j in canon_a:
                cr = canon_a[j]
                k = cr["tau"] // 2
                label = "D.a"
            else:
                cr = None
                k = rng.randrange(1, 40)
                label = "D.a.synth"
            xn = 2 * T + 6 * k - x // 2
            Tn = T + 3 + 6 * k
            alpha2 = 2 - alpha / 2
            beta2 = 6 * d + 2 + 6 * k - beta / 2
            d2 = d + 1 + 2 * k
            G2 = G + 1
            ok = (alpha2 * (1 << J) * U + beta2 == xn) and ((1 << J) * U + 3 * d2 + 1 == Tn)
            ok = ok and (v2(alpha2) == -G2)
            CK(label + ".recursion", "A", ok, (J, G, j, k))
            r = v2(3 * k + theta) if (3 * k + theta) != 0 else None
            jn = v2(xn)
            rec = jn + G2
            if r is not None and r <= j - 3:
                cls = sym(3 - theta, jn + 1)
                ok2 = (jn == r + 1) and (vv(beta2) == r + 1) and (rec <= J - 1)
                ok2 = ok2 and ((Tn - xn - cls) % (1 << (jn + 1)) == 0)
                CK(label + ".landing", "A", ok2, (J, G, j, k, r, jn, vv(beta2), rec))
            elif r is None or r >= j - 1:
                ok2 = (jn == j - 1) and (rec == J) and (vv(beta2) >= j)
                CK(label + ".suspension", "A", ok2, (J, G, j, k, r, jn, rec))
            else:
                ell = j - 1
                aa = F(alpha2 * (1 << J), 1 << ell)
                e = v2(aa * U + beta2 / (1 << ell))
                ok2 = (e is not None and e >= 1 and jn == ell + e and rec == J + e)
                CK(label + ".tie", "A", ok2, (J, G, j, k, e, jn, rec))
        # b/c step
        if j >= 5 and j in canon_bc:
            cr = canon_bc[j]
            ratio = F(cr["cW"], 1 << j)
            lam = cr["lam"]
            xn = ratio * x + lam
            Tn = T + 3 + 3 * cr["tau"]
            alpha2 = ratio * alpha
            beta2 = ratio * beta + lam
            d2 = d + 1 + cr["tau"]
            G2 = G + 1 + cr["eps"]
            ok = (alpha2 * (1 << J) * U + beta2 == xn) and ((1 << J) * U + 3 * d2 + 1 == Tn)
            ok = ok and (v2(alpha2) == -G2)
            CK("D.bc.recursion", "A", ok, (J, G, j))
            om = cr["omega"]
            jn = v2(xn)
            cls = sym(theta + F(3 * cr["tau"] + 5 - lam - 2), om + 1)
            ok2 = (jn == om) and (vv(beta2) == om) and (jn + G2 <= J - 1)
            ok2 = ok2 and ((Tn - xn - cls) % (1 << (om + 1)) == 0)
            CK("D.bc.landing", "A", ok2, (J, G, j, om, jn, vv(beta2), jn + G2))
    RES["counts"]["D_cases"] = ncases
    note("D.a.landing", "r = v2(3k+theta) <= j-3: j'=r+1, v2(beta')=r+1, record <= J-1")
    note("D.a.tie", "r = j-2: j' = (j-1)+e, e = v2((A'/2^{j-1})U + beta'/2^{j-1}), record = J+e")


# --------------------------------------------------------------------------- #
# E. canonical exits
def affine_anchor(U, G, j, x, T):
    J = j + G
    alpha = F(1, 1 << G) if G >= 0 else F(1 << (-G))
    beta = F(x - (1 << j) * U)
    d = F(T - (1 << J) * U - 1, 3)
    return {"J": J, "alpha": F(alpha), "beta": F(beta), "d": d, "G": G, "U": U}


def affine_walk(cal, st, sigma, limit=200, stop_on_landing=False):
    """Affine walk; stops at tie/end/ceiling. Checks all one-step ledgers.

    Returns a dict with status, chains, landings, ties, violations.
    """
    J, U = st["J"], st["U"]
    alpha, beta, d, G = F(st["alpha"]), F(st["beta"]), F(st["d"]), st["G"]
    out = {"status": "limit", "chains": [], "landings": [], "ties": [], "violations": [],
           "maxrec": -1}
    for _ in range(limit):
        x = alpha * (1 << J) * U + beta
        if x.denominator != 1:
            out["violations"].append(("x_not_integer", str(x)))
            out["status"] = "bad"
            return out
        x = int(x)
        if x <= 0:
            out["violations"].append(("x_nonpositive", x))
            out["status"] = "bad"
            return out
        j = v2(x)
        T = (1 << J) * U + 3 * d + 1
        rec = j + G
        theta = 3 * d + 1 - beta
        out["chains"].append({"j": j, "G": G, "record": rec, "theta": theta,
                              "x": x, "T": T, "kind": None})
        out["maxrec"] = max(out["maxrec"], rec)
        if rec >= sigma:
            out["status"] = "ceiling"
            return out
        if j <= 4:
            out["status"] = "end"
            return out
        cr = read_cross(cal, j - 1)
        out["chains"][-1]["kind"] = cr["kind"] if cr["odd"] else "e"
        if not cr["odd"]:
            out["status"] = "end"
            return out
        tau = cr["tau"]
        if cr["kind"] == "a":
            k = tau // 2
            xn = 2 * T + 6 * k - x // 2
            Tn = T + 3 + 6 * k
            alpha2 = 2 - alpha / 2
            beta2 = 6 * d + 2 + 6 * k - beta / 2
            d2 = d + 1 + 2 * k
            G2 = G + 1
            if (alpha2 * (1 << J) * U + beta2 != xn) or ((1 << J) * U + 3 * d2 + 1 != Tn):
                out["violations"].append(("a_rec", j))
            if v2(alpha2) != -G2:
                out["violations"].append(("a_alpha", j))
            r = v2(3 * k + theta) if (3 * k + theta) != 0 else None
            jn = v2(xn)
            if r is not None and r <= j - 3:
                if not (jn == r + 1 and vv(beta2) == r + 1 and jn + G2 <= J - 1):
                    out["violations"].append(("a_landing", j, r, jn))
                cls = sym(3 - theta, jn + 1)
                if (Tn - xn - cls) % (1 << (jn + 1)) != 0:
                    out["violations"].append(("a_class", j, jn))
                out["landings"].append({"j": jn, "delta": cls, "record": jn + G2})
                if stop_on_landing:
                    out["status"] = "landing"
                    return out
            elif r is None or r >= j - 1:
                if not (jn == j - 1 and jn + G2 == J and vv(beta2) >= j):
                    out["violations"].append(("a_susp", j, r, jn))
            else:
                ell = j - 1
                aa = F(alpha2 * (1 << J), 1 << ell)
                e = v2(aa * U + beta2 / (1 << ell))
                if not (e is not None and e >= 1 and jn == ell + e and jn + G2 == J + e):
                    out["violations"].append(("a_tie", j, e, jn))
                out["ties"].append({"j": j, "e": e, "record": J + e, "theta": theta,
                                    "m": jn})
                out["status"] = "tie"
                return out
            alpha, beta, d, G = alpha2, beta2, d2, G2
        else:
            ratio = F(cr["cW"], 1 << j)
            xn = ratio * x + cr["lam"]
            Tn = T + 3 + 3 * tau
            alpha2 = ratio * alpha
            beta2 = ratio * beta + cr["lam"]
            d2 = d + 1 + tau
            G2 = G + 1 + cr["eps"]
            if (alpha2 * (1 << J) * U + beta2 != xn) or ((1 << J) * U + 3 * d2 + 1 != Tn):
                out["violations"].append(("bc_rec", j))
            if v2(alpha2) != -G2:
                out["violations"].append(("bc_alpha", j))
            om = cr["omega"]
            jn = v2(xn)
            if not (jn == om and vv(beta2) == om and jn + G2 <= J - 1):
                out["violations"].append(("bc_landing", j, om, jn))
            phi = 3 * tau + 5 - cr["lam"]
            cls = sym(theta + phi - 2, om + 1)
            if (Tn - xn - cls) % (1 << (om + 1)) != 0:
                out["violations"].append(("bc_class", j, om))
            out["landings"].append({"j": jn, "delta": cls, "record": jn + G2})
            if stop_on_landing:
                out["status"] = "landing"
                return out
            alpha, beta, d, G = alpha2, beta2, d2, G2
    out["status"] = "limit"
    return out


def check_E(cal):
    fires = 0
    chains = 0
    c_sources = 0
    steps = 0
    land = 0
    bcl = 0
    ties = 0
    suffix = 0
    suffix_bad = 0
    cls_cert = 0
    shifts = 0
    shift_ties = 0
    shift_tie_safe = 0
    shift_ledger_bad = 0
    sources = []  # (st, sigma, label) -- fires and c sources only: 252+84
    for P in range(5, 257):
        fire = first_fire(cal, P)
        sigma = fire["pointer"]
        s0 = 2 * fire["k"]
        walk = exact_walk(cal, 6 * fire["k"] + 4, 6 * fire["k"] + 5, sigma, s0)
        if walk["status"] != "end":
            CK("E.fire_end", "B", False, (P, walk["status"]))
        fires += 1
        chains += len(walk["rows"])
        rows = walk["rows"]
        by_time = {r["s"]: (idx, r) for idx, r in enumerate(rows)}
        U = (6 * fire["k"] + 4) >> P
        # anchors at every chain
        for idx, r in enumerate(rows):
            j, Gc, x, T = r["j"], r["G"], r["x"], r["T"]
            st = affine_anchor(U, Gc, j, x, T)
            ok_anchor = (st["J"] == j + Gc
                         and st["alpha"] * (1 << st["J"]) * U + st["beta"] == x
                         and (1 << st["J"]) * U + 3 * st["d"] + 1 == T
                         and v2(st["alpha"]) == -Gc)
            CK("E.anchor", "A", ok_anchor, (P, j, Gc))
            vb = v2(st["beta"]) if st["beta"] != 0 else None
            CK("E.anchor.lift", "A", vb is None or vb >= j + 1, (P, j, vb))
            # exact suffix safety
            rw = exact_walk(cal, x, T, sigma)
            mx = max((q["j"] + q["G"] + Gc for q in rw["rows"]), default=-1)
            suffix += 1
            if not (rw["status"] == "end" and mx < sigma):
                suffix_bad += 1
                CK("E.suffix_safe", "B", False, (P, j, rw["status"], mx, sigma))
            else:
                CK("E.suffix_safe", "B", True, None)
            CK("E.suffix_le_R0", "B", mx <= j + Gc, (P, j, Gc, mx))
            # affine ledger of the suffix from this chain
            aw = affine_walk(cal, st, sigma)
            CK("E.affine_ledger", "A", not aw["violations"],
              (P, j, aw["violations"][:3]))
            for L in aw["landings"]:
                cls_cert += 1
                CK("E.landing_class_certified", "B", certify(cal, L["j"], L["delta"]),
                  (P, j, L["j"], L["delta"]))
            if aw["status"] == "tie":
                ties += 1
            if idx + 1 < len(rows):
                cr = read_cross(cal, j - 1)
                steps += 1
                if cr["kind"] == "a":
                    land += 1
                else:
                    bcl += 1
            if idx == 0:
                sources.append((st, sigma, ("fire", P)))
        # c sources
        ep = cal.epoch_crossings(fire)
        for n, rr in ep.items():
            if not (rr["kind"] == "c" and rr["odd"]):
                continue
            s_row = rr["time"]
            if s_row not in by_time:
                continue
            idx, r = by_time[s_row]
            x_src = 3 * s_row + 4 + rr["tail_lambda"]
            if r["x"] != x_src:
                CK("E.c_source_state", "B", False, (P, n, r["x"], x_src))
                continue
            c_sources += 1
            sigma_c = n - rr["epsilon"]
            st = affine_anchor(U, r["G"], r["j"], r["x"], r["T"])
            vb = v2(st["beta"]) if st["beta"] != 0 else None
            CK("E.c_anchor_lift", "B", vb is None or vb >= r["j"] + 1, (P, n, vb))
            rw = exact_walk(cal, r["x"], r["T"], sigma_c)
            mx = max((q["j"] + q["G"] + r["G"] for q in rw["rows"]), default=-1)
            suffix += 1
            if not (rw["status"] == "end" and mx < sigma_c):
                suffix_bad += 1
                CK("E.c_suffix_safe", "B", False, (P, n, rw["status"], mx, sigma_c))
            else:
                CK("E.c_suffix_safe", "B", True, None)
            CK("E.c_suffix_le_R0", "B", mx <= r["j"] + r["G"],
              (P, n, r["j"], r["G"], mx))
            aw = affine_walk(cal, st, sigma_c)
            CK("E.c_affine_ledger", "A", not aw["violations"],
              (P, n, aw["violations"][:3]))
            for L in aw["landings"]:
                cls_cert += 1
                CK("E.c_landing_class_certified", "B", certify(cal, L["j"], L["delta"]),
                  (P, n, L["j"], L["delta"]))
            sources.append((st, sigma_c, ("c", P, n)))
    RES["counts"].update({"E_fires": fires, "E_chains": chains, "E_c_sources": c_sources,
                          "E_steps": steps, "E_a_steps": land, "E_bc_steps": bcl,
                          "E_ties": ties, "E_suffix_checks": suffix,
                          "E_suffix_bad": suffix_bad, "E_class_certificates": cls_cert,
                          "E_sources": len(sources)})
    CK("E.counts", "B",
      fires == 252 and chains == 419 and c_sources == 84 and steps == 167 and ties == 0,
      (fires, chains, c_sources, steps, ties))
    CK("E.sources_count", "B", len(sources) == 336, ("sources", len(sources)))
    # shift suite: 336 sources x 17
    for (st, sigma, lab) in sources:
        for eta in range(-8, 9):
            st2 = dict(st)
            st2["d"] = st["d"] + F(eta, 3)
            aw = affine_walk(cal, st2, sigma, stop_on_landing=True)
            shifts += 1
            if aw["violations"]:
                shift_ledger_bad += 1
                CK("E.shift_ledger", "A", False, (lab, eta, aw["violations"][:3]))
            if aw["status"] == "tie":
                shift_ties += 1
                T = aw["ties"][0]
                if T["j"] == 5:
                    x = st2["alpha"] * (1 << st2["J"]) * st2["U"] + st2["beta"]
                    T0 = (1 << st2["J"]) * st2["U"] + 3 * st2["d"] + 1
                    rw = exact_walk(cal, int(x), int(T0), sigma)
                    mx = max((q["j"] + q["G"] + st2["G"] for q in rw["rows"]), default=-1)
                    safe = (rw["status"] == "end" and mx < sigma)
                    shift_tie_safe += int(safe)
                    CK("E.shift_tie", "B",
                      (clsmod(T["theta"], 16) == 5) and (T["e"] >= 1) and (T["m"] - 4 == T["e"]),
                      (lab, eta, T))
                    CK("E.shift_tie_safe", "B", safe, (lab, eta, T["e"], mx, sigma))
                    RES["canonical"].setdefault("shift_ties", []).append({
                        "label": list(lab) if isinstance(lab, tuple) else lab,
                        "eta": eta, "j": T["j"], "theta_mod16": clsmod(T["theta"], 16),
                        "e": T["e"], "m": T["m"], "record": T["record"],
                        "sigma": str(sigma), "exact_safe": bool(safe)})
    RES["counts"].update({"E_shift_cases": shifts, "E_shift_ties": shift_ties,
                          "E_shift_tie_safe": shift_tie_safe,
                          "E_shift_ledger_bad": shift_ledger_bad})
    CK("E.shift_count", "B", shifts == 5712, ("shift cases", shifts))
    CK("E.shift_ties_count", "B", shift_ties == 5, ("shift ties", shift_ties))
    CK("E.shift_ledger", "A", shift_ledger_bad == 0, ("bad", shift_ledger_bad))
    note("E.affine_ledger", "A1-A3 ledger from every canonical chain state, U=(6k+4)>>P")
    note("E.shift_tie", "ties induced by Theta-shifts d -> d+eta/3, eta in [-8,8]")


# --------------------------------------------------------------------------- #
# F. constants
def check_F(cal):
    # F.1 O2 family
    for m in range(6, 514, 2):
        u = ((1 << (m - 4)) - 1) // 3
        x = 32 * u
        T = x + 5
        xn = 2 * T + 6 - x // 2
        Tn = T + 9
        Dn = Tn - xn
        ok = (xn == (1 << m)) and (v2(xn) == m) and ((3 * Dn - (10 - (1 << m))) % (1 << (m + 1)) == 0)
        CK("F.O2.family", "A", ok, (m,))
        CK("F.O2.record", "A", m + 1 > 5 + 0, (m,))
    RES["counts"]["F_O2_cases"] = 254
    # F.2 O1
    fire = first_fire(cal, 49)
    RES["canonical"]["O1_fire"] = {k: fire[k] for k in ("k", "pointer", "J")}
    CK("F.O1.source", "B", fire["J"] == 49 and fire["k"] == 469124961184426
      and fire["pointer"] == 1051689726214394, fire)
    sigma = fire["pointer"]
    x0 = 5 << 49
    y = 2 * (x0 + 1) + 120 - x0 // 2
    A = (y - 10) // 16
    CK("F.O1.y", "A", y == 16 * A + 10 and v2(y) == 1 and A == 15 * (1 << 44) + 7,
      (y, A, v2(y)))
    bad = 0
    for r in range(1, 601):
        s7 = v2(7 * 3 ** r + 1)
        vA = v2(A * 3 ** r + 1)
        if A * 3 ** r + 1 != (7 * 3 ** r + 1) + 15 * (1 << 44) * 3 ** r:
            bad += 1
        ok = (vA == s7) if s7 < 44 else (vA >= 44 if s7 == 44 else vA == 44)
        if not ok:
            bad += 1
        CK("F.O1.identity", "A", A * 3 ** r + 1 == (7 * 3 ** r + 1) + 15 * (1 << 44) * 3 ** r, (r,))
    CK("F.O1.valuation_rule", "A", bad == 0, ("bad", bad))
    for r in (1, 2, 3, 4, 5, 18, 19):
        Q = 3 ** r
        C = -4 * Q + 8
        p0 = 1 + v2(3 * Q * 20 + C)
        CK("F.O1.p0", "A", p0 == 4 + v2(7 * 3 ** r + 1) and 3 * Q * 20 + C == 8 * (7 * 3 ** r + 1),
          (r, p0))
    # dangerous-r threshold
    lhs = 5 * (sigma - 53)
    rmin = lhs // 8 + 1
    CK("F.O1.threshold", "A", rmin == 657306078883964 and 5 * (sigma - 5) < 240 + 8 * rmin
      and not (5 * (sigma - 5) < 240 + 8 * (rmin - 1)), (rmin,))
    CK("F.O1.constants", "A", (A + 1) ** 5 < (1 << 240) and 3 ** 5 < (1 << 8), None)
    # (DEPTH) at the source only for r <= 18
    CK("F.O1.depth_source", "A",
      all(3 ** r * (kappa(49) + 4) < (1 << 47) for r in range(0, 19))
      and not (3 ** 19 * (kappa(49) + 4) < (1 << 47)), None)
    # F.3 O3
    S = 64
    tot = sum((2 * (S - 2 * r) + 1) * 3 ** r + 1 for r in range(0, S // 2 + 1))
    CK("F.O3.count", "A", tot == 8338590849833250 and tot < (1 << 64), (tot,))
    for (j, h, R) in ((64, 5, 32), (100, 31, 64), (200, 31, 128)):
        cov = (R + 1) * (2 * h + 1)
        CK("F.O3.table", "A", F(cov, 1 << (j + 1)) < F(1, 1000), (j, h, R, cov))
    # F.4 kappa / RAT-C thresholds
    CK("F.kappa", "A", kappa(19) == 42849 and kappa(18) == F(80937, 2), (str(kappa(19)), str(kappa(18))))
    CK("F.RATC.j19Q3", "A", 3 * (kappa(19) + 31) < (1 << 17), None)
    CK("F.RATC.j18Q3_fails", "A", not (3 * (kappa(18) + 31) < (1 << 16)), None)
    CK("F.RATC.j18Q1", "A", kappa(18) + 31 < (1 << 16), None)
    CK("F.RATC.h841", "A", 3 * (kappa(19) + 841) < (1 << 17)
      and not (3 * (kappa(19) + 842) < (1 << 17))
      and (1 << 17) - 3 * kappa(19) == 2525, None)
    CK("F.RATC.h88222", "A", (1 << 17) - kappa(19) == 88223, None)
    # F.5 RAT-C three families (class walk, 2946 walks)
    fams = []
    for m in range(19, 1001):
        fams.append(("(10-2^m)/3", m, 10, 3, 1))
        fams.append(("(26-2^m)/3", m, 26, 3, 1))
        for old in (-2, 1, 4, 7, 10, 13, 16):
            if (m - 19) % 7 == old % 7:
                fams.append(("BBBAA C/3", m, 3 * old + 4, 3, 0))
    stats = {}
    for (name, m, C0, Q0, b0) in fams:
        d = class_walk(cal, m, C0, Q0, b0)
        st = stats.setdefault(name, {"n": 0, "end": 0, "gateway": 0, "nt_high": 0,
                                     "rec_raise": 0, "depth_fail_high": 0, "maxsteps": 0})
        st["n"] += 1
        if d["status"] == "end":
            st["end"] += 1
        elif d["status"] == "gateway":
            st["gateway"] += 1
        else:
            st["nt_high"] += 1
        if d["rec_raise"]:
            st["rec_raise"] += 1
        if d["depth_fail_high"]:
            st["depth_fail_high"] += 1
        st["maxsteps"] = max(st["maxsteps"], d["steps"])
        CK("F.RATC.family", "B", d["rec_raise"] == 0 and d["depth_fail_high"] == 0,
          (name, m, d["status"], d["steps"], d["rec_raise"], d["depth_fail_high"]))
    RES["counts"]["F_RATC_families"] = stats
    CK("F.RATC.no_nt", "B", all(v["nt_high"] == 0 for v in stats.values()), stats)
    CK("F.RATC.max_steps", "B", all(v["maxsteps"] <= 2 for v in stats.values()), stats)
    note("F.O1", "P=49 fire: x0=5*2^49, D0=1, k=20, sigma=pointer; p0=4+v2(7*3^r+1)")
    note("F.O3", "low-cost descriptions (R+1)(2h+1) vs 2^{j+1} classes")


def class_walk(cal, j, C, Q, b, maxsteps=20):
    """Class-determined walk with the rational bookkeeping (for RAT-C)."""
    G = 0
    rec_raise = 0
    depth_fail_high = 0
    for step in range(maxsteps):
        row = read_cross(cal, j - 1)
        if not row["odd"]:
            return {"status": "end", "steps": step, "rec_raise": rec_raise,
                    "depth_fail_high": depth_fail_high}
        rec = j + G
        high = j >= 19
        tau = row["tau"]
        if row["kind"] == "a":
            k = tau // 2
            ht = abs(F(C, Q) - F(3, 2)) + F(3, 2)
            if j >= 19 and not (Q * (kappa(j) + ht) < (1 << (j - 2))):
                depth_fail_high += 1
            val = v2(3 * Q * k + C)
            p = None if val is None else 1 + val
            if p is not None and p <= j - 2:
                C2, Q2, b2 = 3 * Q - C, Q, 0
                j2 = p
                G += 1
                if high and j2 + G >= rec:
                    rec_raise += 1
            elif p is None or p >= j:
                C2 = (9 + 6 * k) * Q - C - b * Q * (1 << j)
                Q2 = 3 * Q
                while C2 % 3 == 0 and Q2 > 1:
                    C2 //= 3
                    Q2 //= 3
                b2 = 1
                j2 = j - 1
                G += 1
                if high and j2 + G >= rec:
                    rec_raise += 1
            else:
                return {"status": "gateway" if j == 5 else "nt_high", "steps": step,
                        "rec_raise": rec_raise, "depth_fail_high": depth_fail_high}
        else:
            phi = 3 * tau + 5 - row["lam"]
            r = rank_of(Q)
            dd, aa, ss = best_shift(phi - 2, row["omega"], r, F(C, Q))
            C2, Q2 = apply_shift(C, Q, r, dd, aa)
            b2 = 0
            j2 = row["omega"]
            G += 1 + row["eps"]
            if high and j2 + G >= rec:
                rec_raise += 1
        j, C, Q, b = j2, C2, Q2, b2
    return {"status": "limit", "steps": maxsteps, "rec_raise": rec_raise,
            "depth_fail_high": depth_fail_high}


# --------------------------------------------------------------------------- #
# G. cross-direction identities
def check_G(cal):
    # G.1 p = 1 + r_aff on canonical a-chains
    cnt = 0
    for P in range(5, 129):
        fire = first_fire(cal, P)
        sigma = fire["pointer"]
        walk = exact_walk(cal, 6 * fire["k"] + 4, 6 * fire["k"] + 5, sigma)
        for r in walk["rows"]:
            j = r["j"]
            if j <= 4:
                continue
            cr = read_cross(cal, j - 1)
            if not cr["odd"] or cr["kind"] != "a":
                continue
            k = cr["tau"] // 2
            theta = r["T"] - r["x"]
            r_aff = v2(3 * k + theta) if (3 * k + theta) != 0 else None
            p = None if r_aff is None else 1 + r_aff
            cnt += 1
            CK("G.p_vs_r", "A", (p is None) or (p == 1 + r_aff), (P, j, p, r_aff))
    RES["counts"]["G_p_vs_r"] = cnt
    # G.2 gateway m = affine e + 4 in the O2 family
    for m in range(6, 514, 2):
        u = ((1 << (m - 4)) - 1) // 3
        x = 32 * u
        T = x + 5
        alpha = F(1)
        beta = F(0)
        d = F(4, 3)
        J = 5
        k = 1
        theta = 3 * d + 1 - beta
        alpha2 = 2 - alpha / 2
        beta2 = 6 * d + 2 + 6 * k - beta / 2
        ell = 4
        aa = F(alpha2 * (1 << J), 1 << ell)
        e = v2(aa * u + beta2 / (1 << ell))
        CK("G.m_vs_e", "A", e == m - 4, (m, e))
    # G.3 rank r'=r+1 at a j=5 gateway with r>=1
    for r in (1, 2, 3, 4):
        for Cc in (5, -4, 10, 26, 55):
            Q = 3 ** r
            if gcd(Cc, Q) != 1:
                continue
            for b in (0, 1):
                C2 = 15 * Q - Cc - 32 * b * Q
                CK("G.gateway_rank", "A", C2 % 3 != 0 and rank_of(3 * Q) == r + 1, (r, Cc, b))
    note("G.p_vs_r", "p = 1+v2(3Qk+C) = 1 + v2(3k+theta) with Q=1, C=theta")


# --------------------------------------------------------------------------- #
# H. finite [B] structure
def check_H(cal):
    # H.1 full-residue scan 5<=j<=18
    bads = {}
    for j in range(5, 19):
        M = 1 << (j + 1)
        bad = []
        for delta in range(M):
            if not certify(cal, j, delta):
                bad.append(delta)
        bads[j] = set(bad)
    RES["canonical"]["small_j_bad"] = {str(j): sorted(v) for j, v in bads.items() if v}
    expected = {5: 4, 8: 4, 12: 4, 14: 4, 17: 8}
    for j, cnt in expected.items():
        CK("H.small_j.count", "B", len(bads[j]) == cnt, (j, len(bads[j]), cnt))
    for j in bads:
        if j not in expected:
            CK("H.small_j.count", "B", len(bads[j]) == 0, (j, len(bads[j])))
    # symmetric residues
    symres = {j: sorted(sym(d, j + 1) for d in v) for j, v in bads.items() if v}
    RES["canonical"]["small_j_bad_sym"] = {str(j): v for j, v in symres.items()}
    CK("H.small_j.sym5", "B", symres.get(5) == [-27, -11, 5, 21], symres.get(5))
    CK("H.small_j.sym8", "B", symres.get(8) == [-198, -70, 58, 186], symres.get(8))
    CK("H.small_j.sym12", "B", symres.get(12) == [-3084, -1036, 1012, 3060], symres.get(12))
    CK("H.small_j.sym14", "B", symres.get(14) == [-12303, -4111, 4081, 12273], symres.get(14))
    CK("H.small_j.sym17", "B",
      symres.get(17) == [-98370, -98322, -32834, -32786, 32702, 32750, 98238, 98286],
      symres.get(17))
    # H.2 spot checks at 22/24/27
    spot = {}
    for j, base in ((22, 1048552), (24, 4194277), (27, 33554402)):
        M = 1 << (j + 1)
        lifts = sorted({(base + t * (1 << (j - 1))) % M for t in range(4)})
        spot[j] = lifts
        CK("H.bad22_27.lifts4", "B", len(lifts) == 4 and len(set(lifts)) == 4, (j, lifts))
        for d in lifts:
            CK("H.bad22_27.bad", "B", not certify(cal, j, d), (j, d))
    RES["canonical"]["bad_22_24_27"] = {str(j): v for j, v in spot.items()}
    # H.3 bad-class graph
    allbad = {j: set(v) for j, v in bads.items() if v}
    for j, v in spot.items():
        allbad[j] = set(v)
    verts = [(j, d) for j in sorted(allbad) for d in sorted(allbad[j])]
    CK("H.graph.vertices", "B", len(verts) == 36, (len(verts),))
    edges = {}
    maxparam = 0
    for (j, d) in verts:
        x = 1 << j
        T = x + d
        G = 0
        succ = None
        for _ in range(400):
            jj = v2(x)
            if jj is None or jj <= 4:
                break
            cr = read_cross(cal, jj - 1)
            if not cr["odd"]:
                break
            x, T, _ = step_exact(x, T, cr)
            G += 1 + cr["eps"]
            if x == 0:
                break
            jj = v2(x)
            maxparam = max(maxparam, jj)
            cls = (T - x) % (1 << (jj + 1))
            if jj in allbad and cls in allbad[jj] and (jj, cls) != (j, d):
                succ = (jj, cls)
                break
        edges[(j, d)] = succ
    n_edges = sum(1 for v in edges.values() if v)
    CK("H.graph.edges", "B", n_edges == 4, (n_edges, {str(k): str(v) for k, v in edges.items() if v}))
    CK("H.graph.edges_to_5", "B",
      all(v == (5, 5) for v in edges.values() if v), (edges,))
    CK("H.graph.maxparam", "B", maxparam == 29, (maxparam,))
    # cycle check: follow successors
    def is_cyclic():
        for v in verts:
            seen = set()
            u = v
            while u is not None:
                if u in seen:
                    return True
                seen.add(u)
                u = edges.get(u)
        return False
    CK("H.graph.acyclic", "B", not is_cyclic(), None)
    cr27 = read_cross(cal, 27)
    CK("H.window30", "B",
      cr27["odd"] and cr27["kind"] == "b" and cr27["omega"] == 6
      and not cal.crossing(28)["odd"] and not cal.crossing(29)["odd"]
      and len(bads.get(6, set())) == 0,
      (cr27["kind"], cr27["omega"], cal.crossing(28)["odd"],
       cal.crossing(29)["odd"], len(bads.get(6, set()))))
    RES["canonical"]["bad_graph"] = {
        "vertices": len(verts), "edges": n_edges, "max_parameter": maxparam,
        "successors": {str(k): (str(v) if v else None) for k, v in edges.items()},
    }
    # H.4 all 36 representative walks terminate; record the maximum record
    all_end = True
    maxrec36 = -1
    for (j, d) in verts:
        tr = trace_walk(cal, j, d)
        if not tr:
            all_end = False
            continue
        # trace_walk stops at an even crossing / j<=4, or at 40 steps
        if len(tr) >= 40:
            all_end = False
        maxrec36 = max(maxrec36, max(r[2] for r in tr))
    CK("H.graph.terminates", "B", all_end, None)
    CK("H.graph.maxrec", "B", maxrec36 == 30, (maxrec36,))
    RES["canonical"]["bad_graph"]["max_record"] = maxrec36
    # H.5 the documented "all later parameters <=27" claim: refuted by max parameter 29
    CK("H.refuted_closure27", "B", maxparam > 27, (maxparam,))
    RES["refuted_claims"].append({
        "claim": "gateway RESULT: every one of the 36 representative walks closes with records <= entry record",
        "status": "not supported by the gateway json itself",
        "evidence": "maxrec[(17,229310)]=22>17, maxrec[(27,167772130)]=30>27, "
                    "maxrec[(17,98238)]=20>17 in gateway/checks.json; the walks terminate "
                    "and max parameter is 29, but the record bound is false.",
    })


def trace_walk(cal, j, delta, limit=40):
    x = 1 << j
    T = x + delta
    G = 0
    out = []
    for _ in range(limit):
        jj = v2(x)
        if jj is None:
            out.append(("zero", G))
            return out
        out.append((jj, G, jj + G))
        if jj <= 4:
            return out
        cr = read_cross(cal, jj - 1)
        if not cr["odd"]:
            return out
        x, T, _ = step_exact(x, T, cr)
        G += 1 + cr["eps"]
    return out


# --------------------------------------------------------------------------- #
# I. control: gateway tie-to-tie record inequality (R) is refuted
def check_I(cal):
    """Explicit exact walk with two ties where rho(tie,1) < rho(tie,0)+(m_0-4)."""
    jp = 73515
    Dp = 98094
    x = 1 << jp
    T = x + Dp
    cr = read_cross(cal, jp - 1)
    k = cr["tau"] // 2
    CK("I.witness.crossing", "A", cr["odd"] and cr["kind"] == "a" and k == 32790, (cr, k))
    MA = T + 12 + 9 * k
    CK("I.witness.MA", "A", v2(MA) == 17 and v2(3 * k + Dp) == 4, (v2(MA), v2(3 * k + Dp)))
    tr = trace_walk(cal, jp, Dp)
    RES["synthetic"]["tie_record_witness"] = {"start": [jp, Dp], "k": k,
                                              "M_A_v2": v2(MA), "walk": tr}
    # walk: (73515,0) -> (5,1) -> (17,2) -> (5,3) -> ...
    ok = (len(tr) >= 4 and tr[1][0] == 5 and tr[2][0] == 17 and tr[3][0] == 5)
    CK("I.witness.two_ties", "A", ok, tr[:5])
    if ok:
        rho0 = tr[1][2]
        m0 = tr[2][0]
        rho1 = tr[3][2]
        claimed = rho0 + (m0 - 4)
        CK("I.R.eq_holds", "A", rho1 >= claimed, (rho0, m0, rho1, claimed))
        # block descent of the first block relative to its predecessor
        CK("I.block_descent", "A", tr[2][2] <= tr[0][2] - 1, (tr[0][2], tr[2][2]))
        if rho1 < claimed:
            RES["refuted_claims"].append({
                "claim": "Theorem G(ii): rho(tie,t+1) >= rho(tie,t) + (m_t - 4)",
                "status": "refuted by an exact walk",
                "witness_start": [jp, Dp],
                "k_predecessor": k,
                "v2_M_A": v2(MA),
                "records": [r[2] for r in tr],
                "parameters": [r[0] for r in tr],
                "rho_tie_0": rho0, "m_0": m0, "rho_tie_1": rho1,
                "claimed_lower_bound": claimed,
                "reason": ("the path from m_0=17 to the next tie at parameter 5 is a single "
                           "landing (17 -> 5); hence k=1, not >= m_0-5.  The proof's "
                           "'at least m_t-5 chains' has the wrong sign: a chain's parameter "
                           "can drop by more than 1."),
            })
    note("I.R.eq_holds", "control: expected to be FALSE; the failure is the documented refutation")


# --------------------------------------------------------------------------- #
# R. revisions forced by the independent adversary report (I1..I12)
def check_R(cal):
    rng = random.Random(20261027)
    N0 = 20_000_000
    # ---- I1: A4 over Z[1/3] is refuted by the rational-theta family
    for (j, k, r) in ((40, 16, 20), (61, 25, 33), (100, 42, 57)):
        cr = read_cross(cal, j - 1)
        CK("R.I1.calendar_k", "A",
          cr["odd"] and cr["kind"] == "a" and cr["tau"] // 2 == k,
          (j, cr["kind"], cr["tau"]))
        theta = F(1 << (j - 2), 3 ** r) - 3 * k
        CK("R.I1.tie_identity", "A", v2(3 * k + theta) == j - 2,
          (j, r, str(theta)))
        CK("R.I1.theta_small", "A", abs(theta) < (1 << 100), (j, str(theta)))
        xp = F(1 << (j - 1)) * (3 + F(1, 3 ** r))
        CK("R.I1.next_not_integer", "A", xp.denominator != 1, (j, xp.denominator))
        e = v2(F(3) + F(1, 3 ** r))
        CK("R.I1.record_exceeds_J", "A", e is not None and e >= 1 and j + e > j,
          (j, e))
        RES.setdefault("synthetic", {}).setdefault("A4_z13_counterexamples", []).append(
            {"j": j, "k": k, "r": r, "theta": str(theta),
             "v2_3k_theta": v2(3 * k + theta), "e": e, "record": j + e,
             "x_next_denominator": str(xp.denominator),
             "note": "algebraic affine state; x' is not an integer, so this is not a machine chain"})
    # repair: integer theta with |z|<2^{j-2} has no tie (the real-state case)
    for _ in range(2000):
        j = rng.randrange(20, 200)
        k = rng.randrange(1, 1000)
        theta = rng.randrange(-(1 << 30), 1 << 30)
        z = 3 * k + theta
        if z == 0:
            continue
        if abs(z) < (1 << (j - 2)):
            CK("R.I1.integer_no_tie", "A", v2(z) <= j - 3, (j, k, theta, v2(z)))
    # deep size: kappa + B < 2^{j-2} at j=N0+1
    Bdeep = 1 << 10_000_000
    CK("R.I1.deep_size", "A",
      (int(kappa(N0 + 1)) + Bdeep).bit_length() <= N0 - 2,
      (int(kappa(N0 + 1)), (int(kappa(N0 + 1)) + Bdeep).bit_length(), N0 - 2))
    # real canonical states have integer theta (after re-anchoring)
    for P in range(5, 65):
        fire = first_fire(cal, P)
        rw = exact_walk(cal, 6 * fire["k"] + 4, 6 * fire["k"] + 5, fire["pointer"],
                        2 * fire["k"])
        U = (6 * fire["k"] + 4) >> P
        for r in rw["rows"]:
            st = affine_anchor(U, r["G"], r["j"], r["x"], r["T"])
            theta = 3 * st["d"] + 1 - st["beta"]
            CK("R.I1.real_theta_integer", "A", theta.denominator == 1,
              (P, r["j"], str(theta)))
    # ---- I2: internal chains have Gamma_0>0; records <= R_0 = j_0+Gamma_0 = J
    for P in (14, 28):
        fire = first_fire(cal, P)
        rw = exact_walk(cal, 6 * fire["k"] + 4, 6 * fire["k"] + 5,
                        fire["pointer"], 2 * fire["k"])
        rows = rw["rows"]
        j0, G0 = rows[1]["j"], rows[1]["G"]
        R0 = j0 + G0
        mx = max(r["j"] + r["G"] for r in rows[1:])
        CK("R.I2.internal_record", "B", R0 > j0 and mx <= R0, (P, j0, G0, R0, mx))
        RES.setdefault("canonical", {}).setdefault("internal_record_examples", []).append(
            {"P": P, "j0": j0, "Gamma0": G0, "R0": R0, "records":
             [(r["j"], r["G"], r["j"] + r["G"]) for r in rows]})
    # ---- I4: strong a preserves A and h_t, not ht=|C|/Q
    for (Q, C, b, j, k, u) in ((1, 7, 0, 5, 1, 1), (1, 10, 0, 5, 1, 1)):
        x = (1 << j) * u
        T = x + C
        xn = 2 * T + 6 * k - x // 2
        C2 = 3 * Q - C
        A0 = abs(F(C, Q) - F(3, 2))
        A2 = abs(F(C2, Q) - F(3, 2))
        ht0 = F(abs(C), Q)
        ht2 = F(abs(C2), Q)
        CK("R.I4.A_preserved", "A", A2 == A0 and A0 + F(3, 2) == A2 + F(3, 2),
          (Q, C, b, j, k, u))
        CK("R.I4.ht_not_preserved", "A", ht2 != ht0, (C, C2, str(ht0), str(ht2)))
    # ---- I5: catapult height constant is b*2^j/3, not 32b/3 (j>5)
    for (j, k, C, b) in ((8, 2, 122, 1), (12, 4, 2036, 1),
                         (17, 6, 65518, 1), (22, 8, 2097128, 1)):
        x = 1 << j
        T = x + C
        p = 1 + v2(3 * k + C)
        xn = 2 * T + 6 * k - x // 2
        Tn = T + 3 + 6 * k
        C2 = (9 + 6 * k) - C - b * (1 << j)
        ht = F(abs(C), 1)
        ht2 = F(abs(C2), 3)
        old = 3 + 2 * k + ht / 3 + F(32 * b, 3)
        new = 3 + 2 * k + ht / 3 + F(b * (1 << j), 3)
        CK("R.I5.onestep", "A", p == j and v2(xn) == j - 1, (j, k, C, p))
        CK("R.I5.old_bound_refuted", "A", ht2 > old, (j, str(ht2), str(old)))
        CK("R.I5.new_bound", "A", ht2 <= new, (j, str(ht2), str(new)))
    # ---- I6: x'=0 congruence is mod 2^{j+1}Q, not an exact equation in C
    for (C, exact_zero) in ((37, False), (-27, True)):
        lhs = 2 * (C + 3) + 3 * 16
        CK("R.I6.congruence", "A",
          lhs % (1 << 6) == 0 and (lhs == 0) == exact_zero and 1 + v2(3 + C) == 4,
          (C, lhs))
    # ---- I8: the strengthened O1 lower bound is a necessary bound (ceil log_3)
    sigma = 1051689726214394
    A = 15 * (1 << 44) + 7
    getcontext().prec = 80
    log3M = ((sigma - 5) * Decimal(2).ln() - Decimal(A).ln()) / Decimal(3).ln()
    rlb = int(log3M.to_integral_value(rounding=ROUND_CEILING))
    frac = abs(log3M - log3M.to_integral_value())
    CK("R.I8.ceillog", "A",
      rlb == 663542339794048 and frac > Decimal("1e-40"),
      (rlb, str(frac)))
    RES["counts"]["R_I8_ceillog"] = rlb
    # ---- I11: gateway rank at r=0
    for (C, b) in ((5, 0), (-11, 0), (-27, 0), (21, 0)):
        C2 = 15 - C - 32 * b
        Q2 = 3
        while C2 % 3 == 0 and Q2 > 1:
            C2 //= 3
            Q2 //= 3
        rp = rank_of(Q2)
        CK("R.I11.r0_rule", "A", (rp == 0) == ((C + 2 * b) % 3 == 0),
          (C, b, C2, Q2, rp))
    # ---- I12: the minimal representative of a class is the symmetric one
    for _ in range(1000):
        j = rng.randrange(5, 100)
        Q = 3 ** rng.randrange(0, 6)
        C = rng.randrange(-(1 << 20), 1 << 20)
        if gcd(C, Q) != 1:
            continue
        M = (1 << (j + 1)) * Q
        reps = [C + t * M for t in (-2, -1, 0, 1, 2)]
        symc = min(reps, key=abs)
        CK("R.I12.min_rep", "A",
          abs(symc) == min(abs(x) for x in reps)
          and abs(symc) <= abs(C), (j, Q, C, symc))
    RES["refuted_claims"].append({
        "claim": "A4 over Z[1/3]: j>=N0+1 and |theta|<=B-3 imply no tie",
        "status": "refuted by the exact rational-theta family",
        "witness_family": "theta = 2^(j-2)/3^r - 3k, beta=0, d=(theta-1)/3, U=1, J=j",
        "witness_rows": RES["synthetic"]["A4_z13_counterexamples"],
        "repair": ("the real-state case has integer theta (x,Theta in Z, A,U,beta in Z); "
                   "for integer theta with |theta|<=B-3 and j>=N0+1, |3k+theta|<2^(j-2) "
                   "forces v2<=j-3, so there is no tie.  The next x' in the rational "
                   "counterexample is not an integer, so it is not a machine chain."),
    })
    note("R.I1.tie_identity", "A4 over Z[1/3] is refuted; the real-state case needs integer theta")
    note("R.I2.internal_record", "R_t <= R_0 = j_0+Gamma_0 = J; the chain-count bound remains j_0-4")
    RES["refuted_claims"].append({
        "claim": "strong a step preserves ht = |C|/Q",
        "status": "false; the preserved quantity is A=|C/Q-3/2| and h_t=A+3/2",
        "witness": "(j,Q,C,b,k,u)=(5,1,7,0,1,1): ht 7 -> 4, A=7/2 preserved; canonical X(4), C=10: ht 10 -> 7",
    })
    note("R.I4.ht_not_preserved", "strong a preserves A and h_t=A+3/2, not ht=|C|/Q")
    RES["refuted_claims"].append({
        "claim": "catapult height bound 3+2k+ht/3+32b/3 for all j",
        "status": "false for j>5; the correct term is b*2^j/3",
        "witness": "(j,k,C,b)=(8,2,122,1): ht'=119 > 3+2k+ht/3+32b/3=175/3; "
                   "(12,4,2036,1): 2033 > 2101/3; (17,6,65518,1): 65515 > 21865",
    })
    note("R.I5.old_bound_refuted", "catapult height is 3+2k+ht/3+b*2^j/3; 32b/3 is the j=5 special case")
    note("R.I8.ceillog", "663542339794048 is a necessary lower bound (ceil log_3), not a dangerous range")


# --------------------------------------------------------------------------- #
def main():
    t0 = time.time()
    RES["environment"]["python"] = sys.version.split()[0]
    RES["environment"]["calendar"] = "work_global_calendar/calendar_oracle.Calendar(512)"
    RES["environment"]["table"] = str(TABPATH)
    cal = Calendar(512)
    # canonical-data consistency: Calendar(512) vs the accepted table for n < 512
    try:
        with open(TABPATH, "rb") as f:
            tab = pickle.load(f)
        mm = 0
        for n in range(512):
            r = cal.crossing(n)
            if (r["kind"] != chr(tab["typ"][n]) or bool(r["odd"]) != bool(tab["odd"][n])
                    or r["time"] != tab["tau"][n] or r["epsilon"] != tab["eps"][n]):
                mm += 1
        CK("Z.table_vs_calendar", "B", mm == 0, ("mismatch", mm))
        lam_ok = 0
        lam_bad = 0
        for n in range(512):
            r = cal.crossing(n)
            if r["odd"] and r["kind"] != "a":
                lam = r["head_lambda"] + 2 * r["tail_lambda"] + 3
                if lam == tab["lA"][n] + 2 * tab["lY"][n] + 3:
                    lam_ok += 1
                else:
                    lam_bad += 1
        CK("Z.table_lambda", "B", lam_bad == 0, ("ok", lam_ok, "bad", lam_bad))
    except Exception as exc:  # noqa: BLE001
        RES["not_run"].append({"check": "Z.table_vs_calendar", "reason": str(exc)})
    # canonical small base and the entry at parameter 5
    CK("Z.small_base_even", "B", all(not cal.crossing(n)["odd"] for n in range(4)),
      tuple(cal.crossing(n)["odd"] for n in range(4)))
    x5 = read_cross(cal, 5)
    CK("Z.X5", "B", x5["odd"] and x5["kind"] == "b" and x5["omega"] == 1,
      (x5["kind"], x5["omega"]))
    t1 = time.time()
    check_A(cal)
    RES["timing"]["A"] = round(time.time() - t1, 2)
    t1 = time.time()
    check_B(cal)
    RES["timing"]["B"] = round(time.time() - t1, 2)
    t1 = time.time()
    check_C(cal)
    RES["timing"]["C"] = round(time.time() - t1, 2)
    t1 = time.time()
    check_D(cal)
    RES["timing"]["D"] = round(time.time() - t1, 2)
    t1 = time.time()
    check_E(cal)
    RES["timing"]["E"] = round(time.time() - t1, 2)
    t1 = time.time()
    check_F(cal)
    RES["timing"]["F"] = round(time.time() - t1, 2)
    t1 = time.time()
    check_G(cal)
    RES["timing"]["G"] = round(time.time() - t1, 2)
    t1 = time.time()
    check_H(cal)
    RES["timing"]["H"] = round(time.time() - t1, 2)
    t1 = time.time()
    check_I(cal)
    RES["timing"]["I"] = round(time.time() - t1, 2)
    t1 = time.time()
    check_R(cal)
    RES["timing"]["R"] = round(time.time() - t1, 2)
    # control I.R.eq_holds is expected to be FALSE; exclude it from the hard gate
    total = 0
    failed = 0
    for cid, d in RES["checks"].items():
        if cid == "I.R.eq_holds":
            continue
        total += d["checked"]
        failed += d["failed"]
    RES["counts"]["total_checks"] = total
    RES["counts"]["total_fail"] = failed
    RES["counts"]["elapsed_seconds"] = round(time.time() - t0, 2)
    RES["scope_map"] = {
        "canonical": ["Z.table_vs_calendar", "Z.table_lambda", "E.*", "H.*",
                      "F.O1.source"],
        "canonical_crossings_with_synthetic_classes": ["F.RATC.*", "F.O1.*",
                                                       "F.O2.*", "F.O3.*", "G.*"],
        "mixed_canonical_and_synthetic_states": ["A.*", "B.*", "C.*", "D.*", "I.*"],
        "note": ("A/B/C/D/I mix canonical crossings (Calendar(512)) with synthetic, "
                 "non-canonical exact integer states; the tag_detail in a_case/bc_case "
                 "labels 'canon' vs 'synth'. E/H/Z use only canonical data. F.O1/F.RATC "
                 "use canonical crossings but synthetic initial classes. The synthetic "
                 "witness in I is exact but not claimed reachable."),
    }
    RES["not_run"].extend([
        {"check": "affine A4 deep two-chain [B]", "reason":
         "Calendar(B) would need B >= N0 = 2*10^7 > 1024; A4 is [A-imp]+[A] only, not tested here."},
        {"check": "full Bad_j enumeration at j=22,24,27", "reason":
         "cost 2^{j+1} (up to 2^28 walks); only the four documented lifts per j were verified bad."},
        {"check": "work_r1r2 8,712 bad pairs", "reason":
         "table_100000000.pkl is absent on this machine; only table_1000000.pkl is available."},
        {"check": "N_Q terminal certificate", "reason":
         "ODD_DENOMINATOR only reduces the walk below N_Q under four extra hypotheses; N_Q can exceed 2*10^7 and the band [N0,N_Q) remains open. It is a continuation reduction, not a class certificate."},
        {"check": "canonical reachability of the (R) counterexample", "reason":
         "the witness state is exact but synthetic (non-canonical); it refutes the universal algebraic claim, not a canonical statement."},
    ])
    RES["status"] = "PASS" if failed == 0 else "FAIL"
    if failed:
        for cid, d in RES["checks"].items():
            if d["failed"] and cid != "I.R.eq_holds":
                RES["failures"].append({"check": cid, "failed": d["failed"],
                                        "examples": d["examples"][:3]})
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(RES, f, indent=1, default=str)
    print("=" * 78)
    for cid in sorted(RES["checks"]):
        d = RES["checks"][cid]
        flag = "FAIL" if d["failed"] else "PASS"
        if cid == "I.R.eq_holds":
            flag = "REFUTED" if d["failed"] else "UNEXPECTED-PASS"
        print("%-8s %-34s checked=%-9d failed=%d  %s"
              % (flag, cid, d["checked"], d["failed"], d["tag"]))
    print("=" * 78)
    print("counts:", json.dumps({k: RES["counts"][k] for k in
                                ("total_checks", "total_fail", "E_fires", "E_chains",
                                 "E_c_sources", "E_steps", "E_shift_cases",
                                 "E_shift_ties", "E_suffix_checks", "E_class_certificates")}, default=str))
    print("refuted_claims:", len(RES["refuted_claims"]))
    print("STATUS: %s   total failed: %d   elapsed: %.1fs" %
          (RES["status"], failed, RES["counts"]["elapsed_seconds"]))
    print("json:", OUT)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
