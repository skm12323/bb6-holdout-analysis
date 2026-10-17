"""[B] check of the route b/c reduction: for route b/c, S(J) from chain 1 on equals the exact integer walk
V(C,-1) from the real W-chain C at step tau(J-1), with Theta shifted by -1:  (j_C, 3 tau(J-1)+4, u_C)."""
import sys
from collections import Counter
from fdata import lam_walk, small_full, v2
from sj import sym_beta
from sfam import virtual_walk
N=int(sys.argv[1]) if len(sys.argv)>1 else 10**6; NS=400
LD=lam_walk(N+2); SM=small_full(NS)
cnt=Counter(); bad=[]
for J in range(5,N):
    n=J-1
    if not LD['odd'][n] or LD['typ'][n]==97: continue
    t=chr(LD['typ'][n]); T=LD['tau'][n]
    x=LD['lA'][n]+3 if t=='b' else LD['lA'][n]+2*LD['lY'][n]+3
    j=v2(x); W=virtual_walk(j,3*T+5-1,x>>j,SM)
    R=sym_beta(J,LD,SM,NS)
    cnt[t]+=1
    if W['word']!=R['js'][1:] or W['status']!='end': bad.append((J,t,W['word'],R['js']))
print(dict(cnt),'bad',len(bad),bad[:5])
