"""Exact clock projection of a fixed productive block-entry word.

This solves necessary affine integer constraints only. It does not
assert positivity, physical margin, or canonical reachability.
"""
from fractions import Fraction as F
from math import isqrt

def v2(x):
    x=F(x)
    if not x:return 10**30
    n=abs(x.numerator);d=x.denominator
    return (n&-n).bit_length()-(d&-d).bit_length()

def clock_projection(word,blocks):
    """Return None or an exact parametrization of all integer (x0,Theta0).

    The result means Theta0 = theta_residue (mod 2^theta_bits),
    x0 = anchor_slope*Theta0 + anchor_offset (mod 2^anchor_bits).
    Each intermediate x is integral and has exactly the requested v2.
    """
    if not word:raise ValueError('empty word')
    # x_i = a*x0+b*Theta0+c; clock_i = Theta0+3*time.
    a,b,c=F(1),F(0),F(0);elapsed=0
    clock_r=clock_h=0
    anchor_p=anchor_r=anchor_h=None
    for i,q in enumerate(word):
        den=max(a.denominator,b.denominator,c.denominator)
        if den&(den-1):raise ValueError('non-dyadic block map')
        aa,bb,cc=(int(z*den) for z in (a,b,c))
        assert aa%2  # cumulative coefficient has exact denominator den
        h=v2(den)+q+1;mod=1<<h
        inv=pow(aa,-1,mod)
        p=(-bb*inv)%mod;r=((den*(1<<q)-cc)*inv)%mod
        if anchor_h is None:
            anchor_p,anchor_r,anchor_h=p,r,h
        else:
            common=min(h,anchor_h);cm=1<<common
            d=(p-anchor_p)%cm;e=(anchor_r-r)%cm
            s=min(v2(d),common)
            if e%(1<<s):return None
            if s<common:
                nh=common-s;nm=1<<nh
                nr=((e>>s)*pow(d>>s,-1,nm))%nm
                if (nr-clock_r)%(1<<min(nh,clock_h)):return None
                if nh>clock_h:clock_r,clock_h=nr,nh
            if h>anchor_h:anchor_p,anchor_r,anchor_h=p,r,h
        if i+1<len(word):
            block=blocks[q];mul=-block['alpha']/2
            const=6*block['d']+6*block['k']-block['B']/2
            a,b,c=mul*a,mul*b+2,mul*c+6*elapsed+const
            elapsed+=block['T']
    return dict(theta_residue=clock_r,theta_bits=clock_h,
                anchor_slope=anchor_p,anchor_offset=anchor_r,anchor_bits=anchor_h,
                elapsed=elapsed,
                step_residue=((clock_r-5)*pow(3,-1,1<<clock_h))%(1<<clock_h))

def lift(projection,theta_multiple=0,x_multiple=0):
    theta=projection['theta_residue']+(theta_multiple<<projection['theta_bits'])
    mod=1<<projection['anchor_bits']
    x=(projection['anchor_slope']*theta+projection['anchor_offset'])%mod+x_multiple*mod
    return x,theta

def fire_projection(projection):
    """Impose the exact fire identity x0=Theta0-1; return its time cylinder."""
    if projection is None:return None
    p,r,h=(projection[k] for k in ('anchor_slope','anchor_offset','anchor_bits'))
    mod=1<<h
    assert p%2==0
    theta=((r+1)*pow(1-p,-1,mod))%mod
    ch=projection['theta_bits']
    if (theta-projection['theta_residue'])%(1<<min(h,ch)):return None
    assert h>=ch
    return dict(theta_residue=theta,bits=h,
                step_residue=((theta-5)*pow(3,-1,mod))%mod)

def floor_sum(n,m,a,b):
    """Exact sum floor((a*i+b)/m), 0<=i<n, allowing signed a,b."""
    if n<0 or m<=0:raise ValueError('invalid range/modulus')
    ans=0
    while True:
        qa,a=divmod(a,m);qb,b=divmod(b,m)
        ans+=qa*n*(n-1)//2+qb*n
        y=a*n+b
        if y<m:return ans
        n,b=divmod(y,m);m,a=a,m

def count_entry_lifts(projection,max_step):
    """Count exact (s,x0) lifts with 0<=s<=max_step and nonnegative
    reconstructed entry lambdas: Theta-1<=x0<=2Theta-5.
    This does not certify intermediate safety or canonical reachability.
    """
    if projection is None or max_step<0:return 0
    step0=projection['step_residue'];period=1<<projection['theta_bits']
    if step0>max_step:return 0
    n=(max_step-step0)//period+1
    theta0=3*step0+5;delta=3*period
    p,r,h=(projection[k] for k in ('anchor_slope','anchor_offset','anchor_bits'))
    mod=1<<h
    upper=floor_sum(n,mod,(2-p)*delta,(2-p)*theta0-5-r)
    lower=floor_sum(n,mod,(1-p)*delta,(1-p)*theta0-2-r)
    return upper-lower

def failure_pointer_interval(word,blocks):
    """Necessary root-pointer interval for a first safety failure at the
    final entry, using earlier safe entries and s_fire<=rho^2.
    None excludes this word. A nonempty interval is NOT a failure witness.
    """
    if len(word)<2:return None
    f=fire_projection(clock_projection(word,blocks))
    if f is None:return None
    E=0;previous_max=word[0]
    for i,q in enumerate(word[:-1]):
        if i:previous_max=max(previous_max,E+q)
        E+=blocks[q]['G']+1
    M=E+word[-1]
    assert f['bits']>=M+1
    seed=f['step_residue']
    if seed>M*M:return None
    root=isqrt(seed)
    if root*root<seed:root+=1
    lower=max(previous_max+1,E+1,root,5)
    if lower>M:return None
    return dict(min_pointer=lower,max_pointer=M,unique_fire_step=seed,
                total_loss=E,final_parameter=word[-1])

def unsafe_last_parameter_bound(prefix,blocks):
    """All-parameter bound for the output after this productive prefix.
    Assumes a first failure, exact prefix clocks, and C1 at the root
    and every earlier call used by the prefix.
    No crossing data for the candidate final parameter are needed.
    """
    if not prefix:raise ValueError('empty prefix')
    E=sum(blocks[q]['G']+1 for q in prefix)
    elapsed=sum(blocks[q]['T'] for q in prefix)
    C=12*E*E+6*elapsed+5
    fixed_prefix_bound=max(11,C.bit_length())
    # With C1 also at the earlier calls, a first failure has either
    # q<=17 or q<E and 2^q<60*E^3; see PROOF_FAILURE_BUDGET.md.
    loss_only_bound=max(17,(60*E**3).bit_length()-1)
    return min(fixed_prefix_bound,loss_only_bound),E,elapsed

def all_last_failure_candidates(prefix,blocks):
    """Exhaust ALL possible unsafe final valuations after a fixed prefix.
    Returned cases remain necessary arithmetic candidates only.
    This does not handle future failures after a safe final output.
    """
    bound,E,elapsed=unsafe_last_parameter_bound(prefix,blocks)
    candidates=[]
    for q in range(1,bound+1):
        candidate=failure_pointer_interval(tuple(prefix)+(q,),blocks)
        if candidate is None:continue
        # Additional exact total-mass bound at the final candidate.
        if 1<<q>6*(candidate['unique_fire_step']+elapsed)+5:continue
        candidates.append(candidate)
    return dict(last_parameter_bound=bound,total_loss=E,elapsed=elapsed,
                candidates=candidates)

def positive_fire_lift(word,blocks,minimum_step=0):
    """Produce a positive lambda lift of a consistent fire-rooted word.
    Physical coefficients may be chosen with adequate margin separately.
    This is a local realization, NOT canonical reachability.
    All entries except the last must be productive mixed-block inputs.
    """
    projection=fire_projection(clock_projection(word,blocks))
    if projection is None:return None
    h,c,d=F(1),F(-1),0;threshold=5
    for q in word[:-1]:
        b=blocks[q]
        h=2-b['alpha']*h/2
        c=2*d-b['alpha']*c/2+6*b['d']+6*b['k']-b['B']/2
        d+=3*b['T']
        assert 1<h<2
        # Strict positivity of both lambda components at the A output.
        requirements=((c+5-2*d)/(2-h),(d-c-1)/(h-1))
        threshold=max(threshold,*(r.numerator//r.denominator+1 for r in requirements))
    first=max(minimum_step,0,(threshold-5+2)//3)
    period=1<<projection['bits'];residue=projection['step_residue']
    multiple=max(0,(first-residue+period-1)//period)
    step=residue+multiple*period
    return dict(step=step,theta=3*step+5,x=3*step+4,
                sufficient_theta_threshold=threshold,clock_period=period)
