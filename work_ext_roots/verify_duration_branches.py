"""Exact branch reductions and deep genuine duration witnesses."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json

from verify_low_deficit import Calendar,walk,val


def kernel(calendar,H):
    """Exact beta S(H); avoids constructing 2^H at huge H."""
    j=H;u=0;theta=1;duration=loss=0;word=[H]
    for _ in range(100):
        row=calendar.crossing(j-1)
        duration+=1+row['time']
        if not row['odd']:return dict(delta=(duration+2)//2,word=word,loss=loss)
        if row['kind']=='a':
            x=2*theta+3*row['time']-((u << (j-1)) if u else 0)
        else:
            x=row['head_lambda']+2*row['tail_lambda']+3
            if u:
                x+=(row['head_ratio']+2*row['tail_ratio'])*(1 << (j-1))*u
        assert x>0 and getattr(x,'denominator',1)==1
        x=int(x);loss+=1+row['epsilon'];j=val(x)
        assert j+loss<H
        u=x >> j;theta+=3+3*row['time'];word.append(j)
    raise AssertionError('unresolved work limit')


def main():
    calendar=Calendar(8208)
    count=Counter()
    for q in range(5,8193):
        row=calendar.crossing(q-1)
        if not row['odd']:continue
        for U in (1,3,7):
            x=F((1 << q)*U)
            if row['kind']=='b':
                p=row['omega'];y=3*row['time']+4
                assert p<q-2
                original=walk(calendar,q,x,x+3)
                x1=3*x/4+y;theta1=x+y+2
                assert val(theta1-x1-2)==q-2
                ref=walk(calendar,p,x1,x1+2)
                assert [s[0] for s in original[1:]]==[s[0] for s in ref]
                assert all(s[0]+s[3]<=q for s in original)
                count['PLUS_b_all_lifts']+=1
                if p in (5,8):
                    minus=walk(calendar,q,x,x-1)
                    assert [s[0] for s in minus]==[q,p,1 if p==5 else 3]
                    assert all(s[0]+s[3]<=q for s in minus)
                    count['MINUS_b_5_8_lifts']+=1
            elif row['kind']=='a':
                k=row['time']//2;z=F(6*k+6);r=val(z)
                assert r<q-1
                original=walk(calendar,q,x,x+3)
                ref=walk(calendar,r,z,z)
                assert [s[0] for s in original[1:]]==[s[0] for s in ref]
                assert all(s[0]+s[3]<q-1 for s in ref)
                count['PLUS_a_to_Z_finite_lifts']+=1
    # Independently cross-check the large-index kernel routine in a finite range.
    for H in range(5,513):
        k=kernel(calendar,H);old=calendar.kernels[H]
        assert (k['delta'],tuple(k['word']),k['loss'])==(old['delta'],old['word'],old['loss'])
    witnesses=[]
    for family,D in (('minus',((1 << 64)-1)//3),('plus',(1 << 64)+1)):
        fire=calendar.preceding_fire_by_time(2*D)
        found=None
        for H in range(fire['pointer']-128,fire['pointer']+129):
            if kernel(calendar,H)['delta']==D:
                found=H;break
        assert found is not None
        z=6*D+2 if family=='minus' else 6*D-6
        theta=z-1 if family=='minus' else z+3
        assert val(z)==65
        tail=walk(calendar,65,F(z),F(theta))
        assert [s[0] for s in tail]==[65,5,1]
        assert max(s[0]+s[3] for s in tail)==65<found
        witnesses.append(dict(family=family,H=found,delta=D,initial_parameter=65,
                              word=[s[0] for s in tail],max_loss_parameter_record=65))
    result=dict(result='PASS',review_status='unreviewed',branch_checks=dict(count),
                independent_kernel_comparisons=508,genuine_duration_witnesses=witnesses,
                scope='PLUS b and selected MINUS b branch proofs are algebraic; PLUS a-to-Z closure only checked finitely. No global EXT claim.')
    Path(__file__).with_name('duration_branch_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
