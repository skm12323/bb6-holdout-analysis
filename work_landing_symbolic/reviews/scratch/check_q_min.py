"""Check q=v2(real a-output)>=1 and behaviour of crossing(-1)."""
import sys, json
from pathlib import Path
ROOT=Path(r'D:/math_cc')
sys.path.insert(0,str(ROOT/'work_c3_drift'))
sys.path.insert(0,str(ROOT/'work_ext_roots'))
from verify_shift_transport import Calendar, first_fire, val, bounded_walk
cal=Calendar(512)
try:
    r=cal.crossing(-1); print('crossing(-1) returned:',{k:str(v) for k,v in r.items()})
except Exception as e:
    print('crossing(-1) raised',type(e).__name__,e)
qs=[];times=[]
for P in range(5,257):
    fire=first_fire(cal,P);rows=cal.epoch_crossings(fire)
    sources=[(fire['pointer'],6*fire['k']+4,6*fire['k']+5,fire['pointer'],'fire')]
    for n,r in rows.items():
        if r['kind']=='c' and r['odd']:
            sources.append((n,3*r['time']+4+r['tail_lambda'],3*r['time']+5,n-r['epsilon'],'c'))
    for n,x,th,sigma,kind in sources:
        st,real=bounded_walk(cal,x,th,sigma)
        for i,(j,g,xx,tt) in enumerate(real):
            r=cal.crossing(j-1)
            if not r['odd']:break
            if r['kind']=='a':
                y=2*tt+3*r['time']-xx/2; qs.append((val(y),P,n,kind))
                break
print('n first-a returns',len(qs),'min q',min(q[0] for q in qs),'q multiset',sorted(set(q[0] for q in qs)))
print('q=0 cases',[q for q in qs if q[0]==0][:5])
print('min j among real-walk chain parameters:')
mn=99
for P in range(5,257):
    fire=first_fire(cal,P);rows=cal.epoch_crossings(fire)
    sources=[(fire['pointer'],6*fire['k']+4,6*fire['k']+5,fire['pointer'],'fire')]
    for n,r in rows.items():
        if r['kind']=='c' and r['odd']:
            sources.append((n,3*r['time']+4+r['tail_lambda'],3*r['time']+5,n-r['epsilon'],'c'))
    for n,x,th,sigma,kind in sources:
        st,real=bounded_walk(cal,x,th,sigma)
        for j,g,xx,tt in real: mn=min(mn,j)
print(mn)
