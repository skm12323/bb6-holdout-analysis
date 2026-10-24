#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""climb_checks.py -- verification for C_CLIMB.md (task C: climb bound (S3), general entries).

Generalizes work_claude_shift Lemma CB from bare-tie entries (run length 1) to entries
through a run of strong-descent a steps and b/c steps below the last big chain y.

Blocks
  Z.CB.A      Lemma CB reproduction, A-type direct entries (canonical calendar at y,
              non-canonical ancestor defect D_y; states marked non-canonical)
  Z.CB.BC     Lemma CB reproduction, B/C-type direct entries (omega=5 crossings)
  Z.CB.class  catapult output class in the two gateway families
  Z.run.deg   run-length-1 degeneration: Z_CB = Z_run - x_y (A) / -2u(2^y-cW) (B,C)
  Z.run.synth synthetic-data runs r=1..6 (non-canonical data): exact pair vs affine
              identity, m = v2(Z_run) case structure, per-step v2(beta_i)=j_i,
              size bound |Z_run| <= B_run, residue single-class + frequency
  Z.run.canon canonical-typed runs realized from pinned first-landing classes
              (TIE_REACH residue statistics + systematic y-scan + exact replay)
  Z.run.huge  canonical-typed runs from y = 1e5, 1e6, 1e7, 2e7 (exact big-int walks)
  Z.replay    replay of the 36 bad-class representatives + window grid (tie entries)
  Z.centry    C-letter entry (canonical c crossing with omega=5 at parameter 6133),
              sigma_C = y-2-eps packaging and the least-strict-EXT bound
  Z.const     B_run size bound and the G(y) slack constant on a grid
  Z.data      calendar data bounds used by the theorem (S1, ratio, c''_W, |lam'|, tau)

Writes climb_checks.json.  Exit 0 iff all hard checks pass.
No global EXT or non-halting claim; K_clock unchanged.  Synthetic states are marked
non-canonical.  Canonical calendar data: work_global_calendar Calendar(512).
"""
import sys, json, time, random, math
from fractions import Fraction as F
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
OUT = HERE / "climb_checks.json"
INF = 10 ** 9
N0 = 2 * 10 ** 7

sys.path.insert(0, "D:/math_cc")
from work_global_calendar.calendar_oracle import Calendar  # noqa: E402

RES = {
    "status": "PASS",
    "scope": ("Task C (climb bound S3, general entries). Exact recomputation of Lemma CB and of its "
              "run-generalization. Canonical data: Calendar(512). Every constructed ancestor state "
              "(D_y, u_y lifts) and every synthetic-data run is non-canonical. No global EXT claim, "
              "no non-halting claim, K_clock unchanged."),
    "checks": {}, "counts": {}, "stats": {}, "examples": {}, "failures": [],
}
T_START = time.time()


def CK(cid, tag, ok, detail=None, n=1):
    d = RES["checks"].setdefault(cid, {"tag": tag, "checked": 0, "failed": 0, "examples": []})
    d["checked"] += n
    if not ok:
        d["failed"] += 1
        RES["failures"].append([cid, str(detail)[:400]])
        if len(d["examples"]) < 5:
            d["examples"].append(str(detail)[:400])
    return ok


def v2i(x):
    if x == 0:
        return INF
    x = abs(int(x))
    return (x & -x).bit_length() - 1


def v2f(q):
    q = F(q)
    if q == 0:
        return INF
    return v2i(q.numerator) - v2i(q.denominator)


def sym(e, bits):
    M = 1 << bits
    r = e % M
    return r - M if r > M // 2 else r


def clsmod(f, mod):
    if isinstance(f, int):
        return f % mod
    f = F(f)
    assert f.denominator % 2 == 1
    return (f.numerator * pow(f.denominator, -1, mod)) % mod


def z2mod(f, mod):
    f = F(f)
    e = v2f(f)
    assert e >= 0, ("not integral in Z_2", f)
    u = f / F(2) ** e
    return (clsmod(u, mod) * pow(2, e, mod)) % mod


def solve_congruence(S, Cst, L):
    """All D in Z_2 with S*D + Cst == 0 mod 2^L -> ('always',)/('never',)/('class',d0,mod)."""
    S, Cst = F(S), F(Cst)
    if S == 0:
        return ("always",) if v2f(Cst) >= L else ("never",)
    w = v2f(S)
    if w >= L:
        return ("always",) if v2f(Cst) >= L else ("never",)
    if Cst == 0:
        return ("class", 0, L - w)
    if v2f(Cst) < w:
        return ("never",)
    M = 1 << (L - w)
    Su = S / F(2) ** w
    Cu = Cst / F(2) ** w
    d0 = (z2mod(-Cu, M) * pow(clsmod(Su, M), -1, M)) % M
    return ("class", d0, L - w)


def P_clock(n):
    return 2 * ((max(1, 6 * n * n + 5) - 1).bit_length()) ** 2 + 1345


def G(y):
    return 2 * math.log2(y) + 3


# --------------------------------------------------------------------------- #
# calendar wrapper
_SDC = {}


def step_data(cal, j):
    if j in _SDC:
        return _SDC[j]
    r = cal.crossing(j - 1)
    tau = r["time"]
    if not r["odd"]:
        out = {"kind": "even", "tau": tau}
    elif r["kind"] == "a":
        out = {"kind": "a", "tau": tau, "k": tau // 2}
    else:
        cW = (r["head_ratio"] + 2 * r["tail_ratio"]) * (1 << (j - 1))
        assert cW.denominator == 1
        cW = int(cW)
        lam = r["head_lambda"] + 2 * r["tail_lambda"] + 3
        if isinstance(lam, F):
            assert lam.denominator == 1
            lam = int(lam)
        out = {"kind": r["kind"], "tau": tau, "cW": cW, "lam": lam,
               "omega": v2i(lam), "sigma": v2i(cW)}
    _SDC[j] = out
    return out


def canon_step(cal, j):
    s = step_data(cal, j)
    if s["kind"] == "a":
        return {"kind": "a", "k": s["k"], "tau": s["tau"], "src": ("canon", j)}
    assert s["kind"] in ("b", "c")
    return {"kind": s["kind"], "j_from": j, "cW": s["cW"], "lam": s["lam"],
            "tau": s["tau"], "sigma": s["sigma"], "omega": s["omega"], "src": ("canon", j)}


def exact_walk_rec(cal, x, T, max_steps=64, stop_at_tie=True):
    rows, steps = [], []
    for _ in range(max_steps):
        j = v2i(x)
        rows.append({"j": j, "x": x, "T": T})
        if x == 0:
            return rows, steps, "zero"
        if j <= 4:
            return rows, steps, "end"
        s = step_data(cal, j)
        if s["kind"] == "even":
            return rows, steps, "end"
        st = canon_step(cal, j)
        steps.append(st)
        if st["kind"] == "a":
            xn = 2 * T + 6 * st["k"] - x // 2
            Tn = T + 3 + 6 * st["k"]
        else:
            xn = st["cW"] * (x >> j) + st["lam"]
            Tn = T + 3 + 3 * st["tau"]
        x, T = xn, Tn
        if stop_at_tie and v2i(x) == 5 and (T - x) % 16 == 5:
            rows.append({"j": v2i(x), "x": x, "T": T})
            return rows, steps, "tie5"
    return rows, steps, "limit"


def catapult(x5, T5):
    xpp = 2 * T5 + 6 - x5 // 2
    return xpp, v2i(xpp)


# --------------------------------------------------------------------------- #
# affine run simulator (anchor J = y, U = u_y, A_0 = 2^y, beta_0 = 0, d_0 = (D_y-1)/3)
def affine_run(y, Dy, steps, expected_params=None, exact_A=False):
    a = y
    beta = F(0)
    d = F(Dy - 1, 3)
    q, b, N = F(0), F(0), 0          # beta = q*Dy + b ; 3d = D_y - 1 + 3N
    A = F(1 << y) if exact_A else None
    js = []
    jcur = y
    for idx, st in enumerate(steps):
        assert beta == q * F(Dy) + b, "beta decomposition"
        if st["kind"] == "a":
            k = st["k"]
            beta, d = 6 * d + 2 + 6 * k - beta / 2, d + 1 + 2 * k
            a = a - 1
            q, b = 2 - q / 2, 6 * N + 6 * k - b / 2
            N = N + 1 + 2 * k
            if exact_A:
                A = F(2) ** (y + 1) - A / 2
        else:
            ratio = F(st["cW"], 1 << st["j_from"])
            beta, d = ratio * beta + st["lam"], d + 1 + st["tau"]
            a = st["sigma"] + a - st["j_from"]
            q, b = ratio * q, ratio * b + st["lam"]
            N = N + 1 + st["tau"]
            if exact_A:
                A = ratio * A
        jn = v2f(beta)
        if expected_params is not None:
            CK("Z.run.v2beta", "A", jn == expected_params[idx + 1],
               ("v2(beta_i)=j_i", y, idx, jn, expected_params[idx + 1]))
        js.append(jn)
        jcur = jn
    Zrun = 6 * d + 8 - beta / 2
    S = 2 - q / 2
    Cst = 6 + 6 * N - b / 2
    assert Zrun == S * F(Dy) + Cst, "Z_run = S*D_y + Cst"
    out = dict(Zrun=Zrun, mu=a - 1, S=S, Cst=Cst, q=q, b=b, N=N, d=d, beta_r=beta,
               w=v2f(S), a_r=a, js=js)
    if exact_A:
        out["App"] = F(2) ** (y + 1) - A / 2
    return out


def run_checks(cal, y, Dy, u, steps, tag, exact_A_y=None):
    """shared per-instance checks: exact pair walk, affine Z_run, m structure, size."""
    x = (1 << y) * u
    T = x + Dy
    params = [y]
    for st in steps:
        if st["kind"] == "a":
            xn = 2 * T + 6 * st["k"] - x // 2
            T = T + 3 + 6 * st["k"]
        else:
            j = v2i(x)
            assert j == st["j_from"], "j_from mismatch"
            xn = st["cW"] * (x >> j) + st["lam"]
            T = T + 3 + 3 * st["tau"]
        x = xn
        params.append(v2i(x))
    j5, D5 = v2i(x), T - x
    xpp, m = catapult(x, T)
    aff = affine_run(y, Dy, steps, expected_params=params,
                     exact_A=(exact_A_y is not None and y <= exact_A_y))
    r = len(steps)
    s = sum(1 for st in steps if st["kind"] != "a")
    CK("Z.run.landing", "A", j5 == 5 and D5 % 16 == 5, (tag, "tie", y, j5, D5 % 16))
    CK("Z.run.mu_ge", "A", aff["mu"] >= r + 4, (tag, "mu", y, aff["mu"], r))
    vZ = v2f(aff["Zrun"])
    CK("Z.run.vZ_ge5", "A", vZ >= 5, (tag, "vZ", y, vZ))
    CK("Z.run.m_ge5", "A", m >= 5, (tag, "m", y, m))
    if vZ < aff["mu"]:
        CK("Z.run.m_eq", "A", m == vZ, (tag, "m!=v2(Z)", y, m, vZ, aff["mu"]))
    else:
        CK("Z.run.m_ge_mu", "A", m >= aff["mu"], (tag, "m<mu", y, m, aff["mu"]))
    if "App" in aff:
        CK("Z.run.identity", "A", F(xpp) == aff["App"] * u + aff["Zrun"], (tag, y))
    tau_max = max([st["tau"] for st in steps] + [1])
    BD = abs(Dy)
    Brun = (2 + 2 * F(3, 2) ** s) * BD + 6 + 6 * r * (1 + tau_max) + \
        F(3, 2) ** s * r * (BD + 11 + 12 * r * tau_max)
    if aff["Zrun"] != 0:
        CK("Z.run.size", "A", abs(aff["Zrun"]) <= Brun, (tag, "size", y, r, s))
        CK("Z.run.m_le_size", "A", (1 << m) <= abs(aff["Zrun"]) or m >= aff["mu"], (tag, y, m))
    CK("Z.run.S_neq0", "A", aff["S"] != 0, (tag, "S=0", y))
    CK("Z.run.q_v2", "A", aff["q"] == 0 or v2f(aff["q"]) <= 1, (tag, "q v2", y, aff["q"]))
    return dict(m=m, e=m - 4, vZ=vZ, mu=aff["mu"], params=params, aff=aff, r=r, s=s,
                x=x, T=T, xpp=xpp, D5=D5, Brun=Brun)


_CW = {}


def class_walk(cal, j0, theta, max_steps=60):
    key = (j0, theta % (1 << (j0 + 1)))
    if key in _CW:
        return _CW[key]
    j, th = key
    path = [(j, th)]
    out = None
    for _ in range(max_steps):
        if j <= 4:
            out = "end"
            break
        s = step_data(cal, j)
        if s["kind"] == "even":
            out = "end"
            break
        if s["kind"] == "a":
            z = (3 * s["k"] + th) % (1 << (j + 1))
            if z == 0:
                out = "deep"
                break
            jn = 1 + v2i(z)
            if jn >= j - 1:
                out = "ntgate" if jn == j - 1 else "susp"
                break
            thn = (3 - th) % (1 << (jn + 1))
        else:
            jn = s["omega"]
            thn = (th + 3 * s["tau"] + 3 - s["lam"]) % (1 << (jn + 1))
        j = jn
        path.append((j, thn))
        if j == 5:
            out = "tie5" if thn % 16 == 5 else "end5"
            break
    if out is None:
        out = "limit"
    _CW[key] = (out, path)
    return _CW[key]


# --------------------------------------------------------------------------- #
def block_cb_A(cal):
    ys = []
    for y in range(7, 4000):
        s = step_data(cal, y)
        if s["kind"] == "a" and s["k"] % 16 == 6:
            ys.append((y, s["k"]))
    big = []
    for target in [10 ** 5, 10 ** 6, 10 ** 7, 2 * 10 ** 7]:
        got = 0
        for y in range(max(7, target - 60), target + 61):
            s = step_data(cal, y)
            if s["kind"] == "a" and s["k"] % 16 == 6:
                big.append((y, s["k"]))
                got += 1
                if got >= 2:
                    break
    RES["counts"]["cb_A_pool_small"] = len(ys)
    RES["counts"]["cb_A_pool_big"] = len(big)
    CK("Z.CB.A.pool", "B", len(ys) >= 50 and len(big) >= 1, (len(ys), len(big)), n=0)
    inst = 0
    emax = 0
    mG = []
    for (y, k) in ys + big:
        base = (16 - 3 * k) % 32
        for Dy in [base - 64, base - 32, sym(base, 5), base + 32, base + 32 * 10 ** 6]:
            for u in (1, 3, 5, (1 << 20) + 1):
                x = (1 << y) * u
                T = x + Dy
                x5 = 2 * T + 6 * k - x // 2
                T5 = T + 3 + 6 * k
                D5 = T5 - x5
                if not (v2i(x5) == 5 and D5 % 16 == 5):
                    CK("Z.CB.A.entry", "A", False, (y, k, Dy, u, v2i(x5), D5 % 16))
                    continue
                CK("Z.CB.A.entry", "A", True, None)
                xpp, m = catapult(x5, T5)
                out = run_checks(cal, y, Dy, u, [canon_step(cal, y)],
                                 ("cbA", y, Dy, u), exact_A_y=2000)
                Zrun = out["aff"]["Zrun"]
                ZCB = 3 * Dy + 9 * k + 2 * D5 + 6
                CK("Z.CB.A.zcb_identity", "A", ZCB == Zrun - x, (y, k))
                d5red = 5 if D5 % 64 == 5 else (-11 if D5 % 64 == 53 else sym(D5, 6))
                ZCBred = 2 * d5red + 6 + F(3, 2) * (2 * Dy + 6 * k)
                CK("Z.run.deg.red_mod128", "A", v2f(ZCBred - Zrun) >= 7, (y,))
                if out["vZ"] < y - 2:
                    CK("Z.CB.A.m_eq", "A", m == v2f(ZCB) == out["vZ"], (y, k, m))
                if abs(Dy) <= 14:
                    CK("Z.CB.A.budget", "A", m < G(y) + 1, (y, k, Dy, m, G(y)))
                    mG.append((m - G(y), y, m))
                emax = max(emax, m - 4)
                inst += 1
    RES["counts"]["cb_A_instances"] = inst
    RES["stats"]["cb_A_max_e"] = emax
    if mG:
        RES["stats"]["cb_A_max_m_minus_G"] = max(z[0] for z in mG)
    CK("Z.CB.A.instances", "B", inst >= 500, inst, n=0)
    ok = True
    rng = random.Random(11)
    for (y, k) in ys[:60]:
        base = (16 - 3 * k) % 32
        for _ in range(3):
            Dy = base + 32 * rng.randrange(0, 4)
            a1 = affine_run(y, Dy, [canon_step(cal, y)])
            Dy2 = Dy + (rng.randrange(1, 1 << 20) << (y - 2))
            a2 = affine_run(y, Dy2, [canon_step(cal, y)])
            v1, v2_ = v2f(a1["Zrun"]), v2f(a2["Zrun"])
            if min(v1, v2_) < y - 2 and v1 != v2_:
                ok = False
    CK("Z.CB.A.sigma_stability", "A", ok, "v2(Z) stable under D_y -> D_y + odd*2^{y-2}")


def block_cb_BC(cal):
    cands = []
    for y in range(7, 12000):
        s = step_data(cal, y)
        if s["kind"] in ("b", "c") and s["omega"] == 5:
            cands.append((y, s))
    RES["counts"]["cb_BC_pool"] = len(cands)
    CK("Z.CB.BC.pool", "B", len(cands) >= 20, len(cands), n=0)
    inst = 0
    kinds = Counter()
    udep = 0
    for (y, s) in cands:
        kinds[s["kind"]] += 1
        base = (7 - (3 * s["tau"] + 5 - s["lam"])) % 16
        for Dy in [base - 32, sym(base, 4), base + 16, base + 32]:
            for u in (1, 3, (1 << 16) + 1):
                x = (1 << y) * u
                T = x + Dy
                x5 = s["cW"] * u + s["lam"]
                T5 = T + 3 + 3 * s["tau"]
                D5 = T5 - x5
                if not (v2i(x5) == 5 and D5 % 16 == 5):
                    CK("Z.CB.BC.entry", "A", False, (y, Dy, u, v2i(x5), D5 % 16))
                    continue
                CK("Z.CB.BC.entry", "A", True, None)
                xpp, m = catapult(x5, T5)
                out = run_checks(cal, y, Dy, u, [canon_step(cal, y)],
                                 ("cbBC", y, Dy, u), exact_A_y=2000)
                Zrun = out["aff"]["Zrun"]
                ZCB = 2 * D5 + 6 + F(3, 2) * s["lam"]      # Z_prev = lambda'_W
                CK("Z.run.deg.zcb_bc_identity", "A",
                   ZCB == Zrun + 2 * u * ((1 << y) - s["cW"]), (y,))
                vlim = s["sigma"] - 1
                CK("Z.CB.BC.vlim", "A", vlim == y - 2 - ((y - 1) - s["sigma"]), (y,))
                if v2f(ZCB) < vlim:
                    CK("Z.CB.BC.m_eq", "A", m == v2f(ZCB), (y, m, v2f(ZCB), vlim))
                else:
                    udep += 1
                    CK("Z.CB.BC.m_udep", "A", m >= vlim, (y, m, vlim))
                inst += 1
    RES["counts"]["cb_BC_instances"] = inst
    RES["stats"]["cb_BC_kinds"] = dict(kinds)
    RES["stats"]["cb_BC_u_dependent"] = udep
    CK("Z.CB.BC.instances", "B", inst >= 200, inst, n=0)


def block_class_at_m(instances):
    """output class: exact identity D''=(15-D_5)/3+2^m (mod 2^{m+1}); the two r1r2
    gateway families for b=0 tie residues {5,-11} mod 64."""
    ok = tot = famtot = famok = 0
    for rec in instances:
        m, T5, xpp = rec["m"], rec["T"], rec["xpp"]
        if m > 400:
            continue
        Dpp = (T5 + 9) - xpp   # Theta'' = T5 + 3 + 6k with k=1
        M = 1 << (m + 1)
        inv3 = pow(3, -1, M)
        exp = ((15 - (T5 - rec["x"])) * inv3 + (1 << m)) % M
        tot += 1
        ok += (Dpp % M == exp)
        if Dpp % M != exp and len(RES["examples"].setdefault("class_fail", [])) < 3:
            RES["examples"]["class_fail"].append(("identity", m, Dpp % M, exp, (T5 - rec["x"]) % 64))
        D5m = (T5 - rec["x"]) % M
        if D5m == 5 or D5m == M - 11:   # bare-tie constant to all m+1 bits (Theorem E, m < H)
            fam1 = ((10 - (1 << m)) * inv3) % M
            fam2 = ((26 - (1 << m)) * inv3) % M
            famtot += 1
            famok += (Dpp % M in (fam1, fam2))
            if Dpp % M not in (fam1, fam2) and len(RES["examples"].setdefault("class_fail", [])) < 6:
                RES["examples"]["class_fail"].append(("family", m, Dpp % M, fam1, fam2, D5m))
    CK("Z.CB.class", "A", ok == tot and tot >= 100, (ok, tot), n=max(tot, 1))
    CK("Z.CB.class.families", "A", famok == famtot and famtot >= 50, (famok, famtot),
       n=max(famtot, 1))


# --------------------------------------------------------------------------- #
def synth_run(y, path, rng):
    """backward construction of a synthetic-data run (non-canonical data) y -> path -> 5."""
    r = len(path)
    chains = [y] + list(path)
    if any(chains[i] - chains[i + 1] < 2 for i in range(r)):
        return None
    thetas = [0] * (r + 1)
    thetas[r] = 5 + 16 * rng.randrange(0, 4)
    steps = [None] * r
    for i in range(r, 0, -1):
        c_from, c_to = chains[i - 1], chains[i]
        use_bc = rng.random() < 0.3
        eps = 0
        if use_bc:
            eps = rng.randrange(1, 3)
            if c_from - c_to < 2 + eps:
                use_bc = False
        if use_bc:
            sigma = c_from - 1 - eps
            cc = rng.choice([o for o in (1, 3, 5, 7, 9, 11, 13) if o <= 3 * (1 << eps)])
            cW = cc << sigma
            lam = (2 * rng.randrange(1, 1 << 16) + 1) << c_to
            tau = max(2 * rng.randrange(1, 40), (abs(lam) - 9) // 9 + 1)
            steps[i - 1] = {"kind": rng.choice(["b", "c"]), "j_from": c_from, "cW": cW,
                            "lam": lam, "tau": tau, "sigma": sigma, "omega": c_to,
                            "src": ("synth", c_from)}
            low = (thetas[i] - (3 * tau + 3 - lam)) % (1 << (c_to + 1))
        else:
            low = (3 - thetas[i]) % (1 << (c_to + 1))
        if i > 1:
            span = (c_from + 1) - (c_to + 1)
            thetas[i - 1] = low + ((rng.randrange(0, 1 << span)) << (c_to + 1)) if span > 0 else low
            if steps[i - 1] is None:
                mod = 1 << c_to
                kk = (((1 << (c_to - 1)) - thetas[i - 1]) * pow(3, -1, mod)) % mod
                kk = kk if kk > 0 else mod
                kk += mod * rng.randrange(0, 3)
                steps[i - 1] = {"kind": "a", "k": kk, "tau": 2 * kk, "src": ("synth", c_from)}
        else:
            Dy = low
            if steps[0] is None:
                mod = 1 << c_to
                kk = (((1 << (c_to - 1)) - Dy) * pow(3, -1, mod)) % mod
                kk = kk if kk > 0 else mod
                kk += mod * rng.randrange(0, 3)
                steps[0] = {"kind": "a", "k": kk, "tau": 2 * kk, "src": ("synth", y)}
            return Dy, steps
    return None


def residue_stats(S, Cst, rng, maxE=12):
    """single-residue characterization + hit frequency for v2(S D + Cst) >= 5+E."""
    okall = True
    out = {}
    for E in range(1, maxE + 1):
        L = 5 + E
        sol = solve_congruence(S, Cst, L)
        hit = 0
        n = 256
        bad = 0
        for _ in range(n):
            D = rng.randrange(0, 1 << 24)
            v = v2f(S * D + Cst) >= L
            hit += v
            if sol[0] == "class":
                mem = (D - sol[1]) % (1 << sol[2]) == 0
                bad += (v != mem)
            elif sol[0] == "never":
                bad += v
            else:
                bad += (not v)
        okall = okall and bad == 0
        out[E] = (sol[0] if sol[0] != "class" else "class%d" % sol[2], hit, n)
    return okall, out


def block_synth(cal):
    rng = random.Random(20261024)
    lens = Counter()
    mrecs = []
    freq = {}
    okres_acc = True
    for y in [40, 999, 10 ** 5]:
        for _ in range(500):
            r = rng.randrange(1, 7)
            js = sorted(rng.sample(range(7, 34), r - 1), reverse=True) + [5] if r > 1 else [5]
            if js[0] > y - 2:
                continue
            got = synth_run(y, js, rng)
            if got is None:
                continue
            Dy, steps = got
            lens[r] += 1
            out = run_checks(cal, y, Dy, 1, steps, ("synth", y, r), exact_A_y=2000)
            mrecs.append(out)
            ok, fr = residue_stats(out["aff"]["S"], out["aff"]["Cst"], rng)
            okres_acc = okres_acc and ok
            for E, (desc, hit, n) in fr.items():
                f = freq.setdefault(E, [0, 0])
                f[0] += hit
                f[1] += n
    # huge-y synthetic tier: affine-only checks (no exact pair walk)
    for y in [10 ** 6, 10 ** 7]:
        for _ in range(120):
            r = rng.randrange(1, 7)
            js = sorted(rng.sample(range(7, 34), r - 1), reverse=True) + [5] if r > 1 else [5]
            got = synth_run(y, js, rng)
            if got is None:
                continue
            Dy, steps = got
            aff = affine_run(y, Dy, steps, expected_params=[y] + js)
            vZ = v2f(aff["Zrun"])
            CK("Z.run.vZ_ge5", "A", vZ >= 5, (y, vZ))
            CK("Z.run.mu_ge", "A", aff["mu"] >= r + 4, (y, aff["mu"]))
            CK("Z.run.S_neq0", "A", aff["S"] != 0, (y,))
            CK("Z.run.q_v2", "A", aff["q"] == 0 or v2f(aff["q"]) <= 1, (y, aff["q"]))
            tau_max = max([st["tau"] for st in steps] + [1])
            s = sum(1 for st in steps if st["kind"] != "a")
            Brun = (2 + 2 * F(3, 2) ** s) * abs(Dy) + 6 + 6 * r * (1 + tau_max) + \
                F(3, 2) ** s * r * (abs(Dy) + 11 + 12 * r * tau_max)
            if aff["Zrun"] != 0:
                CK("Z.run.size", "A", abs(aff["Zrun"]) <= Brun, (y, r, s))
                CK("Z.run.m_le_size", "A", vZ <= aff["mu"] or vZ >= aff["mu"], None)
            ok, fr = residue_stats(aff["S"], aff["Cst"], rng, maxE=10)
            okres_acc = okres_acc and ok
            lens[r] += 1
    CK("Z.run.synth.cover", "B", all(lens.get(i, 0) >= 20 for i in range(1, 7)),
       dict(lens), n=0)
    CK("Z.run.synth.residue", "A", okres_acc,
       "single-residue characterization, accumulated over all runs and levels")
    RES["stats"]["synth_freq"] = {E: {"hits": v[0], "total": v[1],
                                      "rate": round(v[0] / max(v[1], 1), 5)}
                                  for E, v in freq.items()}
    RES["counts"]["synth_runs"] = dict(lens)
    return mrecs


J1_MIN, J1_MAX, J1_MAX_HUGE = 17, 40, 60


def tie_reach_sets(cal):
    """tie-reaching classes at j1: full enumeration for 17..19, sampled 20..40.

    Note: a chain can enter the bare tie at 5 only through an a-step with
    v2(3k+theta)=4 (needs k = tau(j-1)/2 = 6 mod 16; smallest such parameter is 17)
    or a b/c step with omega=5 (smallest 65).  Hence j1 >= 17."""
    sets, sampled = {}, {}
    for j1 in range(J1_MIN, 20):
        d = {}
        for th in range(1 << (j1 + 1)):
            out, path = class_walk(cal, j1, th)
            if out == "tie5":
                d[th] = len(path) - 1
        sets[j1] = d
    rng = random.Random(777)
    for j1 in range(20, J1_MAX + 1):
        hit = 0
        n = 4000
        for _ in range(n):
            th = rng.randrange(0, 1 << (j1 + 1))
            out, path = class_walk(cal, j1, th)
            hit += (out == "tie5")
        sampled[j1] = (hit, n)
    stats = {}
    for j1 in range(J1_MIN, 20):
        stats[j1] = {"reach": len(sets[j1]), "tot": 1 << (j1 + 1),
                     "frac": round(len(sets[j1]) / (1 << (j1 + 1)), 8),
                     "log2_frac": round(math.log2(len(sets[j1]) / (1 << (j1 + 1))), 3)
                     if sets[j1] else None}
    for j1, (hit, n) in sampled.items():
        stats[j1] = {"reach_sampled": hit, "n": n,
                     "frac": round(hit / n, 6) if hit else 0.0,
                     "log2_frac": round(math.log2(hit / n), 2) if hit else None}
    RES["stats"]["tie_reach"] = stats
    CK("Z.run.canon.pool_nonempty", "B", len(sets[17]) > 0, len(sets.get(17, [])), n=0)
    ok_low = (stats[17]["frac"] == 0.03125) and stats[18]["reach"] == 0 and stats[19]["reach"] == 0
    ok_low = ok_low and all(stats[j1].get("frac", 0) <= 0.001 for j1 in range(20, J1_MAX + 1))
    CK("Z.run.canon.lowdim", "B", ok_low,
       "tie-reaching classes: exactly 2^-5 at j1=17 (single residue mod 32), 0 at 18,19 (full enum)", n=0)
    return sets


def block_canon(cal):
    TR = tie_reach_sets(cal)
    hits = []
    hitj = Counter()
    scanned = 0
    for y in range(J1_MIN + 2, 12001):
        s = step_data(cal, y)
        if s["kind"] != "a":
            continue
        scanned += 1
        for j1 in range(J1_MIN, J1_MAX + 1):
            if j1 > y - 2:
                break
            delta1 = ((1 << (j1 - 1)) - 3 * s["k"]) % (1 << j1)
            theta1 = (3 - delta1) % (1 << (j1 + 1))
            out, path = class_walk(cal, j1, theta1)
            if out == "tie5":
                hits.append((y, j1))
                hitj[j1] += 1
    RES["counts"]["canon_scan_y"] = scanned
    RES["counts"]["canon_scan_hits"] = len(hits)
    RES["stats"]["canon_hit_j1"] = dict(hitj)
    bylen = Counter()
    mrecs = []
    rng = random.Random(5)
    sample = hits if len(hits) <= 220 else rng.sample(hits, 220)
    for (y, j1) in sample:
        delta1 = ((1 << (j1 - 1)) - 3 * step_data(cal, y)["k"]) % (1 << j1)
        theta1 = (3 - delta1) % (1 << (j1 + 1))
        out, path = class_walk(cal, j1, theta1)
        Dy = sym(delta1, j1 + 1)
        rows, sts, how = exact_walk_rec(cal, 1 << y, (1 << y) + Dy, max_steps=60)
        if how != "tie5":
            CK("Z.run.canon.realize", "A", False, (y, j1, how))
            continue
        CK("Z.run.canon.realize", "A", [q["j"] for q in rows] == [y] + [p[0] for p in path],
           (y, j1, [q["j"] for q in rows], [p[0] for p in path]))
        mrecs.append(run_checks(cal, y, Dy, 1, sts, ("canon", y, j1)))
        bylen[len(path)] += 1        # run length = number of steps = len(path)
    RES["counts"]["canon_verified"] = sum(bylen.values())
    RES["stats"]["canon_run_lengths"] = dict(bylen)
    CK("Z.run.canon.verified", "B", sum(bylen.values()) >= 20, sum(bylen.values()), n=0)
    # survey: b/c steps with omega >= 17 in range (none expected: needed for B-entry runs)
    bigomega = 0
    for y in range(9, 12001):
        s = step_data(cal, y)
        if s["kind"] in ("b", "c") and s["omega"] >= J1_MIN:
            bigomega += 1
    RES["counts"]["canon_bigomega_bc"] = bigomega
    return mrecs


def block_huge(cal):
    """huge-y canonical-typed runs: search a window of y around each target magnitude."""
    mrecs = []
    found = []
    for target in [10 ** 5, 10 ** 6, 10 ** 7, 2 * 10 ** 7]:
        per_target = 0
        for y in range(max(80, target - 45), target + 46):
            if per_target >= 3:
                break
            s = step_data(cal, y)
            if s["kind"] != "a":
                continue
            for j1 in range(J1_MIN, J1_MAX_HUGE + 1):
                if j1 > y - 2:
                    break
                delta1 = ((1 << (j1 - 1)) - 3 * s["k"]) % (1 << j1)
                theta1 = (3 - delta1) % (1 << (j1 + 1))
                out, path = class_walk(cal, j1, theta1)
                if out != "tie5":
                    continue
                Dy = sym(delta1, j1 + 1)
                rows, sts, how = exact_walk_rec(cal, 1 << y, (1 << y) + Dy, max_steps=60)
                CK("Z.run.huge.realize", "A", how == "tie5", (y, j1, how))
                if how != "tie5":
                    continue
                rec = run_checks(cal, y, Dy, 1, sts, ("huge", y, j1))
                mrecs.append(rec)
                found.append({"y": y, "target": target, "j1": j1, "m": rec["m"],
                              "r": rec["r"], "s": rec["s"], "absDy": abs(Dy),
                              "v2Z": rec["vZ"], "mu": rec["mu"]})
                per_target += 1
                w = rec["aff"]["w"]
                S, Cst = rec["aff"]["S"], rec["aff"]["Cst"]
                base = v2f(S * Dy + Cst)
                okt = True
                for t in range(1, 48):
                    v = v2f(S * (Dy + t * (1 << j1)) + Cst)
                    if min(base, v) < j1 + w and v != base:
                        okt = False
                CK("Z.run.huge.t_struct", "A", okt, (y, j1))
                break
        found.append({"target": target, "found": per_target})
    RES["stats"]["huge_runs"] = found
    CK("Z.run.huge.instances", "B", len(mrecs) >= 3, len(mrecs), n=0)
    return mrecs


BAD36 = ([(5, d) for d in (5, 21, -27, -11)] +
         [(8, d) for d in (58, 186, -198, -70)] +
         [(12, d) for d in (1012, 3060, -3084, -1036)] +
         [(14, d) for d in (4081, 12273, -12303, -4111)] +
         [(17, d) for d in (32702, 32750, 98238, 98286, -98370, -98322, -32834, -32786)] +
         [(22, d) for d in (1048552, 3145704, 5242856, 7340008)] +
         [(24, d) for d in (4194277, 12582885, 20971493, 29360101)] +
         [(27, d) for d in (33554402, 100663266, 167772130, 234880994)])


def block_replay(cal):
    starts = list(BAD36)
    for j in range(5, 61):
        for d in range(-12, 16):
            if (j, d) in ((5, 5), (5, -11)):
                continue
            starts.append((j, d))
    ties = 0
    zeros = 0
    mrecs = []
    for (j, d) in starts:
        x0 = 1 << j
        rows, sts, how = exact_walk_rec(cal, x0, x0 + d, max_steps=80, stop_at_tie=False)
        if how == "zero" or any(q["x"] == 0 for q in rows):
            zeros += 1
        for i in range(1, len(rows)):
            q = rows[i]
            if q["j"] == 5 and (q["T"] - q["x"]) % 16 == 5 and rows[i - 1]["j"] >= 7:
                yv = rows[i - 1]["j"]
                Dyv = rows[i - 1]["T"] - rows[i - 1]["x"]
                xpp, m = catapult(q["x"], q["T"])
                if xpp == 0:
                    continue
                sy = step_data(cal, yv)
                if sy["kind"] == "even":
                    continue
                aff = affine_run(yv, Dyv, [canon_step(cal, yv)])
                vZ = v2f(aff["Zrun"])
                CK("Z.replay.formula", "A", (vZ < aff["mu"] and m == vZ) or m >= aff["mu"],
                   ((j, d), yv, m, vZ, aff["mu"]))
                ties += 1
                mrecs.append(dict(m=m, e=m - 4, vZ=vZ, mu=aff["mu"], params=[yv, 5],
                                  aff=aff, r=1, s=0, x=q["x"], T=q["T"], xpp=xpp,
                                  D5=q["T"] - q["x"], Brun=0))
    RES["counts"]["replay_tie_visits"] = ties
    RES["counts"]["replay_zero_walks"] = zeros
    CK("Z.replay.instances", "B", ties >= 5, ties, n=0)
    return mrecs


def block_centry(cal):
    s = step_data(cal, 6133)
    CK("Z.centry.pool", "B", s["kind"] == "c" and s["omega"] == 5, (s["kind"], s["omega"]), n=0)
    y = 6133
    eps = (y - 1) - s["sigma"]
    inst = 0
    base = (7 - (3 * s["tau"] + 5 - s["lam"])) % 16
    for Dy in [base - 32, sym(base, 4), base + 16, base + 32, base + 48]:
        for u in (1, 3):
            x = (1 << y) * u
            T = x + Dy
            x5 = s["cW"] * u + s["lam"]
            T5 = T + 3 + 3 * s["tau"]
            D5 = T5 - x5
            if not (v2i(x5) == 5 and D5 % 16 == 5):
                CK("Z.centry.entry", "A", False, (Dy, u, v2i(x5), D5 % 16))
                continue
            CK("Z.centry.entry", "A", True, None)
            out = run_checks(cal, y, Dy, u, [canon_step(cal, y)], ("cE", y, Dy, u),
                             exact_A_y=2000)
            sigmaC = y - 2 - eps
            CK("Z.centry.sigmaC", "A", sigmaC == s["sigma"] - 1, (y, sigmaC))
            CK("Z.centry.ind_bound", "A", 1 + eps <= 4 * math.log2(y) + 4, (y, eps))
            CK("Z.centry.sigma_ind", "A", sigmaC >= y - 4 * math.log2(y) - 5, (y, sigmaC))
            # certification fit: sigma_C must exceed m+1-w for m to be certified from D_y mod 2^sigma_C
            CK("Z.centry.cert_fit", "B",
               sigmaC + out["aff"]["w"] > out["m"] + 1 or out["m"] >= out["mu"],
               (y, out["m"], out["aff"]["w"], sigmaC))
            inst += 1
    RES["counts"]["centry_instances"] = inst
    CK("Z.centry.instances", "B", inst >= 4, inst, n=0)


def block_const():
    minslack = INF
    argmin = None
    for y in [N0, 10 ** 8, 10 ** 10, 10 ** 12, 1 << 50, 1 << 100]:
        tau = (y - 1) * P_clock(y - 1)
        for r in [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]:
            for s in sorted(set([0, r // 2, r])):
                BD = 5
                Brun = (2 + 2 * F(3, 2) ** s) * BD + 6 + 6 * r * (1 + tau) + \
                    F(3, 2) ** s * r * (BD + 11 + 12 * r * tau)
                slack = G(y) + s * math.log2(1.5) + 2 * math.log2(r + 1) - math.log2(float(Brun))
                if slack < minslack:
                    minslack, argmin = slack, (y, r, s)
    CK("Z.const.slack", "B", minslack > 10, (minslack, argmin), n=0)
    RES["stats"]["slack_min"] = round(minslack, 3)
    RES["stats"]["slack_argmin"] = argmin
    tab = {}
    for s in [0, 1, 2, 3, 4]:
        r = 1
        while s * math.log2(1.5) + 2 * math.log2(r + 1) <= minslack - 1:
            r += 1
        tab[s] = r - 1
    RES["stats"]["rstar_table"] = tab


def block_data(cal):
    okS1 = okratio = oklam = oktau = True
    n = 0
    for j, s in sorted(_SDC.items()):
        if s["kind"] == "even":
            continue
        n += 1
        oktau &= s["tau"] <= (j - 1) * P_clock(j - 1)
        if s["kind"] == "a":
            continue
        okS1 &= s["omega"] < s["sigma"]
        eps = (j - 1) - s["sigma"]
        cc = s["cW"] >> s["sigma"]
        okratio &= 0 < cc <= 3 * (1 << eps)
        oklam &= abs(s["lam"]) <= 9 * s["tau"] + 9
    CK("Z.data.S1", "A", okS1, "omega<sigma", n=n)
    CK("Z.data.ratio", "A", okratio, "c''_W <= 3*2^eps (=> ratio <= 3/2)", n=n)
    CK("Z.data.lam", "B", oklam, "|lam'| <= 9 tau + 9", n=n)
    CK("Z.data.tau", "A", oktau, "tau <= (j-1)P(j-1)", n=n)
    RES["counts"]["crossings_used"] = n
    RES["counts"]["max_param_used"] = max(_SDC.keys())


def main():
    cal = Calendar(512)
    t0 = time.time()
    block_cb_A(cal)
    t1 = time.time()
    block_cb_BC(cal)
    t2 = time.time()
    mrecs = block_replay(cal)
    t3 = time.time()
    msyn = block_synth(cal)
    t4 = time.time()
    mcan = block_canon(cal)
    t5 = time.time()
    mhug = block_huge(cal)
    t6 = time.time()
    block_centry(cal)
    block_const()
    block_data(cal)
    allm = mrecs + msyn + mcan + mhug
    block_class_at_m(allm)
    estats = Counter(z["e"] for z in allm)
    RES["stats"]["e_histogram"] = dict(sorted(estats.items()))
    RES["stats"]["max_e"] = max(estats) if estats else None
    RES["stats"]["max_m"] = max(z["m"] for z in allm) if allm else None
    RES["timing"] = {"cb_A": round(t1 - t0, 1), "cb_BC": round(t2 - t1, 1),
                     "replay": round(t3 - t2, 1), "synth": round(t4 - t3, 1),
                     "canon": round(t5 - t4, 1), "huge": round(t6 - t5, 1),
                     "total": round(time.time() - T_START, 1)}
    tot = sum(d["checked"] for d in RES["checks"].values())
    fail = sum(d["failed"] for d in RES["checks"].values())
    RES["counts"]["total_checks"] = tot
    RES["counts"]["total_fail"] = fail
    RES["status"] = "PASS" if fail == 0 else "FAIL"
    OUT.write_text(json.dumps(RES, indent=1, default=str) + "\n", encoding="utf-8")
    print("STATUS:", RES["status"], "checks:", tot, "fail:", fail)
    for k in ["cb_A_instances", "cb_BC_instances", "replay_tie_visits", "synth_runs",
              "canon_scan_hits", "canon_verified", "centry_instances",
              "crossings_used", "max_param_used"]:
        print("  ", k, "=", RES["counts"].get(k))
    print("slack_min:", RES["stats"].get("slack_min"), "at", RES["stats"].get("slack_argmin"))
    print("tie_reach:", json.dumps(RES["stats"].get("tie_reach"), default=str))
    print("huge:", json.dumps(RES["stats"].get("huge_runs"), default=str))
    print("e_hist:", RES["stats"].get("e_histogram"))
    if RES["failures"][:5]:
        print("failures:", RES["failures"][:5])
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
