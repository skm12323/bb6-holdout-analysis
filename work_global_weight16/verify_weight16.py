"""Root-weight grammar through 16 with proved exceptional A normalizers.
Phase sets are overapproximations; a phase does not assert reachability.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
table=vm.Xdata(128,SMALL=128)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
states={0:{F(1)}};a_states={0:set()};ties={}
def nt_ties(phases):
    result=[]
    for theta in sorted(phases):
        for j in range(5,64):
            typ,H,Y,e=table[j-1]
            if typ!='a' or sum(H)%2==0:continue
            k=tau[j-1]//2;n,D=theta.numerator,theta.denominator
            if (n+3*k*D-D*(1<<(j-2)))%(1<<(j-1))==0:
                result.append(dict(theta=str(theta),j=j,k=k))
    return result
for W in range(2,17,2):
    aa={3-z for z in states[W-2]}
    # Normal NT branches stay in the overapproximation; the stated rescue
    # lemmas add the true output phases of the exceptional branches.
    if W in (10,14):aa.add(F(10,3))
    if W==14:aa.add(F(46,9))
    out=aa|{z-1 for z in states[W-2]}
    for Ws in range(2,W-1,2):
        Wo=W-Ws-2
        out|={o+s-2 for o in states[Wo] for s in a_states[Ws]}
    states[W]=out;a_states[W]=aa
    ties[W]=nt_ties(out)
assert ties[8]==[dict(theta='5',j=5,k=1)]
assert ties[10]==[]
assert ties[12]==[dict(theta='-1/3',j=5,k=1),dict(theta='5',j=5,k=1)]
assert ties[14]==[]
assert all(not ties[w] for w in (2,4,6))

# Low-parent exclusions: if the residue vanishes, higher bits could matter,
# so count that case as a possible hit rather than silently discarding it.
def could_output5(p,theta):
    typ,H,Y,e=table[p-1]
    if typ!='a' or sum(H)%2==0:return False
    k=tau[p-1]//2;n,D=theta.numerator,theta.denominator
    r=(2*n+6*k*D-D*(1<<(p-1)))%(1<<p)
    return r==0 or vm.v2(r)==5
for m in range(5):
    assert not any(could_output5(p,F(1-m)) for p in range(5,14))
for theta in (F(-2),F(10,3)):
    assert not any(could_output5(p,theta) for p in range(5,17))
for Q in range(5,65):
    typ,H,Y,e=table[Q-1]
    assert not (typ=='b' and sum(H)%2 and vm.v2(H[1]+3)==5)

# Verify every C-origin of the W=12,theta=5 exceptional state.
c_origins=[]
for Ws in range(2,11,2):
    Wo=10-Ws
    for o in states[Wo]:
        for s in a_states[Ws]:
            if o+s-2==5:c_origins.append((Wo,Ws,o,s))
expected={(8-2*m,2*m+2,F(5-m),F(m+2)) for m in range(5)}
assert set(c_origins)==expected
assert F(2,3) not in states[10]  # no B origin for -1/3 at W=12
for Ws in range(2,11,2):
    assert all(o+s-2!=F(-1,3) for o in states[10-Ws] for s in a_states[Ws])

# Exact signed affine identities of the B-origin and all C-origins.
identity_checks=0
for Q in (65,80,128):
    for u,z,v in ((3,4,5),(7,5,11)):
        x=(1<<Q)*u;T=(1<<Q)*z+6;A=32*v
        x5=3*x//4+A;T5=T+A-1
        out=2*T5-x5//2+6;Tout=T5+9
        assert out==(1<<(Q-3))*(16*z-3*u)+48*v+16
        assert (3*Tout-2*out-10)%(1<<(Q-2))==0
        identity_checks+=1
for m in range(5):
    for p in (14,17,32,64):
        for k in (1,6,17):
            u,z=3,4;T=(1<<p)*z+1-m;x=(1<<p)*u
            xs=2*T-x//2+6*k;Ts=T+3+6*k
            Q=p+2*m+20;c=3*(1<<(Q-2*m-4))
            D=(1<<Q)*7+3-m;outer_base=5
            out=2*(Ts+D)-(xs+c*outer_base)//2+6
            Tout=Ts+D+9
            const=9*k+19-3*m
            assert (out-const)%(1<<(p-2))==0
            assert (3*Tout-2*out-10)%(1<<(p-1))==0
            identity_checks+=1

for p in (17,32,64):
    for k in (22,54,86):
        x=(1<<p)*3;T=F((1<<p)*12+10,3)
        x1=2*T-F(x,2)+6*k
        T1=T+6*k+3
        out=2*T1-x1/2+6;Tout=T1+9
        assert out==F((1<<p)*12,3)+(1<<(p-2))*3+F(27*k+46,3)
        joint=9*Tout-6*out-46
        assert joint.denominator==1 and joint.numerator%(1<<(p-1))==0
        identity_checks+=1

for p in range(14,4096):assert 9*(p-1)**2+38<2*(1<<(p-2))
for p in range(17,4096):assert 27*(p-1)**2+92<2*(1<<(p-2))
for j in range(64,4096):assert 92+27*(j-1)**2<2*(1<<(j-2))
for Q in range(65,4096):assert 9*(Q-2)**2+44<2*(1<<(Q-3))

# A concrete canonical reachability consequence, including one departure
# from W=16 only for the fixed parent parameter 17, not general W=18.
parent17=[]
for W in range(0,15,2):
    for theta in states[W]:
        if could_output5(17,theta):
            c=theta+66  # 9*k + theta + 12, k(16)=6
            q=vm.v2(abs(c.numerator))
            assert q<15 and q!=17
            parent17.append(dict(parent_weight=W,phase=str(theta),rebound=q))
assert {r['phase'] for r in parent17}=={'-2','46/9'}
result=dict(result='PASS',phase_sets={str(w):list(map(str,sorted(s))) for w,s in states.items()},
            candidate_nt_ties=ties,c_origins=[list(map(str,row)) for row in c_origins],
            parent17_rescues=parent17,
            exact_identity_checks=identity_checks,
            scope='Weight<=16 phase inclusion; departures from weight16 are diagnostic only')
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('phase_sets','c_origins')},indent=2))
print('phase counts',{w:len(s) for w,s in states.items()})
