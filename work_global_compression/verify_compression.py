"""Exact affine source-clock elimination; full pair checks on synthetic epochs.
Uses only stdlib; reads existing work_m implementation to obtain crossing data.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm

N=4096
X=vm.Xdata(N,SMALL=N)
tau={n:(A[1]+(Y[1] if Y else 0)-1)//3 for n,(_,A,Y,_) in X.items()}
def v2(x):
    return (abs(x)&-abs(x)).bit_length()-1 if x else 10**9

def first_a(J):
    j=J; A=1; B=-1; G=d=0; path=[]
    while True:
        kind,H,Y,eps=X[j-1]
        if sum(H)%2==0:
            return None
        path.append((j,kind))
        t=tau[j-1]
        if kind=='a':
            A,B,G=(1<<(G+2))-A,-B+(2*d+3*t)*(1<<(G+1)),G+1
            d+=3*t+3
            assert A%2 and F(3,2)<=F(A,1<<G)<2
            assert abs(F(B,1<<G))<=3*d+1
            assert G<=J-4 and d<=6*J**3
            return dict(J=J,A=A,B=B,G=G,d=d,path=path)
        gain=1+eps
        cx=H[0]+2*Y[0]; lx=H[1]+2*Y[1]+3
        a=cx>>(j-gain)
        assert a%2 and F(1,2)<=F(a,1<<gain)<1
        A,B=A*a,B*a+(lx<<(G+gain))
        G+=gain; d+=3*t+3
        assert A%2 and 0<F(A,1<<G)<=1
        assert abs(F(B,1<<G))<=2*d+1
        j=v2(lx)

def raw_until_a(J,V,C=10):
    rho=J+C
    Theta0=(V<<J)+1
    assert (Theta0-5)%3==0
    s=(Theta0-5)//3; s0=s
    H=(1<<rho,Theta0-4); P=[]; i=rho
    top_at=0; prev_kind=None; events=[]
    while True:
        assert sum(c for c,l in [H]+P)==1<<i
        assert sum(l for c,l in [H]+P)==3*s+1
        entries=P[:2]; ni=i
        while len(entries)<2:
            entries.append((1<<ni,0)); ni+=1
        b,c=entries; tail=P[2:]
        if sum(H)%2:
            cx,lx=H[0]+2*b[0],H[1]+2*b[1]+3
            j=v2(lx)
            assert j<v2(cx) and H[0]%2==0
            if s-s0==top_at:
                events.append(dict(j=j,x=lx,Theta=3*s+5,cx=cx,sigma=v2(cx)))
                if prev_kind=='a':
                    return Theta0,events
                prev_kind=X[j-1][0]
                top_at=s-s0+1+tau[j-1]
            u=(cx>>j,lx>>j)
            D=(c[0]+H[0]//2,c[1]+(H[1]+1)//2)
            H=(u[0],u[1]+1)
            P=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[D]+tail
        else:
            H=(H[0]+b[0]+c[0],H[1]+b[1]+c[1]+3)
            P=tail
        i=ni;s+=1
        if not P:
            return Theta0,None
        assert s-s0<50000

def compress(rec,delta):
    A,B,G,d=(rec[k] for k in ('A','B','G','d'))
    return (F(A*d-B)+(A-(1<<(G+1)))*delta)/A

records=[]; denominators=Counter(); Gmax=0
for J in range(2,N):
    r=first_a(J)
    if r:
        records.append(r); Gmax=max(Gmax,r['G'])
        z=compress(r,F(-1))
        assert abs(z)<=3*r['d']+1+F(1,3)
        denominators[z.denominator]+=1

# The complete small b/c prefix certificate used in the analytic G bound.
base_max=0; base_witness=None
for J in range(1,1024):
    j=J; G=0; path=[j]
    while True:
        kind,H,Y,eps=X[j-1]
        if sum(H)%2==0 or kind=='a':break
        G+=1+eps;j=v2(H[1]+2*Y[1]+3);path.append(j)
    if G>base_max:base_max=G;base_witness=[J,path]
assert base_max==4

checked=shift_checks=skipped=joint_steps=copy_checks=0; examples=[]
selected=set(range(2,129))|{129,257,513,1024,2048,4095}
for J in sorted(selected):
    r=first_a(J)
    for offset in (0,6):
        V=(1 if J%2==0 else 5)+offset
        Theta0,events=raw_until_a(J,V)
        assert (events is None)==(r is None)
        if events is None:continue
        A,B,G,d=(r[k] for k in ('A','B','G','d'))
        target=events[-1]; before=events[-2]
        assert target['x']==F(A*Theta0+B,1<<G)
        assert target['Theta']==Theta0+d
        a0,g0,c0=1,0,1
        for t,ev in enumerate(events):
            assert a0*ev['Theta']-(ev['x']<<g0)==c0
            for p in (1,3,19):
                for delta in (-1,0,2):
                    xo=ev['x']+ev['cx']*p
                    to=ev['Theta']+delta
                    L=g0+ev['sigma']
                    assert (a0*to-(xo<<g0)-(c0+a0*delta))%(1<<L)==0
                    copy_checks+=1
            if t==len(events)-1:break
            j=ev['j'];kind,H,Y,eps=X[j-1];tt=tau[j-1]
            if kind=='a':
                an=(1<<(g0+2))-a0
                cn=-c0+an*(3+3*tt)-3*tt*(1<<(g0+1))
                a0,g0,c0=an,g0+1,cn
            else:
                e=1+eps;f=(H[0]+2*Y[0])>>(j-e)
                cn=f*c0+f*a0*(3*tt+3)-(H[1]+2*Y[1]+3)*(1<<(g0+e))
                a0,g0,c0=f*a0,g0+e,cn
            joint_steps+=1
        assert (a0,g0)==(A,G) and c0==A*d-B
        checked+=1
        for delta in list(map(F,[-2,-1,0,1,2,10]))+[F(10,3),F(46,9),F(232,13)]:
            # Use actual integer D congruent to delta to high precision.
            M=before['sigma']+8
            D=(delta.numerator*pow(delta.denominator,-1,1<<M))%(1<<M)+(1<<M)
            outer_x=target['x']+2*D-before['cx']//2
            q=v2(outer_x)
            if q>=before['sigma']-1:
                skipped+=1
                continue # theorem explicitly requires separation
            theta=compress(r,delta)
            diff=F(target['Theta']+D)-theta
            assert v2(diff.numerator)>=q  # denominator is odd
            assert theta.denominator%2==1
            shift_checks+=1
        if J in (5,65):
            examples.append(dict(J=J,V=V,coefficients=r,compressed=str(compress(r,F(-1)))))

# Rational rescue representatives stay real-bounded but can have deep 2-adic resonance.
resonances=[]
for d in range(1,13):
    m=(1<<d)-2
    Q=3**m
    theta=F(6*Q-8,Q)
    B=theta+66
    assert v2(B.numerator)==d+5
    residues=set()
    for u in (1,3,5,7):
        T=(6-8*pow(3,-m,1<<17))%(1<<17)
        Theta=T+(u+1)*(1<<17)
        x1=2*Theta+36-(u<<16)
        assert v2(x1)==5
        x2=Theta+66+(u<<15)
        q=v2(x2);residues.add(q)
        if d<10:assert q==d+5
        elif d>10:assert q==15
        else:assert q>=16
    resonances.append(dict(m=m,nominal_valuation=d+5,actual_j_samples=sorted(residues)))

result=dict(result='PASS',abstract_J_range=[2,N-1],first_a_records=len(records),
            max_G=Gmax,denominators_for_delta_minus_one=dict(denominators),
            base_bc_G_max=base_max,base_witness=base_witness,
            raw_synthetic_epoch_checks=checked,compression_congruence_checks=shift_checks,
            outside_separation_hypothesis=skipped,
            joint_relation_step_checks=joint_steps,joint_copy_checks=copy_checks,
            examples=examples,rational_resonances=resonances)
Path(__file__).with_name('compression_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='examples'},indent=2))
