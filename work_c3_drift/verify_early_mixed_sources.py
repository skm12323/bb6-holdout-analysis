"""Check early-A source budgets on genuine finite symbolic exits."""
from pathlib import Path
from collections import Counter
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_claude_shifted'))
from shiftlib import Tables,sym_beta
from verify_b_prefix_encoding import encode
from verify_height_budget import height
from verify_copy_budget import rank

def main():
    T=Tables(8192,NS=64);sources=0;copies=0;kinds=Counter();max_as=0
    for P in range(512,8192):
        e=P.bit_length()-1;D=3*e+7;limit=P//D-4
        assert limit>=1
        E=(3*(P-1)**2+3).bit_length();K=(6*(P-1)**2+5).bit_length()-1
        assert 2*E+K<=2*D-1
        rows,status=sym_beta(T,P)
        assert status=='end'
        a_count=0
        for i,(j,d,beta,G,kind) in enumerate(rows[:-1]):
            jj,dd,bb,GG,_=rows[i+1]
            if kind in ('b','c'):
                assert GG+jj<G+j;copies+=1
            if kind!='a':continue
            a_count+=1
            if a_count>limit:continue
            assert GG<=(a_count+1)*D and jj<D
            assert GG+3*jj<P
            assert 1<=bb<=6*dd-1 and dd<=GG*P*P
            phi=3*dd+1-bb;c,bit=encode(phi,jj)
            assert GG+jj+2*rank(c.denominator)+height(c)<P
            sources+=1;kinds[''.join(r[4] for r in rows[:i+1])]+=1
        max_as=max(max_as,a_count)
    # Dyadic estimates used by the all-scale induction.
    assert all(2**e>15*e+24 for e in range(9,4097))
    out=dict(status='PASS',review_status='unreviewed',root_range=[512,8191],
             roots=7680,certified_a_outputs=sources,checked_copy_drops=copies,
             maximum_observed_a_count=max_as,observed_source_histories=dict(kinds),
             scope='Actual finite symbolic exits. Long mixed histories and the general step bound rely on the analytic proof, not extrapolation from observed histories.')
    Path(__file__).with_name('early_mixed_sources_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
