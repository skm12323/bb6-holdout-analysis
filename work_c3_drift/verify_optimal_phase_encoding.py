from pathlib import Path
from fractions import Fraction as F
import json
from optimal_phase_encoding import optimal,counting_bound
from verify_height_budget import height
from verify_copy_budget import rank

def main():
    rows=[];checked=0;brute_checked=0
    for m in range(1,13):
        M=1<<m;costs=[];worst=None
        for phi in range(M):
            result=optimal(phi,m);costs.append(result['cost']);checked+=1
            assert result['cost']<=2*m
            c=result['c'];bit=result['bit']
            residue=c.numerator*pow(c.denominator,-1,2*M)+bit*M
            assert (residue-phi)%(2*M)==0
            other=optimal(phi+M,m)
            assert other['cost']==result['cost'] and other['c']==c and other['bit']==1-bit
            if worst is None or result['cost']>worst['cost']:
                worst=dict(phi=phi,cost=result['cost'],phase=str(c),rank=result['rank'],height=result['height'])
        if m<=7:
            brute=[2*m+1]*M
            for r in range(m+1):
                Q=3**r;h=2*m-2*r;inv=pow(Q,-1,M)
                for C in range((1-h)*Q,(2+h)*Q+1):
                    c=F(C,Q);cost=2*rank(c.denominator)+height(c)
                    key=(C*inv)%M;brute[key]=min(brute[key],cost)
            assert brute==costs;brute_checked+=M
        rows.append(dict(m=m,classes=M,maximum_minimum_cost=max(costs),
                         classes_affordable_with_S_eq_m=sum(c<=m for c in costs),worst=worst))
    assert counting_bound(64)<1<<64
    out=dict(status='PASS',review_status='unreviewed',phase_classes_checked=checked,
             independently_bruteforced_classes=brute_checked,rows=rows,
             rank_height_bound_at_64=str(counting_bound(64)),total_classes_at_64=str(1<<64),
             scope='Optimal local phase encoding, not canonical reachability or continuation safety.')
    Path(__file__).with_name('optimal_phase_encoding_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
