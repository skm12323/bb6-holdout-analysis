"""Resonance at b-depth 124 over the parameter-5 fire at pointer 63 (s=52): exact 2-adic continuation.
State: chain with j=65, Theta = -122 (mod 2^65) [true residue], lambda_u free odd.  Exhaustive split."""
from fractions import Fraction as Fr
from fdata import small_full
from padic import Explorer
SM=small_full(80)
print('X(64):',SM[64]['typ'],SM[64]['odd'],'omega',SM[64].get('omega'),' X(63):',SM[63]['typ'],SM[63]['tau'])
E=Explorer(80,SM,cap=40)
# monkeypatch run with custom start
stack=[(65,0,(Fr(0),Fr(1),Fr(0)),(-122)%(1<<65),65,1,1,0,(65,))]
import types
def run_custom(self,stack):
    while stack:
        j,C,(a,b,c),Tr,e1,Lr,e2,depth,path=stack.pop(); self.nodes+=1
        if depth>=self.cap: self.leaf('CAP',depth,e1,e2,path); continue
        n=j-1; R=self.SM[n]
        if not R['odd']: self.leaf('END',depth,e1,e2,path); continue
        C2=C+3+3*R['tau']
        if R['typ']=='a':
            k=R['tau']//2; A=2-(2**n)*a; B=-(2**n)*b; G=2*C+6*k-(2**n)*c
            from padic import v2f,INF
            fr=A*Tr+B*Lr+G; vf=min(v2f(A)+e1 if A!=0 else INF, v2f(B)+e2 if B!=0 else INF); vr=v2f(fr)
            if vr<vf:
                jn=vr; s=Fr(1,2**jn); stack.append((jn,C2,(A*s,B*s,G*s),Tr,e1,Lr,e2,depth+1,path+(jn,)))
            else:
                if A!=0 and v2f(A)+e1==vf:
                    for bit in (0,1): stack.append((j,C,(a,b,c),Tr+bit*2**e1,e1+1,Lr,e2,depth,path))
                else:
                    for bit in (0,1): stack.append((j,C,(a,b,c),Tr,e1,Lr+bit*2**e2,e2+1,depth,path))
        else:
            cu,lu=R['uW']; jn=R['omega']; stack.append((jn,C2,(cu*a,cu*b,cu*c+lu),Tr,e1,Lr,e2,depth+1,path+(jn,)))
run_custom(E,stack)
print(E.stats,'maxdepth',E.maxdepth,'longest',E.longest)
from collections import Counter
