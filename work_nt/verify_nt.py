r"""verify_nt.py -- checks for PROOF_NT.md.  Usage: python -B verify_nt.py [NB=1000000] [NJ=200000] [R=40] [NJ2=20000] [R2=300]
Imports ../work_el/verify_el.py READ-ONLY (real walk + exit automaton); writes nothing.
 N1 real-walk transition census (kind, th_prev -> th_next).
 N2 maximal tie-free window: for every 1<=j<NJ, th in [-R,R], run the automaton from (j,th);
    report the window around 1 free of ties, tie counts per th, and the (n,k) at which each tie occurs.
 N3 residue law of ties (j<NJ2, |th|<=R2): every tie start has th = 6 (mod 8) or th = 5 (mod 16).
 N4 the growth bound inputs: max |th~| over level-0 exits (fire states (J,1), J<10^6) and r.
"""
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','work_el'))
import verify_el as ve
from collections import Counter
a=sys.argv
NB=int(a[1]) if len(a)>1 else 10**6; NJ=int(a[2]) if len(a)>2 else 200000; R=int(a[3]) if len(a)>3 else 40
NJ2=int(a[4]) if len(a)>4 else 20000; R2=int(a[5]) if len(a)>5 else 300
Xt,Xtyp,Xpar,chain_at,st,s=ve.real_walk(NB)
run=ve.make_run(Xt,Xtyp,Xpar,chain_at)
# N1
C=Counter(); prev=None
for sp in sorted(chain_at):
    j,th,kd=chain_at[sp]
    if kd=='F': C[('F',th)]+=1
    else: C[(kd,prev,th)]+=1
    prev=th
print('N1 real-walk transitions (kind,th_prev,th_next):',sorted(C.items(),key=str))
# N2
bad=Counter(); where=Counter(); lo=-R-1; hi=R+1
for j in range(1,NJ):
    for th in range(-R,R+1):
        out,f=run(j,th)
        if f:
            bad[th]+=1; where[(f[1]-1,Xt[f[1]-1]//2)]+=1
            if th<=1: lo=max(lo,th)
            else: hi=min(hi,th)
print('N2 j<%d, |th|<=%d: maximal tie-free window around 1 = [%d,%d]'%(NJ,R,lo+1,hi-1))
print('   tie starts per th:',sorted(bad.items()))
print('   tie location (n,k_n) counts:',sorted(where.items()))
assert (lo,hi)==(-2,5)
# N3
viol=0; nt=Counter(); r7=Counter()
for j in range(1,NJ2):
    for th in range(-R2,R2+1):
        f=run(j,th)[1]
        if f:
            n=f[1]-1; nt[n]+=1
            if n==4 and not (th%8==6 or th%16==5): viol+=1
            if n==7: r7[min(abs(th),999)]+=0; r7['min|th|']=min(r7.get('min|th|',999),abs(th))
print('N3 j<%d,|th|<=%d: tie starts by tie level n: %s'%(NJ2,R2,sorted(nt.items())))
print('   n=4 ties violating (th=6 mod 8 or th=5 mod 16): %d;  n=7 ties: min |th| at start = %s'%(viol,r7.get('min|th|')))
assert viol==0 and set(nt)<={4,7}
# N4
M=0; rmax=0
for J in range(2,10**6):
    out,f=run(J,1); assert f is None
    rmax=max(rmax,len(out))
    for (j,th,kd) in out: M=max(M,abs(th))
print('N4 level 0 (J<10^6): max |th~| over exit chains = %d, max chains after fire = %d'%(M,rmax))
# N5 single-step tie table: tie at odd type-a n iff th~ = c_n (mod 2^n), c_n := 2^{n-1}-3k_n centred
best=[]
for n in range(4,10**6):
    if Xpar[n]==1 and Xtyp[n]=='a':
        m=1<<n; c=((1<<(n-1))-3*(Xt[n]//2))%m
        if c>m//2: c-=m
        best.append((abs(c),n,c))
best.sort()
print('N5 smallest |c_n| over odd type-a 4<=n<10^6:',best[:6])
m8=min(b for b in best if b[1]>=8)
print('   min over n>=8, n!=7: |c_n|=%d at n=%d'%(m8[0],m8[1]))
