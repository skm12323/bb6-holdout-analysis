"""Gate blocks entered from a chain y>=19 (Claude, direction A).  Synthetic affine states, canonical data.
State at chain y: x = 2^y U, Theta = x + theta + 2^(y+1) W, with U (odd) and W free 2-adic symbols and theta a
small rational (rank <= 1).  The walk is run on affine forms; a step is FREE (uncertified) when the output
valuation is not fixed by the constant part.  For forced walks we record the maximal relative record
max_t (j_t + Gamma_t - Gamma_y) and require it < y (block-safety: all later records below R_y)."""
import sys, json, time
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'work_ext_roots'))
from search_roots import Calendar
INF = 10**9
def v2(q):
    q = F(q)
    if q == 0: return INF
    n, d = q.numerator, q.denominator; v = 0
    while n % 2 == 0: n //= 2; v += 1
    while d % 2 == 0: d //= 2; v -= 1
    return v
cal = Calendar(512)
def add(a, b): return {k: a.get(k, 0) + b.get(k, 0) for k in set(a) | set(b)}
def mul(a, c): return {k: c*v for k, v in a.items()}
def run(y, theta, lim=60):
    U0 = 1   # U = 1 + 2V : odd
    x = {'c': F(2**y), 'V': F(2**(y+1))}
    Th = add(x, {'c': F(theta), 'W': F(2**(y+1))})
    j = y; G = 0; maxrel = -INF; gates = 0; ntg = 0; word = []
    for step in range(lim):
        r = cal.crossing(j - 1)
        if not r['odd']: return dict(status='end', maxrel=maxrel, gates=gates, nt_gates=ntg, word=word)
        tau = r['time']
        if r['kind'] == 'a':
            xn = add(mul(Th, 2), add({'c': F(3*tau)}, mul(x, F(-1, 2))))
            G += 1
        else:
            ratio = (r['head_ratio'] + 2*r['tail_ratio'])/2
            lam = r['head_lambda'] + 2*r['tail_lambda'] + 3
            xn = add(mul(x, ratio), {'c': F(lam)}); G += 1 + r['epsilon']
        Th = add(Th, {'c': F(3 + 3*tau)})
        vc = v2(xn.get('c', 0)); vs = min(v2(xn.get('V', 0)), v2(xn.get('W', 0)))
        if vc >= vs:
            return dict(status='free', at=j, free_from=vs, maxrel=maxrel, gates=gates, nt_gates=ntg, word=word)
        m = vc
        if r['kind'] == 'a' and m >= j - 1: gates += 1
        if r['kind'] == 'a' and m >= j: ntg += 1
        word.append(m); j = m; x = xn
        if step >= 0: maxrel = max(maxrel, j + G)
        if j < 2: return dict(status='small', maxrel=maxrel, gates=gates, nt_gates=ntg, word=word)
    return dict(status='limit', maxrel=maxrel, gates=gates, nt_gates=ntg, word=word)

def main():
    T0 = time.time(); st = Counter(); bad = []; gated = Counter(); worst = (-INF, None)
    small = [F(t) for t in range(-60, 61)] + [F(c, 3) for c in range(-180, 181) if c % 3]
    FULL = int(sys.argv[3]) if len(sys.argv) > 3 else 252
    HR = {0: 2048, 1: 2048, 2: 760, 3: 330, 4: 190}       # height caps by 3-adic rank
    def thetas(y):
        if y >= FULL: base = small
        else:
            base = [F(t) for t in range(-HR[0], HR[0]+1)]
            for r in (1, 2, 3, 4):
                Q = 3**r; base += [F(c, Q) for c in range(-Q*HR[r], Q*HR[r]+1) if c % 3]
        for th in base:
            for b in (0, 1): yield th + b*2**y
    Y0 = int(sys.argv[1]) if len(sys.argv) > 1 else 19
    Y1 = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    for y in range(Y0, Y1):
        for th in thetas(y):
            res = run(y, th)
            st[res['status']] += 1
            if res['gates']: gated[res['gates']] += 1
            if res['status'] == 'free' or res['maxrel'] > y or res['gates'] >= 2:
                if len(bad) < 30: bad.append(dict(y=y, theta=str(th), **{k: v for k, v in res.items()}))
                st['UNSAFE_OR_FREE'] += 1
            if res['status'] != 'free':
                rel = res['maxrel'] - y
                if rel > worst[0]: worst = (rel, dict(y=y, theta=str(th), word=res['word']))
    out = dict(stats=dict(st), walks_with_gates=dict(gated), worst_relative_record=worst, problems=bad,
               seconds=round(time.time()-T0, 1),
               scope='Synthetic affine starts on canonical data: y in [%d,%d); for y<%d all classes of 3-adic rank r<=4 with height <= HR[r] (2048,2048,760,330,190) and both lift bits, otherwise rank<=1 heights<=60; not reachability.' % (Y0, Y1, FULL))
    HERE.joinpath('gates_checks.json' if len(sys.argv) <= 1 else 'gates_checks_%s_%s.json' % (Y0, Y1)).write_text(json.dumps(out, indent=1, default=str), encoding='utf-8')
    print(json.dumps({k: out[k] for k in ('stats', 'walks_with_gates', 'worst_relative_record', 'seconds')}, default=str))
    for b in bad[:8]: print(b)
main()
