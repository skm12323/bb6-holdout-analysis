"""Exhaustive binary refinement of ONLY unresolved k residue classes."""
from pathlib import Path
import json
from modular import follow
pending=[(0,0)];closed=[];unresolved=[];counts={}
while pending:
    r,L=pending.pop();result=follow(r,L);counts[L]=counts.get(L,0)+1
    if result['status']=='closed':closed.append(dict(L=L,**result))
    elif L<60:
        pending.extend([(r,L+1),(r+(1<<L),L+1)])
    else:unresolved.append(dict(L=L,**result))
assert sum(1<<(60-r['L']) for r in closed)+len(unresolved)==1<<60
summary=dict(closed_cylinders=len(closed),unresolved=unresolved,
             max_suffix_steps=max(r['suffix_steps'] for r in closed),
             max_suffix_chains=max(len(r['path']) for r in closed),
             min_margin=min(r['min_margin'] for r in closed),nodes=sum(counts.values()))
print(json.dumps(summary,indent=2))
Path(__file__).with_name('refined_certificate.json').write_text(json.dumps(dict(summary=summary,closed=closed),indent=2)+'\n')
