"""Exact inequality checks for the all-scale first-failure loss budget.
The analytic argument, not the finite samples, supplies infinite scope.
"""
from pathlib import Path
import json

def g(n):
    z=6*n*n+5
    return (z-1).bit_length()

def P(n):return 2*g(n)**2+1345

checks=0
for q in range(12,4096):
    assert 12*q*q<1<<(q-1);checks+=1
for q in range(18,4096):
    assert 24*(q+1)*q*q+6*q+5<1<<q;checks+=1

for J in range(16,4096):
    B=1<<(J//2-3)
    Q=max(17,(60*B**3).bit_length()-1)
    assert Q<=B
    assert 3*(B+Q)**2+4<1<<J
    checks+=1
for J in range(64,4096):
    B=(1<<J)//(128*J*J)
    assert B>0 and 2*B<=1<<J
    assert P(2*B)<=9*J*J
    assert 6*B*P(2*B)+4<1<<J
    checks+=1

examples=[]
for J in (16,32,64,128,256):
    examples.append(dict(root_parameter=J,C1_only_loss_budget=1<<(J//2-3),
                         clock_lemma_loss_budget=(1<<J)//(128*J*J) if J>=64 else None))
result=dict(result='PASS',inequality_checks=checks,examples=examples,
            scope='Conditional coefficient-loss safety budgets, not return counts or termination')
Path(__file__).with_name('failure_budget_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
