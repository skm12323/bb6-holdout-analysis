import math
def dlog2(t,N):
    """least k>=0 with 2^k = t mod N (gcd(2,N)=1), or None; plus order of 2."""
    t%=N; m=math.isqrt(N)+1; tab={}; cur=1
    for j in range(m):
        tab.setdefault(cur,j); cur=cur*2%N
    g=pow(pow(2,m,N),-1,N); y=t; ks=[]
    for i in range(m+1):
        if y in tab: ks.append(i*m+tab[y])
        if len(ks)>=1: break
        y=y*g%N
    return ks[0] if ks else None
