"""verify_freeb.py -- verification script for FREE-B (boundary-gate localization).

ZCode agent, 2026-11-10, for work_gc_freeb/NOTES.md.  Run from D:/math_cc:

    PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B work_gc_freeb/verify_freeb.py [--quick]

Checks (all exact; synthetic starts on canonical Calendar(512) crossing data):
  PART 1  engine: det_walk vs cyc.walk exact integer replays (random X, V lifts).
  PART 2  Lemma FB-1/FB-2/FB-3 invariants + boundary census, postgate range
          (every odd-a j < JMAX, j <= m < MMAX, default 400 x 5000):
            v2(A) = j - ell + Lbc + 1 (or A = 0 before the first a-step),
            v2(B) = m + 1 - ell at every step,
            determined landing == v2(constant part) < min variable valuation,
            at a determined next gate: m' = v2(C_final), dR = m'+1+ell-j <= 1+Lbc (DR'),
            boundary (m' >= j-ell)  <=>  2^(j-ell) divides C_final;
          every boundary instance classified into branch (I)/(II)/(III).
  PART 3  FB-4 two-step closed forms: C_final == 3 S_a + 2^(j-2) + 2^(m-2)  (type a),
          == 2^(j-1) - 3*2^(m-3) + U_b/2  (type b),  == 2^(j-1) + 6(k+tau+k_c+2) - lam/2
          - R_c 2^(m-1)  (type c), for every determined two-step pair in the range.
  PART 4  CLOCK/MASS localization: every branch-(I) instance satisfies the FREE
          congruences and j <= 3 + log2(6 m P(m)); every branch-(II) instance with
          nonzero explicit sum satisfies 2^(j-ell) <= |sum| and
          j <= 2+log2(3mP(m)+3) (a) / 2+log2(21mP(m)+20) (b) / 1+eps+log2(30mP(m)+29) (c).
  PART 5  counterexamples A (j=24, m=6268562), B (j=42, m=1095510131453),
          B2 (j=78, m=526980180956824005813092): all invariants + closed forms +
          boundary + exact replay (A: full big-integer replay; B/B2: exact mod-2^P replay).
  PART 6  sweep census: forced-gate starts G(j), j odd-a < SWJ (default 3000), cylinder
          depth SWB (default 3000): every consecutive true-gate pair in every resolved
          leaf checked as in PART 2 (within 400 steps); boundary instances classified.
  PART 7  seeded boundary constructions (NEXT congruences solved on real calendar chains):
          type a for j in {24, 61, 97}, type b for j in {42, 78}; verified as in PART 5.
  PART 8  CL2 census consistency: in the sweep trees every non-record-safe gate is either
          reached through a split (alpha) or is a boundary gate in (I)/(II)/(III).

Output: ASCII lines + work_gc_freeb/freeb_checks.json; last line ALL PASS (exit 0) iff
no *_FAIL counter is set.  --quick shrinks ranges (postgate 120 x 1500, sweep 400 x 400,
seeded iterations reduced); the full run is the census of record.
"""
import sys, json, time, random
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'work_claude_cycle'))
from fb import (Rows, FSt, step_form, det_walk, fb4, fb4_Cform_ab, fb4_Cform_c,  # noqa: E402
                tf_eq, tf_v2, Pc, SAFE_M)
from cyc import Cal, walk, v2, INF  # noqa: E402
import branch as br  # noqa: E402  (accepted engine of work_claude_cycle)

QUICK = '--quick' in sys.argv
JMAX, MMAX = (120, 1500) if QUICK else (400, 5000)
SWJ, SWB = (400, 400) if QUICK else (3000, 3000)
SEED_ITERS = 400 if QUICK else 4000

cnt = {}
fails = []


def chk(name, cond, info=None):
    cnt[name] = cnt.get(name, 0) + 1
    if not cond:
        cnt[name + '_FAIL'] = cnt.get(name + '_FAIL', 0) + 1
        if len(fails) < 40:
            fails.append((name, info))


def replay_exact(cal, rows, j, k, m, trace, rng):
    """exact big-integer replay of a det_walk trace from the generic post-gate start
    with random (X, V); returns the walk's chain word."""
    P = max(m, j) + 128
    X = rng.getrandbits(96)
    V = rng.getrandbits(96)
    Th = 2 ** (j - 2) + 3 * (k + 1) + (1 << (j - 1)) * X
    x = (1 << m) * (1 + 2 * V)
    steps, st = walk(cal, m, Th, x, limit=len(trace) + 3)
    return [s['jn'] for s in steps], steps


def replay_mod(cal, rows, j, k, m, trace, rng, P=200, X0=None, nsteps=None):
    """exact integer replay for huge m, at finite precision.  The start is the genuine
    post-gate state (Theta = c_Theta + 2^(j-1) X0, x = 2^m(1+2V)) with chosen X0, V=0;
    x is carried as (x_rep mod 2^live) with true x = x_rep mod 2^live ('live' precision).
    At the first step q = m >> live, so x_rep = 0; each step's chain reading is exact
    while the chain is below live - 8.  Independent integer code path (no Fractions)."""
    if X0 is None:
        X0 = rng.getrandbits(64)
    Th = 2 ** (j - 2) + 3 * (k + 1) + (1 << (j - 1)) * X0
    x_rep = 0
    live = P
    q = m
    word = []
    for _ in range((nsteps if nsteps else len(trace)) + 3):
        if q <= 4:
            break
        r = rows(q - 1)
        if not r['odd']:
            break
        if r['kind'] == 'a':
            assert x_rep % 2 == 0
            x_rep = (2 * Th + 6 * (r['tau'] // 2) - (x_rep >> 1)) % (1 << live)
            Th = Th + 3 + 6 * (r['tau'] // 2)
            loss = 1
        else:
            if q >= live:
                x_rep = r['lam'] % (1 << live)      # C*(odd) vanishes at the new precision
            else:
                C = r['R'] * (1 << q)
                assert C.denominator == 1
                x_rep = (int(C) * (x_rep >> q) + r['lam']) % (1 << live)
            Th = Th + 3 + 3 * r['tau']
            loss = 1 + r['eps']
        live -= loss
        jn = (x_rep & -x_rep).bit_length() - 1 if x_rep else live
        chk('replaymod_prec', jn < live - 8, (q, jn, live))
        word.append(jn)
        q = jn
    return word


def analyze_pair(rows, j, k, m, max_steps=400):
    """det_walk from the post-gate state of gate (j, k, m) up to the first true NT gate.
    Returns dict(status, trace, mprime, ell, Lbc, dR, boundary, branch, fb4)."""
    trace, status, st = det_walk(rows, j, k, m, max_steps=max_steps)
    d = dict(status=status, trace=trace, st=st, mprime=None, ell=None, Lbc=None,
             dR=None, boundary=None, branch=None, fb4=None)
    if status != 'GATE':
        return d
    last = trace[-1]
    mp, ell, Lbc = last[1]['jn'], st.ell, st.Lbc
    d.update(mprime=mp, ell=ell, Lbc=Lbc, dR=mp + 1 + ell - j,
             boundary=(mp >= j - ell))
    c1 = trace[0][1]['jn']
    depth = len(trace) - 1          # steps from m to G'-input
    if c1 >= j - 1:
        d['branch'] = 'I'
    elif depth == 1:
        d['branch'] = 'II'
        d['fb4'] = fb4(rows, j, k, m)
    else:
        d['branch'] = 'III'
    return d


def invariants(rows, j, k, m, res, tag):
    """FB-1/FB-2/FB-3 invariant checks on a det_walk result (status GATE)."""
    ell, Lbc = res['ell'], res['Lbc']
    st2 = FSt(j, k, m)
    for idx, (q_in, s, t) in enumerate(res['trace']):
        step_form(rows, st2)
        chk(tag + '_vB', st2.m + v2(st2.gamma) == m + 1 - st2.ell, (j, m, idx))
        if st2.a == 0:
            chk(tag + '_A_notentered', st2.ell <= st2.Lbc, (j, m, idx))
        else:
            chk(tag + '_vA', v2(st2.a) == j - st2.ell + st2.Lbc + 1, (j, m, idx))
        chk(tag + '_det', s['jn'] is not None)
    chk(tag + '_vA_final', v2(st2.a) == j - ell + Lbc + 1, (j, m))
    chk(tag + '_vB_final', st2.m + v2(st2.gamma) == m + 1 - ell, (j, m))
    chk(tag + '_mprime', res['mprime'] == tf_v2(st2.u, st2.beta, m), (j, m))
    chk(tag + '_detout', res['mprime'] < min(v2(st2.a), st2.m + v2(st2.gamma)), (j, m))
    chk(tag + '_DRp', res['dR'] <= 1 + Lbc, (j, m, res['dR']))
    # boundary <=> 2^(j-ell) | C_final   (C_final = u + beta*T)
    div = tf_v2(st2.u, st2.beta, m) >= j - ell
    chk(tag + '_boundary_iff_div', div == res['boundary'], (j, m, res['mprime'], j - ell))
    return st2


def check_boundary_instance(rows, cal, j, k, m, res, tag, rng, huge=False):
    """PART 3/4 checks for a branch-(II) or general boundary instance."""
    b = res['branch']
    if b == 'II':
        d = res['fb4']
        r = rows(m - 1)
        kind = d['kind']
        # closed form identity
        if kind == 'a':
            u2, b2 = fb4_Cform_ab(k, 'a', None, d['kc'], j, m, Km=r['tau'] // 2)
        elif kind == 'b':
            u2, b2 = fb4_Cform_ab(k, 'b', r['tau'], d['kc'], j, m)
        else:
            Rc = r['R']
            u2, b2 = fb4_Cform_c(k, r['tau'], d['kc'], j, m, Rc, r['lam'])
        chk(tag + '_fb4_closed', tf_eq(d['Cform'][0], d['Cform'][1], u2, b2, m), (j, m))
        # boundary divisibility of the explicit sum
        S = d.get('S') if kind == 'a' else d.get('U')
        eps1 = d['ell'] - 2  # first-step eps (a: 0)
        # type a: 2^(j-2)|S ; type b: 2^(j-2)|U ; type c: 2^(j-1-eps)|U
        tex = (j - 2) if kind in ('a', 'b') else (j - 1 - eps1)
        chk(tag + '_fb4_div', (v2(S) >= tex) == res['boundary'], (j, m, v2(S), tex))
        if res['boundary']:
            if S != 0:
                chk(tag + '_fb4_size', abs(S) >= 1 << tex, (j, m))
                Pm = Pc(m)
                if kind == 'a':
                    ok = (1 << j) <= 4 * (3 * m * Pm + 3)
                elif kind == 'b':
                    ok = (1 << j) <= 4 * (21 * m * Pm + 20)
                else:
                    ok = (1 << (j - 1 - eps1)) <= 30 * m * Pm + 29
                chk(tag + '_fb4_clock', ok, (j, m))
    if b == 'I':
        r = rows(m - 1)
        if r['kind'] == 'a':
            E = k + 1 + r['tau'] // 2
            chk(tag + '_I_free_a', v2(E) >= j - 2, (j, m))
            if E != 0:
                chk(tag + '_I_clock_a', (1 << j) <= 8 * 6 * m * Pc(m), (j, m))
        else:
            chk(tag + '_I_free_bc', r['omega'] >= j - 1, (j, m))
            chk(tag + '_I_clock_bc', (1 << j) <= 8 * (6 * r['tau'] + 5), (j, m))
            chk(tag + '_I_mass', (1 << (j - 1)) <= 6 * r['tau'] + 5, (j, m))


def main():
    t0 = time.time()
    rng = random.Random(20261110)
    cal = Cal()
    rows = Rows(cal)
    gj = [j for j in range(5, JMAX) if cal.k(j) is not None]
    print('PART 0: calendar up, %d odd-a chains j < %d' % (len(gj), JMAX), flush=True)

    # ---------------- PART 1: engine vs exact integer replays (sample) --------------
    done = 0
    for j in gj[::max(1, len(gj) // 12)]:
        k = cal.k(j)
        got = 0
        for m in range(j, min(j + 600, MMAX)):
            if not rows(m - 1)['odd']:
                continue
            res = analyze_pair(rows, j, k, m, max_steps=m + 3)
            if res['status'] == 'GATE':
                w, _ = replay_exact(cal, rows, j, k, m, res['trace'], rng)
                chk('P1_replay', w[:len(res['trace'])] == [t[1]['jn'] for t in res['trace']],
                    (j, m, w[:8]))
                done += 1
                got += 1
                if got >= 5:
                    break
    print('PART 1: %d determined-gate replays vs cyc.walk' % done, flush=True)

    # ---------------- PART 1b: engine vs the accepted branch.explore -----------------
    # for generic postgate starts (j, m): branch.explore with min_bits=0 has exactly one
    # leaf (a free step is CUT at bits >= 0, not split), whose status classifies the
    # generic continuation: GATE = determined to the next gate, END = determined end,
    # CUT_BITS = a free (split) step.  det_walk must return the matching status, and for
    # GATE the very word.  (branch.py's ZERO leaf = identically-zero output form is
    # unreachable here: the V-coefficient never vanishes on these starts; both engines
    # classify it as non-determined, only the name differs.)
    agree = 0
    p1b = dict(GATE=0, END=0, CUT=0)
    for j in gj:
        if j >= 60:
            break
        k = cal.k(j)
        for m in range(j, 300):
            if not rows(m - 1)['odd']:
                continue
            Th0 = {1: F(2 ** (j - 2) + 3 * (k + 1)), 'X': F(2 ** (j - 1))}
            x0 = {1: F(2 ** m), 'V': F(2 ** (m + 1))}
            L = br.explore(cal, m, Th0, x0, min_bits=0, stop_at_gate=True, max_leaves=4)
            chk('P1b_oneleaf', len(L) == 1 and L[0]['bits'] == 0, (j, m, len(L)))
            st_b = L[0]['status']
            res = analyze_pair(rows, j, k, m, max_steps=m + 3)
            if st_b == 'GATE':
                p1b['GATE'] += 1
                chk('P1b_det', res['status'] == 'GATE', (j, m, res['status']))
                if res['status'] == 'GATE':
                    w1 = [s[3] for s in L[0]['steps']]
                    w2 = [t[1]['jn'] for t in res['trace']]
                    chk('P1b_word', w1 == w2, (j, m, w1[:6], w2[:6]))
                    agree += 1
            elif st_b == 'END':
                p1b['END'] += 1
                chk('P1b_end', res['status'] == 'END', (j, m, res['status']))
            else:                      # CUT_BITS: a free step in the generic tree
                p1b['CUT'] += 1
                chk('P1b_split', res['status'] == 'SPLIT', (j, m, res['status']))
                if res['status'] == 'SPLIT':
                    # my engine must agree with the leaf's word on the determined prefix
                    # (all steps of my trace except the final free one)
                    pre = [t[1]['jn'] for t in res['trace'][:-1]]
                    w1 = [s[3] for s in L[0]['steps']]
                    chk('P1b_splitprefix', w1[:len(pre)] == pre, (j, m, w1[:6], pre[:6]))
    print('PART 1b: %d determined words identical to branch.explore; leaf mix %s'
          % (agree, p1b), flush=True)

    # ---------------- PART 2/3/4: postgate census -----------------------------------
    census = dict(pairs=0, det_end=0, split=0, limit=0, gates=0, boundary=0,
                  by_branch={'I': 0, 'II': 0, 'III': 0}, bII_zero=0, bII_nonzero=0,
                  by_dR={}, p3_all=0, p3_le=0, p3_super=0, typec_two_step=0)
    boundary_list = []
    for j in gj:
        k = cal.k(j)
        for m in range(j, MMAX):
            if not rows(m - 1)['odd']:
                continue
            census['pairs'] += 1
            # cap m+3 is a priori complete: a determined walk has v2(B)=m+1-ell, so once
            # ell >= m-3 every further determined chain is <= 3 and the walk ENDs; hence
            # LIMIT is impossible for determined walks and signals an engine defect.
            res = analyze_pair(rows, j, k, m, max_steps=m + 3)
            if res['status'] == 'END':
                census['det_end'] += 1
            elif res['status'] == 'SPLIT':
                census['split'] += 1
            elif res['status'] == 'LIMIT':
                census['limit'] += 1
            # branch-(I) machinery: FREE congruences at EVERY pair whose first landing
            # (by the accepted LAND formula) is an escape c1 >= j-1, whatever the walk
            # does afterwards (in these ranges such pairs end or split; none gates)
            r_in = rows(m - 1)
            if r_in['kind'] == 'a':
                c1f = 1 + v2(2 ** (j - 2) + 3 * (k + 1 + r_in['tau'] // 2))
            else:
                c1f = r_in['omega']
            if c1f >= j - 1:
                census['escape_landings'] = census.get('escape_landings', 0) + 1
                census['escape_outcome_' + res['status']] = \
                    census.get('escape_outcome_' + res['status'], 0) + 1
                if r_in['kind'] == 'a':
                    E = k + 1 + r_in['tau'] // 2
                    chk('P2I_free_a', v2(E) >= j - 2, (j, m))
                    if E != 0:
                        chk('P2I_clock_a', (1 << j) <= 8 * 6 * m * Pc(m), (j, m))
                else:
                    chk('P2I_free_bc', r_in['omega'] >= j - 1, (j, m))
                    chk('P2I_mass', (1 << (j - 1)) <= 6 * r_in['tau'] + 5, (j, m))
                    chk('P2I_clock_bc', (1 << j) <= 8 * (6 * r_in['tau'] + 5), (j, m))
            if res['status'] == 'GATE':
                census['gates'] += 1
                invariants(rows, j, k, m, res, 'P2')
                if res['boundary']:
                    census['boundary'] += 1
                    census['by_branch'][res['branch']] += 1
                    census['by_dR'][res['dR']] = census['by_dR'].get(res['dR'], 0) + 1
                    check_boundary_instance(rows, cal, j, k, m, res, 'P24', rng)
                    if res['branch'] == 'II':
                        S = res['fb4'].get('S') or res['fb4'].get('U')
                        if S == 0:
                            census['bII_zero'] += 1
                        else:
                            census['bII_nonzero'] += 1
                    boundary_list.append(dict(j=j, m=m, dR=res['dR'], branch=res['branch'],
                                              mprime=res['mprime'], ell=res['ell'],
                                              Lbc=res['Lbc']))
                    w, _ = replay_exact(cal, rows, j, k, m, res['trace'], rng)
                    chk('P2_brep', w[:len(res['trace'])] == [t[1]['jn'] for t in res['trace']],
                        (j, m))
                elif census['gates'] % 7 == 0:
                    # P2_srep: sampled exact integer replay of every 7th determined gate
                    w, _ = replay_exact(cal, rows, j, k, m, res['trace'], rng)
                    chk('P2_srep', w[:len(res['trace'])] == [t[1]['jn'] for t in res['trace']],
                        (j, m))
            # PART 3: closed forms for every determined two-step a-step at c1 (gate or
            # not).  Population note (review round 1): p3_all counts every pair with a
            # determined first landing and an odd a-crossing at c1 (no c1<=j-2 filter);
            # p3_le restricts to c1 <= j-2; the difference is exactly the type-b/c
            # super-escape landings c1 = omega(m-1) >= j (p3_super).
            d4 = fb4(rows, j, k, m)
            if d4 and not d4.get('no_astep'):
                census['p3_all'] += 1
                r = rows(m - 1)
                if d4['c1'] <= j - 2:
                    census['p3_le'] += 1
                elif r['kind'] != 'a' and d4['c1'] >= j:
                    census['p3_super'] += 1
                if d4['kind'] == 'c':
                    census['typec_two_step'] += 1
                if d4['kind'] == 'a':
                    u2, b2 = fb4_Cform_ab(k, 'a', None, d4['kc'], j, m, Km=r['tau'] // 2)
                elif d4['kind'] == 'b':
                    u2, b2 = fb4_Cform_ab(k, 'b', r['tau'], d4['kc'], j, m)
                else:
                    u2, b2 = fb4_Cform_c(k, r['tau'], d4['kc'], j, m, r['R'], r['lam'])
                chk('P3_closed', tf_eq(d4['Cform'][0], d4['Cform'][1], u2, b2, m), (j, m))
                if d4['det2']:
                    chk('P3_mprime', tf_v2(d4['Cform'][0], d4['Cform'][1], m) == d4['mprime'],
                        (j, m))
    print('PART 2/3/4: postgate census %s' % json.dumps(census, sort_keys=True), flush=True)

    # ---------------- PART 2b: extended deep scan for boundary instances -------------
    # larger m for the few j that have continuing pairs, to sample branch-(III) paths.
    ext = dict(pairs=0, gates=0, boundary=0, deep_gates=0, by_branch={'I': 0, 'II': 0, 'III': 0})
    ext_boundary = []
    for j in (24, 42) if not QUICK else (24,):
        k = cal.k(j)
        MM = 60000 if QUICK else 150000
        for m in range(j, MM):
            if not rows(m - 1)['odd']:
                continue
            ext['pairs'] += 1
            res = analyze_pair(rows, j, k, m, max_steps=m + 3)
            if res['status'] == 'GATE':
                ext['gates'] += 1
                if len(res['trace']) >= 3:
                    ext['deep_gates'] += 1
                invariants(rows, j, k, m, res, 'P2b')
                if res['boundary']:
                    ext['boundary'] += 1
                    ext['by_branch'][res['branch']] += 1
                    check_boundary_instance(rows, cal, j, k, m, res, 'P2b', rng)
                    w, _ = replay_exact(cal, rows, j, k, m, res['trace'], rng)
                    chk('P2b_brep', w[:len(res['trace'])] == [t[1]['jn'] for t in res['trace']],
                        (j, m))
                    ext_boundary.append(dict(j=j, m=m, dR=res['dR'], branch=res['branch'],
                                             depth=len(res['trace']) - 1))
    print('PART 2b: extended scan %s boundary=%s' % (json.dumps(ext), ext_boundary[:10]),
          flush=True)

    # ---------------- PART 5: counterexamples ----------------------------------------
    cex = [('A', 24, 6268562, 1), ('B', 42, 1095510131453, 3),
           ('B2', 78, 526980180956824005813092, 3)]
    for nm, j, m, dRexp in cex:
        k = cal.k(j)
        res = analyze_pair(rows, j, k, m, max_steps=m + 3)
        chk('P5_%s_gate' % nm, res['status'] == 'GATE', (nm, res['status']))
        chk('P5_%s_dR' % nm, res['dR'] == dRexp, (nm, res['dR']))
        chk('P5_%s_boundary' % nm, res['boundary'] is True, (nm,))
        invariants(rows, j, k, m, res, 'P5_' + nm)
        check_boundary_instance(rows, cal, j, k, m, res, 'P5_' + nm, rng)
        # exact replay: A full big-integer; B/B2 mod 2^P
        if m <= 20 * 10 ** 6:
            w, _ = replay_exact(cal, rows, j, k, m, res['trace'], rng)
            chk('P5_%s_replay' % nm, w[:len(res['trace'])] == [t[1]['jn'] for t in res['trace']],
                (nm, w[:6]))
        wm = replay_mod(cal, rows, j, k, m, res['trace'], rng)
        chk('P5_%s_replaymod' % nm,
            wm[:len(res['trace'])] == [t[1]['jn'] for t in res['trace']], (nm, wm[:6]))
        print('PART 5: cex %s j=%d m=%d dR=%d branch=%s mprime=%d OK' %
              (nm, j, m, res['dR'], res['branch'], res['mprime']), flush=True)

    # ---------------- PART 6: sweep census (forced-gate starts, branching tree) ------
    sw = dict(starts=0, leaves=0, pairs=0, pairs_det=0, pairs_free=0, pairs_long=0,
              pairs_free_nogen=0, pairs_free_worddiff=0,
              boundary=0, by_branch={'I': 0, 'II': 0, 'III': 0})
    sw_boundary = []
    for j in [q for q in range(5, SWJ) if cal.k(q) is not None]:
        k = cal.k(j)
        Th0 = {1: F(2 ** (j - 2) - 3 * k), 'X': F(2 ** (j - 1))}
        x0 = {1: F(2 ** j), 'V': F(2 ** (j + 1))}
        L = br.explore(cal, j, Th0, x0, min_bits=SWB, max_leaves=5 * 10 ** 6)
        sw['starts'] += 1
        sw['leaves'] += len(L)
        for l in L:
            steps = l['steps']
            gates = [i for i, s in enumerate(steps) if s[1] == 'a' and s[3] >= s[0]]
            for a, b in zip(gates, gates[1:]):
                sw['pairs'] += 1
                ja, ka, ma = steps[a][0], steps[a][2], steps[a][3]
                res = analyze_pair(rows, ja, ka, ma, max_steps=ma + 3)
                # the realized path between the gates:
                mid = [s[3] for s in steps[a + 1:b + 1]]
                if res['status'] == 'GATE':
                    gen = [t[1]['jn'] for t in res['trace']]
                    if gen == mid:
                        sw['pairs_det'] += 1
                        invariants(rows, ja, ka, ma, res, 'P6')
                        if sw['pairs_det'] % 97 == 0 and ma <= 5000:
                            w, _ = replay_exact(cal, rows, ja, ka, ma, res['trace'], rng)
                            chk('P6_srep',
                                w[:len(res['trace'])] == [t[1]['jn'] for t in res['trace']],
                                (ja, ma))
                        if res['boundary']:
                            sw['boundary'] += 1
                            sw['by_branch'][res['branch']] += 1
                            check_boundary_instance(rows, cal, ja, ka, ma, res, 'P6', rng)
                            sw_boundary.append(dict(j=ja, m=ma, dR=res['dR'],
                                                    branch=res['branch']))
                    else:
                        # engine disagreement: determined to a gate but a different word
                        sw['pairs_free'] += 1
                        sw['pairs_free_worddiff'] += 1
                        chk('P6_worddiff_none', False, (ja, ma, gen[:6], mid[:6]))
                elif res['status'] == 'SPLIT':
                    sw['pairs_free'] += 1
                    sw['pairs_free_nogen'] += 1
                    # substantive: my engine must agree with the leaf's realized word on
                    # the whole determined prefix before the split position
                    pre = [t[1]['jn'] for t in res['trace'][:-1]]
                    chk('P6_splitprefix', mid[:len(pre)] == pre and len(pre) < len(mid),
                        (ja, ma, pre[:6], mid[:6]))
                else:
                    sw['pairs_free'] += 1
                    sw['pairs_long'] += 1
                    chk('P6_limit_none', False, (ja, ma, res['status']))
        if j % 400 == 0:
            print('   sweep at j=%d: %s' % (j, json.dumps(sw)), flush=True)
    print('PART 6: sweep census %s' % json.dumps(sw), flush=True)

    # ---------------- PART 7: seeded constructions ------------------------------------
    seeded = []

    def chain_of_label(kk):
        try:
            f = cal.C.preceding_fire_by_time(2 * kk)
        except ValueError:
            return None
        if f['k'] != kk:
            return None
        return f['pointer'] + 1

    # type a: k_j = 9 mod 16; S_a = k+5+3 k_m = 0 mod 2^(j-1)  (u = S_a/2^(j-2) even)
    #         -> determined 5-gate with output m' = j-2, dR = 1 (needs m > j)
    for j in (24, 61, 97):
        k = cal.k(j)
        if k is None or k % 16 != 9:
            continue
        M = 1 << (j - 1)
        r0 = (-(k + 5) * pow(3, -1, M)) % M
        got = None
        for i in range(SEED_ITERS):
            km = r0 + i * M
            m = chain_of_label(km)
            if m is None or m < j + 1:
                continue
            if cal.k(m) != km:
                continue
            got = (km, m)
            break
        if got is None:
            print('PART 7: type-a j=%d: no instance in %d iterations' % (j, SEED_ITERS),
                  flush=True)
            continue
        km, m = got
        res = analyze_pair(rows, j, k, m, max_steps=m + 3)
        chk('P7a_%d_gate' % j, res['status'] == 'GATE' and res['boundary'], (j, m, res['status']))
        if res['status'] == 'GATE':
            chk('P7a_%d_dR' % j, res['dR'] == 1, (j, m, res['dR']))
            chk('P7a_%d_mprime' % j, res['mprime'] == j - 2, (j, m, res['mprime']))
            chk('P7a_%d_branch' % j, res['branch'] == 'II', (j, m))
            invariants(rows, j, k, m, res, 'P7a_%d' % j)
            check_boundary_instance(rows, cal, j, k, m, res, 'P7a_%d' % j, rng)
            wm = replay_mod(cal, rows, j, k, m, res['trace'], rng)
            chk('P7a_%d_replay' % j,
                wm[:len(res['trace'])] == [t[1]['jn'] for t in res['trace']], (j, m, wm[:6]))
            seeded.append(dict(kind='a', j=j, m=m, km=km, dR=res['dR'], mprime=res['mprime']))
            print('PART 7: type-a j=%d m=%d (k_m=%d) dR=%d mprime=%d' %
                  (j, m, km, res['dR'], res['mprime']), flush=True)
            # razor edge: the u-ODD class k_m = km ± 2^(j-2) (v2(S_a) = j-2 exactly) must
            # SPLIT at the gate step (FB-4(a): u odd -> output valuation >= v2(A))
            for kmr in (km - (1 << (j - 2)), km + (1 << (j - 2))):
                if kmr <= 0:
                    continue
                mr = chain_of_label(kmr)
                if mr is None or mr < j + 1 or cal.k(mr) != kmr:
                    continue
                resr = analyze_pair(rows, j, k, mr, max_steps=mr + 3)
                chk('P7r_%d_split' % j, resr['status'] == 'SPLIT', (j, mr, resr['status']))
                # concrete demonstration of the split: two walks in the cylinder with
                # X0 even resp. odd must land identically at c1 and DIFFER at the gate
                # step (FB-4(a): u odd makes the output valuation X-dependent; one of
                # the two walks reads exactly v2(A) = j-1, the other >= j)
                wven = replay_mod(cal, rows, j, k, mr, resr['trace'], rng, X0=2 * rng.getrandbits(60), nsteps=2)
                wodd = replay_mod(cal, rows, j, k, mr, resr['trace'], rng, X0=2 * rng.getrandbits(60) + 1, nsteps=2)
                chk('P7r_%d_c1same' % j, wven[:1] == wodd[:1], (j, mr, wven, wodd))
                chk('P7r_%d_gate_differs' % j, len(wven) > 1 and len(wodd) > 1
                    and wven[1] != wodd[1] and min(wven[1], wodd[1]) == j - 1,
                    (j, mr, wven, wodd))
                if mr <= 10 ** 7:      # branch-engine cross-check only when 2^mr fits
                    Th0 = {1: F(2 ** (j - 2) + 3 * (k + 1)), 'X': F(2 ** (j - 1))}
                    x0 = {1: F(2 ** mr), 'V': F(2 ** (mr + 1))}
                    Lr = br.explore(cal, mr, Th0, x0, min_bits=1, stop_at_gate=True,
                                    max_leaves=8)
                    chk('P7r_%d_branchsplit' % j,
                        any(l['bits'] >= 1 for l in Lr), (j, mr, [l['bits'] for l in Lr][:4]))
                seeded.append(dict(kind='a-razor', j=j, m=mr, km=kmr, dR=None,
                                   mprime='SPLIT'))
                print('PART 7: razor u-odd j=%d m=%d (k_m=%d) -> SPLIT '
                      '(demo walks differ at gate step%s)' %
                      (j, mr, kmr, '; branch engine agrees' if mr <= 10 ** 7 else ''),
                      flush=True)
                break

    # type b: k_j = 1 mod 16; tau_m/2 = -(12k+32)/(2*9) mod 2^(j-3)
    for j in (42, 78):
        k = cal.k(j)
        if k is None or k % 16 != 1:
            continue
        M = 1 << (j - 3)
        r0 = (-(6 * k + 16) * pow(9, -1, M)) % M    # 9*tau = -(12k+32) mod 2^(j-2), tau = 2 kk
        got = None
        for i in range(SEED_ITERS):
            kk = r0 + i * M
            try:
                f = cal.C.preceding_fire_by_time(2 * kk)
            except ValueError:
                break
            if f['k'] != kk:
                continue
            m = f['pointer'] + 2
            row = rows(m - 1)
            if row['kind'] != 'b' or row['tau'] != 2 * kk:
                continue
            if m < j + 2:
                continue
            got = (kk, m)
            break
        if got is None:
            print('PART 7: type-b j=%d: no instance in %d iterations' % (j, SEED_ITERS),
                  flush=True)
            continue
        kk, m = got
        res = analyze_pair(rows, j, k, m, max_steps=m + 3)
        chk('P7b_%d_gate' % j, res['status'] == 'GATE' and res['boundary'], (j, m, res['status']))
        if res['status'] == 'GATE':
            chk('P7b_%d_dR' % j, res['dR'] in (2, 3), (j, m, res['dR']))
            invariants(rows, j, k, m, res, 'P7b_%d' % j)
            check_boundary_instance(rows, cal, j, k, m, res, 'P7b_%d' % j, rng)
            wm = replay_mod(cal, rows, j, k, m, res['trace'], rng)
            chk('P7b_%d_replay' % j,
                wm[:len(res['trace'])] == [t[1]['jn'] for t in res['trace']], (j, m, wm[:6]))
            seeded.append(dict(kind='b', j=j, m=m, tau_half=kk, dR=res['dR'],
                               mprime=res['mprime']))
            print('PART 7: type-b j=%d m=%d dR=%d mprime=%d' % (j, m, res['dR'], res['mprime']),
                  flush=True)

    # ---------------- PART 7b: constructed type-c two-step pairs ---------------------
    # the census box contains ZERO type-c two-step pairs (the first odd c-crossing with
    # omega = 5 and an a-step at c1 is m = 6133 > 5000; census['typec_two_step'] must be
    # 0).  Verify the U_c closed form on constructed pairs (m = 6133 with several gates j).
    chk('P7c_census_vacuous', census['typec_two_step'] == 0, census['typec_two_step'])
    mc = 6133
    rc = rows(mc - 1)
    chk('P7c_row', rc['odd'] and rc['kind'] == 'c' and rc['omega'] == 5, (mc, rc['kind']))
    for j in (24, 42, 61, 97, 152, 186, 239, 275):
        k = cal.k(j)
        if k is None:
            continue
        d4 = fb4(rows, j, k, mc)
        chk('P7c_%d_fb4' % j, d4 is not None and not d4.get('no_astep')
            and d4['kind'] == 'c', (j,))
        if d4 and not d4.get('no_astep'):
            u2, b2 = fb4_Cform_c(k, rc['tau'], d4['kc'], j, mc, rc['R'], rc['lam'])
            chk('P7c_%d_closed' % j, tf_eq(d4['Cform'][0], d4['Cform'][1], u2, b2, mc), (j,))
            if d4['det2']:
                chk('P7c_%d_mprime' % j,
                    tf_v2(d4['Cform'][0], d4['Cform'][1], mc) == d4['mprime'], (j,))
    seeded.append(dict(kind='c-constructed', m=mc, js=[24, 42, 61, 97, 152, 186, 239, 275]))
    print('PART 7b: type-c closed form verified on m=6133 x 8 gates; census type-c count %d'
          % census['typec_two_step'], flush=True)

    # ---------------- PART 7c: the j=24 type-b two-step family is empty --------------
    # (review round 1).  The U_b-class for j=24 is 9*tau = -140 mod 2^22; its members are
    # REALIZED as type-b crossings at every class label (first at m = 1,044,747), but the
    # class fixes tau mod 2^8, hence omega = v2(3 tau + 4) = 7 on the whole class, and the
    # landing chain c1 = 7 has X(6) EVEN (fixed calendar fact), so the landing step is not
    # an a-step: no two-step type-b boundary instance exists for j = 24 at any m.  (The
    # earlier claim 'the type-b class at m ~ 1.1e12' wrongly quoted j=42's counterexample
    # B; the adversary's independent search to m <= 1.89e12 found none as well.)
    j = 24
    k = cal.k(j)
    chk('P7c24_k', k == 9, k)
    M2 = 1 << 21
    kk_lo = ((-(12 * k + 32) * pow(9, -1, 1 << 22)) // 2) % M2
    tau0 = 2 * kk_lo
    chk('P7c24_class', (9 * tau0 + 12 * k + 32) % (1 << 22) == 0, tau0)
    chk('P7c24_omega_fixed', v2(3 * tau0 + 4) == 7, tau0)      # tau mod 2^8 fixed by class
    chk('P7c24_X6_even', not rows(6)['odd'], rows(6)['kind'])  # landing 7: no a-step, ever
    n_real = 0
    first_m = None
    for i in range(200):
        kk = kk_lo + i * M2
        try:
            f = cal.C.preceding_fire_by_time(2 * kk)
        except ValueError:
            break
        if f['k'] != kk:
            continue
        m = f['pointer'] + 2
        row = rows(m - 1)
        if row['kind'] == 'b' and row['tau'] == 2 * kk:
            n_real += 1
            if first_m is None:
                first_m = m
            chk('P7c24_omega7', row['omega'] == 7, (i, m, row['omega']))
    chk('P7c24_first_realized', first_m is not None and first_m == 1044747, first_m)
    print('PART 7c: j=24 type-b U_b-class: %d/200 class labels realized (first m=%s), '
          'all omega=7 with X(6) even -> two-step family empty for j=24 at every m'
          % (n_real, first_m), flush=True)

    # ---------------- PART 8: CL2 census consistency ---------------------------------
    # substantive closing assertions (review round 1): the boundary census decomposes
    # exactly by branch; every free sweep pair was shown non-generic (split with matching
    # determined prefix, or an engine disagreement that fails P6_worddiff_none); no LIMIT.
    chk('P8_boundary_by_branch',
        sw['boundary'] == sum(sw['by_branch'].values()) == len(sw_boundary))
    chk('P8_free_decomposition',
        sw['pairs_free'] == sw['pairs_free_nogen'] + sw['pairs_free_worddiff'])
    chk('P8_no_worddiff', sw['pairs_free_worddiff'] == 0, sw['pairs_free_worddiff'])
    chk('P8_no_limit', sw['pairs_long'] == 0, sw['pairs_long'])
    # (the per-pair P6_splitprefix condition — one substantive check per nogen pair —
    #  carries the prefix-agreement content; no aggregate count identity is asserted,
    #  since any such identity would hold by construction.  Round-2 review.)
    print('PART 8: free/boundary classification exhaustive in sweep census', flush=True)

    ok = not any(vv for kk, vv in cnt.items() if kk.endswith('_FAIL'))
    out = dict(quick=QUICK, JMAX=JMAX, MMAX=MMAX, SWJ=SWJ, SWB=SWB,
               counts=cnt, fails=fails, census=census, boundary=boundary_list,
               ext=ext, ext_boundary=ext_boundary,
               sweep=sw, sweep_boundary=sw_boundary, seeded=seeded,
               seconds=round(time.time() - t0, 1), status='PASS' if ok else 'FAIL')
    print('TOTAL checks: %d, fails: %d, seconds %.1f' % (
        sum(vv for kk, vv in cnt.items() if not kk.endswith('_FAIL')), len(fails),
        time.time() - t0))
    json.dump(out, open(HERE / 'freeb_checks.json', 'w'), indent=1)
    print('ALL PASS' if ok else 'FAILED')


if __name__ == '__main__':
    main()
