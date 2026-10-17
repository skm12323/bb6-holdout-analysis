"""[B] check: odd crossings are (a) fire pointers, (b) fire pointer+1 copying the fire, (c) a-returns of
epoch chain t whose copied chain is chain t+1 of S(J_F), with omega(n)=j_{t+1}, tau(n)-s_F = d_{t+1};
and the route-a recursion r(J) = 2+r(J_F) / 1+r(J_F)-t / 1 (even)."""
import sys
from collections import Counter
from fdata import lam_walk, small_full, v2
from sj import sym_beta
N=int(sys.argv[1]) if len(sys.argv)>1 else 10**6; NS=400
LD=lam_walk(N+2); SM=small_full(NS)
typ=LD['typ']; tau=LD['tau']; odd=LD['odd']; lA=LD['lA']; lY=LD['lY']
lastfire=None; cnt=Counter(); bad=0; cache={}
def S(J):
    if J not in cache: cache[J]=sym_beta(J,LD,SM,NS)
    return cache[J]
pos={}   # n -> (kind, J_F, t)
for n in range(4,N):
    t=chr(typ[n])
    if t=='a':
        # P=empty state at pointer n; odd <=> fire
        if odd[n]:
            lastfire=(n,tau[n]); cnt['a-odd']+=1; pos[n]=('A',v2(3*tau[n]+4),None)
        else: cnt['a-even']+=1
    elif t=='b':
        assert tau[n]==tau[n-1] and odd[n]==odd[n-1]
        if odd[n]:
            om=v2(lA[n]+3); assert om==v2(3*tau[n]+4); cnt['b-odd']+=1; pos[n]=('B',om,None)
    else:
        if not odd[n]: cnt['c-even']+=1; continue
        rho,sF=lastfire; JF=v2(3*sF+4); R=S(JF)
        om=v2(lA[n]+2*lY[n]+3); dd=tau[n]-sF
        # find chain index t+1 with d_{t+1}=dd
        js=R['js']; ok=False
        # recompute d's
        d=0; ds=[0]; j=JF
        for tt in range(1,len(js)):
            m=js[tt-1]-1; d+=1+(SM[m]['tau'] if m<NS else tau[m]); ds.append(d)
        if dd in ds:
            k=ds.index(dd); ok = (js[k]==om) and k>=1 and R['types'][k-1]=='a'
            pos[n]=('C',JF,k)
        if not ok: bad+=1
        else: cnt['c-odd ok']+=1
print(dict(cnt),'bad',bad)
# route-a recursion
rec=Counter(); badr=0
for J in range(5,N):
    R=S(J)
    if not R['types'] or R['types'][0]!='a': continue
    r=len(R['js'])-1; j1=R['js'][1]; n=j1-1
    if n<4 or n not in pos:
        # even crossing at j1-1 (or tiny): r should be 1
        if r==1: rec['even']+=1
        else: badr+=1
        continue
    kind,JF,t=pos[n]; rF=len(S(JF)['js'])-1
    pred = 2+rF if kind in 'AB' else 1+rF-t
    if pred==r: rec[kind]+=1
    else: badr+=1
print('route-a recursion',dict(rec),'bad',badr)
