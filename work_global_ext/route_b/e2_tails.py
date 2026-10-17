"""Exhaustive tails of the beta-walk from the route-a / route-b chain-1 states, for every even tau < 2^B.
route a: (d,bx)=(1+tau,3tau+2); route b: (1+tau,3tau+4).  Records chains after chain 1 (r-1),
non-descents, and the largest j seen.  Also checks Lemma T(2) 1<=bx<=6d-1 along the walk."""
import sys,time
from collections import Counter
from core import *
B=int(sys.argv[1]); T=load(int(sys.argv[2]) if len(sys.argv)>2 else 30000)
def tail(d,bx):
    j=v2(bx); bu=bx>>j; nd=0; L=0; jmax=j; jp=j
    while True:
        n=j-1; row=T[n]
        if not row['odd']: return L,nd,jmax
        if row['typ']=='a': bx=2*(3*d+1)+3*row['tau']-(bu<<n)
        else: cxW,lxW,jW=row['W']; bx=bu*cxW+lxW
        d+=1+row['tau']; assert 1<=bx<=6*d-1
        jn=v2(bx); L+=1
        if jn>=j: nd+=1
        jmax=max(jmax,jn); bu=bx>>jn; j=jn
t0=time.time()
for route,off in (('a',2),('b',4)):
    st=Counter(); ndc=Counter(); best=[]
    for tau in range(0,1<<B,2):
        L,nd,jm=tail(1+tau,3*tau+off)
        st[L]+=1; ndc[nd]+=1
        if nd>0 or L>=4: best.append((tau,L,nd,jm))
    print(route,'B=%d'%B,'tail-length dist',dict(sorted(st.items())),'nondescent dist',dict(sorted(ndc.items())),
          'examples',sorted(best,key=lambda z:(-z[2],-z[1]))[:8], round(time.time()-t0,1),'s')
