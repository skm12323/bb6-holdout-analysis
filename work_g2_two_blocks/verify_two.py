"""Two-block elimination identities, with separate analytic bound checks.
Source arrays in the identity test are formal, not actual orbit records.
"""
from fractions import Fraction as F
from pathlib import Path
import json
def source(m,scale):
    p=[5]+[62+3*i for i in range(1,m+1)]
    a=[(1<<p[i])*(2*scale+1) for i in range(m)]
    return sum(a),sum(F(3,4)**i*a[i] for i in range(m)),F(3,4)**m
count=0
for m in (1,9,25,41):
    for n in (1,9,25,41):
        for scale in (1,3,7):
            A,B,a=source(m,scale);D,E,b=source(n,scale+1)
            for u in (1,5):
                X=F((1<<400)*u);v=F(17)
                H=a*X+B
                Y=(1-a/2)*X+16*v+18+2*A-2*m-B/2
                vn=H/32
                Z=(1-b/2)*Y+16*vn+18+2*D-2*n-E/2
                C=B/2+18+2*D-2*n-E/2
                assert C>0 and C.denominator==1
                assert Z==a*X/2+(1-b/2)*Y+C
                count+=1
bound_checks=0
for q in list(range(65,4097))+[1<<k for k in (16,64,256,1024,10000)]:
    # m<=1+log2(q/65); stronger rounded upper bound used for this check.
    maxm=1+(q//65).bit_length()-1
    assert 2*(2*maxm+1)<=q
    upper=10*q*q+18
    K=(upper-1).bit_length()
    assert upper<=1<<K
    assert 4*q*q>3*((q-2)**2)+4
    bound_checks+=1
result=dict(result='PASS',formal_identity_cases=count,bound_checks=bound_checks,
            scope='Exact algebra and bound constants; no two-block orbit witness')
print(json.dumps(result,indent=2))
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
