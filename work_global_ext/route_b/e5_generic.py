"""Random generic beta-states (j0,d,beta_u), 1<=2^j0*beta_u<=6d-1, d random BIT-bit integer.
Distribution of #chains and #non-descents (size-only behaviour of the beta-system) [C-type evidence]."""
import sys,random
from collections import Counter
from core import *
S=int(sys.argv[1]); BIT=int(sys.argv[2]); T=load(30000); random.seed(7)
oddn=[n for n in range(4,BIT) if T[n]['odd']]
Lc=Counter(); ndc=Counter(); best=None
for _ in range(S):
    n0=random.choice(oddn); j0=n0+1
    d=random.getrandbits(BIT)|(1<<(BIT-1))
    bu=random.randrange(1,max(2,(6*d-1)>>j0))|1
    if (bu<<j0)>6*d-1: continue
    out,st=beta_walk(j0,d,bu,T,limit=10000)
    js=[j0]+[o[0] for o in out]
    nd=sum(1 for i in range(len(js)-1) if js[i+1]>=js[i])
    Lc[len(out)]+=1; ndc[nd]+=1
    if best is None or nd>best[0]: best=(nd,len(out),j0,js[:30])
print('samples',S,'BIT',BIT,'chains dist',dict(sorted(Lc.items())),'non-descent dist',dict(sorted(ndc.items())),'best',best)
