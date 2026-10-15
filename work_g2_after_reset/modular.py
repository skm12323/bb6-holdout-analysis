"""Uniform suffix certificates after an odd a-return from any q>=63.
U is arbitrary positive, V positive odd, k=r+2^L*w with w>=0.
Unknown or colliding branches are retained explicitly.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
X=vm.Xdata(128,SMALL=128)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in X.items()}
def val(n):return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9
def follow(r,L):
    x=(4*(1<<62)+92+6*r,1<<62,3*(1<<63),6*(1<<L))
    T=((1<<62)+49+3*(1<<61)+6*r,1<<62,3*(1<<62),6*(1<<L))
    sigma=64;path=[];states=[];cost=0;minimum=64
    for _ in range(40):
        j=val(x[0])
        if j>=min(map(val,x[1:])):return dict(r=r,status='collision',path=path)
        if j>=sigma:return dict(r=r,status='margin',path=path)
        if j-1 not in X:return dict(r=r,status='table',path=path,j=j)
        kind,H,Y,eps=X[j-1];path.append(j);minimum=min(minimum,sigma-j)
        states.append(dict(x=x,Theta=T,sigma=sigma,j=j))
        cost+=1+tau[j-1]
        if sum(H)%2==0:return dict(r=r,status='closed',path=path,suffix_steps=cost+1,min_margin=minimum,states=states)
        if kind=='a':
            assert all(z%2==0 for z in x)
            xn=tuple(2*T[i]-x[i]//2+(3*tau[j-1] if i==0 else 0) for i in range(4))
        else:
            assert all(z%(1<<j)==0 for z in x)
            cx=H[0]+2*Y[0];lx=H[1]+2*Y[1]+3
            xn=tuple(cx*(x[i]>>j)+(lx if i==0 else 0) for i in range(4))
        T=(T[0]+3*tau[j-1]+3,*T[1:]);sigma-=1+eps;x=xn
    return dict(r=r,status='budget',path=path)
if __name__=='__main__':
    L=int(sys.argv[1]) if len(sys.argv)>1 else 10
    records=[follow(r,L) for r in range(1<<L)]
    closed=[r for r in records if r['status']=='closed']
    summary=dict(L=L,closed=len(closed),total=1<<L,
                 exceptions=[{k:v for k,v in r.items() if k!='states'} for r in records if r['status']!='closed'],
                 max_suffix_steps=max(r['suffix_steps'] for r in closed),
                 max_suffix_chains=max(len(r['path']) for r in closed),
                 min_margin=min(r['min_margin'] for r in closed))
    print(json.dumps(summary,indent=2))
    Path(__file__).with_name('modular_certificate.json').write_text(json.dumps(dict(summary=summary,records=records),indent=2)+'\n')
