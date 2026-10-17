"""core.py -- F's crossing table and the symbolic exit S(J) (copied/adapted from work_global_egx/verify_egx.py),
plus the beta-only reduction (route B).  Standard library only."""
import sys, pickle, os

def v2(z): return (z & -z).bit_length()-1 if z else 10**18

def walk(N):
    """Universal pair walk F until crossings X(0..N) are known.
    Returns X[n]=(typ,A,Q,i), tau[n], and W's chain at step tau(n) when that step is odd: chainW[n]=(c_x,l_x,j)."""
    A=(1,1); Q=[]; i=0; s=0; X={}; tau={}; chainW={}
    while len(X)<N+1:
        k=len(Q)
        reads=[] if k>=2 else ([i] if k==1 else [i,i+1])
        newn=[]
        for n in reads:
            if n not in X and n<=N:
                typ='a' if (k==0 and i==n) else ('b' if k==0 else 'c')
                X[n]=(typ,A,list(Q),i); tau[n]=s; newn.append(n)
        ents=list(Q[:2]); a=i
        while len(ents)<2: ents.append((1<<a,0)); a+=1
        b,c=ents
        if (A[0]+A[1])%2==0:
            A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3); newp=[]
        else:
            x=(A[0]+2*b[0],A[1]+2*b[1]+3); j=v2(x[1]); assert j<v2(x[0]) and A[0]%2==0
            for n in newn: chainW[n]=(x[0],x[1],j)
            u=(x[0]>>j,x[1]>>j)
            newp=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[(c[0]+A[0]//2,c[1]+(A[1]+1)//2)]
            A=(u[0],u[1]+1)
        if k>=2: Q=Q[2:]
        else: i+=2-k; Q=[]
        Q=newp+Q; s+=1
    return X,tau,chainW

def load(N):
    fn='walk_%d.pkl'%N
    if os.path.exists(fn):
        return pickle.load(open(fn,'rb'))
    X,tau,chainW=walk(N)
    # compact table
    T={}
    for n in X:
        typ,A,Q,i=X[n]
        T[n]=dict(typ=typ,A=A,Y=(Q[0] if Q else None),tau=tau[n],eps=n-v2(A[0]),
                  odd=((A[0]+A[1])%2==1) if n>=2 else False, W=chainW.get(n))
    pickle.dump(T,open(fn,'wb'))
    return T

def symexit(J,T):
    """S(J) exactly as in verify_egx.symexit, returning the full chain list with (alpha,beta) pairs."""
    u=(1,0); D=(1<<(J-1),-1); j=J; out=[]; G=0; d=0
    while True:
        n=j-1; row=T[n]; AX=row['A']
        H=(AX[0]*u[0],AX[0]*u[1]+AX[1])
        if (H[0]+H[1])%2==0: return out,'END'
        if row['typ']=='a': bb=D
        elif row['typ']=='b': bb=(u[0]<<(n-1),u[1]<<(n-1))
        else: Y=row['Y']; bb=(Y[0]*u[0],Y[0]*u[1]+Y[1])
        G+=1+row['eps']; d+=1+row['tau']
        x=(H[0]+2*bb[0],H[1]+2*bb[1]+3); jn=v2(x[1])
        if not jn<v2(x[0]): return out+[dict(j=jn,x=x,typ=row['typ'],G=G,d=d,tie=True)],'TIE'
        out.append(dict(j=jn,x=x,typ=row['typ'],G=G,d=d))
        Dn=(H[0]//2,(H[1]+1)//2)
        D=Dn if row['typ']=='a' else (D[0]+Dn[0],D[1]+Dn[1])
        u=(x[0]>>jn,x[1]>>jn); j=jn

def beta_walk(j,d,bu,T,G=None,J=None,limit=10**6):
    """beta-only system (Lemma BR).  State: parameter j of the current chain, d=steps since fire, beta_u.
    Returns list of (j,d,beta_x,typ) of successive chains, and the stop reason."""
    out=[]
    for _ in range(limit):
        n=j-1
        if n not in T: return out,'OUT'
        row=T[n]
        if not row['odd']: return out,'END'
        if row['typ']=='a':
            bx=2*(3*d+1)+3*row['tau']-(bu<<n)
        else:
            cxW,lxW,jW=row['W']; bx=bu*cxW+lxW
        d=d+1+row['tau']
        jn=v2(bx)
        out.append((jn,d,bx,row['typ']))
        if bx<=0: return out,'NONPOS'
        bu=bx>>jn; j=jn
    return out,'LIMIT'
