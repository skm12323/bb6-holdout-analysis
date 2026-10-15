"""Uniform E-family odd-a suffix certificates, retaining signed affine slopes."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
table=vm.Xdata(128,SMALL=128)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
def val(z):return (abs(z)&-abs(z)).bit_length()-1 if z else 10**9
def follow(r,L):
    # E: x=2^18 U, Theta=x-2^15 V-18; U positive, V positive odd.
    x=(3*(1<<17)-(1<<16)+6*r-36,3*(1<<17),-(1<<17),6*(1<<L))
    T=((1<<18)-(1<<15)-15+6*r,1<<18,-(1<<16),6*(1<<L))
    sigma=18;path=[];states=[];cost=0;minimum=18
    for _ in range(40):
        j=val(x[0])
        if j>=min(map(val,x[1:])):return dict(r=r,L=L,status='collision',path=path,x=x,Theta=T)
        if j>=sigma:return dict(r=r,L=L,status='margin',path=path)
        if j-1 not in table:return dict(r=r,L=L,status='table',path=path,j=j)
        kind,H,Y,e=table[j-1];path.append(j);minimum=min(minimum,sigma-j)
        states.append(dict(x=x,Theta=T,j=j,sigma=sigma));cost+=1+tau[j-1]
        if sum(H)%2==0:return dict(r=r,L=L,status='closed',path=path,cost=cost+1,min_margin=minimum,states=states)
        if kind=='a':
            assert all(z%2==0 for z in x)
            xn=tuple(2*T[i]-x[i]//2+(3*tau[j-1] if i==0 else 0) for i in range(4))
        else:
            assert all(z%(1<<j)==0 for z in x)
            c=H[0]+2*Y[0];b=H[1]+2*Y[1]+3
            xn=tuple(c*(x[i]>>j)+(b if i==0 else 0) for i in range(4))
        T=(T[0]+3*tau[j-1]+3,*T[1:]);sigma-=1+e;x=xn
    return dict(r=r,L=L,status='budget',path=path)
if __name__=='__main__':
    todo=[(0,0)];closed=[];open_rows=[]
    while todo:
        r,L=todo.pop();row=follow(r,L)
        if row['status']=='closed':closed.append(row)
        elif L<16:todo.extend([(r,L+1),(r+(1<<L),L+1)])
        else:open_rows.append(row)
    assert sum(1<<(16-r['L']) for r in closed)+len(open_rows)==1<<16
    summary=dict(result='PASS',closed_cylinders=len(closed),open_rows=open_rows,
                 max_suffix_steps=max(r['cost'] for r in closed),
                 max_suffix_chains=max(len(r['path']) for r in closed),
                 min_margin=min(r['min_margin'] for r in closed))
    print(json.dumps(summary,indent=2))
    Path(__file__).with_name('e_certificate.json').write_text(json.dumps(dict(summary=summary,closed=closed),indent=2)+'\n')
