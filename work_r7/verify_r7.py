"""verify_r7.py -- checks for work_r7/PROOF.md.  Usage: python verify_r7.py [V=1000] [N=300000]
check1 [Class-A per v<=V]: symbolic E(w,v), w=2u+1: every odd step has x = 2^kappa*(alpha*u+beta),
        kappa constant, alpha>=0, beta=q at w=1; reports min beta (=min q over all odd w).
check2 [Class-C evidence]: concrete orbit from (3), n<N: q statistics, k vs log2 x, x mod 3."""
import sys, math, collections
V = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300000
class Und(Exception): pass
# affine forms in one symbol u>=0: (a, b) = a*u + b
def par(x):
    if x[0] % 2: raise Und()
    return x[1] % 2
def half(x):
    if x[0] % 2 or x[1] % 2: raise Und()
    return (x[0]//2, x[1]//2)
def add(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def ge3(x):
    if x[0] >= 0 and x[1] >= 3: return True
    if x[0] == 0: return False
    raise Und()
def Ts(L, rec):
    A = L[0]; b = L[1] if len(L) > 1 else (0,0); c = L[2] if len(L) > 2 else (0,0); R = L[3:]
    if par(A) == 0: return [add(A, b, c, (0,3))] + R
    x = add(A, b, b, (0,3)); kap = 0
    while par(x) == 0 and x != (0,0): x = half(x); kap += 1   # uniform halving of x (decisions uniform in u)
    rec.append((kap, x, len(L)))
    m = half(add(b, b, A, (0,-3))); st = [half(add(c, c, A, (0,1)))] + R
    while par(m) == 1 and ge3(m):
        st = [half(add(m, (0,3)))] + st; m = half(add(m, (0,-3)))
    if par(m) == 1: raise Exception('HALT')
    return [add(m, (0,4))] + st
gmin = None
for v in range(1, V+1):
    W = (6, 3); L = [add(W,(0,1))] + [(6<<i, 3<<i) for i in range(v-1)] + [(6<<(v-1), (3<<(v-1))-1)]
    rec = []
    while len(L) > 1: L = Ts(L, rec)
    for kap, q, ln in rec:
        assert q[0] >= 0 and q[1] % 2 == 1 and q[0] % 2 == 0      # q odd for every u
        assert q[1] >= 9, (v, kap, q)
        if gmin is None or q[1] < gmin[0]: gmin = (q[1], v, kap)
print('check1 OK v<=%d: every odd step of E(w,v): q = alpha*u+beta, alpha>=0 even, beta>=9; min beta=%s' % (V, gmin))
def T(L):
    A=L[0]; b=L[1] if len(L)>1 else 0; c=L[2] if len(L)>2 else 0; S=L[3:]
    if A%2==0: return [A+b+c+3]+S, None
    x=A+2*b+3; m=b+(A-3)//2; st=[c+(A+1)//2]+S
    while m%2==1 and m>=3: st=[(m+3)//2]+st; m=(m-3)//2
    assert m!=1
    return [m+4]+st, x
L=[3]; mq=10**9; mr=9.9; cnt=0; mod3=collections.Counter(); kx=-99
for n in range(N):
    L2,x=T(L)
    if x is not None and len(L)>1:
        cnt+=1; k=(x&-x).bit_length()-1; q=x>>k; mq=min(mq,q); mr=min(mr,q/math.sqrt(x)); mod3[x%3]+=1
        kx=max(kx,k-math.log2(x)/2)
    L=L2
print('check2 n<%d: %d non-singleton odd steps; min q=%d; min q/sqrt(x)=%.3f; max k-log2(x)/2=%.3f; x mod 3 counts=%s'%(N,cnt,mq,mr,kx,dict(mod3)))
# check3 [Class-C]: no odd-modulus congruence on x excludes powers of 2 (n<N)
xs=[]; L=[3]
for n in range(N):
    L2,x=T(L)
    if x is not None and len(L)>1: xs.append(x)
    L=L2
for M in [3,5,7,9,15,17,21,27,31,63,73,81,127,151,241,257]:
    R={x%M for x in xs}; P={pow(2,k,M) for k in range(400)}
    assert R & P, M
print('check3: for every tested odd M, x mod M meets the powers of 2; q mod 8 values:', sorted({(x>>((x&-x).bit_length()-1))%8 for x in xs}))
