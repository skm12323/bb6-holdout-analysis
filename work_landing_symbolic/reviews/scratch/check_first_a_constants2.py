"""Corrected constant checks: s_A is the STATE's time (Theta_A=3*s_A+5),
not the time of the crossing X(m-1) that the state reads."""
import sys, json
from pathlib import Path
ROOT=Path(r'D:/math_cc')
sys.path.insert(0,str(ROOT/'work_c3_drift'))
sys.path.insert(0,str(ROOT/'work_ext_roots'))
from verify_shift_transport import Calendar, first_fire, val, bounded_walk

def main():
    cal=Calendar(512);out={}
    bad=[];rows_out=[]
    min_sA=10**9;min_y=10**9;min_ys=10**9;min_m=10**9;minslack=10**9
    qdist={}
    for P in range(5,257):
        fire=first_fire(cal,P);rows=cal.epoch_crossings(fire)
        sources=[(fire['pointer'],6*fire['k']+4,6*fire['k']+5,fire['pointer'],'fire')]
        for n,r in rows.items():
            if r['kind']=='c' and r['odd']:
                sources.append((n,3*r['time']+4+r['tail_lambda'],3*r['time']+5,n-r['epsilon'],'c'))
        for n,x,th,sigma,kind in sources:
            st,real=bounded_walk(cal,x,th,sigma)
            first=None
            for i,(j,g,xx,tt) in enumerate(real):
                r=cal.crossing(j-1)
                if not r['odd']:break
                if r['kind']=='a':first=(i,j,g,xx,tt,r);break
            if first is None:continue
            i,m,g,xx,tt,r=first
            tau=r['time']                       # tau(m-1), the READ crossing
            sA=(tt-5)/3                         # the STATE's time
            if sA.denominator!=1:bad.append(('th_not_3s5',P,n,str(tt)))
            sA=int(sA)
            y=2*tt+3*tau-xx/2
            if y.denominator!=1:bad.append(('y_nonint',P,n))
            y=int(y);sprime=sA+1+tau
            min_sA=min(min_sA,sA);min_y=min(min_y,y);min_m=min(min_m,m)
            minslack=min(minslack,6*sA+5-int(xx))
            if not (xx>=32 and xx<=6*sA+5 and sprime>=8 and y>=28 and y+2*(-8)>0):
                bad.append(('const',P,n,kind,str(xx),sA,str(y),sprime))
            q=val(y)
            for eta in range(-8,9):
                if eta==0:continue
                h=val(2*eta);ys=y+2*eta;min_ys=min(min_ys,ys)
                if q!=h:
                    if val(ys)!=min(q,h) or val(ys)>4:bad.append(('mismatch',P,n,eta,q,h,val(ys)))
                else:
                    if q>4:bad.append(('coll_q>4',P,n,eta,q))
                    qdist[q]=qdist.get(q,0)+1
            if len(rows_out)<6:rows_out.append(dict(P=P,kind=kind,m=m,sA=sA,tau=tau,xA=int(xx),y=y,sprime=sprime,q=q))
    out.update(min_state_time=min_sA,min_y=min_y,min_y_shifted=min_ys,min_m=min_m,
               min_slack_6sA5_minus_xA=minslack,collision_qdist={str(k):v for k,v in sorted(qdist.items())},
               n_bad=len(bad),bad=bad[:8],examples=rows_out,
               base_odd_0_3=[cal.crossing(n)['odd'] for n in range(4)])
    print(json.dumps(out,indent=1,default=str))
    Path(__file__).with_name('check_first_a_constants2.json').write_text(json.dumps(out,indent=1,default=str)+'\n')
if __name__=='__main__':main()
