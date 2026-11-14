"""verify_t5.py -- verification of work_gc_level_t5 (LEVEL-T5: structure lemmas, rational bulk,
gateway tower, level E / C7-E, the orbit obstruction).

Checks (each prints CHECK <n> ... ok / FAIL):
  1  GW identity: for real calendar odd-a chains j and free outputs m>=j-1, the output class
     D' mod 2^(m+1) equals (9+6k_j-delta)/3 + 2^m exactly (integer arithmetic, many (u,h,m)).
  2  GW anchor cases: (5,5)->(10-2^m)/3, (5,-11)->(26-2^m)/3, (5,-1/3)->46/9+2^m,
     (5,-17/3)->62/9+2^m, (8,58)->-37/3+2^m; bare ties fail certify; gateway classes pass.
  3  Closed-form orbit: -3 +/- 8/3^r == 5 mod 16 (r<=12); fired = 6 -/+ 8/3^(r+1);
     a-descendant of fired = next orbit class; observed orbit data matches the closed form.
  4  Drift BFS == hand tables (level E and S(J)).
  5  Rational bulk vs scalar certify: j in [64,3000) full + [3e3,3e5) sampled (2000 chains),
     several families; integer special case == rwalk.bulk (j in [64,3000)).
  6  Truncation faithfulness bound: |3*k*den + num| < 2^53 for all odd-a chains j<2e7 and all
     certified families -- read dynamically from levels_t5_20000000.json (134 families);
     falls back to a fixed list if the json is absent.
  7  T4 reproduction: the P1 level summaries match the accepted levels_20000000.json.
  8  Family closure (smoke range j<3e5): families certify except the chain-5 orbit
     no-lift entries; at FULL range: 8 key + ALL 20 orbit no-lift families (r=1..10) +
     the den-3^10 fired pair + 10 descendants (round-1 review base).
  9  Level E / C7-E: the residual free-entry lists are exactly the chain-5 sets
     {5, 21(=-1/3), -27(=-17/3), -11} (+ int (5,5)); 9b replays the t=0 spec construction
     from recomputed family exports and re-certifies every rebuilt entry.
  10 REG size inequality at table scale (vectorised): 3*Qmax*k + |C|max < 2^(j-2), j>=N0 sample.

ASCII output only; last line ALL PASS iff every check passed.
"""
import sys, json, time
from pathlib import Path
from fractions import Fraction as F

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
import numpy as np
import rwalk as R
import rwalk_t5 as W

T0 = time.time()
T = R.Table()
FAILED = []


def check(n, cond, msg=''):
    print('CHECK %-2d %s %s (%.1fs)' % (n, 'ok' if cond else 'FAIL', msg, time.time() - T0), flush=True)
    if not cond:
        FAILED.append(n)


# ---------------- 1: GW identity ----------------
rng = np.random.default_rng(20261110)
gwk = {}
for j in [5, 8, 9, 12, 17, 24, 42, 61, 100, 1000]:
    t, od, tau, ep, lam = T.row(j - 1)
    if not (od and t == 'a'):
        continue
    k = tau // 2
    ok_here = True
    for delta in [5, -11, 58, 2, -3, 174]:
        for trial in range(40):
            u = int(rng.integers(1, 1 << 20)) * 2 + 1
            h = int(rng.integers(0, 1 << 20))
            x = (1 << j) * u
            D = delta + (1 << (j + 1)) * h
            Th = x + D
            xp = 2 * Th + 3 * tau - (x >> 1)
            if xp == 0:
                continue
            m = R.v2(xp)
            if m < j - 1:
                continue
            Dp = (Th + 3 + 3 * tau) - xp
            M = 1 << (m + 1)
            pred = ((9 + 6 * k - D) % M) * pow(3, -1, M) % M      # exact-defect form
            pred = (pred + (1 << m)) % M
            if (Dp % M) != pred:
                ok_here = False
            if m <= j:                                             # class form (delta mod 2^(j+1))
                val = (F(9 + 6 * k) - F(delta)) / 3
                pred2 = (val.numerator * pow(val.denominator, -1, M)) % M
                pred2 = (pred2 + (1 << m)) % M
                if (Dp % M) != pred2:
                    ok_here = False
    gwk[j] = ok_here
check(1, all(gwk.values()), 'GW identity on %d chains x 6 classes' % len(gwk))

# ---------------- 2: GW anchors ----------------
ok2 = True
M = {}
for (delta, num, den) in [(F(5), 10, 3), (F(-11), 26, 3), (F(-1, 3), 46, 9), (F(-17, 3), 62, 9)]:
    val = F(9 + 6 * 1) - delta
    f = val / 3
    if (f.numerator, f.denominator) != (num, den):
        ok2 = False
val = F(9 + 6 * (T.tau[7] // 2)) - F(58)          # j=8, k=tau(7)/2
f = val / 3
ok2 = ok2 and (f.numerator, f.denominator) == (-37, 3)
# bare ties fail; gateway classes certify
for (j, num, den, lift, exp) in [(5, 5, 1, False, False), (5, -11, 1, False, False),
                                 (5, -1, 3, False, False), (5, -17, 3, False, False),
                                 (9, 10, 3, True, True), (30, 10, 3, True, True),
                                 (7, 46, 9, True, True), (7, 62, 9, True, True)]:
    c = W.certify_rat(T, j, num, den, lift)
    ok2 = ok2 and (c['ok'] == exp)
check(2, ok2, 'anchors + bare ties')

# ---------------- 3: closed-form orbit ----------------
ok3 = True
for r in range(1, 13):
    for sgn in (1, -1):
        d = F(-3) + sgn * F(8, 3 ** r)
        res = (d.numerator * pow(d.denominator, -1, 64)) % 64
        ok3 = ok3 and (res % 16 == 5)
        fired = (F(9 + 6) - d) / 3
        pred = F(6) - sgn * F(8, 3 ** (r + 1))
        ok3 = ok3 and (fired == pred)
        # a-descendant of fired = next orbit class
        Q = fired.denominator
        a_desc = F(3 * Q - fired.numerator, Q)
        ok3 = ok3 and (a_desc == F(-3) + sgn * F(8, 3 ** (r + 1)))
# observed orbit data (smoke json if full not ready, else full)
patt = sorted(HERE.glob('levels_t5_*.json'),
               key=lambda q: int(q.stem.split('_')[-1]), reverse=True)   # largest jmax first
jdata = None
for p in patt:
    try:
        jd = json.loads(p.read_text())
        if 'orbit_free_entries' in jd:
            jdata = (p.name, jd)
            break
    except Exception:
        pass
obs_ok = jdata is not None
if obs_ok:
    name, jd = jdata
    import re as _re
    for key, classes in jd['orbit_free_entries'].items():
        r = int(key.split('^')[1]) - 1           # key = chain,3^(r+1) of the FIRED family
        for c in classes:
            mm = _re.match(r"\('?(-?\d+)/(\d+)'?,\s*(-?\d+)\)", str(c))
            if not mm:
                obs_ok = False
                continue
            dd = F(int(mm.group(1)), int(mm.group(2)))
            fired = int(mm.group(3))
            obs_ok = obs_ok and (dd in (F(-3) + F(8, 3 ** r), F(-3) - F(8, 3 ** r)))
            obs_ok = obs_ok and (fired in (6 * 3 ** (r + 1) - 8, 6 * 3 ** (r + 1) + 8))
check(3, ok3 and obs_ok, 'orbit closed form + observed data (%s)' % (jdata[0] if obs_ok else 'missing'))

# ---------------- 4: drift BFS == hand tables ----------------
DC = {(1, 1), (2, 1), (3, 1)}
DD = {(1, 1), (2, 1), (3, 1)}
DE = {(n, 1) for n in range(0, 5)} | {(10, 3)}


def shift_of(S):
    return {W.add(n, d, -2, 1) for (n, d) in S}


def bfs(root, sets):
    cur = {root}
    out = [cur]
    for S in sets:
        nxt = set()
        for (n, d) in cur:
            nxt.add(W.maps_a(n, d))
            nxt.add(W.maps_b(n, d))
            for (sn, sd) in S:
                nxt.add(W.add(n, d, sn, sd))
        cur = nxt
        out.append(cur)
    return out


HAND_E = [{(1, 1)}, {(0, 1), (1, 1), (2, 1)}, {(n, 1) for n in range(-1, 4)}, {(n, 1) for n in range(-2, 5)}]
HAND_S = [{(1, 1)},
          {(n, 1) for n in range(-1, 4)} | {(7, 3)},
          {(n, 1) for n in range(-2, 5)} | {(2, 3), (4, 3), (7, 3), (10, 3)},
          {(n, 1) for n in range(-3, 6)} | {(n, 3) for n in (-1, 1, 2, 4, 5, 7, 10, 13)},
          {(n, 1) for n in range(-4, 7)} | {(n, 3) for n in (-4, -2, -1, 1, 2, 4, 5, 7, 8, 10)}]
check(4, bfs((1, 1), [shift_of(DD), shift_of(DC), set()]) == HAND_E and
      bfs((1, 1), [shift_of(DE), shift_of(DD), shift_of(DC), set()]) == HAND_S, 'drift sets')

# ---------------- 5: bulk vs scalar ----------------
ok5 = True
FAM5 = [(10, 3, True), (-1, 3, False), (46, 9, True), (7, 3, False), (154, 27, True)]
BULK5 = {}
for (num, den, lift) in FAM5:
    B = W.bulk_rat(T, num, den, lift, 64, 3000)
    bs = set(B['uncert'])
    for j in range(64, 3000):
        c = W.certify_rat(T, j, num, den, lift)
        if c['ok'] != (j not in bs):
            ok5 = False
    BULK5[(num, den, lift)] = W.bulk_rat(T, num, den, lift, 3000, 300003)  # extend to 3e5
for (num, den, lift) in FAM5:
    bset = set(BULK5[(num, den, lift)]['uncert'])
    jsamp = sorted(rng.choice(np.arange(3000, 300003), size=2000, replace=False))
    for j in jsamp:
        c = W.certify_rat(T, int(j), num, den, lift)
        if c['ok'] != (int(j) not in bset):
            ok5 = False
ok5b = True
for d in (-3, -1, 0, 2, 5, 7):
    B1 = R.bulk(T, d, 64, 3000)
    b1 = set(B1['uncert'])
    Dv = W.trunc(d, 1)
    B2 = W.bulk_rat(T, d, 1, False, 64, 3000)
    if sorted(B2['uncert']) != sorted(b1):
        ok5b = False
check(5, ok5 and ok5b, 'bulk=scalar ([64,3000) full + [3e3,3e5) sampled 2000); integer=rwalk.bulk')

# ---------------- 6: truncation faithfulness bound (dynamic family set) ----------------
fams = [(10, 3), (26, 3), (46, 9), (62, 9), (154, 27), (170, 27), (478, 81), (494, 81),
        (-1, 3), (-17, 3), (-19, 9), (-35, 9), (-73, 27), (-89, 27), (-235, 81), (-251, 81),
        (-721, 243), (-737, 243), (-2179, 729), (-2195, 729), (-6553, 2187), (-6569, 2187),
        (-19675, 6561), (-19691, 6561), (-59041, 19683), (-59057, 19683), (7, 3), (23, 3),
        (-37, 3), (53, 9), (37, 9), (8, 9)]
fam_src = 'fixed list'
try:                                    # round-2 review: verify ALL certified families
    jd6 = json.loads((HERE / 'levels_t5_20000000.json').read_text())
    dyn = []
    for key in jd6['families']:
        a, b, l = key.split('/')
        dyn.append((int(a), int(b)))
    if dyn:
        fams = dyn
        fam_src = 'levels_t5_20000000.json (%d families)' % len(dyn)
except Exception:
    pass
js = np.arange(64, T.N, dtype=np.int64)
n = js - 1
od = T.odd[n].astype(bool)
isa = T.typ[n] == 97
sel = od & isa
k = (T.tau[n[sel]] // 2).astype(np.int64)
ok6 = True
mx6 = 0
for (num, den) in fams:
    Cn = 3 * k * den + num
    mx6 = max(mx6, int(np.abs(Cn).max()))
    if mx6 >= (1 << 53):
        ok6 = False
check(6, ok6, '|3k*den+num| < 2^53 over odd-a chains 64<=j<2e7, %d families from %s '
       '(observed max %d < 2^53)' % (len(fams), fam_src, mx6))

# ---------------- 7: T4 reproduction (level summaries) ----------------
old = json.loads((ROOT / 'work_claude_residual' / 'levels_20000000.json').read_text())
ok7 = (old['C7']['n_classes'] == 89 and old['D']['n_classes'] == 148 and
       old['C7']['uncert'][0]['cls'] == 5 and old['bulk']['5']['n_uncert'] == 1 and
       old['bulk']['5']['uncert'] == [5] and old['bulk']['-1']['n_uncert'] == 0)
# re-verify one load-bearing certificate at full range: delta=5 -> only (5,5) free
# ((5,5) itself is below BIG=64, i.e. in the scalar part; the j>=64 bulk is clean)
B5 = R.bulk(T, 5, 64, T.N + 1)
c55 = R.certify(T, 5, 5)
ok7 = ok7 and B5['uncert'] == [] and not c55['ok']
check(7, ok7, 'accepted T4 anchors + delta=5: bulk(j>=64) clean, (5,5) free')

# ---------------- 8: family closure ----------------
def descendants(c, Q):
    out = []
    for tag, nn0 in [('a', 3 * Q - c), ('b', c - Q)] + [('cs%d' % s, c + 3 * s * Q) for s in (-1, 0, 1)]:
        nn, dd = W.canon(nn0, Q)
        if dd != 1:
            out.append((nn, dd, False))
    return out


init = [(10, 3, True), (26, 3, True), (7, 3, True), (23, 3, True)]
for (c, Q) in [(10, 3), (26, 3), (46, 9), (62, 9)]:
    init += [(a, b, l) for (a, b, l) in descendants(c, Q)]
orbit_nolift = []
for r in range(1, 11):                    # r=1..10: delta_10 now inside the den-3^10 cap
    for sgn in (1, -1):
        d = F(-3) + sgn * F(8, 3 ** r)
        orbit_nolift.append((d.numerator, d.denominator, False))
        if r <= 9:
            f = F(6) - sgn * F(8, 3 ** (r + 1))
            init.append((f.numerator, f.denominator, True))
JHI = 300003
ok8 = True
famfail = []
for (num, den, lift) in dict.fromkeys(init + orbit_nolift):
    unc = []
    for j in range(5, 64):
        c = W.certify_rat(T, j, num, den, lift)
        if not c['ok']:
            unc.append(j)
    B = W.bulk_rat(T, num, den, lift, 64, JHI)
    unc += B['uncert']
    if (num, den, lift) in orbit_nolift:
        if unc != [5]:
            ok8 = False
            famfail.append((num, den, lift, unc[:4]))
    else:
        if unc:
            ok8 = False
            famfail.append((num, den, lift, unc[:4]))
# key families + ALL 20 orbit no-lift families (r=1..10) + the den-3^10 fired pair + descendants
# at FULL range (review round-1 items: the [B] base of T5-RED must cover the boundary layer)
full_list = [(10, 3, True), (26, 3, True), (46, 9, True), (62, 9, True),
             (154, 27, True), (170, 27, True), (7, 3, True), (23, 3, True)]
for f in orbit_nolift:                       # 20 orbit no-lift families (r=1..10, +/-)
    full_list.append(f)
for sgn in (1, -1):                          # den-3^10 fired families 6 -/+ 8/3^10
    fr = F(6) - sgn * F(8, 3 ** 10)
    full_list.append((fr.numerator, fr.denominator, True))
    Q = fr.denominator                       # their 5 descendants each
    for tag, nn0 in [('a', 3 * Q - fr.numerator), ('b', fr.numerator - Q)] +             [('cs%d' % s, fr.numerator + 3 * s * Q) for s in (-1, 0, 1)]:
        nn, dd = W.canon(nn0, Q)
        if dd != 1:
            full_list.append((nn, dd, False))
def bulk_chunks(num, den, lift, jlo=64, jhi=None, step=4_000_000):
    """bulk_rat over [jlo, jhi) in chunks (same computation, lower peak memory)."""
    if jhi is None:
        jhi = T.N + 1
    unc, aout, nt = [], {}, {}
    lo = jlo
    while lo < jhi:
        hi = min(lo + step, jhi)
        B = W.bulk_rat(T, num, den, lift, lo, hi)
        unc += B['uncert']
        for kk, vv in B['aout'].items():
            e = aout.setdefault(kk, [0, hi - 1]); e[0] += vv[0]
        for kk, vv in B['nt'].items():
            nt[kk] = nt.get(kk, 0) + vv
        lo = hi
    return dict(uncert=unc, aout=aout, nt=nt)


for (num, den, lift) in dict.fromkeys(full_list):
    unc = []
    for j in range(5, 64):
        c = W.certify_rat(T, j, num, den, lift)
        if not c['ok']:
            unc.append(j)
    B = bulk_chunks(num, den, lift)
    unc += B['uncert']
    d_ = F(num, den)
    is_orbit_nolift = any(d_ == F(-3) + s * F(8, 3 ** r) for r in range(1, 11) for s in (1, -1))
    if is_orbit_nolift:
        if unc != [5]:
            ok8 = False
            famfail.append(('FULL-ORBIT', num, den, lift, unc[:4]))
    elif unc:
        ok8 = False
        famfail.append(('FULL', num, den, lift, unc[:4]))
check(8, ok8, 'families: orbit no-lift uncert exactly [5]; %d families at FULL range incl. '
       'den-3^10 layer' % len(dict.fromkeys(full_list)) + ('' if ok8 else ' %r' % (famfail[:3],)))

# ---------------- 9: level E / C7-E residual lists (from computed json) ----------------
ok9 = False
if jdata is not None:
    Eunc = [u['cls'] for u in jd['E']['uncert_spec']]
    Cunc = [u['cls'] for u in jd['C7E']['uncert_spec']]
    Cint = [u['cls'] for u in jd['C7E']['uncert_int']]
    ok9 = (sorted(Eunc) == [-27, -11, 5, 21] and sorted(Cunc) == [-27, -11, 5, 21] and
           Cint == [5] and all(u['chain'] == 5 for u in jd['E']['uncert_spec'] + jd['C7E']['uncert_spec']))
check(9, ok9, 'json residual free entries == chain-5 set {5, 21(=-1/3), -27(=-17/3), -11}')

# ---------------- 9b: replay of the t=0 spec construction (theta_0 = 1) ----------------
# rebuild the S0 entries (5..63, D-1) from family exports recomputed here (smoke range),
# certify each, and assert the failing set is exactly the mod-64 residues {5,21,37,53} family.
replay_fams = [(10, 3, True), (26, 3, True), (46, 9, True), (62, 9, True), (154, 27, True),
               (170, 27, True), (7, 3, True), (23, 3, True), (37, 9, False), (53, 9, False),
               (-1, 3, False), (8, 9, False), (-37, 3, False), (19, 3, False)]
exports = {}
for (num, den, lift) in replay_fams:
    for j in range(5, 64):
        c = W.certify_rat(T, j, num, den, lift)
        ntout = {b for (_, b) in c['nt']}
        for (c2, r2) in c['aouts']:
            if c2 in ntout or c2 >= j + 1:
                continue
            exports.setdefault((c2, r2), '%d/%d%s' % (num, den, 'L' if lift else ''))
    B = W.bulk_rat(T, num, den, lift, 64, 300003)
    for (c2, r2) in B['aout']:
        exports.setdefault((c2, r2), '%d/%d%s' % (num, den, 'L' if lift else ''))
fail_res = set()
n_ent = 0
for (c, D) in sorted(exports):
    if c < 5:
        continue
    r = (1 + D - 2) % (1 << (c + 1))
    q = R.certify(T, c, r)
    n_ent += 1
    if not q['ok']:
        fail_res.add((c, r % 64))
ok9b = (n_ent > 200 and fail_res and
        all((c == 5 and rr % 16 == 5) or (c, rr) == (8, 58) for (c, rr) in fail_res) and
        {5, 21, 37, 53} <= {rr for (c, rr) in fail_res if c == 5})
check(9, ok9b, 'replay t=0: %d rebuilt entries; failures = chain-5 mod-16=5 set '
       '{5,21,37,53} (+ the known chain-8 entry (8,58), GW-fires -37/3); observed %s'
       % (n_ent, sorted(fail_res)[:8]))

# ---------------- 10: REG size inequality ----------------
Qm, Cm = 3 ** 9, 3 ** 11
# REG inequality at table scale: for all odd-a chains 64<=j<2e7 the left side stays below
# 2^62 <= 2^(j-2) (the shift itself cannot be materialised in int64; the global bound suffices)
lhs_max = int((3 * Qm * k + Cm).max())
bad = 0 if lhs_max < (1 << 62) else 1
check(10, bad == 0, 'REG inequality: max(3*3^9*k+3^11)=%d < 2^62 <= 2^(j-2) for j>=64' % lhs_max)

print()
if FAILED:
    print('FAILED CHECKS:', FAILED)
    print('ALL PASS' if False else 'NOT PASS')
    sys.exit(1)
print('ALL PASS')
sys.exit(0)
