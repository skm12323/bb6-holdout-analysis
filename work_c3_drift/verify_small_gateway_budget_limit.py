"""Negative controls for completing the joint reserve by a local rule alone."""
from pathlib import Path
from fractions import Fraction as F
import json
from verify_shift_transport import Calendar,val,bounded_walk
from verify_height_budget import height

def main():
    cal=Calendar(256);records=[]
    for m in range(6,257,2):
        u=((1<<(m-4))-1)//3
        assert u>0 and u%2 and 3*u+1==1<<(m-4)
        x=32*u;theta=x+5
        assert val(x)==5 and 0<x<2*theta
        W=5+height(F(5));assert W==8<9
        y=2*theta+6-x//2;t=theta+9
        assert y==1<<m and val(y)==m
        rank=1;c=F(10,3)
        assert val(F(t-y)-c-(1<<m))>=m+1
        Wnext=1+m+2*rank+height(c)
        st,rows=bounded_walk(cal,x,theta,9)
        if m>=8:assert st=='ceiling'
        safe,full=bounded_walk(cal,x,theta,m+2)
        assert safe=='end' and max(j+g for j,g,_,_ in full)==m+1
        records.append(dict(m=m,initial_W=W,next_W=Wnext,
                            ceiling9_status=st,valid_certificate_precision=m+2,
                            word=[j for j,_,_,_ in full]))
    out=dict(status='PASS',review_status='unreviewed',negative_controls=len(records),
             records=records,
             scope='Constructed local states with canonical calls. Refutes unconditional local sufficiency of W<ceiling, not EXT or the conditional macro lemmas.')
    Path(__file__).with_name('small_gateway_budget_limit_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}))
    print(json.dumps(records[:2]))

if __name__=='__main__':main()
