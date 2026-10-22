"""Affine validation for three-b canonical lifts of selected catapults."""
from pathlib import Path
from fractions import Fraction as F
import json
from affine_origin import Linear,Origin,v2
from verify_shift_transport import Calendar,val,bounded_walk

def main():
    cal=Calendar(512);records=[]
    for m in range(5,19):
        modulus=1<<m;base=(-10*pow(9,-1,modulus))%modulus
        fire=None
        for lift in range(64):
            k=base+lift*modulus
            if k<1 or val(9*k+10)!=m:continue
            candidate=cal.preceding_fire_by_time(2*k)
            if candidate['k']==k:fire=candidate;break
        assert fire is not None
        p=fire['pointer']+1
        source=cal.crossing(p-1)
        assert source['kind']=='a' and source['odd'] and source['time']==2*k
        assert m+4<=p<=400000
        bounds={'L0':(p,True),'L1':(p+3,False),'L2':(p+6,False)}
        s=Origin()
        for key in ('L2','L1','L0'):s.b(Linear({key:1}))
        assert s.loss==6 and s.beta.exact_valuation(bounds)==p
        s.a(k)
        assert s.loss==7 and s.beta.exact_valuation(bounds)==5
        five_beta=s.beta.serialize()
        s.a(1)
        assert s.loss==8 and s.beta.exact_valuation(bounds)==m
        assert v2(s.alpha)==-8
        # 3*D=-9k modulo 2^(m+1), with every omitted term separately high.
        error=3*(s.theta+s.beta*(-1))+9*k
        assert '1' not in error.terms
        assert all(v2(c)+bounds[name][0]>=m+1 for name,c in error.terms.items())
        delta=((10-(1<<m))*pow(3,-1,1<<(m+1)))%(1<<(m+1))
        status,tail=bounded_walk(cal,1<<m,(1<<m)+delta,m+1,signed=True)
        assert status=='end' and max(j+g for j,g,_,_ in tail)<=m
        assert 8+m<p+9  # p3 >= p+9, sufficient for every suffix record
        records.append(dict(m=m,p=p,k=k,source_pointer=p-1,
                            known_suffix=[p,5]+[j for j,_,_,_ in tail],
                            beta_at_five=five_beta,beta_after_gateway=s.beta.serialize(),
                            suffix_record_bound=m+8))
    assert all(4*(j-1)**2+5 <= 1<<(j-2) for j in range(16,4097))
    out=dict(status='PASS',review_status='unreviewed',cases=len(records),
             largest_target_p=max(r['p'] for r in records),records=records,
             scope='Actual-source reachability is an existence proof using accepted spectrum/horizon imports. Huge lifted fires are not simulated.')
    Path(__file__).with_name('reachable_catapults_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}))
    print(json.dumps([{k:r[k] for k in ('m','p','known_suffix')} for r in records]))

if __name__=='__main__':main()
