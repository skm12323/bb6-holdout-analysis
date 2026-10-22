"""Extra-bit-aware emissions 46/9 and 62/9; finite certificates only."""
from pathlib import Path
import json
from verify_shift_transport import Calendar,bounded_walk,val

def main():
    cal=Calendar(512);identities=0;failed=[];counts={};max_records={}
    for C in (-1,-17):
        A=45-C
        for m in range(5,129):
            r=m-4;mod=1<<r
            # m=4+v2(9u+1) for C=-1; m=4+v2(9u-1) for C=-17.
            sign=1 if C==-1 else -1
            base=(-sign*pow(9,-1,mod))%mod
            u=next(v for v in (base,base+mod,base+2*mod)
                   if v>0 and v%2 and val(9*v+sign)==r)
            H=m+2;D=(C*pow(3,-1,1<<H))%(1<<H)
            for lift in (0,1,3):
                d=D+lift*(1<<H);x=32*u;th=x+d
                y=2*th+6-x//2;t=th+9
                assert val(y)==m
                delta=(A*pow(9,-1,1<<(m+1))+(1<<m))%(1<<(m+1))
                assert (t-y-delta)%(1<<(m+1))==0
                identities+=1
        count=0;maxrec=0
        for m in range(5,16384):
            delta=(A*pow(9,-1,1<<(m+1))+(1<<m))%(1<<(m+1))
            st,rows=bounded_walk(cal,1<<m,(1<<m)+delta,m+1,signed=True)
            count+=1
            if st!='end':failed.append(dict(A=A,m=m,status=st))
            if rows:maxrec=max(maxrec,max(j+g for j,g,_,_ in rows))
        counts[A]=count;max_records[A]=maxrec
    # Both are the same minimal input class, but emission's extra bit differs.
    controls=[]
    for d in (37,165):
        x=32;th=x+d;y=2*th+6-x//2;t=th+9;m=val(y)
        controls.append(dict(input_d=d,input_mod64=d%64,m=m,
                             output_delta=(t-y)%(1<<(m+1))))
    assert controls[0]['input_mod64']==controls[1]['input_mod64']
    assert controls[0]['output_delta']!=controls[1]['output_delta']
    assert not failed
    out=dict(status='PASS',review_status='unreviewed',identity_checks=identities,
             certificate_range=[5,16383],family_counts=counts,failures=failed,
             insufficient_precision_controls=controls,
             scope='Synthetic family certificates. No assertion of canonical reachability or all-scale closure.')
    Path(__file__).with_name('second_gateway_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
