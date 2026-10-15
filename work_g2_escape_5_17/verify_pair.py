"""Full pair-map checks from compatible (5,17,Q) local prefixes."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
from a_certificate import follow,val
X=vm.Xdata(1024,SMALL=1024)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in X.items()}
cases=0
for Q in (54,90,125,161,198,234,343,484,700,1021):
    assert X[Q-1][0]=='a' and sum(X[Q-1][1])%2
    k=tau[Q-1]//2
    for w in (1,3):
        x=(1<<Q)*w;v=(x>>17)+1
        while (x//2+(1<<15)*v+21)%3!=2:v+=2
        u=(x>>4)-4096*v-3
        assert u>0 and u%2 and v%2
        theta=x//2+(1<<15)*v-27
        sigma=Q+4
        A=(1<<sigma,196608*v-x+37)
        P=[(1<<sigma,3*x//2-163840*v-68)]
        assert A[1]>=0 and P[0][1]>=0
        s=(theta-5)//3;s0=s;i=sigma+1;next_top=0;path=[]
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
            else:A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3);P=tail
            i=ni;s+=1
            assert s-s0<10000
        cert=follow(k%(1<<16),16)
        assert cert['status']=='closed'
        assert path==[5,17,Q]+cert['path']
        assert s-s0==16+1+tau[Q-1]+cert['cost']
        # Coefficient identity for a resonant a followed by parameter 17.
        Y=x//2+(1<<16)*v+6*(k+7)
        Z=3*Y//2-(1<<16)*v
        delta=x-(1<<17)*v
        assert Z-Y==delta//4+3*(k+7)
        cases+=1
result=dict(result='PASS',full_pair_cases=cases,
            scope='Compatible local prefixes, not claimed actual orbit witnesses')
print(json.dumps(result,indent=2))
Path(__file__).with_name('pair_checks.json').write_text(json.dumps(result,indent=2)+'\n')
