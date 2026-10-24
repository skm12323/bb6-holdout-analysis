"""Finite checks of the uniform internal-clock orbit and period advance."""
from pathlib import Path
import json
import sys
sys.path.insert(0,'D:/math_cc/work_c3_drift')
from verify_shift_transport import val

def main():
    results=[];points=0
    for L in range(17,25):
        modulus=1<<(L-5);period=1<<(L-7);inverse=pow(3,-1,modulus)
        for start in (1,3,5,7):
            u=start;seen=set();total=0;lifted_total=0
            for i in range(period):
                assert u not in seen and u%2
                seen.add(u);points+=1
                k=8*u-2
                assert k%16==6
                total+=12+6*k
                # Arbitrary higher lifts cannot alter the valuation of total.
                lifted_k=k+8*modulus*(i%7)
                lifted_total+=12+6*lifted_k
                nxt=(inverse*u)%modulus
                assert (4-k+3*(8*nxt-2))%(1<<(L-2))==0
                u=nxt
            assert u==start and len(seen)==period
            assert val(total)==val(lifted_total)==L-2
            results.append(dict(L=L,unit_modulus_bits=L-5,period=period,
                                starting_unit=start,clock_advance_valuation=val(total)))
    out=dict(status='PASS',review_status='unreviewed',orbit_points_checked=points,
             cases=results,
             scope='Arithmetic checks of necessary clock orbits; no canonical train of these lengths is asserted.')
    Path(__file__).with_name('train_clock_orbit_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}))

if __name__=='__main__':main()
