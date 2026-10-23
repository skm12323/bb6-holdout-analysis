"""Check nonnegativity of the canonical mass parts (head/tail lambdas) and
look for a state with time 5 and x=32 (the boundary case of the y>=28 claim)."""
import sys, json
from pathlib import Path
ROOT=Path(r'D:/math_cc')
sys.path.insert(0,str(ROOT/'work_c3_drift'))
sys.path.insert(0,str(ROOT/'work_ext_roots'))
from verify_shift_transport import Calendar, val
cal=Calendar(512)
neg=[];time5=[];nvals=0
for n in range(0,4000):
    r=cal.crossing(n)
    hl=r['head_lambda']; tl=r['tail_lambda']
    nvals+=1
    if hl is not None and hl<0: neg.append(('head',n,hl))
    if tl is not None and tl<0: neg.append(('tail',n,tl))
    if r['time']==5 and r['odd']:
        x=3*r['time']+4+(tl or 0)
        time5.append(dict(n=n,kind=r['kind'],x=str(x),j=val(x),head=hl,tail=tl,eps=r['epsilon']))
print(json.dumps(dict(crossings_checked=nvals,negative_lambda=neg[:8],n_neg=len(neg),
                       states_at_time_5=time5[:10],n_time5=len(time5)),indent=1))
