"""Retained-root affine checks for all return types and seven root phases."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
N=8192;table=vm.Xdata(N,SMALL=N)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
def val(n):return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9
def K(P):return (12*P*P-1).bit_length()
summary={};witnesses={};checks=0;max_returns=0
for P in range(1024,N):
    cutoff=K(P);budget=1+P//(16*cutoff)
    for delta in range(-2,5):
        a=1;b=0;G=c=elapsed=0;d=delta;j=P;path=[]
        for t in range(budget+1):
            assert a%2 and b%4==0 and 2*G<P
            assert P+1-G>j
            if t:
                assert 0<c<=2*d+2 and c<12*P*P
                assert val(c)==j<cutoff and j<P-G
            typ,H,Y,e=table[j-1];path.append(j)
            if sum(H)%2==0:status='closed';break
            if t==budget:status='budget';break
            time=tau[j-1]
            if typ=='a':
                assert c%2==0
                a,b,c=-a,(1<<(G+2))-b,2*d-c//2+3*time
                G+=1
            else:
                cx=H[0]+2*Y[0];lx=H[1]+2*Y[1]+3
                loss=1+e;num=cx>>(j-loss)
                assert num%2 and cx==num*(1<<(j-loss))
                assert c%(1<<j)==0 and lx<=6*time+4
                a,b,c=num*a,num*b,cx*(c>>j)+lx
                G+=loss
            d+=3*time+3;elapsed+=time+1
            assert 16*elapsed<=17*P*P
            assert 16*(G-1)<=5*P
            j=val(c);checks+=1
        key=f'{delta}_{status}';summary[key]=summary.get(key,0)+1
        max_returns=max(max_returns,len(path)-1)
        if delta not in witnesses or len(path)>len(witnesses[delta]['path']):
            witnesses[delta]=dict(P=P,delta=delta,path=path,G=G,elapsed=elapsed,status=status)
result=dict(result='PASS',parent_range=[1024,N-1],root_phases=list(range(-2,5)),
            families=(N-1024)*7,transition_checks=checks,outcomes=summary,
            max_observed_returns=max_returns,longest_by_phase=list(witnesses.values()),
            scope='Uniform affine root families; finite closure evidence does not prove the all-P stopping criterion')
print(json.dumps(result,indent=2))
Path(__file__).with_name('mixed_root_checks.json').write_text(json.dumps(result,indent=2)+'\n')
