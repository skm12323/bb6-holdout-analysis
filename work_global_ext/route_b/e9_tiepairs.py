"""Tie pairs (Lemma Q2): (n,n') odd type-a crossings, n'<n, v2(1+k_n+k_n')=n'-1 (k=tau/2).
A descending a-step from parameter n+1 to n'+1 followed by an odd a-return at X(n') is a non-descent
iff (n,n') is a tie pair.  Necessarily 2^(n'-1) <= 1+k_n+k_n'."""
from collections import Counter
from core import *
T=load(30000)
A=[n for n in range(4,30001) if T[n]['odd'] and T[n]['typ']=='a']
K={n:T[n]['tau']//2 for n in A}
cnt=Counter(); ex={}
for np_ in A:
    if np_>30: break
    for n in A:
        if n<=np_: continue
        if v2(1+K[n]+K[np_])==np_-1:
            cnt[np_]+=1
            ex.setdefault(np_,[]).append(n) if len(ex.get(np_,[]))<8 else None
print('odd type-a crossings n<=30:',[ (n,K[n]) for n in A if n<=30])
print('number of n<=30000 forming a tie pair with n\':',dict(cnt))
print('first partners:',ex)
