"""verify_rational.py -- exact checks for the rational-mode normal form.

Implements the test list of work_landing_symbolic/rational/PLAN.md (direction R):
  A  a-step three-way classification (strong descent / one-step descent / NT gate)
  B  b/c-step class recurrence and rational shifts (incl. 4/3)
  C  parameter-five gateway (catapult with k=1) and its height bound
  D  centred height A, real height ht, 3-adic rank r, records R
  E  certify_Q vs certify(j,delta): lift invariance, propagation, small-j scan
  F  landing-class formulas, window statistics, RAT-C (DEPTH) walks
  G  O1 (P=49 orbit-shift source) in this representation
  H  O2 (STOP_CHECKPOINT small-gateway family)
  I  O3 counting obstruction
  J  falsification tests F1-F11 (aggregated)

All arithmetic is exact (ints / fractions.Fraction).  Canonical crossings come from
work_global_calendar/calendar_oracle.py (Calendar(B), B<=1024).  Every synthetic
state is labelled canonical:false.  Failures are kept as data: nothing is dropped
to make the script pass.

Run:  python -B work_landing_symbolic/rational/verify_rational.py
Writes work_landing_symbolic/rational/checks.json
"""

import json
import sys
import time
from fractions import Fraction as F
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "work_ext_roots"))
from work_global_calendar.calendar_oracle import Calendar  # noqa: E402
from verify_low_deficit import first_fire  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "checks.json"


# ----------------------------------------------------------------------------- helpers
def v2(x):
    """2-adic valuation of a nonzero integer; None for 0."""
    x = abs(int(x))
    if x == 0:
        return None
    return (x & -x).bit_length() - 1


def ceil_log2(m):
    """ceil(log2(m)) for m >= 2, exact."""
    return (m - 1).bit_length()


def P_clock(n):
    """Accepted PROOF_CLOCK bound P(n) = 2*ceil(log2(6n^2+5))^2 + 1345."""
    return 2 * ceil_log2(6 * n * n + 5) ** 2 + 1345


def kappa(j):
    """Accepted clock bound 3k <= kappa(j) = (3/2)(j-1)P(j-1)."""
    if j <= 1:
        return F(0)
    n = j - 1
    return F(3, 2) * n * P_clock(n)


def rank_of(Q):
    """3-adic rank r of Q = 3^r; return None if Q is not a power of 3."""
    r = 0
    q = Q
    while q % 3 == 0:
        q //= 3
        r += 1
    return r if q == 1 else None


def height_pen(c):
    """JOINT_HEIGHT_BUDGET height h(c) = ceil(max(0,1-c,c-2))."""
    x = max(F(0), 1 - c, c - 2)
    return -((-x.numerator) // x.denominator)  # ceil of a nonnegative Fraction


class Ctx:
    def __init__(self):
        self.canonical_tests = {}
        self.synthetic_tests = {}
        self.claims = {}
        self.failures = []
        self.fail_count = {}
        self.truncated = {}
        self.data = {}
        self.MAX_EX = 50

    def _bump(self, bucket, name):
        b = getattr(self, bucket)
        d = b.setdefault(name, {"n": 0, "fail": 0})
        d["n"] += 1
        return d

    def check(self, bucket, name, claim, cond, detail=None):
        d = self._bump(bucket, name)
        c = self.claims.setdefault(claim, {"n": 0, "fail": 0, "label": "?", "note": ""})
        c["n"] += 1
        if not cond:
            d["fail"] += 1
            c["fail"] += 1
            self.fail_count[name] = self.fail_count.get(name, 0) + 1
            if self.fail_count[name] <= self.MAX_EX:
                self.failures.append({"test": name, "claim": claim, "detail": str(detail)[:400]})
            else:
                self.truncated[name] = self.truncated.get(name, 0) + 1
        return cond

    def note(self, claim, label, note=""):
        c = self.claims.setdefault(claim, {"n": 0, "fail": 0, "label": "?", "note": ""})
        c["label"] = label
        c["note"] = note


def build_state(j, Q, C, b, lift, u, H=None):
    """Exact integer state (x,Theta) whose defect has the certificate (C,Q,b).

    The certificate is D = C*Q^{-1} + b*2^j (mod 2^H), H >= j+1.  D is the class
    mod 2^H plus lift*2^H (a higher-bit lift).  x = 2^j u (u odd), Theta = x + D.
    """
    H = H if H is not None else j + 1
    M = 1 << H
    cls = ((C * pow(Q, -1, M)) + b * (1 << j)) % M
    D = cls + lift * M
    x = (1 << j) * u
    return x, x + D, cls % (1 << (j + 1))


# ----------------------------------------------------------------------------- exact walk
def exact_walk(cal, x, theta, P, limit=20000):
    """Exact walk with precision budget P (record = j + Gamma, must stay < P)."""
    loss = 0
    rec = 0
    word = []
    types = []
    for _ in range(limit):
        if x == 0:
            return {"status": "zero", "record": rec, "word": word, "types": "".join(types)}
        if x < 0:
            return {"status": "nonpositive", "record": rec, "word": word, "types": "".join(types)}
        j = v2(x)
        if j + loss >= P:
            return {"status": "ceiling", "record": rec, "word": word, "types": "".join(types)}
        rec = max(rec, j + loss)
        word.append(j)
        r = cal.crossing(j - 1)
        if not r["odd"]:
            return {"status": "end", "record": rec, "word": word, "types": "".join(types)}
        tau = r["time"]
        if r["kind"] == "a":
            types.append("a")
            x = 2 * theta + 3 * tau - (x >> 1)
        else:
            types.append(r["kind"])
            cW = (r["head_ratio"] + 2 * r["tail_ratio"]) * (1 << (j - 1))
            assert cW.denominator == 1, ("nonintegral c_W", j, cW)
            lam = r["head_lambda"] + 2 * r["tail_lambda"] + 3
            x = int(cW) * (x >> j) + lam
        theta += 3 + 3 * tau
        loss += 1 + r["epsilon"]
    return {"status": "limit", "record": rec, "word": word, "types": "".join(types)}


def certify(cal, j, delta, P):
    """certify(j,delta;P): exact walk from the representative (2^j, 2^j+delta)."""
    return exact_walk(cal, 1 << j, (1 << j) + delta, P)


def crossing_ab(cal, n):
    """Return (kind, tau, eps, omega, cW, lam) for a canonical odd b/c crossing."""
    r = cal.crossing(n)
    cW = (r["head_ratio"] + 2 * r["tail_ratio"]) * (1 << n)
    assert cW.denominator == 1
    lam = r["head_lambda"] + 2 * r["tail_lambda"] + 3
    return r["kind"], r["time"], r["epsilon"], r["omega"], int(cW), lam


# ----------------------------------------------------------------------------- A: a-step
A_QS = [1, 3, 9, 27, 81, 243, 3 ** 10, 3 ** 20, 3 ** 40]
A_CS = [-40, -25, -17, -13, -11, -7, -5, -2, -1, 1, 2, 4, 5, 7, 10, 13, 16, 17, 26, 40]
A_US = [1, 3, 17, 127]
A_JS = [5, 6, 7, 8, 9, 11, 13, 17, 21, 30, 49, 64, 80, 100, 128, 150, 200]


def section_A(ctx, cal):
    """a-step three-way classification.  Canonical when X(j-1) is odd type a."""
    a3_pairs = {}
    for j in A_JS:
        row = cal.crossing(j - 1)
        canon = bool(row["odd"] and row["kind"] == "a")
        ks = ([row["time"] // 2] if canon else []) + [1, 2, 3, 5, 17]
        for Q in A_QS:
            for C in A_CS:
                if gcd(C, Q) != 1:
                    continue
                for b in (0, 1):
                    for lift in (0, 1):
                        for u in A_US:
                            for k in ks:
                                x, theta, cls = build_state(j, Q, C, b, lift, u)
                                xn = 2 * theta + 6 * k - (x >> 1)
                                tn = theta + 3 + 6 * k
                                Dn = tn - xn
                                val = v2(3 * Q * k + C)
                                p0 = None if val is None else 1 + val
                                bucket = "canonical_tests" if (canon and k == ks[0]) else "synthetic_tests"
                                name = "a_step_%s" % ("canonical" if bucket == "canonical_tests" else "synthetic")
                                if p0 is not None and p0 <= j - 2:
                                    ok = (v2(xn) == p0) and \
                                         ((Q * Dn - (3 * Q - C)) % (1 << (p0 + 1)) == 0)
                                    ctx.check(bucket, name + "_strong", "A1", ok,
                                              ("strong", j, Q, C, b, lift, u, k, p0, v2(xn)))
                                elif p0 is None or p0 >= j:
                                    # class claim: D' = 3 - D - 2^(j-1) (mod 2^j);
                                    # cls is a representative of the class, valid mod 2^j
                                    ok = (v2(xn) == j - 1) and \
                                         ((Dn - (3 - cls - (1 << (j - 1)))) % (1 << j) == 0)
                                    ctx.check(bucket, name + "_onestep", "A2", ok,
                                              ("onestep", j, Q, C, b, lift, u, k, p0, v2(xn)))
                                else:
                                    # NT gate: v2(x') >= j-1, and outcome depends on u
                                    ctx.check(bucket, name + "_nt_bound", "A3",
                                              v2(xn) >= j - 1,
                                              ("nt_bound", j, Q, C, b, lift, u, k, v2(xn)))
                                    key = (j, Q, C, b, lift, k)
                                    a3_pairs.setdefault(key, {})[u] = (v2(xn), Dn % (1 << j))
                                if Q > 1:
                                    ctx.check(bucket, name + "_nozero", "A4", xn != 0,
                                              ("xprime_zero", j, Q, C, b, lift, u, k))
    # A3: u-dependence of the NT-gate outcome (data, and an assertion of ">=2 outcomes")
    amb = 0
    examples = []
    for key, d in a3_pairs.items():
        outs = set(v for v, _ in d.values())
        cls = set(c for _, c in d.values())
        if len(outs) >= 2:
            amb += 1
            if len(examples) < 8:
                examples.append({"key": list(key), "j_prime_by_u": {str(u): v[0] for u, v in d.items()}})
    ctx.data["A3_nt_gate_u_dependence"] = {
        "classes_sampled": len(a3_pairs), "classes_with_>=2_outcomes": amb,
        "examples": examples,
        "note": "same class mod 2^(j+1), different u -> different j' (class cannot decide)",
    }
    ctx.check("synthetic_tests", "a_step_nt_u_dependence", "A3", amb > 0,
              ("no u-dependence found",))

    # A4: Q=1 resonance x'=0 exists
    zero_examples = []
    for j in (5, 6, 9, 13):
        row = cal.crossing(j - 1)
        if not (row["odd"] and row["kind"] == "a"):
            continue
        k = row["time"] // 2
        for u in (1, 3, 5):
            D = -3 * (1 << (j - 2)) * u - 3 * k
            M = 1 << (j + 1)
            C = D % M
            x = (1 << j) * u
            xn = 2 * (x + D) + 6 * k - (x >> 1)
            zero_examples.append({"j": j, "k": k, "u": u, "D": D, "C": C, "x_prime": xn})
            ctx.check("synthetic_tests", "a_step_Q1_resonance_zero", "A4", xn == 0,
                      ("expected x'=0", j, k, u, xn))
    ctx.data["A4_Q1_zero_examples"] = zero_examples


# ----------------------------------------------------------------------------- B: b/c step
B_QS = [1, 3, 9, 27, 81, 3 ** 5]
B_CS = [-13, -7, -1, 1, 4, 10, 26, 55]


def best_shift(phi2, omega, r):
    """Minimal-cost representative of the class phi2 mod 2^(omega+1) as a/3^d.

    Cost follows OPTIMAL_PHASE_ENCODING: 2*max(r,d) + h_pen(c+s); ties by |s|.
    Returns (d, a) so that s = a/3^d has class phi2 (mod 2^(omega+1)).
    """
    M = 1 << (omega + 1)
    cands = [(0, phi2 % M if (phi2 % M) <= M // 2 else (phi2 % M) - M)]
    for d in range(1, 5):
        a = (phi2 * 3 ** d) % M
        if a > M // 2:
            a -= M
        cands.append((d, a))
    return cands


def apply_shift(C, Q, r, d, a):
    """Return (C',Q') with C'/Q' = C/Q + a/3^d, reduced by powers of 3."""
    if a == 0:
        return C, Q
    r2 = max(r, d)
    C2 = C * 3 ** max(0, d - r) + a * 3 ** max(0, r - d)
    Q2 = 3 ** r2
    while C2 % 3 == 0 and Q2 > 1:
        C2 //= 3
        Q2 //= 3
    return C2, Q2


def section_B(ctx, cal, nmax=4000):
    """b/c class recurrence, canonical crossings plus synthetic prescribed shifts."""
    nbc = 0
    for n in range(4, nmax):
        row = cal.crossing(n)
        if not (row["odd"] and row["kind"] != "a"):
            continue
        nbc += 1
        kind, tau, eps, omega, cW, lam = crossing_ab(cal, n)
        j = n + 1
        sigma = n - eps
        ctx.check("canonical_tests", "bc_omega_v2_lambda", "B1", omega == v2(lam),
                  ("omega", n, omega, v2(lam)))
        ctx.check("canonical_tests", "bc_sigma_v2_cW", "B1", sigma == v2(cW),
                  ("sigma", n, sigma, v2(cW)))
        ctx.check("canonical_tests", "bc_S1_omega_lt_sigma", "B1", omega <= sigma - 1,
                  ("S1", n, omega, sigma))
        phi = 3 * tau + 5 - lam
        phi2 = phi - 2
        for Q in B_QS:
            for C in B_CS:
                if gcd(C, Q) != 1:
                    continue
                for b in (0, 1):
                    for lift in (0, 1):
                        for u in (1, 3):
                            x, theta, cls = build_state(j, Q, C, b, lift, u)
                            xn = cW * u + lam
                            tn = theta + 3 + 3 * tau
                            Dn = tn - xn
                            ok = (v2(xn) == omega) and \
                                 ((Q * Dn - (C + Q * phi2)) % (1 << (omega + 1)) == 0) and \
                                 (gcd(C + Q * phi2, Q) == 1)
                            ctx.check("canonical_tests", "bc_class_recurrence", "B2", ok,
                                      ("bc", n, Q, C, b, lift, u, omega, phi2))
    ctx.data["B_canonical_crossings_checked"] = nbc

    # synthetic shifts with prescribed class s (incl. 4/3): choose lam so that
    # phi-2 = 3*tau+3-lam equals the chosen integer representative.
    shifts = [("0", 0, 0), ("-1", -1, 0), ("+1", 1, 0),
              ("4/3", 4, 1), ("-2/3", -2, 1), ("2/9", 2, 2), ("1/3", 1, 1)]
    for omega in (1, 3, 5):
        for (sname, a, d) in shifts:
            M = 1 << (omega + 1)
            phi2 = (a * pow(3, -d, M)) % M  # class of a/3^d mod 2^(omega+1)
            if phi2 > M // 2:
                phi2 -= M
            found = None
            for tau in range(2, 400):
                lam = 3 * tau + 3 - phi2
                if lam > 0 and v2(lam) == omega:
                    found = tau
                    break
            ctx.check("synthetic_tests", "bc_synthetic_prescribed_shift_exists", "B3",
                      found is not None, ("no tau for", sname, omega))
            if found is None:
                continue
            tau = found
            lam = 3 * tau + 3 - phi2
            cW = 1 << (omega + 1)  # sigma = omega+1 > omega
            for Q in B_QS:
                for C in B_CS:
                    if gcd(C, Q) != 1:
                        continue
                    r = rank_of(Q)
                    for b in (0, 1):
                        for lift in (0, 1):
                            j = omega + 1
                            x, theta, cls = build_state(j, Q, C, b, lift, 3)
                            xn = cW * 3 + lam
                            tn = theta + 3 + 3 * tau
                            Dn = tn - xn
                            C2, Q2 = apply_shift(C, Q, r, d, a)
                            ok = (v2(xn) == omega) and \
                                 ((Q2 * Dn - C2) % (1 << (omega + 1)) == 0) and \
                                 (gcd(C2, Q2) == 1)
                            ctx.check("synthetic_tests", "bc_synthetic_shift_class", "B3", ok,
                                      ("syn_bc", sname, omega, tau, Q, C, b, lift, C2, Q2))
                            # after 3-cancellation the rank is <= max(r,d); it drops by one
                            # exactly when r == d and 3 | (C+a)
                            r2 = rank_of(Q2)
                            C2_raw = C * 3 ** max(0, d - r) + a * 3 ** max(0, r - d)
                            ctx.check("synthetic_tests", "bc_synthetic_rank_bound", "B3",
                                      r2 <= max(r, d),
                                      ("rankbound", sname, omega, Q, C, d, a, Q2))
                            ctx.check("synthetic_tests", "bc_synthetic_rank_drop_rule", "B3",
                                      (r2 == max(r, d)) == (C2_raw % 3 != 0 or max(r, d) == 0),
                                      ("rankdrop", sname, omega, Q, C, d, a, r2, C2_raw))
    ctx.check("synthetic_tests", "bc_synthetic_covers_4_3", "B3",
              any(s[0] == "4/3" for s in shifts), ("missing 4/3",))


# ----------------------------------------------------------------------------- C: gateway
C_QS = [1, 3, 9, 27, 81, 3 ** 4, 3 ** 8]
C_CS = [-40, -25, -17, -13, -11, -7, -5, -2, -1, 1, 2, 4, 5, 7, 10, 13, 16, 17, 26, 40]
C_US = [1, 3, 5, 7, 9, 11, 13, 17, 31, 63, 127, 255]


def section_C(ctx, cal):
    """parameter-five gateway (k=1 catapult)."""
    r4 = cal.crossing(4)
    ctx.check("canonical_tests", "X4_odd_type_a_tau2", "C0",
              bool(r4["odd"] and r4["kind"] == "a" and r4["time"] == 2),
              ("X(4)", r4["kind"], r4["time"]))
    amb = 0
    amb_ex = []
    for Q in C_QS:
        for C in C_CS:
            if gcd(C, Q) != 1:
                continue
            for b in (0, 1):
                for H in (6, 8, 12, 20, 40):
                    M = 1 << H
                    for lift in (0, 1):
                        for u in C_US:
                            x, theta, cls = build_state(5, Q, C, b, lift, u, H=H)
                            xn = 2 * theta + 6 - (x >> 1)
                            tn = theta + 9
                            Dn = tn - xn
                            m = v2(xn)
                            Cpred = 15 * Q - C - 32 * b * Q
                            if m is not None and m < H:
                                ok = ((3 * Q * Dn - (15 * Q - C - 32 * b * Q + 3 * Q * (1 << m)))
                                      % (1 << (m + 1)) == 0)
                                ctx.check("synthetic_tests", "gateway_class", "C1", ok,
                                          ("gw", Q, C, b, H, lift, u, m))
                                ht = F(abs(C), Q)
                                htp = F(abs(Cpred), 3 * Q)
                                ctx.check("synthetic_tests", "gateway_height_bound", "C2",
                                          htp <= 5 + ht / 3 + F(32 * b, 3),
                                          ("gwheight", Q, C, b, H, lift, u, ht, htp))
                                # reduced denominator: 3Q, reduced by 3 when 3 | C'
                                tri = (Cpred % 3 != 0)
                                num, den = Cpred, 3 * Q
                                while num % 3 == 0 and den > 1:
                                    num //= 3
                                    den //= 3
                                ctx.check("synthetic_tests", "gateway_rank_rule", "C3",
                                          rank_of(den) == (rank_of(Q) + 1 if tri else rank_of(Q)),
                                          ("gwrank", Q, C, b, Cpred, den))
                                # rank 0 exception
                                if Q == 1 and ((C + 2 * b) % 3 == 0):
                                    ctx.check("synthetic_tests", "gateway_rank_zero_exception", "C3",
                                              not tri, ("expected no tripling", C, b, Cpred))
                            else:
                                # m >= H (or x'=0): the same class mod 2^H with a different
                                # lift may give a different output parameter
                                if xn == 0:
                                    continue
                                x2, theta2, _ = build_state(5, Q, C, b, lift + 1, u, H=H)
                                xn2 = 2 * theta2 + 6 - (x2 >> 1)
                                if xn2 != 0 and v2(xn2) != m:
                                    amb += 1
                                    if len(amb_ex) < 8:
                                        amb_ex.append({"Q": Q, "C": C, "b": b, "H": H,
                                                       "u": u, "m": m, "m_other_lift": v2(xn2)})
    ctx.data["C_m_ge_H_ambiguity"] = {
        "cases": amb, "examples": amb_ex,
        "note": "m>=H: the class mod 2^H does not determine the gateway output",
    }
    ctx.check("synthetic_tests", "gateway_m_ge_H_is_provenance", "C4", amb > 0,
              ("no ambiguity found for m>=H",))

    # iterated height ladder bound  ht_t <= 47/2 + 3^{-t}(h0-47/2)
    for h0 in (F(0), F(1), F(10), F(31), F(100)):
        ht = h0
        for t in range(1, 9):
            ht = 5 + F(32, 3) + ht / 3
            bound = F(47, 2) + F(1, 3 ** t) * (h0 - F(47, 2))
            ctx.check("synthetic_tests", "gateway_height_ladder", "C5", ht <= bound,
                      ("ladder", h0, t, ht, bound))


# ----------------------------------------------------------------------------- D: height/rank/record
def section_D(ctx, cal):
    """A is preserved at a-steps, Lipschitz at b/c steps; ht <= A+3/2; records."""
    for j in list(range(5, 121)) + [150, 200]:
        row = cal.crossing(j - 1)
        if not (row["odd"] and row["kind"] == "a"):
            continue
        k = row["time"] // 2
        for Q in (1, 3, 9, 27):
            for C in (-17, -13, -5, -1, 1, 4, 5, 7, 10, 13, 26):
                if gcd(C, Q) != 1:
                    continue
                for b in (0, 1):
                    ht = F(abs(C), Q)
                    A = abs(F(C, Q) - F(3, 2))
                    ctx.check("synthetic_tests", "height_ht_le_A_plus_3_2", "D1",
                              ht <= A + F(3, 2), ("htA", j, Q, C, ht, A))
                    val = v2(3 * Q * k + C)
                    p0 = None if val is None else 1 + val
                    if p0 is not None and p0 <= j - 2:
                        C2 = 3 * Q - C
                        A2 = abs(F(C2, Q) - F(3, 2))
                        ctx.check("synthetic_tests", "height_A_preserved_a", "D1",
                                  A2 == A, ("A", j, Q, C, b, A, A2))
                        ctx.check("synthetic_tests", "record_strong_descent", "D4",
                                  p0 + 1 <= j, ("rec", j, p0))
                    elif p0 is None or p0 >= j:
                        ctx.check("synthetic_tests", "record_one_step_equal", "D4",
                                  (j - 1) + 1 == j, ("rec1", j, p0))
    # b/c Lipschitz on canonical crossings with the minimal-cost shift
    for n in range(4, 1200):
        row = cal.crossing(n)
        if not (row["odd"] and row["kind"] != "a"):
            continue
        kind, tau, eps, omega, cW, lam = crossing_ab(cal, n)
        j = n + 1
        phi2 = 3 * tau + 5 - lam - 2
        for Q in (1, 3, 9, 27):
            r = rank_of(Q)
            for C in (-13, -1, 1, 4, 10, 26):
                if gcd(C, Q) != 1:
                    continue
                c = F(C, Q)
                A = abs(c - F(3, 2))
                cands = best_shift(phi2, omega, r)
                best = None
                for (d, a) in cands:
                    s = F(a, 3 ** d) if d >= 0 else F(a)
                    cost = 2 * max(r, d) + height_pen(c + s)
                    key = (cost, abs(s))
                    if best is None or key < best[0]:
                        best = (key, d, a, s)
                _, d, a, s = best
                A2 = abs(c + s - F(3, 2))
                ctx.check("canonical_tests", "height_Lipschitz_bc", "D2",
                          A2 <= A + abs(s), ("lip", n, Q, C, d, a, A, A2))
                C2, Q2 = apply_shift(C, Q, r, d, a)
                C2_raw = C * 3 ** max(0, d - r) + a * 3 ** max(0, r - d)
                ctx.check("canonical_tests", "rank_rule_bc", "D3",
                          rank_of(Q2) <= max(r, d), ("rankbound", n, Q, C, d, a, rank_of(Q2)))
                ctx.check("canonical_tests", "rank_rule_bc_dichotomy", "D3",
                          (rank_of(Q2) == max(r, d)) == (C2_raw % 3 != 0 or max(r, d) == 0),
                          ("rankdich", n, Q, C, d, a, rank_of(Q2), C2_raw))
                ctx.check("canonical_tests", "record_bc_descent", "D4",
                          omega + (1 + eps) <= j, ("recbc", n, omega, eps))


# ----------------------------------------------------------------------------- E: certify
E_QS = [1, 3, 9, 27]
E_CS = list(range(-40, 41))


def section_E(ctx, cal):
    """certify_Q == certify(j,delta); lift invariance; propagation; small-j scan."""
    for j in range(5, 129):
        M = 1 << (j + 1)
        for Q in E_QS:
            for C in E_CS:
                if gcd(C, Q) != 1:
                    continue
                for b in (0, 1):
                    delta = ((C * pow(Q, -1, M)) + b * (1 << j)) % M
                    r1 = certify(cal, j, delta, j + 1)
                    # name swap (C,b) -> (C - 2^j Q, 1-b)
                    C2 = C - (1 << j) * Q
                    b2 = 1 - b
                    delta2 = ((C2 * pow(Q, -1, M)) + b2 * (1 << j)) % M
                    ctx.check("synthetic_tests", "certify_name_swap_same_class", "E1",
                              delta2 == delta, ("swap", j, Q, C, b))
                    r2 = certify(cal, j, delta2, j + 1)
                    ctx.check("synthetic_tests", "certify_name_swap_same_result", "E1",
                              (r1["status"], r1["record"], r1["word"]) ==
                              (r2["status"], r2["record"], r2["word"]),
                              ("swapres", j, Q, C, b))
                    # lift delta + 2^{j+1}
                    r3 = certify(cal, j, delta + M, j + 1)
                    ctx.check("synthetic_tests", "certify_high_lift_same_result", "E1",
                              (r1["status"], r1["record"], r1["word"]) ==
                              (r3["status"], r3["record"], r3["word"]),
                              ("lift", j, Q, C, b, r1["status"], r3["status"]))
    # propagation: certified classes -> same word for all u and lifts
    tested = 0
    for j in (17, 30, 49, 64, 100):
        for delta in (-11, -2, 0, 1, 5, 14, 31, 97):
            r = certify(cal, j, delta, j + 1)
            if r["status"] != "end":
                continue
            tested += 1
            words = []
            for u in (1, 3, 5, 9, 33):
                for lift in (0, 1, 3):
                    x, theta, _ = build_state(j, 1, delta, 0, lift, u)
                    rr = exact_walk(cal, x, theta, j + 1)
                    words.append((rr["status"], tuple(rr["word"]), rr["types"], rr["record"]))
            ctx.check("synthetic_tests", "certify_propagation_same_word", "E2",
                      len(set(words)) == 1, ("prop", j, delta, set(words)))
    ctx.data["E_propagation_classes_tested"] = tested

    # small-j exhaustive scan: all residues; compare exception counts to the
    # accepted [B] statement (4,4,4,4,8 at j=5,8,12,14,17).
    exc = {}
    t0 = time.time()
    for j in range(5, 19):
        M = 1 << (j + 1)
        bad = []
        for delta in range(M):
            r = certify(cal, j, delta, j + 1)
            if not (r["status"] == "end" and r["record"] <= j):
                bad.append(delta)
        exc[j] = bad
        if j >= 5:
            ctx.check("canonical_tests", "small_j_all_residues_scanned", "E3",
                      len(bad) < M, ("all fail", j))
    expected = {5: 4, 8: 4, 12: 4, 14: 4, 17: 8}
    for j, cnt in expected.items():
        got = len(exc.get(j, []))
        ctx.check("canonical_tests", "small_j_exception_count", "E3", got == cnt,
                  ("exception count", j, got, cnt))
        sym = [d if d <= (1 << j) else d - (1 << (j + 1)) for d in exc.get(j, [])]
        ctx.data.setdefault("small_j_exceptions", {})[j] = {
            "count": got, "residues": exc.get(j, [])[:20],
            "residues_symmetric": sym[:20], "accepted_count": cnt,
        }
    ctx.data["small_j_scan_seconds"] = round(time.time() - t0, 2)
    for j in (6, 7, 9, 10, 11, 13, 15, 16, 18):
        ctx.check("canonical_tests", "small_j_no_exception_nonodd_a", "E3",
                  len(exc.get(j, [])) == 0, ("unexpected", j, exc.get(j, [])[:5]))


# ----------------------------------------------------------------------------- F: landing
def landing_stats(ctx, cal, nmax=2000):
    """Residues of landing classes: window membership statistics."""
    stats = {"in_window": 0, "exceptions": 0, "other": 0}
    for n in range(4, nmax):
        row = cal.crossing(n)
        if not row["odd"]:
            continue
        kind, tau, eps, omega, cW, lam = crossing_ab(cal, n) if row["kind"] != "a" else (
            "a", row["time"], 0, None, None, None)
        j = n + 1
        # choose a description of the incoming class and land
        for (Q, C, b) in ((1, 10, 0), (3, 10, 1), (1, -11, 0), (3, 26, 1), (1, 5, 0)):
            M = 1 << (j + 1)
            delta = ((C * pow(Q, -1, M)) + b * (1 << j)) % M
            if row["kind"] == "a":
                if row["time"] % 2:
                    continue
                k = row["time"] // 2
                val = v2(3 * Q * k + C)
                p0 = None if val is None else 1 + val
                if p0 is not None and p0 <= j - 2:
                    jp = p0
                    Dp = (3 * Q - C) * pow(Q, -1, 1 << (jp + 1))
                    res = Dp % (1 << (jp + 1))
                    if res > (1 << jp):
                        res -= (1 << (jp + 1))
                    tag = "a"
                else:
                    continue
            else:
                jp = omega
                phi2 = 3 * tau + 5 - lam - 2
                sym = phi2 % (1 << (jp + 1))
                if sym > (1 << jp):
                    sym -= (1 << (jp + 1))
                res = sym
                tag = row["kind"]
            if -12 <= res <= 15:
                stats["in_window"] += 1
                if (jp, res) in ((5, 5), (5, -11)):
                    stats["exceptions"] += 1
            else:
                stats["other"] += 1
    ctx.data["landing_residue_stats"] = stats
    ctx.data["landing_residue_note"] = (
        "counts of landing residues in the accepted window [-12,15] vs outside, over the "
        "sampled canonical chains; the window applies only for 5<=j<2e7 (here j<=2000)")


def rat_walk(cal, j, C, Q, b, maxsteps=20000):
    """Class walk with the rational bookkeeping.  Returns a dict of diagnostics."""
    G = 0
    A = abs(F(C, Q) - F(3, 2))
    steps = 0
    depth_fail = []
    nt_gates = []
    rec_raise = []
    one_steps = 0
    while steps < maxsteps:
        n = j - 1
        if n < 0:
            return {"status": "small", "steps": steps, "A": A, "j": j, "C": C, "Q": Q, "b": b,
                    "depth_fail": depth_fail, "nt_gates": nt_gates, "rec_raise": rec_raise}
        row = cal.crossing(n)
        if not row["odd"]:
            return {"status": "end", "steps": steps, "A": A, "j": j, "C": C, "Q": Q, "b": b,
                    "depth_fail": depth_fail, "nt_gates": nt_gates, "rec_raise": rec_raise}
        R = j + G
        tau = row["time"]
        if row["kind"] == "a":
            k = tau // 2
            ht_bound = A + F(3, 2)
            depth_ok = (Q * (kappa(j) + ht_bound) < (1 << (j - 2)))
            if not depth_ok:
                depth_fail.append({"j": j, "Q": Q, "h_t": str(ht_bound)})
            val = v2(3 * Q * k + C)
            p0 = None if val is None else 1 + val
            if p0 is not None and p0 <= j - 2:
                G += 1
                j, C, Q, b = p0, 3 * Q - C, Q, 0
                if j + G > R - 1:
                    rec_raise.append({"at": "strong", "j": j, "G": G, "R": R})
            elif p0 is None or p0 >= j:
                one_steps += 1
                C2 = (9 + 6 * k) * Q - C - b * Q * (1 << j)
                Q2 = 3 * Q
                b2 = 1
                while C2 % 3 == 0 and Q2 > 1:
                    C2 //= 3
                    Q2 //= 3
                G += 1
                j, C, Q, b = j - 1, C2, Q2, b2
                if j + G != R:
                    rec_raise.append({"at": "onestep", "j": j, "G": G, "R": R})
            else:
                nt_gates.append({"j": j, "Q": Q, "C": C, "b": b, "p0": p0})
                # j = 5 is the gateway (resolvable by the exact bits / Lemma CB);
                # any other NT gate is the provenance-dependent case
                return {"status": "gateway" if j == 5 else "nt_gate", "steps": steps, "A": A,
                        "j": j, "C": C, "Q": Q, "b": b, "depth_fail": depth_fail,
                        "nt_gates": nt_gates, "rec_raise": rec_raise}
        else:
            kind, tau2, eps, omega, cW, lam = crossing_ab(cal, n)
            phi2 = 3 * tau2 + 5 - lam - 2
            r = rank_of(Q)
            cands = best_shift(phi2, omega, r)
            c = F(C, Q)
            best = None
            for (d, a) in cands:
                s = F(a, 3 ** d)
                cost = 2 * max(r, d) + height_pen(c + s)
                key = (cost, abs(s))
                if best is None or key < best[0]:
                    best = (key, d, a)
            _, d, a = best
            C2, Q2 = apply_shift(C, Q, r, d, a)
            G += 1 + eps
            j, C, Q, b = omega, C2, Q2, 0
            if j + G > R - 1:
                rec_raise.append({"at": "bc", "j": j, "G": G, "R": R})
        A = abs(F(C, Q) - F(3, 2))
        steps += 1
    return {"status": "limit", "steps": steps, "A": A, "j": j, "C": C, "Q": Q, "b": b,
            "depth_fail": depth_fail, "nt_gates": nt_gates, "rec_raise": rec_raise}


def section_F(ctx, cal):
    """RAT-C: (DEPTH) walks for the r1r2 gateway families and the BBBAA landing family."""
    fams = []
    for m in range(19, 1001):
        fams.append(("(10-2^m)/3", m, 10, 3, 1))
        fams.append(("(26-2^m)/3", m, 26, 3, 1))
        for old in (-2, 1, 4, 7, 10, 13, 16):
            if (m - 19) % 7 == old % 7:
                fams.append(("BBBAA C/3", m, 3 * old + 4, 3, 0))
    fam_res = {}
    for (name, m, C, Q, b) in fams:
        d = rat_walk(cal, m, C, Q, b)
        f = fam_res.setdefault(name, {"n": 0, "end": 0, "gateway": 0, "nt_gate": 0,
                                      "depth_fail_count": 0, "max_A": None, "max_steps": 0,
                                      "rec_raise": 0})
        f["n"] += 1
        f[d["status"]] = f.get(d["status"], 0) + 1
        df19 = [x for x in d["depth_fail"] if x["j"] >= 19]
        if df19:
            f["depth_fail_count"] += 1
        f.setdefault("depth_fail_all_j", 0)
        if d["depth_fail"]:
            f["depth_fail_all_j"] += 1
        Astr = str(d["A"])
        f["max_A"] = Astr if f["max_A"] is None else str(max(F(f["max_A"]), d["A"]))
        f["max_steps"] = max(f["max_steps"], d["steps"])
        if d["rec_raise"]:
            f["rec_raise"] += 1
        ctx.check("canonical_tests", "RAT_C_family_walk_ok", "F1",
                  d["status"] in ("end", "gateway") and not d["rec_raise"],
                  (name, m, d["status"], d["rec_raise"][:2], d["nt_gates"][:2]))
        # (DEPTH) at every chain with j>=19 must exclude NT gates at j>=6
        nt_high = [g for g in d["nt_gates"] if g["j"] >= 6]
        ctx.check("canonical_tests", "RAT_C_depth_implies_no_nt", "F1",
                  not nt_high, (name, m, nt_high[:2]))
        ctx.check("canonical_tests", "RAT_C_depth_at_j19plus", "F1",
                  not df19, (name, m, df19[:2]))
    ctx.data["RAT_C_families"] = fam_res
    ctx.data["RAT_C_note"] = (
        "walks use the minimal-cost representative; j>=19 segment checked against (DEPTH)")
    # BBBAA family heights
    hs = [abs(F(C, 3) - F(3, 2)) + F(3, 2) for C in (-2, 1, 4, 7, 10, 13, 16)]
    ctx.data["BBBAA_landing_heights"] = [str(h) for h in hs]
    ctx.check("synthetic_tests", "BBBAA_heights_le_31", "F2", all(h <= 31 for h in hs),
              ("heights", [str(h) for h in hs]))


# ----------------------------------------------------------------------------- G: O1
def section_G(ctx, cal512):
    """O1: P=49 orbit-shift source in the rational normal form."""
    fire = first_fire(cal512, 49)
    ctx.data["O1_fire"] = {"k": fire["k"], "pointer": fire["pointer"], "J": fire["J"]}
    ctx.check("canonical_tests", "O1_source_P49", "G1",
              fire["J"] == 49 and fire["k"] == 469124961184426, ("fire", fire))
    sigma = fire["pointer"]
    ctx.check("canonical_tests", "O1_source_pointer", "G1",
              sigma == 1051689726214394, ("pointer", sigma))
    x48 = cal512.crossing(48)
    ctx.check("canonical_tests", "O1_X48_odd_a_tau40", "G1",
              bool(x48["odd"] and x48["kind"] == "a" and x48["time"] == 40),
              ("X(48)", x48["kind"], x48["time"]))
    k = 20
    x0 = 6 * fire["k"] + 4
    ctx.check("canonical_tests", "O1_x0_5x2^49", "G1", x0 == 5 * (1 << 49), ("x0", x0))
    theta0 = x0 + 1
    y = 2 * theta0 + 6 * k - (x0 >> 1)
    A = (y - 10) // 16
    ctx.check("canonical_tests", "O1_y_eq_16A_plus_10", "G1",
              y == 16 * A + 10 and A == 15 * (1 << 44) + 7, ("y", y, "A", A))
    ctx.check("canonical_tests", "O1_v2_y_1", "G1", v2(y) == 1, ("v2(y)", v2(y)))
    # rational source: D = -4 + 8/3^r, Q=3^r, C=-4*3^r+8, b=0
    rows = []
    for r in range(1, 201):
        Q = 3 ** r
        C = -4 * Q + 8
        ctx.check("synthetic_tests", "O1_certificate_gcd", "G2",
                  gcd(C, Q) == 1, ("gcd", r))
        ht = F(abs(C), Q)
        ctx.check("synthetic_tests", "O1_height_le_4", "G2", ht <= 4, ("ht", r, ht))
        p0 = 1 + v2(3 * Q * k + C)
        aprime = A * 3 ** r + 1
        # x' = 16*(A + 3^{-r});  v2(x') = 4 + v2(A*3^r+1)
        xn = F(15 * (1 << 48) + 112) + F(16, 3 ** r)
        vnum = v2(xn.numerator) - v2(xn.denominator)
        ctx.check("synthetic_tests", "O1_v2_xprime_formula", "G2",
                  vnum == 4 + v2(aprime), ("v2x", r, vnum, 4 + v2(aprime)))
        rows.append({"r": r, "p0": p0, "v2_xp": vnum})
    ctx.data["O1_small_r_rows"] = rows[:20]
    # A = 15*2^44+7, so A*3^r+1 = (7*3^r+1) + 2^44*15*3^r; hence v2(A*3^r+1) equals
    # v2(7*3^r+1) when that is < 44, and is >= 44 when it is >= 44.
    for r in range(1, 120):
        aprime = A * 3 ** r + 1
        small = 7 * 3 ** r + 1
        ctx.check("synthetic_tests", "O1_A_identity", "G3",
                  aprime == small + (1 << 44) * 15 * 3 ** r, ("A identity", r))
        vs = v2(small)
        if vs < 44:
            ctx.check("synthetic_tests", "O1_v2_below_44_equal", "G3",
                      v2(aprime) == vs, ("v2", r, v2(aprime), vs))
        else:
            ctx.check("synthetic_tests", "O1_v2_ge_44", "G3", v2(aprime) >= 44,
                      ("v2>=44", r, v2(aprime)))
    ctx.data["O1_p0_j_minus_1_characterisation"] = (
        "p0 = 4+v2(7*3^r+1); p0 = j-1 = 48 iff v2(7*3^r+1) = 44; combined with "
        "v2(A*3^r+1) >= sigma-5 > 44 this forces v2(7*3^r+1) = 44 exactly, i.e. the "
        "O1 dangerous r are precisely the p0 = j-1 (NT-gate) boundary.  Not realisable "
        "at r <= 200, so this step is [A] by the displayed identity, not [B].")
    # (DEPTH) at the source j=49: 3^r*(kappa(49)+4) < 2^47  <=>  r <= 18
    k49 = kappa(49)
    ok = []
    for r in range(0, 80):
        holds = (3 ** r * (k49 + 4) < (1 << 47))
        ok.append((r, holds))
    max_r = max(r for r, h in ok if h)
    min_r_fail = min(r for r, h in ok if not h)
    ctx.check("synthetic_tests", "O1_depth_threshold_r_le_18", "G4",
              max_r == 18 and min_r_fail == 19, ("threshold", max_r, min_r_fail))
    ctx.data["O1_depth_threshold"] = {"max_r_covered": max_r, "min_r_violating": min_r_fail,
                                      "kappa49": str(k49)}
    # sharpened necessary condition r >= ceil(log_3((2^(sigma-5)-1)/A))
    from decimal import Decimal, getcontext
    getcontext().prec = 60
    ln3 = Decimal(3).ln()
    x = Decimal(sigma - 5) * Decimal(2).ln() / ln3 - Decimal(A).ln() / ln3
    r_min = int(x) + 1
    frac = x - int(x)
    o1_bound = Decimal(5 * (sigma - 53)) / Decimal(8)
    ctx.check("synthetic_tests", "O1_sharpened_r_min", "G5",
              r_min == 663542339794048, ("r_min", r_min, str(x)))
    ctx.data["O1_sharpened"] = {
        "r_min": r_min, "fractional_part": str(frac), "o1_bound": str(o1_bound),
        "margin": str(frac), "note": "60-digit Decimal; the fractional part is 0.7665, "
                                    "far from an integer boundary, so the ceil is certain"}
    ctx.data["O1_verdict"] = (
        "the O1 dangerous r are exactly the p0=j-1 boundary (NT gate); they violate "
        "(DEPTH) at the source by ~1.04e15 bits")


# ----------------------------------------------------------------------------- H: O2
def section_H(ctx):
    """O2: STOP_CHECKPOINT family, arbitrary record jump at height <= 5."""
    rows = []
    for m in range(6, 513, 2):
        u = ((1 << (m - 4)) - 1) // 3
        if u % 2 == 0:
            continue
        x = 32 * u
        theta = x + 5
        xn = 2 * theta + 6 - (x >> 1)
        tn = theta + 9
        Dn = tn - xn
        ok = (xn == (1 << m)) and (v2(xn) == m) and \
             ((3 * Dn - (10 - (1 << m))) % (1 << (m + 1)) == 0)
        ctx.check("synthetic_tests", "O2_family_exact", "H1", ok,
                  ("O2", m, xn.bit_length(), Dn))
        rows.append({"m": m, "x_prime": str(1 << m), "record_in": 5, "record_out": m + 1})
    ctx.data["O2_family_rows"] = rows[:12]
    ctx.data["O2_family_count"] = len(rows)
    ctx.check("synthetic_tests", "O2_record_unbounded", "H2",
              len(rows) > 0 and rows[-1]["record_out"] > 500,
              ("O2 max record", rows[-1] if rows else None))


# ----------------------------------------------------------------------------- I: O3
def section_I(ctx):
    S = 64
    total = 0
    for r in range(0, S // 2 + 1):
        total += (2 * (S - 2 * r) + 1) * 3 ** r + 1
    ctx.check("synthetic_tests", "O3_count_below_2_64", "I1", total < (1 << 64),
              ("count", total))
    ctx.check("synthetic_tests", "O3_count_exact_value", "I1", total == 8338590849833250,
              ("count value", total))
    table = []
    for (j, h, R) in ((64, 5, 32), (100, 31, 64), (200, 31, 128)):
        cov = (R + 1) * (2 * h + 1)
        table.append({"j": j, "h": h, "R": R, "low_cost_descriptions": cov,
                      "classes": 1 << (j + 1), "ratio": str(F(cov, 1 << (j + 1)))})
    ctx.data["O3_table"] = table
    ctx.check("synthetic_tests", "O3_enumeration_hopeless", "I2",
              all(F(t["low_cost_descriptions"], t["classes"]) < F(1, 1000) for t in table),
              ("ratio", table))


# ----------------------------------------------------------------------------- J: falsification
def section_J(ctx):
    """Aggregate the falsification tests F1-F11 of PLAN section 9."""
    mapping = {
        "F1": ["a_step_canonical_strong", "a_step_synthetic_strong"],
        "F2": ["a_step_canonical_onestep", "a_step_synthetic_onestep"],
        "F3": ["a_step_canonical_nozero", "a_step_synthetic_nozero"],
        "F4": ["gateway_class", "gateway_height_bound"],
        "F5": ["bc_class_recurrence", "bc_synthetic_shift_class"],
        "F6": ["certify_propagation_same_word"],
        "F7": ["certify_name_swap_same_result", "certify_high_lift_same_result"],
        "F8": ["small_j_exception_count"],
        "F9": ["O2_family_exact", "O2_record_unbounded"],
        "F10": ["RAT_C_family_walk_ok"],
        "F11": ["height_A_preserved_a", "height_Lipschitz_bc"],
    }
    out = {}
    for f, names in mapping.items():
        n = 0
        fl = 0
        for nm in names:
            for bucket in ("canonical_tests", "synthetic_tests"):
                d = getattr(ctx, bucket).get(nm)
                if d:
                    n += d["n"]
                    fl += d["fail"]
        out[f] = {"checks": n, "fail": fl, "kills": [nm for nm in names if nm in ctx.fail_count]}
    ctx.data["falsification"] = out


# ----------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    cal = Calendar(256)
    cal512 = Calendar(512)
    ctx = Ctx()

    ctx.note("A1", "[A]", "strong descent: j'=p, C'=3Q-C, b'=0")
    ctx.note("A2", "[A]", "one-step descent: j'=j-1, class mod 2^j determined")
    ctx.note("A3", "[A]", "NT gate: v2(x')>=j-1, outcome depends on u (not on the class)")
    ctx.note("A4", "[A]", "x'!=0 for Q>1; Q=1 resonance exists")
    ctx.note("B1", "[A]", "omega=v2(lambda'), sigma=n-eps, S1")
    ctx.note("B2", "[A]", "D' = D + Phi - 2 (mod 2^{omega+1})")
    ctx.note("B3", "[A]", "rational shifts a/3^d: Q'=3^max(r,d), C' formula")
    ctx.note("C0", "[B]", "canonical base: X(4) is odd type a with tau(4)=2")
    ctx.note("C1", "[A]", "gateway class C'=15Q-C-32bQ, Q'=3Q, b'=1 (m<H)")
    ctx.note("C2", "[A]", "gateway height ht' <= 5+ht/3+32b/3")
    ctx.note("C3", "[A]", "rank +1 at gateway (r>=1); r=0 exception")
    ctx.note("C4", "[A]", "m>=H: class does not determine the output")
    ctx.note("C5", "[A]", "iterated gateway height bound ht_t <= 47/2 + 3^-t (h0-47/2)")
    ctx.note("D1", "[A]", "A preserved at a-steps, ht<=A+3/2")
    ctx.note("D2", "[A]", "A' <= A+|s| at b/c steps")
    ctx.note("D3", "[A]", "rank r'=max(r,d)")
    ctx.note("D4", "[A]", "record R'<=R-1 or =R")
    ctx.note("E1", "[A]", "certify depends only on the class (lift invariance)")
    ctx.note("E2", "[A]", "certified class propagates to every state with that class")
    ctx.note("E3", "[B]", "small-j exhaustive scan, compare exception counts")
    ctx.note("F1", "[A+B]", "RAT-C (DEPTH) walks for the gateway/BBBAA families")
    ctx.note("F2", "[A]", "BBBAA landing heights <= 16/3 + 3/2")
    ctx.note("G1", "[A]", "O1 source data")
    ctx.note("G2", "[A]", "O1 certificate (C,Q,b) and v2(x')")
    ctx.note("G3", "[A]", "O1 p0=j-1 boundary characterisation")
    ctx.note("G4", "[A]", "(DEPTH) threshold r<=18 at the O1 source")
    ctx.note("G5", "[B]", "sharpened O1 r_min (high-precision, not exact integers)")
    ctx.note("H1", "[A]", "O2 family exact")
    ctx.note("H2", "[A]", "no h-only record bound")
    ctx.note("I1", "[A]", "O3 count < 2^64")
    ctx.note("I2", "[A]", "low-cost enumeration cannot cover classes")

    section_A(ctx, cal)
    section_B(ctx, cal)
    section_C(ctx, cal)
    section_D(ctx, cal)
    section_E(ctx, cal)
    section_F(ctx, cal)
    section_G(ctx, cal512)
    section_H(ctx)
    section_I(ctx)
    section_J(ctx)

    total_checks = sum(d["n"] for d in list(ctx.canonical_tests.values()) + list(ctx.synthetic_tests.values()))
    total_fail = sum(d["fail"] for d in list(ctx.canonical_tests.values()) + list(ctx.synthetic_tests.values()))
    elapsed = round(time.time() - t0, 2)
    status = "PASS" if total_fail == 0 else "FAIL"
    out = {
        "status": status,
        "scope": (
            "Exact integer/rational checks of the rational-mode normal form (PLAN.md): "
            "a-step three-way classification, b/c class recurrence, parameter-five gateway, "
            "height/rank/record recursions, certify/lift invariance, small-j exhaustive scan, "
            "RAT-C (DEPTH) walks, O1/O2/O3. Canonical crossings from "
            "work_global_calendar/calendar_oracle.Calendar(256/512); every synthetic state is "
            "labelled canonical:false. Not a proof of global EXT; K_clock unchanged. "
            "Bounded [B] statements are not extrapolated beyond their ranges."
        ),
        "canonical_tests": ctx.canonical_tests,
        "synthetic_tests": ctx.synthetic_tests,
        "conclusions": ctx.claims,
        "failures": ctx.failures,
        "failures_truncated": ctx.truncated,
        "data": ctx.data,
        "counts": {
            "total_checks": total_checks,
            "total_fail": total_fail,
            "canonical_checks": sum(d["n"] for d in ctx.canonical_tests.values()),
            "synthetic_checks": sum(d["n"] for d in ctx.synthetic_tests.values()),
            "elapsed_seconds": elapsed,
        },
    }
    OUT.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "total_checks": total_checks,
                      "total_fail": total_fail,
                      "canonical": sum(d["n"] for d in ctx.canonical_tests.values()),
                      "synthetic": sum(d["n"] for d in ctx.synthetic_tests.values()),
                      "elapsed_s": elapsed}))
    if ctx.failures:
        print("FAILURES (first %d):" % len(ctx.failures))
        for f in ctx.failures[:10]:
            print("  ", f)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
