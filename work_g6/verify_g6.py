r"""verify_g6.py -- checks for PROOF_G6.md (self-contained; reads nothing from D:\math_cc).
Usage: python -B verify_g6.py [N=3000]
 V1 [symbolic] Prop 3 algebra: exit fire on D_host, case (gap 1, j_last 2).
 V2 [symbolic] Prop 5 inequality 1+log2(3r^2+2) <= 4r+4 and the (b) step bound.
 V3 [Class-B]  concrete Phi_m, m<=N: canonical re-entry, dk = steps/2, dk>=1, dp>=2,
               all chains u>=3, dk(m) = K_{rho*} + e(m)/2, max e(m), max exit-fire j,
               j_D = 1+v2(3K+4) in every (gap1, j_last=2) exit.
"""
import sys
from fractions import Fraction as Fr
from math import log2
def v2(x): return (x & -x).bit_length()-1
def kappa(j):
    m=1<<j; return ((1<<(j-1))-2)*pow(3,-1,m)%m

# ---- V1: affine forms in (P, k, K, Ku) represented as dict of Fractions -----
def V1():
    # symbols: P (=2^p), k (host), K (universal k at rho*=m-3), X=2^m*u (= 9P+6k+4)
    def add(*fs):
        r={}
        for f in fs:
            for s,c in f.items(): r[s]=r.get(s,0)+Fr(c)
        return {s:c for s,c in r.items() if c!=0}
    def sc(f,c): return {s:Fr(c)*v for s,v in f.items()}
    X={'P':9,'k':6,'1':4}                 # 2^m u
    # level entry E_a = 2^a u ; rho=m-3: 2^rho u = X/8, E_{rho+1}=X/4
    Erho=sc(X,Fr(1,8)); Erho1=sc(X,Fr(1,4))
    Afire=add(sc(Erho,1), {'K':6,'1':1})        # A = 2^rho u + 6K+1
    x=add(Afire, sc(Erho,2), {'1':3})          # x = 3*2^rho u + 6K+4
    assert x==add(sc(Erho,3),{'K':6,'1':4})
    upp=sc(x,Fr(1,4))                           # j=2: u''
    Dpp=add(Erho1, sc(add(Afire,{'1':1}),Fr(1,2)))  # c+(A+1)/2
    A1=add(upp,{'1':1})
    A2=add(A1,upp,Dpp,{'1':3})                  # even step consuming u'', D''
    assert A2==add(sc(X,Fr(1,2)),{'K':6,'1':7}), A2   # = 2^{m-1}u + 6K+7
    Dh={'P':Fr(15,2),'k':3,'1':1}
    xD=add(A2,sc(Dh,2),{'1':3})
    assert xD=={'P':Fr(39,2),'k':9,'K':6,'1':14}, xD
    # mod 2^m reduction: 6k+4 = 2^m*(odd)  =>  9k+6 = 3/2(6k+4) = 3*2^{m-1}*odd
    # so 9k+6K+14 = 3*2^{m-1}*odd + 2(3K+4); spot-check on residues:
    for m in range(6,40):
        k=kappa(m)
        for K in range(1,3000,7):
            t=9*k+6*K+14; a=v2(3*K+4)
            if 1+a < m-1: assert v2(t)==1+a
    print('V1 ok: x_D = 39/2 P + 9k + 6K + 14, j_D = 1+v2(3K+4) when < m-1')

def V2():
    for r in range(2,10**6): assert 1+log2(3*r*r+2) <= 4*r+4
    f=lambda i: i-log2(i)**2-log2(6*i*i+5)
    assert all(f(i+1)>f(i) for i in range(16,10**6)) and f(20000)>0
    print('V2b ok: f(i)=i-log2(i)^2-log2(6i^2+5) increasing on [16,1e6], f(20000)=%.1f>0 (df>0 for i>=16 analytically)'%f(20000))
    print('V2 ok: 1+log2(3r^2+2) <= 4r+4 for 2<=r<1e6 (and trivially beyond: LHS ~ 2log2 r)')

def phi(m, p=None):
    k=kappa(m); p=p or m+60; P=1<<p
    x0=9*P+6*k+4; assert v2(x0)==m
    u=x0>>m; A=u+1
    Q=[(u<<a,('R',a)) for a in range(m-1)]+[(15*P//2+3*k+1,('D',))]+[(3*(1<<e)*P,('T',e)) for e in range(2,40)]
    ev=[]; steps=0; minu=None
    while True:
        b,lb=Q[0]; c,lc=Q[1]
        steps+=1
        if A%2==0:
            A=A+b+c+3; Q=Q[2:]; continue
        x=A+2*b+3; jj=v2(x); uu=x>>jj
        assert uu>=3, ('HALT-like chain', m)
        if lb[0]=='T':
            rest=Q[2:]
            assert all(l[0]=='T' for _,l in rest)        # pure leftovers
            assert c==3*(1<<lc[1])*P and lc[1]==lb[1]+1
            dk6=x-9*(1<<lb[1])*P-4-6*k; assert dk6%6==0
            D2=c+(A+1)//2; assert D2==15*(1<<lb[1])*P//2+3*(k+dk6//6)+1   # canonical D'
            return dk6//6, lb[1], steps, ev
        ev.append((lb,jj,steps))
        Q=[(uu<<a,('M',)) for a in range(jj-1)]+[(c+(A+1)//2,('d',))]+Q[2:]
        A=uu+1

def V3(N):
    # universal sequence (needs table for small j, built on the fly)
    tab={}
    def T(j):
        if j not in tab: dk,dp,_,_=phi(j); tab[j]=(dk,dp)
        return tab[j]
    kat={}; p,k=4,1
    while p<N+5:
        kat[p]=k; jj=1+v2(3*k+2); dk,dp=T(jj); k+=dk; p+=dp
    maxe=0; maxjD=0; nD=0; okD=0; maxdkr=0
    for m in range(1,N):
        dk,dp,s,ev=phi(m)
        assert s==2*dk and dk>=1 and dp>=2, m              # Prop 1
        Rs=[e for e in ev if e[0][0]=='R']
        if Rs:
            rl=Rs[-1][0][1]; e=s-2*kat[rl]+0
            # steps before the last level fire = 2*K_{rl}  (sum identity); e = remaining steps
            assert e>=0; maxe=max(maxe,e)
            for i,(lb,jj,st) in enumerate(ev):
                if lb[0]=='D': maxjD=max(maxjD,jj)
            if m-2-rl==1 and Rs[-1][1]==2:
                nD+=1
                jD=[jj for lb,jj,st in ev if lb[0]=='D'][0]
                okD+= jD==1+v2(3*kat[rl]+4)
        maxdkr=max(maxdkr,dk/m)
        if dk>m: print('dk>m at',m)
    print('V3 ok (m<%d): canonical re-entry, s=2dk, dk>=1, dp>=2, all u>=3;'%N,
          'max exit cost e=%d, max D-fire j=%d, j_D formula %d/%d, max dk/m=%.3f'%(maxe,maxjD,okD,nD,maxdkr))


# ---------------- V4/V5: closure section (symbolic universal walker, generic odd U) -------------
WG=256
def _v2(x): return 10**9 if x==0 else (x&-x).bit_length()-1
def walker(N, on_chain, on_cross):
    """Level process A=U+1, queue 2^a U (a>=0), values (C*U+L)/2^WG, U a generic odd integer.
    Every decision is made only when it is the same for every odd U; else raises."""
    one=1<<WG; A=(one,one); pushed=[]; i=0; s=0; seen=set()
    while i<=N:
        if len(pushed)>=2: b,c=pushed[0],pushed[1]; lb=lc=None
        elif len(pushed)==1: b=pushed[0]; c=(one<<i,0); lb=None; lc=i
        else: b=(one<<i,0); c=(one<<(i+1),0); lb=i; lc=i+1
        for l in (lb,lc):
            if l is not None and l not in seen: seen.add(l); on_cross(l,s,A,pushed)
        a,bb=_v2(A[0]),_v2(A[1]); assert min(a,bb)>=WG
        if ((a==WG)+(bb==WG))%2==0:
            A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3*one); newp=[]
        else:
            x=(A[0]+2*b[0],A[1]+2*b[1]+3*one); vc,vl=_v2(x[0]),_v2(x[1])
            assert vc!=vl, ('TIE',i,s)
            j=min(vc,vl)-WG
            assert x[0]>0 and x[1]>0
            on_chain(i,s,x,j,lb)
            u=(x[0]>>j,x[1]>>j)
            D=(c[0]+A[0]//2,c[1]+(A[1]+one)//2)
            newp=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[D]; A=(u[0],u[1]+one)
        k=len(pushed)
        if k>=2: pushed=pushed[2:]
        else: i+=2-k; pushed=[]
        pushed=newp+pushed; s+=1

def V4(N):
    from collections import Counter
    types=Counter(); first={}; st={'maxdef':0,'maxlam':0.0,'minmarg':10**9,'cltl':0,'lvl':[]}
    def cross(n,s,A,P):
        key=(Fr(A[0],1<<(WG+n)),tuple(Fr(p[0],1<<(WG+n)) for p in P)); types[key]+=1; first.setdefault(key,n)
    def chain(i,s,x,j,lb):
        vc,vl=_v2(x[0])-WG,_v2(x[1])-WG
        if vc<vl: st['cltl']+=1
        st['maxdef']=max(st['maxdef'],i-vc)
        if s>10: st['maxlam']=max(st['maxlam'],(x[1]>>WG)/(3*s+1))
        if i>40: st['minmarg']=min(st['minmarg'],vc-vl)
        if lb is not None:
            assert x[0]==3<<(WG+lb) and ((x[1]>>WG)-4)%6==0     # I(rho): x = 3*2^rho U + 6k+4
            st['lvl'].append((lb,((x[1]>>WG)-4)//6,j))
    walker(N,chain,cross)
    print('V4 ok (walker to level index %d, generic odd U): tie-free; every chain has j=v2(small) (cases v2(scale)<v2(small): %d);'%(N,st['cltl']))
    print('    max deficit i-v2(scale)=%d, max small_x/(3s+1)=%.4f, min margin(i>40)=%d'%(st['maxdef'],st['maxlam'],st['minmarg']))
    for k_,v in sorted(types.items(),key=lambda kv:first[kv[0]]): print('    crossing shape',k_,'count',v,'first n',first[k_])
    return st['lvl']

def V5(lvl,N):
    # cross-check walker level fires against concrete per-m table (Class-C)
    tab={}
    def T(j):
        if j not in tab: dk,dp,_,_=phi(j); tab[j]=(dk,dp)
        return tab[j]
    p,k=4,1; seq=[]
    while p<N-10: seq.append((p,k,1+v2(3*k+2))); dk,dp=T(1+v2(3*k+2)); k+=dk; p+=dp
    w=[t for t in lvl if t[0]>=4 and t[0]<N-10]
    assert w==seq, 'mismatch'
    print('V5 ok: %d level fires of the walker = universal (p,k,j) built from concrete Phi_m table'%len(seq))

# ---------------- V6: formal tagged pair map F (section 5) --------------------------------------
def F_walk(N, on_state=None):
    """Formal map F on states (A; P; i): A=(cA,lA), P = finite list of tagged pairs (c,l,tag),
    original suffix E_a=(2^a,0) for a>=i.  Integer components only.  Decisions:
      parity(A) := (cA+lA) mod 2                       [exact for every odd U]
      chain: x=(cA+2cb, lA+2lb+3); REQUIRE v2(lx)<v2(cx) (margin-safe), cA even, lA odd;
             j=v2(lx); u=(cx>>j, lx>>j); push u*2^t (t<j-1) then D=(cc+cA/2, lc+(lA+1)/2); A=u+(0,1)
    Returns stats; raises AssertionError if a requirement fails (= F undefined there)."""
    A=(1,1); P=[]; i=0; s=0
    st={'chains':0,'level':0,'mass':0,'Iviol':0,'lvlfires':[],'maxstall':0}
    last_i=0; last_move=0
    while i<=N:
        # mass identities over head + pushed only
        assert A[0]+sum(p[0] for p in P)==1<<i and A[1]+sum(p[1] for p in P)==3*s+1
        assert A[0]>0 and A[1]>0 and all(p[0]>0 and p[1]>0 for p in P)
        st['mass']+=1
        if i>=1:
            d=i-min(_v2(v) for v in [A[0]]+[p[0] for p in P])
            st['maxdef']=max(st.get('maxdef',0),d)
            if i>=16: st['hyp_ok']=st.get('hyp_ok',True) and d<=(i.bit_length()-1)**2 and s<=i*i
        ents=[(p[0],p[1],p[2]) for p in P[:2]]
        a=i
        while len(ents)<2: ents.append((1<<a,0,('E',a))); a+=1
        (cb,lb,tb),(cc,lc,tc)=ents
        if (A[0]+A[1])%2==0:
            A=(A[0]+cb+cc,A[1]+lb+lc+3); newp=[]
        else:
            cx,lx=A[0]+2*cb,A[1]+2*lb+3
            vc,vl=_v2(cx),_v2(lx)
            assert vl<vc, ('margin',i,s)
            assert A[0]%2==0 and A[1]%2==1, ('parity invariant',i,s)
            j=vl; u=(cx>>j,lx>>j)
            assert u[0]%2==0 and u[0]>=2 and u[1]%2==1        # u = cU+l >= 2U+1
            st['chains']+=1
            if tb[0]=='E':
                st['level']+=1
                assert len(P)==0 and cx==3<<tb[1] and (lx-4)%6==0 and s%2==0 and lx==3*s+4   # I(rho)
                st['lvlfires'].append((tb[1],s//2,j))
            newp=[(u[0]<<t,u[1]<<t,('M',s)) for t in range(j-1)]+[(cc+A[0]//2,lc+(A[1]+1)//2,('D',s))]
            A=(u[0],u[1]+1)
        k=len(P)
        if k>=2: P=P[2:]
        else: i+=2-k; P=[]
        P=newp+P; s+=1
        if i!=last_i: st['maxstall']=max(st['maxstall'],s-last_move); last_i=i; last_move=s
    return st

def V6(N):
    st=F_walk(N)
    print('V6 ok (formal map F to i=%d): integral components, positivity, mass identities at %d states,'%(N,st['mass']))
    print('    parity invariant cA even & lA odd at all %d chains, strict margin, u=cU+l with c>=2 even, l odd;'%st['chains'])
    print('    %d level fires all clean (P empty) with x=3*2^rho U+3s+4, s even; max steps without pointer advance=%d'%(st['level'],st['maxstall']))
    print('    max deficit over ALL head/pushed values = %d; (M1p) d<=floor(log2 i)^2 and (M2p) s<=i^2 hold at all states i>=16: %s'%(st['maxdef'],st['hyp_ok']))
    return st['lvlfires']

if __name__=='__main__':
    N=int(sys.argv[1]) if len(sys.argv)>1 else 3000
    V1(); V2(); V3(N)
    M=int(sys.argv[2]) if len(sys.argv)>2 else 20000
    lv=V4(M); V5(lv,M)
    lv6=V6(M); assert [t for t in lv6 if t[0]>=4]==[t for t in lv if t[0]>=4]
    print('V6/V4 level-fire streams identical')
