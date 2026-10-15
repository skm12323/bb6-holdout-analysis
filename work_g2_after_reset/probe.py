"""Exact affine exploration of reset families; failures are reported, not pruned."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
N=4096
X=vm.Xdata(N,SMALL=N)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in X.items()}
def val(n):return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9
def follow(q):
    x=(1<<q,1<<(q+1),0)
    T=((1<<(q-1))+46+3*(1<<61),1<<q,3*(1<<62))
    j=q;loss=0;path=[]
    for _ in range(100):
        if j-1 not in X:return dict(q=q,status='table',path=path,j=j)
        kind,H,Y,eps=X[j-1];path.append(j)
        if sum(H)%2==0:return dict(q=q,status='closed',path=path,loss=loss,margin=q+2-loss-j)
        if kind=='a':
            xn=tuple(2*T[i]-x[i]//2+(3*tau[j-1] if i==0 else 0) for i in range(3))
        else:
            cx=H[0]+2*Y[0];lx=H[1]+2*Y[1]+3
            assert all(v%(1<<j)==0 for v in x)
            xn=tuple(cx*(x[i]>>j)+(lx if i==0 else 0) for i in range(3))
        T=(T[0]+3*tau[j-1]+3,T[1],T[2]);loss+=1+eps
        jn=val(xn[0])
        if jn>=min(val(xn[1]),val(xn[2])):
            return dict(q=q,status='collision',path=path,loss=loss,valuations=list(map(val,xn)))
        if jn>=q+2-loss:return dict(q=q,status='margin',path=path,j=jn,loss=loss)
        j,x=jn,xn
    return dict(q=q,status='budget',path=path)
if __name__=='__main__':
    records=[follow(q) for q in range(63,N)]
    summary={s:sum(r['status']==s for r in records) for s in sorted(set(r['status'] for r in records))}
    print(summary)
    print([r for r in records if r['status']!='closed'][:30])
    print('longest',max(records,key=lambda r:len(r['path'])))
    Path(__file__).with_name('probe.json').write_text(json.dumps(records,indent=2)+'\n')
