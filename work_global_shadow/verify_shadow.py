"""Full bigint F checks for the completed-tail shadowing theorem.
All sources are either actual small W crossings or explicitly synthetic states.
No residue engine or NT rule is used to evolve the trajectories.
"""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm

def val(x):
    return 10**12 if x == 0 else (abs(x)&-abs(x)).bit_length()-1

N = 4096
X = vm.Xdata(N,SMALL=N)
tau = {n:(a[1]+(b[1] if b else 0)-1)//3 for n,(_,a,b,_) in X.items()}

def run(A,P,i,s,finite=False,top_limit=None):
    P = list(P)
    s0 = s
    top_at = 0
    events = []
    decisions = []
    while True:
        assert sum(c for c,l in [A]+P) == 1 << i
        assert sum(l for c,l in [A]+P) == 3*s+(0 if finite else 1)
        assert all(c>0 and l>=0 for c,l in [A]+P)
        entries=P[:2]
        ni=i
        while len(entries)<2:
            if finite:
                entries.append((0,0))
            else:
                entries.append((1<<ni,0)); ni+=1
        b,c=entries
        tail=P[2:]
        e=s-s0
        if sum(A)%2 == 0:
            decisions.append(0)
            A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3)
            P=tail
        else:
            cx,lx=A[0]+2*b[0],A[1]+2*b[1]+3
            j=val(lx)
            assert j<val(cx) and A[0]%2==0
            decisions.append(j)
            if e==top_at:
                events.append(dict(j=j,sigma=val(cx),cx=cx,x=lx,Theta=3*s+(4 if finite else 5),e=e))
                if top_limit is not None and len(events)>=top_limit:
                    return events,decisions,e
                top_at=e+1+tau[j-1]
            u=(cx>>j,lx>>j)
            D=(c[0]+A[0]//2,c[1]+(A[1]+1)//2)
            A=(u[0],u[1]+1)
            P=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[D]+tail
        i=ni; s+=1
        if not P:
            return events,decisions,s-s0
        assert s-s0<10000

def lift(A,P,i,s,p,C,extra,D_override=None):
    assert len(P)<=1 and sum(A)%2==1
    b=P[0] if P else (1<<i,0)
    S=A[0]+b[0]
    assert S&(S-1)==0
    D=3*p*S*(1<<extra) if D_override is None else D_override
    assert D%3==0 and D>=p*S
    image=lambda z:(z[0]<<C,p*z[0]+z[1])
    newA=image(A)
    newP=[image(b),(S<<C,D-p*S)]
    newi=S.bit_length()+C
    return (newA,newP,newi,s+D//3),D

def check_source(A,P,i,s):
    events,decisions,duration=run(A,P,i,s)
    cases=transitions=nonnt=0
    for p,C,extra in [(1,1,0),(3,2,1),(19,5,3)]:
        seed,D=lift(A,P,i,s,p,C,extra)
        copied,copy_dec,copy_duration=run(*seed)
        assert copy_dec==decisions and copy_duration==duration
        assert len(copied)==len(events)
        for a,b in zip(events,copied):
            assert a['j']==b['j'] and a['e']==b['e']
            assert b['Theta']-a['Theta']==D and b['sigma']==a['sigma']+C
            assert val(b['x']-a['x'])>=a['sigma']
        for t in range(len(events)-1):
            a,b=events[t],copied[t]
            E=b['x']-a['x']
            E1=copied[t+1]['x']-events[t+1]['x']
            kind,head,Y,eps=X[a['j']-1]
            if kind=='a':
                assert E1==2*D-E//2
                nonnt+=events[t+1]['j']>=a['j']
            else:
                cross_cx=head[0]+2*Y[0]
                assert E%(1<<a['j'])==0
                assert E1==cross_cx*(E>>a['j'])
            transitions+=1
        cases+=1
    return cases,transitions,nonnt

def check_finite(A,P,i,s):
    events,decisions,duration=run(A,P,i,s)
    p,C=3,3
    b=P[0] if P else (1<<i,0)
    S=A[0]+b[0]
    q=p+1
    while (S*q)%3 != 2:
        q+=1
    D=S*q
    image=lambda z:(z[0]<<C,p*z[0]+z[1])
    seed=(image(A),[image(b),(S<<C,D-p*S)],S.bit_length()+C,s+(D+1)//3)
    out,dec,dur=run(*seed,finite=True)
    assert decisions==dec and duration==dur
    for a,b in zip(events,out):
        assert a['j']==b['j'] and b['sigma']==a['sigma']+C
        assert b['Theta']-a['Theta']==D and val(b['x']-a['x'])>=a['sigma']
    return 1

total=[0,0,0]
real_sources=0
odd_terminations=odd_collisions=0
finite_copies=0
small_shift_checks=small_shift_collisions=0
for n,(kind,A,Y,eps) in X.items():
    if kind not in ('b','c') or sum(A)%2==0:
        continue
    P=[] if kind=='b' else [Y]
    i=n-1 if kind=='b' else n
    counts=check_source(A,P,i,tau[n])
    total=[a+b for a,b in zip(total,counts)]
    real_sources+=1
    finite_copies+=check_finite(A,P,i,tau[n])
    events,_,_=run(A,P,i,tau[n])
    first_a=next((t for t in range(len(events)-1) if X[events[t]['j']-1][0]=='a'),None)
    if first_a is not None:
        r=events[first_a+1]['j']
        B=events[first_a+1]['x']-2
        Sval=events[first_a]['sigma']-1
        if 0<B<(1<<Sval):
            z=2
            D=-1+(z<<(n+1))
            while D%3 or D<2*(1<<n):
                z+=1; D=-1+(z<<(n+1))
            seed,_=lift(A,P,i,tau[n],1,2,0,D_override=D)
            oe,_,_=run(*seed,top_limit=first_a+2)
            assert oe[-1]['j']==val(B)<Sval
            small_shift_checks+=1
            small_shift_collisions+=r==1
        if r==1:
            odd_collisions+=1
        else:
            b=P[0] if P else (1<<i,0)
            S=A[0]+b[0]
            D=3*S+3  # odd, divisible by 3, and larger than p*S for p=3.
            seed,_=lift(A,P,i,tau[n],3,2,0,D_override=D)
            oe,_,_=run(*seed)
            assert [e['j'] for e in oe[:first_a+1]]==[e['j'] for e in events[:first_a+1]]
            assert len(oe)==first_a+2 and oe[-1]['j']==1
            odd_terminations+=1

# Safe 17 -> 5 -> 6 -> 1 synthetic sources, independently lifted and replayed.
synthetic=0
for z in (2,5,8,3*(1<<60)+2):
    u=z+1 if z%2==0 else z
    for sigma in (18,32):
        A=(1<<sigma,(1<<17)*(2*z-u)-9)
        P=[(1<<sigma,(1<<17)*(u-z)+3)]
        s=((1<<17)*z-7)//3
        counts=check_source(A,P,sigma+1,s)
        total=[a+b for a,b in zip(total,counts)]
        synthetic+=1
        finite_copies+=check_finite(A,P,sigma+1,s)

result=dict(result='PASS',actual_crossing_sources=real_sources,
            synthetic_rescue_sources=synthetic,copied_full_runs=total[0],
            exact_error_transition_checks=total[1],copied_non_NT_transitions=total[2],
            source_crossing_limit=N,odd_shift_first_a_terminal=odd_terminations,
            odd_shift_collision_sources=odd_collisions,finite_tail_shadow_runs=finite_copies)
result['small_shift_dominance_checks']=small_shift_checks
result['small_shift_collision_resolutions']=small_shift_collisions
Path(__file__).with_name('shadow_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
