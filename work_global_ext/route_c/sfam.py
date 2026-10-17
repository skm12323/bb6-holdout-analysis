"""sfam.py -- exact 'virtual' walks (Height Principle) of real chains shifted in Theta.

virtual_walk(j, Th, u, SM): exact integer walk from a chain with parameter j, Theta=Th, lambda_u=u (odd),
using the real small crossing table SM (full pair data):  a: x=2(Th+3k)-2^n u ; b/c: u'=c_uW*u+l_uW;
Th' = Th+3+3tau(n).  Reports the j-word, types, non-descents, resonance (x==0).

Family F0[q]: the real level fire F0 (time s0, parameter p0) with Theta shifted by q:
  (p0, 3 s0+5+q, (3 s0+4)/2^p0).   q=-d is the bottom state of a depth-d pure b-ancestry
  p_d -> ... -> p_1 -> p0 (work_g2_obstruction section 4; exact mod 2^rho0).
"""
import sys,time,json
from collections import Counter
from fdata import small_full, lam_walk, v2

def virtual_walk(j,Th,u,SM,limit=200):
    word=[j]; types=''; nd=0; res=None
    for _ in range(limit):
        n=j-1
        R=SM[n]
        if not R['odd']: return dict(word=word,types=types,nd=nd,status='end')
        T=R['tau']
        if R['typ']=='a':
            x=2*(Th+3*(T//2))-(u<<n)
            if x==0: return dict(word=word,types=types+'a',nd=nd,status='RESONANCE')
            jn=v2(x); u=x>>jn
        else:
            cu,lu=R['uW']; jn=R['omega']; u=cu*u+lu
        types+=R['typ']; Th+=3+3*T
        if jn>=j: nd+=1
        word.append(jn); j=jn
    return dict(word=word,types=types,nd=nd,status='limit')

if __name__=='__main__':
    NSTEP=int(sys.argv[1]) if len(sys.argv)>1 else 200000
    D=int(sys.argv[2]) if len(sys.argv)>2 else 64
    SM=small_full(64)
    # real fires: type-a odd crossings
    LD=lam_walk(NSTEP)
    fires=[(n,LD['tau'][n]) for n in range(4,NSTEP) if LD['typ'][n]==97 and LD['odd'][n]]
    print('fires',len(fires))
    seen={}; stats=Counter(); lens=Counter(); nds=Counter(); longest=[]; reson=[]; check0=0
    for rho,s in fires:
        p=v2(3*s+4); u=(3*s+4)>>p
        if p<5: continue
        for q in range(-D,D+1):
            # the walk depends on (p, Th mod 2^64-ish, u mod ...) ; cache by exact data is cheap anyway
            W=virtual_walk(p,3*s+5+q,u,SM)
            stats[W['status']]+=1
            r=len(W['word'])-1; lens[(q<0,r)]+=1
            if W['nd']: nds[q]+=1
            if W['status']=='RESONANCE' and len(reson)<30: reson.append((rho,s,q,W['word']))
            if r>=5 and len(longest)<60: longest.append((s,q,W['word'],W['types']))
    print(dict(stats))
    print('length dist (q<0?, r):',dict(sorted(lens.items())))
    print('non-descents by q (first 40):',dict(sorted(nds.items())[:80]))
    print('resonances:',reson[:10])
    print('longest examples:',longest[:20])
    json.dump(dict(stats=dict(stats),lens={str(k):v for k,v in lens.items()},nds=dict(nds),reson=reson,longest=longest),
              open('sfam_%d_%d.json'%(NSTEP,D),'w'),indent=1)
