"""Shared-clock identities and finite rescue of the new phase -2 family."""
from fractions import Fraction as F
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
table=vm.Xdata(1024,SMALL=1024)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
def val(z):return (abs(z)&-abs(z)).bit_length()-1 if z else 10**9
ids=0
for a in range(8):
    for b in range(8):
        k=32761+65536*a;l=54614+65536*b
        x=F(1<<120);v=F(12345)
        T=x/2+(1<<15)*v+21
        y=2*T-x/2+6*k;T1=T+3+6*k
        z=2*T1-y/2+6*l;T2=T1+3+6*l
        out=2*T2-z/2+6;Tout=T2+9
        assert out==x/4+3*y/4+3*(k+3*l+5)
        assert Tout==x/4+y/2+3*k+6*l+15
        assert Tout.denominator==1 and int(Tout)%65536==32766
        ids+=1
records=[]
for r in range(16,1024):
    x=(1<<r,1<<(r+1),0);T=(32766,0,65536)
    sigma=max(r+1,18);path=[];states=[];cost=0;margin=sigma-r
    for _ in range(40):
        j=val(x[0])
        assert j<min(map(val,x[1:])) and j<sigma
        typ,H,Y,e=table[j-1];path.append(j)
        states.append(dict(j=j,x=x,Theta=T,sigma=sigma))
        margin=min(margin,sigma-j);cost+=1+tau[j-1]
        if sum(H)%2==0:
            records.append(dict(r=r,path=path,cost=cost+1,margin=margin,states=states));break
        if typ=='a':
            xn=tuple(2*T[i]-x[i]//2+(3*tau[j-1] if i==0 else 0) for i in range(3))
        else:
            assert all(z%(1<<j)==0 for z in x)
            c=H[0]+2*Y[0];b=H[1]+2*Y[1]+3
            xn=tuple(c*(x[i]>>j)+(b if i==0 else 0) for i in range(3))
        T=(T[0]+3*tau[j-1]+3,T[1],T[2]);sigma-=1+e;x=xn
    else:raise AssertionError('unclosed')
summary=dict(result='PASS',shared_clock_identities=ids,symbolic_families=len(records),
             max_tail_steps=max(r['cost'] for r in records),
             max_chains=max(len(r['path']) for r in records),
             minimum_margin=min(r['margin'] for r in records),
             parameter17=next({k:v for k,v in r.items() if k!='states'} for r in records if r['r']==17))
print(json.dumps(summary,indent=2))
Path(__file__).with_name('shared_clock_certificate.json').write_text(json.dumps(dict(summary=summary,records=records),indent=2)+'\n')
