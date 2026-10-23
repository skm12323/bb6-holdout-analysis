"""Independent scratch checks for work_c3_drift/FIRST_A_REDUCTION.md (reviewer).
Does NOT rerun verify_first_a.py: it checks the constants used in section 2,
the mass-identity facts needed there, and the section-6 table."""
import sys, json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(r'D:/math_cc')
sys.path.insert(0,str(ROOT/'work_c3_drift'))
sys.path.insert(0,str(ROOT/'work_ext_roots'))
from verify_shift_transport import Calendar, first_fire, val, bounded_walk

def main():
    cal=Calendar(512)
    out={}
    # (1) canonical small base: X(0..3) even
    out['base_odd_0_3']=[cal.crossing(n)['odd'] for n in range(4)]
    # (2) real-chain x = 3*time+4+lambda_Y, lambda_Y>=0, v2(x)>=1
    neg=[];j0=[];cnt=0;mins=10**9
    for n in range(4,2000):
        r=cal.crossing(n)
        if not r['odd']:continue
        cnt+=1;ly=r['tail_lambda']
        if ly is not None and ly<0:neg.append((n,ly))
        x=3*r['time']+4+(ly or 0)
        if val(x)<1:j0.append((n,r['kind'],r['time'],ly,str(x)))
        mins=min(mins,r['time'])
    out['odd_crossings_checked']=cnt;out['neg_lambda_Y']=neg[:5];out['real_x_j0']=j0[:5]
    out['min_time']=mins
    # (3) sources: counts by kind, first-a constants
    nsrc=0;nf=0;nc=0;a_by={'fire':0,'c':0};na_by={'fire':0,'c':0}
    miny=10**9;minys=10**9;minxA=10**9;maxxA_ratio=None;minsA=10**9;minsprime=10**9
    qdist={};bad=[]
    for P in range(5,257):
        fire=first_fire(cal,P)
        rows=cal.epoch_crossings(fire)
        sources=[(fire['pointer'],6*fire['k']+4,6*fire['k']+5,fire['pointer'],'fire')]
        for n,r in rows.items():
            if r['kind']=='c' and r['odd']:
                sources.append((n,3*r['time']+4+r['tail_lambda'],3*r['time']+5,n-r['epsilon'],'c'))
        for n,x,th,sigma,kind in sources:
            nsrc+=1;nf+= (kind=='fire');nc+=(kind=='c')
            st,real=bounded_walk(cal,x,th,sigma)
            if st!='end':bad.append(('real_not_end',P,n,kind,st))
            first=None
            for i,(j,g,xx,tt) in enumerate(real):
                r=cal.crossing(j-1)
                if not r['odd']:break
                if r['kind']=='a':first=(i,j,g,xx,tt,r);break
            if first is None:
                na_by[kind]+=1;continue
            a_by[kind]+=1
            i,m_,g,xx,tt,r=first
            sA=r['time'];k=r['time']//2;tau=3*r['time']
            xa=xx
            y=2*tt+3*r['time']-xa/2
            if y.denominator!=1:bad.append(('nonint',P,n))
            y=int(y);sprime=sA+1+tau
            minsA=min(minsA,sA);minsprime=min(minsprime,sprime);minxA=min(minxA,int(xa));miny=min(miny,y)
            if not (xa>=32 and xa<=6*sA+5 and sprime>=8 and y>=28):bad.append(('const',P,n,kind,str(xa),sA,str(y),sprime))
            q=val(y)
            for eta in range(-8,9):
                if eta==0:continue
                h=val(2*eta)
                ys=y+2*eta
                minys=min(minys,ys)
                if q!=h:
                    if val(ys)!=min(q,h) or val(ys)>4:bad.append(('mismatch',P,n,eta,q,h,val(ys)))
                else:
                    if q>4:bad.append(('coll_q>4',P,n,eta,q))
                    qdist[q]=qdist.get(q,0)+1
    out.update(sources=nsrc,fires=nf,c_sources=nc,with_a=a_by,without_a=na_by,
               min_xA=minxA,min_sA=minsA,min_sprime=minsprime,min_y=miny,min_y_shifted=minys,
               collision_qdist={str(k):v for k,v in sorted(qdist.items())},bad=bad[:10],n_bad=len(bad))
    # (4) section-6 table: extra bits and residue collisions
    js=json.load(open(ROOT/'work_c3_drift/first_a_checks.json'))
    ex=js['extra_precision_examples']
    tb=[(e['P'],e['eta'],e['certificate_bits'],e['x_residue'],e['theta_residue'],tuple(e['word']),e['certificate_bits']-6) for e in ex]
    out['extra_table']=tb
    out['distinct_residues']=len(set((e['certificate_bits'],e['x_residue'],e['theta_residue']) for e in ex))
    out['distinct_words']=len(set(tuple(e['word']) for e in ex))
    out['json_counts']=js['counts'];out['json_cert']=js['collision_certificates'];out['json_max_extra']=js['max_extra_bits']
    print(json.dumps(out,indent=1,default=str))
    Path(__file__).with_name('check_first_a_constants.json').write_text(json.dumps(out,indent=1,default=str)+'\n')

if __name__=='__main__':main()
