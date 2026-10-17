"""exp1: classification of S*_e(J) and real-vs-symbolic comparison on synthetic defects e.
Checks (Class B):
 (i)  before the first EXACT tie, for every odd U the real recursion equals S*_e(J) evaluated at U
      (same types, X_t = alpha_t U + beta_t, j_t), through OVER-ties;
 (ii) S*_e(J) without exact tie: real run never halts for any tested U, ends at the predicted even return;
 (iii) at the first exact tie (alpha,beta): the real chain t* halts iff alpha U + beta is a power of 2.
"""
import sys, collections
import tielab as T
L=T.Lab(400)
JMAX=int(sys.argv[1]) if len(sys.argv)>1 else 40
EMAX=int(sys.argv[2]) if len(sys.argv)>2 else 400
Us=list(range(1,400,2))+[2**61-1,3*(2**40)+1,10**30+1]
cls=collections.Counter(); over_cases=[]; exact_cases=[]
nreal=0; viol=0; halt_pre=0; halts=collections.Counter()
for J in range(3,JMAX+1):
    for e in range(1,EMAX+1):
        r=L.symstar(J,e); kinds=[c['kind'] for c in r['ch']]
        key=r['st']+('+over' if 'over' in kinds else '')
        cls[key]+=1
        if 'over' in kinds and r['st']=='END': over_cases.append((J,e))
        if r['st']=='EXACT': exact_cases.append((J,e))
        # real comparison
        for U in Us:
            if (U<<(J-1))-e<1: continue
            rr=L.realrec(U,J,e); nreal+=1
            sym=r['ch']; real=rr['ch']
            # compare chains before the exact tie
            npre=len(sym)-(1 if r['st']=='EXACT' else 0)
            for k in range(npre):
                s=sym[k]; 
                if k>=len(real) or real[k][0]!=s['typ'] or real[k][1]!=s['x'][0]*U+s['x'][1] or real[k][2]!=s['j']:
                    viol+=1; break
            if r['st']=='END':
                if rr['st']!='END' or len(real)!=len(sym): viol+=1
            if r['st']=='EXACT':
                s=sym[-1]; Xp=s['x'][0]*U+s['x'][1]
                pred_halt = Xp>0 and Xp&(Xp-1)==0
                if len(real)<npre+1: viol+=1; continue
                act_halt = rr['st']=='HALT' and len(real)==npre+1
                if pred_halt!=act_halt: viol+=1
                if act_halt: halts['at t*']+=1
                elif rr['st']=='HALT': halts['after t*']+=1
            else:
                if rr['st']=='HALT': halt_pre+=1
print('classes of S*_e(J), 3<=J<=%d, 1<=e<=%d:'%(JMAX,EMAX),dict(cls))
print('real runs compared:',nreal,' violations:',viol,' halts without exact tie:',halt_pre,' halts with exact tie:',dict(halts))
print('first over-tie-only cases:',over_cases[:12])
print('first exact cases:',exact_cases[:12])
