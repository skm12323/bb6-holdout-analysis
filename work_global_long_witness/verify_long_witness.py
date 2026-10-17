"""Seven productive block entries in a positive safe LOCAL continuation.

Actual canonical source records are recomputed. The constructed outer
state is not claimed reachable from F's initial state.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
sys.path.insert(0,str(ROOT/'work_global_clock_words'))
import verify_m as vm
from clock_words import clock_projection,fire_projection,v2

P=122436;R=367354
half_times={5:1,17:6,P:54614,R:163862}
sources={};start=time.monotonic()
def capture(n,data):
    if n+1 in half_times:
        typ,H,Y,eps=data;k=half_times[n+1]
        assert typ=='a' and Y is None and eps==0
        assert H==(1<<n,6*k+1)
        sources[n+1]=dict(parameter=n+1,type=typ,half_time=k,epsilon=eps)
vm.Xdata(R,capture,SMALL=64)
assert set(sources)==set(half_times)
print('Actual source records verified',round(time.monotonic()-start,2),'seconds',flush=True)

blocks={q:dict(alpha=F(1),B=F(0),d=0,G=0,k=k,T=1+2*k)
        for q,k in half_times.items()}
word=(R,5,17,5,P,5,17,5)
projection=clock_projection(word,blocks)
assert projection is not None
assert projection['theta_bits']==122439 and projection['anchor_bits']==R+1
assert projection['anchor_slope']==0 and projection['anchor_offset']==1<<R
assert fire_projection(projection) is None

# Choose an integer clock inside the positive mass cone, using the exact
# clock cylinder. x0=3*2^R satisfies its retained root congruence.
x0=3*(1<<R);period=1<<projection['theta_bits'];residue=projection['step_residue']
target=(3*x0//4-3)//3
multiple=max(0,(target-residue+period-1)//period)
s0=residue+multiple*period;theta0=3*s0+5
assert theta0==9*(1<<(R-2))+5*(1<<(P+2))-1081554
assert (theta0-projection['theta_residue'])%period==0
assert theta0-1<x0<2*theta0-5

# An explicit pair-map lift; sigma may subsequently be increased by
# scaling every coefficient and shifting the unread-original pointer.
sigma=R+16;gap=2*R+1;i=sigma+gap;s=s0
H=(((1<<gap)-1)<<sigma,2*theta0-x0-5)
D=(1<<sigma,x0-theta0+1)
path=[];margins=[];identities=0
for q in word:
    theta=3*s+5;x=H[1]+2*D[1]+3;c=H[0]+2*D[0]
    assert H[0]+D[0]==1<<i and H[1]+D[1]==3*s+1
    assert min(H+D)>0 and sum(H)%2==1
    assert v2(x)==q and v2(c)>q and q<i
    path.append(q);margins.append(v2(c)-q)
    k=half_times[q]
    u_c,u_l=c>>q,x>>q
    # Exact source replay followed by return, using the proven image map.
    new_D=((1<<i)+H[0]//2,(H[1]+1)//2)
    new_H=((1<<(q-1))*u_c,(1<<(q-1))*u_l+6*k+1)
    assert new_H[1]+2*new_D[1]+3==2*theta-x//2+6*k
    H,D=new_H,new_D;i+=1;s+=1+2*k;identities+=1

theta=3*s+5;x=H[1]+2*D[1]+3;c=H[0]+2*D[0]
assert v2(x)==6 and v2(c)==sigma-8 and v2(c)>6
assert min(H+D)>0 and H[0]+D[0]==1<<i and H[1]+D[1]==3*s+1
path.append(6)
# The actual q=6 b return copies X(5)'s chain (coefficient 48, lambda 10).
x=48*(x>>6)+10;c=48*(c>>6);theta+=9
assert v2(x)==1 and v2(c)==sigma-10 and v2(c)>1
path.append(1)  # X(0) is even-headed, so this terminal chain ends the epoch.

assert path==[R,5,17,5,P,5,17,5,6,1]
assert v2(3*(3*half_times[P]-2))==15
assert all(2*k<=(q-1)**2 for q,k in half_times.items())

# Symbolic coefficient lift sigma'=s0: no number 2^s0 is materialized.
# These scale inequalities check compatibility with the numeric clock,
# pointer-speed and deficit bounds, not canonical reachability.
lift_sigma=s0;lift_i=lift_sigma+gap
assert lift_sigma>sigma
assert lift_i<=2*s0 and s0<=lift_i**2
assert 4*(gap+32)<=lift_i
assert gap+32<=(lift_i.bit_length()-1)**3
assert lift_sigma-10>R
assert s-s0+5<gap

def digest(n):return hashlib.sha256(n.to_bytes((n.bit_length()+7)//8,'big')).hexdigest()
result=dict(result='PASS',sources=list(sources.values()),path=path,
            seven_productive_entries=path[1:8],pair_macro_checks=identities,
            initial_parameter=R,initial_sigma=sigma,initial_pointer=sigma+gap,
            clock_bits=projection['theta_bits'],initial_time_bit_length=s0.bit_length(),
            minimum_checked_margin=min(margins),
            witness_recipe=dict(x0='3*2^367354',
                theta0='9*2^367352 + 5*2^122438 - 1081554',
                clock='s0=(theta0-5)/3',
                coefficient_gap=gap,initial_time_sha256=digest(s0),initial_theta_sha256=digest(theta0)),
            symbolic_lift_checks='sigma=s0 satisfies numeric clock, pointer-speed, deficit and margin bounds',
            scope='Positive safe local continuation using actual sources; outer canonical reachability unproved')
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
