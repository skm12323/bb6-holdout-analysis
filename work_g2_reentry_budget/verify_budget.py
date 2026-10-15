"""Exact arithmetic for the guarded R21 -> 17 -> R21 reentry budget."""
from fractions import Fraction as F
from pathlib import Path
import json
cases=0
for t in range(1,128,2):
    for d in range(-255,256,2):
        for v in (1,5,17):
            X=(1<<17)*(v+d)
            k=(1<<15)*t-7
            Y=F(X,2)+(1<<16)*v+6*(k+7)
            Z=F(3,2)*Y-(1<<16)*v
            vn=Y/(1<<17);dn=(Z-(1<<17)*vn)/(1<<17)
            assert dn==F(d+3*t,4)
            assert vn==v+2*dn
            assert vn+dn-(v+d)==F(9*t-d,4)
            cases+=1
for t in range(1,1024,2):
    d=9*t;dn=(d+3*t)//4
    assert dn==3*t and (dn+3*t)%4==2

g=1<<127
K=F((g-1)**2,2)
T=(K+7)/(1<<15)
M=3*(K+7)
assert 3*T < 1<<240
assert 4*M/(1<<17)==3*T
assert F(256**2,2)>=32761 and F(255**2,2)<32761
assert 32761%65536==32761 and (32761+7)==1<<15

# The absolute-value envelope, including negative starting coordinates.
envelope_checks=0
for initial in (-10**12,-1000,0,1000,10**12):
    bound=100;z=F(initial)
    for n in range(1,25):
        forcing=(n*17)%bound+1
        z=z/4+forcing
        envelope=F(abs(initial),4**n)+F(4*bound,3)*(1-F(1,4**n))
        assert abs(z)<=envelope
        envelope_checks+=1
result=dict(result='PASS',exact_identity_cases=cases,
            equal_entry_obstructions=512,envelope_checks=envelope_checks,
            certified_cap='2^127',source_lower_parameter=257,
            scope='Guarded-pattern algebra and conditional constants; not actual trajectory simulation')
print(json.dumps(result,indent=2))
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
