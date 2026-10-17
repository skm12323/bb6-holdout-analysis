"""Exhaustive lazy-bit enumeration of the beta-walk over ALL integers X in [0,2^B) of a 1-parameter family.
Quantities are affine forms (p*X+r)/2^s; X is revealed bit by bit only when a valuation needs it.
family 'a': (d,bx)=(1+X,3X+2), X even      (route a, X=tau(J-1))
family 'b': (d,bx)=(1+X,3X+4), X even      (route b)
Output: for each leaf (cylinder of X) the tail (list of j's after chain 1), #non-descents, measure."""
import sys
from collections import Counter
from core import load, v2
sys.setrecursionlimit(100000)
T=load(30000)

class Aff:
    __slots__=('p','r','s')
    def __init__(s_,p,r,s=0): s_.p=p; s_.r=r; s_.s=s
BFULL=[10**9]
def val_query(N_p,N_r,M,Xlow):
    """v2(N_p*X+N_r) given X mod 2^M (X exact once M>=BFULL). Returns v or None if undetermined."""
    if N_p==0: return v2(N_r) if N_r else 10**9
    if M>=BFULL[0]:
        w=N_p*Xlow+N_r; assert w!=0; return v2(w)
    P=M+v2(N_p)
    w=(N_p*Xlow+N_r)%(1<<P)
    if w: return v2(w)
    return None

def run(family,B,maxleaves=10**7):
    off={'a':2,'b':4}[family]; BFULL[0]=B
    stats=Counter(); ndstats=Counter(); worst=[]; leaves=[0]; jhist=Counter()
    # stack of (M,Xlow, state) ; state = (stage, j, d=(p,r), bu=(p,r,s), tail, nd)
    # we simply re-run the walk from scratch for each partial assignment (walks are short)
    def walk(M,Xlow):
        # returns ('need',) or ('done',tail,nd)
        dp,dr=1,1              # d = dp*X+dr  (dp is always 1)
        bp,br=3,off            # beta_x = bp*X+br (integer affine)
        j=val_query(bp,br,M,Xlow)
        if j is None: return ('need',)
        tail=[]; nd=0
        # beta_u = (bp X + br)/2^j  : keep numerator and shift
        up,ur,us=bp,br,j
        while True:
            n=j-1
            if n not in T: return ('done',tail,nd,'OUT')
            row=T[n]
            if not row['odd']: return ('done',tail,nd,'END')
            if row['typ']=='a':
                # bx = 2(3d+1)+3tau - 2^n*bu = 6dpX+6dr+2+3tau - (up X+ur)*2^(n-us)
                sh=n-us
                if sh>=0:
                    np_=6*dp-(up<<sh); nr=6*dr+2+3*row['tau']-(ur<<sh); ns=0
                else:
                    np_=(6*dp<<(-sh))-up; nr=((6*dr+2+3*row['tau'])<<(-sh))-ur; ns=-sh
            else:
                cxW,lxW,jW=row['W']
                np_=up*cxW; nr=ur*cxW+(lxW<<us); ns=us
            dr+=1+row['tau']
            vv=val_query(np_,nr,M,Xlow)
            if vv is None: return ('need',)
            jn=vv-ns
            assert jn>=0
            if jn>=j: nd+=1
            tail.append(jn); j=jn; up,ur,us=np_,nr,ns+jn
    stack=[(1,0)]          # X even: bit0 = 0
    while stack:
        M,Xlow=stack.pop()
        res=walk(M,Xlow)
        if res[0]=='need':
            if M>=B:
                raise RuntimeError('undetermined at full precision')  # cannot happen: X exact
            stack.append((M+1,Xlow)); stack.append((M+1,Xlow|(1<<M)))
            continue
        _,tail,nd,why=res
        leaves[0]+=1
        meas=2.0**(-(M-1))
        stats[len(tail)]+=meas; ndstats[nd]+=1
        for jj in tail: jhist[jj]+=1
        if len(tail)>=3 or nd>0: worst.append((len(tail),nd,M,Xlow,tail,why))
        if leaves[0]>maxleaves: raise RuntimeError('too many leaves')
    return stats,ndstats,worst,leaves[0]

if __name__=='__main__':
    fam=sys.argv[1]; B=int(sys.argv[2])
    import time; t0=time.time()
    stats,nds,worst,nl=run(fam,B)
    print('family',fam,'B',B,'leaves',nl,'time %.1f'%(time.time()-t0))
    print(' tail-length measure',{k:round(v,10) for k,v in sorted(stats.items())})
    print(' non-descent leaf counts',dict(nds))
    worst.sort(key=lambda z:(-z[1],-z[0]))
    for w in worst[:10]: print(' ',w[:3],w[4],w[5])
