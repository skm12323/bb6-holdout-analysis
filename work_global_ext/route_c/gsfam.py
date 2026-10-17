"""gsfam.py JMAX Q : GS(J',t,delta) = chain t>=1 of the symbolic exit S(J') (formal fire base lam), Theta shifted
by delta; 2-adic tree over lam (gtree.explore).  These are the states reached by route c (delta=-1) and by
c-copies out of large states (delta = theta-2)."""
import sys,json
from collections import Counter
from fdata import small_full, lam_walk, v2
from gtree import explore
JMAX=int(sys.argv[1]); Q=int(sys.argv[2])
NS=max(400,JMAX+2); SM=small_full(NS)
def sym_chains(J):
    """chains t>=1 of S(J): (t, j, d, alpha_u, beta_u, created_by)"""
    j=J; au,bu=1,0; d=0; out=[]
    while True:
        n=j-1; R=SM[n]
        if not R['odd']: return out
        T=R['tau']
        if R['typ']=='a':
            k=T//2; ax=2*(1<<J)-(au<<n); bx=2*(3*d+1+3*k)-(bu<<n); jn=v2(bx)
            assert v2(ax)>jn; au,bu=ax>>jn,bx>>jn; by='a'
        else:
            cu,lu=R['uW']; jn=R['omega']; au,bu=cu*au,cu*bu+lu; by=R['typ']
        d+=1+T; j=jn; out.append((len(out)+1,j,d,au,bu,by))
agg=Counter(); lamdep=Counter(); maxd=0; worst=None; ex=[]; nch=0
for J in range(5,JMAX):
    for (t,j,d,au,bu,by) in sym_chains(J):
        nch+=1
        for dl in range(-Q,Q+1):
            init=((1<<(J+1),(1<<J)+3*d+1+dl),(2*au,au+bu))
            r=explore(j,None,SM,NS,init=init)
            for k,v in r['st'].items(): agg[k]+=v
            if r['splits']:
                M=1<<j; th=((1<<J)+3*d+1+dl)%M
                lamdep[(j,th if th<=M//2 else th-M)]+=1
                if len(ex)<10: ex.append((J,t,j,dl,r['longest'],r['st']))
            if r['maxd']>maxd: maxd=r['maxd']; worst=(J,t,j,dl,r['longest'])
print('chains',nch,'leaves',dict(agg),'max further depth',maxd,worst)
print('lambda-dependent classes (j,theta):',sorted(lamdep.items())[:40])
print('examples',ex[:6])
