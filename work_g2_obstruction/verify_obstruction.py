"""Checks for the DL/fire-spectrum obstruction. No reachability claim for synthetic seeds.
Stdlib only; work_m's full pair map supplies a small audited-source table.
"""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm

def val(n):
    assert n>0
    return (n&-n).bit_length()-1

X=vm.Xdata(128,SMALL=128)
tau={n:(A[1]+(Y[1] if Y else 0)-1)//3 for n,(_,A,Y,_) in X.items()}
assert X[64]==('b',(1<<63,157),(1<<63,0),1)
assert tau[64]==52 and tau[4]==2 and tau[0]==0

small=[]
base_patterns=[]
for J in range(1,65):
    result=vm.sym_exit(J,X)
    js,types,r,G=result
    assert all(a>b for a,b in zip(js,js[1:]))
    duration=sum(1+tau[j-1] for j in js)+1
    duration+=duration%2
    base_patterns.append([J,list(js),duration//2])
    if J<=8:small.append(duration//2)
assert small==[1,1,2,2,3,3,3,4]
for J,js,gap in base_patterns:
    assert gap<=(1 if J==1 else 1<<(J-2))

# Accepted six-exit certificate gives dk <= (7*(J-1)^2+9)/2.
assert 7*15**2+9 < 1<<15
for J in range(16,513):
    assert 7*(J-1)**2+9 < 1<<(J-1)
    assert 7*J**2+9 < 2*(7*(J-1)**2+9)

# Strict-descent source-time upper bound: P(J) numerator with denominator 12.
def Pnum(J):return 2*J**3-3*J**2+7*J+12
assert Pnum(9)<=12*(1<<7)
for J in range(9,513):
    assert Pnum(J)<=12*(1<<(J-2))
    assert Pnum(J+1)<2*Pnum(J)
    assert 2*Pnum(J)-Pnum(J+1)==2*J**3-9*J**2+7*J+6

def label(k):return 1+val(3*k+2)
def maxgap(j):return 1 if j==1 else 1<<(j-2)
barriers=[];checks=0
for J in range(1,19):
    target=1 if J==1 else 8 if J==2 else (((1 if J%2==0 else 5)<<(J-1))-2)//3
    assert label(target)==J
    for k in range(1,target):
        assert maxgap(label(k))<=target-k,(J,target,k,label(k))
        checks+=1
    barriers.append([J,target])

# Synthetic canonical last-parent phase forced by eleven prior b returns.
def macro(z,u,sigma):
    assert z%3==0 and z<=u<2*z and u%2 and sigma>=66
    T=(z<<65)-10;s=(T-5)//3;s0=s
    A=(1<<sigma,((2*z-u)<<65)-25)
    P=[(1<<sigma,((u-z)<<65)+11)]
    i=sigma+1;js=[];margins=[]
    while True:
        assert sum(c for c,l in [A]+P)==1<<i
        assert sum(l for c,l in [A]+P)==3*s+1
        if not P:
            assert s-s0==61 and js==[65,5,5,1]
            return min(margins)
        entries=P[:2];ni=i
        while len(entries)<2:
            entries.append((1<<ni,0));ni+=1
        b,c=entries;tail=P[2:]
        if sum(A)%2:
            cx,lx=A[0]+2*b[0],A[1]+2*b[1]+3;j=val(lx)
            assert j<val(cx)
            margins.append(val(cx)-j)
            if s-s0 in (0,53,56,59):js.append(j)
            base=(cx>>j,lx>>j);D=(c[0]+A[0]//2,c[1]+(A[1]+1)//2)
            A=(base[0],base[1]+1)
            P=[(base[0]<<t,base[1]<<t) for t in range(j-1)]+[D]+tail
        else:
            A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3);P=tail
        i=ni;s+=1
        assert s-s0<=61

cases=0;minmargin=10**9
for z in list(range(3,61,3))+[3*(1<<80)]:
    us={u for u in (z,z+1,2*z-1) if z<=u<2*z and u%2}
    for u in us:
        for sig in (66,67,128):
            minmargin=min(minmargin,macro(z,u,sig));cases+=1

# The copied phase after b^m is 1-m. At q=5, first non-descent is m=12.
bad_depths=[m for m in range(1,33) if (1-m+3)%16==8]
assert bad_depths==[12,28]
result=dict(result='PASS',small_dk=small,barrier_pairs_checked=checks,
            six_exit_gap_bound_checked_J=[16,512],
            symbolic_descent_base_J=[1,64],base_patterns=base_patterns,
            barriers=barriers,macro_cases=cases,macro_parameters=[65,5,5,1],
            macro_steps=61,minimum_margin=minmargin,bad_b_depths_through_32=bad_depths,
            scope='Surjectivity is conditional on the global gap bound; synthetic seeds are not reachability certificates')
Path(__file__).with_name('obstruction_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
