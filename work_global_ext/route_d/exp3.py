"""exp3: synthetic LATE-STAGE states of a symbolic exit (margin m = J-Gamma small), the only regime in
which ties of S(J) are possible (Lemma T).  State after a tie-free chain with parameter jt:
  x=(alpha_x,beta_x), alpha_x=2^m*gamma in [2^J,2^(J+1)), v2(beta_x)=jt<m, beta_x<=12J^2,
  u=x/2^jt, D=(2^J-alpha_x/2, beta_D), beta_D in [0,12J^2]   (mass sum alpha = 2^J).
For each sampled state:
  A. symbolic S* from the state (over-ties continued, stop at first exact tie);
  B. real recursion for many odd U, compared with S* (through over-ties) -- must agree, no halt;
  C. brute-force integer top map on the actual list for a subset of U (validates realstate);
  D. for exact ties: the full refinement tree (Bmax) vs brute-force halting set for odd U<2^Bc.
"""
import sys, random, collections
import tielab as T
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
NS=int(sys.argv[2]) if len(sys.argv)>2 else 3000
L=T.Lab(400)
st=collections.Counter(); viol=0; nreal=0; nbrute=0; badbrute=0
exact_states=[]; over_states=[]
Us=list(range(1,600,2))+[2**61-1,3*2**50+1]
for it in range(NS):
    J,jt,u,D,d=T.late_state(random,Jr=(24,48),jr=(5,14),hs=(1,1,2,3))
    r=T.symstate(L,jt,u,D)
    kinds=[c['kind'] for c in r['ch']]
    key=(r['st'],'over' in kinds); st[key]+=1
    if r['st']=='EXACT': exact_states.append((J,jt,u,D,r))
    elif 'over' in kinds: over_states.append((J,jt,u,D,r))
    else:
        if random.random()>0.002: continue
    # B: real vs symbolic
    npre=len(r['ch'])-(1 if r['st']=='EXACT' else 0)
    for U in Us:
        rr=T.realstate(L,U,jt,u,D); nreal+=1
        for k in range(npre):
            s=r['ch'][k]
            if k>=len(rr['ch']) or rr['ch'][k]!=(s['typ'],s['x'][0]*U+s['x'][1],s['j']): viol+=1; break
        if r['st']=='END' and (rr['st']!='END' or len(rr['ch'])!=npre): viol+=1
        if r['st']!='EXACT' and rr['st']=='HALT': viol+=1
        if r['st']=='EXACT':
            s=r['ch'][-1]; Xp=s['x'][0]*U+s['x'][1]; ph=(Xp&(Xp-1)==0)
            ah=(rr['st']=='HALT' and len(rr['ch'])==npre+1)
            if ph!=ah: viol+=1
    # C: brute force top map on the list for small U
    for U in range(1,40,2):
        Lst=T.statelist(U,jt,u,D)
        if min(Lst)<0: continue
        a=T.realstate(L,U,jt,u,D); b=T.toprun(Lst); nbrute+=1
        if a['st']!=b['st'] or (a['st']=='END' and a['final']!=b['final']): badbrute+=1
print('state classes (status, had over-tie):',dict(st))
print('real-vs-S* comparisons:',nreal,'violations:',viol,'| brute-force top-map checks:',nbrute,'mismatches:',badbrute)
# D: refinement trees of the exact-tie states
Bc=13; Bmax=22
tot=collections.Counter(); hal=[]; mism=0; deep=collections.Counter(); maxch=0; nsplit=collections.Counter()
for (J,jt,u,D,r) in exact_states[:150]:
    tt=T.tietree(L,jt,u,D,Bmax=Bmax)
    hs=sorted(h[0] for h in tt['halts'])
    unres=tt['unres']
    brute=[U for U in range(1,1<<Bc,2) if T.realstate(L,U,jt,u,D)['st']=='HALT']
    pred=set(h for h in hs if h<(1<<Bc))
    # every brute halt must be a tree halt (all classes of depth<=Bmax resolved for U<2^Bc unless unresolved)
    ok=set(brute)==pred or all((U in pred) or any(U%(1<<B)==rr%(1<<B) for rr,B,_,_ in unres) for U in brute)
    if not ok: mism+=1
    tot['states']+=1; tot['leaves']+=len(tt['leaves']); tot['unres']+=len(unres)
    for lf in tt['leaves']:
        deep[lf[1]]+=1; maxch=max(maxch,lf[3]); tot[lf[2]]+=1
    hal.append((len(hs),sum(1 for h in hs if h%3==0)))
    nsplit[len(tt['leaves'])+len(unres)]+=0
print('exact-tie states analysed:',tot['states'],' tree leaves:',tot['leaves'],' unresolved classes (B=%d):'%Bmax,tot['unres'],
      ' leaf status:',{k:tot[k] for k in ('END','LONG','NODATA')},' max chains on a leaf:',maxch)
print('brute-force halting set (odd U<2^%d) == tree prediction: mismatches'%Bc,mism)
print('halting reps per state (all odd U / U=3w) found below 2^%d:'%Bmax, collections.Counter(hal).most_common(12))
print('leaf depth B distribution:',sorted(deep.items())[:30])
