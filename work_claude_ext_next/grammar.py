from functools import lru_cache
from collections import Counter
# word = tuple of letters; letter 'A','B' or ('C',subword)
@lru_cache(None)
def words(W):            # histories of weight W (ending in A)
    return tuple(p+('A',) for p in prefixes(W-2))
@lru_cache(None)
def prefixes(W):
    if W<0:return ()
    if W==0:return ((),)
    out=[]
    for p in prefixes(W-2): out+= [p+('A',),p+('B',)]
    for w2 in range(2,W-1,2):
        for sub in words(w2):
            for p in prefixes(W-2-w2): out.append(p+(('C',sub),))
    return tuple(out)
def phi_seq(w):
    d=1;seq=[]
    for L in w:
        if L=='A':d=3-d
        elif L=='B':d=d-1
        else:d=d+phi(L[1])-2
        seq.append(d)
    return seq
def phi(w):return phi_seq(w)[-1]
def show(w):return ''.join(L if isinstance(L,str) else 'C('+show(L[1])+')' for L in w)
def classify(w):
    s=phi_seq(w)
    if 2 in s[:-1]:return 'P2'+(' (A-SOURCE)' if w[0]=='A' else '')
    delta=s[-1]-1
    if delta==1:return 'F1'
    if delta==2:return 'AB2'
    return 'open G_%d'%delta
if __name__=='__main__':
    seen=set()
    for eps in range(3,16,2):
        ws=words(eps-1);cnt=Counter();opens=Counter()
        for w in ws:
            c=classify(w);cnt[c.split(' ')[0] if not c.startswith('open') else 'open']+=1
            if c.startswith('open'):opens[int(c.split('_')[1])]+=1
        new=sorted(set(opens)-seen);seen|=set(opens)
        print(eps,len(ws),dict(cnt),'open deltas',dict(sorted(opens.items())),'new',new)
        if eps<=11:
            for w in ws:
                if w[0]!='A':print('   ',show(w),phi_seq(w),classify(w))
