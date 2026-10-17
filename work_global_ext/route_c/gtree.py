"""gtree.py N0 Q [cap] -- 2-adic tree of the shifted-fire walk G(j,q)[lam] over the hidden odd lam.

G(j,q): a chain with parameter j, Theta = q + 2^j lam, lambda_u = lam (lam odd, hidden).
  q=1 is the fire state of S(j); by the Height Principle (REPORT section 3) a chain whose data agree with
  G(j,q)[lam*] to precision P follows this walk while j_i + Gamma_i < P.
  q = 1-d : bottom of a depth-d b-ancestry over a fire of parameter j (lam = that fire's odd base);
  q = 3-theta_b : chain after an a-step out of a large state with residue theta_b (lam = hidden m).
Exact affine bookkeeping in one 2-adic variable z (lam = 1+2z, refined by splitting).
Leaves: END (even return / j<=4), EXIT (parameter >= N0 forced: a climb), RES (x == 0 identically), CAP.
"""
import sys,json
from fractions import Fraction as Fr
from collections import Counter
from fdata import small_full

INF=10**9
def v2(x): return (x & -x).bit_length()-1 if x else INF

def explore(j0,q,SM,N0,cap=40,maxleaves=10**6,init=None):
    st=Counter(); meas=Counter(); maxd=0; longest=None; exits=[]; splits=0; ndesc=0
    if init is None: init=((1<<(j0+1),q+(1<<j0)),(2,1))
    stack=[(j0,init[0],init[1],0,1,(j0,))]   # (j, Theta=(a,b), u=(a,b)) affine in z (lam=1+2z), depth, level e, path
    leaves=0
    while stack:
        j,(aT,bT),(aU,bU),dep,e,path=stack.pop()
        if dep>=cap: st['CAP']+=1; meas['CAP']+=Fr(1,2**(e-1)); continue
        n=j-1
        R=SM[n]
        if n<4 or not R['odd']:
            st['END']+=1; meas['END']+=Fr(1,2**(e-1)); leaves+=1
            if dep>maxd: maxd=dep; longest=path
            continue
        T=R['tau']
        if R['typ']=='a':
            k=T//2
            A=2*aT-(aU<<n); B=2*bT+6*k-(bU<<n)
            if A==0 and B==0:
                st['RES']+=1; meas['RES']+=Fr(1,2**(e-1)); continue
            vA=v2(A); vB=v2(B)
            if vB<vA:
                jn=vB
                if jn>=N0:
                    st['EXIT']+=1; meas['EXIT']+=Fr(1,2**(e-1))
                    if len(exits)<20: exits.append(path+(jn,))
                    continue
                if jn>=j: ndesc+=1
                stack.append((jn,(aT,bT+3+6*k),(A>>jn,B>>jn),dep+1,e,path+(jn,)))
            else:
                if vA>=N0 and vB>=N0:
                    st['EXIT']+=1; meas['EXIT']+=Fr(1,2**(e-1))
                    if len(exits)<20: exits.append(path+('>=%d'%N0,))
                    continue
                splits+=1
                for bit in (0,1):
                    stack.append((j,(2*aT,bT+aT*bit),(2*aU,bU+aU*bit),dep,e+1,path))
        else:
            cu,lu=R['uW']; jn=R['omega']
            stack.append((jn,(aT,bT+3+3*T),(cu*aU,cu*bU+lu),dep+1,e,path+(jn,)))
        if leaves>maxleaves: st['ABORT']+=1; break
    return dict(st=dict(st),meas={k:float(v) for k,v in meas.items()},maxd=maxd,longest=longest,
                exits=exits,splits=splits,ndesc=ndesc)

if __name__=='__main__':
    N0=int(sys.argv[1]); Q=int(sys.argv[2]); cap=int(sys.argv[3]) if len(sys.argv)>3 else 40
    SM=small_full(N0+2)
    agg=Counter(); worst=[]; lamdep=[]; exitcases=[]; rescases=[]; maxd=0; ndc=0
    for q in range(-Q,Q+1):
        for j in range(5,N0):
            r=explore(j,q,SM,N0,cap)
            for k,v in r['st'].items(): agg[k]+=v
            if r['splits']: lamdep.append((j,q,r['splits'],r['maxd']))
            if r['st'].get('EXIT'): exitcases.append((j,q,r['meas'].get('EXIT'),r['exits'][:2]))
            if r['st'].get('RES'): rescases.append((j,q))
            if r['maxd']>maxd: maxd=r['maxd']; worst=(j,q,r['longest'])
            ndc+=r['ndesc']
    print('N0',N0,'Q',Q,'leaf totals',dict(agg),'max depth',maxd,'example',worst)
    print('lambda-dependent (j,q):',len(lamdep),'of',(2*Q+1)*(N0-5),' non-descent steps:',ndc)
    print('EXIT cases (j,q,measure,paths):',len(exitcases),exitcases[:12])
    print('RESONANCE cases:',len(rescases),rescases[:20])
    json.dump(dict(N0=N0,Q=Q,agg=dict(agg),maxd=maxd,worst=worst,lamdep=lamdep,exitcases=exitcases,rescases=rescases),
              open('gtree_%d_%d.json'%(N0,Q),'w'),indent=1,default=str)
