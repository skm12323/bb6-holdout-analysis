"""Stream actual crossing records to find unresolved R/E b/c suffix families.
Only first-return b/c entries are scanned. Every failure is retained.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
N=int(sys.argv[1]) if len(sys.argv)>1 else 100000
small={};counts={};failures=[];seen=0;maxpath=0
def val(z):return (abs(z)&-abs(z)).bit_length()-1 if z else 10**9
def follow(q,first,family):
    x=(1<<q,1<<(q+1),0)
    T=((1<<(q-1))+(1<<15)+21,1<<q,1<<16) if family=='R' else ((1<<q)-(1<<15)-18,1<<(q+1),-(1<<16))
    sigma=q+1;path=[]
    for step in range(40):
        j=val(x[0])
        if j>=min(map(val,x[1:])):
            return dict(status='collision',path=path,valuations=list(map(val,x)),
                        constant=x[0],v_slope=x[2])
        if j>=sigma:return dict(status='margin',path=path,j=j)
        data=first if not path else small.get(j-1)
        if data is None:return dict(status='table',path=path,j=j)
        kind,H,Y,e=data;path.append(j)
        if sum(H)%2==0:return dict(status='closed',path=path)
        tau=(H[1]+(Y[1] if Y else 0)-1)//3
        if kind=='a':xn=tuple(2*T[i]-x[i]//2+(3*tau if i==0 else 0) for i in range(3))
        else:
            assert all(z%(1<<j)==0 for z in x)
            c=H[0]+2*Y[0];b=H[1]+2*Y[1]+3
            xn=tuple(c*(x[i]>>j)+(b if i==0 else 0) for i in range(3))
        T=(T[0]+3*tau+3,T[1],T[2]);sigma-=1+e;x=xn
    return dict(status='budget',path=path)
def callback(n,data):
    global seen,maxpath
    if n<256:small[n]=data
    q=n+1;kind,H,Y,e=data
    if q<1024 or kind=='a' or sum(H)%2==0:return
    for family in ('R','E'):
        result=follow(q,data,family);seen+=1
        counts[family+'_'+result['status']]=counts.get(family+'_'+result['status'],0)+1
        maxpath=max(maxpath,len(result['path']))
        if result['status']!='closed':
            result.update(q=q,family=family,initial_type=kind)
            # Avoid enormous unneeded high coefficients: exact low constants
            # are emitted only when they fit in a short diagnostic.
            if 'constant' in result:
                c=result.pop('constant');result['constant_mod_2_32']=c%(1<<32)
            failures.append(result)
            if len(failures)<=8:print(json.dumps(result),flush=True)
vm.Xdata(N,cb=callback,SMALL=0)
result=dict(result='COMPLETED',crossing_limit=N,tested_families=seen,counts=counts,
            max_path=maxpath,failures=failures,
            scope='Actual source records; local families are not asserted orbit-reachable')
print(json.dumps({k:v for k,v in result.items() if k!='failures'},indent=2))
Path(__file__).with_name(f'scan_{N}.json').write_text(json.dumps(result,indent=2)+'\n')
