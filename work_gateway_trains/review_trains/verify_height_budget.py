"""Joint rank/height copy reserve with explicit extra-bit control."""
import sys
sys.path.insert(0,'D:/math_cc/work_c3_drift')
from pathlib import Path
from fractions import Fraction as F
from math import ceil
from collections import Counter
import json
from verify_copy_budget import Calendar,small_full,rank,val

def height(c):return ceil(max(F(0),1-c,c-2))

def main():
    cal=Calendar(256);sources=small_full(128);counts=Counter()
    small_fire_gaps=[]
    for n,row in sources.items():
        if n<16 and row['odd'] and row['typ']=='a':
            P=val(3*row['tau']+4)
            assert n-P>=3;small_fire_gaps.append(dict(rho=n,P=P,gap=n-P))
    assert all(3*n*n+4 < 1<<(n-2) for n in range(16,4097))
    assert all(3*(P+10)**2+4 < 1<<P for P in range(14,4097))
    parents=[F(1),F(2),F(-2),F(14),F(10,3),F(26,3),F(-1,3),F(-17,3),F(46,9),F(62,9)]
    for n,row in sources.items():
        if not row['odd'] or row['typ'] not in ('b','c'):continue
        fire=cal.preceding_fire_by_pointer(n);rho=fire['pointer'];P=fire['J']
        cx,lam=row['x'];omega=row['omega'];sigma=val(cx);Gs=rho-sigma
        phi=3*row['tau']+5-lam;j=n+1;eps=n-sigma
        candidates={F(C,3**r) for r in range(4) for C in range(-2*3**r,4*3**r+1)}
        for cs in candidates:
            Q=cs.denominator;rs=rank(Q);hs=height(cs)
            mod=1<<(omega+1)
            residue=cs.numerator*pow(Q,-1,mod)%mod
            diff=(phi-residue)%mod
            if diff not in (0,1<<omega) or Gs+omega+2*rs+hs>P:continue
            bs=diff//(1<<omega)
            for cp in parents:
                rp=rank(cp.denominator);hp=height(cp);cn=cp+cs-2
                rn=rank(cn.denominator);hn=height(cn)
                assert rn<=max(rp,rs) and hn<=hp+hs+1
                D=cp.numerator*pow(cp.denominator,-1,1<<(j+1))%(1<<(j+1))
                x=1<<j;theta=x+D;y=cx+lam;t=theta+3+3*row['tau']
                assert val(F(t-y)-cn-bs*(1<<omega))>=omega+1
                old=j+2*rp+hp;new=1+eps+omega+2*rn+hn
                assert new<=old-(rho-P)+1<=old
                counts[row['typ']]+=1
    # Matching rank-zero source bits can still have an uncertified large height.
    assert (9-1)%4==0 and height(F(9))==7
    assert -3+height(F(1)+F(9)-2)-height(F(1))==3
    paired=0
    for cp in parents:
        for c in (cp,3-cp):
            assert height(3-c)==height(c)
            assert height(4+c/3)<=height(c)+3
            paired+=1
    out=dict(status='PASS',review_status='unreviewed',height_copy_checks=dict(counts),
             reflection_gateway_checks=paired,uncertified_height_control_increase=3,
             small_fire_gaps=small_fire_gaps,
             scope='Real small copy coefficients with synthetic eligible phase certificates. No claim of global certificate existence.')
    Path(__file__).with_name('height_budget_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
