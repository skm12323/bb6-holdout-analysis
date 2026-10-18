"""Check low-deficit c-entry reductions using canonical calendar records.

The all-scale proof is separate. Finite checks do not establish EXT globally.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json

from search_roots import Calendar,val


def walk(calendar,j,x,theta,limit=100):
    out=[];G=0
    for _ in range(limit):
        assert x>0 and val(x)==j
        out.append((j,x,theta,G))
        r=calendar.crossing(j-1)
        if not r['odd']:return out
        if r['kind']=='a':
            xn=2*theta+3*r['time']-x/2
        else:
            ratio=(r['head_ratio']+2*r['tail_ratio'])/2
            xn=ratio*x+r['head_lambda']+2*r['tail_lambda']+3
        assert xn.denominator==1
        x=F(xn);theta+=3+3*r['time'];G+=1+r['epsilon'];j=val(x)
    raise AssertionError('work limit: not interpreted as termination')


def first_fire(calendar,P):
    modulus=1 << (P-1)
    base=(-2*pow(3,-1,modulus)) % modulus
    for t in range(8):
        k=base+t*modulus
        if k<1 or 1+val(3*k+2)!=P:continue
        fire=calendar.preceding_fire_by_time(2*k)
        if fire['k']==k:return fire
    raise AssertionError(('no sampled canonical fire',P))


def main():
    calendar=Calendar(512)
    kinds=Counter();examples=[];state_checks=0
    aa_checks=0;ancestry_checks=0
    for P in range(5,257):
        first=calendar.crossing(P-1)
        if not first['odd']:continue
        category=None
        if first['kind']=='a':
            category='A';p=P;k=first['time']//2
        elif first['kind']=='b':
            y=3*first['time']+4;p=val(y)
            second=calendar.crossing(p-1)
            if second['odd'] and second['kind']=='a':
                category='BA';k=second['time']//2
        if category is None:continue
        fire=first_fire(calendar,P)
        rho=fire['pointer'];s0=2*fire['k'];x0=3*s0+4
        assert val(x0)==P and P<rho
        n=rho+2
        row=calendar.crossing(n)
        expected_epsilon=3 if category=='A' else 5
        assert row['kind']=='c' and row['odd'] and row['epsilon']==expected_epsilon
        theta=3*row['time']+4
        x=theta+row['tail_lambda']
        if category=='A':
            assert x==3*x0//2+6*k+2
            assert theta==x0+6*k+3
            reference_x=F(6*k+2)
            reference_theta=reference_x+1
            q=val(reference_x)
            assert val(x-reference_x)==P-1
            assert val(theta-reference_theta)==P
            sigma=rho-1
        else:
            assert x==13*x0//8+3*y//2+6*k
            assert theta==x0+y+2+6*k
            reference_x=F(x)
            reference_theta=reference_x+2
            q=1+val(k)
            assert theta-reference_theta==-5*x0//8-y//2
            assert val(theta-reference_theta)==p-1
            assert P>=p+3
            sigma=rho-3
        assert val(x)==q and q<p-1
        actual=walk(calendar,q,F(x),F(theta))
        reference=walk(calendar,q,reference_x,reference_theta)
        assert len(actual)==len(reference)
        for a,b in zip(actual,reference):
            ja,xa,ta,ga=a;jb,xb,tb,gb=b
            assert ja==jb and ga==gb
            assert ja+ga<=q
            assert sigma-ga>ja
            assert min(val(xa-xb),val(ta-tb))>=p-1-ga
            state_checks+=1
        if category=='A':
            assert tuple(z[0] for z in reference)==calendar.kernels[q]['word']
            # Examine all subsequent c crossings in this A-initial source epoch.
            source_walk=walk(calendar,P,F(x0),F(x0+1))
            if len(source_walk)>2:
                qfirst=source_walk[1][0]
                entry=calendar.crossing(qfirst-1)
                assert entry['odd']
                refx=F(entry['head_lambda']+2*(entry['tail_lambda'] or 0)+3)
                reftheta=F(3*entry['time']+5)
                refj=val(refx)
                refsigma=qfirst-1-entry['epsilon']
                refwalk=walk(calendar,refj,refx,reftheta)
                assert len(refwalk)==len(source_walk)-2
                isfire=entry['kind'] in ('a','b')
                pointer=qfirst-1 if entry['kind'] in ('a','c') else qfirst-2
                pending=0 if isfire else 1
                a_count=1
                for i,(src,ref) in enumerate(zip(source_walk[2:],refwalk)):
                    previous_type=calendar.crossing(source_walk[i+1][0]-1)['kind']
                    if previous_type=='a':a_count+=1
                    assert src[0]==ref[0]
                    assert src[3]==1+(1+entry['epsilon'])+ref[3]
                    precision=refsigma-ref[3]
                    assert min(val(src[1]-ref[1]),val(src[2]-ref[2]))>=precision
                    # Only the first comparison (i==0) is exercised and implemented; later mixed-history
                    # steps would need the reference pointer advanced, so they are not checked here.
                    if previous_type=='a' and i==0:
                        n_outer=rho+1+a_count
                        outer=calendar.crossing(n_outer)
                        assert outer['kind']=='c' and outer['time']==(src[2]-5)//3
                        n_ref=pointer+1 if (i==0 and isfire) else pointer
                        inner=calendar.crossing(n_ref)
                        assert inner['kind'] in ('b','c') and inner['odd']
                        assert inner['time']==(ref[2]-5)//3
                        assert n_ref+1<n_outer+1
                        lhs=walk(calendar,src[0],src[1],src[2]-1)
                        rhs=walk(calendar,ref[0],ref[1],ref[2]-1)
                        assert [z[0] for z in lhs]==[z[0] for z in rhs]
                        assert all(z[0]+z[3]<precision for z in rhs)
                        assert all(z[0]+z[3]<rho-src[3] for z in lhs)
                        ancestry_checks+=1
                        if i==0 and previous_type=='a':
                            l=entry['time']//2;y=6*l+4
                            assert src[1]-y==F(5*x0,4)+3*(3*k+1)
                            assert src[2]-1-y==x0+2*(3*k+1)
                            assert val(src[1]-y)==qfirst-1
                            assert val(src[2]-1-y)==qfirst
                            aa_checks+=1
                    if i+1<len(refwalk):
                        rcall=calendar.crossing(ref[0]-1)
                        pointer+=2-min(pending,2)
                        pending=1 if rcall['kind']=='a' else 2
        kinds[category]+=1
        if len(examples)<12 or (category=='BA' and not any(e['history']=='BA' for e in examples)):
            examples.append(dict(history=category,P=P,p=p,q=q,
                                 outer_index_bits=(n+1).bit_length(),
                                 tail=[z[0] for z in actual]))
    # Small productive A cases and the all-scale size bound's bases.
    small=[]
    for p in range(5,10):
        row=calendar.crossing(p-1)
        if row['odd'] and row['kind']=='a':
            k=row['time']//2
            assert val(6*k+2)<p-1 and val(6*k)<p-1
            small.append((p,k))
    inequalities=0
    for p in range(10,4097):
        assert 3*(p-1)**2+2<1 << (p-1)
        inequalities+=1
    assert kinds['A'] and kinds['BA']
    # Exercise nonterminal phase-2 shadows with algebraic outer lifts.
    # The inner fire and subsequent call table are canonical. P=p+3 below
    # is deliberately NOT claimed to be its actual b-parent parameter.
    algebra_cases=0;algebra_states=0;algebra_examples=[]
    for p in range(10,257):
        row=calendar.crossing(p-1)
        if not row['odd'] or row['kind']!='a':continue
        k=row['time']//2;q=1+val(k)
        if q<5 or not calendar.crossing(q-1)['odd']:continue
        inner=first_fire(calendar,p)
        y=6*inner['k']+4
        P=p+3
        for U in (1,3,7):
            x0=(1 << P)*U
            x=F(13*x0//8+3*y//2+6*k)
            theta=F(x0+y+2+6*k)
            assert val(x)==q and val(theta-x-2)==p-1
            actual=walk(calendar,q,x,theta)
            reference=walk(calendar,q,x,x+2)
            assert len(actual)==len(reference)>1
            for a,b in zip(actual,reference):
                assert a[0]==b[0] and a[3]==b[3] and a[0]+a[3]<=q
                assert min(val(a[1]-b[1]),val(a[2]-b[2]))>=p-1-a[3]
                algebra_states+=1
            algebra_cases+=1
            if len(algebra_examples)<5:
                algebra_examples.append(dict(p=p,q=q,tail=[a[0] for a in actual]))
    assert algebra_cases>0
    # The last turn's fake epsilon-3 source violates the mandatory first-A phase.
    fake_theta_real=3*27+5;fake_x=160
    assert (fake_theta_real-2) % (1 << val(fake_x)) != 0
    result=dict(result='PASS',review_status='unreviewed',
                canonical_source_histories=dict(kinds),shadow_state_checks=state_checks,
                inequality_checks=inequalities,small_productive_a_cases=small,
                canonical_AA_reductions=aa_checks,
                later_A_initial_c_ancestry_reductions=ancestry_checks,
                noncanonical_outer_algebra_cases=algebra_cases,
                noncanonical_outer_shadow_states=algebra_states,
                noncanonical_outer_examples=algebra_examples,
                examples=examples,fake_epsilon3_source_excluded=True,
                scope='Canonical low-deficit examples and exact identities; proposed all-scale reductions require review.')
    Path(__file__).with_name('low_deficit_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
