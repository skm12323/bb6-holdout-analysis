#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""verify_gateway.py -- Direction G (repeated gateway chains) exact checks.

Implements the test list of work_landing_symbolic/gateway/PLAN.md (I1..I16, C1..C8).
Exact integer / rational arithmetic only.

Canonical data: work_global_calendar/calendar_oracle.Calendar(512) for the small range,
and the canonical lambda-walk table D:/math_cc_astra/deep1/table_1000000.pkl otherwise.
Every synthetic construction is labelled non-canonical in the json.

Run:  python -B work_landing_symbolic/gateway/verify_gateway.py
Writes: work_landing_symbolic/gateway/checks.json
"""
import sys, json, pickle, time, random, traceback
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TABPATH = Path(r'D:/math_cc_astra/deep1/table_1000000.pkl')
sys.path.insert(0, str(ROOT / 'work_global_calendar'))
sys.path.insert(0, str(ROOT / 'work_global_ext' / 'route_c'))

import os
NMAX = 64
STEPCAP = 400
ENUM_MAX_J = int(os.environ.get('GW_ENUM_MAX_J', '27'))   # full Bad_j enumeration bound


def v2(x):
    if x == 0:
        return 10 ** 9
    return (x & -x).bit_length() - 1


def symres(e, bits):
    M = 1 << bits
    r = e % M
    return r - M if r > M // 2 else r


def clsmod(f, mod):
    """2-adic class of a rational with odd denominator, modulo mod."""
    p, q = f.numerator, f.denominator
    if q % 2 == 0:
        return None
    return (p * pow(q, -1, mod)) % mod


# ---------------------------------------------------------------- data source
class Data:
    def __init__(self):
        from fdata import small_full
        self.S = small_full(1024)
        with open(TABPATH, 'rb') as f:
            d = pickle.load(f)
        self.tau = d['tau']; self.eps = d['eps']; self.odd = d['odd']
        self.lY = d['lY']; self.lA = d['lA']; self.typ = d['typ']
        self.N = len(self.tau)
        self.TYP = [chr(self.typ[n]) for n in range(NMAX)]
        self.TAU = [self.tau[n] for n in range(NMAX)]
        self.EPS = [self.eps[n] for n in range(NMAX)]
        self.ODD = [bool(self.odd[n]) for n in range(NMAX)]
        self.LAM = [self.lA[n] + 2 * self.lY[n] + 3 for n in range(NMAX)]
        self.CPR = [None] * NMAX
        for n in range(min(NMAX, 1024)):
            r = self.S[n]
            if r['odd'] and r['typ'] != 'a':
                self.CPR[n] = r['x'][0]
                assert r['x'][1] == self.LAM[n], ('lambda mismatch', n)


DATA = None


def row(n):
    """Full-range canonical row (n < 10**6)."""
    return {"kind": chr(DATA.typ[n]), "odd": bool(DATA.odd[n]),
            "tau": DATA.tau[n], "eps": DATA.eps[n],
            "lam": DATA.lA[n] + 2 * DATA.lY[n] + 3}


# ---------------------------------------------------------------- exact walks
def walk(j0, delta, path=False):
    """Exact walk from the representative (2^j0, 2^j0+delta) at precision j0+1."""
    j = j0
    x = 1 << j
    Th = x + delta
    G = 0
    mx = j0
    chain = [(j0, delta % (1 << (j0 + 1)), 0, j0, None, None)] if path else None
    for _ in range(STEPCAP):
        if j <= 4:
            return ('end', mx, chain)
        n = j - 1
        if n >= NMAX:
            return ('nodata', mx, chain)
        if not DATA.ODD[n]:
            return ('end', mx, chain)
        jprev = j
        kindprev = DATA.TYP[n]
        if kindprev == 'a':
            k = DATA.TAU[n] // 2
            x2 = 2 * Th + 6 * k - x // 2
            Th = Th + 3 + 6 * k
            G += 1
        else:
            c = DATA.CPR[n]
            if c is None:
                return ('nodata', mx, chain)
            x2 = c * (x >> j) + DATA.LAM[n]
            Th = Th + 3 + 3 * DATA.TAU[n]
            G += 1 + DATA.EPS[n]
        if x2 == 0:
            return ('zero', mx, chain)
        j = v2(x2)
        x = x2
        if j + G > mx:
            mx = j + G
        if path:
            chain.append((j, (Th - x) % (1 << (j + 1)), G, j + G, jprev, kindprev))
    return ('limit', mx, chain)


def certify(j, delta):
    st, mx, _ = walk(j, delta)
    return st == 'end' and mx <= j


BAD = {}
GENERIC_BAD = {}
REFUTED = []


def enumerate_bad(j):
    """All delta mod 2^{j+1} with certify(j,delta) false (full enumeration, tight loop)."""
    if j in BAD:
        return BAD[j]
    if j <= 4 or not DATA.ODD[j - 1]:
        # j<=4: X(j-1) even -> immediate end.  Even crossing at j-1: same.
        BAD[j] = set()
        return BAD[j]
    TYP = DATA.TYP; TAU = DATA.TAU; EPS = DATA.EPS; ODD = DATA.ODD
    LAM = DATA.LAM; CPR = DATA.CPR
    S = set()
    ap = S.add
    for d in range(1 << (j + 1)):
        jj = j
        x = 1 << jj
        Th = x + d
        G = 0
        mx = jj
        ok = True
        while True:
            if jj <= 4:
                break
            nn = jj - 1
            if not ODD[nn]:
                break
            if TYP[nn] == 'a':
                k = TAU[nn] >> 1
                x = 2 * Th + 6 * k - (x >> 1)
                Th = Th + 3 + 6 * k
                G += 1
            else:
                x = CPR[nn] * (x >> jj) + LAM[nn]
                Th = Th + 3 + 3 * TAU[nn]
                G += 1 + EPS[nn]
            if x == 0:
                ok = False
                break
            jj = (x & -x).bit_length() - 1
            if jj + G > mx:
                mx = jj + G
        if not (ok and mx <= j):
            ap(d)
    BAD[j] = S
    return S


def tie_class(j):
    k = DATA.TAU[j - 1] // 2
    return (pow(2, j - 2, 1 << (j - 1)) - 3 * k) % (1 << (j - 1))


# ---------------------------------------------------------------- result store
RES = {
    "status": "PASS",
    "scope": "",
    "environment": {},
    "canonical_tests": {},
    "synthetic_tests": {},
    "conclusions": {},
    "failures": [],
    "not_run": [],
    "controls": {},
    "refuted_claims": [],
    "timing": {},
}
CNT = {}


def cnt(name, ok, detail=None):
    c = CNT.setdefault(name, {"checked": 0, "failed": 0, "examples": []})
    c["checked"] += 1
    if not ok:
        c["failed"] += 1
        if len(c["examples"]) < 5:
            c["examples"].append(detail)
    return ok


def fail(tag, detail):
    RES["failures"].append({"check": tag, "detail": detail})


# ============================================================ canonical tests
def canonical_tests():
    from calendar_oracle import Calendar
    t0 = time.time()
    cal = Calendar(512)
    out = {}

    # C1  oracle vs table on the reachable small range
    mism = 0; nn = 0
    for n in range(512):
        try:
            r = cal.crossing(n)
        except Exception:
            break
        nn += 1
        rw = row(n)
        if (r['kind'] != rw['kind'] or bool(r['odd']) != rw['odd']
                or r['time'] != rw['tau'] or r['epsilon'] != rw['eps']):
            mism += 1
    out["oracle_vs_table"] = {"n": nn, "mismatch": mism}
    cnt("C1.oracle", mism == 0, out["oracle_vs_table"])

    # C2  X(4) odd type a, tau=2, k=1
    r4 = cal.crossing(4)
    out["X4"] = {"kind": r4['kind'], "odd": bool(r4['odd']), "tau": r4['time'], "k": r4['time'] // 2}
    cnt("C2.X4", r4['kind'] == 'a' and r4['odd'] and r4['time'] == 2, out["X4"])

    # C3  X(6132), four lifts
    n = 6132
    rw = row(n)
    tau = rw['tau']; eps = rw['eps']; lamv = rw['lam']; om = v2(lamv)
    sigma = n - eps
    r16 = (5 - (3 * tau + 3 - (1 << om))) % 16
    rec = {"n": n, "kind": rw['kind'], "odd": rw['odd'], "tau": tau, "eps": eps,
           "lam": lamv, "omega": om, "sigma": sigma, "lambdaY": DATA.lY[n],
           "tie_theta_mod16": r16, "lifts": []}
    okc = True
    for s in range(4):
        th = symres(r16 + 16 * s, 6)
        cls5 = (th + 3 * tau + 3 - (1 << om)) % 64
        tie_ok = (cls5 % 16 == 5)
        M = 2 * th + 12 + 6 * tau - lamv // 2
        j2 = v2(M)
        d2 = (th + 6 + 3 * tau + 3 * DATA.TAU[4] - M) % (1 << (j2 + 1))
        below = (j2 < sigma - 1)
        rec_ok = (j2 + 2 + eps <= n)
        bad = enumerate_bad(j2) if 4 < j2 <= ENUM_MAX_J else None
        notbad = (d2 not in bad) if bad is not None else None
        cert = certify(j2, d2)
        ok = tie_ok and below and rec_ok and (notbad is not False) and cert
        okc = okc and ok
        rec["lifts"].append({"theta_T": th, "delta_5_mod64": cls5, "tie": tie_ok,
                             "M_B": str(M), "j2": j2, "delta2": str(d2),
                             "j2_lt_sigma_minus_1": below, "record_descent": rec_ok,
                             "in_Bad": notbad, "certify": cert})
        cnt("C3.X6132_lift", ok, {"theta_T": th, "j2": j2, "d2": d2})
    rec["all_ok"] = okc
    out["X6132"] = rec
    cnt("C3.X6132", okc, {"n": n})

    # C4  every omega=5 odd type-c crossing with n < 10**6, four lifts each
    ROWS = {m: row(m) for m in range(DATA.N)}
    rows = [m for m in ROWS if ROWS[m]['odd'] and ROWS[m]['kind'] == 'c' and v2(ROWS[m]['lam']) == 5]
    c4 = {"crossings": len(rows), "cases": 0, "ok": 0, "j2_hist": {}, "fail": 0,
          "first": rows[:5], "last": rows[-3:]}
    for m in rows:
        tau_m = ROWS[m]['tau']; eps_m = ROWS[m]['eps']; lam_m = ROWS[m]['lam']
        sig = m - eps_m
        base16 = (5 - (3 * tau_m + 3 - 32)) % 16
        for s in range(4):
            th = symres(base16 + 16 * s, 6)
            cls5 = (th + 3 * tau_m + 3 - 32) % 64
            M = 2 * th + 12 + 6 * tau_m - lam_m // 2
            j2 = v2(M)
            d2 = (th + 6 + 3 * tau_m + 3 * DATA.TAU[4] - M) % (1 << (j2 + 1))
            c4["cases"] += 1
            c4["j2_hist"][j2] = c4["j2_hist"].get(j2, 0) + 1
            good = (cls5 % 16 == 5) and (j2 < sig - 1) and (j2 + 2 + eps_m <= m) and certify(j2, d2)
            if good and j2 <= ENUM_MAX_J:
                stx, mxx, chx = walk(j2, d2, path=True)
                good = all(c[0] <= ENUM_MAX_J + 1 for c in chx)
                if not good:
                    fail("C4.closure", {"n": m, "j2": j2, "maxj": max(c[0] for c in chx)})
            if good:
                c4["ok"] += 1
            else:
                c4["fail"] += 1
                fail("C4", {"n": m, "theta_T": th, "j2": j2, "delta2": d2, "cls5": cls5,
                            "sigma": sig})
            cnt("C4.omega5_lift", good, {"n": m, "theta_T": th})
    out["omega5_family"] = c4
    cnt("C4.omega5", c4["fail"] == 0, c4)

    # C5  small-regime constants
    tmax = max(DATA.TAU[n] for n in range(27))
    lmax = max(DATA.LAM[n] for n in range(27))
    kmax = max(DATA.TAU[n] // 2 for n in range(27) if DATA.ODD[n] and DATA.TYP[n] == 'a')
    emax = max(DATA.EPS[n] for n in range(27))
    out["small_constants"] = {"max_tau_n_le26": tmax, "max_lam_n_le26": lmax,
                              "max_k_odd_a_n_le26": kmax, "max_eps_n_le26": emax}
    cnt("C5.consts", tmax == 20 and lmax == 89 and kmax == 10 and emax == 3, out["small_constants"])

    # C6  Bad_j: full enumeration for every odd parameter 5..27 (even crossings are trivially empty)
    bads = {}
    GENERIC_BAD.clear()
    for j in range(5, ENUM_MAX_J + 1):
        s_j = sorted(enumerate_bad(j))
        if DATA.ODD[j - 1] and DATA.TYP[j - 1] == 'a':
            bads[j] = s_j
        elif s_j:
            GENERIC_BAD[j] = s_j
    out["Bad_j_counts"] = {str(j): len(v) for j, v in bads.items()}
    out["generic_counts"] = {str(j): len(v) for j, v in GENERIC_BAD.items()}
    expect4 = [5, 8, 12, 14, 22, 24, 27]
    ok6 = all(len(bads.get(j, [])) == 4 for j in expect4) and len(bads.get(17, [])) == 8
    ok6 = ok6 and (len(GENERIC_BAD) == 0)
    struct = {}
    struct_ok = True
    for j, v in bads.items():
        groups = {}
        for d in v:
            groups.setdefault(d % (1 << (j - 1)), []).append(d)
        struct[str(j)] = {str(r): len(g) for r, g in groups.items()}
        want = 2 if j == 17 else 1
        struct_ok = struct_ok and (len(groups) == want) and all(len(g) == 4 for g in groups.values())
        if j != 17:
            struct_ok = struct_ok and (list(groups)[0] == tie_class(j))
    out["Bad_j_structure"] = struct
    out["Bad_j_tie_class"] = {str(j): str(tie_class(j)) for j in bads}
    cnt("C6.Bad_j_counts", ok6, out["Bad_j_counts"])
    cnt("C6.Bad_j_struct", struct_ok, struct)

    # C7  representative dynamics from the canonical bad classes.
    #     Vertices: canonical bad classes.  Successor: first later chain whose class is bad
    #     (Bad_j for j<=27, certify for larger j).  Also record parameter jumps.
    def is_bad_state(j, cls):
        if j <= ENUM_MAX_J:
            return cls in enumerate_bad(j)
        if j < NMAX:
            return not certify(j, cls)
        return None                      # no data

    t0g = time.time()
    nodes = {}
    frontier = [(j, d) for j, v in bads.items() for d in v]
    jumps_ok = True
    maxj = 0
    closure27 = True
    nodata = []
    steps = 0
    while frontier:
        u = frontier.pop()
        if u in nodes:
            continue
        (j, d) = u
        st, mx, chain = walk(j, d, path=True)
        steps += 1
        for a, b in zip(chain, chain[1:]):
            kind = b[5]
            if kind in ('b', 'c'):
                okstep = b[0] < a[0]
            else:
                # a-step: the gateway step at parameter 5 is excluded (jump to m = v2(x2))
                okstep = (b[0] <= a[0] + 3) if a[0] != 5 else True
            if not okstep:
                jumps_ok = False
                fail("I13.step_bound", {"from": a[0], "to": b[0], "kind": kind,
                                        "start": str((j, d))})
        mj = max(c[0] for c in chain)
        maxj = max(maxj, mj)
        if mj > ENUM_MAX_J:
            closure27 = False
        nxt = None
        for (jj, cls, G, r, _pj, _k) in chain[1:]:
            isb = is_bad_state(jj, cls)
            if isb is None:
                nodata.append({"start": str((j, d)), "j": jj})
                break
            if isb:
                nxt = (jj, cls)
                break
        nodes[u] = {"status": st, "maxrec": mx, "maxj": mj, "succ": nxt}
        if nxt is not None and nxt not in nodes:
            frontier.append(nxt)
    # cycle detection on the (possibly partial) successor map
    color = {}
    cyc = []
    def dfs(uu):
        color[uu] = 1
        w = nodes.get(uu, {}).get("succ")
        if w is not None:
            if w in nodes:
                if color.get(w) == 1:
                    cyc.append((uu, w))
                elif color.get(w, 0) == 0:
                    dfs(w)
        color[uu] = 2
    for uu in list(nodes):
        if color.get(uu, 0) == 0:
            dfs(uu)
    out["bad_graph"] = {
        "vertices": len(nodes),
        "edges": sum(1 for v in nodes.values() if v["succ"] is not None),
        "cycles": [{"from": str(a), "to": str(b)} for a, b in cyc],
        "max_parameter": maxj,
        "nodata": nodata[:10],
        "successors": {str(k): (str(v["succ"]) if v["succ"] else None) for k, v in nodes.items()},
        "maxrec": {str(k): v["maxrec"] for k, v in nodes.items()},
    }
    cnt("I13.step_bound", jumps_ok, {})
    # The ORIGINAL PLAN claim "once j<=27 all later parameters are <=27" is FALSE.
    # It is recorded as a refuted claim with its witness, NOT as a pass/fail assertion
    # of the current theorem (the theorem now states the corrected window below).
    st_w, mx_w, ch_w = walk(17, 163822, path=True)
    REFUTED.append({
        "claim": "PLAN (iii) original: 'once j<=27, all later parameters are <=27'",
        "status": "refuted; superseded by the corrected window checked below",
        "witness_start": [17, 163822],
        "witness_chain": [[c[0], c[1] % 64] for c in ch_w],
        "max_parameter_over_36_bad_classes": maxj,
    })
    RES["controls"]["closure27_refuted"] = REFUTED[-1]
    # corrected closure [B]: every representative walk from the 36 bad classes stays <= 30,
    # and 28/29/30 carry no bad classes:
    #   j=29,30 read the even crossings X(28),X(29) -> Bad empty by definition;
    #   j=28 reads the odd b crossing X(27) (omega=6) and sends the class to parameter 6;
    #   Bad_6 = empty (full enumeration) => Bad_28 = empty.
    ok_window = (maxj <= ENUM_MAX_J + 3) and (len(enumerate_bad(6)) == 0)         and (not DATA.ODD[28]) and (not DATA.ODD[29])
    out["window30"] = {"max_parameter": maxj, "Bad6": len(enumerate_bad(6)),
                       "X28_odd": DATA.ODD[28], "X29_odd": DATA.ODD[29],
                       "ok": ok_window}
    cnt("I13.window30", ok_window, out["window30"])
    out["closure27"] = {"holds": closure27, "max_parameter": maxj}

    cnt("C7.acyclic", len(cyc) == 0, {"cycles": len(cyc), "vertices": len(nodes)})
    out["graph_time"] = round(time.time() - t0g, 1)

    # C8  record law (R): needs a walk through two gateways
    r_ok = 0; r_chk = 0; r_bad = []
    for u in list(nodes):
        j0, d0 = u
        st, mx, chain = walk(j0, d0, path=True)
        ties = [i for i, c in enumerate(chain) if c[0] == 5 and c[1] % 16 == 5]
        if len(ties) >= 2:
            i, kk = ties[0], ties[1]
            m = chain[i + 1][0]
            drec = chain[kk][3] - chain[i][3]
            r_chk += 1
            if drec >= m - 4:
                r_ok += 1
            else:
                r_bad.append({"start": str((j0, d0)), "m": m, "delta_rec": drec})
                fail("C8", {"start": str((j0, d0)), "m": m, "delta_rec": drec})
        # single-gateway instances: check the descent of the gateway block itself
        elif len(ties) == 1:
            i = ties[0]
            if i + 1 < len(chain):
                m = chain[i + 1][0]
                if m < 5:
                    fail("C8.m", {"start": str((j0, d0)), "m": m})
                cnt("C8.m_ge_5", m >= 5, {"m": m})
    out["record_law_R"] = {"checked": r_chk, "ok": r_ok, "bad": r_bad,
                           "note": "needs a representative walk through two gateways; "
                                   "0 such canonical instances found" if r_chk == 0 else "ok"}
    cnt("C8.R", len(r_bad) == 0, r_bad)

    RES["timing"]["canonical"] = round(time.time() - t0, 1)
    return out


# ============================================================ synthetic tests
def make_a_gateway(jp, k, up, Dp):
    xp = (1 << jp) * up
    Tp = xp + Dp
    x5 = 2 * Tp + 6 * k - xp // 2
    T5 = Tp + 3 + 6 * k
    x2 = 2 * T5 + 6 - x5 // 2
    T2 = T5 + 9
    return dict(xp=xp, Tp=Tp, x5=x5, T5=T5, x2=x2, T2=T2, D2=T2 - x2,
                MA=Tp + 12 + 9 * k, Dp=Dp)


def synth_a_gateway(count, bigcount=20):
    """I1-I4, I8 (Q=1) on synthetic non-canonical a-gateways."""
    res = {"checked": 0, "ids": {}, "control_outside_hypothesis": {"n": 0, "record_fail": 0}}
    ids = {k: 0 for k in ("I1", "I2", "I3", "I4", "I4.record", "I8.Q1", "n")}
    random.seed(20261023)

    def one(jp, k):
        up = random.choice([1, 3, 5, 7, 9, random.getrandbits(60) | 1])
        Dp = 14 if k % 32 == 22 else 30
        s = make_a_gateway(jp, k, up, Dp)
        x2 = s['x2']; D2 = s['D2']; MA = s['MA']
        d = {}
        d["I1"] = (x2 == MA + s['xp'] // 4)
        d["I2"] = (D2 == -3 * k - s['xp'] // 4)
        j2 = v2(x2)
        d["I3"] = (v2(MA) == j2) if v2(MA) <= jp - 3 else None
        if j2 <= jp - 3:
            d["I4"] = ((D2 + 3 * k) % (1 << (j2 + 1)) == 0)
            d["I4.record"] = (j2 + 2 <= jp - 1)
        else:
            d["I4"] = None; d["I4.record"] = None
        m = j2
        if m < 40:
            C = (s['T5'] - s['x5']) % (1 << (m + 1))
            lhs = D2 % (1 << (m + 1))
            rhs = ((15 - C) * pow(3, -1, 1 << (m + 1)) + (1 << m)) % (1 << (m + 1))
            d["I8.Q1"] = (lhs == rhs)
        else:
            d["I8.Q1"] = None
        return d, j2

    for _ in range(count):
        jp = random.randint(7, 400)
        k = random.choice([6, 22]) + 32 * random.randint(0, 10 ** 6)
        d, j2 = one(jp, k)
        ids["n"] += 1
        for key in ("I1", "I2", "I8.Q1", "I3", "I4", "I4.record"):
            if d.get(key) is not None:
                ids[key] += 1
                cnt(key if key.startswith("I") else "I4", d[key], {"jp": jp, "k": k})
        if d.get("I4.record") is None:
            res["control_outside_hypothesis"]["n"] += 1
            if j2 + 2 > jp - 1:
                res["control_outside_hypothesis"]["record_fail"] += 1
    for _ in range(bigcount):
        jp = random.randint(10 ** 4, 10 ** 5)
        k = random.choice([6, 22]) + 32 * random.randint(0, 10 ** 6)
        d, j2 = one(jp, k)
        ids["n"] += 1
        for key in ("I1", "I2"):
            ids[key] += 1
            cnt(key, d[key], {"jp": jp})
    res["checked"] = ids["n"]
    res["ids"] = ids
    return res


def make_bc_gateway(jT, sigma, tau, lamp, thT, uT, cpar):
    ThT = (1 << jT) * uT + thT
    x5 = cpar * uT + lamp
    T5 = ThT + 3 + 3 * tau
    x2 = 2 * T5 + 6 - x5 // 2
    # M_B uses the exact defect D_T = theta_T (mod 2^{j_T+1}), NOT Theta_T:
    #   2*Theta_T = 2^{j_T+1}*u_T + 2*D_T  ->  the 2^{j_T+1}*u_T term is carried separately.
    M = 2 * thT + 12 + 6 * tau - lamp // 2
    return dict(ThT=ThT, x5=x5, T5=T5, x2=x2, T2=T5 + 9, M=M, D2=T5 + 9 - x2,
                D5=T5 - x5)


def synth_bc_gateway(count):
    """I5-I7 on synthetic non-canonical b/c gateways (omega=5)."""
    res = {"checked": 0, "ids": {}}
    ids = {k: 0 for k in ("I5", "I6", "I7", "I7.uT", "I4.bc_record", "n")}
    random.seed(777)
    for _ in range(count):
        jT = random.randint(16, 300)
        sigma = random.randint(8, jT - 2)
        eps = jT - 1 - sigma                       # eps = n_T - sigma
        if eps < 1:
            continue
        tau = random.randint(2, 10 ** 4)
        lamY = random.randint(0, 3 * tau + 1)
        lamp = 3 * tau + 4 + lamY
        if v2(lamp) != 5:
            continue
        c = (random.getrandbits(80) | 1) << sigma
        uT = random.choice([1, 3, 5, 17]) * (random.getrandbits(40) * 2 + 1)
        Phi = 3 * tau + 5 - lamp
        base = (5 - Phi + 2) % 16                  # theta_T making theta_5 = 5 mod 16
        thT = base - 16 * ((base + 8) // 16)       # representative in [-8,8)
        s = make_bc_gateway(jT, sigma, tau, lamp, thT, uT, c)
        ids["n"] += 1
        I5 = (s['x2'] == s['M'] + uT * ((1 << (jT + 1)) - c // 2)) and (s['x2'] == 2 * s['T5'] + 6 - s['x5'] // 2)
        ids["I5"] += 1
        cnt("I5", I5, {"jT": jT})
        if s['M'] % (1 << (sigma - 1)) != 0:
            j2 = v2(s['M'])
            ids["I6"] += 1
            cnt("I6", j2 == v2(s['x2']) and j2 < sigma - 1, {"jT": jT, "sigma": sigma, "j2": j2})
            d2 = s['D2'] % (1 << (j2 + 1))
            f = (thT + 6 + 3 * tau + 3 * DATA.TAU[4]) % (1 << (j2 + 1))
            ids["I7"] += 1
            cnt("I7", d2 == (f - s['M']) % (1 << (j2 + 1)), {"jT": jT})
            u2 = uT + 2
            s2 = make_bc_gateway(jT, sigma, tau, lamp, thT, u2, c)
            d2b = s2['D2'] % (1 << (j2 + 1))
            ids["I7.uT"] += 1
            cnt("I7.ut", d2b == d2, {"jT": jT})
            ids["I4.bc_record"] += 1
            cnt("I4.bc_record", j2 + 2 + eps <= jT - 1, {"jT": jT, "j2": j2, "eps": eps})
    res["checked"] = ids["n"]
    res["ids"] = ids
    return res


def synth_description(count):
    """I8: denominator, height, lift bit, (D1) on real synthetic b/c gateways."""
    res = {"checked": 0, "den_ok": 0, "height_ok": 0, "D1": 0, "D1_bad": 0}
    random.seed(4242)
    for _ in range(count):
        r = random.randint(1, 40)
        Q = 3 ** r
        jT = random.randint(16, 120)
        sigma = random.randint(8, jT - 2)
        tau = random.randint(2, 10 ** 4)
        lamY = random.randint(0, 3 * tau + 1)
        lamp = 3 * tau + 4 + lamY
        if v2(lamp) != 5:
            continue
        c = (random.getrandbits(40) | 1) << sigma
        uT = random.getrandbits(30) * 2 + 1
        Phi = 3 * tau + 5 - lamp
        base = (5 - Phi + 2) % 16
        thT = base - 16 * ((base + 8) // 16)
        s = make_bc_gateway(jT, sigma, tau, lamp, thT, uT, c)
        m = v2(s['x2'])
        D5 = s['D5']; D2 = s['D2']
        # rational description of D5 matching it modulo 2^{m+1}, with 3 not dividing C
        C = (D5 % (1 << (m + 1))) * Q % (1 << (m + 1))
        step = 1 << (m + 1)
        for _t in range(3):
            if C % 3 != 0:
                break
            C += step
        ok_den = (F(15 * Q - C, 3 * Q).denominator == 3 * Q)
        c5 = F(C, Q)
        ok_h = abs(5 - c5 / 3) <= 5 + abs(c5) / 3
        res["checked"] += 1
        if ok_den:
            res["den_ok"] += 1
        if ok_h:
            res["height_ok"] += 1
        cnt("I8.den", ok_den, {"Q": str(Q), "C": C})
        cnt("I8.height", ok_h, {"Q": str(Q), "C": C})
        rhs = ((15 * Q - C) * pow(3 * Q, -1, 1 << (m + 1)) + (1 << m)) % (1 << (m + 1))
        lhs = D2 % (1 << (m + 1))
        if lhs == rhs:
            res["D1"] += 1
        else:
            res["D1_bad"] += 1
            fail("I8.D1", {"Q": str(Q), "m": m, "lhs": str(lhs), "rhs": str(rhs)})
        cnt("I8.D1", lhs == rhs, {"Q": str(Q), "m": m})
    return res


def synth_iteration(count):
    """I9, I10, I10.tie on exact rationals."""
    res = {"checked": 0}
    random.seed(99)
    for _ in range(count):
        c0 = F(random.randint(-10 ** 6, 10 ** 6), random.choice([1, 3, 9, 27, 81]))
        t = random.randint(1, 20)
        c = c0
        ok9 = True
        for _i in range(t):
            C = c.numerator; Q = c.denominator
            c = F(15 * Q - C, 3 * Q)
            ok9 = ok9 and (c == 5 - F(C, Q) / 3)
        closed9 = F(15, 4) + (c0 - F(15, 4)) * F((-1) ** t, 3 ** t)
        cnt("I9", ok9 and (c == closed9), {"c0": str(c0), "t": t})
        c = c0
        for _i in range(t):
            c = c / 3 - 2
        cnt("I10", c == -3 + (c0 + 3) * F(1, 3 ** t), {"c0": str(c0), "t": t})
        c = F(random.randint(0, 15) + 16 * random.randint(-100, 100),
              random.choice([1, 3, 9, 27, 7, 11]))
        if clsmod(c, 16) == 5:
            cnt("I10.tie", clsmod(c / 3 - 2, 16) == 5 and clsmod(5 - c / 3, 16) == 14,
                {"c": str(c)})
        res["checked"] += 1
    ok_orbit = True
    c = F(5)
    for t in range(61):
        ok_orbit = ok_orbit and (c == -3 + 8 * F(1, 3 ** t)) and (clsmod(c, 16) == 5)
        c = c / 3 - 2
    cnt("I10.orbit5", ok_orbit, {})
    return res


def synth_height(count):
    """I12."""
    res = {"checked": 0, "ok": 0}
    random.seed(5)
    for _ in range(count):
        h = F(random.choice([0, 1, 2, 4, 5, 15, 100]), random.choice([1, 3, 9]))
        s = F(random.randint(-30, 30), random.choice([1, 3, 9, 27]))
        x = h
        ok = True
        for _i in range(50):
            xn = 5 + (x + abs(s)) / 3
            ok = ok and (abs(xn) <= 5 + (abs(x) + abs(s)) / 3)
            x = xn
        bound = max(h, F(15)) if abs(s) <= h else None
        if bound is not None:
            ok = ok and (x <= bound + F(1, 10 ** 6))
        res["checked"] += 1
        if ok:
            res["ok"] += 1
        cnt("I12", ok, {"h": str(h), "s": str(s)})
    return res


def synth_closure():
    """I13: |M| bound for j <= 27 implies m <= 27 (non-canonical theta)."""
    res = {"checked": 0, "ok": 0, "max_tau": None, "max_lam": None}
    random.seed(11)
    res["max_tau"] = max(DATA.TAU[n] for n in range(27))
    res["max_lam"] = max(DATA.LAM[n] for n in range(27))
    for j in range(5, 28):
        n = j - 1
        if not DATA.ODD[n]:
            continue
        for _ in range(200):
            th = random.randint(-(1 << (j - 1)) + 1, 1 << (j - 1))
            if DATA.TYP[n] == 'a':
                Mabs = abs(th + 12 + 9 * (DATA.TAU[n] // 2))
                bound = (1 << j) + 102
            else:
                Mabs = abs(2 * th + 12 + 6 * DATA.TAU[n] - DATA.LAM[n] // 2)
                bound = (1 << j) + 177
            if Mabs == 0:
                # M == 0: the successor parameter is the correction's valuation (j-2), <= 27
                m = j - 2
                res["zero_M"] = res.get("zero_M", 0) + 1
                ok = (m <= 27)
            else:
                m = v2(Mabs)
                ok = (m <= 27) and (Mabs < (1 << 28)) and (Mabs <= bound)
            res["checked"] += 1
            if ok:
                res["ok"] += 1
            cnt("I13", ok, {"j": j, "bits": (Mabs.bit_length() if Mabs else 0), "m": m})
    return res


def synth_entry(count=5000):
    """I14: the a-gateway entry congruence is exactly k = 6 (mod 16)."""
    res = {"checked": 0, "canonical_preimages": None}
    random.seed(31415)
    for _ in range(count):
        k = random.randrange(1, 10 ** 6)
        exists = (v2(3 * k + 14) == 4) or (v2(3 * k + 30) == 4)
        cnt("I14", exists == (k % 16 == 6), {"k": k})
        res["checked"] += 1
    # canonical realisation: the (5,5)-preimage classes at j=17 must land at 5 with the tie class
    pre = []
    for d in sorted(enumerate_bad(17)):
        st, mx, ch = walk(17, d, path=True)
        if len(ch) > 1 and ch[1][0] == 5:
            pre.append({"delta": d, "class_at_5": ch[1][1] % 64, "tie": ch[1][1] % 16 == 5})
    res["canonical_preimages"] = pre
    cnt("I14.preimage", len(pre) == 4 and all(x["tie"] for x in pre), pre)
    return res


def synth_o1():
    """I10/O1S: orbit and threshold arithmetic, exact integers."""
    A = 263882790666247
    sigma = 1051689726214394
    ok_A = (A % 8 == 7) and (A + 1 < (1 << 48))
    ok_pow = ((A + 1) ** 5) < (1 << 240)
    ok3 = 3 ** 5 < (1 << 8)
    thr_num = 5 * (sigma - 53)
    r_min = thr_num // 8 + 1
    tight = (240 + 8 * (r_min - 1)) < 5 * (sigma - 5)
    tight2 = (240 + 8 * r_min) >= 5 * (sigma - 5)
    out = {"A_mod8": A % 8, "A_plus_1_lt_2_48": ok_A, "A_plus_1_pow5_lt_2_240": ok_pow,
           "3_pow5_lt_2_8": ok3, "sigma": sigma, "r_min_claimed_by_O1": 657306078883964,
           "r_min_computed": r_min, "threshold_tight_at_r_min_minus_1": tight,
           "threshold_tight_from_r_min": tight2}
    cnt("O1S.pow5", ok_pow, {})
    cnt("O1S.r_min", r_min == 657306078883964, out)
    cnt("O1S.tight", tight and tight2, out)
    out["threshold_identity"] = {"240 + 5*(sigma-53)": 240 + 5 * (sigma - 53),
                                 "5*(sigma-5)": 5 * (sigma - 5)}
    # gateway-only map 5 -> 10/3
    c = 5 - F(5, 3)
    out["gateway_only_5_to"] = str(c)
    out["gateway_only_5_mod16"] = clsmod(c, 16)
    cnt("I10.bbb", c == F(10, 3) and clsmod(c, 16) == 14, out)
    return out


def synth_train(count=300):
    """I16: GATEWAY_TRAIN identities and the TRAIN valuation inequality."""
    out = {"algebra_checked": 0, "algebra_ok": 0, "trains_built": 0,
           "valuation_checked": 0, "valuation_ok": 0, "train_examples": []}
    random.seed(12345)
    # constructed genuine trains: k0=k1=6, T0 = 37 mod 256 (found by an offline residue search)
    for j in range(40):
        k0 = 6; k1 = 6; T0 = 37 + 256 * j
        y0 = -F(32, 2) + 2 * T0 + 6
        x1 = F(32, 4) + T0 + 15 + 6 * k0
        T1 = T0 + 12 + 6 * k0
        y1 = -x1 / 2 + 2 * T1 + 6
        x2 = x1 / 4 + T1 + 15 + 6 * k1
        T2 = T1 + 12 + 6 * k1
        y2 = -x2 / 2 + 2 * T2 + 6
        m0, m1, m2 = v2(int(y0)), v2(int(y1)), v2(int(y2))
        out["trains_built"] += 1
        out["valuation_checked"] += 1
        okv = v2(4 - k0 + 3 * k1) >= min(m0 - 2, m1 - 2, m2)
        out["valuation_ok"] += 1 if okv else 0
        out["train_examples"].append({"k0": k0, "k1": k1, "T0": T0, "m": [m0, m1, m2],
                                      "v2(4-k0+3k1)": v2(4 - k0 + 3 * k1)})
        cnt("I16.TRAIN", okv, {"k0": k0, "T0": T0})
    for _ in range(count):
        x0 = random.choice([32, 64, 96]) * random.choice([1, 3, 5, 7])
        T0 = random.randint(10, 10 ** 6)
        k0 = random.randint(1, 100)
        k1 = random.randint(1, 100)
        y0 = -F(x0, 2) + 2 * T0 + 6
        x1 = F(x0, 4) + T0 + 15 + 6 * k0
        T1 = T0 + 12 + 6 * k0
        y1 = -x1 / 2 + 2 * T1 + 6
        x2 = x1 / 4 + T1 + 15 + 6 * k1
        T2 = T1 + 12 + 6 * k1
        y2 = -x2 / 2 + 2 * T2 + 6
        out["algebra_checked"] += 1
        ok1 = (4 * y2 - 5 * y1 + y0 == 12 * (4 - k0 + 3 * k1))
        ok2 = (y1 - y0 / 4 == T0 + 21 + 9 * k0)
        if ok1 and ok2:
            out["algebra_ok"] += 1
        cnt("I16.algebra", ok1 and ok2, {"x0": x0, "T0": T0})
        m0 = v2(int(y0)); m1 = v2(int(y1)); m2 = v2(int(y2))
        if (y0.denominator == 1 and y1.denominator == 1 and y2.denominator == 1
                and m0 >= 5 and m1 >= 5 and m2 >= 5 and v2(int(x1)) == 5 and v2(int(x2)) == 5):
            out["trains_built"] += 1
            out["valuation_checked"] += 1
            okv = v2(4 - k0 + 3 * k1) >= min(m0 - 2, m1 - 2, m2)
            if okv:
                out["valuation_ok"] += 1
            cnt("I16.TRAIN", okv, {"k0": k0, "k1": k1})
    return out


# ============================================================ main
def main():
    t00 = time.time()
    global DATA
    DATA = Data()
    RES["environment"] = {"script": str(Path(__file__).resolve()),
                          "table": str(TABPATH),
                          "calendar": "work_global_calendar/calendar_oracle.Calendar(512)",
                          "nmax": NMAX, "enum_max_j": ENUM_MAX_J}
    RES["scope"] = (
        "Exact integer/rational checks of PLAN.md for direction G. Canonical: Calendar(512) for the "
        "reachable small range and the accepted canonical lambda-walk table (n<10**6) otherwise; "
        "X(6132) plus all 28 omega=5 odd type-c crossings with n<10**6, four lifts each; full Bad_j "
        "enumeration for every odd-a parameter 5<=j<=27. Synthetic (explicitly non-canonical): "
        "a-gateway and b/c-gateway states, rational descriptions, iteration/orbit, height recursion, "
        "closure bound, TRAIN algebra.")
    RES["not_run"] = [
        "work_r1r2's accepted 8,712 bad pairs are NOT reproduced: table_100000000.pkl is absent on "
        "this machine (D:/math_cc_astra/deep1/ holds only table_1000000.pkl). The local analogue is "
        "the 28 crossings x 4 lifts below.",
        "Bad_j for j>27 and the corresponding bad graph are not computed (enumeration cost grows as "
        "2^{j+1}); the repeated-chain theorem is only used inside j<=27.",
        "O1's canonical source (P=49 fire, pointer) is not re-verified here; only the threshold "
        "arithmetic and the exact factors are re-derived.",
        "TRAIN: no canonical 5,m,5,m,... train exists in the small canonical data; only the algebraic "
        "identities and constructed non-canonical chains are checked.",
    ]

    print("== canonical ==")
    RES["canonical_tests"] = canonical_tests()
    print("== synthetic ==")
    RES["synthetic_tests"]["a_gateway"] = synth_a_gateway(6000)
    RES["synthetic_tests"]["bc_gateway"] = synth_bc_gateway(4000)
    RES["synthetic_tests"]["description"] = synth_description(3000)
    RES["synthetic_tests"]["iteration"] = synth_iteration(1500)
    RES["synthetic_tests"]["height"] = synth_height(2000)
    RES["synthetic_tests"]["closure"] = synth_closure()
    RES["synthetic_tests"]["entry_congruence"] = synth_entry()
    RES["synthetic_tests"]["o1"] = synth_o1()
    RES["synthetic_tests"]["train"] = synth_train()

    RES["refuted_claims"] = REFUTED
    RES["conclusions"] = {k: {"checked": v["checked"], "failed": v["failed"],
                              "examples": v["examples"]} for k, v in sorted(CNT.items())}
    total_failed = sum(v["failed"] for v in CNT.values())
    RES["status"] = "PASS" if (total_failed == 0 and not RES["failures"]) else "FAIL"
    RES["timing"]["total"] = round(time.time() - t00, 1)

    print("\n--- per-conclusion counts ---")
    for k, v in sorted(CNT.items()):
        print("  %-18s checked=%-8d failed=%d" % (k, v["checked"], v["failed"]))
        if v["failed"]:
            print("     examples:", v["examples"][:3])
    print("\n--- failures ---")
    if RES["failures"]:
        for f in RES["failures"][:20]:
            print("  ", f)
    else:
        print("   none")
    ct = RES["canonical_tests"]
    print("\ncanonical summary:",
          json.dumps({"oracle_vs_table": ct.get("oracle_vs_table"),
                      "X4": ct.get("X4"),
                      "X6132_lifts": [{"theta_T": l["theta_T"], "j2": l["j2"], "d2": l["delta2"],
                                       "cert": l["certify"]} for l in ct["X6132"]["lifts"]],
                      "omega5": {k: v for k, v in ct["omega5_family"].items() if k != "first"},
                      "Bad_j_counts": ct.get("Bad_j_counts"),
                      "Bad_j_all_in_tie": ct.get("Bad_j_all_in_tie_class"),
                      "bad_graph": {k: v for k, v in ct["bad_graph"].items() if k != "successors"},
                      "record_law_R": ct.get("record_law_R")}, default=str))
    print("\nSTATUS:", RES["status"], " total failed:", total_failed,
          " time:", RES["timing"]["total"], "s")
    with open(HERE / "checks.json", "w", encoding="utf-8") as f:
        json.dump(RES, f, indent=1, default=str)
    print("wrote", HERE / "checks.json")
    return 0 if RES["status"] == "PASS" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        with open(HERE / "checks.json", "w", encoding="utf-8") as f:
            json.dump({"status": "ERROR", "traceback": traceback.format_exc()}, f, indent=1)
        sys.exit(2)
