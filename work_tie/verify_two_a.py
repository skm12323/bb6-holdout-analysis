"""Additional exact checks of the general AA identity, not a global certificate."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'work_el'))
import verify_el as ve

Xt, typ, par, chains, _, _ = ve.real_walk(600)
checks = 0
second_non_descents = 0
for j in range(12, 501):
    n = j-1
    if typ[n] != 'a' or not par[n]:
        continue
    k = Xt[n]//2
    for theta in range(-10, 11):
        residue = (theta+3*k+(1 << (j-2))) % (1 << (j-1))
        assert residue
        q = 1+ve.v2(residue)
        assert q < j
        if typ[q-1] != 'a' or not par[q-1]:
            continue
        l = Xt[q-1]//2
        B = theta+6+9*k+6*l
        assert 11 <= B and 2*B <= 32+15*(j-1)**2 < 1 << (j-1)
        for z in (1, 3, (1 << 80)+1):
            for u in (1,3):
                Theta = theta+(z << j)
                x1 = 2*Theta+6*k-(u << (j-1))
                assert x1 > 0 and ve.v2(x1) == q
                u1 = x1 >> q
                Theta1 = Theta+3+6*k
                x2 = 2*Theta1+6*l-(u1 << (q-1))
                assert x2 == Theta+6+9*k+6*l+(u << (j-2))
                j2 = ve.v2(x2)
                assert j2 == ve.v2(B) and j2 <= j-3
                # Initial minimal safe sigma=j+1.
                assert q < j and j2 < j-1
                checks += 1
                second_non_descents += j2 >= q
print('Exact two-a checks:', checks)
print('Cases with second-transition non-descent:', second_non_descents)
print('All combined descents and minimal-sigma margins passed.')
