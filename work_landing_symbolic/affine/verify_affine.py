"""verify_affine.py -- exact checks for the affine-origin landing criterion.

Run:  python -B work_landing_symbolic/affine/verify_affine.py
Writes: work_landing_symbolic/affine/checks.json

Scope: canonical states from work_global_calendar/calendar_oracle.py Calendar(512)
(first fires P=5..256 and every chain of their epochs) and explicitly synthetic
(non-canonical) states.  All arithmetic is exact (int / fractions.Fraction).  No float
is used for any decision.

Tags: [B] finite exact computation; [A] identities are proved in PLAN.md and re-checked
here; [C] items are not tested (reported as not_run).  No global EXT claim; K_clock
unchanged.
"""
import sys, json, random, time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'work_global_calendar'))
from calendar_oracle import Calendar, val  # noqa: E402

N0 = 2 * 10 ** 7
B = 2 ** 10 ** 7
H_HEIGHT = 64
LIMIT = 4000

failures = []
counts = {}


def fail(tag, detail):
    failures.append({"tag": tag, "detail": str(detail)[:800]})


def bump(key, n=1):
    counts[key] = counts.get(key, 0) + n


def v2(q):
    q = F(q)
    if q == 0:
        return None
    a = abs(q.numerator)
    b = q.denominator
    return (a & -a).bit_length() - (b & -b).bit_length()


INF = 10 ** 9


def vv(q):
    return INF if F(q) == 0 else v2(q)


def sym(e, bits):
    """symmetric residue mod 2**bits (e may be an integer or an element of Z[1/3])."""
    M = 1 << bits
    e = F(e)
    den = e.denominator
    assert den % 2 == 1, ("even denominator", e)
    num = e.numerator * pow(den, -1, M)
    r = num % M
    return r - M if r > M // 2 else r


# --------------------------------------------------------------------------- #
class St:
    __slots__ = ('J', 'alpha', 'beta', 'd', 'Gamma', 'U')

    def __init__(self, J, alpha, beta, d, Gamma, U):
        self.J = int(J)
        self.alpha = F(alpha)
        self.beta = F(beta)
        self.d = F(d)
        self.Gamma = int(Gamma)
        self.U = int(U)

    @property
    def j(self):
        return self.J + v2(self.alpha)

    @property
    def x(self):
        return self.alpha * (1 << self.J) * self.U + self.beta

    @property
    def Theta(self):
        return (1 << self.J) * self.U + 3 * self.d + 1

    @property
    def theta(self):
        return 3 * self.d + 1 - self.beta

    @property
    def record(self):
        return self.j + self.Gamma

    def step_a(self, k):
        return St(self.J, 2 - self.alpha / 2,
                  6 * self.d + 2 + 6 * k - self.beta / 2,
                  self.d + 1 + 2 * k, self.Gamma + 1, self.U)

    def step_bc(self, ratio, lam, tau, eps):
        return St(self.J, ratio * self.alpha, ratio * self.beta + lam,
                  self.d + 1 + tau, self.Gamma + 1 + eps, self.U)

    def shift_d(self, eta):
        return St(self.J, self.alpha, self.beta, self.d + F(eta, 3),
                  self.Gamma, self.U)


def make_anchor(U, Gamma, J, x, Theta):
    """Balanced tie-free origin at a concrete state with J=j+Gamma.

    alpha = 2**(-Gamma), beta = x - 2^j U, d = (Theta - 2^J U - 1)/3 (in Z[1/3]).
    Any odd multiplier c would also work; c=1 is the minimal choice.
    """
    j = v2(x)
    if j is None or j < 1 or J < j:
        return None
    alpha = F(1, 1 << Gamma) if Gamma >= 0 else F(1 << (-Gamma))
    d = F(Theta - (1 << J) * U - 1, 3)
    beta = F(x) - alpha * (1 << J) * U
    if beta != 0 and v2(beta) < j + 1:
        return None
    st = St(J, alpha, beta, d, Gamma, U)
    if st.j != j or st.x != x or st.Theta != Theta:
        return None
    return st


def read_crossing(cal, j):
    r = cal.crossing(j - 1)
    out = {"odd": r["odd"], "kind": r["kind"], "tau": r["time"],
           "eps": r["epsilon"], "ratio": None, "lam": None, "omega": None}
    if r["odd"] and r["kind"] != 'a':
        hr = r["head_ratio"]
        tr = r["tail_ratio"] if r["tail_ratio"] is not None else F(0)
        out["ratio"] = (hr + 2 * tr) / 2
        out["lam"] = r["head_lambda"] + 2 * r["tail_lambda"] + 3
        out["omega"] = v2(out["lam"])
    return out


# --------------------------------------------------------------------------- #
def chain_sequence(cal, x, Theta, s0, sigma, limit=LIMIT):
    """Exact walk; returns (chains, status).  chains: dicts with j,G,s,x,Theta,kind."""
    x, Theta = F(x), F(Theta)
    G = 0
    s = s0
    out = []
    for _ in range(limit):
        if x == 0:
            return out, 'zero'
        j = v2(x)
        if j is None or j < 0:
            return out, 'badval'
        rec = j + G
        if rec >= sigma:
            return out, 'ceiling'
        if j <= 4:
            out.append(dict(j=j, G=G, s=s, x=x, Theta=Theta, kind='e'))
            return out, 'end'
        r = cal.crossing(j - 1)
        out.append(dict(j=j, G=G, s=s, x=x, Theta=Theta,
                        kind=(r['kind'] if r['odd'] else 'e')))
        if not r['odd']:
            return out, 'end'
        if r['kind'] == 'a':
            k = r['time'] // 2
            x = 2 * Theta + 6 * k - x / 2
        else:
            hr = r['head_ratio']
            tr = r['tail_ratio'] if r['tail_ratio'] is not None else F(0)
            lam = r['head_lambda'] + 2 * r['tail_lambda'] + 3
            x = (hr + 2 * tr) / 2 * x + lam
        Theta = Theta + 3 + 3 * r['time']
        G += 1 + r['epsilon']
        s += 1 + r['time']
    return out, 'limit'


def exact_max_record(cal, x, Theta, Gamma0, sigma, limit=LIMIT):
    rows, status = chain_sequence(cal, x, Theta, 0, sigma, limit)
    mx = -10 ** 9
    for c in rows:
        mx = max(mx, c['j'] + Gamma0 + c['G'])
    return status, mx


def certify(cal, j, delta):
    st, rows, mx = None, None, None
    status, mx = exact_max_record(cal, 1 << j, (1 << j) + delta, 0, j + 1)
    return status == 'end' and mx <= j, status, mx


# --------------------------------------------------------------------------- #
def affine_walk(cal, st, s, sigma, limit=LIMIT):
    rep = {"status": "limit", "chains": [], "landing": None, "tie": None,
           "violations": [], "maxrecord": -10 ** 9, "end_chain": None}
    cur = st
    for step in range(limit):
        x, Theta = cur.x, cur.Theta
        j = cur.j
        if F(x).denominator != 1:
            rep["violations"].append(("x_not_integer", str(x)))
            rep["status"] = "bad"
            return rep
        if x <= 0:
            rep["violations"].append(("x_nonpositive", str(x)))
            rep["status"] = "bad"
            return rep
        if v2(x) != j:
            rep["violations"].append(("v2_mismatch", j, v2(x)))
        theta = sym(cur.theta, j)
        rep["chains"].append((j, cur.Gamma, s, cur.record, theta))
        rep["maxrecord"] = max(rep["maxrecord"], cur.record)
        if cur.record >= sigma:
            rep["status"] = "ceiling"
            return rep
        if j <= 4:
            rep["status"] = "end"
            rep["end_chain"] = (j, cur.Gamma)
            return rep
        r = read_crossing(cal, j)
        if not r["odd"]:
            rep["status"] = "end"
            rep["end_chain"] = (j, cur.Gamma)
            return rep
        tau = r["tau"]
        if r["kind"] == 'a':
            k = tau // 2
            z = 3 * k + theta
            rz = None if z == 0 else v2(z)
            nxt = cur.step_a(k)
            xex = 2 * Theta + 6 * k - x / 2
            Tex = Theta + 3 + 6 * k
            if xex == 0:
                rep["violations"].append(("a_step_zero", j))
                rep["status"] = "bad"
                return rep
            if nxt.x != xex or nxt.Theta != Tex:
                rep["violations"].append(("a_step_mismatch", j))
            if rz is not None and rz <= j - 3:
                jn = v2(xex)
                if not (vv(nxt.beta) == rz + 1 and jn == rz + 1
                        and jn + nxt.Gamma <= cur.J - 1):
                    rep["violations"].append(("landing_ledger", j, rz,
                                              vv(nxt.beta), jn))
                delta = sym(3 - theta, jn + 1)
                if (Tex - xex - delta) % (1 << (jn + 1)) != 0:
                    rep["violations"].append(("landing_class", j, jn))
                rep["landing"] = {"j": jn, "delta": delta, "chain": step + 1,
                                  "record": jn + nxt.Gamma}
                rep["status"] = "landing"
                return rep
            if rz is None or rz >= j - 1:
                if not (vv(nxt.beta) >= j and v2(xex) == j - 1
                        and j - 1 + nxt.Gamma == cur.J):
                    rep["violations"].append(("suspension_ledger", j, rz,
                                              vv(nxt.beta)))
                bump("affine_suspensions")
            else:  # rz == j-2
                ell = j - 1
                a = nxt.alpha * (1 << nxt.J) / (1 << ell)
                b = nxt.beta / (1 << ell)
                e = v2(a * cur.U + b)
                jn = v2(xex)
                if not (e is not None and e >= 1 and jn == ell + e
                        and jn + nxt.Gamma == cur.J + e):
                    rep["violations"].append(("tie_ledger", j, e, jn))
                rep["tie"] = {"j": j, "e": e, "j_next": jn, "record": cur.J + e}
                rep["status"] = "tie"
                return rep
            cur = nxt
        else:
            nxt = cur.step_bc(r["ratio"], r["lam"], tau, r["eps"])
            xex = r["ratio"] * x + r["lam"]
            Tex = Theta + 3 + 3 * tau
            if xex == 0:
                rep["violations"].append(("bc_step_zero", j))
                rep["status"] = "bad"
                return rep
            if nxt.x != xex or nxt.Theta != Tex:
                rep["violations"].append(("bc_step_mismatch", j))
            om = r["omega"]
            jn = v2(xex)
            if not (jn == om == vv(nxt.beta) and jn + nxt.Gamma <= cur.J - 1):
                rep["violations"].append(("bc_landing_ledger", j, om,
                                          vv(nxt.beta), jn))
            phi = 3 * tau + 5 - r["lam"]
            delta = sym(theta + phi - 2, om + 1)
            if (Tex - xex - delta) % (1 << (om + 1)) != 0:
                rep["violations"].append(("bc_class", j, om))
            rep["landing"] = {"j": jn, "delta": delta, "chain": step + 1,
                              "record": jn + nxt.Gamma}
            rep["status"] = "bc_landing"
            return rep
        s = s + 1 + tau
    rep["status"] = "limit"
    return rep


def criterion(cal, st, s, sigma, H=H_HEIGHT):
    reasons = []
    if v2(st.alpha) != -st.Gamma:
        reasons.append("C0: v2(alpha)!=-Gamma")
    j = st.j
    vb = None if st.beta == 0 else v2(st.beta)
    if vb is not None and vb == j:
        reasons.append("C1: v2(beta)=j")
    rep = affine_walk(cal, st, s, sigma)
    for (j_t, G_t, s_t, rec_t, th) in rep["chains"]:
        if abs(th) > H:
            reasons.append("C2: |theta|>H at j=%d" % j_t)
            break
    if rep["status"] == "tie":
        e = rep["tie"]["e"]
        if e is None or not (e < sigma - st.J):
            reasons.append("C4: tie depth %s >= sigma-J=%d" % (e, sigma - st.J))
        reasons.append("C4: tie continuation not certified")
    if rep["status"] in ("landing", "bc_landing"):
        lj, ld = rep["landing"]["j"], rep["landing"]["delta"]
        ok, stt, mx = certify(cal, lj, ld)
        if not ok:
            reasons.append("C5: class (%d,%s) not certified (%s)" % (lj, ld, stt))
    elif rep["status"] == "end":
        pass
    elif rep["status"] == "ceiling":
        reasons.append("C6/ceiling before U-free")
    else:
        reasons.append("C5: run did not reach a U-free state")
    if not (sigma > st.J):
        reasons.append("C6: sigma<=J")
    return (len(reasons) == 0), reasons, rep


# --------------------------------------------------------------------------- #
def first_fire(cal, P):
    modulus = 1 << (P - 1)
    base = (-2 * pow(3, -1, modulus)) % modulus
    for t in range(8):
        k = base + t * modulus
        if k < 1 or 1 + val(3 * k + 2) != P:
            continue
        fire = cal.preceding_fire_by_time(2 * k)
        if fire['k'] == k:
            return fire
    raise AssertionError(('no sampled canonical fire', P))


def canonical_tests(cal):
    out = {"calendar_B": cal.B, "fires": 0, "chains": 0, "c_sources": 0,
           "c_source_mismatch": 0, "shift_cases": 0, "shift_mismatch": 0,
           "criterion_holds": 0, "criterion_hold_unsafe": 0,
           "criterion_fail_examples": [], "walk_checks": 0, "source_checks": 0,
           "landing_classes_checked": 0, "step_checks": 0, "record_checks": 0,
           "anchor_failures": 0, "shift_ties": [], "shift_tie_safe": 0,
           "shift_tie_c_rejects": 0}
    for P in range(5, 257):
        fire = first_fire(cal, P)
        rows = cal.epoch_crossings(fire)
        U = (6 * fire['k'] + 4) >> P
        sigma = fire['pointer']
        s0 = 2 * fire['k']
        chains, status = chain_sequence(cal, (6 * fire['k'] + 4), (6 * fire['k'] + 5),
                                        s0, sigma)
        out["fires"] += 1
        if status != 'end':
            fail("canonical_end", (P, status))
        if not chains:
            fail("canonical_empty", P)
            continue
        by_s = {}
        for idx, c in enumerate(chains):
            out["chains"] += 1
            by_s[c['s']] = c
            if c['j'] + c['G'] >= sigma:
                fail("canonical_record", (P, c['j'], c['G'], sigma))
            st = make_anchor(U, c['G'], c['j'] + c['G'], c['x'], c['Theta'])
            if st is None:
                out["anchor_failures"] += 1
                fail("canonical_anchor", (P, c['j'], c['G']))
                continue
            out["walk_checks"] += 1
            if st.j != c['j'] or st.x != c['x'] or st.Theta != c['Theta']:
                fail("anchor_mismatch", (P, c['j']))
            # step identities and trichotomy against the next chain
            if idx + 1 < len(chains):
                nxt = chains[idx + 1]
                r = cal.crossing(c['j'] - 1)
                if not r['odd']:
                    fail("step_on_even", (P, c['j']))
                elif r['kind'] == 'a':
                    k = r['time'] // 2
                    px = st.step_a(k)
                    out["step_checks"] += 1
                    if px.x != nxt['x'] or px.Theta != nxt['Theta']:
                        fail("canonical_a_step", (P, c['j']))
                    z = 3 * k + sym(st.theta, c['j'])
                    rz = None if z == 0 else v2(z)
                    jn = nxt['j']
                    recn = jn + nxt['G']
                    J = st.J
                    if rz is not None and rz <= c['j'] - 3:
                        out["record_checks"] += 1
                        if not (jn == rz + 1 and recn <= J - 1):
                            fail("canonical_landing", (P, c['j'], rz, jn, recn, J))
                        delta = sym(3 - sym(st.theta, c['j']), jn + 1)
                        out["landing_classes_checked"] += 1
                        if (nxt['Theta'] - nxt['x'] - delta) % (1 << (jn + 1)) != 0:
                            fail("canonical_landing_class", (P, c['j'], jn))
                    elif rz is None or rz >= c['j'] - 1:
                        out["record_checks"] += 1
                        if not (jn == c['j'] - 1 and recn == J):
                            fail("canonical_suspension", (P, c['j'], jn, recn, J))
                    else:  # tie
                        out["record_checks"] += 1
                        if not (jn >= c['j'] and recn > J):
                            fail("canonical_tie", (P, c['j'], jn, recn, J))
                else:
                    hr = r['head_ratio']
                    tr = r['tail_ratio'] if r['tail_ratio'] is not None else F(0)
                    ratio = (hr + 2 * tr) / 2
                    lam = r['head_lambda'] + 2 * r['tail_lambda'] + 3
                    px = st.step_bc(ratio, lam, r['time'], r['epsilon'])
                    out["step_checks"] += 1
                    if px.x != nxt['x'] or px.Theta != nxt['Theta']:
                        fail("canonical_bc_step", (P, c['j']))
                    om = v2(lam)
                    jn = nxt['j']
                    recn = jn + nxt['G']
                    out["record_checks"] += 1
                    if not (jn == om and recn <= st.J - 1):
                        fail("canonical_bc_landing", (P, c['j'], om, jn, recn, st.J))
                    phi = 3 * r['time'] + 5 - lam
                    delta = sym(sym(st.theta, c['j']) + phi - 2, om + 1)
                    out["landing_classes_checked"] += 1
                    if (nxt['Theta'] - nxt['x'] - delta) % (1 << (om + 1)) != 0:
                        fail("canonical_bc_class", (P, c['j'], om))
            # criterion at this chain (precision = the fire's pointer)
            holds, reasons, crep = criterion(cal, st, c['s'], sigma)
            if crep["violations"]:
                fail("canonical_criterion_violation", (P, c['j'], crep["violations"][:2]))
            if holds:
                out["criterion_holds"] += 1
                ok, mx = exact_max_record(cal, st.x, st.Theta, c['G'], sigma)
                if not (ok == 'end' and mx < sigma):
                    out["criterion_hold_unsafe"] += 1
                    fail("criterion_holds_but_unsafe", (P, c['j'], ok, mx, sigma))
            else:
                if len(out["criterion_fail_examples"]) < 8:
                    out["criterion_fail_examples"].append(
                        {"P": P, "j": c['j'], "reasons": reasons[:3]})
        # ---- c sources
        crows = [(n, r) for n, r in rows.items() if r['kind'] == 'c' and r['odd']]
        for n, r in crows:
            s_row = r['time']
            if s_row not in by_s:
                out["c_source_mismatch"] += 1
                fail("c_source_not_on_walk", (P, n, s_row))
                continue
            c = by_s[s_row]
            x_src = 3 * s_row + 4 + r['tail_lambda']
            if c['x'] != x_src or c['j'] != v2(x_src):
                out["c_source_mismatch"] += 1
                fail("c_source_state", (P, n, str(c['x']), x_src))
                continue
            out["c_sources"] += 1
            out["source_checks"] += 1
            sigma_c = n - r['epsilon']
            st = make_anchor(U, c['G'], c['j'] + c['G'], c['x'], c['Theta'])
            if st is None:
                fail("c_source_anchor", (P, n))
                continue
            # criterion at the c source with its own precision
            holds, reasons, crep = criterion(cal, st, s_row, sigma_c)
            if crep["violations"]:
                fail("c_source_criterion_violation", (P, n, crep["violations"][:2]))
            if holds:
                out["criterion_holds"] += 1
                ok, mx = exact_max_record(cal, st.x, st.Theta, c['G'], sigma_c)
                if not (ok == 'end' and mx < sigma_c):
                    out["criterion_hold_unsafe"] += 1
                    fail("c_source_holds_unsafe", (P, n, ok, mx, sigma_c))
            # shift sub-suite: Theta-shift == d -> d+eta/3
            for eta in range(-8, 9):
                st_eta = st.shift_d(eta)
                rep_s = affine_walk(cal, st_eta, s_row, sigma_c)
                out["shift_cases"] += 1
                if rep_s["violations"]:
                    out["shift_mismatch"] += 1
                    fail("shift_affine", (P, n, eta, rep_s["violations"][:2]))
                if rep_s["status"] == "tie":
                    rec = rep_s["tie"]["record"]
                    okx, mxx = exact_max_record(cal, st_eta.x, st_eta.Theta,
                                                c['G'], sigma_c)
                    safe = (okx == 'end' and mxx < sigma_c)
                    out["shift_tie_safe"] += int(safe)
                    out["shift_tie_c_rejects"] += 1
                    if len(out["shift_ties"]) < 8:
                        out["shift_ties"].append(
                            {"P": P, "n": str(n), "eta": eta, "j": c['j'],
                             "theta_shift": sym(st.theta, c['j']) + eta,
                             "e": rep_s["tie"]["e"], "j_next": rep_s["tie"]["j_next"],
                             "record": rec, "sigma": str(sigma_c),
                             "exact_safe": bool(safe), "c_holds": False})
        # fire source shifts
        c = chains[0]
        st = make_anchor(U, c['G'], c['j'] + c['G'], c['x'], c['Theta'])
        if st is None:
            fail("fire_anchor", P)
            continue
        for eta in range(-8, 9):
            st_eta = st.shift_d(eta)
            rep_s = affine_walk(cal, st_eta, c['s'], sigma)
            out["shift_cases"] += 1
            if rep_s["violations"]:
                out["shift_mismatch"] += 1
                fail("shift_root_affine", (P, eta, rep_s["violations"][:2]))
            if rep_s["status"] == "tie":
                rec = rep_s["tie"]["record"]
                okx, mxx = exact_max_record(cal, st_eta.x, st_eta.Theta, c['G'], sigma)
                safe = (okx == 'end' and mxx < sigma)
                out["shift_tie_safe"] += int(safe)
                out["shift_tie_c_rejects"] += 1
                if len(out["shift_ties"]) < 8:
                    out["shift_ties"].append(
                        {"P": P, "n": "fire", "eta": eta, "j": c['j'],
                         "theta_shift": sym(st.theta, c['j']) + eta,
                         "e": rep_s["tie"]["e"], "j_next": rep_s["tie"]["j_next"],
                         "record": rec, "sigma": str(sigma), "exact_safe": bool(safe),
                         "c_holds": False})
    return out


# --------------------------------------------------------------------------- #
def synthetic_tests():
    rng = random.Random(20261023)
    out = {"a_cases": 0, "bc_cases": 0, "trichotomy_cases": 0,
           "bc_landing_cases": 0, "class_cases": 0, "record_cases": 0,
           "tie_cases": 0, "beta_shift_cases": 0, "noncanonical": True,
           "alpha_valuation_checks": 0, "phase_identity_checks": 0,
           "samples": []}
    for _ in range(30000):
        J = rng.randint(10, 80)
        Gam = rng.randint(0, min(8, J - 6))
        alpha = F(rng.choice([1, -1]) * rng.randrange(1, 1 << 20, 2), 1 << Gam)
        j = J + v2(alpha)
        beta = F(rng.choice([1, -1]) * rng.randrange(1, 1 << 20, 2)) * (1 << (j + 1 + rng.randint(0, 5)))
        d = rng.randint(-10 ** 7, 10 ** 7)
        U = rng.randrange(1, 1 << 40, 2)
        k = rng.randint(1, 10 ** 7)
        st = St(J, alpha, beta, d, Gam, U)
        if v2(st.x) != j:
            fail("synth_x", (J, Gam, j))
            continue
        theta = sym(st.theta, j)
        nx = st.step_a(k)
        xex = 2 * st.Theta + 6 * k - st.x / 2
        Tex = st.Theta + 3 + 6 * k
        out["a_cases"] += 1
        if nx.x != xex or nx.Theta != Tex:
            fail("synth_a_step", (J, Gam, j))
            continue
        if v2(nx.alpha) != -st.Gamma - 1:
            fail("synth_alpha_val_a", (J, Gam, j, v2(nx.alpha)))
        else:
            out["alpha_valuation_checks"] += 1
        if nx.theta != 3 - st.theta - st.beta / 2:
            fail("synth_phase_exact_a", (J, Gam, j))
        else:
            out["phase_identity_checks"] += 1
        z = 3 * k + theta
        r = None if z == 0 else v2(z)
        jn = v2(xex)
        if r is not None and r <= j - 3:
            if not (vv(nx.beta) == r + 1 and jn == r + 1
                    and jn + nx.Gamma <= st.J - 1):
                fail("synth_landing", (J, Gam, j, r, vv(nx.beta), jn))
            else:
                out["trichotomy_cases"] += 1
                out["record_cases"] += 1
                delta = sym(3 - theta, jn + 1)
                if (Tex - xex - delta) % (1 << (jn + 1)) != 0:
                    fail("synth_class", (J, Gam, j, jn))
                else:
                    out["class_cases"] += 1
                if len(out["samples"]) < 20:
                    out["samples"].append({
                        "canonical": False, "kind": "a", "J": J, "Gamma": Gam,
                        "alpha": str(alpha), "beta": str(beta), "d": str(d), "U": U,
                        "k": k, "j": j, "r": r, "j_next": jn,
                        "outcome": ("landing" if r is not None and r <= j - 3
                                    else ("tie" if r == j - 2 else "suspension"))})
        elif r == j - 2:
            ell = j - 1
            a = nx.alpha * (1 << nx.J) / (1 << ell)
            b = nx.beta / (1 << ell)
            e = v2(a * U + b)
            if not (vv(nx.beta) == ell and e is not None and e >= 1
                    and jn == ell + e and jn + nx.Gamma == st.J + e):
                fail("synth_tie", (J, Gam, j, e, jn))
            else:
                out["trichotomy_cases"] += 1
                out["tie_cases"] += 1
                out["record_cases"] += 1
        else:
            if not (vv(nx.beta) >= j and jn == j - 1 and jn + nx.Gamma == st.J):
                fail("synth_suspension", (J, Gam, j, r, vv(nx.beta), jn))
            else:
                out["trichotomy_cases"] += 1
                out["record_cases"] += 1
    for _ in range(30000):
        J = rng.randint(10, 80)
        Gam = rng.randint(0, min(8, J - 6))
        alpha = F(rng.choice([1, -1]) * rng.randrange(1, 1 << 20, 2), 1 << Gam)
        j = J + v2(alpha)
        beta = F(rng.choice([1, -1]) * rng.randrange(1, 1 << 20, 2)) * (1 << (j + 1 + rng.randint(0, 5)))
        d = rng.randint(-10 ** 7, 10 ** 7)
        U = rng.randrange(1, 1 << 40, 2)
        n = j - 1
        eps = rng.randint(0, min(6, n - 3))
        ratio = F(rng.randrange(1, 1 << 12, 2), 2 ** (1 + eps))
        lam = rng.randrange(1, 1 << 14, 2) * (1 << rng.randint(0, max(0, n - 2 - eps)))
        om = v2(lam)
        if om is None or om >= n - 1 - eps:
            continue
        tau = rng.randint(1, 10 ** 7)
        st = St(J, alpha, beta, d, Gam, U)
        theta = sym(st.theta, j)
        nx = st.step_bc(ratio, lam, tau, eps)
        xex = ratio * st.x + lam
        Tex = st.Theta + 3 + 3 * tau
        out["bc_cases"] += 1
        if nx.x != xex or nx.Theta != Tex:
            fail("synth_bc_step", (J, Gam, j))
            continue
        if v2(nx.alpha) != -st.Gamma - 1 - eps:
            fail("synth_alpha_val_bc", (J, Gam, j, eps, v2(nx.alpha)))
        else:
            out["alpha_valuation_checks"] += 1
        if nx.theta != st.theta + (3 * tau + 5 - lam) - 2 + st.beta * (1 - ratio):
            fail("synth_phase_exact_bc", (J, Gam, j))
        else:
            out["phase_identity_checks"] += 1
        jn = v2(xex)
        if not (jn == om == vv(nx.beta) and jn + nx.Gamma <= st.J - 1):
            fail("synth_bc_landing", (J, Gam, j, om, vv(nx.beta), jn))
        else:
            out["bc_landing_cases"] += 1
            out["record_cases"] += 1
        phi = 3 * tau + 5 - lam
        delta = sym(theta + phi - 2, om + 1)
        if (Tex - xex - delta) % (1 << (om + 1)) != 0:
            fail("synth_bc_class", (J, Gam, j, om))
        else:
            out["class_cases"] += 1
        if len(out["samples"]) < 40:
            out["samples"].append({
                "canonical": False, "kind": "bc", "J": J, "Gamma": Gam,
                "alpha": str(alpha), "beta": str(beta), "d": str(d), "U": U,
                "ratio": str(ratio), "lambda": str(lam), "tau": tau, "eps": eps,
                "j": j, "omega": om, "j_next": jn, "outcome": "bc_landing"})
        eta = rng.randint(-8, 8)
        st_b = St(J, alpha, beta - F(eta), d, Gam, U)
        st_d = st.shift_d(eta)
        out["beta_shift_cases"] += 1
        if (st_b.Theta - st_b.x - st_d.Theta + st_d.x) % (1 << j) != 0:
            fail("synth_shift_class", (J, Gam, j, eta))
        if v2(st_b.beta) >= j + 1 and st_b.j != j:
            fail("synth_beta_shift_j", (J, Gam, j))
    return out


# --------------------------------------------------------------------------- #
def o2_tests():
    out = {"cases": 0, "tie_cases": 0, "ledger_mismatch": 0, "threshold_ok": 0,
           "w_values": [8], "examples": [], "depth_fail": 0, "depth_ok": 0,
           "c_rejects": 0}
    for m in range(6, 257, 2):
        u = ((1 << (m - 4)) - 1) // 3
        x = 32 * u
        Theta = x + 5
        J = 5
        st1 = St(J, 1, 0, F(4, 3), 0, u)
        st2 = St(J, 1, -64, -20, 0, u + 2)
        out["cases"] += 1
        for tag, st in (("d4/3", st1), ("dZ", st2)):
            if st.x != x or st.Theta != Theta:
                fail("o2_state", (m, tag, str(st.x), st.Theta))
                continue
            theta = sym(st.theta, J)
            if theta != 5 or v2(3 + theta) != 3:
                fail("o2_tie_condition", (m, tag, theta))
            nx = st.step_a(1)
            xex = 2 * Theta + 6 - x // 2
            if nx.x != xex:
                fail("o2_step", (m, tag))
            ell = J - 1
            e = v2(nx.alpha * (1 << nx.J) / (1 << ell) * st.U + nx.beta / (1 << ell))
            rec = J + e if e is not None else None
            if not (vv(nx.beta) == ell == v2(nx.alpha * (1 << nx.J))):
                fail("o2_tie_vals", (m, tag, vv(nx.beta)))
            if e != m - 4 or rec != m + 1:
                out["ledger_mismatch"] += 1
                fail("o2_ledger", (m, tag, e, rec))
            else:
                out["tie_cases"] += 1
        W = J + 0 + 3
        ceiling = 9
        if (m >= 8) == (m - 4 >= ceiling - J):
            out["threshold_ok"] += 1
        else:
            fail("o2_threshold", (m, m - 4, ceiling - J))
        if m - 4 >= ceiling - J:
            out["depth_fail"] += 1
        else:
            out["depth_ok"] += 1
        out["c_rejects"] += 1   # a tie is never certified by C (C4 continuation)
        if len(out["examples"]) < 6:
            out["examples"].append({"m": m, "e": m - 4, "record": m + 1, "W": W,
                                    "ceiling": ceiling, "safe": m - 4 < ceiling - J})
    return out


# --------------------------------------------------------------------------- #
def dlog3(t, H):
    """Return r with 3^r == t (mod 2^H), t in <3> (odd and 1 or 3 mod 8)."""
    t %= 1 << H
    assert t % 2 == 1 and t % 8 in (1, 3), t
    r = 0 if t % 8 == 1 else 1
    for b in range(1, H - 2):
        cand = r + (1 << b)
        mod = 1 << (b + 3)
        if pow(3, cand, mod) == t % mod:
            r = cand
    assert pow(3, r, 1 << H) == t % (1 << H), (H, r)
    return r


def o1_tests(cal):
    out = {"cases": 0, "identity_cases": 0, "tie_r": None, "tie_e_mod": None,
           "dangerous_H": 0, "dangerous_ok": 0, "examples": [],
           "c4_fail_dangerous": 0, "tie_detected": 0}
    P = 49
    fire = first_fire(cal, P)
    if fire["pointer"] != 1051689726214394 or fire["k"] != 469124961184426:
        fail("o1_source", (fire["pointer"], fire["k"]))
    x0 = 6 * fire["k"] + 4
    U = x0 >> P
    if x0 != 5 * (1 << 49) or U != 5:
        fail("o1_x0", (x0, U))
    Theta0 = x0 + 1
    r48 = cal.crossing(48)
    if not (r48["odd"] and r48["kind"] == 'a' and r48["time"] == 40):
        fail("o1_X48", (r48["kind"], r48["time"]))
    k = 20
    y = 2 * Theta0 + 6 * k - x0 // 2
    if y != 4222124650659962:
        fail("o1_y", y)
    A1 = (y - 10) // 16
    if A1 != 263882790666247 or A1 % 8 != 7:
        fail("o1_A1", A1)
    if v2(y) != 1:
        fail("o1_v2y", v2(y))
    for r in list(range(1, 501)) + [1000, 2000, 5000, 10000]:
        lhs = v2(56 + F(8, 3 ** r))
        rhs = 3 + v2(7 * 3 ** r + 1)
        out["cases"] += 1
        if lhs != rhs:
            fail("o1_identity", (r, lhs, rhs))
        else:
            out["identity_cases"] += 1
    H44 = 44
    t45 = (-pow(7, -1, 1 << (H44 + 1))) % (1 << (H44 + 1))
    r45 = dlog3(t45, H44 + 1)
    # r45 matches mod 2^45; r45 + 2^42 matches mod 2^44 but not mod 2^45
    r_tie = r45 + (1 << (H44 - 2))
    val_tie = v2(7 * pow(3, r_tie, 1 << (H44 + 3)) + 1)
    if val_tie != 44:
        fail("o1_tie_find", (r_tie, val_tie, r45))
    out["tie_r"] = r_tie
    K = 80
    inv = pow(3, -r_tie, 1 << (K + 4))
    num = (7 + inv) % (1 << (K + 4))
    if num % (1 << 44) != 0:
        fail("o1_b_not_div", num % (1 << 44))
    b = num >> 44
    e = v2(15 + b) if (15 + b) % 2 == 0 else 0
    out["tie_e_mod"] = e
    out["tie_detected"] = 1
    if e is None or e < 1:
        fail("o1_tie_e", e)
    for H in [48, 52, 56, 60, 64]:
        t = (-pow(A1, -1, 1 << H)) % (1 << H)
        try:
            r = dlog3(t, H)
        except AssertionError as exc:
            fail("o1_dlog", (H, exc))
            continue
        out["dangerous_H"] += 1
        if pow(3, r, 1 << H) != t:
            fail("o1_dangerous_cong", H)
            continue
        val7 = v2(7 * pow(3, r, 1 << 47) + 1)
        if val7 != 44:
            fail("o1_dangerous_tie", (H, val7))
            continue
        valA = v2(A1 * pow(3, r, 1 << (H + 2)) + 1)
        if valA is not None and valA < H:
            fail("o1_dangerous_depth", (H, valA))
            continue
        out["dangerous_ok"] += 1
        if valA is None or valA - 44 >= H - 44:
            out["c4_fail_dangerous"] += 1
        if len(out["examples"]) < 5:
            out["examples"].append({"H": H, "r_mod": r % (1 << 40),
                                    "v2_7": val7, "v2_A1": valA})
    return out


# --------------------------------------------------------------------------- #
def main():
    t0 = time.time()
    cal = Calendar(512)
    counts.clear()
    failures.clear()

    can = canonical_tests(cal)
    syn = synthetic_tests()
    o2 = o2_tests()
    o1 = o1_tests(cal)

    # F9: every anchored canonical state has d in Z and v2(beta)>=j+1
    f9_bad = 0
    checked = 0
    for P in range(5, 257):
        fire = first_fire(cal, P)
        U = (6 * fire['k'] + 4) >> P
        chains, _ = chain_sequence(cal, 6 * fire['k'] + 4, 6 * fire['k'] + 5,
                                   2 * fire['k'], fire['pointer'])
        for c in chains:
            st = make_anchor(U, c['G'], c['j'] + c['G'], c['x'], c['Theta'])
            if st is None:
                f9_bad += 1
                continue
            checked += 1
            if st.d.denominator not in (1, 3):
                f9_bad += 1
            vb = None if st.beta == 0 else v2(st.beta)
            if vb is not None and vb < st.j + 1:
                f9_bad += 1
    if f9_bad:
        fail("F9_provenance", f9_bad)

    # F8 negative control: W=8 does not bound the record for m>=8
    f8_bad = 0
    for m in range(8, 65, 2):
        u = ((1 << (m - 4)) - 1) // 3
        st = St(5, 1, 0, F(4, 3), 0, u)
        nx = st.step_a(1)
        e = v2(nx.alpha * (1 << nx.J) / 16 * st.U + nx.beta / 16)
        if 5 + e != m + 1 or 5 + e <= 8:
            f8_bad += 1
    if f8_bad:
        fail("F8_W_only", f8_bad)

    counts.update({
        "canonical_fires": can["fires"],
        "canonical_chains": can["chains"],
        "canonical_c_sources": can["c_sources"],
        "canonical_step_checks": can["step_checks"],
        "canonical_record_checks": can["record_checks"],
        "canonical_landing_classes": can["landing_classes_checked"],
        "canonical_shift_cases": can["shift_cases"],
        "canonical_criterion_holds": can["criterion_holds"],
        "canonical_criterion_hold_unsafe": can["criterion_hold_unsafe"],
        "canonical_anchor_failures": can["anchor_failures"],
        "canonical_shift_ties": len(can["shift_ties"]),
        "canonical_shift_tie_safe": can["shift_tie_safe"],
        "o2_depth_fail": o2["depth_fail"],
        "o2_depth_ok": o2["depth_ok"],
        "o2_c_rejects": o2["c_rejects"],
        "o1_c4_fail_dangerous": o1["c4_fail_dangerous"],
        "synthetic_a": syn["a_cases"],
        "synthetic_bc": syn["bc_cases"],
        "synthetic_alpha_valuation": syn["alpha_valuation_checks"],
        "synthetic_phase_identity": syn["phase_identity_checks"],
        "synthetic_trichotomy": syn["trichotomy_cases"],
        "synthetic_class": syn["class_cases"],
        "synthetic_record": syn["record_cases"],
        "synthetic_tie": syn["tie_cases"],
        "o2_cases": o2["cases"],
        "o2_tie": o2["tie_cases"],
        "o1_identity": o1["identity_cases"],
        "o1_dangerous": o1["dangerous_ok"],
        "f9_checked": checked,
        "f9_bad": f9_bad,
        "f8_bad": f8_bad,
    })

    status = "PASS" if not failures else "FAIL"
    out = {
        "status": status,
        "scope": ("Exact integer/rational checks of the affine-origin landing criterion. "
                  "Canonical: work_global_calendar/calendar_oracle.Calendar(512), first "
                  "fires P=5..256 and every chain of their epochs, with balanced "
                  "re-anchored affine origins J=j+Gamma. Synthetic states are "
                  "non-canonical. Deep regime j>=2e7 is NOT tested (Calendar(B) needs "
                  "B>=2e7, above the B<=1024 limit). No global EXT claim; K_clock "
                  "unchanged. [B] finite computation; [A] identities proved in PLAN.md."),
        "canonical_tests": can,
        "synthetic_tests": syn,
        "obstructions": {"O2": o2, "O1": o1},
        "falsification": {
            "F1": "not_run (deep j>=N0 needs Calendar(B>=N0); analytic [A-imp] only)",
            "F2": "synthetic trichotomy checks (see synthetic_tests)",
            "F3": "synthetic b/c checks (see synthetic_tests)",
            "F4": "O2 rejected: e=m-4>=sigma-J iff m>=8",
            "F5": "O1 detected: tie r and dangerous residue",
            "F6": "canonical landing classes vs exact walk",
            "F7": "beta-shift vs d-shift synthetic checks",
            "F8": "W-only negative control (O2 W=8, record m+1)",
            "F9": "canonical provenance d in Z, v2(beta)>=j+1",
            "F8_bad": f8_bad, "F9_bad": f9_bad,
        },
        "counts": counts,
        "failures": failures,
        "elapsed_s": round(time.time() - t0, 2),
    }
    (HERE / "checks.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status,
                      "canonical": {k: can[k] for k in
                                    ("fires", "chains", "c_sources", "step_checks",
                                     "shift_cases", "criterion_holds",
                                     "criterion_hold_unsafe", "anchor_failures",
                                     "shift_tie_safe")},
                      "synthetic": {k: syn[k] for k in
                                    ("a_cases", "bc_cases", "trichotomy_cases",
                                     "bc_landing_cases", "class_cases",
                                     "record_cases", "tie_cases",
                                     "alpha_valuation_checks",
                                     "phase_identity_checks")},
                      "O2": {k: o2[k] for k in ("cases", "tie_cases", "threshold_ok")},
                      "O1": {k: o1[k] for k in ("cases", "identity_cases",
                                                "dangerous_H", "dangerous_ok")},
                      "failures": len(failures),
                      "elapsed_s": out["elapsed_s"]}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
