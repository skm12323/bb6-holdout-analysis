"""Complete last-valuation/source filtering for a FIXED productive prefix.

Scope: first strict EXT tie, with EXT at smaller outer indices and actual
earlier source kernels. Passing gives necessary candidates, not reachability.
"""
from collections import Counter
from clock_words import clock_projection


def bounds(prefix,blocks):
    if not prefix:raise ValueError('nonempty productive prefix required')
    E=T=R=0
    for q in prefix:
        R=max(R,E+q)
        b=blocks[q];E+=b['G']+1;T+=b['T']
    fixed=max(14,(48*E*E+6*T+5).bit_length())
    loss=max(19,(203*E**3).bit_length()-1)
    return dict(loss=E,duration=T,previous_record=R,
                last_parameter_bound=min(fixed,loss),fixed_bound=fixed,loss_bound=loss)


def match(projection,theta,x):
    if (theta-projection['theta_residue']) & ((1 << projection['theta_bits'])-1):return False
    return not ((x-projection['anchor_slope']*theta-projection['anchor_offset'])
                & ((1 << projection['anchor_bits'])-1))


def inspect(prefix,blocks,source,include_small=False,noncanonical=False):
    info=bounds(prefix,blocks)
    E,T,R=info['loss'],info['duration'],info['previous_record']
    counts=Counter();candidates=[]
    # J<128 is optional diagnostics, outside the large-J endpoint theorem.
    # Its independent C1/mass bound is 2^q<=6*127^2+6T+5.
    diagnostic_bound=(6*127**2+6*T+5).bit_length()-1 if include_small else 0
    enumerated_bound=max(info['last_parameter_bound'],diagnostic_bound)
    for q in range(1,enumerated_bound+1):
        counts['final_parameters']+=1
        M=E+q
        if M<=R:
            counts['record_rejected']+=1;continue
        p=clock_projection(tuple(prefix)+(q,),blocks)
        if p is None:
            counts['word_rejected']+=1;continue
        upper=max(127 if include_small else 0,2*M)
        lower=2 if include_small else 128
        for J in range(lower,upper+1):
            if J>=128 and q>info['last_parameter_bound']:continue
            counts['source_indices']+=1
            row=source(J-1)
            if row is None:
                if not noncanonical: raise ValueError(('missing canonical source',J-1))
                continue
            if not row['odd'] or row['kind'] not in ('b','c'):continue
            counts['bc_sources']+=1
            if row['kind']=='b' and not R+3<=J<=M+2:continue
            gamma=1+row['epsilon']
            if not gamma+R<J<=gamma+M:continue
            counts['margin_survivors']+=1
            tau=row['time'];tail=row['tail_lambda'] or 0
            theta=3*tau+4;x=theta+tail
            if not match(p,theta,x):continue
            counts['source_congruence_survivors']+=1
            # Read the final numerator from the exact block maps, separately
            # from the projector, and check every earlier entry margin.
            value=x;clock=theta;loss=0
            for entry in prefix:
                assert getattr(value,'denominator',1)==1
                iv=int(value);valuation=(iv & -iv).bit_length()-1
                assert valuation==entry and entry<J-gamma-loss
                b=blocks[entry]
                value=-b['alpha']*value/2+2*clock+6*b['d']+6*b['k']-b['B']/2
                clock+=3*b['T'];loss+=b['G']+1
            assert value.denominator==1 and value>0
            iv=int(value);assert (iv & -iv).bit_length()-1==q
            if iv>6*(1+tau+T)-1:continue
            candidates.append(dict(J=J,kind=row['kind'],prefix=list(prefix),
                                   final_parameter=q,loss=E,gamma=gamma,
                                   final_coefficient_valuation=J-gamma-E,
                                   final_beta=iv))
    return dict(**info,enumerated_parameter_bound=enumerated_bound,
                counts=dict(counts),candidates=candidates,
                scope='J>=128' if not include_small else 'includes small J diagnostics; large-J endpoint theorem unchanged')
