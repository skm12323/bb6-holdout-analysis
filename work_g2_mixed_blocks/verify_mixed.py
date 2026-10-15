"""Exact mixed-corridor identities and finite checks against real crossing data."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
def corridor(h,seed):
    a=F(1);B=F(0);d=G=0;steps=[]
    for i in range(h):
        e=2+(i+seed)%2;n=(1<<e)-1;r=F(n,1<<e)
        tau=2+(i+seed)%11;lam=6*tau+3
        a=r*a;B=r*B+lam;d+=1+tau;G+=e
        steps.append((r,lam,tau))
    assert 0<a<=1 and 0<=B<=6*d-h
    return a,B,d,G,steps
def direct(x,T,steps,k):
    for r,lam,t in steps:x=r*x+lam;T+=3*t+3
    H=x
    return 2*T-x/2+6*k,T+3+6*k,H
identities=0
for h in range(9):
    for t in range(9):
        for seed in (1,2,5):
            a,B,d,G,st=corridor(h,seed)
            b,E,f,L,uv=corridor(t,seed+1)
            X=F(1<<160);Hprev=F(32*12345);kprev=3
            T=X/2+Hprev/4+3+3*kprev;k1=seed+1;k2=seed+7
            Y,T1,H1=direct(X,T,st,k1)
            Z,T2,H2=direct(Y,T1,uv,k2)
            C=B/2+6+6*k1+6*k2+6*f-E/2
            assert C>0
            assert Z==a*X/2+(1-b/2)*Y+C
            assert T1-Y/2==H1/4+3+3*k1
            identities+=1

N=4096;table=vm.Xdata(N,SMALL=N)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
def val(z):return (abs(z)&-abs(z)).bit_length()-1 if z else 10**9
corridors=0;ends={};max_h=0
for q in range(1024,N):
    j=q;d=G=h=0
    while True:
        typ,H,Y,e=table[j-1]
        if sum(H)%2==0:reason='even';break
        if typ=='a':reason='odd_a';break
        cx=H[0]+2*Y[0];lx=H[1]+2*Y[1]+3
        assert 0<cx<(1<<j) and 0<lx<=6*tau[j-1]+5
        jn=val(lx)
        assert jn<=j-2-e
        if j>=64:assert 2*jn<=j
        d+=1+tau[j-1];G+=1+e;h+=1;j=jn
    assert d<2*q*q and 4*G<=3*q
    corridors+=1;ends[reason]=ends.get(reason,0)+1;max_h=max(max_h,h)
result=dict(result='PASS',formal_mixed_identities=identities,
            actual_table_corridors=corridors,end_types=ends,
            max_observed_bc_steps=max_h,
            scope='Formal two-block identities; real finite corridor bounds, not a global orbit proof')
print(json.dumps(result,indent=2))
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
