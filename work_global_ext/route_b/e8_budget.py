"""Integer checks of the inequalities used in Theorems L' (non-descent budget) and L'' (chain budget with
C2-log at small indices).  All logs are replaced by exact integer floor-logs (bit_length) so the check is exact.
  g      := floor(log2(12 J^2))            (>= every j_t, t>=1, while d_t<=2J^2)
  L      := floor(J/(3 l)),  l := floor(log2 J)   (non-descent budget)
  chains <= (L+1)(g-3)                     (descending runs between non-descents)
  dbound : 1+(J-1)^2 + chains*(1+(g-1)^2) <= 2J^2
  h1     >= J-1-max(eps1)-g1, eps1 <= max(3, 2 floor(log2(3(J-1)^2+3)) -1), g1 := floor(log2(6(J-1)^2+5))
  L'     : h1 - L*(g-4) >= 1
  L''    : E := 2*floor(log2(3(g-1)^2+3)) ; L2 := floor((J-g-1-G1)/E), G1 := 1+eps1 ;
           need L2>=L (so L'' is weaker than Theorem L) and dbound with chains=L2+1."""
import random
def flog(x): return x.bit_length()-1          # floor(log2 x), x>=1
def check(J):
    l=flog(J); g=flog(12*J*J); L=J//(3*l)
    chains=(L+1)*(g-3)
    db=1+(J-1)**2+chains*(1+(g-1)**2)<=2*J*J
    eps1=max(3,2*flog(3*(J-1)**2+3)-1); g1=flog(6*(J-1)**2+5)
    h1=J-1-eps1-g1
    Lp=h1-L*(g-4)>=1
    E=2*flog(3*(g-1)**2+3); G1=1+eps1; L2=(J-g-1-G1)//E
    db2=1+(J-1)**2+(L2+1)*(1+(g-1)**2)<=2*J*J
    return db and Lp and db2 and L2>=L, (L,L2,E)
ok=[];bad=[]
for e in list(range(10,200))+[256,512,1024,2048,4096]:
    r,info=check(1<<e); (ok if r else bad).append(e)
random.seed(1)
for _ in range(20000):
    J=random.randrange(1<<10,1<<random.randrange(11,300)); r,_=check(J)
    if not r: bad.append(J)
print('powers ok:',len(ok),'bad:',bad[:10])
for e in (10,20,64,1024,4096):
    r,(L,L2,E)=check(1<<e); print('J=2^%d: L=floor(J/3l)=%d, L\'\'=%d  (=J/%.1f), E=%d'%(e,L,L2,(1<<e)/max(L2,1),E))
