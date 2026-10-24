"""Necessary gateway graph with the missing parameter-five clock condition."""
from pathlib import Path
from collections import deque
import json
import sys
import sys
sys.path.insert(0,'D:/math_cc/work_c3_drift')
from verify_shift_transport import Calendar,val
sys.path.insert(0,'D:/math_cc/work_global_ext/route_c')
from fdata import lam_walk

def analyze():
    cal=Calendar(256)
    base=lam_walk(16381)
    assert all(t<=n for n,t in enumerate(base['tau']))
    aindices=[n for n in range(16381) if base['odd'][n] and base['typ'][n]==97]
    gap_checks=0
    for n,nxt in zip(aindices,aindices[1:]):
        k=base['tau'][n]//2
        if val(6*k+4)==3:
            assert nxt-n>=5;gap_checks+=1
    assert cal.kernels[3]['advance']==5
    assert all(n+1>=17 for n in aindices if (base['tau'][n]//2)%16==6)
    ks={m:cal.crossing(m-1)['time']//2 for m in range(5,257)
        if cal.crossing(m-1)['odd'] and cal.crossing(m-1)['kind']=='a'}
    def admissible(a,b):
        # A pair of catapults requires the two five-input phases to be 5 mod 16.
        if (12+6*ks[a])%16:return False
        e=min(a-2,b);phase=(-21-9*ks[a])%(1<<e)
        return (phase-5)%(1<<min(e,4))==0
    vertices=[(a,b) for a in ks for b in ks if admissible(a,b)]
    graph={v:[] for v in vertices};indeg={v:0 for v in vertices}
    for a,b in vertices:
        z=4-ks[a]+3*ks[b];v=10**9 if z==0 else val(z)
        for c in ks:
            if (b,c) in graph and v>=min(a-2,b-2,c):
                # In the exact four-term identity, a unique lowest
                # 2-adic valuation cannot cancel. Do not retain only divisibility.
                valuations=[a,b,c+2]+([2+v] if z else [])
                if valuations.count(min(valuations))<2:continue
                graph[a,b].append((b,c));indeg[b,c]+=1
    queue=deque(v for v in vertices if indeg[v]==0);order=[]
    while queue:
        v=queue.popleft();order.append(v)
        for w in graph[v]:
            indeg[w]-=1
            if not indeg[w]:queue.append(w)
    assert len(order)==len(vertices)
    length={};nxt={}
    for v in reversed(order):
        if graph[v]:
            w=max(graph[v],key=lambda w:length[w]);length[v]=1+length[w];nxt[v]=w
        else:length[v]=0
    v=max(vertices,key=lambda v:length[v]);maximum=2+length[v];path=list(v)
    while v in nxt:v=nxt[v];path.append(v[1])
    # Replay the shared initial-clock constraints along the longest graph path.
    residue=5;precision=4;elapsed=0;consistent=True
    for a,b in zip(path,path[1:]):
        e=min(a-2,b);need=(-21-9*ks[a]-elapsed)%(1<<e)
        if (need-residue)%(1<<min(e,precision)):
            consistent=False;break
        if e>precision:residue=need;precision=e
        elapsed+=12+6*ks[a]
    out=dict(status='PASS',review_status='unreviewed',parameter_range=[5,256],
             vertices=len(vertices),edges=sum(map(len,graph.values())),acyclic=True,
             maximum_catapult_labels=maximum,longest_necessary_word=path,
             longest_word_clock_consistent=consistent,
             initial_clock_residue=str(residue),initial_clock_precision=precision,
             internal_labels=[m for m,k in ks.items() if k%16==6],
             linear_clock_checks=16381,parameter_three_pointer_gaps=gap_checks,
             scope='Necessary-condition graph. Upper bound is valid for actual trains; the displayed longest word is not claimed reachable.')
    Path(__file__).with_name('clock_filtered_train_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':analyze()
