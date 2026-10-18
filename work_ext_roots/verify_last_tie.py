"""All last valuations on finite generic words; noncanonical positive control."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json

from search_roots import Calendar,build,clock_projection
from last_tie_filter import inspect


def main():
    calendar=Calendar(64)
    blocks={q:build(calendar,q) for q in range(5,64)}
    blocks={q:b for q,b in blocks.items() if b is not None}
    frontier=[(q,) for q in blocks]
    words=[];lengths=Counter()
    while frontier:
        following=[]
        for word in frontier:
            words.append(word);lengths[len(word)]+=1
            for q in blocks:
                if clock_projection(word+(q,),blocks) is not None:
                    following.append(word+(q,))
        assert not following or len(following[0])<=7
        frontier=following
    totals=Counter();survivors=[];largest=0;largest_diagnostic=0
    for word in words:
        result=inspect(word,blocks,calendar.crossing,include_small=True)
        totals.update(result['counts']);survivors+=result['candidates']
        largest=max(largest,result['last_parameter_bound'])
        largest_diagnostic=max(largest_diagnostic,result['enumerated_parameter_bound'])
    assert not survivors
    # Fake c source at X(9): actual local masses, C1 and S1, but NOT canonical.
    fake=dict(kind='c',time=27,epsilon=3,odd=True,
              head_ratio=F(1,8),head_lambda=7,
              tail_ratio=F(7,8),tail_lambda=75,omega=5)
    assert fake['head_lambda']+fake['tail_lambda']==3*fake['time']+1
    assert fake['time']<=9**2
    assert 64+448==1 << 9
    assert ((960 & -960).bit_length()-1)==6>5
    control=inspect((5,),blocks,lambda n:fake if n==9 else None,include_small=True,noncanonical=True)
    target=[c for c in control['candidates'] if c['J']==10 and c['final_parameter']==5]
    assert len(target)==1 and target[0]['final_beta']==96
    # Independent pair replay: first chain (960,160), base (30,5), tail (544,3).
    head=(16*30,16*5+7)
    x=(head[0]+2*544,head[1]+2*3+3)
    assert x==(1568,96)
    assert (x[0]&-x[0]).bit_length()==(x[1]&-x[1]).bit_length()==6
    inequalities=0
    for q in range(15,4096):
        assert 48*q*q<1 << (q-1);inequalities+=1
    for q in range(20,4096):
        assert 96*(q+1)*q*q+6*q+5<1 << q;inequalities+=1
    for E in range(1,10000):
        assert 96*(E+1)*E*E+6*E+5<=203*E**3;inequalities+=1
    result=dict(result='PASS',review_status='unreviewed',
                productive_source_parameters=len(blocks),prefixes=len(words),
                prefix_lengths=dict(sorted(lengths.items())),
                largest_last_parameter_bound=largest,filter_counts=dict(totals),
                largest_diagnostic_parameter_bound=largest_diagnostic,
                canonical_candidates=survivors,inequality_checks=inequalities,
                noncanonical_positive_control=target,
                scope='Exhaustive final valuations for these finite prefixes only; source control is deliberately noncanonical, not a machine counterexample.')
    Path(__file__).with_name('last_tie_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
