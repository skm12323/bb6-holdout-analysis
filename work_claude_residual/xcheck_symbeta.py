import sys,time
sys.path.insert(0,r'D:\math_cc\work_claude_residual'); sys.path.insert(0,r'D:\math_cc\work_global_ext\route_c')
import rwalk as R
from fdata import lam_walk, small_full
from sj import sym_beta
T=R.Table()
N=10**6; LD=lam_walk(N+2); SM=small_full(400)
bad=0
for Q in range(5,N):
    S=sym_beta(Q,LD,SM,400)
    c=R.certify(T,Q,1)
    if S['status']=='TIE': print('tie',Q); continue
    if S['js']!=c['word'] or not c['ok']:
        bad+=1
        if bad<5: print(Q,S['js'],c['word'],c['ok'],c['status'])
    # classes at a-outputs: compare theta (mod 2^j) of sym_beta
    ao=[a for a in c['aouts']]
    tys=S['types']; js=S['js']; th=S['theta']
    k=0
    for t in range(1,len(js)):
        if tys[t-1]=='a':
            cj,res=ao[k]; k+=1
            assert cj==js[t] and (res-th[t])%(1<<cj)==0,(Q,t,ao,th)
print('bad',bad)
