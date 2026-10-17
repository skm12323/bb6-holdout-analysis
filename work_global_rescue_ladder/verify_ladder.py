"""Exact root-retaining ladder identities and analytic bound constants.
Constant-k trajectories are formal algebra tests, not canonical F itineraries.
"""
from pathlib import Path
import json
def val(n):return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9
cases=0;max_m=0
for P in (64,128,256,1024,2048):
    U,z=7,4
    x=(1<<P)*U;T=(1<<P)*z-2;b=0;d=-2
    for m in range(1,P//4+1):
        k=6 # synthetic at later parameters; actual table not asserted here
        mid=2*T-x//2+6*k;Tmid=T+3+6*k
        assert val(mid)==5
        x=2*Tmid-mid//2+6;T=Tmid+9
        assert b%4==0
        b=b//4+d+9*k+12;d+=6*k+12
        root=(1<<(P-2*m))*(U+4*((4**m-1)//3)*z)
        assert x==root+b and T==(1<<P)*z+d
        assert val(root)==P-2*m
        assert b==64*m and d==48*m-2
        assert 0<b<6*m*P*P and b<(1<<(P-2*m))
        assert val(x)==val(b)<P-2*m
        if P>=1024:assert b<8*P*P
        cases+=1;max_m=max(max_m,m)

phase_checks=0
for n in range(128):
    D=3**n
    for k in (6+32*3 if n%2==0 else 22+32*3,6 if n%2==0 else 22):
        A=3*D*(k+2)-8;N=9*D*(k+2)-8
        assert val(A)==4 and val(N)>=5
        assert N==3*A+16
        phase_checks+=1
    P=2*n+32
    assert 3**(n+2)*((P-1)**2+4)<2*(1<<(P-2))

# The phase-only collision at n=1022,p=17 is real in the relaxed model.
n=1022;p=17;k=6;D=3**n;N=9*D*(k+2)-8
assert val(3*D*(k+2)-8)==4 and val(N)==p-2
collision=[]
for R in (41,101,201):
    target=1<<R
    delta_mod=(6-8*pow(D,-1,1<<p))%(1<<p)
    u=(1<<(R-17))+1
    while (-32768*u-66-delta_mod)%(1<<p) or (target-32768*u-66)%3!=2:u+=2
    T=target-32768*u-66;x=(1<<p)*u
    assert 2*T-x-5>0 and x-T+1>0
    assert (D*(T-6)+8)%(1<<p)==0
    mid=2*T-x//2+36;Tmid=T+39
    out=2*Tmid-mid//2+6
    assert val(mid)==5 and out==target
    collision.append(dict(n=n,parent=p,output=R))
result=dict(result='PASS',root_identity_checks=cases,max_formal_depth=max_m,
            rational_phase_checks=phase_checks,phase_only_collision=collision,
            scope='Exact algebra and bound checks; formal long ladders and phase collisions are not claimed canonical-reachable')
print(json.dumps(result,indent=2))
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
