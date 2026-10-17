"""exp4 (Class B): the real top-map orbit of #1 from (3).  Checks Lemma RIGID's shape statements:
 - every top step with A odd: list length k; for k=2 (list (H,D)) check H+D=3N+3 and X=A+2b+3=6N+9-H;
 - the excursion bookkeeping: which odd-A steps are 'endgame a-returns' (2-lists) vs others;
 - closeness to halting: the odd part u of X (halting <=> u=1); minimum u over 2-lists and over k>=3.
"""
import sys
from collections import Counter
N=int(sys.argv[1]) if len(sys.argv)>1 else 200000
def v2(z): return (z&-z).bit_length()-1
L=[3]; cnt=Counter(); minu={2:None,3:None}; bad=0; ex2=[]
for n in range(N):
    A=L[0]; b=L[1] if len(L)>1 else 0; c=L[2] if len(L)>2 else 0
    assert sum(L)==3*n+3
    if A%2:
        k=len(L); X=A+2*b+3; u=X>>v2(X); kk=2 if k==2 else (3 if k>=3 else 1)
        cnt[kk]+=1
        if k==2:
            if not (A+b==3*n+3 and X==6*n+9-A): bad+=1
            if len(ex2)<6: ex2.append((n,A,b,X,v2(X),u))
        if kk in minu and (minu[kk] is None or u<minu[kk][0]): minu[kk]=(u,n,k)
    # top map
    S=L[3:]
    if A%2==0: L=[A+b+c+3]+S
    else:
        m=b+(A-3)//2; S=[c+(A+1)//2]+S
        assert (m+3)&(m+2)!=0, 'HALT'
        while m%2: S=[(m+3)//2]+S; m=(m-3)//2
        L=[m+4]+S
print('top steps:',N,' odd-A steps by list length (1 / 2 / >=3):',dict(cnt),' 2-list identity violations:',bad)
print('first 2-list odd states (N,H,D,X,v2X,u):',ex2)
print('min odd part u of X: 2-lists',minu[2],' lists>=3',minu[3])
