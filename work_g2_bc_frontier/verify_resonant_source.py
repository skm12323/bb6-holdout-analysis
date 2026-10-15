"""Real small crossing datum and symbolic-compatible unbounded b/a rebounds.
The outer local prefixes are NOT asserted reachable on the canonical orbit.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
p=24480;hits=[]
def cb(n,data):
    if n==p-1:
        kind,H,Y,e=data
        assert kind=='a' and sum(H)%2
        s=(H[1]-1)//3
        assert s==21832
        hits.append(dict(parameter=p,source_crossing=n,half_time=s//2))
vm.Xdata(p,cb=cb,SMALL=0)
assert len(hits)==1
A=1<<p;k=10916
assert (A-4)%3==0 and 40+6*k==65536
checks=[]
for Q in (p+3,p+11,p+101):
    for gap in (8,20,100):
        r=Q+gap
        if r%2==0:r+=1
        Y=1<<r;w=(9*(1<<(r-Q)))//10
        if w%2==0:w-=1
        X=(1<<Q)*w
        v=(Y-5*X//8-3*A//2)//65536-1
        assert Y-5*X//8-3*A//2==(v+1)*65536
        assert v>0 and v%2 and vm.v2(X)==Q
        u=X//16-4096*v-3
        assert u>0 and u%2
        theta0=X//2+(1<<15)*v-27
        la=196608*v-X+37;lb=3*X//2-163840*v-68
        assert la>=0 and lb>=0 and theta0%3==2
        assert la+2*lb+3==32*u
        assert la+lb==theta0-4
        assert 15*X <32*65536*v<17*X
        # Make the first parameter-5 entry a genuine local a-return as
        # required by the mixed-block representation, not just a free pair.
        prev_x=393216*v-2*X;prev_theta=theta0-39
        prev_a=3*X-327680*v-137
        prev_b=360448*v-5*X//2+67
        assert prev_a>0 and prev_b>0 and vm.v2(prev_x)==17
        assert prev_a+2*prev_b+3==prev_x
        assert 2*prev_theta-prev_x//2+36==32*u
        assert prev_x//2+37==la and (prev_a+1)//2==lb
        # Two a steps produce the exact R21 entry X.
        x1=2*theta0-(32*u)//2+6;theta1=theta0+9
        assert x1==(1<<17)*v
        x2=2*theta1-x1//2+36;theta2=theta1+39
        assert x2==X and theta2==X//2+(1<<15)*v+21
        # Formal b replay from the actual parameter-p fire, then known a at p.
        xp=3*X//4+A;tp=theta2+A-1
        assert vm.v2(xp)==p
        out=2*tp-xp//2+6*k
        assert out==Y and vm.v2(out)==r
        tout=tp+3+6*k
        assert tout-Y//2==3*X//16+A//4+32751
        # A sufficiently large coefficient scale also meets the elementary
        # pointer/time envelopes; no huge coefficient 2^sigma is materialized.
        s0=(theta0-5)//3;sig0=s0
        assert sig0-5>r and sig0+3<=2*s0
        assert (tout-5)//3<sig0**2
        checks.append(dict(formal_Q=Q,output_parameter=r,initial_time_bits=s0.bit_length(),
                           satisfies_local_mass_time_and_margin=True))
result=dict(result='PASS',actual_small_source=hits[0],formal_checks=checks,
            real_fire_mass='2^24480',
            actual_parent='Q=rho_p+2; rho_p is the pointer of the certified barrier fire',
            caveat='Numerical Q values test algebra, not actual parent pointers. The actual-Q construction is symbolic; outer reachability is unproved.')
Path(__file__).with_name('resonant_source_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='formal_checks'},indent=2))
print('formal checks',len(checks))
