# Q6 checker. Section 1 = the single Class-B computation; sections 2-4 are sanity checks of the
# Class-A lemmas in LEMMAS.md (not proofs); section 5 = Class-C evidence.
import sys, random, collections
sys.path.insert(0,'D:/math_cc/work_q4'); _argv=sys.argv; sys.argv=['x']
from verify_q4 import macro, Halt, inv          # frozen v2 map M (RULES.md Sec.3)
sys.argv=_argv
def rows(B,ph):
    """name of the v2 table row that M applies (mirrors RULES.md L1 decision tree)"""
    k,i=ph; m=len(B)
    if k=='A':
        n=B[i]
        if n>=2: return "R1'" if i==0 else 'R1'
        if n==0:
            if i>=1: return 'R2'
            return "R2'" if B[1]>=2 else ('X0' if m==2 else 'H1')
        if i+1==m-1: return "R3''"
        if B[i+2]>=2: return "R3'" if i==0 else 'R3'
        return 'R3k' if i+2==m-1 else 'H2'
    if i==m-1: return 'R5'
    if B[i+1]>=2: return 'R4'
    return 'R6' if i+1==m-1 else 'H3'
def in_SA(B,ph):
    k,i=ph; m=len(B)
    return (k=='A' and 0<=i<=m-4 and B[-2:]==[4,2] and all(b>=1 for b in B[:i])
            and all(b>=2 for b in B[i+2:m-2]) and B[i+1]>=1
            and (B[i]>=1 or (B[i]==0 and i>=1 and B[i+1]>=2 and (B[i-1]>=2 or i==1))))
def in_SD(B,ph):
    k,d=ph; m=len(B)
    return (k=='D' and m>=3 and 1<=d<=m-2 and B[-2:]==[4,2] and all(b>=1 for b in B)
            and all(b>=2 for b in B[d:m-2]))
def phi(b):
    """Sweep Lemma map on sweep-start prefix b=[b_0..b_s] (config (b+[1,4,2],A,s)).
    returns ('HALT',None,None) | (b', e0 or None, l)"""
    s=len(b)-1; e=b[s]+2; t=s-1; e0=None; es={}
    while True:
        e=(b[t] if t>=0 else 0)+e//2
        if t==0: e0=e
        if e%2:
            break
        if t<0 and e==2: return 'HALT',e0,t
        es[t]=e; t-=1
    l=t; off=max(0,1-l); pre=[0]*off+b
    new=pre[:l-1+off]+[pre[l-1+off]+(e-1)//2,(e+5)//2]+[es[u]//2 for u in range(l+1,s)]+[(b[s]+2)//2+4]
    return new,e0,l

if __name__=='__main__':
    print('== 1. [Class-B] exact initial segment c_0..c_20 of M ==')
    B,ph=[1,1],('A',0); seg=[]
    for s in range(21):
        r=rows(B,ph); seg.append((B,ph)); print(f'  c_{s:<2} {str(B):22s} {ph}  row {r}')
        assert r not in ('H1','H2',"H2'",'H3')
        if s<20: B,ph,_=macro(B,ph)
    assert in_SA(*seg[10]) and seg[10]==([5,1,4,2],('A',0))
    assert seg[20]==([3,10,1,4,2],('A',1))
    print('  c_0..c_20 not in H; c_10 in S_A; c_20 = sweep start [3,10] (b_s=10)')
    print('== 2. sanity of Lemma C (closure of S, exit only to H1) on random S-configs ==')
    random.seed(1); cnt=collections.Counter()
    for _ in range(200000):
        m=random.randint(4,9)
        if random.random()<0.6:
            i=random.randint(0,m-4); B=[random.randint(1,6) for _ in range(m-2)]+[4,2]
            for t in range(i+2,m-2): B[t]=random.randint(2,7)
            B[i]=random.randint(0,6); ph=('A',i)
        else:
            d=random.randint(1,m-2); B=[random.randint(1,6) for _ in range(m-2)]+[4,2]
            for t in range(d,m-2): B[t]=random.randint(2,7)
            ph=('D',d)
        if not(in_SA(B,ph) or in_SD(B,ph)): continue
        r=rows(B,ph); cnt[r]+=1; X=B
        if r=='H1': raise SystemExit('H1 directly from S?')
        if ph[0]=='D' and ph[1]==m-2:          # gadget G: 7 steps
            for _ in range(7): B,ph,_=macro(B,ph)
            assert (B,ph)==(X[:-3]+[X[-3]+4,1,4,2],('A',m-3)); continue
        B2,ph2,_=macro(B,ph)
        if (B2,ph2)[1]==('A',0) and B2[0]==0:
            assert r=='R2' and ph==('A',1) and X[0]==1 and rows(B2,ph2)=='H1'; cnt['->H1']+=1; continue
        assert in_SA(B2,ph2) or in_SD(B2,ph2),(X,ph,B2,ph2)
    print('  rows seen:',dict(cnt))
    print('== 3. sanity of Lemma E (edge cascade) ==')
    for u in range(1,3000):
        B,ph=[u,1,5,4,2],('A',0); h=False; us=[u]
        try:
            while ph[0]=='A':
                B,ph,_=macro(B,ph)
                if ph==('A',0): us.append(B[0])
        except Halt: h=True
        assert h==((u+2)&(u+1)==0), u
        assert all(us[k+1]==us[k]//2-1 for k in range(len(us)-1))
    print('  u=1..2999: halts iff u+2=2^k (k>=2); cascade u->u/2-1 confirmed')
    print('== 4. sanity of Sweep Lemma: phi vs M on the orbit and on random sweep starts ==')
    def run_to_next_start(b):
        B,ph=b+[1,4,2],('A',len(b)-1); first=True
        while True:
            try: B,ph,_=macro(B,ph)
            except Halt: return 'HALT'
            if ph[0]=='A' and B[-3:]==[1,4,2] and ph[1]==len(B)-4 and not first: return B[:-3]
            if ph[0]=='D': first=False
    b=[3,10]
    for k in range(3000):
        nb=run_to_next_start(b); assert phi(b)[0]==nb,(k,b); b=nb
    for _ in range(3000):
        b=[random.randint(1,40) for _ in range(random.randint(1,6))]+[10]
        nb=run_to_next_start(b); p=phi(b)[0]; assert p==nb,(b,p,nb)
    print('  3000 orbit sweeps + 3000 random prefixes: phi == M exactly (incl. HALT cases)')
    print('== 5. [Class-C] iterate phi from [3,10] ==')
    N=int(sys.argv[1]) if len(sys.argv)>1 else 3*10**6
    b=[3,10]; arr=[]; depth=collections.Counter()
    for k in range(N):
        s=len(b)-1; nb,e0,l=phi(b)
        if nb=='HALT': print('  HALT at sweep',k); break
        depth[min(s-1-l,12)]+=1
        if e0 is not None: arr.append((k,e0-2,len(b)))
        b=nb
    print('  sweeps',N,'final prefix length',len(b),'real arrivals (sweep, u0, s+1):')
    for a in arr: print('   ',a,' u0+2 =',a[1]+2,'power of 2:',(a[1]+2)&(a[1]+1)==0)
    tot=sum(depth.values()); print('  P(chain passes >=k positions):',[round(sum(v for d,v in depth.items() if d>=k)/tot,4) for k in range(8)])
