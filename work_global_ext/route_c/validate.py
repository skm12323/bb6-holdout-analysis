import sys,time
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'work_m'))
import verify_m as vm
from fdata import lam_walk, small_full
from sj import sym_beta
M=20000; NS=300
LD=lam_walk(M+2); SM=small_full(NS)
X=vm.Xdata(M+1,SMALL=M+1)
bad=0
for J in range(2,M+1):
    a=vm.sym_exit(J,X); b=sym_beta(J,LD,SM,NS)
    if isinstance(a[0],str) or tuple(b['js'])!=a[0] or b['types']+('' if True else '')!=a[1][:len(b['types'])] or b['G']!=a[3]:
        bad+=1
        if bad<5: print(J,a,b)
print('mismatches',bad)
# consistency of lam data with full data for n<NS
for n in range(NS):
    R=SM[n]
    assert R['typ']=='abc'[LD['typ'][n]-97] and R['tau']==LD['tau'][n] and R['eps']==LD['eps'][n] and R['odd']==LD['odd'][n], n
print('lam vs full ok')
