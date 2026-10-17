"""Period-clock divisibility: exact block identities and a finite base.

No sampled affine word is asserted canonically reachable. The small
clock certificate is generated anew from the canonical crossing table.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sys,json,random

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
table=vm.Xdata(4096,SMALL=4096)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}

def val(x):
    x=F(x)
    if not x:return 10**9
    return vm.v2(abs(x.numerator))-vm.v2(x.denominator)

def block(q):
    j=q;alpha=F(1);B=F(0);d=G=0
    while True:
        typ,H,Y,eps=table[j-1]
        if sum(H)%2==0:return None
        if typ=='a':
            k=tau[j-1]//2
            return dict(q=q,alpha=alpha,B=B,d=d,G=G,k=k,T=d+1+2*k,
                        z=q-G-1)
        ratio=F(H[0]+2*Y[0],1<<j)
        constant=H[1]+2*Y[1]+3
        alpha*=ratio;B=ratio*B+constant
        G+=1+eps;d+=1+tau[j-1];j=val(constant)

blocks={q:b for q in range(5,4096) if (b:=block(q)) is not None}
small=[b for q,b in blocks.items() if q<1024]
assert len(small)==325
pair_count=0;min_gap=10**9
for b in small:
    for c in small:
        gap=max(b['z'],c['z'])-val(b['T']+c['T'])
        assert gap>0,(b['q'],c['q'])
        min_gap=min(min_gap,gap);pair_count+=1

def compose(word):
    # (x,Theta) -> (a*x+b*Theta+c, Theta+3*T)
    a,b,c=F(1),F(0),F(0);T=E=0
    for q in word:
        r=blocks[q];s=-r['alpha']/2
        v=6*r['d']+6*r['k']-r['B']/2
        a,b,c=s*a,s*b+2,s*c+6*T+v
        T+=r['T'];E+=r['G']+1
    return a,b,c,T,E

rng=random.Random(20261016)
keys=list(blocks)
words=[[q] for q in keys]
words += [rng.choices(keys,k=m) for m in range(2,33) for _ in range(12)]
checks=0
for word in words:
    a,b,c,T,E=compose(word)
    assert val(a)==-E
    assert val(b)==blocks[word[0]]['G']+2-E
    for x0,t0 in ((F(32),F(59)),(F(96),F(110))):
        x1=a*x0+b*t0+c;t1=t0+3*T
        x2=a*x1+b*t1+c
        assert x2-x1==a*(x1-x0)+3*b*T
        # Independently apply the original maps, not the affine composition.
        x,t=x0,t0
        for q in word:
            r=blocks[q]
            x=2*t-r['alpha']*x/2+6*r['d']+6*r['k']-r['B']/2
            t+=3*r['T']
        assert x==x1 and t==t1
        checks+=1

for Q in range(1024,8192):
    # Small-q times in the period also fit this max-Q bound.
    assert max(b['T'] for b in small)<3*Q*Q+1
    # 2^(Q/4-1)>2*(3Q^2+1), avoiding fractional exponents by flooring.
    assert 2*(3*Q*Q+1)<1<<(Q//4-1)
    # Stronger endpoint useful for short-period exclusion.
    assert (1<<233)*(3*Q*Q+1)<1<<(Q//4-1)

result=dict(result='PASS',productive_small=len(small),small_ordered_pairs=pair_count,
            small_pair_minimum_divisibility_gap=min_gap,
            max_small_block_time=max(b['T'] for b in small),
            affine_words_checked=len(words),affine_identity_checks=checks,
            max_formal_word_length=max(map(len,words)),
            small_block_records=[{k:v for k,v in b.items() if k in ('q','G','T','z')}
                                 for b in small],
            scope='All-scale conditional period divisibility and no six alternating entries; no global exit bound')
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='small_block_records'},indent=2))
