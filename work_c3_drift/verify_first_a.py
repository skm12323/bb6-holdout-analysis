"""Exact first-A reduction for bounded common shifts of canonical chains."""
from pathlib import Path
from collections import Counter
import json
from verify_shift_transport import Calendar, first_fire, val, bounded_walk

def main():
    cal=Calendar(512);stats=Counter();collisions=[];checked=0
    cert_stats=Counter();extra_examples=[];max_extra=0
    for P in range(5,257):
        fire=first_fire(cal,P)
        rows=cal.epoch_crossings(fire)
        sources=[(fire['pointer'],6*fire['k']+4,6*fire['k']+5,fire['pointer'],'fire')]
        for n,r in rows.items():
            if r['kind']=='c' and r['odd']:
                sources.append((n,3*r['time']+4+r['tail_lambda'],3*r['time']+5,n-r['epsilon'],'c'))
        for n,x,th,sigma,kind in sources:
            st,real=bounded_walk(cal,x,th,sigma)
            assert st=='end'
            first=None
            for i,(j,g,xx,tt) in enumerate(real):
                r=cal.crossing(j-1)
                if not r['odd']:break
                if r['kind']=='a':first=(i,j,g,xx,tt,r);break
            for eta in range(-8,9):
                st,shifted=bounded_walk(cal,x,th+eta,sigma);checked+=1
                if eta==0:
                    assert st=='end';stats['zero_shift']+=1;continue
                if first is None:
                    assert st=='end'
                    assert [(j,g) for j,g,_,_ in shifted]==[(j,g) for j,g,_,_ in real]
                    stats['no_A']+=1;continue
                i,j,g,xx,tt,r=first
                # Before the first a-step, numerators are exactly identical.
                assert len(shifted)>i
                for a,b in zip(real[:i+1],shifted[:i+1]):
                    assert a[:3]==b[:3] and b[3]-a[3]==eta
                yr=2*tt+3*r['time']-xx/2
                tr=tt+3+3*r['time'];ys=yr+2*eta;ts=tr+eta
                assert yr.denominator==ys.denominator==1
                assert xx>=32 and yr>=28 and ys>0
                q=val(yr);h=val(2*eta);remaining=sigma-g-1
                suffix_status,suffix=bounded_walk(cal,ys,ts,remaining)
                assert st==suffix_status
                if suffix_status=='end':
                    assert [(j0,g0-g-1) for j0,g0,_,_ in shifted[i+1:]]==[(j0,g0) for j0,g0,_,_ in suffix]
                if q!=h:
                    assert val(ys)==min(q,h)<=4
                    assert st=='end';stats['valuation_mismatch_closes']+=1
                else:
                    assert q<=4 and not cal.crossing(q-1)['odd']
                    assert i+2==len(real)  # real epoch terminates at its first A
                    stats['collision_'+st]+=1
                    v=val(ys);delta=int(ts-ys) % (1<<(v+1))
                    cs,cr=bounded_walk(cal,1<<v,(1<<v)+delta,v+1,signed=True)
                    cert_stats['minimal_class_'+cs]+=1
                    # A stronger exact cylinder is certified using the observed
                    # record bound, then re-executed from its finite residues.
                    K=max(jj+gg for jj,gg,_,_ in suffix)+1
                    ss,sr=bounded_walk(cal,int(ys)%(1<<K),int(ts)%(1<<K),K,signed=True)
                    assert ss=='end'
                    assert [(jj,gg) for jj,gg,_,_ in sr]==[(jj,gg) for jj,gg,_,_ in suffix]
                    assert K<=remaining
                    max_extra=max(max_extra,K-v-1)
                    if cs!='end' and len(extra_examples)<12:
                        extra_examples.append(dict(P=P,kind=kind,eta=eta,j=v,delta=delta,
                            minimal_status=cs,certificate_bits=K,
                            x_residue=int(ys)%(1<<K),theta_residue=int(ts)%(1<<K),
                            word=[jj for jj,_,_,_ in sr]))
                    if len(collisions)<12:
                        collisions.append(dict(P=P,kind=kind,n=str(n),eta=eta,
                            real_output_parameter=q,shifted_output_parameter=val(ys),
                            residual_precision=str(remaining),suffix=[a[0] for a in suffix]))
    out=dict(status='PASS',review_status='unreviewed',source_P=[5,256],shifts=[-8,8],
             cases=checked,counts=dict(stats),collision_examples=collisions,
             collision_certificates=dict(cert_stats),max_extra_bits=max_extra,
             extra_precision_examples=extra_examples,
             scope='Actual canonical fires and c chains at selected fires. Conditional all-scale reduction is in FIRST_A_REDUCTION.md.')
    Path(__file__).with_name('first_a_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='collision_examples'}))
    print(json.dumps(collisions[:3]))
    print(json.dumps(extra_examples[:3]))

if __name__=='__main__':main()
