"""Finite anchoring and exponent bookkeeping; enormous ancestor pointers are NOT simulated."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_el'))
import verify_el as ve

tau,typ,par,chains,stats,steps=ve.real_walk(250000)
k=(5*(1<<16)-2)//3
s=2*k
assert chains[s]==(17,1,'F')
rho=next(n for n in range(250000) if tau[n]==s and typ[n]=='a')
assert rho==244873
p1=rho+2
assert p1==244875

# For the chosen fire-time target K(j), rho(j)+2 < 2^(j+3).
p2_exponent=p1+3
p3_inner_exponent=p1+4
available_K_exponent=(1<<499997)-2
assert (1<<p3_inner_exponent)+2<available_K_exponent
assert 3*(10**8)**2+4 < 1<<55

result=dict(result='PASS',anchor_parameter=17,anchor_k=k,anchor_s=s,anchor_rho=rho,
            p1=p1,p2_bound='2^'+str(p2_exponent),
            p3_bound='2^(2^'+str(p3_inner_exponent)+')',
            accepted_parameter_cutoff='K=2^(2^499997-2)',
            witness_chain=['p3','p2',p1,17,5,6,1],
            exits=6,scope='p2 and p3 are existentially specified fire positions, not numerically computed')
Path(__file__).with_name('finite_witness_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
