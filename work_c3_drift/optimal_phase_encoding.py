"""Exact minimum of 2*rank+height for a finite phase class; not a tail proof."""
from fractions import Fraction as F
from verify_height_budget import height
from verify_copy_budget import rank

def optimal(phi,m):
    M=1<<m;best=None
    # A rank-m height-zero representation costs <=2m, so primitive
    # denominators of rank >m cannot improve the minimum.
    for r in range(m+1):
        Q=3**r;res=(phi*Q)%M;k=(Q-res)//M
        # Closest lattice values below/above the interval [Q,2Q].
        for C in (res+k*M,res+(k+1)*M):
            c=F(C,Q);rr=rank(c.denominator);cost=2*rr+height(c)
            if best is None or cost<best[0]:best=(cost,c,rr)
    cost,c,r=best
    delta=(phi-c.numerator*pow(c.denominator,-1,2*M))%(2*M)
    assert delta in (0,M)
    return dict(cost=cost,c=c,rank=r,height=height(c),bit=delta//M)

def counting_bound(S):
    return sum((2*(S-2*r)+1)*3**r+1 for r in range(S//2+1))
