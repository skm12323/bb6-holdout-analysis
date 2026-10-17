"""All-prefix positivity in root-consistent finite word cylinders."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,random

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
sys.path.insert(0,str(ROOT/'work_global_clock_words'))
import verify_m as vm
from clock_words import positive_fire_lift,v2
table=vm.Xdata(4096,SMALL=4096)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
blocks={}
for q in range(2,4096):
    j=q;alpha=F(1);B=F(0);d=G=0
    while True:
        typ,H,Y,e=table[j-1]
        if sum(H)%2==0:break
        if typ=='a':
            k=tau[j-1]//2
            blocks[q]=dict(alpha=alpha,B=B,d=d,G=G,k=k,T=d+1+2*k)
            break
        ratio=F(H[0]+2*Y[0],1<<j);lam=H[1]+2*Y[1]+3
        alpha*=ratio;B=ratio*B+lam;d+=1+tau[j-1];G+=1+e;j=v2(lam)

word_count=checks=0;max_threshold=0
sample_words={}
for J in range(2,4096):
    U=1 if J%2==0 else 5
    x=F((1<<J)*U);theta=int(x)+1;word=[J]
    for _ in range(16):
        if word[-1] not in blocks:break
        b=blocks[word[-1]]
        x=2*theta-b['alpha']*x/2+6*b['d']+6*b['k']-b['B']/2
        theta+=3*b['T'];word.append(v2(x))
    else:raise AssertionError('unexpected long finite-base word')
    word_count+=1
    if J in (5,14,28,65):sample_words[J]=word
    for minimum in (0,1<<8192):
        lift=positive_fire_lift(word,blocks,minimum)
        assert lift is not None and lift['step']>=minimum
        max_threshold=max(max_threshold,lift['sufficient_theta_threshold'])
        x=F(lift['x']);theta=lift['theta']
        assert theta%3==2 and x==theta-1
        for i,q in enumerate(word):
            assert x.denominator==1 and v2(x)==q
            if i:
                assert 2*theta-x-5>0 and x-theta+1>0
            if i+1<len(word):
                b=blocks[q]
                x=2*theta-b['alpha']*x/2+6*b['d']+6*b['k']-b['B']/2
                theta+=3*b['T']
        checks+=1

# Arbitrary formal block orders: positivity of the cone does not rely
# on choosing the correct valuation branch. These tests do NOT claim
# that the randomized words are feasible integer itineraries.
rng=random.Random(20261017);keys=list(blocks);cone_checks=0
for _ in range(64):
    x=F(4);theta=F(5)
    for q in rng.choices(keys,k=64):
        b=blocks[q]
        assert 0<b['alpha']<=1 and 0<=b['B']<=6*b['d']
        xc=b['alpha']*x+b['B'];tc=theta+3*b['d']
        assert 0<xc<=2*tc-5
        x=2*tc-xc/2+6*b['k'];theta=tc+6*b['k']+3
        assert theta-1<x<2*theta-5
        cone_checks+=1

# Independent microstep realization from a synthetic fire, not a replay
# of only the affine scalar equations. Coefficients are deliberately
# large enough for all calls. The starts are not claimed canonical.
raw_checks=[]
for J,word in sample_words.items():
    lift=positive_fire_lift(word,blocks,1<<256)
    s=lift['step'];start=s;i=J+128;head=(1<<i,3*s+1);pending=[]
    calls=[];return_kind={};seen=[];microsteps=0;first=True
    while first or pending:
        while calls and calls[-1]<s:calls.pop()
        top=not calls
        entries=pending[:2];pos=i
        while len(entries)<2:entries.append((1<<pos,0));pos+=1
        (cb,lb),(cc,lc)=entries
        assert head[0]+sum(v[0] for v in pending)==1<<i
        assert head[1]+sum(v[1] for v in pending)==3*s+1
        assert min(head)>0 and all(c>0 and l>=0 for c,l in pending)
        if sum(head)%2==0:
            head=(head[0]+cb+cc,head[1]+lb+lc+3);push=[]
        else:
            cx,lx=head[0]+2*cb,head[1]+2*lb+3;j=v2(lx)
            assert j<v2(cx) and head[0]%2==0
            if top:
                if first or return_kind.get(s)=='a':seen.append(j)
                t=tau[j-1];return_kind[s+1+t]=table[j-1][0]
                if t:calls.append(s+t)
            u=(cx>>j,lx>>j)
            push=[(u[0]<<z,u[1]<<z) for z in range(j-1)]
            push.append((cc+head[0]//2,lc+(head[1]+1)//2))
            head=(u[0],u[1]+1)
        count=len(pending)
        if count>=2:pending=pending[2:]
        else:i+=2-count;pending=[]
        pending=push+pending;s+=1;first=False;microsteps+=1
        assert microsteps<10000
    assert seen==word,(J,seen,word)
    raw_checks.append(dict(J=J,word=seen,microsteps=microsteps))

result=dict(result='PASS',rooted_words=word_count,positive_lift_checks=checks,
            maximum_sufficient_theta_threshold=max_threshold,
            arbitrary_formal_cone_checks=cone_checks,
            full_pair_microstep_lifts=raw_checks,
            larger_clock_test='minimum starting step 2^8192',
            scope='All-prefix lambda positivity and exact word congruences; constructed lifts are not asserted canonical')
Path(__file__).with_name('positive_lift_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
