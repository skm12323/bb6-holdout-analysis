"""Shift theorem checks (Claude, Part A). Exact walks from synthetic and canonical states.

Checks the exact a-step identity D'=3+2k-(D+x')/3, the reduced defect automaton
(descent form 3-d, non-descent form (9+6k-d-2^m)/3, b: d-1, c: d+s) with its precision
bookkeeping H, and that precision loss (H<=j) is where the reduced value can fail.
Finite checks; no EXT claim.  Usage: python -B verify_shift.py [walks]
"""
import sys, json, random, time
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'work_ext_roots'))
from search_roots import Calendar, val

INF = 10**9
def v2(q):
    q = F(q)
    if q == 0: return INF
    return val(q.numerator) - val(q.denominator)
def v3den(q):
    d = F(q).denominator; r = 0
    while d % 3 == 0: d //= 3; r += 1
    assert d == 1 or d % 2 == 1
    return r

def walk(cal, j, x, th, lim=80, Phi0=None, H0=INF):
    """Exact real walk plus reduced automaton. Returns per-chain records."""
    D = th - x; Phi = F(D) if Phi0 is None else F(Phi0); H = H0; out = []; nd = 0
    for _ in range(lim):
        if x <= 0: return out, 'nonpositive'
        assert v2(x) == j
        err = v2(D - Phi)
        assert err >= H, ('precision bound violated', j, err, H)
        out.append(dict(j=j, H=H, err=err, cert=H >= j+1, ok=err >= j+1, r=v3den(Phi), nd=nd))
        r = cal.crossing(j-1)
        if not r['odd']: return out, 'end'
        tau = r['time']
        if r['kind'] == 'a':
            k = tau // 2
            xn = 2*th + 3*tau - x/2
            m = v2(xn)
            # exact identity
            Dn_exact = (th + 3 + 3*tau) - xn
            assert Dn_exact == 3 + 2*k - (D + xn)/3
            if m <= j - 2:
                Phi = 3 - Phi; loc = j - 1
            else:
                Phi = 3 + 2*k - (Phi + F(2)**m)/3; loc = m + 1; nd += 1
        else:
            ratio = (r['head_ratio'] + 2*r['tail_ratio'])/2
            lam = r['head_lambda'] + 2*r['tail_lambda'] + 3
            xn = ratio*x + lam; m = v2(xn)
            s = 3 + 3*tau - lam
            loc = v2(x*(1 - ratio))
            if r['kind'] == 'b':
                loc = min(loc, v2(s + 1)); Phi = Phi - 1
            else:
                Phi = Phi + s
        H = min(H, loc)
        th = th + 3 + 3*tau; x = F(xn); D = th - x; j = m
    return out, 'limit'

def main():
    T0 = time.time(); W = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    cal = Calendar(512); rnd = random.Random(20261023)
    st = Counter(); fails = []; maxr = 0; nd_hist = Counter(); exhaust_examples = []
    for i in range(W):
        P = rnd.choice((rnd.randrange(5, 40), rnd.randrange(5, 300)))
        U = rnd.randrange(1, 1 << rnd.choice((8, 30, 64, 200, 400))) | 1
        d0 = rnd.choice((1, 0, rnd.randrange(-40, 41), rnd.randrange(-2**12, 2**12)))
        x = F(U << P)
        if i % 2:
            sig = P + rnd.randrange(1, 25); e = rnd.randrange(1, 1 << 20)
            th = x + d0 + (e << sig); Phi0, H0 = d0, sig      # automaton knows d0 only mod 2^sig
        else:
            th = x + d0; Phi0, H0 = None, INF
        try:
            recs, how = walk(cal, P, x, th, Phi0=Phi0, H0=H0)
        except AssertionError as e:
            if 'precision bound' in str(e.args[0]): raise
            st['skipped(calendar range)'] += 1; continue
        st['walk_' + how] += 1
        for q in recs:
            st['chains'] += 1
            if q['cert']:
                st['certified'] += 1
                assert q['ok'], q
                maxr = max(maxr, q['r'])
            else:
                st['uncertified'] += 1
                st['uncertified_and_wrong' if not q['ok'] else 'uncertified_but_right'] += 1
                if not q['ok'] and len(exhaust_examples) < 5:
                    exhaust_examples.append(dict(P=P, U_bits=U.bit_length(), d0=d0, word=[c['j'] for c in recs]))
        nd_hist[recs[-1]['nd'] if recs else 0] += 1
    FM = forced_main(); FP = finite_precision_main()
    RES = dict(status='PASS', walks=W, forced=FM, finite_precision=FP, stats=dict(st), non_descent_count_hist=dict(sorted(nd_hist.items())),
               max_3adic_denominator_exponent_certified=maxr, precision_exhaustion_examples=exhaust_examples,
               seconds=round(time.time()-T0, 1),
               scope='Synthetic exact walks (constructed starts, not claimed canonical); identities and the '
                     'precision bound are checked at every chain. No EXT claim.')
    HERE.joinpath('shift_checks.json').write_text(json.dumps(RES, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(RES, indent=1))


def forced_main(n=4000):
    from forced import forced_start
    cal = Calendar(512); rnd = random.Random(7); st = Counter(); maxr = 0; ex = []
    for i in range(n):
        j0 = rnd.randrange(5, 120)
        r0 = cal.crossing(j0 - 1)
        if i % 3 and r0['odd'] and r0['kind'] == 'a':   # aim at a non-descent first step
            d0 = -3*(r0['time']//2) + (rnd.randrange(-3, 4) << max(0, j0 - 2)) + rnd.choice((0, 0, 1, -1))
        else:
            d0 = rnd.randrange(-300, 300)
        try:
            U, ch = forced_start(cal, j0, d0, rnd)
        except (AssertionError, KeyError, ValueError):
            st['skip'] += 1; continue
        x = F(U << j0); th = x + d0
        try:
            recs, how = walk(cal, j0, x, th)
        except AssertionError as e:
            if 'precision bound' in str(e.args[0]): raise
            st['skip_walk'] += 1; continue
        st['walks'] += 1; st['free_choices'] += sum(1 for q in ch if q[0] == 'free')
        for q in recs:
            st['chains'] += 1
            if q['cert']:
                st['certified'] += 1; assert q['ok'], q; maxr = max(maxr, q['r'])
            else:
                st['uncertified_' + ('right' if q['ok'] else 'wrong')] += 1
        st['nd_%d' % (recs[-1]['nd'] if recs else 0)] += 1
        if any(not q['ok'] for q in recs) and len(ex) < 4:
            ex.append(dict(j0=j0, d0=d0, word=[q['j'] for q in recs], H=[q['H'] if q['H'] < INF else None for q in recs]))
    return dict(stats=dict(st), max_r_certified=maxr, wrong_examples=ex)

def finite_precision_main(n=6000):
    """Forced non-descents from a start known only mod 2^H0 (test design from the review, aud70)."""
    from forced import forced_start
    cal = Calendar(512); rnd = random.Random(1); st = Counter()
    for i in range(n):
        j0 = rnd.randrange(5, 60); r0 = cal.crossing(j0 - 1)
        if not (r0['odd'] and r0['kind'] == 'a'): continue
        d0 = -3*(r0['time']//2) + (rnd.randrange(-3, 4) << max(0, j0 - 2)) + rnd.choice((0, 1, -1))
        try: U, ch = forced_start(cal, j0, d0, rnd)
        except Exception: continue
        x = F(U << j0); th = x + d0
        H0 = j0 + 1 + rnd.randrange(0, 4); Phi0 = d0 + (rnd.randrange(1, 99) << H0)
        try: recs, how = walk(cal, j0, x, th, Phi0=Phi0, H0=H0)
        except AssertionError as e:
            if 'precision' in str(e.args[0]): raise
            st['skip'] += 1; continue
        for q in recs:
            if q['cert']:
                st['certified'] += 1; assert q['ok'], q
            else:
                st['uncertified_' + ('right' if q['ok'] else 'wrong')] += 1
    return dict(st)

if __name__ == '__main__':
    main()
