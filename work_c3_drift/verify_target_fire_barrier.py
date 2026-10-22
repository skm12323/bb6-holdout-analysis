"""Arithmetic controls for the prescribed-v2 canonical fire barrier."""
from pathlib import Path
import json
from verify_shift_transport import Calendar,val

def target(m):
    v=(1,5,7,17,13,11)[m%6]
    assert (v*(1<<m)-10)%9==0
    return (v*(1<<m)-10)//9

def main():
    cal=Calendar(256)
    gaps={P:cal.kernels[P]['delta'] for P in range(1,16)}
    small=[]
    for P,gap in gaps.items():
        mod=1<<(P-1);distance=(-4*pow(9,-1,mod))%mod or mod
        assert gap<=distance
        small.append(dict(P=P,gap=gap,min_distance=distance))
    assert all(9*P**3<=2*((1<<(P-1))-4) for P in range(16,4097))
    assert all(9*(m+3)**3<=2*((1<<m)-4) for m in range(16,4097))
    checks=0
    for m in (16,17,18):
        k=target(m)
        assert val(9*k+10)==m
        for h in range(1,k):
            P=val(6*h+4)
            gap=gaps[P] if P<16 else P**3//2
            assert P<=m+3 and gap<=k-h
            checks+=1
    targets=[]
    for m in range(5,129):
        k=target(m);f=cal.preceding_fire_by_time(2*k)
        assert f['k']==k and f['J']==3
        p=f['pointer']+1
        assert p>=m+4
        targets.append(dict(m=m,k_bits=k.bit_length(),p_bits=p.bit_length()))
    # C1 forces p>=m+4 from this real-time lower bound, for all m>=16.
    assert all(2*((1<<m)-10)>9*(m+3)**2 for m in range(16,4097))
    out=dict(status='PASS',review_status='unreviewed',small_kernel_barriers=small,
             all_integer_predecessor_checks=checks,canonical_targets_checked=len(targets),
             scope='Arithmetic and finite calendar checks. The all-m construction under global EXT is an analytic conditional theorem, not a computation.')
    Path(__file__).with_name('target_fire_barrier_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
