"""Fixed bounded rational phase, unbounded two-a parameter jump.
Synthetic mass-compatible states only; no actual-orbit reachability assertion.
"""
import json
from pathlib import Path

def v2(x):
    assert x>0
    return (x&-x).bit_length()-1

M=1022
theta_res=(6-8*pow(3,-M,1<<17))%(1<<17)
assert theta_res==32702
assert (theta_res+66)%(1<<15)==0
u_mod4=(-((theta_res+66)//(1<<15)))%4
assert u_mod4%2==1

def check(q):
    u0=1<<(q-17)
    u=next(u0+r for r in range(12) if (u0+r)%4==u_mod4 and ((1<<q)+u0+r)%3==2)
    assert u==u0+11
    Theta=(1<<q)-66-(u<<15)
    assert Theta%(1<<17)==theta_res and Theta%3==2 and u%2==1
    s=(Theta-5)//3
    sigma=q+3
    i=sigma+1
    A=(1<<sigma,2*Theta-(u<<17)-5)
    P=[(1<<sigma,(u<<17)-Theta+1)]
    assert min(A[1],P[0][1])>0
    top=[]
    for elapsed in range(17):
        assert sum(c for c,l in [A]+P)==1<<i
        assert sum(l for c,l in [A]+P)==3*s+1
        entries=P[:2]; ni=i
        while len(entries)<2:
            entries.append((1<<ni,0));ni+=1
        b,c=entries;tail=P[2:]
        if sum(A)%2:
            cx,lx=A[0]+2*b[0],A[1]+2*b[1]+3
            j=v2(lx)
            assert j<v2(cx)
            if elapsed in (0,13,16):top.append(j)
            if elapsed==16:
                assert lx==1<<q and j==q and v2(cx)==q+1
                break
            base=(cx>>j,lx>>j)
            D=(c[0]+A[0]//2,c[1]+(A[1]+1)//2)
            A=(base[0],base[1]+1)
            P=[(base[0]<<t,base[1]<<t) for t in range(j-1)]+[D]+tail
        else:
            A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3);P=tail
        i=ni;s+=1
    assert top==[17,5,q]

qs=list(range(24,129))+[512,4096]
for q in qs:check(q)
result=dict(result='PASS',fixed_phase='6-8/3^1022',phase_mod_2_17=theta_res,
            u_mod_4=u_mod4,cases=len(qs),contiguous_q=[24,128],extra_q=[512,4096],
            scope='Synthetic states, not a refutation of an actual-orbit invariant')
Path(__file__).with_name('resonant_family_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
