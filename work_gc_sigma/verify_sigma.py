"""verify_sigma.py -- independent re-verification of the R4 (SIGMA) claims in NOTES.md.

Checks (each prints 'ok <name>'; ASCII only; last line ALL PASS, exit 0):
  V1  P1 re-run: integer bulk (all 19 delta values) + levels B,C,OUT,D rebuilt with the
      accepted levels.py logic and asserted field-by-field equal to the accepted
      work_claude_residual/levels_20000000.json (the accepted T4 [B] artifact); the bulk
      uncertified set is exactly {(5,5)}.
  V2  Theta^E drift sets: independent BFS (own Fraction arithmetic, no rwalk_t5 import)
      == the hand table of the accepted Lemma DL5 (level-E part); all integral.
  V3  GW / OBST closed forms exactly (Fractions):
      - every artifact family's fire arithmetic re-derived from its recorded source
        ((9+6*k5-delta)/3 with k5 = tau(4)/2 = 1 read off the table);
      - delta_r = -3 + 8/3^r == 5 (mod 16) for r = 1..12 (congruence in Z[1/3]);
      - REG descendant a of the fired family == delta_{r+1}, and both the fired family
        (with lift) and the descendant (no lift) are in the artifact family set, r = 1..9;
      - the full REG descendant set {3Q-C, C-Q, C+3sQ}/Q of 10/3 is in the family set.
  V4  fired-entry residues: for every artifact fired family and every chain m in [5,64),
      the residue of shift-value (+2^m lift bit unless 'deep') mod 2^{m+1} is present in
      the artifact's Sigma_{<T4>} chain-m residue set.
  V5  family-set consistency: every family of sigma4_20000000.json lies in the accepted
      T5 artifact's 134-family closure (levels_t5_20000000.json); spot re-certification of
      five load-bearing families over the full table with the accepted rwalk_t5 machinery
      (with-lift families certified at every chain; no-lift orbit families free only at
      chain 5; zero bulk failures).
  V6  independent classifier + invariant logic over the artifact's residue sets:
      baseline (h <= 3) has zero out-of-list residues; Sigma_{<T4>} has out-of-list
      residues in exactly the artifact's count; the fired values include the first precise
      violations 1/3, -5/3, 13/3 (den 3, outside {4/3,-7/3}) and 28/9 (den 9, 3-height 2);
      denominators reach 3^10 with beyond-cap fires logged (the orbit does not close);
      the baseline_ok flags are all true; the exact integer set of Sigma_{<T4} is [-3,3].
  V7  realised shifts: independent full-table recomputation of the (omega, shift-class)
      cross-tab of all odd c crossings n < 2*10^7 == the artifact's table; omega >= 5
      gives exactly {0}; all realised classes lie in {-1, 0}.
  V8  possible-value sets: deep/a-landing shift values re-derived from the hand drift
      tables == the artifact's deep_values (<=N0 empty; <T1 {0}; <T3 gains exactly 2;
      <T4 = [-3,3]); artifact covers the full table.

Usage: PYTHONUTF8=1 <python> -B work_gc_sigma/verify_sigma.py        (from D:/math_cc)
"""
import sys, json, time
from pathlib import Path
from fractions import Fraction

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
sys.path.insert(0, str(ROOT / 'work_gc_level_t5'))
import numpy as np
import rwalk as R          # accepted T4 machinery (read-only)
import rwalk_t5 as W       # accepted T5 machinery (read-only)

T0 = time.time()
JMAX_EXPECT = 20000000
ART = json.loads((HERE / ('sigma4_%d.json' % JMAX_EXPECT)).read_text(encoding='utf-8'))
ACC = json.loads((ROOT / 'work_claude_residual' / 'levels_20000000.json').read_text(encoding='utf-8'))
T5 = json.loads((ROOT / 'work_gc_level_t5' / 'levels_t5_20000000.json').read_text(encoding='utf-8'))
FAIL = []


def check(name, cond, info=''):
    if cond:
        print('ok %s (%.0fs) %s' % (name, time.time() - T0, info), flush=True)
    else:
        FAIL.append(name)
        print('FAIL %s %s' % (name, info), flush=True)


def sym(r, c):
    M = 1 << (c + 1)
    r %= M
    return r - M if r > M // 2 else r


# ---------------- V1: P1 re-run and reproduction of the accepted T4 levels ----------------
T = R.Table()
INTS = list(range(-8, 11))
E = {}; UNC = {}
for d in INTS:
    agg = {}; unc = []
    for j in range(5, R.BIG):
        c = R.certify(T, j, d)
        if not c['ok']:
            unc.append(j)
        for a in c['aouts']:
            agg.setdefault(a, [0, ('bulk', d, j)])[0] += 1
    B = R.bulk(T, d, R.BIG, T.N + 1)
    unc += B['uncert']
    for k, v in B['aout'].items():
        e = agg.setdefault(k, [0, ('bulk', d, v[1])]); e[0] += v[0]
    E[d] = agg; UNC[d] = unc
summary = {}
memo = {}


def cert_specific(c, r):
    key = (c, r % (1 << (c + 1)))
    if key not in memo:
        memo[key] = R.certify(T, c, sym(r, c))
    return memo[key]


def level(name, plan, ints, generic_out):
    all_ints = {}; spec = {}
    for d in ints:
        all_ints.setdefault(d, (name, 'a/b-landing'))
    for Ep, Gp, ds, tag in plan:
        for d in ds:
            for g in Gp:
                all_ints.setdefault(d + g - 2, (name, tag, 'generic', d, g))
            for (c, D), prov in Ep.items():
                if c < 5:
                    continue
                r = (d + D - 2) % (1 << (c + 1))
                spec.setdefault((c, r), (name, tag, d, c, sym(D, c), prov))
    unc = []; Eo = {}
    for d, prov in sorted(all_ints.items()):
        if UNC[d]:
            unc.append(dict(kind='all-chain integer', cls=d, chains=UNC[d][:10], why=prov))
        for k, v in E[d].items():
            Eo.setdefault(k, v[1])
    for (c, r), prov in spec.items():
        s = sym(r, c)
        if s in INTS and s in all_ints:
            continue
        q = cert_specific(c, r)
        if not q['ok']:
            unc.append(dict(kind='specific', chain=c, cls=s, status=q['status'],
                            word=q['word'][:12], why=prov))
            continue
        for a in q['aouts']:
            Eo.setdefault(a, ('spec', name, c, s))
    summary[name] = dict(n_classes=len(Eo), generic_out=sorted(generic_out),
                         all_chain_integer_entries=sorted(all_ints), uncert=unc,
                         chain5=sorted({sym(r, c) for (c, r) in Eo if c == 5}),
                         exotic=sorted({(c, sym(r, c)) for (c, r) in Eo
                                        if sym(r, c) not in range(-20, 21)}))
    return Eo, set(generic_out)


def U(*Es):
    out = {}
    for Ed in Es:
        for k, v in Ed.items():
            out.setdefault(k, v)
    return out


EA = {k: v[1] for k, v in E[1].items()}; GA = set()
EB, GB = level('B', [(EA, GA, [1], 'root-c')], [2, 0], {2})
EAB, GAB = U(EA, EB), GA | GB
EC, GC = level('C', [(EAB, GAB, [1], 'root-c'), (EA, GA, [0, 2], 'depth2-c')],
               [2, 0, 3, 1, -1], {1, 2, 3})
EABC, GABC = U(EAB, EC), GAB | GC
shapeD = lambda tag: [(EABC, GABC, [1], tag + '0'), (EAB, GAB, [0, 1, 2], tag + '1'),
                      (EA, GA, [-1, 0, 1, 2, 3], tag + '2')]
EO, GO = level('OUT', shapeD('L'), list(range(-2, 5)), {0, 1, 2, 3, 4})
ED, GD = level('D', shapeD('depth'), list(range(-2, 5)), {0, 1, 2, 3, 4})


def _norm(x):
    def _n(v):
        if isinstance(v, (tuple, list)):
            return [_n(w) for w in v]
        if isinstance(v, dict):
            return {k: _n(w) for k, w in v.items()}
        return v
    return _n(x)


okrep = (ACC['A']['n_classes'] == len(EA)
         and ACC['A']['chain5'] == sorted({sym(r, 5) for (c, r) in EA if c == 5}))
for name in ('B', 'C', 'OUT', 'D'):
    m = summary[name]
    okrep = okrep and (ACC[name]['n_classes'] == m['n_classes']
                       and ACC[name]['chain5'] == m['chain5']
                       and ACC[name]['exotic'] == _norm(m['exotic'])
                       and ACC[name]['uncert'] == _norm(m['uncert'])
                       and ACC[name]['generic_out'] == m['generic_out']
                       and ACC[name]['all_chain_integer_entries'] == m['all_chain_integer_entries'])
check('V1a_P1_reproduction_vs_levels_20000000', okrep)
check('V1b_bulk_uncert_exactly_5_at_chain5',
      all(UNC[d] == ([5] if d == 5 else []) for d in INTS),
      str({d: UNC[d] for d in INTS if UNC[d]}))

# ---------------- V2: Theta^E independent BFS ----------------
def bfsE():
    D_C = {Fraction(n) for n in (1, 2, 3)}
    D_D = {Fraction(n) for n in (1, 2, 3)}
    S_D = {d - 2 for d in D_D}
    S_C = {d - 2 for d in D_C}
    cur = {Fraction(1)}
    out = [set(cur)]
    for S in (S_D, S_C, set()):
        nxt = set()
        for th in cur:
            nxt.add(Fraction(3) - th)
            nxt.add(th - 1)
            for s in S:
                nxt.add(th + s)
        cur = nxt
        out.append(set(cur))
    return out


TH_E = bfsE()
HAND_E = [{Fraction(1)},
          {Fraction(n) for n in (0, 1, 2)},
          {Fraction(n) for n in range(-1, 4)},
          {Fraction(n) for n in range(-2, 5)}]
check('V2a_ThetaE_bfs_equals_hand_table', TH_E == HAND_E)
check('V2b_ThetaE_integral', all(v.denominator == 1 for S in TH_E for v in S))

# ---------------- V3: GW / OBST closed forms ----------------
check('V3a_k5_is_1', int(T.tau[4]) // 2 == 1 and chr(T.typ[4]) == 'a' and bool(T.odd[4]))
K5 = 1
fam = dict(ART['families'])


def fire_cls(delta, k=K5):
    return (Fraction(9 + 6 * k) - delta) / 3


ok3 = True
nfire = 0
for key, why in fam.items():
    if 'GW fire' not in why:
        continue
    nfire += 1
    num, den, lift = (int(x) for x in key.split('/'))
    dstr = why.split('delta=')[1].rstrip(')')
    ok3 = ok3 and (fire_cls(Fraction(dstr)) == Fraction(num, den))
check('V3b_fire_arithmetic_from_recorded_sources', ok3, '%d fired families' % nfire)


def cong_mod16(x, target):
    d = x.denominator
    if d % 2 == 0:
        return False
    num = (x.numerator - target * d) % 16
    return (num * pow(d, -1, 16)) % 16 == 0


check('V3c_orbit_delta_r_eq_5_mod16',
      all(cong_mod16(Fraction(-3) + Fraction(8, 3 ** r), 5) for r in range(1, 13)))
ok3 = True
for r in range(1, 10):
    dr = Fraction(-3) + Fraction(8, 3 ** r)
    fired = fire_cls(dr)                             # 6 - 8/3^{r+1}
    desca = Fraction(3) - fired                      # REG descendant a (3Q-C)/Q with Q=3^{r+1}
    ok3 = ok3 and (desca == Fraction(-3) + Fraction(8, 3 ** (r + 1)))
    ok3 = ok3 and ('%d/%d/1' % (fired.numerator, fired.denominator) in fam)
    ok3 = ok3 and ('%d/%d/0' % (desca.numerator, desca.denominator) in fam)
check('V3d_desc_a_recursion_and_family_presence', ok3, 'r=1..9')
desc = {Fraction(3 * 3 - 10, 3), Fraction(10 - 3, 3)} | \
       {Fraction(10 + 3 * s * 3, 3) for s in (-1, 0, 1)}
present = {'%d/%d/0' % (v.numerator, v.denominator) for v in desc}
check('V3e_REG_descendant_set_of_10/3_in_families', present <= set(fam), str(sorted(present)))

# ---------------- V4: family certificates (round-1 fix: check the CERTIFICATES, not the
# synthesised table against itself) ----------------
ok4 = True
nfre = 0
for fkey in sorted(ART['families']):
    num, den, lift = (int(x) for x in fkey.split('/'))
    unc = []
    for m in range(5, 64):
        c = W.certify_rat(T, m, num, den, bool(lift))
        if not c['ok']:
            unc.append((m, c['status']))
    art_unc = [(int(j), st) for (j, st, w) in ART['family_unc'][fkey]['unc_s']]
    ok4 = ok4 and (unc == art_unc)
    if bool(lift):
        ok4 = ok4 and (unc == [])          # with-lift families certified at every chain 5..63
    else:
        nfre += len(unc)
check('V4a_all_families_scalar_certification_matches_artifact', ok4,
      'no-lift unc entries total=%d' % nfre)
ok4 = True
kinds = {}
for fkey, (vstr, mlo, mhi, kind) in ART['fired_shift_ranges'].items():
    kinds[kind] = kinds.get(kind, 0) + 1
    num, den, lift = (int(x) for x in fkey.split('/'))
    if kind == 'top':
        ok4 = ok4 and (mlo == 5 and mhi == JMAX_EXPECT and lift == 1)
    elif kind == 'orbit':
        ok4 = ok4 and (mlo == 5 and mhi == 64 and lift == 1)
    else:
        ok4 = ok4 and (kind == 'deep' and mlo == 5 and mhi == 54 and lift == 0)
check('V4b_fired_shift_ranges_structure', ok4 and kinds.get('top', 0) >= 1
      and kinds.get('orbit', 0) >= 1, str(kinds))
sig4 = {int(c): set(v) for c, v in ART['sigma']['<T4'].items()}
ok4 = True
n4 = 0
for fkey, (vstr, mlo, mhi, kind) in ART['fired_shift_ranges'].items():
    sv = Fraction(vstr)
    for m in range(mlo, min(mhi, 64)):
        r = (sv.numerator * pow(sv.denominator, -1, 1 << (m + 1))) % (1 << (m + 1))
        if kind != 'deep':
            r = (r + (1 << m)) % (1 << (m + 1))
        if sym(r, m) not in sig4.get(m, set()):
            ok4 = False
            n4 += 1
check('V4c_fired_residues_present_in_spectrum', ok4, 'missing=%d' % n4)

# ---------------- V5: consistency with the accepted T5 artifact + spot re-certification ----
t5fams = set(T5['families'].keys())
mine = set(fam.keys())
spine = set()
for r in range(1, 11):                       # no-lift delta_r: den 3^r <= 3^10
    dr = Fraction(-3) + Fraction(8, 3 ** r)
    spine.add('%d/%d/0' % (dr.numerator, dr.denominator))
for r in range(1, 10):                       # fired family of delta_r: den 3^{r+1} <= 3^10
    dr = Fraction(-3) + Fraction(8, 3 ** r)
    fired = fire_cls(dr)
    spine.add('%d/%d/1' % (fired.numerator, fired.denominator))
check('V5a_orbit_spine_in_both_closures', spine <= mine and spine <= t5fams,
      'spine=%d mine=%d t5=%d mine-only=%s' %
      (len(spine), len(mine), len(t5fams), sorted(mine - t5fams)))
spots = [(10, 3, True), (-1, 3, False), (46, 9, True), (154, 27, True), (354286, 59049, True)]
ok5 = True
info5 = []
for (num, den, lift) in spots:
    unc_s = []
    for j in range(5, 64):
        c = W.certify_rat(T, j, num, den, lift)
        if not c['ok']:
            unc_s.append((j, c['status']))
    B = W.bulk_rat(T, num, den, lift, 64, T.N + 1)
    ok5 = ok5 and (len(B['uncert']) == 0)
    if lift:
        ok5 = ok5 and (unc_s == [])
    else:
        ok5 = ok5 and ([j for (j, st) in unc_s] == [5])
    info5.append('%d/%d/%d:unc_s=%s,bulk_unc=%d' % (num, den, lift, unc_s, len(B['uncert'])))
check('V5b_spot_recertification_5_families', ok5, '; '.join(info5))

# ---------------- V6: independent classifier + invariant logic ----------------
ECAP = 10
VCAP = 64


def reps(c, s):
    out = []
    M = 1 << (c + 1)
    for e in range(0, ECAP + 1):
        den = 3 ** e
        for m in [None] + list(range(5, min(c, 64) + 1)):
            t = (s - (1 << m)) % M if m is not None else s % M
            num = (t * den) % M
            if num > M // 2:
                num -= M
            v = Fraction(num, den)
            if abs(v) <= VCAP:
                out.append((v, m))
    return out


def in_list(v, m):
    return ((v.denominator == 1 and m is None and abs(v) <= 16) or v == Fraction(4, 3)
            or (v == Fraction(-7, 3) and m is None))


def in_list_fast(c, s):
    '''exact integer twin of any(in_list(v,m) for (v,m) in reps(c,s)):
    a Fraction rep (num/3^e, m) with v reduced equals one of the three value conditions,
    and each value condition is a congruence on s:
      (k, None) with |k|<=16  <=>  |s| <= 16 (s is already the symmetric residue);
      (4/3, m) m in [5,min(c,64)] or None
                             <=>  (s - 2^m) mod 2^{c+1} == 4*inv3  for such m;
      (-7/3, None)            <=>  s == sym(-7*inv3, c).
    (Fraction auto-reduction cannot create values outside these congruence classes: an
    e>0 rep reducing to the integer k satisfies k = s mod 2^{c+1}, caught by the first.)'''
    if abs(s) <= 16:
        return True
    M = 1 << (c + 1)
    inv3 = pow(3, -1, M)
    t4 = (4 * inv3) % M
    if s % M == t4:                        # bare 4/3 (m=None) -- L_GW ignores the lift position
        return True
    if s % M == (-7 * inv3) % M:           # -7/3 with m=None (both sides in [0, M))
        return True
    for m in range(5, min(c, 64) + 1):
        if (s - (1 << m)) % M == t4:
            return True
    return False


bad = {k: [] for k in ('<T1', '<T2', '<T3', '<T4')}
for k in bad:
    for c, vs in ART['sigma'][k].items():
        for s in vs:
            if not in_list_fast(int(c), s):
                bad[k].append((int(c), s))
# equivalence spot check against the Fraction implementation (sampled)
import random
rng = random.Random(12345)
pool = [(int(c), s) for k in ('<T4',) for c, vs in ART['sigma'][k].items() for s in vs]
sample = pool                      # full equivalence over every <T4 residue (not a sample)
okfast = all(in_list_fast(c, s) == any(in_list(v, m) for (v, m) in reps(c, s))
             for (c, s) in sample)
check('V6a0_fast_classifier_fully_equivalent', okfast, 'n=%d' % len(sample))
check('V6a_baseline_h_le_3_zero_out_of_list',
      all(len(bad[k]) == 0 for k in ('<T1', '<T2', '<T3')),
      str({k: len(bad[k]) for k in bad}))
check('V6b_T4_out_of_list_nonempty_and_count_matches',
      len(bad['<T4']) == ART['invariants']['rat_<T4']['n_bad'] and len(bad['<T4']) > 0,
      'n=%d' % len(bad['<T4']))
fired_vals = {Fraction(v[0]) for v in ART['fired_shift_ranges'].values()}
check('V6c_first_violation_values_present',
      {Fraction(1, 3), Fraction(-5, 3), Fraction(28, 9), Fraction(13, 3)} <= fired_vals)
maxden = max(v.denominator for v in fired_vals)
fbk = [(x[0], x[1], x[2]) for x in ART['fire_beyond_cap']]
check('V6d_den_reaches_3pow10_and_beyond_cap_fires',
      maxden == 3 ** 10 and len(fbk) > 0 and len(set(fbk)) == len(fbk)
      and max(x[1] for x in fbk) == 3 ** 11,
      'maxden=%d beyond_distinct=%d note=%s'
      % (maxden, len(fbk), ART.get('fire_beyond_cap_note', '')))
check('V6e_baseline_ok_flags_all_true', all(ART['baseline_ok'].values()), str(ART['baseline_ok']))
check('V6f_tier1_violations_nonempty', ART['invariants']['tier1_<T4']['n_bad'] > 0,
      'n=%d' % ART['invariants']['tier1_<T4']['n_bad'])
check('V6g_int_T4_sets',
      set(Fraction(x) for x in ART['invariants']['int_<T4']['exact_structural']) ==
      {Fraction(n) for n in range(-3, 4)}
      and set(Fraction(x) for x in ART['invariants']['int_<T4']['witnessed_core']) ==
      {Fraction(n) for n in (-4, -3, -2, -1, 0, 1, 3, 4)}
      and set(Fraction(x) for x in ART['invariants']['int_<T4']['union']) ==
      {Fraction(n) for n in range(-4, 5)}
      and not ART['invariants']['int_<T4']['ok_pm1_union']
      and not ART['invariants']['int_<T4']['ok_lc_union'],
      str(ART['invariants']['int_<T4']['union']))
check('V6h_den3_height_measure',
      ART['measurements']['<T3']['max_min_den3_exp'] <= 1
      and ART['measurements']['<T4']['max_min_den3_exp'] == 10
      and ART['M_h']['<T4']['fired_range'] == [5, JMAX_EXPECT],
      'T3=%d T4=%d' % (ART['measurements']['<T3']['max_min_den3_exp'],
                       ART['measurements']['<T4']['max_min_den3_exp']))

# ---------------- V7: realised shifts, independent recomputation ----------------
oddc = np.nonzero(T.odd.astype(bool) & (T.typ == 99))[0]
lamY = T.lY[oddc]
lam = T.lam[oddc]
lv = (lam & (-lam)).astype(np.int64)
om = np.rint(np.log2(lv.astype(np.float64))).astype(np.int64)
sres = (-1 - lamY) % ((np.int64(1) << (om + 1)))
real = {}
for o, s in zip(om.tolist(), sres.tolist()):
    key = (int(o), sym(int(s), int(o)))
    real[key] = real.get(key, 0) + 1
check('V7a_realised_crosstab_matches_artifact',
      {('%d,%d' % k): v for k, v in sorted(real.items())} == ART['realized'],
      str(sorted(real.items())))
check('V7b_omega_ge5_shifts_exactly_0', sorted({s for (o, s) in real if o >= 5}) == [0])
check('V7c_all_realised_in_-1_0', sorted({s for (o, s) in real}) == [-1, 0])

# ---------------- V8: possible-value (deep/a-landing) sets ----------------
def landing_shifts(Thetas):
    out = set()
    for S in Thetas:
        for th in S:
            out.add(Fraction(1) - th)
    return out


TH_B = [{Fraction(1)}]
TH_C = [{Fraction(1)}, {Fraction(n) for n in (0, 1, 2)}]
TH_D = [{Fraction(1)}, {Fraction(n) for n in (0, 1, 2)}, {Fraction(n) for n in range(-1, 4)}]
dv = {k: {Fraction(x) for x in ART['deep_values'][k]} for k in ART['deep_values']}
deepBCD = {Fraction(n - 2) for n in (1, 2, 3)}
check('V8a_deep_values_formulas',
      dv['<=N0'] == {Fraction(0)} and dv['<T1'] == landing_shifts(TH_B[:1])
      and dv['<T2'] == deepBCD | landing_shifts(TH_C)
      and dv['<T3'] == deepBCD | landing_shifts(TH_D)
      and dv['<T4'] == ({Fraction(n - 2) for n in range(0, 5)} | landing_shifts(HAND_E)),
      str({k: sorted(v) for k, v in dv.items()}))
check('V8b_T3_possible_reading_adds_exactly_2',
      Fraction(2) in dv['<T3']
      and ART['ints_witnessed']['<T3'] == [str(Fraction(n)) for n in (-3, -2, -1, 0, 1, 3)])
check('V8c_artifact_scope_full_table',
      ART['jmax'] == JMAX_EXPECT and ART['scope'].startswith('[B] canonical table'))

print()
if FAIL:
    print('FAILED:', FAIL)
    sys.exit(1)
print('ALL PASS')
sys.exit(0)
