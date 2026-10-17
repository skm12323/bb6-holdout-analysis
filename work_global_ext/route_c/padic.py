"""padic.py -- exhaustive 2-adic exploration of the small-index exit walk (route C adversary).

Model: a top-level chain with parameter j, Theta = T0 + C, lambda_u = a*T0 + b*L0 + c, where (T0, L0) in
Z_2 x Z_2^x are FREE (the adversary's choice, i.e. arbitrary hidden high bits).  Exact transitions with
the real crossing table X(n), n < N0 (PROOF_EL A1/A2 before reduction, TIE2 section 2):
  a-step: x = 2(Theta+3k) - 2^n lambda_u, j'=v2(x), lambda_u' = x/2^j', Theta' = Theta+3+3tau(n)
  b/c   : j'=omega(n), lambda_u' = lambda_uW + c_uW*lambda_u,  Theta' = Theta+3+3tau(n)
Whenever a valuation is not determined on the current cylinder (T0 mod 2^e1, L0 mod 2^e2) we split the
cylinder (exhaustive case split).  Leaves: END (even return), EXIT (j' >= N0 forced), CAP (depth cap).
"""
import sys
from fractions import Fraction as Fr
from fdata import small_full

INF=10**9
def v2i(x):
    return (x & -x).bit_length()-1 if x else INF
def v2f(f):
    if f==0: return INF
    return v2i(f.numerator)-v2i(f.denominator)

class Explorer:
    def __init__(self,N0,SM,cap=60):
        self.N0=N0; self.SM=SM; self.cap=cap
        self.stats=dict(END=0,EXIT=0,CAP=0); self.meas=dict(END=Fr(0),EXIT=Fr(0),CAP=Fr(0))
        self.maxdepth=0; self.depthhist={}; self.exits=[]; self.caps=[]; self.nodes=0; self.longest=None
    def leaf(self,kind,depth,e1,e2,path):
        self.stats[kind]+=1; self.meas[kind]+=Fr(1,2**(e1+e2-1))
        if kind=='END':
            self.depthhist[depth]=self.depthhist.get(depth,0)+1
            if depth>self.maxdepth: self.maxdepth=depth; self.longest=list(path)
        elif kind=='EXIT' and len(self.exits)<50: self.exits.append(list(path))
        elif kind=='CAP' and len(self.caps)<5: self.caps.append(list(path))
    def run(self,j0):
        # stack items: (j, C, (a,b,c), Tr,e1, Lr,e2, depth, path)
        stack=[(j0,0,(Fr(0),Fr(1),Fr(0)),0,0,1,1,0,(j0,))]
        while stack:
            j,C,(a,b,c),Tr,e1,Lr,e2,depth,path=stack.pop(); self.nodes+=1
            if depth>=self.cap: self.leaf('CAP',depth,e1,e2,path); continue
            n=j-1; R=self.SM[n]
            if not R['odd']: self.leaf('END',depth,e1,e2,path); continue
            C2=C+3+3*R['tau']
            if R['typ']=='a':
                k=R['tau']//2
                # x = A*T0 + B*L0 + G
                A=2-(2**n)*a; B=-(2**n)*b; G=2*C+6*k-(2**n)*c
                fr=A*Tr+B*Lr+G
                vf=min(v2f(A)+e1 if A!=0 else INF, v2f(B)+e2 if B!=0 else INF)
                vr=v2f(fr)
                if vr<vf:
                    jn=vr
                    if jn>=self.N0: self.leaf('EXIT',depth+1,e1,e2,path+(jn,)); continue
                    s=Fr(1,2**jn)
                    stack.append((jn,C2,(A*s,B*s,G*s),Tr,e1,Lr,e2,depth+1,path+(jn,)))
                else:
                    if vf>=self.N0 and vr>=self.N0:
                        self.leaf('EXIT',depth+1,e1,e2,path+('>=%d'%self.N0,)); continue
                    # split on the variable achieving vf
                    if A!=0 and v2f(A)+e1==vf:
                        for bit in (0,1): stack.append((j,C,(a,b,c),Tr+bit*2**e1,e1+1,Lr,e2,depth,path))
                    else:
                        for bit in (0,1): stack.append((j,C,(a,b,c),Tr,e1,Lr+bit*2**e2,e2+1,depth,path))
            else:
                cu,lu=R['uW']; jn=R['omega']
                stack.append((jn,C2,(cu*a,cu*b,cu*c+lu),Tr,e1,Lr,e2,depth+1,path+(jn,)))

if __name__=='__main__':
    N0=int(sys.argv[1]) if len(sys.argv)>1 else 24
    cap=int(sys.argv[2]) if len(sys.argv)>2 else 60
    SM=small_full(N0+2)
    tot=None
    for j0 in range(5,N0):
        E=Explorer(N0,SM,cap); E.run(j0)
        print(j0,E.stats,'maxdepth',E.maxdepth,'nodes',E.nodes,'EXITmeas %.3g'%float(E.meas['EXIT']),'CAPmeas %.3g'%float(E.meas['CAP']),'longest',E.longest)
        if E.caps: print('   CAP example',E.caps[0][:40])
