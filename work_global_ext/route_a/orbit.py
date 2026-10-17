"""orbit.py -- [B] the 3-adic macro orbit (REPORT.md section 4).
c_0 = 5, c_{m+1} = 3 - (15 - c_m)/3 = (c_m - 6)/3, i.e. c_m = -3 + 8*3^(-m);  P_m = (15 - c_m)/3 = 6 - 8*3^(-m-1).
Checks: (i) v2(c_m + 3) = 3 (so Psi(5;c_m,1) ties at X(4)); (ii) the exact Psi automaton on the real crossing
table emits Psi(.;P_m,2/3) from Psi(5;c_m,1) for m < 12; (iii) residues c_m mod 2^B are pairwise distinct for
m < 2^(B-5)  (B = 6..16)."""
from fractions import Fraction as Fr
import famlib as F
Xt, typ, par, chain, real, steps = F.walk()
ext = F.t2.make_ext(Xt, typ, par, real); psi = F.make_psi(Xt, typ, par, real, ext)
c = Fr(5); ok = True
for m in range(12):
    assert c == -3 + Fr(8, 3**m) and F.v2(F.res(c + 3)) == 3
    L = psi(5, F.res(c), 1)
    Pm = (15 - c) / 3
    assert L['res'] == 'ANYJ' and L['anyj'][1] == F.res(Pm) and L['anyj'][2] == F.res(Fr(2, 3)) and L['anyj'][0] == 5
    print('m=%2d  c_m=%-22s c_m mod 32=%2d   emits P_m=%s' % (m, c, F.res(c, 5), Pm))
    c = 3 - Pm
for B in range(6, 17):
    vals = {F.res(-3 + Fr(8, 3**m), B) for m in range(2**(B - 5))}
    assert len(vals) == 2**(B - 5)
print('distinct residues: c_m mod 2^B pairwise distinct for m < 2^(B-5), 6 <= B <= 16')
