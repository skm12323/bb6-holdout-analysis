r"""verify_el.py -- checks for PROOF_EL.md.   Usage:  python -B verify_el.py [NB=1000000] [NCHK=20000] [L2=1]

Reads no files; imports ../work_m/verify_m.py READ-ONLY (only for the cross-check E2).
Notation as in PROOF_EL.md: theta(chain) = (3s+5) mod 2^j ; integer representative th~ by the rules
    fire: 1 ;  a-step: 3 - th ;  b/c-step (copy of W's chain at step tau(n)): th~_W + th - 2.

 E1 [Class-B, real lambda walk, i <= NB]  every top-level chain: fire has 3s+4 = 0 mod 2^J;
    a-step j = 1+v2(3s_t+5+3k_n-2^{n-1}lam_u) exactly and j < j_prev (NT); b/c-step j = j of W's
    chain at tau(n) and j <= j_prev-3; th~ = 3s+5 mod 2^j; crossings only at top-level states;
    X(0..3) even-headed.
 E2 [Class-B]  the exit automaton (PROOF_EL Thm A) = verify_m.sym_exit for 2 <= J < NCHK.
 E3 [Class-B]  alpha/beta lemma (PROOF_EL Lemma T): v2(alpha_x) = J - Gamma_t, 1 <= beta_x <= 6d-1.
 E4 [Class-B]  level 0: automaton from every fire state (J,1), 2 <= J < NJ=10^6: no tie, r <= 2.
 E5 [Class-B]  level 1 certificate: from every entry state (j,2),(j,0) (1 <= j < NJ) and
    (j_W, th_W - 1) for every a-step pair (j_W,th_W) of level 0: no tie; chains after entry <= 3.
 E6 [Class-B, informational]  level 2 adversarial entries: lists the ties (the method stops here).
 E7 [analytic constants]  1.5n^2+10 < 2^{n-1} for n >= 8 (checked to 400 + monotonicity).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work_m'))

def v2(x): return (x & -x).bit_length()-1

NJ = 10**6

# ------------------------------------------------------------------------------------------------
# real lambda-only walk (the certified walker of PROOF_M sec. 4) with chain/theta bookkeeping
# ------------------------------------------------------------------------------------------------
def real_walk(NB):
    CAP = NB+10
    Xt=[None]*CAP; Xtyp=[None]*CAP; Xpar=[None]*CAP
    lA=1; S=[]; i=0; s=0; calls=[]; first=True
    chain_at={}; cur=None
    st=dict(fires=0, a=0, bc=0, minbc=99, minad=99)
    while i<=NB:
        while calls and calls[-1]<s: calls.pop()
        k=len(S)
        if k>=2: lb=S[-1]; lc=S[-2]; nb=nc=None
        elif k==1: lb=S[-1]; lc=0; nb=None; nc=i
        else: lb=lc=0; nb=i; nc=i+1
        par=(lA+(1 if first else 0))&1          # real head parity (c_A odd only at s=0)
        for n in (nb,nc):
            if n is not None and n<CAP and Xt[n] is None:
                assert not calls, 'crossing inside a call'
                Xt[n]=s; Xtyp[n]='a' if (k==0 and i==n) else 'b' if k==0 else 'c'; Xpar[n]=par
        if par==0:
            lA=lA+lb+lc+3; push=None
        else:
            lx=lA+2*lb+3; j=v2(lx); u=lx>>j
            if not calls:                                   # top-level chain
                if k==0:                                    # level fire
                    assert (3*s+4)%(1<<j)==0 and ((3*s+4)>>j)&1
                    th=1; kind='F'; st['fires']+=1
                else:
                    jp,thp,sp,lup=cur; n=jp-1
                    assert Xpar[n]==1 and s==sp+1+Xt[n]
                    if Xtyp[n]=='a':
                        assert Xt[n]%2==0; kn=Xt[n]//2
                        assert j==1+v2(3*sp+5+3*kn-(lup<<(n-1))), 'a-step formula'
                        assert j<jp, 'NON-DESCENT (tie)'
                        st['minad']=min(st['minad'],jp-j)
                        th=3-thp; kind='a'; st['a']+=1
                    else:
                        jw,thw,_=chain_at[Xt[n]]
                        assert j==jw, 'b/c copy j'
                        assert j<=jp-3, 'b/c descent'
                        st['minbc']=min(st['minbc'],jp-j)
                        th=thw+thp-2; kind=Xtyp[n]; st['bc']+=1
                assert (th-(3*s+5))%(1<<j)==0, 'theta rule'
                chain_at[s]=(j,th,kind); cur=(j,th,s,u)
            T=Xt[j-1]
            if T>0: calls.append(s+T)
            push=(u,j,lc+(lA+1)//2); lA=u+1
        if k>=2: del S[-2:]
        else: i+=2-k; S.clear()
        if push:
            u,j,D=push; S.append(D)
            for t in range(j-2,-1,-1): S.append(u<<t)
        s+=1; first=False
    for n in range(4): assert Xpar[n]==0
    return Xt,Xtyp,Xpar,chain_at,st,s

# ------------------------------------------------------------------------------------------------
# the exit automaton (PROOF_EL Theorem A); state (j, th~)
# ------------------------------------------------------------------------------------------------
def make_run(Xt,Xtyp,Xpar,chain_at):
    def run(j,th):
        out=[]
        while True:
            n=j-1
            if Xpar[n]==0: return out,None
            if Xtyp[n]=='a':
                A=(th+3*(Xt[n]//2)+(1<<(n-1)))%(1<<n)
                if A==0: return out,('TIE',j,th)
                j=1+v2(A); th=3-th; kd='a'
            else:
                jw,thw,_=chain_at[Xt[n]]; j=jw; th=thw+th-2; kd='c'
            out.append((j,th,kd))
    return run

def E2(run,NCHK):
    import verify_m as vm
    X=vm.Xdata(NCHK,SMALL=NCHK); bad=0
    for J in range(2,NCHK):
        out,f=run(J,1); r=vm.sym_exit(J,X)
        if f is not None or isinstance(r[0],str) or tuple([J]+[o[0] for o in out])!=r[0]: bad+=1
    print('E2 automaton == verify_m.sym_exit for 2<=J<%d: mismatches %d'%(NCHK,bad)); assert bad==0
    return X

def E3(X,Xt,NCHK):
    """symbolic recursion of PROOF_M Lemma 6.1 with alpha/beta bookkeeping"""
    n_ok=0
    for J in range(2,NCHK):
        u=(1,0); D=(1<<(J-1),-1); j=J; d=0; Gam=0
        for t in range(50):
            n=j-1; typ,(cH,lH),Y,eps=X[n]
            H=(cH*u[0], cH*u[1]+lH)
            if (H[0]+H[1])%2==0: break
            b=D if typ=='a' else (Y[0]*u[0],Y[0]*u[1]+Y[1])
            x=(H[0]+2*b[0], H[1]+2*b[1]+3)
            Gam+=1+eps; d+=1+Xt[n]
            assert v2(x[0])==J-Gam, ('alpha valuation',J,t)
            assert 1<=x[1]<=6*d-1, ('beta bound',J,t)
            assert v2(x[1])<v2(x[0]); n_ok+=1
            j=v2(x[1]); u=(x[0]>>j,x[1]>>j)
            Dn=(H[0]//2,(H[1]+1)//2)
            D=Dn if typ=='a' else (D[0]+Dn[0],D[1]+Dn[1])
    print('E3 alpha/beta lemma: v2(alpha_x)=J-Gamma_t and 1<=beta_x<=6d-1 at all %d exit chains, J<%d'%(n_ok,NCHK))

def levels(run, L2=True):
    from collections import Counter
    A0=set(); ties=0; rc=Counter(); TH=Counter()
    for J in range(2,NJ):
        out,f=run(J,1); ties+= f is not None; rc[len(out)]+=1
        for (j,th,kd) in out:
            TH[th]+=1
            if kd=='a': A0.add((j,th))
    print('E4 level 0 (fires 2<=J<10^6): ties %d, r distribution %s, exit-chain th~ values %s'%(ties,sorted(rc.items()),sorted(TH)))
    print('   a-step pairs (j,th~) of level 0 (%d): %s'%(len(A0),sorted(A0)))
    assert ties==0 and max(rc)<=2
    # level 1
    entries=[('any',2),('any',0)]+[('spec',(j,th-1)) for (j,th) in sorted(A0)]
    T=[]; R=Counter(); A1=set()
    for kind,e in entries:
        rng=[(j,e) for j in range(1,NJ)] if kind=='any' else [e]
        for (j,th) in rng:
            out,f=run(j,th)
            if f: T.append((j,th,f))
            R[len(out)]+=1
            for (jj,tt,kd) in out:
                if kd=='a': A1.add((jj,tt))
    print('E5 level 1 certificate: %d entry families (any j<10^6 with th~ in {2,0}; %d specific c-entries):'%(len(entries),len(entries)-2))
    print('   ties %d; chains after the entry chain: distribution %s  => r <= %d'%(len(T),sorted(R.items()),1+max(R)))
    assert not T and 1+max(R)<=4
    if not L2: return
    # level 2 (adversarial; informational)
    big1={2,0}; anyth=set(); spec=set()
    for th in big1:
        anyth|={3-th, th-1}
        for (jw,tw) in A0|A1: spec.add((jw,th+tw-2))
    anyth|={2,0}
    T2=[]
    for th in sorted(anyth):
        for j in range(1,NJ):
            out,f=run(j,th)
            if f: T2.append((j,th,out,f))
    for (j,th) in sorted(spec):
        out,f=run(j,th)
        if f: T2.append((j,th,out,f))
    print('E6 level 2 (adversarial entries any-j th~ in %s, %d specific): ties %d'%(sorted(anyth),len(spec),len(T2)))
    for x in T2[:3]: print('   tie path: entry (j,th~)=(%d,%d) -> %s -> %s'%x)

def E7():
    ok=all(1.5*n*n+10 < 2**(n-1) for n in range(8,401))
    # for n>=400: (1.5(n+1)^2+10)/(1.5n^2+10) < 2, so the inequality propagates
    print('E7 1.5n^2+10 < 2^(n-1) for 8<=n<=400 (and inductively beyond): %s'%ok); assert ok

if __name__=='__main__':
    NB=int(sys.argv[1]) if len(sys.argv)>1 else 10**6
    NCHK=int(sys.argv[2]) if len(sys.argv)>2 else 20000
    L2=(sys.argv[3]!='0') if len(sys.argv)>3 else True
    assert NB>=NJ
    Xt,Xtyp,Xpar,chain_at,st,s=real_walk(NB)
    print('E1 real walk i<=%d (%d steps): %d fires, %d a-steps (all descending, min drop %d), %d b/c-steps (min drop %d);'%(
          NB,s,st['fires'],st['a'],st['minad'],st['bc'],st['minbc']))
    print('   a-step formula, b/c copy rule, theta rule hold at every top-level chain; X(0..3) even-headed')
    print('   odd type-a crossings n<40 with k_n:',[(n,Xt[n]//2) for n in range(40) if Xpar[n]==1 and Xtyp[n]=='a'])
    run=make_run(Xt,Xtyp,Xpar,chain_at)
    X=E2(run,NCHK)
    E3(X,Xt,NCHK)
    levels(run,L2)
    E7()
