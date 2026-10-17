"""stream.py -- one pass of the universal walk F to N crossings, processing each crossing n as soon as F's
step tau(n) has been executed.  Memory-light (compact rows; full rows only for n<=SMALL).
For every n it computes
  (1) S(J), J=n+1, through the beta-walk (Lemma BR) from its chain-1 state (Cor. BR'), with the tie test
      j_t < J-Gamma_t (Lemma T(1)), Lemma T(2), the h-identity, Lemma Z, Lemma P checks;
  (2) the deep route-a/route-b tails for m=n+1 (Cor. BR': state (1+tau,3tau+2)/(1+tau,3tau+4) with
      v2(3tau+off)=m) for 2 values of tau (the canonical residue and a random lift), checking independence.
Writes a JSON summary."""
import sys,random,json,time
from collections import Counter
def v2(z): return (z & -z).bit_length()-1 if z else 10**18
N=int(sys.argv[1]); SMALL=4000; random.seed(12345)
R={}            # compact rows
def row_par(A,n): return ((A[0]+A[1])%2==1) if n>=2 else False

stat=Counter(); rdist=Counter(); deep={'a':Counter(),'b':Counter()}; deepfirst={'a':{},'b':{}}
deepnd=Counter(); deepdep=Counter(); ex={}; jsJ={}; viol=Counter()
G_={'maxG':0,'minh':10**9,'maxj1':0,'maxjlater':0}

def bwalk(j,d,bx):
    """beta-walk from a chain with parameter j=v2(bx); returns (list of (j,d,bx,typ,eps,n_prev), why)."""
    bu=bx>>j; out=[]
    while True:
        n=j-1
        row=R.get(n)
        if row is None: return out,'OUT'
        if not row['odd']: return out,'END'
        if row['typ']=='a': bx=6*d+2+3*row['tau']-(bu<<n)
        else:
            if 'cW' not in row: return out,'NEEDCW'
            bx=bu*row['cW']+row['lW']
        d+=1+row['tau']; jn=v2(bx); out.append((jn,d,bx,row['typ'],row['eps'],n))
        if len(out)>10000: return out,'LONG'
        bu=bx>>jn; j=jn

def jsJ_store(J,js):
    if J<=SMALL: jsJ[J]=js

def process(n):
    row=R[n]; J=n+1
    if J>=3:
        if not row['odd']:
            rdist[0]+=1; jsJ_store(J,[J])
        else:
            tau=row['tau']; typ=row['typ']
            bx1=3*tau+2 if typ=='a' else row['lW']
            d1=1+tau; j1=v2(bx1)
            assert 1<=bx1<=6*d1-1
            G_['maxj1']=max(G_['maxj1'],j1)
            chains=[(j1,d1,bx1,typ,row['eps'],n)]
            tail,why=bwalk(j1,d1,bx1)
            if why!='END': viol['S(J) '+why]+=1
            chains+=tail
            js=[J]+[c[0] for c in chains]
            Gs=[0]
            for c in chains: Gs.append(Gs[-1]+1+c[4])
            pin=None
            for t in range(1,len(js)):
                jt=js[t]; Gt=Gs[t]; h=J-Gt-jt
                G_['minh']=min(G_['minh'],h); G_['maxG']=max(G_['maxG'],Gt)
                if h<1: viol['TIE']+=1
                jd,dd,bx,ty,ep,nn=chains[t-1]
                if not (1<=bx<=6*dd-1): viol['LemmaT2']+=1
                if t>=2:
                    G_['maxjlater']=max(G_['maxjlater'],jt)
                    dh=h-(J-Gs[t-1]-js[t-1])
                    if dh!=js[t-1]-jt-1-ep: viol['h-identity']+=1
                    if ty!='a':
                        stat['bc']+=1
                        if dh<1: viol['bc-gain']+=1
                    else:
                        stat['a']+=1
                        if jt>=js[t-1]: stat['nondescent']+=1
                        k=R[nn]['tau']//2; pb=chains[t-2]
                        z0=3*pb[2]-12*pb[1]-4; z1=3*bx-12*dd-4
                        if 2*z1!=-z0-12*k-24: viol['Z']+=1
                        stat['Z']+=1
                if t==1:
                    m=js[1]; rho=(3*dd+1)%(1<<m); rho=rho if rho<(1<<(m-1)) else rho-(1<<m)
                    pin=(dd,rho,m); stat['rho1=%d'%rho]+=1
                else:
                    ds,rho,mu=pin
                    if (3*dd+1-(rho+3*(dd-ds)))%(1<<mu): viol['P']+=1
                    stat['P']+=1
                    if ty=='a' and jt<js[t-1]: pin=(dd,3+3*(R[nn]['tau']//2),jt-1)
            r=len(js)-1; rdist[r]+=1
            if r>=2 and r not in ex: ex[r]=(J,js,''.join(c[3] for c in chains))
            jsJ_store(J,js)
    # deep tails m=n+1
    m=n+1
    if m<2: return
    for route,off in (('a',2),('b',4)):
        base=(-off*pow(3,-1,1<<m))%(1<<m)
        if ((3*base+off)>>m)%2==0: base+=1<<m
        outs=set()
        for rep in range(2):
            tau=base+((random.getrandbits(64)|1)<<(m+1) if rep else 0)
            out,why=bwalk(m,1+tau,3*tau+off)
            js=tuple(o[0] for o in out); outs.add((js,why))
            deepnd[route]+=sum(1 for i2,jj in enumerate(js) if jj>=(m if i2==0 else js[i2-1]))
        if len(outs)>1: deepdep[route]+=1
        js,why=sorted(outs)[0]
        if why!='END': deepdep[route+'_'+why]+=1
        L=len(js); deep[route][L]+=1
        if L not in deepfirst[route]: deepfirst[route][L]=(m,js)

t0=time.time()
A=(1,1); Q=[]; i=0; s=0; seen=0
while seen<=N:
    k=len(Q)
    reads=[] if k>=2 else ([i] if k==1 else [i,i+1])
    newn=[]
    for n in reads:
        if n==seen:
            typ='a' if (k==0 and i==n) else ('b' if k==0 else 'c')
            R[n]=dict(typ=typ,tau=s,eps=n-v2(A[0]),odd=row_par(A,n)); newn.append(n); seen+=1
    ents=list(Q[:2]); a=i
    while len(ents)<2: ents.append((1<<a,0)); a+=1
    b,c=ents
    if (A[0]+A[1])%2==0:
        A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3); newp=[]
    else:
        x=(A[0]+2*b[0],A[1]+2*b[1]+3); j=v2(x[1]); assert j<v2(x[0]) and A[0]%2==0
        for n in newn:
            R[n]['lW']=x[1]; R[n]['omega']=j
            R[n]['cW']=x[0]
        u=(x[0]>>j,x[1]>>j)
        newp=[(u[0]<<t,u[1]<<t) for t in range(j-1)]+[(c[0]+A[0]//2,c[1]+(A[1]+1)//2)]
        A=(u[0],u[1]+1)
    if k>=2: Q=Q[2:]
    else: i+=2-k; Q=[]
    Q=newp+Q; s+=1
    for n in newn:
        process(n)
        if n>SMALL: R[n].pop('cW',None)
    if newn and newn[-1]%50000==0: print('n=%d %.0fs'%(newn[-1],time.time()-t0)); sys.stdout.flush()
ss=Counter()
for J,js in jsJ.items():
    if R[J-1]['odd'] and R[J-1]['typ']=='a' and len(js)>=3 and R[js[1]-1]['odd'] and R[js[1]-1]['typ'] in 'ab':
        J2=js[2]
        if J2 in jsJ: ss['ok' if js[2:]==jsJ[J2] else 'BAD']+=1
        else: ss['J2<3']+=1
out=dict(N=N,seconds=round(time.time()-t0),r_dist=dict(sorted(rdist.items())),examples=ex,**G_,
         steps={k:v for k,v in stat.items() if not k.startswith('rho')},
         chain1_rep={k:v for k,v in stat.items() if k.startswith('rho')},violations=dict(viol),
         deep_tails={r:dict(sorted(deep[r].items())) for r in deep},deep_first=deepfirst,deep_nondescents=dict(deepnd),
         deep_tau_dependence=dict(deepdep),SS=dict(ss))
print(json.dumps(out,indent=1,default=str))
json.dump(out,open('stream_%d.json'%N,'w'),indent=1,default=str)
