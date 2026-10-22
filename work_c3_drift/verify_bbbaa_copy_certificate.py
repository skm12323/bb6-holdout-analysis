"""Compressed source certificate for BBBAA with intermediate parameter five."""
from pathlib import Path
from fractions import Fraction as F
import json
from affine_origin import Linear,Origin,v2
from verify_shift_transport import Calendar,val
from verify_height_budget import height
from verify_copy_budget import rank

def main():
    cal=Calendar(512);sources=[];copies=0
    parents=[F(i) for i in range(-12,16)]+[F(10,3),F(26,3),F(-1,3)]
    for p in range(5,4097):
        row=cal.crossing(p-1)
        if not row['odd'] or row['kind']!='a':continue
        k=row['time']//2
        if val(6*k-4)!=5:continue
        assert p>=17
        m=val(9*k+10);assert 5<=m<=p-4
        bounds={'L2':(p+6,False),'L1':(p+3,False),'L0':(p,True),'X0':(p+9,False)}
        s=Origin()
        for name in ('L2','L1','L0'):s.b(Linear({name:1}))
        assert s.beta.exact_valuation(bounds)==p
        s.a(k);assert s.beta.exact_valuation(bounds)==5
        s.a(1);assert s.beta.exact_valuation(bounds)==m and s.loss==8
        error=Linear({'X0':3*(1-s.alpha)})+3*(s.theta+s.beta*(-1))+9*k
        assert '1' not in error.terms
        assert all(v2(coef)+bounds[name][0]>=m+1 for name,coef in error.terms.items())
        P_lower=p+9;assert 8+m+2+height(F(10,3))<P_lower
        phi=F(10,3)+(1<<m)
        for cp in parents:
            cn=cp+F(4,3);rp=rank(cp.denominator);rn=rank(cn.denominator)
            assert rn<=max(rp,1)
            assert height(cn)<=height(cp)+2
            assert cp+phi-2==cn+(1<<m)
            rho=P_lower+3;j=rho+4
            old=j+2*rp+height(cp)
            new=12+m+2*rn+height(cn)
            assert old-new>=rho-P_lower
            copies+=1
        sources.append(dict(p=p,k=k,m=m,source_loss=8,deficit=11,
                            source_certificate_budget=m+12,root_lower=P_lower))
    assert sources
    assert all(9*(p-1)**2+20 < 1<<(p-2) for p in range(17,4097))
    out=dict(status='PASS',review_status='unreviewed',selected_calls=len(sources),
             parent_copy_checks=copies,sources=sources,
             scope='Canonical call data and affine separation. Huge BBBAA source occurrences use the earlier spectrum construction, not direct simulation; all-p lemma remains unreviewed.')
    Path(__file__).with_name('bbbaa_copy_certificate_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='sources'}))

if __name__=='__main__':main()
