"""levels_t5.py -- LEVEL-T5 computation: level E (sources T3<=Q<T4), the S(J) landing families
for T4<=J<T5, the exact drift sets, and the gateway-tower closure.

Structure (NOTES.md sections referenced as N<x>):
  Phase 1  reproduce the accepted T4 level computation (levels.py logic verbatim):
           integer bulk INTS=[-8,10], levels A,B,C,OUT,D, C7(J<T4); assert the summaries match
           the accepted levels_20000000.json.
  Phase 2  drift BFS: exact deep drift sets Theta^E_t (level E) and Theta_t (S(J), T4<=J<T5)
           from the hand shift sets (N3); assert == the hand tables.
  Phase 3  rational families: all-chain no-lift {num/den} and with-lift {num/den+2^j} bulk
           certificates for the families required by level E and S(J) (N4); tower closure.
  Phase 4  level E: over-approximated entries (ints / rationals / specific c-entries /
           gateway families), walks, exports E_E; uncert report (N5).
  Phase 5  C7-E: the S(J) landing families (ints / rationals / specific / with-lift copies);
           uncert report -- must be exactly the absorbed bare-tie set (N6).
  Output:  levels_t5.json + console log.

Usage: python -B work_gc_level_t5/levels_t5.py [jmax]     (jmax default = table size)
"""
import sys, json, time
from pathlib import Path
from fractions import Fraction
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
import numpy as np
import rwalk as R
import rwalk_t5 as W

T0 = time.time()
T = R.Table()
JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else T.N
INTS = list(range(-8, 11))
LOG = []

def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)

# ============================ Phase 1: T4 levels (accepted reproduction) ============================
def sym(r, c):
    M = 1 << (c + 1); r %= M
    return r - M if r > M // 2 else r

E = {}; UNC = {}; NT = {}
for d in INTS:
    agg = {}; unc = []; ntc = {}
    for j in range(5, min(R.BIG, JMAX + 1)):
        c = R.certify(T, j, d)
        if not c['ok']:
            unc.append(j)
        for a in c['aouts']:
            e = agg.setdefault(a, [0, ('bulk', d, j)]); e[0] += 1
        for q in c['nt']:
            ntc[q] = ntc.get(q, 0) + 1
    if JMAX >= R.BIG:
        B = R.bulk(T, d, R.BIG, JMAX + 1)
        unc += B['uncert']
        for k, v in B['aout'].items():
            e = agg.setdefault(k, [0, ('bulk', d, v[1])]); e[0] += v[0]
        for q, v in B['nt'].items():
            ntc[q] = ntc.get(q, 0) + v
    E[d] = agg; UNC[d] = unc; NT[d] = ntc
log('P1 integer bulk done', round(time.time() - T0, 1))

memo = {}
def cert_specific(c, r):
    key = (c, r % (1 << (c + 1)))
    if key not in memo:
        memo[key] = R.certify(T, c, sym(r, c))
    return memo[key]

summary = {}
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
        assert d in INTS, ('integer entry outside bulk range', d)
        if UNC[d]:
            unc.append(dict(kind='all-chain integer', cls=d, chains=UNC[d][:10], why=prov))
        for k, v in E[d].items():
            Eo.setdefault(k, v[1])
    n_spec = 0
    for (c, r), prov in spec.items():
        s = sym(r, c)
        if s in INTS and s in all_ints:
            continue
        n_spec += 1
        q = cert_specific(c, r)
        if not q['ok']:
            unc.append(dict(kind='specific', chain=c, cls=s, status=q['status'], word=q['word'][:12], why=prov))
            continue
        for a in q['aouts']:
            Eo.setdefault(a, ('spec', name, c, s))
    summary[name] = dict(n_classes=len(Eo), generic_out=sorted(generic_out),
                         all_chain_integer_entries=sorted(all_ints), n_specific_entries=n_spec,
                         uncert=unc, chain5=sorted({sym(r, c) for (c, r) in Eo if c == 5}),
                         exotic=sorted({(c, sym(r, c)) for (c, r) in Eo if sym(r, c) not in range(-20, 21)}))
    log('P1 level', name, 'classes', len(Eo), 'specific', n_spec, 'uncert', len(unc), round(time.time() - T0, 1))
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
EC, GC = level('C', [(EAB, GAB, [1], 'root-c'), (EA, GA, [0, 2], 'depth2-c')], [2, 0, 3, 1, -1], {1, 2, 3})
EABC, GABC = U(EAB, EC), GAB | GC

def shapeD(tag):
    return [(EABC, GABC, [1], tag + '0'), (EAB, GAB, [0, 1, 2], tag + '1'), (EA, GA, [-1, 0, 1, 2, 3], tag + '2')]

EO, GO = level('OUT', shapeD('L'), list(range(-2, 5)), {0, 1, 2, 3, 4})
ED, GD = level('D', shapeD('depth'), list(range(-2, 5)), {0, 1, 2, 3, 4})
EABCD, GABCD = U(EABC, ED), GABC | GD
EL, GL = level('C7', [(EABCD, GABCD, [1], 't0'), (EABC, GABC, [0, 1, 2], 't1'), (EAB, GAB, [-1, 0, 1, 2, 3], 't2'),
                      (EA, GA, list(range(-2, 5)), 't3')], [], set())

# assert equality with the accepted T4 json (exotic normalised tuple->list)
def _norm(x):
    def _n(v):
        if isinstance(v, tuple):
            return [_n(w) for w in v]
        if isinstance(v, list):
            return [_n(w) for w in v]
        if isinstance(v, dict):
            return {k: _n(w) for k, w in v.items()}
        return v
    return _n(x)
old = json.loads((ROOT / 'work_claude_residual' / 'levels_20000000.json').read_text())
if JMAX != T.N:
    log('P1 SKIP reproduction assert (jmax truncated for smoke test)')
for name in (() if JMAX != T.N else ('A', 'B', 'C', 'OUT', 'D', 'C7')):
    mine = summary.get(name)
    if name == 'A':
        ok = (old['A']['n_classes'] == len(EA) and old['A']['chain5'] == sorted({sym(r, 5) for (c, r) in EA if c == 5}))
    else:
        ok = (old[name]['n_classes'] == mine['n_classes'] and old[name]['chain5'] == mine['chain5']
              and old[name]['exotic'] == _norm(mine['exotic']) and old[name]['uncert'] == _norm(mine['uncert'])
              and old[name]['generic_out'] == mine['generic_out']
              and old[name]['all_chain_integer_entries'] == mine['all_chain_integer_entries'])
    if not ok:
        log('P1 REPRODUCTION DIFF', name)
        for f in ('n_classes', 'chain5', 'exotic', 'uncert', 'generic_out', 'all_chain_integer_entries'):
            mv = mine.get(f) if name != 'A' else None
            ov = old[name].get(f)
            if isinstance(mv, list):
                mv = _norm(mv)
            if mv != ov:
                log('  field', f, 'mine=', str(mv)[:300], ' old=', str(ov)[:300])
        raise AssertionError('T4 reproduction mismatch %s' % name)
log('P1 T4 reproduction matches levels_20000000.json (levels A,B,C,OUT,D,C7)', round(time.time() - T0, 1))

# ============================ Phase 2: exact drift sets (NOTES N3) ============================
# Deep a-output class sets of the sources, by level (NOTES N3.2):
#   D_C (T1<=Q<T2) = {1,2,3}                [T4 DL(iii)]
#   D_D (T2<=Q<T3) = {1,2,3}                [no deep-entered bare tie in level D; N3.2]
#   D_E (T3<=Q<T4) = [0,4] u {10/3}         [integer drifts only in level E; 10/3 = the chain-3
#                                             (5,5) catapult output at the single deep chain m=N0]
DC_SET = {(1, 1), (2, 1), (3, 1)}
DD_SET = {(1, 1), (2, 1), (3, 1)}
DE_SET = {(n, 1) for n in range(0, 5)} | {(10, 3)}

def shift_of(Dset):
    return {W.add(n, d, -2, 1) for (n, d) in Dset}

def bfs(root, shift_sets):
    """Theta_0 = root; Theta_{t+1} = {3-th} u {th-1} u {th+s : s in shift_sets[t]}."""
    cur = {root}
    out = [cur]
    for S in shift_sets:
        nxt = set()
        for (n, d) in cur:
            nxt.add(W.maps_a(n, d)); nxt.add(W.maps_b(n, d))
            for (sn, sd) in S:
                nxt.add(W.add(n, d, sn, sd))
        cur = nxt
        out.append(cur)
    return out                      # Theta_0..Theta_len(shift_sets); caller passes one set per
                                    # update INTO deep chains 1..T (chain T+1 is never deep)

def show(S):
    ints = sorted(n for (n, d) in S if d == 1)
    rats = sorted('%d/%d' % (n, d) for (n, d) in S if d != 1)
    return ints, rats

TH_E = bfs((1, 1), [shift_of(DD_SET), shift_of(DC_SET), set()])
TH_S = bfs((1, 1), [shift_of(DE_SET), shift_of(DD_SET), shift_of(DC_SET), set()])
# hand tables (NOTES N3.3-N3.4); zero-margin check: code == hand
HAND_E = [
    {(1, 1)},
    {(0, 1), (1, 1), (2, 1)},
    {(n, 1) for n in range(-1, 4)},
    {(n, 1) for n in range(-2, 5)},
]
HAND_S = [
    {(1, 1)},
    {(n, 1) for n in range(-1, 4)} | {(7, 3)},
    {(n, 1) for n in range(-2, 5)} | {(2, 3), (4, 3), (7, 3), (10, 3)},
    {(n, 1) for n in range(-3, 6)} | {(n, 3) for n in (-1, 1, 2, 4, 5, 7, 10, 13)},
    {(n, 1) for n in range(-4, 7)} | {(n, 3) for n in (-4, -2, -1, 1, 2, 4, 5, 7, 8, 10)},
]
assert TH_E == HAND_E, ('level E drift mismatch', [show(s) for s in TH_E])
assert TH_S == HAND_S, ('S(J) drift mismatch')
log('P2 drift sets: level E ints', [show(s)[0] for s in TH_E], 'S(J) ints', [show(s)[0] for s in TH_S])
log('P2 S(J) rational drifts by t:', [show(s)[1] for s in TH_S])

# ============================ Phases 3-5: families, level E, C7-E (fixpoint) ====================
# A family (num, den, lift) certifies the entry (j, num/den (+2^j)) at EVERY chain j < JMAX
# (j<64: exact residue scalar; j>=64: 56-bit truncation bulk).  Every UNCERTIFIED entry (j, delta)
# at a table chain j fires the NT gateway (Theorem S non-descent map; r1r2 Lemma 2.3 is the
# special case j=5, k=1): the next output has class
#       (9+6*k_j - delta)/3 + 2^m     (delta integer; numerator 9+6k_j-delta over 3), resp.
#       (9Q + 6*k_j*Q - C)/(3Q) + 2^m (delta = C/Q),
# at chain m = v2(Z), Z the provenance sum (Lemma GW, NOTES N4.3).  The fired families'
# walks are certified in turn; their failures fire again (fixpoint).

from fractions import Fraction as Frac


def k_of(j):
    return int(T.tau[j - 1]) // 2


def fire(j, delta):
    """NT-gateway family for the free entry (j, delta) (delta = exact Fraction class)."""
    val = Frac(9 + 6 * k_of(j)) - delta
    nn, dd = W.canon(val.numerator, 3 * val.denominator)
    return (nn, dd, True, 'NT-gateway from free entry (j=%d, delta=%s)' % (j, delta))


RAT_MEMO = {}


def family_cert(num, den, lift, jhi=None):
    if jhi is None:
        jhi = JMAX + 1
    key = (num, den, lift, jhi)
    if key in RAT_MEMO:
        return RAT_MEMO[key]
    unc_s = []
    aout_s = {}
    for j in range(5, 64):
        c = W.certify_rat(T, j, num, den, lift)
        if not c['ok']:
            unc_s.append((j, c['status'], tuple(c['word'][:8])))
            continue
        ntout = {b for (_, b) in c['nt']}          # NT/climb outputs: representative artifact,
        for (c2, r2) in c['aouts']:                # class unreliable -> excluded from exports
            if c2 in ntout or c2 >= j + 1:
                continue
            aout_s.setdefault((c2, r2), 0)
            aout_s[(c2, r2)] += 1
    B = W.bulk_rat(T, num, den, lift, 64, jhi) if jhi > 64 else {'aout': {}, 'uncert': [], 'nt': {}}
    aout_all = dict(B.get('aout', {}))
    for k, v in aout_s.items():
        e = aout_all.setdefault(k, [0, 5])
        e[0] += v
    d = dict(num=num, den=den, lift=lift, unc_s=unc_s, unc_b=B.get('uncert', []),
             aout=aout_all, nt=B.get('nt', {}))
    RAT_MEMO[key] = d
    return d


def initial_families():
    out = []
    for t in range(1, 5):
        for (n, dd) in TH_S[t]:
            for (nn, ddd) in [(3 * dd - n, dd), (n - dd, dd)]:
                nn, ddd = W.canon(nn, ddd)
                if ddd != 1:
                    out.append((nn, ddd, False, 'S(J) landing class t%d' % t))
    out.append((10, 3, True, 'gateway (10-2^m)/3'))
    out.append((26, 3, True, 'gateway (26-2^m)/3 (covered for safety)'))
    for (c, Q) in [(10, 3), (26, 3)]:
        nn, ddd = W.canon(Q + c - 2 * Q, Q)
        out.append((nn, ddd, True, 'S(J) t0 copy of gateway %d/%d' % (c, Q)))
    return out


def descendants(c, Q):
    out = []
    for tag, nn0 in [('a', 3 * Q - c), ('b', c - Q)] + [('cs%d' % s, c + 3 * s * Q) for s in (-1, 0, 1)]:
        nn, ddd = W.canon(nn0, Q)
        if ddd != 1:
            out.append((nn, ddd, False, 'deep-m %d/%d descendant %s' % (c, Q, tag)))
    return out


FAM_SET = {}
ORBIT = {}          # tower-level data: depth r = log3(den) -> free-entry classes at each chain
FIRE_LOG = []

def add_fam(fam, record=True):
    (num, den, lift, why) = fam
    if den > 3 ** 10:
        if record:
            FIRE_LOG.append((num, den, lift, why))   # beyond the cap: obstruction data
        return False
    if (num, den, lift) not in FAM_SET:
        FAM_SET[(num, den, lift)] = why
        return True
    return False


def certify_families():
    """closure within den <= 3^9; free entries beyond the cap are logged as obstruction data."""
    for _ in range(80):
        changed = False
        for key in sorted(list(FAM_SET)):
            num, den, lift = key
            d = family_cert(num, den, lift)
            for (j, st, w) in d['unc_s']:
                delta = W.sym_rep(num, den, j)
                if lift:
                    delta = (delta + (1 << j)) % (1 << (j + 1))
                    delta = delta - (1 << (j + 1)) if delta > (1 << j) else delta
                fam = fire(j, Frac(delta, 1) if den == 1 else Frac(num, den))
                r = (fam[0], fam[1])
                ORBIT.setdefault((j, fam[1]), set()).add(
                    (delta if den == 1 else '%d/%d' % (num, den), fam[0]))
                if add_fam(fam):
                    changed = True
                for x in descendants(*fam[:2]):
                    if add_fam(x):
                        changed = True
            for j in d['unc_b']:
                # exact class of the family at chain j (big-int) -- provisional path; all runs
                # to date have zero bulk failures, so this branch is dormant.
                # NOTE (round-2 review): if ever enabled, LIFT families must add the 2^j lift
                # bit into the class before firing (rj already includes it via residue(lift))
                rj = W.residue(num, den, j, lift)
                delta = rj - (1 << (j + 1)) if rj > (1 << j) else rj
                fam = fire(j, Frac(num, den) if den != 1 else Frac(delta, 1))
                ORBIT.setdefault((j, fam[1]), set()).add(('%d/%d' % (num, den), fam[0]))
                if add_fam(fam):
                    changed = True
        if not changed:
            return


def level_entries(plan, Thetas, ints):
    all_ints = set(ints)
    spec = {}
    for t, (Ep, Gp, tag) in enumerate(plan):
        for th in Thetas[t]:
            for (nn, dd) in [(3 * th[1] - th[0], th[1]), (th[0] - th[1], th[1])]:
                nn, dd = W.canon(nn, dd)
                if dd == 1:
                    all_ints.add(nn)
                else:
                    add_fam((nn, dd, False, 'entry family %s a/b t%d' % (tag, t)))
            for g in Gp:
                nn, dd = W.canon(th[0] + th[1] * g - 2 * th[1], th[1])
                if dd == 1:
                    all_ints.add(nn)
                else:
                    add_fam((nn, dd, False, 'generic-c family %s t%d (theta=%d/%d, g=%d)'
                             % (tag, t, th[0], th[1], g)))
            for (c, D), prov in Ep.items():
                if c < 5:
                    continue
                if th[1] == 1:
                    r = (th[0] + D - 2) % (1 << (c + 1))
                    spec.setdefault((c, r), (tag, 'c', th[0], c, sym(D, c), prov))
                else:
                    rr = (W.residue(th[0], th[1], c) + D - 2) % (1 << (c + 1))
                    nn, dd = W.canon(th[0] * 1 + (D - 2) * th[1], th[1])
                    spec.setdefault((c, rr), (tag, 'c-rat', '%d/%d' % (nn, dd), c, sym(D, c), prov))
    return all_ints, spec


for fam in (initial_families() + descendants(10, 3) + descendants(46, 9) +
            descendants(62, 9) + descendants(26, 3)):
    add_fam(fam)
certify_families()
log('P3 families closed:', len(FAM_SET), '(%.0fs)' % (time.time() - T0))

for _round in range(8):
    E_FAM = {}
    for (num, den, lift) in FAM_SET:
        d = family_cert(num, den, lift)
        for k in d['aout']:
            E_FAM.setdefault(k, ('family', '%d/%d' % (num, den), lift))
    for d in INTS:
        for k, v in E[d].items():
            E_FAM.setdefault(k, ('int-bulk', d))
    PLAN_E = [({**EABCD, **E_FAM}, GABCD, 'E0'), (EABC, GABC, 'E1'), (EAB, GAB, 'E2'), (EA, GA, 'E3')]
    INTS_E, SPEC_E = level_entries(PLAN_E, TH_E, list(range(-3, 6)))
    EE_unc, EE_spec_unc = [], []
    for d in sorted(INTS_E):
        assert d in INTS, ('E int outside INTS', d)
        if UNC[d]:
            EE_unc.append(dict(kind='int', cls=d, chains=UNC[d][:6]))
    E_E = {}
    for (c, r), prov in sorted(SPEC_E.items()):
        s = sym(r, c)
        if not (s in INTS and s in INTS_E and not UNC[s]):
            q = cert_specific(c, r)
            if not q['ok']:
                EE_spec_unc.append(dict(kind='spec', chain=c, cls=s, status=q['status'],
                                        word=q['word'][:8], why=prov))
                continue
            for a in q['aouts']:
                E_E.setdefault(a, ('spec-E', c, s))
    PLAN_S = [({**EABCD, **E_FAM, **E_E}, GABCD, 'S0'), (EABCD, GABCD, 'S1'), (EABC, GABC, 'S2'),
              (EAB, GAB, 'S3'), (EA, GA, 'S4')]
    INTS_S, SPEC_S = level_entries(PLAN_S, TH_S, list(range(-6, 8)))
    C7E_unc, C7E_spec_unc = [], []
    for d in sorted(INTS_S):
        assert d in INTS, ('C7E int outside INTS', d)
        if UNC[d]:
            C7E_unc.append(dict(kind='int', cls=d, chains=UNC[d][:6]))
    for (c, r), prov in sorted(SPEC_S.items()):
        s = sym(r, c)
        if not (s in INTS and s in INTS_S and not UNC[s]):
            q = cert_specific(c, r)
            if not q['ok']:
                C7E_spec_unc.append(dict(kind='spec', chain=c, cls=s, status=q['status'],
                                         word=q['word'][:8], why=prov))
    log('round %d: E spec=%d unc_spec=%d | C7E spec=%d unc_int=%d unc_spec=%d | fams=%d (%.0fs)' %
        (_round, len(SPEC_E), len(EE_spec_unc), len(SPEC_S), len(C7E_unc), len(C7E_spec_unc),
         len(FAM_SET), time.time() - T0))
    changed = False
    for unc in (EE_unc + EE_spec_unc + C7E_unc + C7E_spec_unc):
        if unc['kind'] != 'spec' or unc['chain'] >= 64:
            continue
        fires = {fire(unc['chain'], Frac(unc['cls'], 1))}          # by residue class...
        why = unc.get('why')
        if isinstance(why, (list, tuple)) and len(why) > 2 and isinstance(why[2], str)                 and '/' in why[2]:
            nn0, dd0 = why[2].split('/')                            # ...and by exact fraction
            fires.add(fire(unc['chain'], Frac(int(nn0), int(dd0))))
        for fam in fires:
            if add_fam(fam):
                changed = True
            for x in descendants(*fam[:2]):
                if add_fam(x):
                    changed = True
    certify_families()
    if not changed:
        break
else:
    raise AssertionError('entry fixpoint did not close (within den cap)')

summary['E'] = dict(ints=sorted(INTS_E), n_specific=len(SPEC_E), uncert_int=EE_unc, uncert_spec=EE_spec_unc)
summary['C7E'] = dict(ints=sorted(INTS_S), n_specific=len(SPEC_S), uncert_int=C7E_unc, uncert_spec=C7E_spec_unc)
summary['families'] = {'%d/%d/%d' % (k[0], k[1], k[2]): FAM_SET[k] for k in sorted(FAM_SET)}
summary['family_status'] = {'%d/%d/%d' % k: dict(
    unc_s=family_cert(k[0], k[1], k[2])['unc_s'][:3],
    unc_b=family_cert(k[0], k[1], k[2])['unc_b'][:3]) for k in sorted(FAM_SET)}
summary['orbit_free_entries'] = {('%d,3^%d' % (j, round(np.log2(k) / np.log2(3)))):
                                  sorted(str(x) for x in v) for (j, k), v in sorted(ORBIT.items())}
summary['fire_beyond_cap'] = [(a, b, c, d) for (a, b, c, d) in FIRE_LOG[:40]]
summary['orbit_cap_note'] = ('families beyond den=3^10 are not certified; the free-entry orbit at '
                             'chain 5 (and other shallow chains) persists through every computed '
                             'tower level -- the static closure does NOT close (Theorem OBST)')
log('P3 ORBIT free-entry levels:', {('%d,3^%d' % (j, round(np.log2(k) / np.log2(3)))):
                                    len(v) for (j, k), v in sorted(ORBIT.items())})
log('P3 ORBIT beyond-cap fires:', len(FIRE_LOG), FIRE_LOG[:3])
log('P4/P5 FINAL: E unc_spec', [u.get('cls') for u in EE_spec_unc], 'C7E unc_int', C7E_unc,
    'C7E unc_spec', [u.get('cls') for u in C7E_spec_unc], 'families', len(FAM_SET))

HERE.joinpath('levels_t5_%d.json' % JMAX).write_text(
    json.dumps(summary, indent=1, default=str) + '\n', encoding='utf-8')
HERE.joinpath('levels_t5_run.log').write_text('\n'.join(LOG) + '\n', encoding='utf-8')
log('WROTE levels_t5_%d.json  elapsed %.1f s' % (JMAX, time.time() - T0))
