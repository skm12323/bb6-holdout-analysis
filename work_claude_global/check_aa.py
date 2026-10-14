# Verify: first return type a (odd) => j1 = v2(3s'+2), s'=tau(J-1);
# second return type a (odd) => j2 = min(J'', j1-1) when J''!=j1-1, J''=v2(3*tau(j1-1)+4)
# first return type b (odd) => j1 = v2(3s'+4)
from fdata import crossings, v2
from collections import Counter
NM=20000
tau,typ,hpar,X=crossings(NM+40)
def exit_run(Th,x):
    js=[]
    while True:
        j=v2(x); js.append(j); n=j-1
        if not hpar[n]: return js
        if typ[n]=='a':
            k=tau[n]//2; x=2*Th-x//2+6*k; Th=Th+3+6*k
        else:
            cX,lX,_=X[n]; x=((cX*x)>>j)+lX; Th=Th+3*tau[n]+3
res=Counter()
for J in range(12,NM):
    if not hpar[J-1]: continue
    for lam in range(1,200,2):
        v=(lam<<J)-4
        if v%3==0 and (v//3)%2==0: break
    js=exit_run(v+5, v+4)
    sp=tau[J-1]
    if typ[J-1]=='a': res['a:j1 ok' if js[1]==v2(3*sp+2) else 'a:j1 BAD']+=1
    elif typ[J-1]=='b': res['b:j1 ok' if js[1]==v2(3*sp+4) else 'b:j1 BAD']+=1
    if typ[J-1]=='a' and len(js)>2 and typ[js[1]-1]=='a':
        j1=js[1]; Jpp=v2(3*tau[j1-1]+4)
        if Jpp!=j1-1: res['aa ok' if js[2]==min(Jpp,j1-1) else 'aa BAD']+=1
        else: res['aa tie']+=1
print(res)
