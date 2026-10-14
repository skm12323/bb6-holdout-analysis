"""verify_g2.py -- finite checks for work_g2/PROOF_G2.md.  Run: python -B verify_g2.py [NM]
Uses the exact crossing data of F from work_claude_global/fdata.py (read-only import)."""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work_claude_global'))
from fdata import crossings, v2
from collections import Counter
NM = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
tau, typ, hpar, X = crossings(NM + 60)
R = Counter()
def ok(name, cond):
    R[name + (' ok' if cond else ' FAIL')] += 1
    if not cond: print('FAIL', name)

def run(Th, x, limit):
    """exit recurrence (NOTES s1). returns list of (Theta, x, j, type_of_return)."""
    tr = []
    while True:
        j = v2(x); n = j - 1
        if n >= limit: tr.append((Th, x, j, '?')); return tr
        if n < 0 or not hpar[n]: tr.append((Th, x, j, 'e')); return tr
        t = typ[n]; tr.append((Th, x, j, t))
        if t == 'a': k = tau[n] // 2; x = 2*Th - x//2 + 6*k; Th = Th + 3 + 6*k
        else: cX, lX, _ = X[n]; assert (cX * x) % (1 << j) == 0; x = (cX * x >> j) + lX; Th = Th + 3*tau[n] + 3

# ---- input facts used by the proofs
for n in range(1, NM):
    ok('F0 tau(n)<=n', tau[n] <= n)
    if typ[n] == 'b' and hpar[n]:
        cX, lX, _ = X[n]; s = tau[n]
        ok('F1 b-crossing: cX=3*2^(n-1), lamX=3tau+4, tau even>=1', cX == 3 << (n-1) and lX == 3*s + 4 and s % 2 == 0 and s >= 1)
    if typ[n] in 'ab' and hpar[n]: ok('F2 a/b odd head => tau even >=1', tau[n] % 2 == 0 and tau[n] >= 1)
    if typ[n] == 'c' and hpar[n]: ok('F3 c-crossing: v2(cX)=n-eps, 0<=eps<=7', 0 <= n - v2(X[n][0]) <= 7)
# small parameters for Lemma A (J<=11 and q<=5)
small = [(J, tau[J-1], v2(3*tau[J-1]+4)) for J in range(3, 12) if typ[J-1] == 'b' and hpar[J-1]]
print('small b-type J (J, s\', q):', small, ' crossings q-1 needed:', [(q-1, typ[q-1], hpar[q-1]) for _, _, q in small])
for J, s, q in small: ok('A-small: q<=1 or crossing q-1 even or q<=J-3', q <= J-3 or q <= 1 or not hpar[q-1])
for q in range(2, 6):
    if typ[q-1] == 'a' and hpar[q-1]: ok('A-small: tau(q-1)<2^(q-1)', tau[q-1] < 1 << (q-1))

# ---- Part A: first step b, second step a
old = Counter(); random.seed(1)
def fire_u(J, pick):
    """odd u with s0=(2^J u-4)/3 an even integer"""
    lams = [l for l in range(1, 400, 2) if ((l << J) - 4) % 3 == 0 and (((l << J) - 4)//3) % 2 == 0]
    return lams[0] if pick == 0 else random.choice(lams) + 400*random.getrandbits(30)*6
for J in range(3, NM):
    n = J - 1
    if not (typ[n] == 'b' and hpar[n]): continue
    for pick in range(4):
        u = fire_u(J, pick)
        if pick and ((u << J) - 4) % 3: continue
        s0 = ((u << J) - 4)//3
        if s0 % 2: continue
        tr = run(3*s0 + 5, 3*s0 + 4, NM)
        K = tau[n] // 2
        Th1, x1, q, t1 = tr[1]
        ok('A1 x1=3*2^(J-2)u+6K+4', x1 == 3*(u << (J-2)) + 6*K + 4)
        ok('A1 Theta1-x1=2^(J-2)u', Th1 - x1 == u << (J-2))
        ok('A1 q=v2(6K+4)<=J-3', q == v2(6*K+4) and (J < 12 or q <= J-3))
        if t1 != 'a': continue
        k = tau[q-1] // 2
        Th2, x2, j2, t2 = tr[2]
        ok('A2 x2=13*2^(J-3)u+9K+6+6k', x2 == 13*(u << (J-3)) + 9*K + 6 + 6*k)
        ok('A2 j2=1+v2(k)<=q-2', j2 == 1 + v2(k) and j2 <= q-2)
        ok('A2 whole tail strictly descends', all(tr[i+1][2] < tr[i][2] for i in range(len(tr)-1)))
        if pick == 0 and J >= 12:   # the population of NOTES s6 (smallest lambda, J in [12,20000))
            Jpp = v2(3*tau[q-1] + 4)
            old['cases'] += 1
            if Jpp != q-1 and j2 != min(Jpp, q-1): old['old a->a formula fails'] += 1
            if j2 != 1 + v2(k): old['new formula fails'] += 1
print('NOTES s6 reconciliation:', dict(old))

# ---- Parts B/C: classify every a-return that follows a b/c return, over hypothetical fires
cls = Counter(); rises = []
def shadow_tail(n):
    """reference tail: W's chain at step tau(n), Theta=3tau+5, x=lamX"""
    return [r[2] for r in run(3*tau[n] + 5, X[n][1], NM)]
LIM = min(NM, int(sys.argv[2]) if len(sys.argv) > 2 else 3000)
for J in range(3, LIM):
    if not hpar[J-1]: continue
    for trial in range(3):
        while True:
            u = random.getrandbits(48) | 1
            if ((u << J) - 4) % 3 == 0 and (((u << J) - 4)//3) % 2 == 0: break
        s0 = ((u << J) - 4)//3
        tr = run(3*s0 + 5, 3*s0 + 4, LIM)
        js = [r[2] for r in tr]
        if tr[-1][3] == '?': cls['no data'] += 1; continue
        if any(js[i+1] >= js[i] for i in range(len(js)-1)): rises.append((J, js, ''.join(r[3] for r in tr)))
        for i in range(1, len(tr)):
            Th, x, j, t = tr[i - 1]
            if t not in 'bc': continue
            n = j - 1; sig0 = v2(X[n][0])
            D = Th - (3*tau[n] + 5)
            if i == 1: kind = 'first-step-' + t
            elif v2(Th - 2) >= j: kind = 'theta=2 exact copy (' + t + ')'
            elif v2(Th - 2) >= sig0 - 2: kind = 'SHADOW copy (' + t + ')'
            else: kind = 'other offset (' + t + ')'
            if kind.startswith('theta') or kind.startswith('SHADOW'):
                ok('B copy: outer tail = source tail', js[i:] == shadow_tail(n))
            nxt = tr[i][3]
            cls[(kind, 'next=' + nxt)] += 1
print('b/c-return classes (kind, type of following return):')
for k_, v in sorted(cls.items(), key=str): print('  ', k_, v)
print('epochs with a non-descent:', len(rises), rises[:5])
print('\nSUMMARY'); [print('  ', k_, v) for k_, v in sorted(R.items())]
print('ALL OK' if not any('FAIL' in k_ for k_ in R) else 'FAILURES')

# ---- Part C: offset classification at every b/c copy, and the small-offset copy lemma
print('\nPart C: offsets delta = (Theta_parent - 2) mod 2^j_parent (signed), per pattern')
offs = Counter(); lemma = Counter()
for J in range(3, LIM):
    if not hpar[J-1]: continue
    while True:
        u = random.getrandbits(48) | 1
        if ((u << J) - 4) % 3 == 0 and (((u << J) - 4)//3) % 2 == 0: break
    s0 = ((u << J) - 4)//3
    tr = run(3*s0 + 5, 3*s0 + 4, LIM)
    if tr[-1][3] == '?': continue
    js = [r[2] for r in tr]; ty = ''.join(r[3] for r in tr)
    for i in range(1, len(tr)):
        Th, x, jp, t = tr[i-1]
        if t not in 'bc': continue
        n = jp - 1; M = 1 << jp
        d = (Th - 2) % M; d = d - M if d > M//2 else d
        offs[(ty[:i], d)] += 1
        ref = run(3*tau[n] + 5, X[n][1], LIM); rj = [r[2] for r in ref]
        if d == 0: lemma['delta=0: tail equal' + (' ok' if js[i:] == rj else ' FAIL')] += 1; continue
        ta = next((q for q, r in enumerate(ref) if r[3] == 'a'), None)
        pre_ok = js[i:i + (ta + 1 if ta is not None else len(rj))] == rj[:(ta + 1 if ta is not None else len(rj))]
        if ta is None: lemma['no ref a-return: tail equal' + (' ok' if js[i:] == rj else ' FAIL')] += 1; continue
        r = rj[ta + 1]; h = v2(2*abs(d))
        if not pre_ok: lemma['b/c prefix copied FAIL'] += 1; continue
        if r != h: lemma['first ref a-return: outer j=min(r,v2(2delta))' + (' ok' if js[i+ta+1] == min(r, h) else ' FAIL')] += 1
        else: lemma[('collision r=v2(2delta)', d, 'outer j', js[i+ta+1], 'parent j', jp)] += 1
for k_, v in sorted(offs.items(), key=str): print('  ', k_, v)
for k_, v in sorted(lemma.items(), key=str): print('  ', k_, v)
print('Part C ALL OK' if not any('FAIL' in str(k_) for k_ in lemma) else 'Part C FAILURES')
