"""exp2: brute-force scan of synthetic defects e in [-2^(J+1), 2^(J+1)] for 6<=J<=JM:
how often S*_e(J) has an over-tie / exact tie, at which chain index t, at which return type."""
import sys, collections
import tielab as T
L=T.Lab(200)
JM=int(sys.argv[1]) if len(sys.argv)>1 else 14
for J in range(6,JM+1):
    c=collections.Counter(); where=collections.Counter(); typ=collections.Counter(); n=0
    for e in range(-(1<<(J+1)),(1<<(J+1))+1):
        r=L.symstar(J,e); n+=1
        ks=[ch['kind'] for ch in r['ch']]
        nover=ks.count('over')
        c[(r['st'], min(nover,2))]+=1
        for ch in r['ch']:
            if ch['kind']!='free': where[(ch['kind'],ch['t'])]+=1; typ[(ch['kind'],ch['typ'])]+=1
    print('J=%d  n=%d  (status,#over):%s'%(J,n,dict(sorted(c.items()))))
    print('      tie chain index:',dict(sorted(where.items())),' return type:',dict(typ))
