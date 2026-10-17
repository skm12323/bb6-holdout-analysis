"""exp6 (Class B): shape of the exact refinement tree after a first exact tie (synthetic late-stage states).
'spine only' = the tree is one infinite path (the 2-adic root of gamma*U+mu=0) with every side branch ending
tie-free (no further undetermined valuation).  Counts states whose side branches contain further exact ties,
max chains on side branches, and halting representatives below 2^Bmax."""
import sys, random, collections
import tielab as T
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 7)
NS=int(sys.argv[2]) if len(sys.argv)>2 else 400
Bmax=int(sys.argv[3]) if len(sys.argv)>3 else 30
L=T.Lab(400)
got=0; shape=collections.Counter(); maxch=0; halts=0; chdist=collections.Counter()
while got<NS:
    J,jt,u,D,d=T.late_state(random,Jr=(20,60),jr=(5,14),hs=(1,1,2))
    r=T.symstate(L,jt,u,D)
    if r['st']!='EXACT': continue
    got+=1
    tt=T.tietree(L,jt,u,D,Bmax=Bmax)
    extra=len(tt['leaves'])+len(tt['unres'])-Bmax
    shape['spine only' if extra==0 else 'extra splits']+=1
    for lf in tt['leaves']:
        maxch=max(maxch,lf[3]); chdist[lf[3]-len(r['ch'])]+=1
    halts+=len(tt['halts'])
print('exact-tie states:',NS,' tree shape:',dict(shape),' halting reps < 2^%d:'%Bmax,halts)
print('chains after the tie chain on side-branch leaves (distribution):',dict(sorted(chdist.items())),' max total chains',maxch)
