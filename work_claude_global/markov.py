from fdata import crossings, v2
from collections import defaultdict
NX=700
tau,typ,hpar,X=crossings(NX)
def ex(Th,x):
    js=[]; ts=[]
    while True:
        j=v2(x); js.append(j); n=j-1
        if n>=NX-5: return js,ts,'nodata'
        if not hpar[n]: return js,ts,'stop'
        ts.append(typ[n])
        if typ[n]=='a': k=tau[n]//2; x=2*Th-x//2+6*k; Th=Th+3+6*k
        else: cX,lX,_=X[n]; x=((cX*x)>>j)+lX; Th=Th+3*tau[n]+3
trans=defaultdict(set); maxr=0; inc=[]
import random
random.seed(5)
for j1 in range(2,660):
    for first in 'ab':
        for trial in range(3):
            # random s with required valuation, s even
            while True:
                s=random.getrandbits(j1+40)*2
                if first=='b' and v2(3*s+4)==j1: break
                if first=='a' and v2(3*s+2)==j1: break
                # adjust s to satisfy: solve 3s+c = 2^j1 * odd
                c=4 if first=='b' else 2
                m=random.getrandbits(40)*2+1
                if (m<<j1)-c>0 and ((m<<j1)-c)%3==0 and (((m<<j1)-c)//3)%2==0:
                    s=((m<<j1)-c)//3; break
            js,ts,why=ex(4+3*s, 3*s+4 if first=='b' else 3*s+2)
            if why!='stop': print("!!",first,j1,js,why)
            maxr=max(maxr,len(js))
            prev=first
            for t in range(len(js)-1):
                trans[(prev,js[t])].add(js[t+1]); prev=ts[t]
                if js[t+1]>=js[t]: inc.append((first,j1,js))
nd=[(k,v) for k,v in trans.items() if len(v)>1]
print("max tail length",maxr,"non-deterministic transitions:",len(nd), nd[:15])
print("non-decreasing steps:",inc[:10],len(inc))
