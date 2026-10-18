"""Full-pair ENTRY checks and integer first-tie source endpoint bounds."""
from collections import Counter
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_global_ext'/'route_c'))
from fdata import small_full


def main():
    table=small_full(8192)
    counts=Counter()
    for n,row in table.items():
        if n<4 or not row['odd'] or row['typ']=='a':continue
        A,Y=row['A'],row['Y']
        tau=row['tau']
        assert A[1]+Y[1]==3*tau+1
        # Independent first symbolic call: beta base zero, defect lambda -1.
        beta=A[1]+2*Y[1]+3
        theta=3*(1+tau)+1
        assert beta==row['x'][1]==3*tau+4+Y[1]
        assert theta-beta==-Y[1]
        if row['typ']=='b':
            assert Y[1]==0 and theta==beta and tau%2==0
        counts[row['typ']]+=1
    tested=0
    for J in list(range(128,100000))+[(1 << e)+d for e in range(17,4097) for d in (-1,0,1)]:
        bound=max(4,2*((3*(J-1)**2+4).bit_length()-1))
        assert 2*bound<=J
        # Check exact half endpoint, including the smallest possible M.
        M=J-bound
        assert J<=2*M
        tested+=1
    search=json.loads(Path(__file__).with_name('root_search.json').read_text())
    assert search['productive_parameters']==2621
    assert all(r['escape_count']==0 for r in search['results'])
    zero=next(r for r in search['results'] if r['defect']==0)
    assert zero['counts']=={'1':2621,'2':128}
    result=dict(result='PASS',review_status='unreviewed',
                full_pair_entry_checks=dict(counts),endpoint_inequality_checks=tested,
                root_projection_comparisons=sum(r['projection_comparisons'] for r in search['results']),
                scope='Exact entry identities and finite endpoint/root checks; no global EXT proof.')
    Path(__file__).with_name('entry_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
