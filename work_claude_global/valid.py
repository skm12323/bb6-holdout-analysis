from fcore import run
import hypo_lib as H
tau,typ,hpar,hlam,eps,steps,ifin=run(60000)
S=len(steps); s=0; bad=0; cnt=0
while s<S:
    st=steps[s]
    if not st[3]: s+=1; continue
    ch=[]; cur=s; ok=True
    while True:
        _,_,_,odd,j,xl,_=steps[cur]; ch.append(j)
        nxt=cur+1+tau[j-1]
        if nxt>=S: ok=False; break
        if steps[nxt][3]: cur=nxt
        else: end=nxt+1; break
    if not ok: break
    js,why=H.exit_run(3*s+5,3*s+4)
    cnt+=1
    if js!=ch: bad+=1; print(s,ch,js)
    s=end
print("epochs",cnt,"mismatch",bad)
