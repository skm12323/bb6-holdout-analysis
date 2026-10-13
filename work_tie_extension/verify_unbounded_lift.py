"""Mass-compatible j=5 states with arbitrarily high next parameter.
No assertion that these states lie on the distinguished F orbit.
"""
import json
from pathlib import Path

def v2(n):
    assert n > 0
    return (n & -n).bit_length()-1

def check(q):
    sigma = q+2
    i = sigma+1
    s = 1 << (q-2)
    A = (1 << sigma, (1 << (q-1))-27)
    P = [(1 << sigma, (1 << (q-2))+28)]
    assert (3*s+5) % 32 == 5
    js = []
    for step in range(4):
        assert sum(c for c,l in [A]+P) == 1 << i
        assert sum(l for c,l in [A]+P) == 3*s+1
        entries = P[:2]
        ni = i
        while len(entries)<2:
            entries.append((1 << ni,0))
            ni += 1
        b,c = entries
        rest = P[2:]
        if sum(A) % 2:
            cx,lx = A[0]+2*b[0], A[1]+2*b[1]+3
            j = v2(lx)
            assert j < v2(cx)
            js.append(j)
            if step == 3:
                assert j == q and lx == 1 << q and v2(cx) == q+1
                break
            assert step == 0 and j == 5
            u = (cx >> j,lx >> j)
            D = (c[0]+A[0]//2,c[1]+(A[1]+1)//2)
            A = (u[0],u[1]+1)
            P = [(u[0] << t,u[1] << t) for t in range(j-1)]+[D]+rest
        else:
            A = (A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3)
            P = rest
        i = ni
        s += 1
    assert js == [5,q]

qs = list(range(7,513))+[4096,65536]
for q in qs:
    check(q)
result = dict(result='PASS', cases=len(qs), contiguous_q=[7,512], extra_q=[4096,65536],
              scope='Synthetic mass-compatible states, not claimed reachable from F start')
Path(__file__).with_name('unbounded_lift_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
