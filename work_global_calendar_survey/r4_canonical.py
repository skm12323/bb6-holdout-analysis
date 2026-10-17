"""Construct the canonical deep target a-type m=6131 and project its full exit."""
import sys,time,json,hashlib
sys.path.insert(0,'../work_global_calendar')
from calendar_oracle import Calendar, val
m=int(sys.argv[1]); B=int(sys.argv[2])
t=time.time(); cal=Calendar(B); print("build %.0fs"%(time.time()-t),flush=True)
h=(-pow(3,-1,1<<(m-1)))%(1<<(m-1))
for tt in range(64):
    k=h+tt*(1<<(m-1))
    if k<1 or k%2==0 or val(3*k+1)!=m-1: continue
    t=time.time(); f=cal.preceding_fire_by_time(2*k)
    print("lift",tt,"nav %.0fs"%(time.time()-t),"fire at k?",f['k']==k,flush=True)
    if f['k']==k:
        J=f['pointer']+1; r=cal.projected_epoch(J,limit=64)
        out=dict(m=m,lift=tt,k_bits=k.bit_length(),J_bits=J.bit_length(),J_sha256=hashlib.sha256(str(J).encode()).hexdigest(),
                 fire_J=f['J'],status=r['status'],word=[str(x) if x>10**6 else x for x in r['word']],types=r.get('types'),loss=r.get('loss'))
        print(json.dumps(out)); json.dump(out,open('r4_m%d.json'%m,'w'),indent=1); break
