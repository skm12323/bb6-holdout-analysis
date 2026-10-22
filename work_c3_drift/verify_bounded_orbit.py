"""Cover an exponent interval by HP-certified binary residue classes."""
from pathlib import Path
from collections import Counter
import sys,json
from verify_shift_transport import Calendar,first_fire,bounded_walk
from verify_orbit_shift_obstruction import discrete_log_three

def cover(R,max_nodes=100000,max_bits=128):
    cal=Calendar(512);fire=first_fire(cal,49)
    x0=6*fire['k']+4;y=3*x0//2+122;T=x0+124
    sigma=fire['pointer'];A=(y-10)//16
    H=3
    while True:
        rr=discrete_log_three((-pow(A,-1,1<<H))%(1<<H),H)
        if rr>R:break
        H+=1
    # Thus the maximum first residual parameter on the interval is H+3.
    previous=discrete_log_three((-pow(A,-1,1<<(H-1)))%(1<<(H-1)),H-1)
    assert previous<=R and rr>R
    pending=[(0,1),(1,1)];covered=0;nodes=0;certs=[];open_nodes=[];hist=Counter()
    while pending:
        a,b=pending.pop()
        if a>R:continue
        nodes+=1;K=b+5
        if nodes>max_nodes or b>max_bits or K>=sigma-1:
            open_nodes.append((a,b));continue
        modulus=1<<K
        inv=pow(pow(3,a,modulus),-1,modulus)
        xx=(y-10+16*inv)%modulus;tt=(T-5+8*inv)%modulus
        status,rows=bounded_walk(cal,xx,tt,K,signed=True)
        if status=='end':
            count=(R-a)//(1<<b)+1;covered+=count;hist[b]+=1
            certs.append(dict(a=str(a),b=b,K=K,count=str(count),
                              x=xx,theta=tt,word=[j for j,_,_,_ in rows]))
        else:
            pending.extend(((a,b+1),(a+(1<<b),b+1)))
    out=dict(status='PASS' if not open_nodes else 'INCOMPLETE',review_status='unreviewed',
             exponent_upper=str(R),nodes=nodes,covered=str(covered),expected=str(R+1),
             max_first_output_parameter=H+3,attaining_exponent=str(previous),
             first_excluded_lift=dict(H=H,r=str(rr)),certificate_depths=dict(sorted(hist.items())),
             open_nodes=[dict(a=str(a),b=b) for a,b in open_nodes],certificates=certs,
             scope='Entire finite exponent interval at one canonical source; not joint reachability or all-source EXT.')
    if not open_nodes:assert covered==R+1
    return out

def main():
    R=int(sys.argv[1]) if len(sys.argv)>1 else 10**6
    out=cover(R)
    Path(__file__).with_name(f'bounded_orbit_{R}.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='certificates'}))

if __name__=='__main__':main()
