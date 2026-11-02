import sys,time,json
sys.path.insert(0,r'D:\math_cc\work_claude_residual')
import rwalk as R
t=time.time(); T=R.Table(); print('table',time.time()-t,flush=True)
# compare bulk vs certify
for delta in (1,-1,2):
    t=time.time(); B=R.bulk(T,delta,64,300000); print('bulk',delta,time.time()-t,len(B['aout']),len(B['uncert']),B['nt'])
    agg={}
    for j in range(64,300000):
        c=R.certify(T,j,delta)
        if not c['ok']: print('uncert',j)
        for a in c['aouts']:
            e=agg.setdefault(a,[0,j]); e[0]+=1
    assert {k:v[0] for k,v in agg.items()}=={k:v[0] for k,v in B['aout'].items()}, 'mismatch'
    print('match',delta,time.time()-t)
