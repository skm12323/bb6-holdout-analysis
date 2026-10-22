"""Low-height rational phase transitions and small landing obstructions."""
from pathlib import Path
from collections import Counter
import json
from verify_shift_transport import Calendar,bounded_walk,val

def main():
    cal=Calendar(256);checks=0;failures=[];counts=Counter();levels={}
    allc=set()
    for c0 in (10,26):
        states={c0};levels[c0]=[]
        for t in range(5):
            assert all(c%3!=0 and abs(c)<=c0+3*t for c in states)
            levels[c0].append(sorted(states));allc|=states
            states={z for c in states for z in (9-c,c-3,c,c+3)}
    # Test exact a-step identities where the claimed strong descent occurs.
    for j in range(5,129):
        r=cal.crossing(j-1)
        for c in sorted(allc):
            mod=1<<(j+1);d=(c*pow(3,-1,mod))%mod
            st,rows=bounded_walk(cal,1<<j,(1<<j)+d,j+1,signed=True)
            counts[st]+=1
            if st!='end' and len(failures)<24:
                failures.append(dict(j=j,C=c,delta=str(d),status=st,
                                     accepted_prefix=[a[0] for a in rows]))
            if not r['odd'] or r['kind']!='a':continue
            k=r['time']//2;z=9*k+c
            assert z!=0
            q=1+val(z)
            if q>j-2:continue
            for lift in (0,1):
                dd=d+lift*(1<<j)
                x=1<<j;th=x+dd
                xn=2*th+6*k-x//2;tn=th+6*k+3
                assert val(xn)==q
                assert (3*(tn-xn)-(9-c))%(1<<(q+1))==0
                checks+=1
    out=dict(status='PASS',review_status='unreviewed',numerator_levels=levels,
             numerators=sorted(allc),a_transition_checks=checks,
             landing_scan_range=[5,128],landing_status=dict(counts),
             landing_obstructions=failures,
             scope='All-scale mode lemma is conditional. These are synthetic class tests, not claimed canonical shifted trajectories.')
    Path(__file__).with_name('rational_mode_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('numerator_levels','landing_obstructions','numerators')}))
    print(json.dumps(failures[:4]))

if __name__=='__main__':main()
