"""example.py (Class B): an explicit mass-consistent late-stage state with a first EXACT tie and an odd w
for which the list with U=3w HALTS -- confirmed by the brute-force integer top map (work_r1 RULES section 5)."""
import random, math
import tielab as T
from exp5_helpers import dlog2
L=T.Lab(200); rnd=random.Random(2024)
best=None
for it in range(400000):
    J,jt,u,D,d=T.late_state(rnd,Jr=(16,22),jr=(5,9),hs=(1,1,2))
    r=T.symstate(L,jt,u,D)
    if r['st']!='EXACT': continue
    x=r['ch'][-1]['x']; m=T.v2(x[0]); g=x[0]>>m; mu=x[1]>>m; N3=3*g
    if mu%3==0 or math.gcd(mu,g)>1: continue
    k=dlog2(mu,N3)
    if k is None: continue
    if (1<<k)<=mu: continue
    w=((1<<k)-mu)//N3
    if best is None or w<best[0]: best=(w,J,jt,u,D,d,r,m,g,mu,k)
    if w.bit_length()<60: break
w,J,jt,u,D,d,r,m,g,mu,k=best
print('state: J=%d jt=%d u=%s D=%s d=%d'%(J,jt,u,D,d))
print('S* chains:',[(c['t'],c['typ'],c['x'],c['kind']) for c in r['ch']])
print('exact tie: m=%d gamma=%d mu=%d ; 3w*gamma+mu=2^%d with w=%d (%d bits)'%(m,g,mu,k,w,w.bit_length()))
U=3*w; Lst=T.statelist(U,jt,u,D)
res=T.toprun(list(Lst))
print('brute-force integer top map on the list (length %d):'%len(Lst),res['st'],'after',res['steps'],'top steps; halting list =',res.get('L'))
H,Dd=res['L'][0],res['L'][1]; print('halting list is a 2-list:',len(res['L'])==2,' H+2D+3 = 2^%d'%T.v2(H+2*Dd+3), (H+2*Dd+3)&(H+2*Dd+2)==0)
# neighbours do not halt
print('U=3(w+2):',T.toprun(T.statelist(3*(w+2),jt,u,D))['st'],'  U=3(w-2):',T.toprun(T.statelist(3*(w-2),jt,u,D))['st'])
