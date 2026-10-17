"""Rooted affine intercept bounds and the long witness's ancestry cost.

Actual-source tests are finite; the all-history implication is proved
in PROOF_ANCESTRY.md. No reachability is inferred from passing examples.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
table=vm.Xdata(4096,SMALL=4096)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}

def ancestry_lower_bound(x,theta):
    H=(2*theta-5).bit_length()-1
    delta=abs(3*x-4*theta)
    # Exact monotone necessary inequality, using d<=3G(H^2+1).
    def allowed(G):
        d=3*G*(H*H+1)
        return theta<=(1<<G)*(delta+4*d+3)+d
    lo,hi=0,H+1
    assert allowed(hi)
    while lo<hi:
        mid=(lo+hi)//2
        if allowed(mid):hi=mid
        else:lo=mid+1
    return lo

records=0;max_loss=0
for J in range(2,4096):
    U=1 if J%2==0 else 5
    theta_root=(1<<J)*U+1
    x=F(theta_root-1);theta=theta_root
    A=1;G=0;c=F(-1);d=0
    for _ in range(16):
        assert x==F(A,1<<G)*theta_root+c
        assert theta==theta_root+d and A%2 and 0<F(A,1<<G)<2
        assert G==0 and c==-1 or G>0 and 0<c<=2*d+1
        delta=3*x-4*theta
        assert theta_root<=(1<<G)*(abs(delta)+4*d+3)
        assert x.denominator==1
        if (2*theta-5).bit_length()-1>=32:
            assert ancestry_lower_bound(int(x),theta)<=G
        records+=1;max_loss=max(max_loss,G)
        j=vm.v2(int(x));typ,H,Y,eps=table[j-1]
        if sum(H)%2==0:break
        t=tau[j-1]
        if typ=='a':
            x=2*theta-x/2+3*t
            c=2*d-c/2+3*t
            A=(1<<(G+2))-A;G+=1
        else:
            ratio=F(H[0]+2*Y[0],1<<j);lam=H[1]+2*Y[1]+3
            assert 0<ratio<1 and 1<=lam<=6*t+5
            e=1+eps;odd=ratio*(1<<e)
            assert odd.denominator==1 and int(odd)%2
            x=ratio*x+lam;c=ratio*c+lam;A*=int(odd);G+=e
        d+=3*t+3;theta+=3*t+3
    else:raise AssertionError('unexpected finite-base long root exit')

P=122436;R=367354
x=3*(1<<R);theta=9*(1<<(R-2))+5*(1<<(P+2))-1081554
H=(2*theta-5).bit_length()-1
delta=abs(3*x-4*theta)
assert H==R+2 and delta==80*(1<<P)-4326216
bound=ancestry_lower_bound(x,theta)
assert bound==R-P-5==244913
C=delta+12*H*(H*H+1)+3
coarse=max(0,H-1-(C-1).bit_length())
assert coarse==244912

# Existing V4 certificate applies to ANY root fire preceding this fixed
# time: its J<=floor(log2(theta-1))=R+1<10^6, and its total loss is <=6.
root_parameter_cap=(theta-1).bit_length()-1
assert root_parameter_cap==R+1<10**6 and bound>6
assert bound>=1 and (bound+7)//8==30615

# U-scaled family: the deviation is fixed but the clock grows.
family=[]
for U in (1,3,(1<<1024)+1,(1<<1000000)+1):
    xx=3*(1<<R)*U
    tt=9*(1<<(R-2))*U+5*(1<<(P+2))-1081554
    assert abs(3*xx-4*tt)==delta and tt%3==2
    HH=(2*tt-5).bit_length()-1
    CC=delta+12*HH*(HH*HH+1)+3
    assert CC*CC<1<<HH
    needed=ancestry_lower_bound(xx,tt)
    assert needed>=HH//2-1
    family.append(dict(odd_U_bits=U.bit_length(),clock_bits=tt.bit_length(),
                       required_loss=needed))

for Htest in range(32,4096):
    assert 3*Htest*(Htest*Htest+1)<1<<(Htest-2)
result=dict(result='PASS',actual_source_affine_records=records,
            observed_max_loss=max_loss,witness_required_loss=bound,
            witness_coarse_required_loss=coarse,
            witness_prior_returns_if_base_eps7=(bound+7)//8,
            witness_root_parameter_cap=root_parameter_cap,
            existing_V4_total_loss_cap=6,
            fixed_witness_canonical_reachability='excluded by the existing V4 certificate',
            odd_U_family=family,
            scope='General conditional ancestry inequality; concrete fixed-clock witness excluded. Unbounded-clock word reachability remains open.')
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
