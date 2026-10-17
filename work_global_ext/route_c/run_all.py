"""run_all.py N : S(J) for every 2<=J<=N via the exact beta walk; statistics -> stats_N.json"""
import sys,time,json
from collections import Counter,defaultdict
from fdata import lam_walk, small_full
from sj import sym_beta
N=int(sys.argv[1]); NS=400
t0=time.time(); LD=lam_walk(N+2); SM=small_full(NS); print('data %.0fs'%(time.time()-t0),flush=True)
rc=Counter(); thc=Counter(); tha=Counter(); nondesc=[]; ties=[]; maxG=0; maxj2=0
words=Counter(); tailmap=defaultdict(set); longest=[]; minh=10**9; minhJ=None
route=Counter(); maxjt=Counter()
for J in range(2,N+1):
    R=sym_beta(J,LD,SM,NS)
    if R['status']=='TIE': ties.append(J); continue
    js=R['js']; r=len(js)-1; rc[r]+=1
    tys=R['types']
    if r>=1: route[tys[0]]+=1
    for t in range(1,r+1):
        thc[R['theta'][t]]+=1
        if t<len(tys) and tys[t]=='a': tha[R['theta'][t]]+=1
        if t>=1 and js[t]>=js[t-1]: nondesc.append((J,t,js))
        if J>=64: 
            if R['h'][t]<minh: minh=R['h'][t]; minhJ=J
    maxG=max(maxG,R['G'])
    if r>=2: maxj2=max(maxj2,max(js[2:]))
    if r>=1:
        key=(tys[0],js[1],R['theta'][1])
        tailmap[key].add((tuple(js[1:]),tys[1:]))
    words[tys]+=1
    if r>=3: longest.append((J,js,tys))
print('time %.0fs'%(time.time()-t0))
func=all(len(v)==1 for v in tailmap.values())
out=dict(N=N,r_dist=dict(sorted(rc.items())),ties=ties[:20],nties=len(ties),nondescents=len(nondesc),nondesc_ex=nondesc[:10],
 theta_all=dict(sorted(thc.items())),theta_before_a=dict(sorted(tha.items())),maxGamma=maxG,max_j_after_chain1=maxj2,
 route1=dict(route),min_h_J_ge_64=[minh,minhJ],tail_function_of_route_j1_theta1=func,
 n_tail_keys=len(tailmap),words=dict(words.most_common(40)),r_ge3=longest[:60],n_r_ge3=len(longest))
json.dump(out,open('stats_%d.json'%N,'w'),indent=1)
print(json.dumps({k:v for k,v in out.items() if k not in('words','r_ge3')},indent=0))
print('r>=3:',len(longest),longest[:10])
