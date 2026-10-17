from fdata import small_full, lam_walk, v2
from sfam import virtual_walk
from sj import sym_beta
SM=small_full(400); LD=lam_walk(300000)
bad=0;n0=0
for n in range(4,300000):
    if LD['typ'][n]==97 and LD['odd'][n]:
        s=LD['tau'][n]; p=v2(3*s+4); u=(3*s+4)>>p
        W=virtual_walk(p,3*s+5,u,SM); R=sym_beta(p,LD,SM,400)
        n0+=1
        if W['word']!=R['js']: bad+=1
print('fires',n0,'q=0 virtual walk != S(p):',bad)
