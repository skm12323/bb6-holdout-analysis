"""Classify the first a-return in completed copied source suffixes."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
N=4096;X=vm.Xdata(N,SMALL=N)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in X.items()}
def val(n):return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9
records=[]
for q in range(63,N):
    kind,H,Y,e=X[q-1]
    if kind=='a' or sum(H)%2==0:continue
    initial_kind=kind
    x=H[1]+2*Y[1]+3;c=H[0]+2*Y[0];T=3*tau[q-1]+5
    prefix=[]
    while True:
        j=val(x);prefix.append(j);kind,H,Y,e=X[j-1]
        if sum(H)%2==0:
            records.append(dict(q=q,result='even_before_a',prefix=prefix));break
        if kind=='a':
            out=2*T-x//2+3*tau[j-1];r=val(out)
            if r==3:
                assert initial_kind=='b' and prefix==[5]
                assert X[q-2][0]=='a' and tau[q-2]==tau[q-1]
                source_base=(3*tau[q-1]+4)//32
                assert 3*tau[q-1]+4==32*source_base and source_base%2
                assert out==48*source_base+8 and val(out+88)==4
            records.append(dict(q=q,result='collision' if r==3 else 'terminal_shortcut',
                                prefix=prefix,r=r,S=val(c)-1,source_x_out=out,
                                center=out+88));break
        cx=H[0]+2*Y[0];lx=H[1]+2*Y[1]+3
        c=cx*(c>>j);x=cx*(x>>j)+lx;T+=3*tau[j-1]+3
counts={k:sum(r['result']==k for r in records) for k in sorted({r['result'] for r in records})}
print(counts)
print([r for r in records if r['result']=='collision'][:15])
Path(__file__).with_name('source_classification.json').write_text(json.dumps(dict(counts=counts,records=records),indent=2)+'\n')
