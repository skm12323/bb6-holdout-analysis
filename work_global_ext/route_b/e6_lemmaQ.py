"""Lemma Q (three-term rule) on random generic beta-states and on all consecutive a-a pairs of the walks.
For chains t,t+1 both followed by odd type-a returns:
   beta_x(t+2) = x(t+1)/2 + 2^{n_t} beta_u(t) + 6(1+k_t+k_{t+1})        (identity)
   A1=j_{t+1}-1, A2=n_t, A3=1+v2(1+k_t+k_{t+1});  j_{t+2}=min if attained once."""
import random
from collections import Counter
from core import *
T=load(30000); random.seed(3)
an=[n for n in range(4,40) if T[n]['odd'] and T[n]['typ']=='a']
C=Counter()
for trial in range(2000000):
    n0=random.choice(an); j=n0+1
    d=random.getrandbits(random.choice([40,80,200,1000]))+10
    bu=random.getrandbits(max(1,d.bit_length()-j))|1
    bx=bu<<j
    if bx>6*d-1: continue
    # step 1
    k0=T[n0]['tau']//2
    bx1=6*d+2+3*T[n0]['tau']-(bu<<n0); d1=d+1+T[n0]['tau']
    if bx1<=0: C['nonpos']+=1; continue
    j1=v2(bx1); n1=j1-1
    if n1 not in T or not T[n1]['odd'] or T[n1]['typ']!='a': continue
    k1=T[n1]['tau']//2; bu1=bx1>>j1
    bx2=6*d1+2+3*T[n1]['tau']-(bu1<<n1)
    assert bx2==bx1//2+(bu<<n0)+6*(1+k0+k1), 'identity'
    j2=v2(bx2); A=[j1-1,n0,1+v2(1+k0+k1)]; m=min(A)
    if A.count(m)==1: assert j2==m; C['unique-min ok']+=1
    elif A.count(m)==3: assert j2==m; C['triple ok']+=1
    else: assert j2>m; C['double -> larger ok']+=1
    if j1<j and j2>=j1:   # non-descent after descending a-step
        assert v2(1+k0+k1)==n1-1; C['Q2 nondescent ok']+=1
    if j1>j and A.count(m)==1 and not (v2(1+k0+k1)==n0-1): assert j2<j; C['Q3 fallback ok']+=1
print(dict(C))
