"""Canonical sources forcing long precision requirements at class (5,5)."""
from pathlib import Path
from collections import Counter
import json
from verify_shift_transport import Calendar,first_fire,val,bounded_walk

def main():
    cal=Calendar(512);records=[];misses=[];direct=0
    for m in range(5,257):
        mod=1<<m;base=(-10*pow(9,-1,mod))%mod
        chosen=None
        for lift in range(64):
            k=base+lift*mod
            if k<1 or val(9*k+10)!=m:continue
            fire=cal.preceding_fire_by_time(2*k)
            if fire['k']==k:
                chosen=(k,fire,lift);break
        if chosen is None:
            misses.append(m);continue
        k,fire,lift=chosen;P=fire['pointer']+1
        row=cal.crossing(P-1)
        assert row['kind']=='a' and row['odd'] and row['time']==2*k
        assert fire['J']==3 and P>=m+4
        # PROOF_SPECTRUM: every P+4<B is an actual fire parameter.
        # B=2^(2^499997-2), so this much smaller bound is sufficient.
        assert (P+4).bit_length()<=499997
        assert val(6*k-4)==5 and val(9*k+10)==m
        K=m+2
        xr=(6*k-4)%(1<<K);tr=(6*k+1)%(1<<K)
        assert (tr-xr) % 64 == 5
        status,trace=bounded_walk(cal,xr,tr,K,signed=True)
        assert status=='end' and [r[0] for r in trace[:2]]==[5,m]
        assert max(j+g for j,g,_,_ in trace)==m+1
        # Independent check of the existing gateway family at this m.
        delta=((10-(1<<m))*pow(3,-1,1<<(m+1)))%(1<<(m+1))
        cs,ct=bounded_walk(cal,1<<m,(1<<m)+delta,m+1,signed=True)
        assert cs=='end'
        # The real root fire has numerator 2^P or 5*2^P at the
        # accepted spectrum target. Materialize only moderate examples.
        if P<=10000:
            u=1 if P%2==0 else 5
            x0=u*(1<<P);t0=x0-2
            x1=2*t0+6*k-x0//2;t1=t0+6*k+3
            x2=2*t1+6-x1//2;t2=t1+9
            assert x1==3*x0//2+6*k-4
            assert x2==5*x0//4+9*k+10
            assert val(x1)==5 and val(x2)==m
            assert x1%(1<<K)==xr and t1%(1<<K)==tr
            assert (t2-x2-delta)%(1<<(m+1))==0
            direct+=1
        records.append(dict(m=m,k=str(k),source_pointer=str(P-1),root_parameter=str(P),
                            lift=lift,required_bits=K,extra_bits_over_minimal=m-4,
                            x_residue=str(xr),theta_residue=str(tr),
                            certificate_word=[r[0] for r in trace]))
    assert not misses
    out=dict(status='PASS',review_status='unreviewed',calendar_B=512,
             target_range=[5,256],targets=len(records),misses=misses,
             direct_bigint_examples=direct,max_required_bits=max(r['required_bits'] for r in records),
             scope='Canonical input sources verified by calendar; outer root fires exist by accepted finite spectrum theorem, not simulated. Shift eta=-3 is counterfactual.',
             records=records)
    Path(__file__).with_name('targeted_precision_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}))
    print(json.dumps([records[0],records[-1]]))

if __name__=='__main__':main()
