from skeleton import run
from fdata import crossings
cross,_,_=run(3000,check=True,report=0)
tau,typ,hpar,X=crossings(3100)
bad=0
for n,t,s,h in cross:
    if n>=3000: continue
    if (typ[n],tau[n],hpar[n])!=(t,s,h): bad+=1; print("mismatch",n,(typ[n],tau[n],hpar[n]),(t,s,h)); 
    if bad>5: break
print("checked",len([c for c in cross if c[0]<3000]),"bad",bad, "missing", set(range(3000))-set(c[0] for c in cross))
