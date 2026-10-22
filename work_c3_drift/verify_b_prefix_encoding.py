"""Universal bounded-height phase encoding and B^t AA budget controls."""
from pathlib import Path
from fractions import Fraction as F
import json
from verify_shift_transport import Calendar,val
from verify_height_budget import height
from verify_copy_budget import rank

def encode(phi,m):
    Q=3**m;mod=1<<m
    C=Q+(phi*Q-Q)%mod
    c=F(C,Q)
    residue=c.numerator*pow(c.denominator,-1,2*mod)%(2*mod)
    diff=(phi-residue)%(2*mod)
    assert diff in (0,mod)
    assert 1<=c<=2 and height(c)==0 and rank(c.denominator)<=m
    return c,diff//mod

def main():
    encodings=0
    for m in range(1,13):
        for phi in range(1<<(m+1)):
            c,b=encode(phi,m)
            assert val(F(phi)-c-b*(1<<m))>=m+1
            encodings+=1
    cal=Calendar(256);cases=[]
    for p in (17,54,90,125,161):
        row=cal.crossing(p-1);assert row['kind']=='a' and row['odd']
        k=row['time']//2
        for t in sorted(set(list(range(3,100))+[9*k+13])):
            if val(6*k+2-2*t)!=5:continue
            # Algebraic source lifts obey the valuation hierarchy and clock
            # size bound. They are not claimed to be canonical B ancestries.
            lambdas=[(1<<(p+3*i))*(1 if i%2==0 else 3) for i in range(t)]
            P=max(512,p+3*t,1<<((p+3*t)//2+2))
            assert all(L<=3*(P-1)**2+4 for L in lambdas)
            beta1=sum((2-F(3,4)**i/2)*L for i,L in enumerate(lambdas))+6*k+2-2*t
            beta2=sum((1+F(3,4)**i/4)*L for i,L in enumerate(lambdas))+9*k+13-t
            theta2=sum(lambdas)+6*k+13-t
            assert beta1.denominator==beta2.denominator==1 and val(beta1)==5
            assert 0<beta2<2*P**3
            m=val(beta2);G=2*t+2
            assert G+3*m<P
            phi=int(theta2-beta2);c,b=encode(phi,m)
            assert G+m+2*rank(c.denominator)+height(c)<P
            cases.append(dict(p=p,t=t,m=m,root_bits=P.bit_length(),
                              resonance=(9*k+13-t==0),encoded_rank=rank(c.denominator)))
    # Dyadic proof boundary: for P in [2^e,2^(e+1)), 3m+2 <=9e+14.
    assert all(3*(9*e+14)<1<<e for e in range(9,4097))
    out=dict(status='PASS',review_status='unreviewed',phase_class_encodings=encodings,
             algebra_prefix_cases=len(cases),resonant_cases=sum(c['resonance'] for c in cases),
             cases=cases,
             scope='Exhaustive small phase encodings plus algebraic source lifts. Canonical ancestry of the lifts is not asserted; the reached-prefix theorem is analytic.')
    Path(__file__).with_name('b_prefix_encoding_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}))

if __name__=='__main__':main()
