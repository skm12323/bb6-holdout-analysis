r"""verify_m.py -- checks for PROOF_M.md (self-contained; reads nothing else).
Usage:  python -B verify_m.py [N1=20000] [NB=10000000]

 V1 [Class-B, full pair map F, i <= N1]  checks every Class-A lemma of PROOF_M sections 2-3 on
    the actual walk: replay (call) structure, return state = image of X(j-1) followed by D,
    crossings only at top-level states, crossing types a/b/c and eps formula,
    sigma recursion sigma_{t+1} = sigma_t - 1 - eps(j_t - 1), v2(c_D) = sigma - 1,
    deficit bound Delta <= i - sigma_t + j_t inside the epoch, Delta = 0 at P = empty.
 V2 [Class-B, lambda-only certificate, i <= NB]  the walker of PROOF_M section 4: it runs only the
    small parts, recomputes sigma by the proved recursion and checks j < sigma at every
    top-level chain.  By Theorem 4.1 this certifies that F is defined for i <= NB.
    Also records r (exit chains / epoch), eps, Gamma, deficit bound, s/i, and whether the exit
    pattern is a function of J = j_0 alone (Class-C observation).
 V3 [elementary inequalities used in section 5]  checked on a range + monotone tail argument.
"""
import sys
from math import log2

def v2(x): return (x & -x).bit_length()-1

# ----------------------------------------------------------------------------------------------
# V1: full pair walk with call/return bookkeeping
# ----------------------------------------------------------------------------------------------
def V1(N1):
    A=(1,1); P=[]; i=0; s=0
    Xst={}; Xt={}; Xtyp={}; Xeps={}
    calls=[]            # end times (last call step) of active calls
    pending={}          # return time -> (u, j, D, sigma, n)
    cur=None            # current top-level chain data: dict(sig, j)
    ep=None; nchk=0; ndef=0; nret=0
    while i<=N1:
        while calls and calls[-1]<s: calls.pop()
        top=not calls
        # ---- return-state check (Lemma 2.3) ----
        if s in pending:
            u,j,D,sg,n=pending.pop(s); nret+=1
            assert top
            XA,XP,Xi=Xst[n]
            img=lambda v:(v[0]*u[0], v[0]*u[1]+v[1])
            assert A==img(XA)
            exp=[img(p) for p in XP]+[(u[0]<<a,u[1]<<a) for a in range(Xi,j-1)]+[D]
            assert [(p[0],p[1]) for p in P]==exp, ('return image',s)
            if Xtyp[n]=='a': assert len(P)==1 and v2(A[0])==sg-1
        # ---- deficit ----
        if i>=1:
            d=i-min(v2(v) for v in [A[0]]+[p[0] for p in P])
            if not P: assert d==0
            elif cur is not None:
                assert d<=i-cur['sig']+cur['j'], ('deficit bound',s,i,d)
                ndef+=1
        ents=[(p[0],p[1],p[2]) for p in P[:2]]; a=i
        while len(ents)<2: ents.append((1<<a,0,('E',a))); a+=1
        (cb,lb,tb),(cc,lc,tc)=ents
        # ---- crossings (Lemma 2.4) ----
        for t in (tb,tc):
            if t[0]=='E' and t[1] not in Xt:
                n=t[1]; Xt[n]=s; assert top, 'crossing inside a call'
                if n<=400: Xst[n]=(A,[(p[0],p[1]) for p in P],i)
                if not P and i==n: typ='a'
                elif not P: typ='b'; assert i==n-1
                else: typ='c'; assert len(P)==1 and P[0][2][0]=='D' and i==n
                eps=n-v2(A[0]); Xtyp[n]=typ; Xeps[n]=eps
                assert eps==(0 if typ=='a' else 1 if typ=='b' else i-cur['sig']+1)
        if (A[0]+A[1])%2==0:
            A=(A[0]+cb+cc,A[1]+lb+lc+3); newp=[]
        else:
            cx,lx=A[0]+2*cb,A[1]+2*lb+3
            vc,vl=v2(cx),v2(lx)
            assert vl<vc and A[0]%2==0
            j=vl; u=(cx>>j,lx>>j)
            D=(cc+A[0]//2,lc+(A[1]+1)//2)
            if top:
                if not P:                   # level fire
                    assert tb==('E',i) and vc==i
                    ep={'rho':i,'sig':[vc],'typ':[]}
                else:                       # exit chain: sigma recursion (Lemma 3.1)
                    jp=cur['j']; assert vc==cur['sig']-1-Xeps[jp-1], ('sigma',s)
                    ep['sig'].append(vc)
                assert j<i                  # E_{j-1} already read
                cur={'sig':vc,'j':j}; nchk+=1
                pending[s+1+Xt[j-1]]=(u,j,D,vc,j-1)
                assert v2(D[0])>=vc-1
            T=Xt[j-1]
            if T>0: calls.append(s+T)
            newp=[(u[0]<<t,u[1]<<t,('M',s)) for t in range(j-1)]+[(D[0],D[1],('D',s))]
            A=(u[0],u[1]+1)
        k=len(P)
        if k>=2: P=P[2:]
        else: i+=2-k; P=[]
        P=newp+P; s+=1
        if not P and not calls: cur=None
    print('V1 ok (full pair map, i<=%d, %d steps): %d top-level chains, %d return states = image of X(j-1)+[D],'%(N1,s,nchk,nret))
    print('    sigma recursion, crossing types/eps formula, crossings only top-level, deficit bound at %d states'%ndef)

# ----------------------------------------------------------------------------------------------
# V2: lambda-only certificate walker
# ----------------------------------------------------------------------------------------------
CAP=4096
def V2(NB, verbose=True):
    lA=1; S=[]; i=0; s=0
    Xt=[None]*CAP; Xeps=[0]*CAP; Xpar=[0]*CAP
    calls=[]; sig_last=None; jl=None
    st=dict(epochs=0,rmax=0,G=0,epsmax=0,defb=0,sratio=0.0,minmarg=10**9,jmax=0,maxlen=0)
    rdist={}; pat={}
    ep_j=[]; ep_rho=0; ep_s=0; ep_typ=''
    first=True
    def close():
        if not ep_j: return
        r=len(ep_j)-1; rdist[r]=rdist.get(r,0)+1; st['rmax']=max(st['rmax'],r)
        st['G']=max(st['G'],ep_rho-sig_last)
        pat.setdefault(ep_j[0],set()).add((tuple(ep_j),ep_typ))
    while i<=NB or S or calls:
        while calls and calls[-1]<s: calls.pop()
        k=len(S)
        if i>NB and not S and not calls: break
        if k>=2: lb=S[-1]; lc=S[-2]; nb=nc=None
        elif k==1: lb=S[-1]; lc=0; nb=None; nc=i
        else: lb=lc=0; nb=i; nc=i+1
        for n in (nb,nc):
            if n is not None and n<CAP and Xt[n] is None:
                assert not calls
                Xt[n]=s
                if k==0 and i==n: e=0
                elif k==0: e=1
                else: e=n-(sig_last-1)
                Xeps[n]=e; st['epsmax']=max(st['epsmax'],e)
            elif n is not None and n>=CAP and k==1:
                st['epsmax']=max(st['epsmax'],n-(sig_last-1))
        if i>=16 and s>i*i: raise AssertionError('s>i^2')
        if i>=1: st['sratio']=max(st['sratio'],s/i)
        par=(lA+(1 if first else 0))&1
        if par==0:
            lA=lA+lb+lc+3; push=None
        else:
            lx=lA+2*lb+3; j=v2(lx); u=lx>>j
            if not calls:                       # top-level chain
                if k==0:
                    close(); ep_j=[j]; ep_rho=i; ep_s=s; sg=i; ep_typ=''
                    st['epochs']+=1
                else:
                    sg=sig_last-1-Xeps[jl-1]; ep_j.append(j)
                assert j<sg, ('MARGIN FAILS',i,s,j,sg)
                st['minmarg']=min(st['minmarg'],sg-j) if i>64 else st['minmarg']
                # deficit bound during this call: i - sigma + j  (pointer after the chain read)
                ia=i+(2 if k==0 else (1 if k==1 else 0))
                st['defb']=max(st['defb'],ia-sg+j)
                sig_last=sg; jl=j
            assert j-1<CAP and Xt[j-1] is not None
            T=Xt[j-1]
            if not calls: ep_typ+=('a' if Xeps[j-1]==0 else 'b' if Xeps[j-1]==1 else 'c')
            if T>0: calls.append(s+T)
            st['jmax']=max(st['jmax'],j)
            push=(u,j,lc+(lA+1)//2); lA=u+1
        if k>=2: del S[-2:]
        else: i+=2-k; S.clear()
        if push:
            u,j,D=push; S.append(D)
            for t in range(j-2,-1,-1): S.append(u<<t)
        s+=1; first=False
    close()
    func=all(len(v)==1 for v in pat.values())
    if verbose:
        print('V2 ok (lambda certificate, i<=%d, %d steps): margin j<sigma at every top-level chain;'%(NB,s))
        print('    epochs=%d, r distribution %s, max Gamma=%d, max eps=%d, max (i-sigma+j)=%d, max j=%d,'%(
              st['epochs'],sorted(rdist.items()),st['G'],st['epsmax'],st['defb'],st['jmax']))
        print('    max s/i=%.4f, min (sigma-j) for i>64 = %d; exit pattern a function of J alone: %s'%(st['sratio'],st['minmarg'],func))
        for J in sorted(pat): print('      J=%2d  %s'%(J,sorted(pat[J])))
    return st,rdist,pat

# ----------------------------------------------------------------------------------------------
# V3: elementary inequalities of section 5
# ----------------------------------------------------------------------------------------------
def V3(NB):
    lg=log2
    L=lambda r: lg(r)**2                 # (EL) bound on exit chains per epoch
    g=lambda r: 2*lg(r)+4                # bound on every top-level j in the epoch
    E=lambda r: max(7.0, g(r)/4)         # bound on eps at indices < g
    f={'I1': lambda r: r-L(r)*(1+E(r))-g(r),            # margin: sigma_t > j_t
       'I2': lambda r: r/4-3-L(r)*(2+E(r)),             # eps(n) <= n/4 for crossings in the epoch
       'I3': lambda r: 2*r-(L(r)+1)*(1+g(r)**2),        # tau(n) <= n^2 for n in the epoch
       'I4': lambda r: lg(r)**3-2-L(r)*(2+E(r))-g(r)}  # deficit Delta <= log2(i)^3
    # analytic residuals (PROOF_M section 5): x=log2 rho, L->x^2, E=x/2+1, g=2x+4
    from math import log
    x0=log2(1e6); assert x0>12 and 4/x0<log(2)
    P1=lambda x:0.5*x**3+2*x*x+2*x+4; P2=lambda x:2*x**3+12*x*x+12; P3=lambda x:0.5*(x*x+1)*(4*x*x+16*x+17)
    R4=lambda x:0.5*x**3-3*x*x-2*x-6
    assert P1(x0)<2**x0 and P2(x0)<2**x0 and P3(x0)<2**x0 and R4(10)>0
    print('V3 analytic: at x0=log2(1e6): P1=%.0f P2=%.0f P3=%.0f < 2^x0=1e6; 4/x0<ln2; R4(10)=%.0f>0'%(P1(x0),P2(x0),P3(x0),R4(10)))
    r=float(NB); ok=True
    while r<1e300:
        for k in f: ok&= f[k](r)>0 and f[k](r*1.001)>f[k](r)
        r*=1.001
    print('V3 ok: (I1)-(I4) hold and increase along a 0.1%%-geometric grid of [%d,1e300]; values at NB: %s'%(NB,
          ', '.join('%s=%.0f'%(k,f[k](NB)) for k in f)))
    assert ok

# ----------------------------------------------------------------------------------------------
# V4: symbolic exit per J (PROOF_M section 6).  Top-level small parts are affine a*lu+b in the
#     odd symbol lu = (3 s_0 + 4)/2^J of the level fire; W-crossing data X(n), n < J, are concrete.
# ----------------------------------------------------------------------------------------------
def Xdata(NX, cb=None, SMALL=4000):
    """crossing data of the universal walk for n < NX: (type, head pair, Y pair or None, eps).
    Stores n < SMALL; calls cb(n, data) for every n < NX as soon as X(n) is reached."""
    A=(1,1); P=[]; i=0; s=0; X={}; seen=-1
    while seen<NX-1:
        ents=[(p[0],p[1]) for p in P[:2]]; a=i
        while len(ents)<2: ents.append((1<<a,0)); a+=1
        (cb_,lb),(cc,lc)=ents
        k=len(P)
        for n in ([i] if k==1 else [i,i+1] if k==0 else []):
            if n>seen and n<NX:
                seen=n
                if k==0 and i==n: d=('a',A,None,0)
                elif k==0: d=('b',A,(1<<(n-1),0),1)
                else: d=('c',A,P[0],n-v2(A[0]))
                if n<SMALL: X[n]=d
                if cb: cb(n,d)
        if (A[0]+A[1])%2==0:
            A=(A[0]+cb_+cc,A[1]+lb+lc+3); newp=[]
        else:
            cx,lx=A[0]+2*cb_,A[1]+2*lb+3; vc,vl=v2(cx),v2(lx); assert vl<vc and A[0]%2==0
            j=vl; u=(cx>>j,lx>>j)
            newp=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[(cc+A[0]//2,lc+(A[1]+1)//2)]
            A=(u[0],u[1]+1)
        if k>=2: P=P[2:]
        else: i+=2-k; P=[]
        P=newp+P; s+=1
    return X

def sym_exit(J,X,first=None):
    INF=10**18
    vv=lambda z: INF if z==0 else v2(z)
    js=[J]; typs=''; G=0
    u=(1,0); D=(1<<(J-1),-1); j=J
    for t in range(60):
        n=j-1; typ,(cH,lH),Y,eps=(first if (t==0 and first is not None) else X[n]); typs+=typ
        H=(cH*u[0], cH*u[1]+lH)
        if Y is not None: Yv=(Y[0]*u[0], Y[0]*u[1]+Y[1])
        if (H[0]+H[1])%2==0:
            return tuple(js),typs,len(js)-1,G
        G+=1+eps
        b=D if typ=='a' else Yv
        x=(H[0]+2*b[0], H[1]+2*b[1]+3)
        va,vb=vv(x[0]),vv(x[1])
        if not vb<va: return ('TIE',J,t)
        assert H[0]%2==0 and H[1]%2==1
        j=vb; u=(x[0]>>j, x[1]>>j); assert u[0]<<j==x[0] and u[1]<<j==x[1]
        Dn=(H[0]//2,(H[1]+1)//2)
        D=Dn if typ=='a' else (D[0]+Dn[0],D[1]+Dn[1])
        js.append(j)
        if j-1 not in X: return ('NODATA',J,j)
    return ('LONG',J)

def V4(JMAX, emp=None):
    from collections import Counter
    rc=Counter(); bad=[]; G=[0,0]; pats={}; X={}
    def cb(n,d):
        if n<4000: X[n]=d
        J=n+1                                   # exit after a level fire with parameter J uses X(J-1)
        res=sym_exit(J,X,first=d)
        if isinstance(res[0],str): bad.append(res); return
        js,typs,r,g=res; rc[r]+=1; G[0]=max(G[0],g); G[1]=max(G[1],max(js[1:],default=0))
        if J<400: pats[J]=(js,typs)
    Xdata(JMAX-1, cb)
    Gm=G[0]
    print('V4 symbolic exits for 1<=J<%d: undecided/long: %d, r distribution %s, max Gamma %d, max exit j %d'%(JMAX,len(bad),sorted(rc.items()),Gm,G[1]))
    if bad: print('    first problems:',bad[:10])
    if emp:
        for J,ps in emp.items():
            assert len(ps)==1 and next(iter(ps))==pats[J], ('V2/V4 mismatch',J)
        print('    V4 patterns = V2 empirical patterns for all J observed in V2 (J<=%d)'%max(emp))
    return bad,rc

if __name__=='__main__':
    N1=int(sys.argv[1]) if len(sys.argv)>1 else 20000
    NB=int(sys.argv[2]) if len(sys.argv)>2 else 10**7
    JM=int(sys.argv[3]) if len(sys.argv)>3 else 30000
    V1(N1)
    st,_,pat=V2(NB)
    V3(10**6)
    V4(JM, emp=pat)
