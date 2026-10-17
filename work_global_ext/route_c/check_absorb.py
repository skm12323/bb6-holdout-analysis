"""[B] check of the Absorption Lemma / Theorem RA on the phase-2 automaton tails:
for every 5<=m<N, the exit tail from (m, theta=2) has length
   1                      if X(m-1) is even,
   2 + r(J_F)             if X(m-1) is an odd type a (fire at m-1) or b (fire at m-2),
   1 + r(J_W) - t         if X(m-1) is an odd type c sitting after chain t of an epoch of parameter J_W.
Also checks sigma(C) = precision P_0 for the c case: m-1-eps(m-1) = J_W... (records min slack)."""
import sys
from collections import Counter
from fdata import lam_walk, small_full, v2
from sj import sym_beta
from tails import make_tail
N=int(sys.argv[1]) if len(sys.argv)>1 else 10**6; NS=400
LD=lam_walk(N+2); SM=small_full(NS)
typ=LD['typ']; tau=LD['tau']; odd=LD['odd']
tail,step=make_tail(LD)
cache={}
def r(J):
    if J not in cache: cache[J]=len(sym_beta(J,LD,SM,NS)['js'])-1
    return cache[J]
lastfire=None; cnt=Counter(); bad=[]
for m in range(5,N):
    n=m-1; t=chr(typ[n])
    if t=='a' and odd[n]: lastfire=(n,tau[n])
    w,ty,ok=tail(m,2)
    L=len(w)
    if not odd[n]: pred=1; kind='even'
    elif t=='a': pred=2+r(v2(3*tau[n]+4)); kind='A'
    elif t=='b': pred=2+r(v2(3*tau[n]+4)); kind='B'
    else:
        rho,sF=lastfire; JW=v2(3*sF+4); R=sym_beta(JW,LD,SM,NS)
        d=0; ds=[0]
        for tt in range(1,len(R['js'])):
            mm=R['js'][tt-1]-1; d+=1+(SM[mm]['tau'] if mm<NS else tau[mm]); ds.append(d)
        k=ds.index(tau[n]-sF)   # copied chain index t_W+1
        pred=1+(len(R['js'])-1)-(k-1); kind='C'
    cnt[kind]+=1
    if pred!=L or not ok: bad.append((m,kind,w,pred))
print(dict(cnt),'bad',len(bad),bad[:10])
