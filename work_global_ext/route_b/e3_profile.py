"""Profile of S(J) for 3<=J<=N+1 and checks of the route-B lemmas:
 BR  beta-walk == S(J) (j, beta_x, d at every chain; same stop)
 H   h_{t+1}-h_t = j_t-j_{t+1}-1-eps(n_t); >=1 at b/c steps; h_t>=1 at every chain
 Z   a-steps: z_{t+1} = -z_t/2 - 6k - 12, z := 3 beta_x - 12 d - 4
 P   pins: Theta_t := 3d_t+1 == rho_s + 3(d_t-d_s) (mod 2^mu_s) for s = last a-created chain (descending) or s=1
 SS  route a, second return odd of type a/b:  chain list of S(J) from chain 2 == chain list of S(J2) (j's), J2 = j_2
 L   Lemma T(2) 1<=beta_x<=6d-1; non-descents counted."""
import sys,time,json
from collections import Counter
from core import *
N=int(sys.argv[1]); t0=time.time(); T=load(N); print('walk/load %.1fs'%(time.time()-t0))
rc=Counter(); stats=Counter(); jmax_after1=0; Gmax=0; minh=10**9; ex={}
js_of={}
for J in range(3,N+2):
    se,st=symexit(J,T); assert st=='END',(J,st)
    bw,bst=beta_walk(J,0,0,T); assert bst=='END'
    assert [(c['j'],c['x'][1],c['d']) for c in se]==[(a,bx,dd) for (a,dd,bx,_) in bw],('BR',J)
    js=[J]+[c['j'] for c in se]; js_of[J]=js
    r=len(se); rc[r]+=1
    if r>=2 and (r not in ex): ex[r]=(J,js,''.join(c['typ'] for c in se))
    # H, Z, P, L
    dlist=[0]+[c['d'] for c in se]; bx=[None]+[c['x'][1] for c in se]
    G=[0]+[c['G'] for c in se]
    pin=None
    for t in range(1,r+1):
        h=J-G[t]-js[t]; minh=min(minh,h); assert h>=1
        assert 1<=bx[t]<=6*dlist[t]-1
        Gmax=max(Gmax,G[t])
        if t>=2:
            n=js[t-1]-1; row=T[n]
            dh=(J-G[t]-js[t])-(J-G[t-1]-js[t-1])
            assert dh==js[t-1]-js[t]-1-row['eps']
            if row['typ']!='a': assert dh>=1; stats['bc']+=1
            else:
                stats['a']+=1
                if js[t]>=js[t-1]: stats['nondescent']+=1
                k=row['tau']//2
                z0=3*bx[t-1]-12*dlist[t-1]-4; z1=3*bx[t]-12*dlist[t]-4
                assert 2*z1==-z0-12*k-24, ('Z',J,t); stats['Zchecks']+=1
            jmax_after1=max(jmax_after1,js[t])
        # pins
        if t==1:
            Th=3*dlist[1]+1; rho=Th%(1<<js[1]); rho=rho if rho<(1<<(js[1]-1)) else rho-(1<<js[1])
            pin=(1,rho,js[1]); stats['pin_rho1_'+str(rho)]+=1
        else:
            s,rho,mu=pin
            assert (3*dlist[t]+1-(rho+3*(dlist[t]-dlist[s])))%(1<<mu)==0,('P',J,t); stats['Pchecks']+=1
            n=js[t-1]-1
            if T[n]['typ']=='a' and js[t]<js[t-1]:
                pin=(t,3+3*(T[n]['tau']//2),js[t]-1)
print('BR,H,Z,P,LemmaT(2) all hold; r-dist',dict(sorted(rc.items())),'max Gamma',Gmax,'min h',minh,'max j after chain 1',jmax_after1)
print('steps',{k:v for k,v in stats.items() if not k.startswith('pin')},'chain-1 representatives',{k:v for k,v in stats.items() if k.startswith('pin')})
print('examples',ex)
# SS check
ss=Counter()
for J,js in js_of.items():
    se_typ=T[J-1]['typ']
    if se_typ=='a' and T[J-1]['odd'] and len(js)>=3:
        n=js[1]-1
        if T[n]['odd'] and T[n]['typ'] in 'ab':
            J2=js[2]
            if J2>=3 and J2 in js_of:
                ss['ok' if js[2:]==js_of[J2] else 'BAD']+=1
            else: ss['J2<3 or out']+=1
print('SS (route a, 2nd return a/b): ',dict(ss),' time %.0fs'%(time.time()-t0))
