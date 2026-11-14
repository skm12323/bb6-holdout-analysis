"""sigma4.py -- R4 (SIGMA stage 1): the exact shift spectrum Sigma_{<T4} and the level-by-level
generator closure, computed on the canonical table (chains < N0 = 2*10^7).

Conventions (identical to the accepted work_claude_residual/levels.py):
  * ENTRY (chain j, integer residue class mod 2^{j+1}); certify = work_claude_shifted Prop 3.2
    via rwalk (integer) and rwalk_t5 (rational families, 56-bit truncation bulk for j >= 64).
  * Sigma_L := shift classes s = (class of an a-output chain at omega >= 5 of the kernel walk
    S(Q), Q in level L) - 2.  Three data kinds, kept distinct:
      (w) witnessed: residues recorded by representative walks (count > 0), as in levels.py;
      (f) fired: gateway-fired entry classes (num/den + 2^m at chain m, 5 <= m < N0), covered by
          the all-chain family certificate (which m occur is calendar-open; GW bounds m);
      (d) deep: a-output classes at chains >= N0 (beyond the table), from the accepted structure
          lemmas (DL(iii) / DEEP-E), incl. the m = N0 boundary fire and its REG no-lift
          descendants (the 3-adic orbit).
  * Classification: a shift residue s at chain c is *explained* by (v, m) if v = num/3^e,
    e <= E_CAP, |v| <= V_CAP, m in {None} U [5, c], v + (2^m if m else 0) = s (mod 2^{c+1}).
    Canonical reading = min (|num|, e) among denominators 3^0, 3^1 (matches the accepted reading
    of Sigma_{<T3}: 12@5 -> 4/3+2^5, 83@7 -> -7/3, -3..1,3 -> integers).

Phases:
  P1  reproduce the accepted T4 level computation verbatim (A,B,C,OUT,D from integer bulk);
      assert field-by-field equality with work_claude_residual/levels_20000000.json.
  P2  deep drift sets Theta^E (BFS over one-step maps); assert == hand table (DL5).
  P3  TIGHT level-E entries from the DL source bounds (E0<-ABCD[+OUT variant], E1<-ABC, E2<-AB,
      E3<-A; a/b landings 3-theta, theta-1; specific c-entries theta+D-2 over lower-level
      a-output residues).  Free entries fire through GW; family closure (den cap 3^10, beyond-cap
      logged) certifies the fired families and aggregates their walk a-outputs.
  P4  assemble Sigma_{<=N0}, Sigma_{<T1}, Sigma_{<T2}, Sigma_{<T3}, Sigma_{<T4} (residues by
      chain + deep classes + fired ranges); classify; per-family witnesses.
  P5  invariant tests (integer set; 3-height; rational family list; M_h) -> verdict data.
  P6  realised shifts: every odd c crossing n < 2*10^7, s = -1-lambda_Y, cross-tabulated by omega.

Usage:  PYTHONUTF8=1 <python> -B work_gc_sigma/sigma4.py [jmax]     (default: full table)
Writes sigma4_<jmax>.json + sigma4_run.log into this directory.  Read-only elsewhere.
"""
import sys, json, time
from pathlib import Path
from fractions import Fraction

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
sys.path.insert(0, str(ROOT / 'work_gc_level_t5'))
import numpy as np
import rwalk as R          # accepted T4 machinery (work_claude_residual), read-only use
import rwalk_t5 as W       # accepted T5 rational machinery (work_gc_level_t5), read-only use

T0 = time.time()
T = R.Table()
JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else T.N
INTS = list(range(-8, 11))
E_CAP = 10         # classification search: denominator 3^e, e <= 10 (= family closure cap)
CANON_ECAP = 1     # canonical reporting: denominators 1 and 3 only
V_CAP = 64         # classification search: |value| <= V_CAP
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def sym(r, c):
    M = 1 << (c + 1)
    r %= M
    return r - M if r > M // 2 else r


# ================================ P1: accepted T4 levels ================================
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
            unc.append(dict(kind='specific', chain=c, cls=s, status=q['status'],
                            word=q['word'][:12], why=prov))
            continue
        for a in q['aouts']:
            Eo.setdefault(a, ('spec', name, c, s))
    summary[name] = dict(n_classes=len(Eo), generic_out=sorted(generic_out),
                         all_chain_integer_entries=sorted(all_ints), n_specific_entries=n_spec,
                         uncert=unc,
                         chain5=sorted({sym(r, c) for (c, r) in Eo if c == 5}),
                         exotic=sorted({(c, sym(r, c)) for (c, r) in Eo
                                        if sym(r, c) not in range(-20, 21)}))
    log('P1 level', name, 'classes', len(Eo), 'specific', n_spec, 'uncert', len(unc),
        round(time.time() - T0, 1))
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


def shapeD(tag):
    return [(EABC, GABC, [1], tag + '0'), (EAB, GAB, [0, 1, 2], tag + '1'),
            (EA, GA, [-1, 0, 1, 2, 3], tag + '2')]


EO, GO = level('OUT', shapeD('L'), list(range(-2, 5)), {0, 1, 2, 3, 4})
ED, GD = level('D', shapeD('depth'), list(range(-2, 5)), {0, 1, 2, 3, 4})
EABCD, GABCD = U(EABC, ED), GABC | GD
EABCDO = U(EABCD, EO)          # sources Q<T3 incl. the OUT-shaped (H5_res) entries


def _norm(x):
    def _n(v):
        if isinstance(v, (tuple, list)):
            return [_n(w) for w in v]
        if isinstance(v, dict):
            return {k: _n(w) for k, w in v.items()}
        return v
    return _n(x)


if JMAX == T.N:
    old = json.loads((ROOT / 'work_claude_residual' / 'levels_20000000.json').read_text(encoding='utf-8'))
    for name in ('A', 'B', 'C', 'OUT', 'D'):
        mine = summary.get(name)
        if name == 'A':
            ok = (old['A']['n_classes'] == len(EA)
                  and old['A']['chain5'] == sorted({sym(r, 5) for (c, r) in EA if c == 5}))
        else:
            ok = (old[name]['n_classes'] == mine['n_classes'] and old[name]['chain5'] == mine['chain5']
                  and old[name]['exotic'] == _norm(mine['exotic'])
                  and old[name]['uncert'] == _norm(mine['uncert'])
                  and old[name]['generic_out'] == mine['generic_out']
                  and old[name]['all_chain_integer_entries'] == mine['all_chain_integer_entries'])
        if not ok:
            raise AssertionError('T4 reproduction mismatch %s' % name)
    log('P1 T4 reproduction matches levels_20000000.json (A,B,C,OUT,D)', round(time.time() - T0, 1))
else:
    log('P1 SKIP reproduction assert (jmax truncated)')

# ================================ P2: deep drift sets (level E) ================================
DC_SET = {(n, 1) for n in (1, 2, 3)}
DD_SET = {(n, 1) for n in (1, 2, 3)}
DE_SET = {(n, 1) for n in range(0, 5)} | {(10, 3)}


def shift_of(Dset):
    return {W.add(n, d, -2, 1) for (n, d) in Dset}


def bfs(root, shift_sets):
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
    return out


TH_E = bfs((1, 1), [shift_of(DD_SET), shift_of(DC_SET), set()])
HAND_E = [{(1, 1)},
          {(0, 1), (1, 1), (2, 1)},
          {(n, 1) for n in range(-1, 4)},
          {(n, 1) for n in range(-2, 5)}]
assert TH_E == HAND_E, 'level E drift mismatch'
assert all(d == 1 for S in TH_E for (n, d) in S), 'level E drift must be integral'
log('P2 Theta^E ok (integral):', [sorted(n for (n, d) in S) for S in TH_E])

# ================================ P3: TIGHT level E ================================
def k_of(j):
    return int(T.tau[j - 1]) // 2


def fire(j, delta):
    val = Fraction(9 + 6 * k_of(j)) - delta
    nn, dd = W.canon(val.numerator, 3 * val.denominator)
    return (nn, dd, True, 'GW fire from free entry (j=%d, delta=%s)' % (j, delta))


RAT_MEMO = {}


def family_cert(num, den, lift, jhi=None):
    """certify the family (num/den (+lift)) as an entry at every chain 5<=j<jhi; aggregate walk
    a-outputs (scalar exact-residue j<64 -- NT outputs included, matching levels.py -- and the
    56-bit bulk for j>=64)."""
    if jhi is None:
        jhi = JMAX + 1
    key = (num, den, lift, jhi)
    if key in RAT_MEMO:
        return RAT_MEMO[key]
    unc_s = []; aout_s = {}
    for j in range(5, min(64, jhi)):
        c = W.certify_rat(T, j, num, den, lift)
        if not c['ok']:
            unc_s.append((j, c['status'], tuple(c['word'][:8])))
            continue
        for (c2, r2) in c['aouts']:
            aout_s[(c2, r2)] = aout_s.get((c2, r2), 0) + 1
    B = W.bulk_rat(T, num, den, lift, 64, jhi) if jhi > 64 else {'aout': {}, 'uncert': [], 'nt': {}}
    aout_all = {k: list(v) for k, v in B.get('aout', {}).items()}
    for k, v in aout_s.items():
        e = aout_all.setdefault(k, [0, 5]); e[0] += v
    d = dict(num=num, den=den, lift=lift, unc_s=unc_s, unc_b=B.get('uncert', []),
             aout=aout_all, nt=B.get('nt', {}))
    RAT_MEMO[key] = d
    return d


FAM_SET = {}
FIRE_LOG = []          # deduplicated by (num, den, lift); RAW_FIRE_LOG counts every append
RAW_FIRE_LOG = 0
FIRE_SEEN = set()
FIRE_WHY = {}
DEN_CAP = 3 ** 10


def add_fam(fam, src=None):
    (num, den, lift, why) = fam
    if den > DEN_CAP:
        global RAW_FIRE_LOG
        RAW_FIRE_LOG += 1
        if (num, den, lift) not in FIRE_SEEN:
            FIRE_SEEN.add((num, den, lift))
            FIRE_LOG.append((num, den, lift, why, str(src)))
        return False
    if (num, den, lift) not in FAM_SET:
        FAM_SET[(num, den, lift)] = why
        FIRE_WHY[(num, den, lift)] = src
        return True
    return False


def descendants(c, Q):
    out = []
    for tag, nn0 in [('a', 3 * Q - c), ('b', c - Q)] + [('cs%d' % s, c + 3 * s * Q) for s in (-1, 0, 1)]:
        nn, ddd = W.canon(nn0, Q)
        out.append((nn, ddd, False, 'REG descendant %s of %d/%d' % (tag, c, Q)))
    return out


def certify_families():
    for _ in range(300):
        changed = False
        for key in sorted(list(FAM_SET)):
            num, den, lift = key
            d = family_cert(num, den, lift)
            for (j, st, w) in d['unc_s']:
                delta = W.sym_rep(num, den, j)
                if lift:
                    delta = (delta + (1 << j)) % (1 << (j + 1))
                    delta = delta - (1 << (j + 1)) if delta > (1 << j) else delta
                fam = fire(j, Fraction(delta, 1) if den == 1 else Fraction(num, den))
                if add_fam(fam, ('family-free', key, j)):
                    changed = True
                for x in descendants(*fam[:2]):
                    if add_fam(x, ('desc', fam[:2])):
                        changed = True
            for j in d['unc_b']:
                rj = W.residue(num, den, j, lift)
                delta = rj - (1 << (j + 1)) if rj > (1 << j) else rj
                fam = fire(j, Fraction(num, den) if den != 1 else Fraction(delta, 1))
                if add_fam(fam, ('family-bulk-free', key, j)):
                    changed = True
        if not changed:
            return
    raise AssertionError('family closure did not terminate')


def level_entries_tight(Thetas, use_out):
    src = [EABCDO, EABC, EAB, EA] if use_out else [EABCD, EABC, EAB, EA]
    plans = list(zip(src, ['E0', 'E1', 'E2', 'E3']))
    all_ints = set(); spec = {}
    for t, (Ep, tag) in enumerate(plans):
        Gp = [GABCD, GABC, GAB, GA][t]
        for th in Thetas[t]:
            for (nn, dd) in [(3 - th[0], 1), (th[0] - 1, 1)]:
                all_ints.add(nn)
            for g in Gp:
                all_ints.add(th[0] + g - 2)
            for (c, D), prov in Ep.items():
                if c < 5:
                    continue
                r = (th[0] + D - 2) % (1 << (c + 1))
                spec.setdefault((c, r), (tag, 'c', th[0], c, sym(D, c), prov))
    unc_int = []
    for d in sorted(all_ints):
        assert d in INTS, ('E int outside INTS', d)
        if UNC[d]:
            unc_int.append(dict(kind='int', cls=d, chains=UNC[d][:6]))
    return all_ints, spec, unc_int


def build_E(use_out):
    INTS_E, SPEC_E, unc_int = level_entries_tight(TH_E, use_out)
    E_E = {}; unc_spec = []
    for (c, r), prov in sorted(SPEC_E.items()):
        s = sym(r, c)
        if s in INTS and s in INTS_E and not UNC[s]:
            continue
        q = cert_specific(c, r)
        if not q['ok']:
            unc_spec.append(dict(kind='spec', chain=c, cls=s, status=q['status'],
                                 word=q['word'][:8], why=prov))
            continue
        for a in q['aouts']:
            E_E.setdefault(a, ('spec-E', c, s))
    log('P3 E[use_out=%s] ints %s spec %d unc_int %s unc_spec %s (%.0fs)' %
        (use_out, sorted(INTS_E), len(SPEC_E), [(u['cls'], u['chains']) for u in unc_int],
         [(u['chain'], u['cls']) for u in unc_spec], time.time() - T0))
    return INTS_E, SPEC_E, unc_int, unc_spec, E_E


INTS_E, SPEC_E, UNC_INT_E, UNC_SPEC_E, E_E = build_E(False)
# integer free entries fire by exact integer value; specific free entries fire by residue AND by
# every denominator<=3 value fitting the residue (the exact value of a specific entry is not
# carried by the tight construction; firing all candidates over-approximates the GW output).
def class_value_candidates(c, cls, ecap=4):
    """candidate exact class values num/3^e (e<=ecap) fitting the residue cls at chain c
    (num/den = cls mod 2^{c+1}  <=>  num = cls*den mod 2^{c+1}, symmetric).  The exact value of a
    specific free entry is not carried by the residue machinery; firing all candidates
    over-approximates the GW output family."""
    M = 1 << (c + 1)
    out = [Fraction(cls)]
    for e in range(1, ecap + 1):
        den = 3 ** e
        num = (cls * den) % M
        if num > M // 2:
            num -= M
        out.append(Fraction(num, den))
    return out


for u in UNC_INT_E:
    d = u['cls']
    for j in UNC[d]:
        if j < 64:
            fam = fire(j, Fraction(d, 1))
            add_fam(fam, ('int-free', d, j))
            # the fired chain m can reach the deep boundary m = N0 (GW(b): m <= G(j_3)+1 <= N0,
            # j_3 < T1); there the continuation is the REG no-lift descendant set [A]:
            for x in descendants(*fam[:2]):
                add_fam(x, ('desc-top', fam[:2]))
for u in UNC_SPEC_E:
    if u['chain'] < 64:
        for v in class_value_candidates(u['chain'], u['cls']):
            famv = fire(u['chain'], v)
            add_fam(famv, ('spec-free', u['chain'], u['cls'], str(v)))
            for x in descendants(*famv[:2]):
                add_fam(x, ('desc-spec', famv[:2]))
certify_families()
log('P3 tight family closure: %d families, %d beyond-cap fires (%.0fs)' %
    (len(FAM_SET), len(FIRE_LOG), time.time() - T0))
INTS_E2, SPEC_E2, UNC_INT_E2, UNC_SPEC_E2, _ = build_E(False)
assert INTS_E2 == INTS_E and SPEC_E2 == SPEC_E, 'tight entry sets unexpectedly changed'
E_E_FINAL = dict(E_E)
for d in sorted(INTS_E):
    for k in E[d]:
        E_E_FINAL.setdefault(k, ('int-bulk', d))
FAM_AOUT = {}
for (num, den, lift) in sorted(FAM_SET):
    fc = family_cert(num, den, lift)
    for k in fc['aout']:
        FAM_AOUT.setdefault(k, ('family', '%d/%d' % (num, den), lift))
INTS_EO, SPEC_EO, UNC_INT_EO, UNC_SPEC_EO, E_EO = build_E(True)
DIFF_OUT = set(SPEC_EO) ^ set(SPEC_E)
log('P3 OUT-merge variant: ints %s spec %d sym-diff %d unc_spec %s (%.0fs)' %
    (sorted(INTS_EO), len(SPEC_EO), len(DIFF_OUT),
     [(u['chain'], u['cls']) for u in UNC_SPEC_EO], time.time() - T0))

# ================================ P4: spectrum assembly ================================
def shifts_of(Eset):
    by = {}
    for (c, r) in Eset:
        if c >= 5:
            by.setdefault(c, set()).add(sym(r - 2, c))
    return by


def merge(a, b):
    out = {c: set(v) for c, v in a.items()}
    for c, v in b.items():
        out.setdefault(c, set()).update(v)
    return out


FIRED_SHIFT_RANGE = {}     # keyed by the FULL family key (num, den, lift) -- a fired with-lift
#                          family and its no-lift cs0 descendant share (num,den) but are distinct
#                          possible classes (lift bit 2^m at the fired chain); keying by
#                          (num,den) alone made the cs0 twin overwrite the lifted entry
#                          (round-1 review, MEDIUM).
TOPFIRE = 'top'            # fired from E's integer (5,5) entry (deep provenance y=j_3<T1: m<=N0)
DEEPFIRE = 'deep'          # no-lift REG descendant of a deep chain: possible chains < G(N0)+1~54
ORBITFIRE = 'orbit'        # fired from a chain-5 free entry with shallow provenance; GW(b)
#                          true bound m < G(y)+1 with y < 54 shallow, i.e. m <=~16-17; the [17,64)
#                          part of the synthesis range is a direction-safe relaxation (the extra
#                          residues share values with the deep no-lift twins -- no spurious
#                          out-of-list entries; round-2 review note)
for (num, den, lift) in sorted(FAM_SET):
    sv = Fraction(num - 2 * den, den)
    src = FIRE_WHY.get((num, den, lift))
    if not lift:
        FIRED_SHIFT_RANGE[(num, den, lift)] = (sv, [5, 54], DEEPFIRE)
        continue
    kind = TOPFIRE if (src and src[0] == 'int-free') else ORBITFIRE
    mhi = JMAX if kind == TOPFIRE else 64
    FIRED_SHIFT_RANGE[(num, den, lift)] = (sv, [5, mhi], kind)

FIRED_RES = {}             # synthesised entry residues: no-lift/deep families m<54, ALL lifted
#                          families m<64 (the classifier's lift search covers m<=64; chains
#                          m>=65 are claimed ONLY through the family's all-chain certificate
#                          and M_h.fired_range -- all such values are 4/3+2^m, inside the
#                          candidate list, so no Tier-2 residue is lost by this cap).
for (num, den, lift), (sv, (mlo, mhi), kind) in sorted(FIRED_SHIFT_RANGE.items()):
    for m in range(mlo, min(mhi, 54 if kind == DEEPFIRE else 64)):
        r = (sv.numerator * pow(sv.denominator, -1, 1 << (m + 1))) % (1 << (m + 1))
        if kind != DEEPFIRE:
            r = (r + (1 << m)) % (1 << (m + 1))     # lift bit at the fired chain itself
        s = sym(r, m)
        FIRED_RES.setdefault(m, set()).add(s)

SIGMA = {}
SIGMA['<=N0'] = shifts_of(EA)
SIGMA['<T1'] = shifts_of(EAB)
SIGMA['<T2'] = shifts_of(EABC)
SIGMA['<T3'] = shifts_of(U(EABC, ED, EO))
SIGMA['<T4'] = merge(shifts_of(U(EABC, ED, EO, E_E_FINAL)), shifts_of(FAM_AOUT))
SIGMA['<T4'] = merge(SIGMA['<T4'], FIRED_RES)
SIGMA['<T4-core'] = shifts_of(U(EABC, ED, EO, E_E_FINAL))   # witnessed only (no families/fires)
# drift-derived POSSIBLE a-output shift values beyond the witnessed walk data:
#  deep a-output classes at chains >= N0 (DL(iii) / DEEP-E) AND the a-step landing classes
#  3 - theta_t at the first shallow chain (a-landings ARE a-outputs; landing chain may be >= 5).
#  B: generic 2; C: deep {1,2,3} + landings 1-{0,1,2}; D: deep {1,2,3} + landings 1-[-1,3];
#  E: deep [0,4] + landings 1-Theta^E_1..3 = [0,4] u [1-{0,1,2}] u ... = [-3,3].
DEEP_VALUES = {'<=N0': [Fraction(0)], '<T1': [Fraction(0)],   # 0 already witnessed at level A
               '<T2': [Fraction(n - 2) for n in (1, 2, 3)],
               '<T3': sorted({Fraction(n - 2) for n in (1, 2, 3)} |
                             {Fraction(1 - t) for t in range(-1, 4)}),
               '<T4': sorted({Fraction(n - 2) for n in range(0, 5)} |
                             {Fraction(1 - t) for t in list(range(-2, 5)) + [0, 1, 2] + list(range(-1, 4))})}


# classification
def reps(c, s, ecap=E_CAP):
    """all (value, m): value=num/3^e (e<=ecap), |value|<=V_CAP, m in {None}U[5,min(c,64)],
    value+(2^m if m) == s (mod 2^{c+1}).  num = (s-2^m)*3^e mod 2^{c+1}, symmetric."""
    out = []
    M = 1 << (c + 1)
    for e in range(0, ecap + 1):
        den = 3 ** e
        for m in [None] + list(range(5, min(c, 64) + 1)):
            t = (s - (1 << m)) % M if m is not None else s % M
            num = (t * den) % M
            if num > M // 2:
                num -= M
            v = Fraction(num, den)
            if abs(v) <= V_CAP:
                out.append((v, m))
    return out


def canon(c, s):
    rr = [r for r in reps(c, s, ecap=CANON_ECAP)]
    if not rr:
        return None
    return min(rr, key=lambda r: (abs(r[0].numerator), 1 if r[0].denominator != 1 else 0,
                                  0 if r[1] is None else 1))


CLASS_CANON = {}
UNEXPLAINED = {}
UNEXPLAINED4 = {}
for key in SIGMA:
    can = {}; unexp = []; unexp4 = []
    for c in sorted(SIGMA[key]):
        for s in sorted(SIGMA[key][c]):
            cr = canon(c, s)
            if cr is None:
                unexp.append((c, s))
            else:
                can.setdefault(cr, set()).add((c, s))
            if not reps(c, s, ecap=E_CAP):
                unexp4.append((c, s))
    CLASS_CANON[key] = can
    UNEXPLAINED[key] = unexp
    UNEXPLAINED4[key] = unexp4
    log('P4 Sigma[%s]: chains %d residues %d canon-families %d unexplained(e<=%d) %d '
        'unexplained(e<=%d) %d (%.0fs)' %
        (key, len(SIGMA[key]), sum(len(v) for v in SIGMA[key].values()), len(can), CANON_ECAP,
         len(unexp), E_CAP, len(unexp4), time.time() - T0))


def ints_of(key):
    vals = {v for (v, m) in CLASS_CANON[key] if v.denominator == 1 and m is None}
    vals |= set(DEEP_VALUES.get(key, []))
    return sorted(vals)


def ints_witnessed(key):
    vals = {v for (v, m) in CLASS_CANON[key] if v.denominator == 1 and m is None}
    return sorted(vals)


def ratfams_of(key):
    return sorted(((str(v), m) for (v, m) in CLASS_CANON[key]
                   if v.denominator != 1 or m is not None), key=str)


for key in ('<=N0', '<T1', '<T2', '<T3', '<T4'):
    log('P4 %s ints %s ; non-integer/lifted canon families %s' %
        (key, ints_of(key), ratfams_of(key)[:30]))

# ================================ P5: invariant tests ================================
# candidate list (task): integer drift interval (|v|<=16, no lift) u {4/3 + 2^m} u {-7/3};
# a residue passes iff it admits SOME representation (e <= E_CAP) in the list.
L_INT = lambda v, m: v.denominator == 1 and m is None and abs(v) <= 16
L_GW = lambda v, m: v == Fraction(4, 3)
L_M2 = lambda v, m: v == Fraction(-7, 3) and m is None

# baseline verification: the accepted Sigma_{<T3} claim (witnessed reading) must reproduce.
BASE_OK = {}
for k, h in (('<T1', 1), ('<T2', 2), ('<T3', 3)):
    want = sorted(set(range(-h, 2)) | ({3} if h >= 2 else set()))
    BASE_OK['ints_' + k] = (ints_witnessed(k) == want)
BASE_OK['gw_<T3'] = None
BASE_OK['m2_<T3'] = (Fraction(-7, 3), None) in CLASS_CANON['<T3']


def in_list(v, m):
    return L_INT(v, m) or L_GW(v, m) or L_M2(v, m)


INV = {}
for k, h in (('<T1', 1), ('<T2', 2), ('<T3', 3)):
    got = set(ints_of(k))
    INV['int_' + k] = dict(got=sorted(got), cand=sorted(set(range(-h, 2)) | {3}),
                           ok=(got <= set(range(-h, 2)) | {3}))
exact4 = set(DEEP_VALUES['<T4']) | {sv for (sv, rng, kind) in FIRED_SHIFT_RANGE.values()
                                    if sv.denominator == 1}
wit4 = set(ints_witnessed('<T4-core'))      # E-walk witnessed integers (families excluded:
# their residue canon readings are value/lift-ambiguous)
union4 = exact4 | wit4
canon4 = set(ints_of('<T4'))
INV['int_<T4'] = dict(exact_structural=sorted(exact4), witnessed_core=sorted(wit4),
                      union=sorted(union4), canon_residue_readings_all=sorted(canon4),
                      cand_pm1=sorted(set(range(-4, 2)) | {3}),
                      ok_pm1_union=(union4 <= set(range(-4, 2)) | {3}),
                      cand_lc=sorted(set(range(-3, 3)) | {3}),
                      ok_lc_union=(union4 <= set(range(-3, 3)) | {3}),
                      note=('exact_structural = deep classes (DL/DEEP-E) + a-landings + fired '
                            'integer values; witnessed_core = canonical integer readings of the '
                            'non-family level-E walk residues (E[d] bulk + spec walks)'))
for k in ('<T1', '<T2', '<T3', '<T4'):
    bad = []; badv = {}
    for c in sorted(SIGMA[k]):
        for s in sorted(SIGMA[k][c]):
            rr = reps(c, s)
            if not any(in_list(v, m) for (v, m) in rr):
                # keep the smallest-|num| e<=E_CAP readings as the presumed true values
                best = min(rr, key=lambda r: (abs(r[0].numerator), r[0].denominator)) if rr else None
                bad.append((c, s, str(best[0]) if best else None,
                            ('lift %d' % best[1]) if best and best[1] is not None else 'no-lift'))
                if best:
                    badv.setdefault((str(best[0]), best[1]), []).append((c, s))
    INV['rat_' + k] = dict(n_bad=len(bad), bad=bad[:16],
                           bad_values={str(kk): sorted(vv)[:6] for kk, vv in sorted(badv.items(),
                                                                                    key=str)},
                           bad_values_note=('keys are stringified (value, lift-position) '
                                            'records (%d keys, %d distinct values in this run); '
                                            'each key keeps only its 6 smallest (chain, class) '
                                            'witnesses, so the detailed sample saturates by '
                                            'chain 30 although n_bad counts the full scan over '
                                            'all chains' % (len(badv),
                                                            len({b[0] for b in badv}))))
# Tier 1: exact-value elements -- the fired families' shift values (with their m-ranges and
# provenance) and the deep classes, tested directly against the candidate list.
T1_BAD = []
for (num, den, lift), (sv, (mlo, mhi), kind) in sorted(FIRED_SHIFT_RANGE.items()):
    if not (L_INT(sv, None) or L_GW(sv, None if kind == DEEPFIRE else 5) or L_M2(sv, None)):
        T1_BAD.append(dict(kind='fired-value', value=str(sv),
                           family='%d/%d/%d' % (num, den, lift),
                           m_range=[mlo, mhi], fire_kind=kind,
                           why=FAM_SET.get((num, den, True)) or FAM_SET.get((num, den, False)),
                           src=str(FIRE_WHY.get((num, den, True)) or FIRE_WHY.get((num, den, False)))))
for v in DEEP_VALUES['<T4']:
    if not (L_INT(v, None) or L_GW(v, None) or L_M2(v, None)):
        T1_BAD.append(dict(kind='deep-value', value=str(v), family='deep-E [0,4] classes minus 2'))
INV['tier1_<T4'] = dict(n_bad=len(T1_BAD), bad=T1_BAD[:40])
INV['tier1_deep_gateway'] = dict(value='4/3 + 2^N0 at chain N0 (fired boundary class 10/3+2^N0)',
                                 in_list=True)
MH = {}
for k in ('<T2', '<T3', '<T4'):
    ms = sorted({m for (v, m) in CLASS_CANON[k] if v == Fraction(4, 3) and m is not None})
    full = list(range(ms[0], ms[-1] + 1)) if ms else []
    MH[k] = dict(min=ms[0] if ms else None, max=ms[-1] if ms else None,
                 missing=[m for m in full if m not in ms], n=len(ms))
MH['<T4']['fired_range'] = [5, JMAX]        # top-fire 10/3-family: class (10-2^m)/3 certified
# at every chain m < JMAX (family certificate); which m occur is calendar-open
BASE_OK['gw_<T3'] = (MH['<T3'].get('min') == 5 and MH['<T3'].get('max') == 24
                     and MH['<T3'].get('missing') == [23])
# per-level measurements
def log3_den(den):
    e = 0
    while 3 ** (e + 1) <= den:
        e += 1
    return e


MEAS = {}
for k in ('<=N0', '<T1', '<T2', '<T3', '<T4'):
    nres = sum(len(v) for v in SIGMA[k].values())
    maxe = 0
    for c in SIGMA[k]:
        for s in SIGMA[k][c]:
            rr = reps(c, s)
            if rr:
                emin = min(log3_den(v.denominator) for (v, m) in rr)
                maxe = max(maxe, emin)
    MEAS[k] = dict(n_chains=len(SIGMA[k]), n_residues=nres,
                   n_canon_families=len(CLASS_CANON[k]),
                   ints_witnessed=(ints_witnessed('<T4-core') if k == '<T4' else ints_witnessed(k)),
                   ints_with_possible=list(map(str, ints_of(k))),
                   max_min_den3_exp=maxe)
MEAS['<T4']['fired_values'] = sorted({str(sv) for (sv, rng, kind) in FIRED_SHIFT_RANGE.values()})
log('P5 baseline verification (witnessed reading):', json.dumps(BASE_OK, default=str))
log('P5 invariants:', json.dumps(INV, default=str))
log('P5 M_h (canonical 4/3+2^m):', json.dumps(MH, default=str))
log('P5 measurements:', json.dumps(MEAS, default=str))

# ================================ P6: realised shifts ================================
oddc = np.nonzero(T.odd.astype(bool) & (T.typ == 99))[0]
lamY = T.lY[oddc]
lam = T.lam[oddc]
lv = (lam & (-lam).astype(np.int64)).astype(np.float64)
om = np.rint(np.log2(lv)).astype(np.int64)
sraw = (-1 - lamY) % ((np.int64(1) << (om + 1)))
realized = {}
for o, s in zip(om.tolist(), sraw.tolist()):
    o = int(o); s = int(s)
    s = sym(s, o)
    realized[(o, s)] = realized.get((o, s), 0) + 1
log('P6 realised (omega, shift-class) -> count:', sorted(realized.items()))
real_ge5 = sorted({s for (o, s) in realized if o >= 5})
real_all = sorted({s for (o, s) in realized})
log('P6 realised shift classes omega>=5:', real_ge5, ' all omega:', real_all)

# ================================ artifact ================================
def jsf(x):
    return str(x)


out = dict(jmax=JMAX, seconds=round(time.time() - T0, 1),
           scope=('[B] canonical table chains < %d; tight level-E construction (DL source bounds); '
                  'families certified scalar j<64 + bulk 56-bit truncation; fired-entry residues '
                  'synthesised for m<54 (no-lift/deep families) and m<64 (lifted families, '
                  'matching the classifier lift range); chains m>=64 are claimed only through '
                  "the family's all-chain certificate (M_h.fired_range), not synthesised"
                  % JMAX),
           levels={k: summary[k] for k in ('B', 'C', 'OUT', 'D')},
           E=dict(ints=sorted(INTS_E), n_spec=len(SPEC_E), unc_int=UNC_INT_E, unc_spec=UNC_SPEC_E),
           E_out_variant=dict(ints=sorted(INTS_EO), n_spec=len(SPEC_EO),
                              spec_sym_diff=len(DIFF_OUT), unc_spec=UNC_SPEC_EO),
           families={'%d/%d/%d' % k: FAM_SET[k] for k in sorted(FAM_SET)},
           family_src={'%d/%d/%d' % k: str(FIRE_WHY.get(k)) for k in sorted(FAM_SET)},
           family_unc={('%d/%d/%d' % k): dict(unc_s=family_cert(*k)['unc_s'],
                                              unc_b=family_cert(*k)['unc_b'])
                       for k in sorted(FAM_SET)},
           fire_beyond_cap=[list(x) for x in FIRE_LOG[:80]],
           fire_beyond_cap_note=('deduplicated by (num,den,lift); %d distinct families, '
                                 '%d raw log appends' % (len(FIRE_LOG), RAW_FIRE_LOG)),
           fired_shift_ranges={'%d/%d/%d' % k: [str(v), lo, hi, kind]
                               for k, (v, (lo, hi), kind) in sorted(FIRED_SHIFT_RANGE.items())},
           sigma={k: {str(c): sorted(v) for c, v in sorted(SGM.items())} for k, SGM in SIGMA.items()},
           sigma_ints={k: ints_of(k) for k in SIGMA},
           sigma_ints_note=('ints_witnessed for h<=3 and <T4-core are value claims; '
                            'sigma_ints/ints_with_possible for <T4 include canonical integer '
                            'readings of orbit-family residues (e.g. -64..16) which are residue '
                            'readings, NOT value claims (the INV logic excludes family residues '
                            'via witnessed_core/exact_structural)'),
           canon_families={k: {'%s|%s' % (v, m): dict(n=len(w), ex=sorted(map(str, w))[:8])
                               for (v, m), w in CC.items()} for k, CC in CLASS_CANON.items()},
           unexplained={k: [(c, s) for (c, s) in UNEXPLAINED[k]] for k in UNEXPLAINED},
           unexplained4={k: [(c, s) for (c, s) in UNEXPLAINED4[k]] for k in UNEXPLAINED4},
           baseline_ok=BASE_OK, measurements=MEAS, ints_witnessed={k: ints_witnessed(k)
                                                                   for k in SIGMA},
           deep_values={k: [jsf(v) for v in vs] for k, vs in DEEP_VALUES.items()},
           deep_note=('level-E deep a-output classes [0,4] (shifts [-2,2]) plus the fired boundary '
                      'class 10/3+2^N0 (shift 4/3+2^N0 at chain N0) and its REG no-lift '
                      'descendants (the 3-adic orbit -3+/-8/3^r) -- the orbit enters through the '
                      'family closure; see families/family_unc/fire_beyond_cap'),
           invariants=INV, M_h=MH,
           realized={('%d,%d' % k): v for k, v in sorted(realized.items())},
           realized_ge5=real_ge5, realized_all=real_all)
HERE.joinpath('sigma4_%d.json' % JMAX).write_text(json.dumps(out, indent=1, default=str) + '\n',
                                                  encoding='utf-8')
HERE.joinpath('sigma4_run.log').write_text('\n'.join(LOG) + '\n', encoding='utf-8')
log('WROTE sigma4_%d.json  elapsed %.1f s' % (JMAX, time.time() - T0))
