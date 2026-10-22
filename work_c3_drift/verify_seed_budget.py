"""Low-deficit reference and integer-parent seed budget checks."""
from pathlib import Path
from collections import Counter
import json
from verify_shift_transport import Calendar,val

def main():
    cal=Calendar(512);counts=Counter();small=[]
    for s in range(5,4097):
        row=cal.crossing(s-1)
        if not row['odd'] or row['kind']!='a':continue
        k=row['time']//2
        for history,c,loss,j_offset in (('A',2,5,4),('AA',4,7,7),('BA',0,7,7)):
            z=6*k+c
            if val(z)!=5:continue
            for d in (5,-11):
                y=3*z//2+2*d+6;t=z+d+9;m=val(y)
                assert y>0 and m<=s-4
                expected=((15-d-(1<<m))*pow(3,-1,1<<(m+1)))%(1<<(m+1))
                assert (t-y-expected)%(1<<(m+1))==0
                j_lower=s+j_offset
                assert m+loss+2<j_lower
                if s<15:small.append(dict(history=history,s=s,k=k,d=d,m=m))
                counts[history]+=1
    for j in range(64,4097):
        row=cal.crossing(j-1)
        if not row['odd'] or row['kind'] not in ('a','b'):continue
        k=row['time']//2;x=1<<j
        for theta in ((-2,14) if row['kind']=='a' else (6,-10)):
            th=x+theta
            if row['kind']=='a':
                y=2*th+6*k-x//2;t=th+6*k+3;loss=2
            else:
                z=6*k+4;y=3*x//4+z;t=th+z-1;loss=3
            if val(y)!=5:continue
            z2=2*t+6-y//2;t2=t+9;m=val(z2)
            d=3-theta if row['kind']=='a' else theta-1
            assert d in (5,-11)
            expected=((15-d-(1<<m))*pow(3,-1,1<<(m+1)))%(1<<(m+1))
            assert (t2-z2-expected)%(1<<(m+1))==0
            assert m+loss+2<j
            counts['parent_'+row['kind']]+=1
    assert all(v>0 for v in counts.values()) and len(counts)==5
    assert all(9*(s-1)**2+44 < 1<<(s-2) for s in range(15,4097))
    out=dict(status='PASS',review_status='unreviewed',checks=dict(counts),small_cases=small,
             scope='Canonical call clocks and reference forms; AA/BA outer histories are not claimed realized for every selected s. All-scale size proof is separate.')
    Path(__file__).with_name('seed_budget_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
