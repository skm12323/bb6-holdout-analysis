"""Exact b^m-a block identities and loss of a parameter-only rank.
Synthetic source arrays below are algebra inputs, NOT orbit records.
"""
from pathlib import Path
from fractions import Fraction as F
import json
def val(x):return (abs(x)&-abs(x)).bit_length()-1 if x else 10**9
checks=0
for m in range(1,41):
    p=[5]+[62+3*i for i in range(1,m+1)]
    source=[(1<<p[i])*(5 if p[i]%2 else 1) for i in range(m)]
    A=sum(source);B=sum(F(3,4)**i*source[i] for i in range(m));a=F(3,4)**m
    assert B.denominator==1;B=int(B)
    for u in (1,3,11):
        X=(1<<p[m])*u
        for v in (1,5,101):
            T=F(X,2)+8*v+6;x=F(X);theta=T
            for i in range(m-1,-1,-1):
                x=F(3,4)*x+source[i];theta+=source[i]-1
                assert x.denominator==1 and val(x.numerator)==p[i]
            assert x==a*X+B and theta==T+A-m
            Y=2*theta-x/2+6;Tout=theta+9;H=x
            expected=(1-a/2)*X+16*v+18+2*A-2*m-F(B,2)
            assert Y==expected and Tout-Y/2==H/4+6
            assert Y.denominator==1 and val(H.numerator)==5
            assert (H/32).denominator==1 and (H/32).numerator%2
            assert int(Y)%32==2*(9-m)%32
            if m%16!=9:assert val(int(Y))==1+val(9-m)<=4
            else:assert int(Y)%32==0 and Tout%16==14
            checks+=1

# A fixed formal block can have an arbitrarily large rebound once the
# incoming joint variable v is freed from its actual ancestry constraints.
m=9;p=[5]+[62+3*i for i in range(1,m+1)];q=p[m]
source=[(1<<p[i])*(5 if p[i]%2 else 1) for i in range(m)]
A=sum(source);B=int(sum(F(3,4)**i*source[i] for i in range(m)))
a=F(3,4)**m;D=18+2*A-2*m-F(B,2)
rebounds=[]
for r in (101,201,501):
    target=1<<r
    u=int((target-D)//((1-a/2)*(1<<q)))-2
    if u%2==0:u-=1
    X=(1<<q)*u
    v=(target-(1-a/2)*X-D)/16
    assert v.denominator==1 and v>0 and int(v)%2
    v=int(v);T=X//2+8*v+6
    assert T%3==2
    assert 2*T-X-5>=0 and X-T+1>=0 # compatible pair lambda components
    H=a*X+B;Y=(1-a/2)*X+16*v+D
    assert Y==target and val(Y.numerator)==r
    assert H/32>v # even the last parameter-5 odd base need not decrease
    rebounds.append(dict(input_parameter=q,output_parameter=r,
                         source_count=m,old_base_bits=v.bit_length(),
                         new_base_bits=int(H/32).bit_length()))
result=dict(result='PASS',block_identity_cases=checks,
            formal_rebounds=rebounds,
            caveat='Synthetic algebra sources; not orbit reachability or counterexamples to actual termination')
print(json.dumps(result,indent=2))
Path(__file__).with_name('block_checks.json').write_text(json.dumps(result,indent=2)+'\n')
