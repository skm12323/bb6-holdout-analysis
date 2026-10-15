"""Small symbolic base for the initial b/c-prefix first-a lemma.
No NT rule is used: x and Theta are affine in the odd initial fire base U.
"""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm

N=4096
X=vm.Xdata(N,SMALL=N)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in X.items()}
def val(x):return (abs(x)&-abs(x)).bit_length()-1 if x else 10**9
assert all(eps<=7 for n,(_,_,_,eps) in X.items() if n<64)

records=[]
for J in range(1,N):
    xc,x0=1<<J,0
    Tc,T0=1<<J,1
    j=J;G=m=D=0;path=[j]
    while True:
        kind,H,Y,eps=X[j-1]
        if sum(H)%2==0:
            records.append(dict(J=J,result='even_end',copies=m,G=G,parameters=path))
            break
        if kind=='a':
            assert 0 < xc <= 1 << J and 0 <= x0 <= 6*D-m
            ac=2*Tc-xc//2
            beta=2*T0-x0//2+3*tau[j-1]
            assert ac>0 and beta>0 and val(ac)==J-G-1
            r=val(beta)
            assert r<val(ac)
            assert beta<3*J**3
            if J>=1024:
                assert 4*G<=3*J
                assert beta.bit_length()-1 < (J-4)//4
            records.append(dict(J=J,result='first_a_safe',copies=m,G=G,
                                parameters=path+[r],beta=beta,coefficient_valuation=val(ac),
                                margin=val(ac)-r))
            break
        cx=H[0]+2*Y[0];lx=H[1]+2*Y[1]+3
        assert 0 < cx <= 1 << j and 0 < lx <= 6*tau[j-1]+5
        assert xc%(1<<j)==0 and x0%(1<<j)==0
        xc,x0=cx*(xc>>j),cx*(x0>>j)+lx
        Tc,T0=Tc,T0+3*tau[j-1]+3
        G+=1+eps;m+=1;D+=1+tau[j-1]
        jn=val(x0)
        assert jn<val(xc) and jn<=j-2-eps
        assert val(xc)==J-G
        j=jn;path.append(j)

first=[r for r in records if r['result']=='first_a_safe']
result=dict(result='PASS',J_range=[1,N-1],small_base_J=[1,1023],
            first_a_cases=len(first),even_end_cases=len(records)-len(first),
            min_symbolic_margin=min(r['margin'] for r in first),
            max_bc_copies=max(r['copies'] for r in records),records=records)
Path(__file__).with_name('first_a_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
