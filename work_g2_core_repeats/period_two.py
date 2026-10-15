"""Exact necessary 2-adic constraints for alternating block entry words.
Feasible means only congruence-feasible; no orbit reachability is asserted.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
N=256;table=vm.Xdata(N,SMALL=N)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
def val(x):return (abs(x)&-abs(x)).bit_length()-1 if x else 10**9
def block(q):
    j=q;a=F(1);B=F(0);d=0
    while True:
        typ,H,Y,e=table[j-1]
        if sum(H)%2==0:return None
        if typ=='a':return a,B,d,tau[j-1]//2
        c=H[0]+2*Y[0];l=H[1]+2*Y[1]+3;r=F(c,1<<j)
        a*=r;B=r*B+l;d+=1+tau[j-1];j=val(l)
def constrain(base,cols,A,B,target,mod):
    cs=[A*v[0]+B*v[1] for v in cols]
    rhs=(target-A*base[0]-B*base[1])%mod
    s=min(val(cs[0]),val(cs[1]),val(mod));g=1<<s
    if rhs%g:return None
    M=mod//g
    if M==1:return base,cols
    p=0 if val(cs[0])==s else 1;o=1-p
    inv=pow((cs[p]//g)%M,-1,M)
    offset=(rhs//g*inv)%M;adjust=(-(cs[o]//g)*inv)%M
    nb=tuple(base[i]+offset*cols[p][i] for i in range(2))
    nc=[None,None]
    nc[p]=tuple(M*v for v in cols[p])
    nc[o]=tuple(cols[o][i]+adjust*cols[p][i] for i in range(2))
    return nb,nc
def solve(q,r,limit=10):
    # Affine values in initial odd bases U,V.
    xs=[(F(0),F(1<<q),F(0)),(F(0),F(0),F(1<<r))]
    base=(1,1);cols=[(2,0),(0,2)]
    for i in range(2,limit):
        qa=q if i%2==0 else r;qb=r if i%2==0 else q
        a,B,d,k=blocks[qa];b,E,f,l=blocks[qb]
        C=B/2+6+6*k+6*l+6*f-E/2
        x=tuple(a*xs[-2][z]/2+(1-b/2)*xs[-1][z]+(C if z==0 else 0) for z in range(3))
        den=max(v.denominator for v in x)
        coeff=[int(v*den) for v in x]
        ans=constrain(base,cols,coeff[1],coeff[2],den*(1<<qa)-coeff[0],den*(1<<(qa+1)))
        if ans is None:return i+1
        base,cols=ans;xs.append(x)
        # Check the retained lattice really satisfies this necessary condition.
        for u,v in [base,tuple(base[z]+cols[0][z] for z in range(2)),tuple(base[z]+cols[1][z] for z in range(2))]:
            assert (coeff[0]+coeff[1]*u+coeff[2]*v)%(den*(1<<(qa+1)))==den*(1<<qa)
    return None
solver_checks=0
for seed in range(64):
    base=(1,1);cols=[(2,0),(0,2)]
    possible={(u,v) for u in range(16) for v in range(16) if u%2 and v%2}
    for t in range(3):
        A=(seed+3*t)%9-4;B=(3*seed+t)%11-5
        mod=1<<(1+(seed+t)%4);target=(seed*7+t*3)%mod
        possible={(u,v) for u,v in possible if (A*u+B*v-target)%mod==0}
        ans=constrain(base,cols,A,B,target,mod)
        if ans is None:
            assert not possible;solver_checks+=1;break
        base,cols=ans
        represented={((base[0]+i*cols[0][0]+j*cols[1][0])%16,
                      (base[1]+i*cols[0][1]+j*cols[1][1])%16)
                     for i in range(16) for j in range(16)}
        assert represented==possible;solver_checks+=1

blocks={q:block(q) for q in range(5,N)};blocks={q:v for q,v in blocks.items() if v is not None}
rows=[]
for q in blocks:
    for r in blocks:
        if q==r:continue
        rows.append(dict(q=q,r=r,first_impossible_length=solve(q,r)))
counts={str(n):sum(row['first_impossible_length']==n for row in rows) for n in sorted({r['first_impossible_length'] for r in rows},key=lambda x:100 if x is None else x)}
result=dict(result='PASS',parameter_range=[5,N-1],productive_parameters=len(blocks),
            solver_bruteforce_crosschecks=solver_checks,
            ordered_pairs=len(rows),length_counts=counts,
            survivors=[r for r in rows if r['first_impossible_length'] is None],records=rows)
print(json.dumps({k:v for k,v in result.items() if k not in ('records','survivors')},indent=2))
print('survivors',result['survivors'][:10])
Path(__file__).with_name('period_two_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
