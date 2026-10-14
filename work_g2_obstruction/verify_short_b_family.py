"""Canonical last-parent phase after m-1 pure b copies, 1<=m<=123.
Synthetic full pair seeds; the family is conditional on actual ancestry when used in F.
"""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
X=vm.Xdata(128,SMALL=128)
tau={n:(A[1]+(Y[1] if Y else 0)-1)//3 for n,(_,A,Y,_) in X.items()}
rows=[]
for m in range(1,124):
    z=1000
    while z%3!=(2*m)%3:z+=1
    u=z+1 if z%2==0 else z+2
    T=(z<<65)+2-m;s=(T-5)//3;s0=s
    A=(1<<66,((2*z-u)<<65)-2*m-1)
    P=[(1<<66,((u-z)<<65)+m-1)]
    i=67;next_top=0;js=[]
    while P:
        assert sum(c for c,l in [A]+P)==1<<i
        assert sum(l for c,l in [A]+P)==3*s+1
        ent=P[:2];ni=i
        while len(ent)<2:ent.append((1<<ni,0));ni+=1
        b,c=ent;tail=P[2:]
        if sum(A)%2:
            cx,lx=A[0]+2*b[0],A[1]+2*b[1]+3;j=vm.v2(lx)
            assert j<vm.v2(cx)
            if s-s0==next_top:
                js.append(j);next_top=s-s0+1+tau[j-1]
            base=(cx>>j,lx>>j);D=(c[0]+A[0]//2,c[1]+(A[1]+1)//2)
            A=(base[0],base[1]+1)
            P=[(base[0]<<t,base[1]<<t) for t in range(j-1)]+[D]+tail
        else:A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3);P=tail
        i=ni;s+=1
        assert s-s0<=61
    q=1+vm.v2(124-m)
    assert js[:3]==[65,5,q]
    assert js[3:]==([1] if q in (5,6) else [])
    rows.append(dict(b_depth=m,parameters=js,steps=s-s0,strict_G2_failure=q>=5))
result=dict(result='PASS',b_depth_range=[1,123],cases=len(rows),max_steps=max(r['steps'] for r in rows),
            non_descent_depths=[r['b_depth'] for r in rows if r['strict_G2_failure']],rows=rows)
Path(__file__).with_name('short_b_family_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
