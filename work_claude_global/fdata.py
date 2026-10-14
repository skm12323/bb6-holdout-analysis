"""Run F (formal pair map) and record crossing data per index n:
typ, head parity, tau, and (if odd) the chain value x=(cX,lamX) at step tau(n)."""
from collections import deque
def v2(x): return (x & -x).bit_length()-1
def crossings(NMAX):
    A=(1,1); P=deque(); i=0; s=0
    tau={}; typ={}; hpar={}; X={}
    while i<NMAX:
        pe=len(P)
        if pe==0: cr=[(i,'a'),(i+1,'b')]
        elif pe==1: cr=[(i,'c')]
        else: cr=[]
        par=(A[0]+A[1])&1
        for n,t in cr: tau[n]=s; typ[n]=t; hpar[n]=par
        if pe>=2: b=P.popleft(); c=P.popleft()
        elif pe==1: b=P.popleft(); c=(1<<i,0); i+=1
        else: b=(1<<i,0); c=(1<<(i+1),0); i+=2
        if par==0:
            A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3)
        else:
            xc=A[0]+2*b[0]; xl=A[1]+2*b[1]+3
            j=v2(xl); assert v2(xc)>j
            for n,t in cr: X[n]=(xc,xl,j)
            uc=xc>>j; ul=xl>>j
            D=(c[0]+(A[0]>>1), c[1]+((A[1]+1)>>1))
            P.extendleft(reversed([(uc<<a,ul<<a) for a in range(j-1)]+[D]))
            A=(uc,ul+1)
        s+=1
    return tau,typ,hpar,X
