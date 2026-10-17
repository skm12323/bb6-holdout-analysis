"""Canonical deep-first-step targets: for each m, find actual fires giving first exit parameter j1=m,
then project the full exit of the corresponding huge root parameter J."""
import sys,json,time
from collections import Counter
sys.path.insert(0,'../work_global_calendar')
from calendar_oracle import Calendar, val
B=int(sys.argv[1]); MMAX=int(sys.argv[2])
cal=Calendar(B); top=cal.boundary_pointer; M=1<<B
res=[]; stat=Counter(); t0=time.time()
def fire_at_k(k):
    f=cal.preceding_fire_by_time(2*k)
    return f if f['k']==k else None
def project(J):
    if not 5<=J<top: return {'status':'out of range'}
    try: return cal.projected_epoch(J,limit=64)
    except AssertionError: return {'status':'non-descent/assert'}
for m in range(2,MMAX+1):
    # type b: first fire with parameter exactly m is at k=h with 3h+2 = 0 mod 2^(m-1), minimal positive
    h=(-2*pow(3,-1,1<<(m-1)))%(1<<(m-1))
    cands=[h+t*(1<<(m-1)) for t in range(0,8)]
    found_b=False
    for k in cands:
        if k<1 or 1+val(3*k+2)!=m: continue
        f=fire_at_k(k)
        if f:
            found_b=True
            J=f['pointer']+2; r=project(J); stat[('b',r['status'])]+=1
            res.append(dict(m=m,first='b',k_bits=k.bit_length(),J_bits=J.bit_length(),**{x:(str(y) if x=='word' else y) for x,y in r.items() if x in('status','word','types','loss')}))
            break
    if not found_b: stat[('b','no canonical fire in first 8 lifts')]+=1
    # type a: fire at odd k (J(k)=1) with v2(3k+1)=m-1, i.e. v2(3s+2)=m
    h=(-pow(3,-1,1<<(m-1)))%(1<<(m-1))
    found=False
    for t in range(0,64):
        k=h+t*(1<<(m-1))
        if k<1 or k%2==0 or val(3*k+1)!=m-1: continue
        if 2*k>=2*cal.boundary_k:
            stat[('a','out of calendar range')]+=1; found=True; break
        f=fire_at_k(k)
        if f:
            J=f['pointer']+1; r=project(J); stat[('a',r['status'])]+=1
            res.append(dict(m=m,first='a',k_bits=k.bit_length(),J_bits=J.bit_length(),**{x:(str(y) if x=='word' else y) for x,y in r.items() if x in('status','word','types','loss')}))
            found=True; break
    if not found: stat[('a','no canonical fire in first 64 lifts')]+=1
lens=Counter(len(eval(x['word']))-1 for x in res if 'word' in x and x['status']=='closed')
out=dict(B=B,MMAX=MMAX,seconds=round(time.time()-t0,1),status={str(k):v for k,v in stat.items()},r_dist=dict(sorted(lens.items())),records=res)
json.dump(out,open('deep_B%d.json'%B,'w'),indent=1)
print(out['seconds'],out['status'],out['r_dist'])
for x in res:
    if x['status']!='closed' or len(eval(x['word']))>=4: print(x)
