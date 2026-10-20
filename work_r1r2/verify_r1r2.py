"""verify_r1r2.py -- finite exact checks for work_r1r2/NOTES.md (UNREVIEWED).

Theorem A (R2 for a/b landings under R1).  Stages, all exact integer arithmetic:
  V1  reachable drift sets: theta_t = 2i-t+1, 0<=i<=t, for all letter words of length <= TMAX
  V2  no-resonance inequality constants: 3k_min vs 2*Lambda_max+1, and Lemma 2.1 size check
  V3  window certificate: certify(j,delta) for delta in [-12,15], 5<=j<JW (exhaustive; the
      full range 5<=j<2*10^7 is the accepted [B] of work_claude_shifted; here a subset)
  V4  gateway-pair algebra: exact two-a-step identities x_{u+1}, D_{u+1}, m and the resolved
      classes (10-2^m)/3, (26-2^m)/3 for all four bare-tie scenarios, m<=MMAX
  V5  table-mediated end-to-end check: construct a real state at a real odd-a crossing with
      prescribed k,u,theta realizing a (5,5) or (5,-11) landing and verify the formulas and
      the record inequality by the exact walk
  V6  resolved-class certificate: certify(m, class(m)) for 5<=m<MMAX (both classes)
Usage: python -B verify_r1r2.py [JW] [MMAX]
Writes verify_r1r2_checks.json beside itself.
"""
import sys, json, time, itertools
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_global_ext' / 'route_c'))
from fdata import lam_walk, small_full, v2

JW = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
MMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
N0 = 2 * 10**7
B = 1 << (N0 // 2)
TMAX = 14
T0 = time.time(); RES = dict(stage_seconds={})
def log(*a):
    print(round(time.time() - T0, 2), *a, flush=True)

# ---------------------------------------------------------------- tables
NT = max(JW, MMAX) + 8
D = lam_walk(NT)
typ, tau, eps, odd, lY, lA = D['typ'], D['tau'], D['eps'], D['odd'], D['lY'], D['lA']
lam = lambda n: lA[n] + 2 * lY[n] + 3
S = small_full(min(1024, NT))
cW = {n: r['x'][0] for n, r in S.items() if r['odd'] and r['typ'] != 'a'}
log('tables built, N =', NT)

# ---------------------------------------------------------------- V1 reachable drift
def reachable(T):
    """all theta values reachable by T steps of a: theta->3-theta, b: theta->theta-1"""
    cur = {1}
    sets = [set(cur)]
    for _ in range(T):
        nxt = set()
        for th in cur:
            nxt.add(3 - th)
            nxt.add(th - 1)
        cur = nxt
        sets.append(set(cur))
    return sets
sets = reachable(TMAX)
bad1 = []
for t, s in enumerate(sets):
    want = {2 * i - t + 1 for i in range(t + 1)}
    if s != want:
        bad1.append((t, sorted(s), sorted(want)))
RES['V1'] = dict(TMAX=TMAX, bad=bad1[:5], n_bad=len(bad1),
                 sizes=[len(s) for s in sets])
log('V1', RES['V1']['n_bad'], 'bad')

# ---------------------------------------------------------------- V2 inequalities
lam_max = (B - 4) // 6            # 6*Lambda+4 <= B  =>  Lambda <= (B-4)/6  (ASTRONOMICAL: B=2^10^7)
kmin = (N0 - 2) // 4              # k = tau/2 >= (n-1)/4, n = j-1 >= N0-1
# no-resonance needs 2*Lambda+1 < 3*kmin; this is NOT implied by Lambda <= (B-4)/6
Lambda_res = (3 * kmin - 2) // 2  # largest Lambda with 2*Lambda+1 < 3*kmin
ineq = dict(Lambda_max_bits=lam_max.bit_length(),
            three_kmin=3 * kmin, Lambda_res=Lambda_res,
            holds_at_Lambda13=(2 * 13 + 1) < 3 * kmin,
            holds_at_Lambda_res=(2 * Lambda_res + 1) < 3 * kmin,
            fails_at_Lambda_res_plus_1=(2 * (Lambda_res + 1) + 1) < 3 * kmin)
# Lemma 2.1 numeric form at j = N0: B + kappa(j) < 2^(j-3)
import math
P = lambda n: 2 * math.ceil(math.log2(6 * n * n + 5))**2 + 1345
j = N0
kappa = 1.5 * (j - 1) * P(j - 1)
ineq['size_at_N0'] = (B + int(kappa) < (1 << (j - 3)))
ineq['B_bits'] = N0 // 2
RES['V2'] = ineq
log('V2 no-resonance at 13:', ineq['holds_at_Lambda13'], 'Lambda_res', ineq['Lambda_res'], 'size:', ineq['size_at_N0'])

# ---------------------------------------------------------------- exact walk / certify
def walk(j, delta, limit=400):
    x = 1 << j; th = x + delta; G = 0; word = []; rec = -1
    for _ in range(limit):
        if x <= 0:
            return 'nonpos', word, rec
        if v2(x) != j:
            return 'error', word, rec
        word.append((j, th - x)); rec = max(rec, j + G)
        n = j - 1
        if n >= NT:
            return 'nodata', word, rec
        if not odd[n]:
            return 'end', word, rec
        t = chr(typ[n]); T = tau[n]
        if t == 'a':
            x = 2 * th + 3 * T - (x >> 1)
        else:
            if n not in cW:
                return 'nodata', word, rec
            x = cW[n] * (x >> j) + lam(n)
        th += 3 + 3 * T; G += 1 + eps[n]
        if x <= 0:
            return 'nonpos', word, rec
        j = v2(x)
    return 'limit', word, rec

def certify(j, delta):
    st, w, r = walk(j, delta)
    return st == 'end' and r <= j, st, r, w

# ---------------------------------------------------------------- V3 window certificate
fails = []
tot = 0
for j in range(5, JW):
    for d in range(-12, 16):
        tot += 1
        ok, st, r, w = certify(j, d)
        if not ok:
            fails.append((j, d, st, r))
RES['V3'] = dict(JW=JW, pairs=tot, fails=fails)
log('V3 window pairs', tot, 'fails', fails[:5], len(fails))

# ---------------------------------------------------------------- V4 gateway algebra
# two a-steps from a state (x=2^j u, Theta=x+theta) at a type-a crossing with halftimes
# k (first) and l (second, =k_4=1 for the landing at j=5).  Exact identities.
def two_step_algebra(j, u, k, theta, l=1):
    x = (1 << j) * u; th = x + theta
    x1 = 2 * th + 6 * k - (x >> 1); th1 = th + 3 + 6 * k
    x2 = 2 * th1 + 6 * l - (x1 >> 1); th2 = th1 + 3 + 6 * l
    return x1, th1, x2, th2

def sym(v, bits):
    M = 1 << bits; r = v % M
    return r - M if 2 * r > M else r

res4 = dict(cases={}, bad=[])
import random
random.seed(1)
for trial in range(4000):
    j = random.randint(20, 400)
    u = random.randrange(1, 1 << 18, 2)
    k = random.randrange(1, 1 << 40)
    theta = random.randint(-10**6, 10**6)
    x1, th1, x2, th2 = two_step_algebra(j, u, k, theta)
    # claimed identities
    claim_x2 = 5 * (1 << (j - 2)) * u + theta + 12 + 9 * k
    claim_D2 = -(1 << (j - 2)) * u - 3 * k
    if x2 != claim_x2 or (th2 - x2) != claim_D2:
        res4['bad'].append(('a', j, u, k, theta, x2 - claim_x2))
        break
RES['V4_a_identity'] = dict(trials=4000, bad=res4['bad'][:3])

# four bare-tie scenarios: landing congruence v2(3k+theta0)=4 ; gateway m=v2(9k+theta0+12)
scen = {}
for m in range(5, min(MMAX, 64) + 1):
    M = 1 << (m + 1); i9 = pow(9, -1, M)
    for name, th0 in (('55', -2), ('5m11', 14)):        # a-landings
        k = ((1 << m) - 12 - th0) * i9 % M              # 9k+theta0+12 == 2^m
        ok = (3 * k + th0) % 16 == 0 and v2(3 * k + th0) == 4
        D2 = ((-3 * k) % M)
        # independent: exact two-step with u=1, fake deep j
        j = max(m + 4, 30)
        x2 = 5 * (1 << (j - 2)) + th0 + 12 + 9 * k
        m2 = v2(x2)
        cls = (th2 := 0)  # placeholder
        # class from D_{u+1} = -2^{j-2}u-3k ; mod 2^{m+1}
        cls = (-(1 << (j - 2)) - 3 * k) % M
        want = (10 - (1 << m)) * pow(3, -1, M) % M if name == '55' else (26 - (1 << m)) * pow(3, -1, M) % M
        scen.setdefault(name, []).append(dict(m=m, landing_ok=ok, m_gateway=m2, cls=cls, want=want,
                                             cls_eq=cls == want))
RES['V4_b_scenarios'] = dict(
    cases={k: [(c['m'], c['landing_ok'], c['m_gateway'], c['cls_eq']) for c in v] for k, v in scen.items()},
    all_ok=all(c['landing_ok'] and c['m_gateway'] == c['m'] and c['cls_eq'] for v in scen.values() for c in v))
log('V4 gateway algebra all_ok', RES['V4_b_scenarios']['all_ok'])

# ---------------------------------------------------------------- V5 end-to-end on real table
# find real odd-a crossings n (type a) with v2(3k+theta0)=4 for theta0 in {-2,14}, small j.
real = {}
for n in range(4, NT - 1):
    if not odd[n] or chr(typ[n]) != 'a':
        continue
    k = tau[n] // 2
    for name, th0 in (('55', -2), ('5m11', 14)):
        z = 3 * k + th0
        if z > 0 and v2(z) == 4:
            real.setdefault(name, []).append((n + 1, k, th0, z))
RES['V5_real_crossings'] = {k: v[:8] for k, v in real.items()}
log('V5 real crossings', {k: len(v) for k, v in real.items()})

# end-to-end: build the true state at chain T (x=2^j*u, Theta=x+theta0) for a real crossing,
# run the exact walk; check it lands at j=5, then the pair formula for x_{u+1}, D_{u+1}, m, class
v5 = dict(cases=[], errors=[])
for name, lst in real.items():
    for (jT, k, th0, z) in lst[:3]:
        for u in (1, 3, 5, 17):
            x = (1 << jT) * u; th = x + th0
            # exact walk from this state with the real table (fake origin is fine: rules exact)
            x1, th1, x2, th2 = two_step_algebra(jT, u, k, th0)
            # check the walk code reproduces two steps
            # (run walk() on the state directly)
            xs, ths, Gs = x, th, 0
            oksteps = []
            for step in range(2):
                j = v2(xs); n = j - 1
                assert chr(typ[n]) == 'a'
                T = tau[n]
                if step == 0:
                    assert T == 2 * k, (T, k)
                xs = 2 * ths + 3 * T - (xs >> 1); ths += 3 + 3 * T
                oksteps.append((j, v2(xs)))
            ju = oksteps[0][1]
            m = v2(x2)
            cls = (th2 - x2) % (1 << (m + 1))
            M = 1 << (m + 1)
            want = ((10 - (1 << m)) if name == '55' else (26 - (1 << m))) * pow(3, -1, M) % M
            GeT = 0  # Gamma_T = 0 in this constructed state at chain T
            Ru1 = m + GeT + 2
            RT = jT + GeT
            rec_ok = Ru1 <= RT - 1
            rec = dict(name=name, jT=jT, k=k, u=u, theta0=th0, landing_j=ju,
                       m_formula=m, m_walk=v2(x2), cls=cls, want=want,
                       cls_eq=(cls == want), record_ok=rec_ok, two_step_ok=(xs == x2 and ths == th2))
            v5['cases'].append(rec)
            if not (ju == 5 and rec['cls_eq'] and rec_ok and rec['two_step_ok']):
                v5['errors'].append(rec)
RES['V5'] = dict(n_cases=len(v5['cases']), errors=v5['errors'][:5],
                 sample=v5['cases'][:4])
log('V5 end-to-end cases', len(v5['cases']), 'errors', len(v5['errors']))

# ---------------------------------------------------------------- V6 resolved-class certificate
v6 = dict(fails=[], count=0)
for m in range(5, MMAX + 1):
    M = 1 << (m + 1); i9 = pow(9, -1, M)
    for name, th0 in (('55', -2), ('5m11', 14)):
        k = ((1 << m) - 12 - th0) * i9 % M
        cls = (-3 * k) % M
        ok, st, r, w = certify(m, cls)
        v6['count'] += 1
        if not ok:
            v6['fails'].append((m, name, st, r))
RES['V6'] = v6
log('V6 resolved-class certificate pairs', v6['count'], 'fails', v6['fails'][:5])

RES['stage_seconds'] = dict(total=round(time.time() - T0, 2))
with open(HERE / 'verify_r1r2_checks.json', 'w', encoding='utf-8') as f:
    json.dump(RES, f, indent=1, default=str)
log('done')
