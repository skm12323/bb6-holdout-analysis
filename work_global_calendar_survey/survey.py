"""Survey canonical projected exits for many huge root parameters J (calendar prefix only)."""
import sys,random,json,time
from collections import Counter
sys.path.insert(0,'../work_global_calendar')
from calendar_oracle import Calendar
B=int(sys.argv[1]); N=int(sys.argv[2]); seed=int(sys.argv[3])
cal=Calendar(B); top=cal.boundary_pointer
random.seed(seed)
stat=Counter(); rlen=Counter(); words=Counter(); losses=Counter(); odd=[]
t0=time.time()
def J_sample(i):
    m=i%4
    if m==0: return random.randrange(5,top)                       # uniform
    if m==1: b=random.randrange(3,top.bit_length()-1); return random.randrange(1<<b,1<<(b+1))  # log-uniform
    if m==2: b=random.randrange(3,top.bit_length()-1); return (1<<b)+random.randrange(-64,65)  # near powers of 2
    b=random.randrange(3,top.bit_length()-2); return ((1<<b)*random.choice((3,5,7,9)))//4+random.randrange(-8,9)
for i in range(N):
    J=J_sample(i)
    if not 5<=J<top: continue
    try: r=cal.projected_epoch(J,limit=64)
    except AssertionError as e: r={'status':'non-descent/assert','word':[J]}
    stat[r['status']]+=1
    w=r.get('word',[])
    rlen[len(w)-1]+=1
    if r['status']=='closed':
        words[(tuple(x for x in w[1:]), r['types'])]+=1; losses[r['loss']]+=1
    if r['status']!='closed' or len(w)>=4: odd.append(dict(J=str(J),bits=J.bit_length(),**{k:(str(v) if k=='word' else v) for k,v in r.items()}))
out=dict(B=B,N=N,seed=seed,seconds=round(time.time()-t0,1),status=dict(stat),r_dist=dict(sorted(rlen.items())),
         loss_dist=dict(sorted(losses.items())),top_tails=[[str(k[0]),k[1],v] for k,v in words.most_common(25)],
         unusual=odd[:200],unusual_count=len(odd))
json.dump(out,open('survey_B%d_s%d.json'%(B,seed),'w'),indent=1)
print(json.dumps({k:out[k] for k in ('seconds','status','r_dist','loss_dist','unusual_count')}))
for u in odd[:15]: print(u)
