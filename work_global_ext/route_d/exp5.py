"""exp5 (Class B/C): arithmetic of the halting set at a first EXACT tie, synthetic late-stage states.
At the exact tie x=2^m(gamma,mu) (gamma,mu odd) the excursion E(w,.) with U=3w halts at that chain iff
3w*gamma+mu = 2^k.  Solvable iff mu mod 3gamma lies in <2>; minimal w from the least such k with 2^k>mu.
Also: density/transfer check (Lemma DENS): runs of U and U*=U+2^B V (B large, 3|U*) coincide."""
import sys, random, math, collections
import tielab as T
random.seed(5)
L=T.Lab(400)
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
def order2(N):
    m=math.isqrt(N)+1; tab={}; cur=1
    for j in range(1,m+1):
        cur=cur*2%N; tab.setdefault(cur,j)
    g=pow(pow(2,m,N),-1,N); y=g; best=None
    for i in range(1,m+2):
        # 2^(i*m - j)=1 ? search 2^j = 2^(i m)  -> use direct: find smallest k with 2^k=1 by scanning multiples
        pass
    # fallback: smallest k>0 with 2^k=1 via dlog of 1 shifted
    k=dlog2(2,N)   # 2^k = 2 with k>=0 -> k=1 trivially; not useful
    return None
stat=collections.Counter(); wmins=[]; dens_bad=0; dens_n=0; got=0
while got<300:
    J,jt,u,D,d=T.late_state(random)
    r=T.symstate(L,jt,u,D)
    if r['st']!='EXACT': continue
    got+=1
    x=r['ch'][-1]['x']; mm=T.v2(x[0]); gam=x[0]>>mm; mu=x[1]>>mm
    N3=3*gam
    if mu%3==0: stat['3|mu: no halting w']+=1; continue
    if math.gcd(mu,gam)>1: stat['gcd(mu,gamma)>1: no halting w']+=1; continue
    k=dlog2(mu,N3)
    if k is None: stat['mu not in <2> mod 3gamma: no halting w']+=1; continue
    # make 2^k>mu by adding the period: period = least p>0 with 2^p=1; find via dlog of 1 after k... use dlog(2^-1)
    if (1<<k)<=mu:
        p=dlog2(pow(2,-1,N3),N3)+1    # 2^(p-1)=2^-1 => 2^p=1
        while (1<<k)<=mu: k+=p
    w=((1<<k)-mu)//N3
    assert w*N3+mu==(1<<k) and w%2==1
    # confirm with the real recursion: E-state with U=3w halts at the tie chain
    rr=T.realstate(L,3*w,jt,u,D)
    assert rr['st']=='HALT' and len(rr['ch'])==len(r['ch']), rr['st']
    stat['solvable']+=1; wmins.append((J, gam.bit_length(), w.bit_length()))
    # density check on a few U
for it in range(400):
    J=random.randint(20,40); jt=random.randint(5,12); m=jt+1
    lo=(1<<J)>>m; g=random.randrange(lo,2*lo)|1; ax=g<<m
    if not ((1<<J)<=ax<(1<<(J+1))): continue
    bx=(random.randrange(1,max(2,12*J*J>>jt))|1)<<jt
    u=(ax>>jt,bx>>jt); D=((1<<J)-ax//2, random.randint(0,12*J*J))
    for _ in range(20):
        U=random.randrange(1,1<<40)|1
        B=400; V=next(V for V in (1,2,3) if (U+(V<<B))%3==0); Us=U+(V<<B)
        a=T.realstate(L,U,jt,u,D,halt=False); b=T.realstate(L,Us,jt,u,D,halt=False); dens_n+=1
        if [(c[0],c[2]) for c in a['ch']]!=[(c[0],c[2]) for c in b['ch']] or a['st']!=b['st']: dens_bad+=1
print('first exact ties analysed: 300 ->',dict(stat))
if wmins:
    print('solvable cases: bit-length of minimal halting w vs bit-length of gamma (J, |gamma|, |w_min|), first 25:',wmins[:25])
    print('median |w_min| = %d bits, min = %d bits, max = %d bits'%(sorted(z[2] for z in wmins)[len(wmins)//2],min(z[2] for z in wmins),max(z[2] for z in wmins)))
print('DENS transfer check: %d (U, U*=U+2^400 V, 3|U*) pairs, mismatching chain sequences: %d'%(dens_n,dens_bad))
