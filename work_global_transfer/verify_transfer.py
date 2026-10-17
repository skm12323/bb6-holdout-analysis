"""General rescue transport identities and the complete W=16 boundary.

The identities are algebraic tests, not claims of canonical reachability.
The finite source table is used only for explicitly bounded exclusions.
"""
from pathlib import Path
from fractions import Fraction as F
import contextlib, io, json, runpy

ROOT=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()):
    old=runpy.run_path(str(ROOT/'work_global_weight16/verify_weight16.py'))
S,A,T=old['states'],old['a_states'],old['table']
could5=old['could_output5'];vm=old['vm']

def val(x):
    x=F(x)
    assert x.denominator%2
    if not x:return None
    return vm.v2(abs(x.numerator))

def cong(x,y,r):
    delta=F(x)-F(y)
    return not delta or val(delta)>=r

eta_set={F(row['theta']) for row in old['ties'][16]}
assert eta_set=={F(5),F(-1,3),F(-19,9)}
origins=[]
for eta in sorted(eta_set):
    alpha=3-eta
    assert alpha in S[14]
    origins.append(dict(kind='A',eta=eta,alpha=alpha))
    if eta+1 in S[14]:
        origins.append(dict(kind='B',eta=eta,beta=eta+1))
    for ws in range(2,15,2):
        wo=14-ws
        for beta in sorted(S[wo]):
            for phi in sorted(A[ws]):
                if beta+phi-2!=eta:continue
                # Neither exceptional source representative is used here.
                assert phi not in {F(10,3),F(46,9)}
                alpha=3-phi
                origins.append(dict(kind='C',eta=eta,alpha=alpha,beta=beta,
                                    outer_weight=wo,source_weight=ws))
assert len(origins)==20

for row in origins:
    if row['kind']=='B':continue
    alpha=row['alpha']
    pmin=17 if alpha.denominator>1 or row['kind']=='A' else 14
    assert not any(could5(p,alpha) for p in range(5,pmin))
    row['parent_lower_bound']=pmin

# Exact transport checks with arbitrary odd-denominator phases and shifts.
# These need not correspond to parameter-5 source occurrences: they test
# the polynomial identities only. The theorem separately assumes those.
count=0
for p in (14,17,32,64):
    for alpha in (F(-2),F(1),F(7,3),F(46,9)):
        for beta in (F(-1,3),F(2),F(6)):
            for k in (1,6,22):
                x=F((1<<p)*3);theta=F((1<<p)*4)+alpha
                xs=2*theta-x/2+6*k;ts=theta+6*k+3
                # Direct A-origin second return.
                out=2*ts-xs/2+6;tout=ts+9
                assert cong(out,alpha+9*k+12,p-2)
                assert cong(3*tout-2*out,alpha+12,p-1)
                count+=1
                # C transport, at both minimal and generous source margin.
                for sigma_pre in (p+1,p+8):
                    s=sigma_pre-1;Q=s+11;c_s=3*(1<<s)
                    shift=F((1<<Q)*7)+beta-2
                    copied=xs+c_s*5;tc=ts+shift
                    out=2*tc-copied/2+6;tout=tc+9
                    eta=beta+1-alpha
                    assert cong(out,alpha+2*beta+9*k+8,p-2)
                    assert cong(3*tout-2*out,15-eta,p-1)
                    count+=1
for Q in (65,80,128):
    for beta in (F(6),F(2,3),F(-20,9)):
        for v in (1,5,11):
            x=F((1<<Q)*3);theta=F((1<<Q)*4)+beta;src=32*v
            y=3*x/4+src;t=theta+src-1
            out=2*t-y/2+6;tout=t+9
            assert cong(out,F(3,2)*src+2*beta+4,Q-3)
            assert cong(3*tout-2*out,16-beta,Q-2)
            count+=1

# Analytic size bounds: finite checks cover the bases and sample the
# monotone tail. The proof supplies the factor-of-two argument.
for p in range(14,4096):
    assert F(9,2)*(p-1)**2+22 < 1<<(p-2)
    assert F(27,2)*(p-1)**2+25 < 1<<(p-2)
for p in range(17,4096):
    assert F(81,2)*(p-1)**2+154 < 1<<(p-2)
for Q in range(65,4096):
    assert F(27,2)*(Q-2)**2+66 < 1<<(Q-3)
for j in range(64,4096):
    assert 92+27*(j-1)**2 < 2*(1<<(j-2))

new_a={3-z for z in S[16]}|{5-eta/3 for eta in eta_set}
new_s=new_a|{z-1 for z in S[16]}
for ws in range(2,17,2):
    new_s|={o+s-2 for o in S[16-ws] for s in A[ws]}
assert {5-eta/3 for eta in eta_set}=={F(10,3),F(46,9),F(154,27)}

# A copy of an already-rescued source: integer local lift illustrating
# why the normal-source theorem cannot be reapplied indiscriminately.
# Canonical reachability of this outer lift is NOT asserted.
source_table=vm.Xdata(256,SMALL=256)
typ,H,Y,e=source_table[233]
assert typ=='a' and sum(H)%2 and (H[1]-1)//6==102
p=234;k=102;source_sigma=p+10;Q=source_sigma+12
x=F(7*(1<<p));theta=F(4*(1<<p)-2)
x1=2*theta-x/2+6*k;t1=theta+6*k+3
xs=2*t1-x1/2+6;ts=t1+9
assert val(x1)==5 and val(xs)==5
assert cong(3*ts-2*xs,10,p-1)
mod=1<<Q
shift=3*((5*pow(9,-1,mod))%mod)+12*mod
assert shift%3==0 and cong(shift,F(5,3),Q)
outer_theta=shift+2
outer_u=(outer_theta.numerator+mod-1)//mod
if outer_u%2==0:outer_u+=1
assert mod*outer_u>=outer_theta-1 and mod*outer_u<=2*outer_theta-5
cs=81*(1<<source_sigma)
yc=xs+cs*outer_u;tc=ts+shift
assert val(yc)==5 and cong(tc,5,5)
out=2*tc-yc/2+6;tout=tc+9
assert val(out)==6
assert cong(5*tout-4*out,6,p-1)
assert cong(tout,F(6,5),6) and not cong(tout,F(10,3),6)
witness=dict(source_parent=p,source_half_time=k,source_output_parameter=5,
             copied_parameter=5,output_parameter=6,new_phase='6/5',
             invalid_naive_phase='10/3',
             scope='Integer local transport witness; outer canonical reachability unproved')

# Iterated joint transport: the 2-adic divisibility of b compensates
# for falling source-coefficient precision. These are formal identities.
R=160;aa=3;bb=2;ll=94;yy=F(16);tt=F(42)
assert cong(aa*tt-bb*yy,ll,R)
for r in range(128):
    sigma=R-r-1;coeff=3*(1<<sigma);shift=3*(r+1);k=1+r%7
    yc=yy+coeff*5;tc=tt+shift
    yy=2*tc-yc/2+6*k;tt=tc+6*k+3
    ll=(12*k+12)*bb-(6*k+3)*aa-ll-aa*shift
    aa,bb=4*bb-aa,2*bb
    assert aa==(2**(r+4)+(-1)**(r+1))//3 and bb==2**(r+2)
    assert cong(aa*tt-bb*yy,ll,R)

result=dict(result='PASS',exact_identity_checks=count,
            iterated_joint_checks=128,
            boundary_origins=[{k:str(v) if isinstance(v,F) else v for k,v in r.items()}
                              for r in origins],
            weight18_phase_set=list(map(str,sorted(new_s))),
            rescued_source_copy_witness=witness,
            scope='Uniform separated transfer lemma; complete W=16 departures to W=18. No all-weight closure.')
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='boundary_origins'},indent=2))
print('Boundary origins:',len(origins))
