"""A four-catapult local witness with canonical calls, checked two ways."""
from pathlib import Path
import sys,json,hashlib
import sys
sys.path.insert(0,'D:/math_cc/work_c3_drift')
from verify_shift_transport import Calendar,val,bounded_walk
sys.path.insert(0,'D:/math_cc/work_global_ext/route_c')
from fdata import lam_walk

def fingerprint(x):
    return hashlib.sha256(x.to_bytes((x.bit_length()+7)//8,'big')).hexdigest()

def main():
    cal=Calendar(256);ka=819270;kb=229398
    fa=cal.preceding_fire_by_time(2*ka);fb=cal.preceding_fire_by_time(2*kb)
    assert fa['k']==ka and fb['k']==kb and fa['J']==fb['J']==3
    a=fa['pointer']+1;b=fb['pointer']+1
    y0=1<<a;y1=(1<<b)+(1<<(a+10))
    th=y1-y0//4-21-9*ka;x=4*th+12-2*y0
    assert x>0 and th>0 and val(x)==5
    precision=a+2
    status,rows=bounded_walk(cal,x,th,precision)
    expected=[5,a,5,b,5,17,5,17,19]
    assert status=='end' and [j for j,_,_,_ in rows]==expected
    assert max(j+g for j,g,_,_ in rows)==a+1
    # Independent canonical data and direct a-step evaluator; no Calendar replay.
    table=lam_walk(a)
    assert table['tau'][a-1]==2*ka and table['tau'][b-1]==2*kb
    xx=x;tt=th;direct=[]
    while True:
        j=val(xx);direct.append(j);n=j-1
        if not table['odd'][n]:break
        assert table['typ'][n]==97
        xx=2*tt+3*table['tau'][n]-xx//2
        tt+=3+3*table['tau'][n]
        assert xx>0
        assert len(direct)<32
    assert direct==expected
    D=th-x
    assert val(D+3)==3
    unit=(D+3)//8
    assert unit%8 in (1,3)
    # Thus for every H>=6 there exists an orbit exponent r with
    # -3+8/3^r == D mod 2^H (group argument; no joint reachability).
    z0=4-ka+3*kb;z1=4-kb+3*6
    assert z0==-(1<<17) and z1==-7*(1<<15)
    out=dict(status='PASS',review_status='unreviewed',ka=ka,kb=kb,
             source_a=a,source_b=b,word=expected,losses=[g for _,g,_,_ in rows],
             max_record=a+1,certificate_precision=precision,
             x_bits=x.bit_length(),theta_bits=th.bit_length(),
             x_sha256=fingerprint(x),theta_sha256=fingerprint(th),
             initial_defect_mod64=D%64,orbit_unit_mod8=unit%8,
             normalized_clock_residues=[((k+2)//8)%4096 for k in (ka,kb,6)],
             direct_table_size=a,
             scope='Local scalar starting state is constructed, not canonical. Every called crossing is canonical; the trace is independently replayed. No EXT counterexample.')
    Path(__file__).with_name('cross_scale_train_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
