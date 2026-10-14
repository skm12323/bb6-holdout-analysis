import sys, pickle
from collections import Counter
from fdata import crossings, v2
NM=420
tau,typ,hpar,X=crossings(NM)
def exit_run(Th, x, maxr=1000):
    js=[]
    while True:
        j=v2(x); js.append(j); n=j-1
        if n not in hpar: return js,'unknown'
        if not hpar[n]: return js,'stop'
        if len(js)>maxr: return js,'long'
        if typ[n]=='a':
            k=tau[n]//2; x=2*Th-x//2+6*k; Th=Th+3+6*k
        else:
            cX,lX,jj=X[n]; assert jj==j or True
            assert (cX*x) % (1<<j)==0, (n,cX,j)
            x=((cX*x)>>j)+lX; Th=Th+3*tau[n]+3
