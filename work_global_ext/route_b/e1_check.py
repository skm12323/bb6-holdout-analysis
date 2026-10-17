import sys,time
from collections import Counter
from core import *
N=int(sys.argv[1])
t0=time.time(); T=load(N); print('walk',N,round(time.time()-t0,1),'s')
rc=Counter(); nd=0; mism=0; maxr=0; ex={}
for J in range(3,N+2):
    se,st=symexit(J,T); assert st=='END',(J,st)
    bw,bst=beta_walk(J,0,0,T)
    if [(c['j'],c['x'][1],c['d']) for c in se]!=[(a,bx,dd) for (a,dd,bx,_) in bw] or bst!='END': mism+=1
    js=[J]+[c['j'] for c in se]
    nd+=sum(1 for t in range(1,len(js)-1) if js[t+1]>=js[t])
    r=len(se); rc[r]+=1
    if r>=2 and r not in ex: ex[r]=(J,js,[c['typ'] for c in se])
print('beta-walk mismatches',mism,'r-dist',dict(sorted(rc.items())),'non-descents after chain1',nd,ex)
