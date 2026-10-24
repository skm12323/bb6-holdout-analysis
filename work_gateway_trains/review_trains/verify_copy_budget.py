"""Source-certified denominator inheritance through exact b/c copies."""
import sys
sys.path.insert(0,'D:/math_cc/work_c3_drift')
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json
from verify_shift_transport import Calendar,val
sys.path.insert(0,'D:/math_cc/work_global_ext/route_c')
from fdata import small_full

def rank(q):
    r=0
    while q%3==0:q//=3;r+=1
    assert q==1
    return r

def main():
    cal=Calendar(512);full=small_full(512);counts=Counter();maximum_source_rank=0
    control=None
    for n,row in full.items():
        if not row['odd'] or row['typ'] not in ('b','c'):continue
        fire=cal.preceding_fire_by_pointer(n);rho=fire['pointer'];P=fire['J']
        cx,lam=row['x'];omega=row['omega'];sigma=val(cx)
        Gs=rho-sigma;eps=n-sigma
        assert Gs>=0 and P<rho and omega<=P-Gs
        phi=3*row['tau']+5-lam;j=n+1
        for rs in range((P-Gs-omega)//2+1):
            maximum_source_rank=max(maximum_source_rank,rs)
            Qs=3**rs
            for source_bit in (0,1):
                Cs=(phi-source_bit*(1<<omega))*Qs+((1<<(omega+1)) if rs else 0)
                assert rank(F(Cs,Qs).denominator)==rs
                for rp in range(5):
                    Qp=3**rp;Cp=10
                    D=Cp*pow(Qp,-1,1<<(j+1))%(1<<(j+1))
                    for parent_bit in (0,1):
                        for u in (1,3):
                            x=(1<<j)*u;theta=x+D+parent_bit*(1<<j)
                            y=cx*u+lam;t=theta+3+3*row['tau']
                            assert val(y)==omega
                            phase=F(Cp,Qp)+F(Cs,Qs)-2+source_bit*(1<<omega)
                            rn=rank(phase.denominator)
                            assert rn<=max(rp,rs)
                            assert val(F(t-y)-phase)>=omega+1
                            G=7;old=G+j+2*rp;new=G+1+eps+omega+2*rn
                            assert old-new>=rho-P>=1
                            counts[row['typ']]+=1
        if control is None:
            # A high-rank approximation can match source bits while lacking
            # the stronger source budget. It must NOT be accepted as certified.
            rs=sigma-omega;Qs=3**rs;Cs=phi*Qs+(1<<(omega+1))
            phase=F(10)+F(Cs,Qs)-2;rn=rank(phase.denominator)
            assert val(F(Cs,Qs)-phi)>=omega+1
            delta=-(sigma-omega)+2*rn
            assert Gs+omega+2*rs>P and delta>0
            control=dict(n=n,source_parameter=P,source_rank=rs,
                         source_budget=Gs+omega+2*rs,potential_increase=delta)
    out=dict(status='PASS',review_status='unreviewed',exact_copy_checks=dict(counts),
             max_tested_source_rank=maximum_source_rank,uncertified_rank_control=control,
             scope='Real small source coefficients; synthetic matching phase representations constrained by the stated source budget. No assertion that all sources admit such a certificate.')
    Path(__file__).with_name('copy_budget_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
