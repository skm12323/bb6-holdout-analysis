"""Common-shift transport on actual AA ancestor pairs, with failure controls."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys, json
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'work_ext_roots'))
from verify_low_deficit import Calendar,first_fire,val

def bounded_walk(cal,x,th,precision,signed=False):
    x,th=F(x),F(th); loss=0; rows=[]
    for _ in range(128):
        if x==0: return 'zero',rows
        if x<0 and not signed: return 'nonpositive',rows
        j=val(x)
        if j+loss>=precision: return 'ceiling',rows
        rows.append((j,loss,x,th))
        r=cal.crossing(j-1)
        if not r['odd']: return 'end',rows
        if r['kind']=='a': x=2*th+3*r['time']-x/2
        else:
            x=(r['head_ratio']+2*r['tail_ratio'])*x/2+r['head_lambda']+2*r['tail_lambda']+3
        th+=3+3*r['time'];loss+=1+r['epsilon']
    return 'limit',rows

def main():
    cal=Calendar(512);pairs=[];states=0;stats=Counter();controls=[]
    for P in range(5,257):
        a=cal.crossing(P-1)
        if not a['odd'] or a['kind']!='a':continue
        p=val(3*a['time']+2);b=cal.crossing(p-1)
        if not b['odd'] or b['kind']!='a':continue
        fire=first_fire(cal,P);n=fire['pointer']+3
        d=cal.crossing(n);c=cal.crossing(p)
        assert d['kind']=='c' and c['kind']=='b'
        xd=3*d['time']+4+d['tail_lambda'];td=3*d['time']+5
        xc=3*c['time']+4;tc=3*c['time']+5
        sc=p-1;sd=n-d['epsilon']
        assert sd>sc and min(val(xd-xc),val(td-tc))>=sc
        pairs.append(dict(P=P,p=p,source_index=str(n),ancestor_index=p,precision=sc))
        for eta in range(-32,33):
            assert val((td+eta)-(tc+eta))>=sc
            status,ref=bounded_walk(cal,xc,tc+eta,sc)
            stats[status]+=1
            if status!='end':
                if len(controls)<8:controls.append(dict(P=P,p=p,eta=eta,status=status))
                continue
            actual,rows=bounded_walk(cal,xd,td+eta,sc)
            assert actual=='end'
            assert [(j,g) for j,g,_,_ in rows]==[(j,g) for j,g,_,_ in ref]
            for (j,g,x,t),(jj,gg,y,u) in zip(rows,ref):
                assert min(val(x-y),val(t-u))>=sc-g
                states+=1
    # Nontrivial canonical b-reference tails, with explicitly synthetic
    # congruent lifts. No claim that these lifts have an AA origin.
    synthetic=Counter(); synthetic_states=0
    for p in range(5,257):
        a=cal.crossing(p-1)
        if not a['odd'] or a['kind']!='a':continue
        xc=3*a['time']+4;tc=xc+1;sc=p-1
        shifts=list(range(-32,33))
        q=val(xc);nxt=cal.crossing(q-1)
        if nxt['odd'] and nxt['kind']=='a':
            forcing=(1<<sc)-2*tc-3*nxt['time']+xc//2
            assert forcing%2==0
            shifts.append(forcing//2)  # deliberately force next x=2^sc
        for eta in shifts:
            status,ref=bounded_walk(cal,xc,tc+eta,sc)
            synthetic[status]+=1
            if status!='end':
                if len(controls)<8:controls.append(dict(p=p,eta=eta,status=status,kind='canonical reference'))
                continue
            actual,rows=bounded_walk(cal,xc+(1<<sc),tc+eta+3*(1<<sc),sc)
            assert actual=='end'
            assert [(j,g) for j,g,_,_ in rows]==[(j,g) for j,g,_,_ in ref]
            for (j,g,x,t),(jj,gg,y,u) in zip(rows,ref):
                assert min(val(x-y),val(t-u))>=sc-g
                synthetic_states+=1
    assert pairs and stats['end'] and synthetic['ceiling']
    out=dict(status='PASS',review_status='unreviewed',canonical_pairs=pairs,
             common_shifts=[-32,32],reference_status=dict(stats),matched_states=states,
             synthetic_lift_reference_status=dict(synthetic),synthetic_lift_matched_states=synthetic_states,
             unresolved_controls=controls,
             scope='Actual AA pairs are terminal. Nontrivial tails use canonical references with synthetic congruent lifts. Mixed histories not sampled.')
    Path(__file__).with_name('transport_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
