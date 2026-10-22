"""Sparse dyadic affine constants; an unresolved valuation is never a proof."""
from fractions import Fraction as F

def v2(q):
    q=F(q)
    if not q:return None
    a=abs(q.numerator);b=q.denominator
    return (a&-a).bit_length()-(b&-b).bit_length()

class Linear:
    def __init__(self,terms=None):
        self.terms={k:F(v) for k,v in (terms or {}).items() if v}
    @staticmethod
    def constant(n):return Linear({'1':n})
    def __add__(self,other):
        if not isinstance(other,Linear):other=Linear.constant(other)
        out=self.terms.copy()
        for k,v in other.terms.items():out[k]=out.get(k,F(0))+v
        return Linear(out)
    __radd__=__add__
    def __mul__(self,c):return Linear({k:v*F(c) for k,v in self.terms.items()})
    __rmul__=__mul__
    def evaluate(self,values):
        return sum((v*(1 if k=='1' else values[k]) for k,v in self.terms.items()),F(0))
    def exact_valuation(self,bounds):
        """bounds maps symbol to (lower valuation bound, whether exact)."""
        terms=[]
        for k,c in self.terms.items():
            low,exact=(0,True) if k=='1' else bounds[k]
            terms.append((v2(c)+low,exact,k))
        if not terms:return None
        minimum=min(v for v,_,_ in terms)
        leaders=[t for t in terms if t[0]==minimum]
        if len(leaders)==1 and leaders[0][1]:return minimum
        return None
    def serialize(self):return {k:str(v) for k,v in sorted(self.terms.items())}

class Origin:
    """x=alpha*X0+beta, Theta=X0+theta, X0=2^J*U."""
    def __init__(self):
        self.alpha=F(1);self.beta=Linear();self.theta=Linear.constant(1);self.loss=0
    def b(self,source_numerator):
        self.alpha*=F(3,4)
        self.beta=self.beta*F(3,4)+source_numerator
        self.theta=self.theta+source_numerator+-1
        self.loss+=2
    def a(self,k):
        self.alpha=2-self.alpha/2
        self.beta=2*self.theta+6*k+self.beta*F(-1,2)
        self.theta=self.theta+6*k+3
        self.loss+=1
