"""Exact crossing-table classification of repeated mixed blocks."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
N=4096;X=vm.Xdata(N,SMALL=N)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in X.items()}
def val(z):return (abs(z)&-abs(z)).bit_length()-1 if z else 10**9
records=[]
for q in range(5,N):
    j=q;d=G=h=0
    while True:
        kind,H,Y,e=X[j-1]
        if sum(H)%2==0:break
        if kind=='a':
            T=d+1+tau[j-1];r=1+val(T)
            records.append(dict(q=q,p=j,h=h,G=G,T=T,output=r,
                                separation=q-G-r))
            assert r<q-G
            break
        d+=1+tau[j-1];G+=1+e;h+=1
        j=val(H[1]+2*Y[1]+3)
counts={str(r):sum(a['output']==r for a in records) for r in sorted({a['output'] for a in records})}
result=dict(productive=len(records),outputs=counts,min_separation=min(r['separation'] for r in records),
            nonterminal=[r for r in records if r['output']>4],records=records)
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
Path(__file__).with_name('repeat_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
