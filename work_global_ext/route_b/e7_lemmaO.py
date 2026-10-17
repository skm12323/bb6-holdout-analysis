"""Lemma O (offset junction) on random generic beta-states.
Chain s with parameter j_s, X(n_s) odd type b/c, X(n_{s+1}) odd type a (n_{s+1}=omega(n_s)-1).
Claim: x_{s+2} = x^W + 2*delta - 2^{n_{s+1}} c_{u^W} beta_{u_s} with delta = Theta_s-2 = 3d_s-1 (beta-parts),
x^W = F's own next chain after C^W (computed from real data), so j_{s+2}=min(j^W,1+v2(delta)) if unique."""
import random
from collections import Counter
from core import *
T=load(30000); random.seed(5)
bcn=[n for n in range(4,29000) if T[n]['odd'] and T[n]['typ'] in 'bc' and T[n]['W'][2]-1 in T
     and T[T[n]['W'][2]-1]['odd'] and T[T[n]['W'][2]-1]['typ']=='a']
print('b/c crossings followed by an odd a-crossing:',bcn[:20],len(bcn))
C=Counter()
for trial in range(300000):
    n0=random.choice(bcn); j=n0+1
    d=random.getrandbits(random.choice([30,60,200]))+10
    bu=random.getrandbits(max(1,d.bit_length()-j))|1
    if (bu<<j)>6*d-1: continue
    cW,lW,jW=T[n0]['W']
    bx1=bu*cW+lW; d1=d+1+T[n0]['tau']; j1=v2(bx1); assert j1==jW
    n1=j1-1; k=T[n1]['tau']//2; bu1=bx1>>j1
    bx2=6*d1+2+3*T[n1]['tau']-(bu1<<n1); j2=v2(bx2)
    # W's own next chain (real F): Theta^W = 3 tau(n0)+5, u^W = (cW,lW)>>jW
    ThW=3*T[n0]['tau']+5; luW=lW>>jW; cuW=cW>>jW
    xW=2*(ThW+3*k)-(luW<<n1)
    delta=3*d-1
    assert bx2==xW+2*delta-((cuW*bu)<<n1), 'identity'
    A=[v2(xW),1+v2(delta),n1+v2(cuW)]; m=min(A)
    if A.count(m)==1: assert j2==m; C['unique ok']+=1
    elif A.count(m)==3: assert j2==m; C['triple ok']+=1
    else: assert j2>m; C['double->larger ok']+=1
print(dict(C))
