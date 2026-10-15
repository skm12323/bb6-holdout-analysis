"""Uniform R21 closure for every entry parameter 17..1023."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
table=vm.Xdata(1024,SMALL=1024)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
def val(z):return (abs(z)&-abs(z)).bit_length()-1 if z else 10**9
records=[]
for q in range(17,1024):
    x=(1<<q,1<<(q+1),0)
    T=((1<<(q-1))+(1<<15)+21,1<<q,1<<16)
    sigma=q+1;path=[];states=[];cost=0;margin=1
    for _ in range(40):
        j=val(x[0])
        assert j<min(map(val,x[1:])) and j<sigma
        typ,H,Y,e=table[j-1];path.append(j)
        states.append(dict(j=j,x=x,Theta=T,sigma=sigma))
        margin=min(margin,sigma-j);cost+=1+tau[j-1]
        if sum(H)%2==0:
            records.append(dict(q=q,path=path,cost=cost+1,margin=margin,states=states));break
        if typ=='a':xn=tuple(2*T[i]-x[i]//2+(3*tau[j-1] if i==0 else 0) for i in range(3))
        else:
            assert all(z%(1<<j)==0 for z in x)
            c=H[0]+2*Y[0];b=H[1]+2*Y[1]+3
            xn=tuple(c*(x[i]>>j)+(b if i==0 else 0) for i in range(3))
        T=(T[0]+3*tau[j-1]+3,T[1],T[2]);sigma-=1+e;x=xn
    else:raise AssertionError('unclosed')
summary=dict(result='PASS',symbolic_families=len(records),
             max_tail_steps=max(r['cost'] for r in records),
             max_chains=max(len(r['path']) for r in records),
             minimum_margin=min(r['margin'] for r in records))
print(json.dumps(summary,indent=2))
Path(__file__).with_name('small_r_certificate.json').write_text(json.dumps(dict(summary=summary,records=records),indent=2)+'\n')
