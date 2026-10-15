"""Finite checks of ancestry identities and analytic bound constants.
The formal chains below are algebra test inputs, NOT asserted F-orbit records.
Dominance estimates are tested separately as conditional inequalities.
"""
from pathlib import Path
import json

identity_checks=0
for ell in range(1,51):
    p=[5]+[62+3*i for i in range(1,ell+1)]
    U=[5]+[1 if q%2==0 else 5 for q in p[1:]]
    values=[(1<<p[i])*U[i] for i in range(ell)]
    M=4+sum(((1<<(2*i+2))-3**i)*(1<<(p[i]-2*i-2))*U[i] for i in range(ell))
    S=p[ell]-2*ell-1
    for m in (ell,ell+7,(1<<20)+ell):
        # Coefficients of independent symbols Z,v,1.
        T=(1<<p[ell],0,ell+1-m)
        x=(0,1<<p[ell],0)
        for i in range(ell-1,-1,-1):
            assert all(z%4==0 for z in x)
            x=tuple(3*z//4+(values[i] if a==2 else 0) for a,z in enumerate(x))
            T=(T[0],T[1],T[2]+values[i]-1)
        assert all(z%2==0 for z in x)
        xa=tuple(2*T[i]-x[i]//2+(6 if i==2 else 0) for i in range(3))
        expected=(1<<(p[ell]+1),-(3**ell)*(1<<S),2*(M-m))
        assert xa==expected
        identity_checks+=1
    if ell>=2:
        prev=4+sum(((1<<(2*i+2))-3**i)*(1<<(p[i]-2*i-2))*U[i] for i in range(ell-1))
        shift=M-prev
        previous_S=p[ell-1]-2*(ell-1)-1
        assert (shift&-shift).bit_length()-1==previous_S-1

bound_checks=0
for ell in range(1,101):
    for P in (3*ell+62,3*ell+63,6*ell+128):
        S=P-2*ell-1
        upper=4+ell*(3*(P-2)**2+4)
        assert upper<P**3
        assert 2*P**3 < 1<<S
        bound_checks+=1
for P in range(65,4097):
    assert (1<<P)>3*(2*P-2)**2+4

for m in list(range(1,10000))+[1<<61,(1<<61)+124,1<<200]:
    ratio=(m+64)//65
    ell=1+(ratio-1).bit_length()
    assert ell<=m and 65*(1<<(ell-1))>=m

result=dict(result='PASS',formal_identity_checks=identity_checks,
            conditional_bound_checks=bound_checks,doubling_base_checks=[65,4096],
            scope='Formal coefficient identities and bound constants; not deep-orbit simulation')
Path(__file__).with_name('ancestry_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
