"""Recover the accepted canonical non-descent witness without huge integers."""
from pathlib import Path
from fractions import Fraction as F
import json
from affine_origin import Linear,Origin,v2

def main():
    p1=244875;bounds={'L1':(p1,True),'L2':(p1+3,False)}
    L1=Linear({'L1':1});L2=Linear({'L2':1});L0=655360
    state=Origin();rows=[]
    steps=[('b',L2),('b',L1),('b',Linear.constant(L0)),('a',6),('a',1),('b',Linear.constant(10))]
    valuations=[None,p1,17,5,6,1]
    for (kind,arg),expected in zip(steps,valuations):
        getattr(state,kind)(arg)
        result=state.beta.exact_valuation(bounds)
        assert result==expected
        assert v2(state.alpha)==-state.loss
        rows.append(dict(step=kind,loss=state.loss,alpha=str(state.alpha),
                         beta=state.beta.serialize(),theta=state.theta.serialize(),
                         exact_beta_valuation=result))
    five=rows[3];six=rows[4]
    assert five['beta']=={'1':'983072','L1':'13/8','L2':'55/32'}
    assert six['beta']=={'1':'819264','L1':'19/16','L2':'73/64'}
    assert v2(819264)==6
    # Independent numeric affine update on moderate algebraic lifts.
    # These substitute the source symbols, not canonical root histories.
    checks=0
    for e1,e2 in ((25,30),(40,48),(64,80)):
        for u1,u2 in ((1,1),(3,5),(5,7)):
            vals={'L1':u1*(1<<e1),'L2':u2*(1<<e2)}
            X0=1<<(e2+12);x=F(X0);theta=F(X0+1)
            for (kind,arg),row in zip(steps,rows):
                if kind=='b':
                    y=arg.evaluate(vals);x=3*x/4+y;theta=theta+y-1
                else:x=2*theta+6*arg-x/2;theta+=6*arg+3
                assert x==F(row['alpha'])*X0+Linear(row['beta']).evaluate(vals)
                assert theta==X0+Linear(row['theta']).evaluate(vals)
                checks+=1
    # The engine must not silently infer a valuation through cancellation.
    ambiguous=Linear({'L1':1,'L2':-1})
    assert ambiguous.exact_valuation({'L1':(10,True),'L2':(10,True)}) is None
    out=dict(status='PASS',review_status='unreviewed',symbolic_rows=rows,
             numeric_substitution_checks=checks,cancellation_control='unresolved as required',
             scope='Accepted WITNESS provenance is imported from PROOF_SPECTRUM section 4. This is an affine replay, not a new reachability theorem or global bound.')
    Path(__file__).with_name('affine_origin_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='symbolic_rows'}))
    print(json.dumps([five,six]))

if __name__=='__main__':main()
