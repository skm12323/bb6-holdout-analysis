"""Positive two-a recurrence and small-parameter-core checks, exact integers.
Actual F epochs plus explicitly synthetic resonant epochs. Stdlib only.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm

N=8192
X=vm.Xdata(N,SMALL=N)
tau={n:(A[1]+(Y[1] if Y else 0)-1)//3 for n,(_,A,Y,_) in X.items()}
assert all(t<=n*n for n,t in tau.items())
def v2(x):
    assert x>0
    return (x&-x).bit_length()-1

def epochs(A,P,i,s,limit=None):
    top_at=s; current=[]; output=[]; s0=s
    while True:
        assert sum(c for c,l in [A]+P)==1<<i
        assert sum(l for c,l in [A]+P)==3*s+1
        ent=P[:2];ni=i
        while len(ent)<2:
            ent.append((1<<ni,0));ni+=1
        b,c=ent;tail=P[2:]
        if sum(A)%2==0:
            A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3);P=tail
            if s==top_at:
                if current:output.append(current);current=[]
                top_at=s+1
        else:
            cx,lx=A[0]+2*b[0],A[1]+2*b[1]+3;j=v2(lx)
            assert j<v2(cx) and A[0]%2==0
            if s==top_at:
                current.append(dict(j=j,x=lx,Theta=3*s+5,sigma=v2(cx),kind=X[j-1][0]))
                top_at=s+1+tau[j-1]
            u=(cx>>j,lx>>j);D=(c[0]+A[0]//2,c[1]+(A[1]+1)//2)
            A=(u[0],u[1]+1)
            P=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[D]+tail
        i=ni;s+=1
        if not P and (limit is None or i>limit):
            assert not current
            return output,s-s0
        assert s-s0<10**6

stats=dict(epochs=0,synthetic_epochs=0,two_a_checks=0,resonant_two_a_checks=0,
           same_k_parity_terminations=0,max_high_run=0,max_resonant_output=0,
           max_epoch_chains=0,core_return_maps=0,max_core_return_length=0)
examples=[]
def check(ep,synthetic=False):
    stats['epochs']+=1;stats['synthetic_epochs']+=synthetic
    js=[e['j'] for e in ep];g=max(js);B=(6*g*g+5).bit_length()
    m=sum(j<=B for j in js)
    assert len(js)<=3*m+2
    high=0
    for j in js:
        high=high+1 if j>B else 0
        assert high<=2
        stats['max_high_run']=max(stats['max_high_run'],high)
    stats['max_epoch_chains']=max(stats['max_epoch_chains'],len(js))
    for a,b,c in zip(ep,ep[1:],ep[2:]):
        if a['kind']!='a' or b['kind']!='a':continue
        k,l=tau[a['j']-1]//2,tau[b['j']-1]//2
        term=6*(k+l+1)
        assert c['x']==(a['x']+b['x'])//2+term
        stats['two_a_checks']+=1
        if k%2==l%2:
            assert c['j']==1
            stats['same_k_parity_terminations']+=1
        if a['j']==b['j']:
            assert c['j']==1
        else:
            p=min(a['j'],b['j'])-1;h=v2(term)
            if p!=h:
                assert c['j']==min(p,h)
            else:
                assert c['j']>=min(a['j'],b['j'])
                stats['resonant_two_a_checks']+=1
                stats['max_resonant_output']=max(stats['max_resonant_output'],c['j'])
        if a['j']>B and b['j']>B:
            assert c['j']<B
    for a,b,c,d in zip(ep,ep[1:],ep[2:],ep[3:]):
        if all(e['kind']=='a' for e in (a,b,c)) and a['j']==c['j']:
            assert d['x']==(3*c['x']-a['x'])//2 and d['j']>=a['j']
    low=[t for t,e in enumerate(ep) if e['j']<=B]
    for start,end in zip(low,low[1:]):
        assert 1<=end-start<=3
        alpha,beta,gamma,delta=F(1),F(0),F(0),0
        for t in range(start,end):
            e=ep[t];kind,H,Y,eps=X[e['j']-1];tt=tau[e['j']-1]
            if kind=='a':
                alpha,beta,gamma=-alpha/2,2-beta/2,2*delta+3*tt-gamma/2
            else:
                factor=F(H[0]+2*Y[0],1<<e['j'])
                alpha,beta,gamma=factor*alpha,factor*beta,factor*gamma+H[1]+2*Y[1]+3
            delta+=3*tt+3
        assert ep[end]['x']==alpha*ep[start]['x']+beta*ep[start]['Theta']+gamma
        assert ep[end]['Theta']==ep[start]['Theta']+delta
        assert abs(alpha)<1 and 0<=beta<=2
        stats['core_return_maps']+=1
        stats['max_core_return_length']=max(stats['max_core_return_length'],end-start)
    if synthetic and (g in (24,128,4096) or high==2):
        examples.append(dict(g=g,B=B,parameters=js,core_visits=m))

actual,steps=epochs((1,1),[],0,0,limit=N-2)
for ep in actual:check(ep)

# Extend the fixed rational-phase construction beyond the large jump to its end.
for q in list(range(24,129))+[256,512,1024,4096]:
    u=(1<<(q-17))+11
    Theta=(1<<q)-66-(u<<15)
    sigma=q+3
    A=(1<<sigma,2*Theta-(u<<17)-5)
    P=[(1<<sigma,(u<<17)-Theta+1)]
    es,_=epochs(A,P,sigma+1,(Theta-5)//3)
    assert len(es)==1 and [e['j'] for e in es[0]][:3]==[17,5,q]
    check(es[0],synthetic=True)

# A nonvacuous two-high-chain excursion: low 5 -> high 17 -> high 17 -> low 1.
u,v,sigma=19,23,21
Theta=(v<<17)-66-(u<<15)
A=(1<<sigma,2*Theta-(u<<17)-5)
P=[(1<<sigma,(u<<17)-Theta+1)]
es,_=epochs(A,P,sigma+1,(Theta-5)//3)
assert [e['j'] for e in es[0]]==[17,5,17,17,1]
check(es[0],synthetic=True)
examples.append(dict(g=17,B=(6*17**2+5).bit_length(),parameters=[17,5,17,17,1],core_visits=2))

# Explicit infeasibility of the apparent 17,5,17,5 all-a cycle.
a,b=17,5;k,l=tau[a-1]//2,tau[b-1]//2
x0=1<<a;x2=3<<a;x1=2*x2-x0-12*(k+l+1)
x3=(x1+x2)//2+6*(l+k+1)
assert [v2(x0),v2(x1),v2(x2),v2(x3)]==[17,5,17,19]

# Integer upper checks at rho=10^8; monotone polynomial proof is in the note.
g_upper=58;R_upper=3*g_upper**2+2
assert R_upper*31+2*g_upper<2*10**8
assert 4*(6+33*R_upper)<2*10**8
assert (R_upper+1)*(1+g_upper**2)<2*10**8
res=dict(result='PASS',actual_F_steps=steps,actual_F_epochs=len(actual),stats=stats,
         examples=examples,no_two_cycle_example=[17,5,17,19],
         scope='Synthetic examples are not claimed reachable on the actual orbit')
Path(__file__).with_name('core_checks.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
