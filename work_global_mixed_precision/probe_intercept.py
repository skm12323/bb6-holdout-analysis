"""Explore the first-rescue intercept family without discarding its variable.
This is a probe, not a proof of closure of the unresolved cylinders.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
table=vm.Xdata(256,SMALL=256)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
def val(n):return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9
def follow(r,L):
    x=(64+288*r,288*(1<<L));T=(46+192*r,192*(1<<L));path=[];loss=cost=0
    for _ in range(60):
        j=val(x[0])
        if j>=val(x[1]):return dict(r=r,L=L,status='collision',path=path)
        if j-1 not in table:return dict(r=r,L=L,status='table',path=path,j=j)
        kind,H,Y,e=table[j-1];path.append(j);cost+=1+tau[j-1]
        if sum(H)%2==0:return dict(r=r,L=L,status='closed',path=path,cost=cost+1,loss=loss)
        if kind=='a':xn=(2*T[0]-x[0]//2+3*tau[j-1],2*T[1]-x[1]//2)
        else:
            assert all(v%(1<<j)==0 for v in x)
            c=H[0]+2*Y[0];b=H[1]+2*Y[1]+3
            xn=(c*(x[0]>>j)+b,c*(x[1]>>j))
        T=(T[0]+3*tau[j-1]+3,T[1]);x=xn;loss+=1+e
    return dict(r=r,L=L,status='budget',path=path)
if __name__=='__main__':
    limit=int(sys.argv[1]) if len(sys.argv)>1 else 20
    todo=[(0,0)];closed=[];unresolved=[]
    while todo:
        r,L=todo.pop();res=follow(r,L)
        if res['status']=='closed':closed.append(res)
        elif L<limit:todo.extend([(r,L+1),(r+(1<<L),L+1)])
        else:unresolved.append(res)
    assert sum(1<<(limit-r['L']) for r in closed)+len(unresolved)==1<<limit
    summary=dict(limit=limit,closed=len(closed),unresolved=unresolved,
                 max_chains=max(len(r['path']) for r in closed),
                 max_loss=max(r['loss'] for r in closed),max_steps=max(r['cost'] for r in closed))
    print(json.dumps(summary,indent=2))
    Path(__file__).with_name(f'intercept_{limit}.json').write_text(json.dumps(dict(summary=summary,closed=closed),indent=2)+'\n')
