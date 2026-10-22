"""Generic odd-denominator transition, emission, and size checks."""
from pathlib import Path
from math import gcd
import json
from verify_shift_transport import Calendar,val

def main():
    cal=Calendar(256);a_checks=0;emissions=0
    qs=(3,5,7,9,27,81,243,3**20)
    for Q in qs:
        for C in range(-25,27):
            if gcd(C,Q)!=1:continue
            for j in range(5,65):
                r=cal.crossing(j-1)
                if not r['odd'] or r['kind']!='a':continue
                k=r['time']//2;z=3*Q*k+C
                assert z!=0
                p=1+val(z)
                if p>j-2:continue
                d=C*pow(Q,-1,1<<(j+1))%(1<<(j+1))
                for bit in (0,1):
                    x=1<<j;th=x+d+bit*(1<<j)
                    y=2*th+6*k-x//2;t=th+6*k+3
                    assert val(y)==p
                    assert (Q*(t-y)-(3*Q-C))%(1<<(p+1))==0
                    a_checks+=1
        C=5*Q+16;H=32;d=C*pow(Q,-1,1<<H)%(1<<H)
        assert d%16==5
        numerator=15*Q-C;denominator=3*Q;g=gcd(numerator,denominator)
        A,R=numerator//g,denominator//g
        assert gcd(A,R)==1 and R in (Q,3*Q)
        for u in range(1,64,2):
            x=32*u;th=x+d;y=2*th+6-x//2;t=th+9;m=val(y)
            assert 5<=m<H
            expected=(A*pow(R,-1,1<<(m+1))+(1<<m))%(1<<(m+1))
            assert (t-y-expected)%(1<<(m+1))==0
            emissions+=1
    N0=20_000_000;e=N0//2;size=[]
    # Include denominator bit lengths that force the adaptive threshold up.
    for Q in (*qs,(1<<(N0//4-2))-1,(1<<(N0//4))-1,(1<<(N0//4+3))-1):
        d=(Q-1).bit_length();N=max(N0,4*(d+2))
        for j in (N,N+1,N+127):
            n=j-1;g=(6*n*n+4).bit_length();P=2*g*g+1345
            twice=3*Q*n*P+2*(Q<<e)
            assert twice.bit_length()<=j-1
            L=max(twice.bit_length()-1,(6*n*P+5).bit_length()-1)
            assert L<j
            size.append(dict(denominator_bits=Q.bit_length(),threshold=N,j=j,LQ=L))
    out=dict(status='PASS',review_status='unreviewed',a_transition_checks=a_checks,
             gateway_emission_checks=emissions,size_checks=len(size),size_samples=size,
             scope='Finite exact algebra and adaptive-threshold checks, not landing certification or canonical reachability.')
    Path(__file__).with_name('odd_denominator_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='size_samples'}))

if __name__=='__main__':main()
