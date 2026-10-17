"""tielab.py -- shared code for route D (ties in the symbolic exit).  Standard library only.

walk(N)            : F's crossing table X(n)=(type, head pair, pending list, pointer), tau(n), eps(n)
symstar(J,e)       : extended symbolic exit S*_e(J) (defect D_0=(2^(J-1),-e)); continues through
                     OVER-ties (v2 beta > v2 alpha: j:=v2 alpha), stops at the first EXACT tie.
realrec(U,J,e)     : the same top-level recursion with integers (real excursion E_e(U,J)), any U.
toplist(U,J,e)     : brute-force integer top map (work_r1 RULES section 5) on
                     (U+1; U, 2U, ..., 2^(J-2)U, 2^(J-1)U - e), for validation.
"""
import sys
def v2(z): return (z & -z).bit_length()-1 if z else 10**18

def walk(N):
    A=(1,1); Q=[]; i=0; s=0; X={}; tau={}
    while len(X)<N+1:
        k=len(Q)
        reads=[] if k>=2 else ([i] if k==1 else [i,i+1])
        for n in reads:
            if n not in X and n<=N:
                typ='a' if (k==0 and i==n) else ('b' if k==0 else 'c')
                X[n]=(typ,A,list(Q),i); tau[n]=s
        ents=list(Q[:2]); a=i
        while len(ents)<2: ents.append((1<<a,0)); a+=1
        b,c=ents
        if (A[0]+A[1])%2==0:
            A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3); newp=[]
        else:
            x=(A[0]+2*b[0],A[1]+2*b[1]+3); j=v2(x[1]); assert j<v2(x[0]) and A[0]%2==0
            u=(x[0]>>j,x[1]>>j)
            newp=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[(c[0]+A[0]//2,c[1]+(A[1]+1)//2)]
            A=(u[0],u[1]+1)
        if k>=2: Q=Q[2:]
        else: i+=2-k; Q=[]
        Q=newp+Q; s+=1
    eps={n:n-v2(X[n][1][0]) for n in X}
    return X,tau,eps

class Lab:
    def __init__(self,N=400):
        self.N=N; self.X,self.tau,self.eps=walk(N)
    # ---------------- symbolic S*_e(J) -----------------
    def symstar(self,J,e=1,maxch=10**6):
        X,eps,tau=self.X,self.eps,self.tau
        u=(1,0); D=(1<<(J-1),-e); j=J; G=0; ch=[]; d=1+tau[J-1]
        for t in range(maxch):
            n=j-1
            if n not in X: return dict(st='NODATA',ch=ch)
            typ,AX,QX,iX=X[n]
            H=(AX[0]*u[0],AX[0]*u[1]+AX[1])
            if (H[0]+H[1])%2==0: return dict(st='END',ch=ch,G=G)
            assert H[0]%2==0
            if typ=='a': bb=D
            elif typ=='b': bb=(u[0]<<(n-1),u[1]<<(n-1))
            else: Y=QX[0]; bb=(Y[0]*u[0],Y[0]*u[1]+Y[1])
            G+=1+eps[n]
            x=(H[0]+2*bb[0],H[1]+2*bb[1]+3); va=v2(x[0]); vb=v2(x[1])
            rec=dict(t=t+1,typ=typ,x=x,va=va,vb=vb,G=G,d=d)
            if vb==va:
                rec['kind']='EXACT'; ch.append(rec); return dict(st='EXACT',ch=ch,G=G)
            jn=min(va,vb); rec['kind']='free' if vb<va else 'over'; rec['j']=jn; ch.append(rec)
            Dn=(H[0]//2,(H[1]+1)//2)
            D=Dn if typ=='a' else (D[0]+Dn[0],D[1]+Dn[1])
            u=(x[0]>>jn,x[1]>>jn); j=jn; d+=1+tau[j-1]
        return dict(st='LONG',ch=ch)
    # ---------------- real top-level recursion -----------------
    def realrec(self,U,J,e=1,maxch=10**5):
        """integer recursion; returns dict(st=END/HALT/NODATA/LONG, ch=[(typ,X,j)], steps)"""
        X,tau=self.X,self.tau
        u=U; D=(U<<(J-1))-e; j=J; ch=[]; steps=tau[J-1]   # steps of the excursion before X(J-1)
        for t in range(maxch):
            n=j-1
            if n not in X: return dict(st='NODATA',ch=ch,need=n)
            typ,AX,QX,iX=X[n]
            H=AX[0]*u+AX[1]
            if typ=='a': b=D; c=0
            elif typ=='b': b=u<<(n-1); c=D
            else: Y=QX[0]; b=Y[0]*u+Y[1]; c=D
            if H%2==0:
                return dict(st='END',ch=ch,steps=steps+1,final=H+b+c+3)
            x=H+2*b+3
            if x&(x-1)==0: return dict(st='HALT',ch=ch+[(typ,x,None)],steps=steps)
            jn=v2(x); ch.append((typ,x,jn))
            D=c+(H+1)//2; u=x>>jn; j=jn; steps+=1+tau[j-1]
        return dict(st='LONG',ch=ch)

def top(L):
    A=L[0]; b=L[1] if len(L)>1 else 0; c=L[2] if len(L)>2 else 0; S=L[3:]
    if A%2==0: return [A+b+c+3]+S
    m=b+(A-3)//2; S=[c+(A+1)//2]+S
    if (m+3)&(m+2)==0: return None
    while m%2: S=[(m+3)//2]+S; m=(m-3)//2
    return [m+4]+S
def toplist(U,J,e=1,maxsteps=10**6):
    L=[U+1]+[U<<a for a in range(J)]; L[-1]-=e; s=0
    while len(L)>1 and s<maxsteps:
        L2=top(L)
        if L2 is None: return dict(st='HALT',steps=s,L=L)
        L=L2; s+=1
    return dict(st='END' if len(L)==1 else 'LONG',steps=s,final=L[0])

# ---------------------------------------------------------------------------------------------
# general start states: after a top-level chain with parameter j, base u, defect-accumulator D.
# u, D are pairs (coefficient of U, constant).  The list is (u+1; u, 2u, ..., 2^(j-2)u, D).
# ---------------------------------------------------------------------------------------------
def symstate(lab,j,u,D,maxch=10**5):
    """S*-type symbolic recursion (U odd symbol) from a general state; stops at first EXACT tie."""
    X,eps,tau=lab.X,lab.eps,lab.tau; ch=[]
    for t in range(maxch):
        n=j-1
        if n not in X: return dict(st='NODATA',ch=ch)
        typ,AX,QX,iX=X[n]
        H=(AX[0]*u[0],AX[0]*u[1]+AX[1])
        if (H[0]+H[1])%2==0: return dict(st='END',ch=ch)
        if H[0]%2: return dict(st='ODDC',ch=ch)
        if typ=='a': bb=D
        elif typ=='b': bb=(u[0]<<(n-1),u[1]<<(n-1))
        else: Y=QX[0]; bb=(Y[0]*u[0],Y[0]*u[1]+Y[1])
        x=(H[0]+2*bb[0],H[1]+2*bb[1]+3); va=v2(x[0]); vb=v2(x[1])
        rec=dict(t=t+1,typ=typ,x=x,va=va,vb=vb)
        if vb==va: rec['kind']='EXACT'; ch.append(rec); return dict(st='EXACT',ch=ch)
        jn=min(va,vb); rec['kind']='free' if vb<va else 'over'; rec['j']=jn; ch.append(rec)
        Dn=(H[0]//2,(H[1]+1)//2)
        D=Dn if typ=='a' else (D[0]+Dn[0],D[1]+Dn[1])
        u=(x[0]>>jn,x[1]>>jn); j=jn
    return dict(st='LONG',ch=ch)

def realstate(lab,U,j,u,D,maxch=10**5,halt=True):
    """integer recursion from the state with real base u(U), D(U)."""
    X,tau=lab.X,lab.tau; uu=u[0]*U+u[1]; DD=D[0]*U+D[1]; ch=[]
    for t in range(maxch):
        n=j-1
        if n not in X: return dict(st='NODATA',ch=ch,need=n)
        typ,AX,QX,iX=X[n]
        H=AX[0]*uu+AX[1]
        if typ=='a': b=DD; c=0
        elif typ=='b': b=uu<<(n-1); c=DD
        else: Y=QX[0]; b=Y[0]*uu+Y[1]; c=DD
        if H%2==0: return dict(st='END',ch=ch,final=H+b+c+3)
        x=H+2*b+3
        if halt and x&(x-1)==0: return dict(st='HALT',ch=ch+[(typ,x,None)])
        jn=v2(x); ch.append((typ,x,jn))
        DD=c+(H+1)//2; uu=x>>jn; j=jn
    return dict(st='LONG',ch=ch)

def statelist(U,j,u,D):
    uu=u[0]*U+u[1]; DD=D[0]*U+D[1]
    return [uu+1]+[uu<<t for t in range(j-1)]+[DD]
def toprun(L,maxsteps=10**6):
    s=0
    while len(L)>1 and s<maxsteps:
        L2=top(L)
        if L2 is None: return dict(st='HALT',steps=s,L=L)
        L=L2; s+=1
    return dict(st='END' if len(L)==1 else 'LONG',steps=s,final=L[0])

def tietree(lab,j,u,D,Bmax=24,maxch=200):
    """Exact refinement tree.  U = r + 2^B V (V>=0).  Pairs are (c,l) meaning c*V+l.
    Start U=1+2V.  At a chain whose valuation is not determined uniformly in V (v2 l >= v2 c),
    split V=2V'+bit.  Returns: leaves (r,B,status,#chains), halting reps (U=r with V=0 and u=1),
    unresolved classes (B>Bmax)."""
    X=lab.X
    def sub(p,bit): return (2*p[0],p[1]+bit*p[0])
    tr=lambda p:(2*p[0],p[0]+p[1])
    stack=[(1,1,j,tr(u),tr(D),0)]
    leaves=[]; halts=[]; unres=[]
    while stack:
        r,B,jj,uu,DD,nch=stack.pop()
        while True:
            n=jj-1
            if n not in X: leaves.append((r,B,'NODATA',nch)); break
            if nch>maxch: leaves.append((r,B,'LONG',nch)); break
            typ,AX,QX,iX=X[n]
            H=(AX[0]*uu[0],AX[0]*uu[1]+AX[1])
            assert H[0]%2==0
            if H[1]%2==0: leaves.append((r,B,'END',nch)); break
            if typ=='a': bb=DD
            elif typ=='b': bb=(uu[0]<<(n-1),uu[1]<<(n-1))
            else: Y=QX[0]; bb=(Y[0]*uu[0],Y[0]*uu[1]+Y[1])
            x=(H[0]+2*bb[0],H[1]+2*bb[1]+3)
            if x[1]!=0 and v2(x[1])<v2(x[0]):
                jn=v2(x[1]); un=(x[0]>>jn,x[1]>>jn)
                if un[1]==1: halts.append((r,B,nch+1,typ))     # V=0 member halts here
                Dn=(H[0]//2,(H[1]+1)//2)
                DD=Dn if typ=='a' else (DD[0]+Dn[0],DD[1]+Dn[1])
                uu=un; jj=jn; nch+=1
                continue
            # undetermined: split
            if B>=Bmax: unres.append((r,B,nch+1,typ)); break
            stack.append((r+(1<<B),B+1,jj,sub(uu,1),sub(DD,1),nch))
            r,B,uu,DD=r,B+1,sub(uu,0),sub(DD,0)
    return dict(leaves=leaves,halts=halts,unres=unres)

def late_state(rnd,Jr=(20,30),jr=(5,12),hs=(1,1,2)):
    """random mass-consistent late-stage state of a symbolic exit (Lemma T shape):
    alpha_x=2^m gamma in [2^J,2^(J+1)), m=jt+h, beta_x even with v2=jt, d in [J,2J^2],
    beta_x<=6d-8, u=x/2^jt, D=(2^J-alpha_x/2, 3d-4-beta_x/2)  (so sum alpha=2^J, sum beta=3d-3)."""
    while True:
        J=rnd.randint(*Jr); jt=rnd.randint(*jr); m=jt+rnd.choice(hs)
        if m>=J-1: continue
        lo=(1<<J)>>m; g=rnd.randrange(lo,2*lo)|1; ax=g<<m
        if not ((1<<J)<=ax<(1<<(J+1))): continue
        d=rnd.randint(J,2*J*J)
        top_=(6*d-8)>>jt
        if top_<1: continue
        bx=(rnd.randrange(1,top_+1)|1)<<jt
        if bx>6*d-8: continue
        return J,jt,(ax>>jt,bx>>jt),((1<<J)-ax//2,3*d-4-bx//2),d
