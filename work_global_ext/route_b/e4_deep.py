"""Deep exits through the beta-walk.  For J >= K' the chain-1 state of S(J) is
  route a: (d,bx)=(1+tau, 3tau+2),  route b: (1+tau, 3tau+4),   tau=tau(J-1) unknown (huge),
  route c: (1+tau, lambda of F's chain at step tau), that chain being chain t_W (a-created) of a W-epoch
           with fire step s_W, parameter J_W=v2(3s_W+4):  lambda = alpha^W*(3s_W+4)/2^J_W + beta^W,
           tau = s_W + d^W_{t_W}  (alpha^W,beta^W,d^W from S(J_W)).
For every m=j_1 (routes a,b) resp. every (J_W,t_W) (route c) we run the beta-walk for several random
values of the free high bits and check that the tail is independent of them; we record tail lengths and
non-descents.  (The walk only needs crossing data at indices < j_1.)"""
import sys,random,time
from collections import Counter
from core import *
M=int(sys.argv[1]); NT=int(sys.argv[2]); MW=int(sys.argv[3]) if len(sys.argv)>3 else 2000
T=load(NT); random.seed(1)
def tailw(d,bx):
    j=v2(bx); bu=bx>>j; js=[]; nd=0
    while True:
        n=j-1
        if n not in T: return js,nd,'OUT'
        row=T[n]
        if not row['odd']: return js,nd,'END'
        if row['typ']=='a': bx=2*(3*d+1)+3*row['tau']-(bu<<n)
        else: cxW,lxW,jW=row['W']; bx=bu*cxW+lxW
        d+=1+row['tau']; jn=v2(bx); js.append(jn)
        if jn>=j: nd+=1
        bu=bx>>jn; j=jn
def inv3(m): return pow(3,-1,1<<m)
t0=time.time(); res={}
for route,off in (('a',2),('b',4)):
    dist=Counter(); ndt=0; dep=0; first={}
    for m in range(2,M+1):
        base=(-off*inv3(m))%(1<<m)          # 3*base+off == 0 mod 2^m
        if base%2: base+=1<<m               # need tau even  (cannot happen, -off/3 is even 2-adically)
        assert base%2==0
        q=(3*base+off)>>m
        if q%2==0: base+=1<<m               # make v2(3tau+off)=m exactly (changes q by 3)
        outs=set()
        for rep in range(3):
            tau=base+(random.getrandbits(m+40)<<(m+1)) if rep else base
            assert tau%2==0 and v2(3*tau+off)==m
            js,nd,why=tailw(1+tau,3*tau+off)
            outs.add((tuple(js),why)); ndt+=nd
        if len(outs)>1: dep+=1
        js,why=outs.pop(); L=len(js); dist[L]+=1
        if L not in first: first[L]=(m,js)
    res[route]=dict(dist=dict(sorted(dist.items())),nondescents=ndt,tau_dependent=dep,first=first)
    print(route,res[route],'%.0fs'%(time.time()-t0)); sys.stdout.flush()
# route c
symc=Counter(); ndc=0; depc=0; firstc={}
for JW in range(3,MW+1):
    se,st=symexit(JW,T)
    for tW,c in enumerate(se,start=1):
        # chain tW is a-created iff the return after chain tW-1 had type a
        if c['typ']!='a': continue
        outs=set()
        for rep in range(3):
            # s_W even with v2(3 s_W+4)=JW
            base=(-4*inv3(JW))%(1<<JW); q=(3*base+4)>>JW
            if q%2==0: base+=1<<JW
            sW=base+((random.getrandbits(60))<<(JW+1) if rep else 0)
            assert v2(3*sW+4)==JW
            lu=(3*sW+4)>>JW
            lam=c['x'][0]*lu+c['x'][1]; tau=sW+c['d']
            js,nd,why=tailw(1+tau,lam); outs.add((tuple(js),why)); ndc+=nd
        if len(outs)>1: depc+=1
        js,why=outs.pop(); L=len(js); symc[L]+=1
        if L not in firstc: firstc[L]=(JW,tW,js)
print('c',dict(dist=dict(sorted(symc.items())),nondescents=ndc,dependent=depc,first=firstc),'%.0fs'%(time.time()-t0))
