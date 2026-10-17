"""fdata.py -- crossing data of the universal pair walk F (route C, standard library only).

lam_walk(N): lambda-only walker (PROOF_M section 4 / V2 logic, re-implemented) recording for every
crossing n < N:  typ[n] in 'abc', tau[n], eps[n], odd[n] (parity of W's head at X(n)),
lY[n] (lambda of the pending entry Y for type c; 0 otherwise), lA[n] (lambda of the head).
sigma is recomputed by the proved recursion (PROOF_M Lemma 3.2) and S1 (j < sigma) is asserted.

small_full(NS): full (c,lambda) pair walk for n < NS, giving for every odd crossing the W-chain
at tau(n): (c'_x, lambda'_x), omega = v2(lambda'_x), and u_W = x'/2^omega.
"""
import sys
from array import array

def v2(x): return (x & -x).bit_length()-1

def lam_walk(N, check=True):
    typ=bytearray(b'?'*N); tau=array('q',[-1])*N; eps=array('h',[0])*N
    odd=bytearray(N); lY=array('q',[0])*N; lA=array('q',[0])*N
    la=1; S=[]; i=0; s=0; calls=[]; sig_last=None; jl=None; first=True
    seen=-1
    while seen<N-1:
        while calls and calls[-1]<s: calls.pop()
        k=len(S)
        if k>=2: lb=S[-1]; lc=S[-2]; reads=()
        elif k==1: lb=S[-1]; lc=0; reads=(i,)
        else: lb=lc=0; reads=(i,i+1)
        par=(la+(1 if first else 0))&1
        for n in reads:
            if n>seen and n<N:
                seen=n
                assert not calls
                tau[n]=s; odd[n]=par; lA[n]=la
                if k==0 and i==n: typ[n]=97; eps[n]=0
                elif k==0: typ[n]=98; eps[n]=1
                else: typ[n]=99; eps[n]=n-(sig_last-1); lY[n]=lb
        if par==0:
            la=la+lb+lc+3; push=None
        else:
            lx=la+2*lb+3; j=v2(lx); u=lx>>j
            if not calls:
                if k==0: sg=i
                else: sg=sig_last-1-eps[jl-1]
                if check: assert j<sg, ('S1 fails',i,s,j,sg)
                sig_last=sg; jl=j
            T=tau[j-1]; assert T>=0
            if T>0: calls.append(s+T)
            push=(u,j,lc+(la+1)//2); la=u+1
        if k>=2: del S[-2:]
        else: i+=2-k; S.clear()
        if push:
            u,j,D=push; S.append(D)
            for t in range(j-2,-1,-1): S.append(u<<t)
        s+=1; first=False
    return dict(typ=typ,tau=tau,eps=eps,odd=odd,lY=lY,lA=lA,N=N)

def small_full(NS):
    """full pair walk; returns dict n -> record with W-chain data at tau(n)."""
    A=(1,1); P=[]; i=0; s=0; X={}; seen=-1
    while seen<NS-1:
        ents=[(p[0],p[1]) for p in P[:2]]; a=i
        while len(ents)<2: ents.append((1<<a,0)); a+=1
        (cb,lb),(cc,lc)=ents
        k=len(P)
        for n in ([i] if k==1 else [i,i+1] if k==0 else []):
            if n>seen and n<NS:
                seen=n
                t='a' if (k==0 and i==n) else ('b' if k==0 else 'c')
                rec=dict(typ=t,tau=s,A=A,Y=(P[0] if t=='c' else ((1<<(n-1),0) if t=='b' else None)),
                         eps=n-v2(A[0]),odd=(A[0]+A[1])%2)
                if rec['odd'] and t!='a':
                    x=(A[0]+2*cb,A[1]+2*lb+3); om=v2(x[1])
                    rec.update(x=x,omega=om,uW=(x[0]>>om,x[1]>>om),ThW=3*s+5)
                X[n]=rec
        if (A[0]+A[1])%2==0:
            A=(A[0]+cb+cc,A[1]+lb+lc+3); newp=[]
        else:
            cx,lx=A[0]+2*cb,A[1]+2*lb+3; vc,vl=v2(cx),v2(lx); assert vl<vc and A[0]%2==0
            j=vl; u=(cx>>j,lx>>j)
            newp=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[(cc+A[0]//2,lc+(A[1]+1)//2)]
            A=(u[0],u[1]+1)
        if k>=2: P=P[2:]
        else: i+=2-k; P=[]
        P=newp+P; s+=1
    return X

if __name__=='__main__':
    import time
    N=int(sys.argv[1]) if len(sys.argv)>1 else 10**6
    t=time.time(); D=lam_walk(N); print('lam_walk',N,'%.1fs'%(time.time()-t))
