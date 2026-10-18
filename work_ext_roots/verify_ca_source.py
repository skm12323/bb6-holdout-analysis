"""An actual CA-history c source, plus exact reduced-fire shadow checks."""
from fractions import Fraction as F
from pathlib import Path
import json
import time

from verify_low_deficit import Calendar,first_fire,walk,val


def main():
    started=time.monotonic()
    P=6133
    calendar=Calendar(6144)
    print('calendar ready',round(time.monotonic()-started,2),flush=True)
    copied=calendar.crossing(P-1)
    assert copied['kind']=='c' and copied['epsilon']==3 and copied['odd']
    inner=calendar.preceding_fire_by_pointer(P-1)
    rho_inner=inner['pointer'];P0=inner['J'];y0=6*inner['k']+4
    assert P==rho_inner+3 and val(y0)==P0
    h=calendar.crossing(P0-1)['time']//2
    assert calendar.crossing(P0-1)['kind']=='a'
    p=val(6*h+2)
    assert p==copied['omega'] and p<P0-1
    cx=(copied['head_ratio']+2*copied['tail_ratio'])*(1 << (P-1))
    assert cx.denominator==1 and val(cx)==rho_inner-1
    print('inner source',P0,p,'locating outer fire',flush=True)
    outer=first_fire(calendar,P)
    rho=outer['pointer'];x0=6*outer['k']+4;U=x0 >> P
    assert val(x0)==P and P<rho
    middle_x=cx*U+F(3*y0,2)+6*h+2
    middle_theta=x0+y0+6*h+3
    assert val(middle_x)==p
    endpoint=calendar.crossing(p-1)
    assert endpoint['kind']=='a' and endpoint['odd']
    k=endpoint['time']//2
    x=2*middle_theta+6*k-middle_x/2
    theta=middle_theta+2+6*k
    row=calendar.crossing(rho+2)
    assert row['kind']=='c' and row['epsilon']==7 and row['odd']
    assert theta==3*row['time']+4
    assert x==row['head_lambda']+2*row['tail_lambda']+3
    z=6*k+2;q=val(z)
    assert q<p-1
    assert x-z==2*x0-cx*U/2+F(5*y0,4)+3*(3*h+1)
    assert theta-(z+1)==x0+y0+2*(3*h+1)
    assert val(x-z)==p-1 and val(theta-z-1)==p
    actual=walk(calendar,q,F(x),F(theta))
    ref=walk(calendar,q,F(z),F(z+1))
    assert len(actual)==len(ref)
    for a,b in zip(actual,ref):
        assert a[0]==b[0] and a[3]==b[3]
        assert a[0]+a[3]<=q<p-1
        assert rho-5-a[3]>a[0]
        assert min(val(a[1]-b[1]),val(a[2]-b[2]))>=p-1-a[3]
    result=dict(result='PASS',review_status='unreviewed',
                outer_source_fire_parameter=P,inner_fire_parameter=P0,
                middle_parameter=p,reduced_parameter=q,
                outer_EXT_index_bits=(rho+3).bit_length(),source_deficit=row['epsilon'],
                tail=[a[0] for a in actual],shadow_states=len(actual),
                seconds=round(time.monotonic()-started,2),
                scope='One canonical CA source and its exact shadow; all-scale argument is separate and unreviewed.')
    Path(__file__).with_name('ca_source_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
