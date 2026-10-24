"""Exact two-a recurrence and necessary clock-congruence graph."""
from pathlib import Path
from collections import deque
from fractions import Fraction as F
import json
import sys
import sys
sys.path.insert(0,'D:/math_cc/work_c3_drift')
from verify_shift_transport import Calendar,val

def main():
    cal=Calendar(256)
    ks={m:cal.crossing(m-1)['time']//2 for m in range(5,257)
        if cal.crossing(m-1)['odd'] and cal.crossing(m-1)['kind']=='a'}
    identities=0
    # Deliberately algebraic checks: valuations/provenance are not assumed.
    for x in (32,96,160,224):
        for th in (37,101,165):
            for k in (1,2,6,20):
                for ell in (1,6,20):
                    xx=F(x);tt=F(th);ys=[]
                    for kk in (k,ell,1):
                        y=2*tt+6-xx/2;ys.append(y)
                        xx=y;tt+=9
                        xx=2*tt+6*kk-xx/2;tt+=3+6*kk
                    assert 4*ys[2]-5*ys[1]+ys[0]==12*(4-k+3*ell)
                    identities+=1
    ms=sorted(ks);vertices=[(a,b) for a in ms for b in ms]
    graph={v:[] for v in vertices};indegree={v:0 for v in vertices}
    for a,b in vertices:
        z=4-ks[a]+3*ks[b]
        v=10**9 if z==0 else val(z)
        for c in ms:
            if v>=min(a-2,b-2,c):
                graph[a,b].append((b,c));indegree[b,c]+=1
    queue=deque(v for v in vertices if indegree[v]==0);order=[]
    while queue:
        v=queue.popleft();order.append(v)
        for w in graph[v]:
            indegree[w]-=1
            if not indegree[w]:queue.append(w)
    acyclic=len(order)==len(vertices)
    cycle=None;cycle_clock=None
    if not acyclic:
        sys.setrecursionlimit(20000)
        color={};stack=[];position={}
        def visit(v):
            nonlocal cycle
            color[v]=1;position[v]=len(stack);stack.append(v)
            for w in graph[v]:
                if color.get(w,0)==0:
                    if visit(w):return True
                elif color[w]==1:
                    cycle=stack[position[w]:].copy();return True
            stack.pop();position.pop(v);color[v]=2;return False
        for v in vertices:
            if not color.get(v) and visit(v):break
        advance=sum(12+6*ks[a] for a,b in cycle)
        required=max(min(a-2,b) for a,b in cycle)
        cycle_clock=dict(advance=advance,valuation=val(advance),required_bits=required,
                         repeating_same_cycle_not_excluded=val(advance)>=required)
    maximum=None;witness=None
    if acyclic:
        length={};successor={}
        for v in reversed(order):
            if graph[v]:
                w=max(graph[v],key=lambda w:length[w]);length[v]=1+length[w];successor[v]=w
            else:length[v]=0
        start=max(vertices,key=lambda v:length[v]);maximum=2+length[start]
        witness=list(start);v=start
        while v in successor:v=successor[v];witness.append(v[1])
    diagonal=[]
    for m,k in ks.items():
        assert val(4+2*k)<m-2
        diagonal.append(m)
    # The polynomial induction used for the no-three-identical lemma.
    assert all((m-1)**2+4 < 1<<(m-2) for m in range(8,4097))
    out=dict(status='PASS',review_status='unreviewed',algebra_identity_checks=identities,
             parameter_interval=[5,256],odd_a_parameters=len(ms),vertices=len(vertices),
             edges=sum(map(len,graph.values())),acyclic=acyclic,
             max_catapults_if_acyclic=maximum,necessary_graph_longest_word=witness,
             sample_cycle=cycle,sample_cycle_clock=cycle_clock,
             diagonal_checks=len(diagonal),
             scope='Graph is a necessary-condition overapproximation. Longest word is not asserted reachable; an acyclic upper bound applies to all actual trains in the interval.')
    Path(__file__).with_name('gateway_train_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
