"""Replay saved cover using full-pair tables, not Calendar tail execution."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_claude_shifted'))
from shiftlib import Tables,exact_tail

def main():
    R=int(sys.argv[1]) if len(sys.argv)>1 else 10**30
    path=Path(__file__).with_name(f'bounded_orbit_{R}.json')
    data=json.loads(path.read_text(encoding='utf-8'))
    assert data['status']=='PASS' and not data['open_nodes']
    certs=data['certificates'];N=max(c['K'] for c in certs)+2
    tables=Tables(N,NS=N);total=0;period_checks=0
    x0=5*(1<<49);y=3*x0//2+122;T=x0+124
    for i,c in enumerate(certs):
        a=int(c['a']);b=c['b'];K=c['K'];mod=1<<K
        assert 0<=a<1<<b and K==b+5
        count=(R-a)//(1<<b)+1
        assert count>0 and count==int(c['count']);total+=count
        inv=pow(pow(3,a,mod),-1,mod)
        assert c['x']==(y-10+16*inv)%mod
        assert c['theta']==(T-5+8*inv)%mod
        # Full-pair evaluator independently reconstructs each small c'_W.
        status,word,record=exact_tail(tables,c['x'],c['theta'],K)
        assert status=='end' and word==c['word'] and record<K
        for lift in (1,3,17):
            other=pow(pow(3,a+lift*(1<<b),mod),-1,mod)
            assert (16*(other-inv))%mod==0
            assert (8*(other-inv))%mod==0
            period_checks+=1
        for p in certs[:i]:
            assert (a-int(p['a']))%(1<<min(b,p['b']))!=0
    assert total==R+1
    out=dict(status='PASS',review_status='unreviewed',exponent_upper=str(R),
             certificates=len(certs),covered=str(total),period_checks=period_checks,
             max_reference_table_index=N-1,
             scope='Independent full-pair replay plus prefix-disjointness/count check; not an independent human proof review.')
    Path(__file__).with_name(f'bounded_orbit_replay_{R}.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
