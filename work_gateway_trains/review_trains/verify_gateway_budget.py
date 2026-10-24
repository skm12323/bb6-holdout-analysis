"""Exact paired-gateway algebra and its denominator-rank potential."""
import sys
sys.path.insert(0,'D:/math_cc/work_c3_drift')
from pathlib import Path
from math import gcd
import json
from verify_shift_transport import val
from verify_height_budget import height
from fractions import Fraction as F

def main():
    cases=0
    for r in range(9):
        Q=3**r
        for j in (64,96,128,256):
            for k in (j//4,j//2,j*j//4):
                C=(16-3*Q*k)%32
                while C%3==0:C+=32
                assert gcd(C,Q)==1 and val(3*Q*k+C)==4
                for bit in (0,1):
                    x=1<<j;D=C*pow(Q,-1,1<<(j+1))%(1<<(j+1))+bit*(1<<j)
                    theta=x+D
                    x1=2*theta+6*k-x//2;t1=theta+6*k+3
                    assert val(x1)==5
                    x2=2*t1+6-x1//2;t2=t1+9;m=val(x2)
                    assert m==val(Q*(9*k+12)+C) and m<=j-8
                    expected=((12*Q+C)*pow(3*Q,-1,1<<(m+1))+(1<<m))%(1<<(m+1))
                    assert (t2-x2-expected)%(1<<(m+1))==0
                    assert gcd(12*Q+C,3*Q)==1
                    G=7
                    assert G+2+m+2*(r+1)<G+j+2*r
                    hp=height(F(C,Q));hn=height(F(12*Q+C,3*Q))
                    assert hn<=hp+3
                    assert G+2+m+2*(r+1)+hn<G+j+2*r+hp
                    cases+=1
    out=dict(status='PASS',review_status='unreviewed',paired_gateway_checks=cases,
             joint_height_budget_checks=cases,
             scope='Synthetic calls satisfying the displayed algebraic hypotheses; not claimed canonical trajectories. All-scale size argument is analytic.')
    Path(__file__).with_name('gateway_budget_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
