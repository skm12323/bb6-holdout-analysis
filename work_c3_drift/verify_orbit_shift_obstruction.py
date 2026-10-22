"""Canonical source plus modular witnesses for bounded-height orbit shifts."""
from pathlib import Path
import json
from verify_shift_transport import Calendar,first_fire,val

def discrete_log_three(target,H):
    """Exact lifting in <3> modulo 2^H, H>=3; no huge 3^r expansion."""
    assert target%8 in (1,3)
    r=0 if target%8==1 else 1
    for h in range(3,H):
        modulus=1<<(h+1)
        if pow(3,r,modulus)!=target%modulus:r+=1<<(h-2)
        assert pow(3,r,modulus)==target%modulus
    assert r<1<<(H-2)
    return r

def main():
    cal=Calendar(512)
    inner=cal.preceding_fire_by_time(40)
    assert inner['k']==20 and inner['pointer']==48
    P=49;fire=first_fire(cal,P);sigma=fire['pointer']
    x0=6*fire['k']+4;y=3*x0//2+122;A=(y-10)//16
    assert x0==5*(1<<49)
    assert y==4222124650659962 and val(y)==1
    assert y==16*A+10 and A%8==7 and A+1<1<<48
    samples=[]
    for H in (3,4,5,8,16,32,64,128,256):
        modulus=1<<H;target=(-pow(A,-1,modulus))%modulus
        r=discrete_log_three(target,H)
        assert (A*pow(3,r,modulus)+1)%modulus==0
        entry=dict(H=H,r=str(r),r_bits=r.bit_length(),output_valuation_at_least=H+4)
        if r<10000:
            numerator=A*3**r+1
            assert val(numerator)>=H
            entry['exact_output_valuation']=4+val(numerator)
        samples.append(entry)
    out=dict(status='PASS',review_status='unreviewed',source_parameter=P,
             source_fire_k=str(fire['k']),source_pointer=str(sigma),
             real_terminal_y=str(y),A=str(A),A_mod8=A%8,
             symbolic_failure_H=str(sigma-5),
             necessary_r_lower_bound=str(5*(sigma-53)//8+1),samples=samples,
             scope='Actual canonical source. Full precision failure is proved by the subgroup theorem, not simulated. No joint reachability of its orbit shift is claimed.')
    Path(__file__).with_name('orbit_shift_obstruction_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='samples'}))
    print(json.dumps(samples[:4]))

if __name__=='__main__':main()
