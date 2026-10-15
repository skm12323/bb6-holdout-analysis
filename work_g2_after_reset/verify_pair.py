"""Cross-check compatible reset states using the full integer pair map."""
from pathlib import Path
import json
from probe import follow,tau,val
count=0;max_steps=0
for q in list(range(63,256))+[256,511,1024,2048,4095]:
    for V in (1,12345):
        K=46+3*(1<<61)*V
        u=4*K+1
        while ((1<<(q-1))*u+K)%3!=2:u+=2
        x=(1<<q)*u;T=x//2+K;s=(T-5)//3;s0=s;sigma=q+2
        A=(1<<sigma,2*T-x-5)
        P=[(1<<sigma,x-T+1)]
        assert A[1]>=0 and P[0][1]>=0
        i=sigma+1;next_top=0;path=[]
        while P:
            assert sum(c for c,l in [A]+P)==1<<i
            assert sum(l for c,l in [A]+P)==3*s+1
            entries=P[:2];ni=i
            while len(entries)<2:entries.append((1<<ni,0));ni+=1
            b,c=entries;tail=P[2:]
            if sum(A)%2:
                cx,lx=A[0]+2*b[0],A[1]+2*b[1]+3;j=val(lx)
                assert j<val(cx)
                if s-s0==next_top:
                    path.append(j);next_top=s-s0+1+tau[j-1]
                base=(cx>>j,lx>>j)
                D=(c[0]+A[0]//2,c[1]+(A[1]+1)//2)
                A=(base[0],base[1]+1)
                P=[(base[0]<<t,base[1]<<t) for t in range(j-1)]+[D]+tail
            else:
                A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3);P=tail
            i=ni;s+=1
            assert s-s0<10000
        expected=follow(q)
        assert expected['status']=='closed' and path==expected['path']
        assert s-s0==sum(1+tau[j-1] for j in path)+1
        count+=1;max_steps=max(max_steps,s-s0)
result=dict(result='PASS',full_pair_cases=count,max_observed_steps=max_steps,
            scope='Compatible local reset states, not orbit reachability')
print(json.dumps(result,indent=2))
Path(__file__).with_name('pair_checks.json').write_text(json.dumps(result,indent=2)+'\n')
