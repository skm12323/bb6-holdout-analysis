"""Tail length of the canonical exit after a deep first step, as a function of m only:
a-type first step -> state (j=m, theta=2); b-type -> (j=m, theta=0)  (projected_epoch automaton).
Uses calendar crossings at indices < m (small)."""
import sys,json,time
sys.path.insert(0,'../work_global_calendar')
from calendar_oracle import Calendar, val
M=int(sys.argv[1]); B=int(sys.argv[2])
cal=Calendar(B)
def tail(j,theta,limit=64):
    word=[]
    for _ in range(limit):
        row=cal.crossing(j-1);t=row['time'];kind=row['kind'];word.append(j)
        if not row['odd']: return word,'closed'
        if kind=='a':
            v=theta+3*(t//2)
            if v>0 and v.bit_length()<=j-2: nxt=1+val(v)
            else:
                rem=(v-(1<<(j-2)))%(1<<(j-1))
                if not rem: return word,'NT tie'
                nxt=1+val(rem)
            if not nxt<j: return word,'non-descent'
            theta=(3-theta)%(1<<nxt);j=nxt
        else:
            nxt=row['omega']
            if not nxt<j: return word,'non-descent'
            theta=(theta+3*t+3)%(1<<nxt);j=nxt
    return word,'limit'
t0=time.time(); first={}; bad=[]
for m in range(2,M+1):
    for typ,th in (('a',2),('b',0)):
        w,st=tail(m,th%(1<<m))
        if st!='closed': bad.append((m,typ,w,st))
        r=len(w)
        if r not in first: first[r]=(m,typ,w)
        if r>=4 and len(first.get('r4list',[]))<20: first.setdefault('r4list',[]).append((m,typ,w))
print("time %.0fs"%(time.time()-t0)); print({k:v for k,v in first.items() if k!='r4list'}); print("r>=4 examples:",first.get('r4list',[])[:20]); print("non-closed:",bad[:10],len(bad))
