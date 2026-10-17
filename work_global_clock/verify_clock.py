"""Crossing-to-crossing clock identities and global reduction constants.
No epoch-length hypothesis is used to predict a next crossing.
"""
from pathlib import Path
from math import isqrt
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
N=8192
X=vm.Xdata(N+1,SMALL=N+1)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in X.items()}
def val(z):return (abs(z)&-abs(z)).bit_length()-1 if z else 10**9
def ceil_log2(n):return (n-1).bit_length()
def P(n):return 2*ceil_log2(6*n*n+5)**2+1345
def H(rho):
    n=2*rho+2
    return ceil_log2(6*n*P(n)+5)
def predict(n):
    kind,A,Y,e=X[n]
    if kind=='a':return 0,[],'same_step'
    if sum(A)%2==0:return 1,[],'even_step'
    j=val(A[1]+2*Y[1]+3);path=[];duration=0
    while True:
        path.append(j);duration+=1+tau[j-1]
        typ,B,Z,eps=X[j-1]
        if typ=='a':return duration,path,'a_crossing'
        if sum(B)%2==0:return duration+1,path,'even_bc_then_crossing'
        jn=val(B[1]+2*Z[1]+3)
        assert jn<=j-2-eps and jn<=j-3
        j=jn
counts={};maxgap=0;maxchains=0
for n in range(1,N):
    gap,path,reason=predict(n)
    assert gap==tau[n+1]-tau[n]
    assert gap<=P(n)
    counts[reason]=counts.get(reason,0)+1
    maxgap=max(maxgap,gap);maxchains=max(maxchains,len(path))
assert all(tau[n]<=n for n in range(64))
samples=list(range(100000000,100000128))+[1<<k for k in (27,32,64,128,256,512,1024)]
for n in samples:
    assert P(n)<2*n+1
    rho=n;h=H(rho);L=isqrt(rho)
    assert (L+2)*h<rho
    assert 4*(3+L*(h+1))<rho
    assert h<rho
    assert (rho-h-1)//h>L
p=24480;rho_lower=1<<(p-35)
assert rho_lower*P(rho_lower)<((1<<p)-4)//3
result=dict(result='PASS',crossing_gap_checks=N-1,case_counts=counts,
            max_observed_gap=maxgap,max_corridor_chains=maxchains,
            inequality_instances=len(samples),
            at_base=dict(rho=100000000,P=P(100000000),H=H(100000000),
                         safe_exit_budget=(100000000-H(100000000)-1)//H(100000000),
                         square_root_budget=isqrt(100000000)),
            strengthened_source_pointer_lower_exponent=p-35,
            scope='Finite identities and constant checks; all-scale arguments are analytic in PROOF_CLOCK.md')
print(json.dumps(result,indent=2))
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
