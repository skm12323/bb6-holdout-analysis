"""validate_psi.py -- [B] the exact Psi automaton (famlib.make_psi) against brute-force integer chains.
For families Psi(j;P,Q) and many j, draw random odd lambda (1900 bits), put Theta = P + Q 2^j lambda mod 2^2000
(an integer chain of the family), and iterate the exact a-step identities with the real crossing table until
an even return or a b/c return.  Check: same j-sequence as psi; at an emission (ANYJ, depth d, jmin) the
integer chain reaches the tie, its next j' >= jmin and the new chain lies in Psi(j';P',Q')."""
import random
from fractions import Fraction as Fr
import famlib as F
random.seed(7)
Xt, typ, par, chain, real, steps = F.walk()
ext = F.t2.make_ext(Xt, typ, par, real); psi = F.make_psi(Xt, typ, par, real, ext)
run = F.ve.make_run(Xt, typ, par, chain)
B = 2000
fams = [(Fr(5), Fr(1)), (Fr(-1, 3), Fr(1)), (Fr(10, 3), Fr(2, 3)), (Fr(-2), Fr(1)), (Fr(4), Fr(1)), (Fr(7, 3), Fr(2, 3)),
        (Fr(46, 9), Fr(2, 3)), (Fr(-3), Fr(1)), (Fr(6), Fr(1)), (Fr(7, 3), Fr(1)), (Fr(154, 27), Fr(2, 3))]
def rr(P, j): return F.t2.ratrep(P.numerator, P.denominator, j) if P.denominator > 1 else P.numerator
nchk = Counter = 0; stats = dict(END=0, EXT=0, ANYJ=0, tie_entries=0, int_chains=0)
for (P, Q) in fams:
    js = list(range(5, 400)) + random.sample(range(400, 1800), 150)
    for j in js:
        out, f = run(j, rr(P, j) % (1 << j))
        L = psi(j, F.res(P), F.res(Q))
        if f is not None: stats['tie_entries'] += 1
        stats[L['res']] = stats.get(L['res'], 0) + 1
        pj = [a for (a, T, kd, h) in L['path']]
        for it in range(25 if f is not None else 3):
            lam = random.getrandbits(1900) | 1
            Th = (F.res(P, B) + F.res(Q, B) * (lam << j)) % (1 << B)
            jj = j; seq = []; kinds = []
            while True:
                n = jj - 1
                if par[n] == 0: kinds.append('END'); break
                if typ[n] != 'a': kinds.append('BC'); break
                k = Xt[n] // 2
                x = 2 * (Th + 3 * k) - (lam << (jj - 1))
                jn = F.v2(x); lam = x >> jn; Th = Th + 3 + 6 * k; jj = jn; seq.append(jj)
                if L['res'] == 'ANYJ' and len(seq) == len(pj) + 1: kinds.append('AT'); break
            stats['int_chains'] += 1
            if L['res'] == 'END':
                assert kinds == ['END'] and seq == pj, (P, Q, j, seq, pj)
            elif L['res'] == 'EXT':
                assert kinds == ['BC'] and seq == pj[:-1], (P, Q, j, seq, pj)
            else:
                jm, Pn, Qn = L['anyj']
                assert kinds == ['AT'] and seq[:-1] == pj and seq[-1] >= jm, (P, Q, j, seq, pj, jm)
                prec = B - seq[-1] - 8
                assert (Th - Pn - Qn * (lam << seq[-1])) % (1 << prec) == 0
print('validate_psi: all integer chains agree with the Psi automaton;', stats)
