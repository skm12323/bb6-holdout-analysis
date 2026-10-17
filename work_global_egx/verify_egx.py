"""verify_egx.py -- finite checks for PROOF_EGX.md (Class B; the theorems are proved in the text).

Usage:  python -B verify_egx.py [N=30000]

 C1  pair endgame of E(U,v) (defect (2^(v-1),-1), then zero fill) versus the symbolic exit
     recursion of PROOF_M Lemma 6.1 for J=v, written here from the lemma text: identical
     top-level chain pairs (c_x,l_x)=(alpha_x,beta_x), return types, final singleton
     (2^v,3*ell), for 3<=v<=N+1.
 C2  the pair endgame agrees with the integer top map of work_r1 (6 values of w, v<400).
 C3  the endgame j-sequences equal work_m/verify_m.sym_exit (read-only import), v<=min(N,20000).
 C4  Lemma T identities inside endgames: v2(c_x)=J-Gamma_t, 1<=l_x<=6d_t-1 (d_t = steps since
     the virtual fire = 1+endgame step index s, i.e. F-step s_0+1+s); C2-log bound eps(n)<=2log2(3n^2+4)-1 at type c.
 C5  Theorem L in integer form J > 6l+7+L(2l+4), L=J//(3l), and d <= 2J^2, at J=2^10..2^4096.
Only the Python standard library is needed.
"""
import sys, json
from pathlib import Path
from collections import Counter

def v2(z): return (z & -z).bit_length()-1 if z else 10**18
N=int(sys.argv[1]) if len(sys.argv)>1 else 30000

# ---- the universal walk F in pair form; crossings X(n) = (type, head, pending, pointer), tau(n)
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
    return X,tau

X,tau=walk(N)
eps={n:n-v2(X[n][1][0]) for n in X}

# ---- endgame: pair run from X(v-1) with the finite suffix
def endgame(v):
    n=v-1; typ,A,Q,i=X[n]; Q=list(Q); s=tau[n]; top=s; chains=[]
    while True:
        ents=list(Q[:2]); a=i
        while len(ents)<2 and a<=v-1:
            ents.append((1<<a,0) if a<v-1 else (1<<(v-1),-1)); a+=1
        if not ents: break                       # singleton: excursion over
        if len(ents)==1: ents.append((0,0))      # missing entry read as 0
        b,c=ents
        if (A[0]+A[1])%2==0:
            A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3); newp=[]
        else:
            x=(A[0]+2*b[0],A[1]+2*b[1]+3); j=v2(x[1])
            if not (j<v2(x[0]) and A[0]%2==0): return ('UNSAFE',v,s)
            if s==top:
                chains.append(dict(j=j,x=x,d=s+1)); top=s+1+tau[j-1]
            u=(x[0]>>j,x[1]>>j)
            newp=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[(c[0]+A[0]//2,c[1]+(A[1]+1)//2)]
            A=(u[0],u[1]+1)
        if len(Q)>=2: Q=Q[2:]
        else: i=a; Q=[]
        Q=newp+Q; s+=1
    return ('END',s,A,chains)

# ---- symbolic exit recursion, PROOF_M Lemma 6.1 (alpha,beta) for alpha*lambda_u+beta
def symexit(J):
    u=(1,0); D=(1<<(J-1),-1); j=J; out=[]; G=0
    while True:
        n=j-1; typ,AX,QX,iX=X[n]
        H=(AX[0]*u[0],AX[0]*u[1]+AX[1])
        if (H[0]+H[1])%2==0: return out
        if typ=='a': bb=D
        elif typ=='b': bb=(u[0]<<(n-1),u[1]<<(n-1))
        else: Y=QX[0]; bb=(Y[0]*u[0],Y[0]*u[1]+Y[1])
        G+=1+eps[n]
        x=(H[0]+2*bb[0],H[1]+2*bb[1]+3); jn=v2(x[1])
        if not jn<v2(x[0]): return out+[('TIE',x)]
        out.append(dict(j=jn,x=x,typ=typ,G=G))
        Dn=(H[0]//2,(H[1]+1)//2)
        D=Dn if typ=='a' else (D[0]+Dn[0],D[1]+Dn[1])
        u=(x[0]>>jn,x[1]>>jn); j=jn

res={}
# C1 + C4
mism=0; rc=Counter(); maxsteps=0; nch=0; lemT=0; types=Counter()
for v in range(3,N+2):
    eg=endgame(v); assert eg[0]=='END',eg
    se=symexit(v); assert all(isinstance(z,dict) for z in se),('tie',v)
    if [(c['j'],c['x']) for c in eg[3]]!=[(c['j'],c['x']) for c in se]: mism+=1
    assert eg[2]==(1<<v,3*eg[1]),('final',v)
    for c,z in zip(eg[3],se):
        assert v2(c['x'][0])==v-z['G'], ('Lemma T(1)',v)
        assert 1<=c['x'][1]<=6*c['d']-1, ('Lemma T(2)',v)
        lemT+=1; types[z['typ']]+=1
    rc[len(eg[3])]+=1; nch+=len(eg[3]); maxsteps=max(maxsteps,eg[1]-tau[v-1])
assert mism==0
res['C1']=dict(v_range=[3,N+1],mismatches=mism,exit_chain_count_distribution=dict(sorted(rc.items())),
              chains=nch,return_types=dict(types),max_endgame_steps=maxsteps)
res['C4_lemmaT_checks']=lemT
from math import log2
c2=0
for n in range(1,N+1):
    if X[n][0]=='c':
        assert eps[n]<=2*log2(3*n*n+4)-1, ('C2-log',n); c2+=1
res['C4_C2log_typec_crossings']=c2; res['max_eps']=max(eps.values())

# C2 real integer top map
def top(L):
    A=L[0]; b=L[1] if len(L)>1 else 0; c=L[2] if len(L)>2 else 0; S=L[3:]
    if A%2==0: return [A+b+c+3]+S
    m=b+(A-3)//2; S=[c+(A+1)//2]+S
    if (m+3)&(m+2)==0: return None
    while m%2: S=[(m+3)//2]+S; m=(m-3)//2
    return [m+4]+S
def real(w,v):
    U=3*w; L=[U+1]+[U<<a for a in range(v)]; L[-1]-=1; s=0
    while len(L)>1:
        L=top(L); assert L is not None,'HALT'; s+=1
    return s,L[0]
for v in range(3,min(400,N+2)):
    s0=endgame(v)[1]
    for w in (1,3,5,7,101,2**61-1):
        s,f=real(w,v); assert s==s0 and f==3*w*2**v+3*s,(v,w)
res['C2']='pair endgame == integer top map (length, final singleton) for 3<=v<%d, w in {1,3,5,7,101,2^61-1}'%min(400,N+2)

# C3 cross-check against work_m (read-only)
ROOT=Path(__file__).resolve().parents[1]
try:
    sys.path.insert(0,str(ROOT/'work_m')); import verify_m as vm
    M=min(N,20000); Xm=vm.Xdata(M+1,SMALL=M+1); bad=0
    for v in range(3,M+1):
        r=vm.sym_exit(v,Xm); js=tuple([v]+[c['j'] for c in endgame(v)[3]])
        if r[0]!=js: bad+=1
    assert bad==0; res['C3']='endgame j-sequences == work_m sym_exit for 3<=v<=%d'%M
except ImportError:
    res['C3']='skipped (work_m not found)'

# C5 Theorem L inequality (integer form) and the d-bound
ok=[]
for e in (10,12,16,32,64,128,256,1024,4096):
    J=1<<e; l=e
    lhs=J; L=J//(3*l)
    rhs=(6*l+7)+L*(2*l+4)
    dbound=1+(J-1)**2+L*(1+(2*l+4)**2) <= 2*J*J
    assert lhs>rhs and dbound,(e)
    ok.append(e)
res['C5_scales_log2J']=ok
res['result']='PASS'
print(json.dumps(res,indent=1))
Path(__file__).with_name('checks.json').write_text(json.dumps(res,indent=1)+'\n')
