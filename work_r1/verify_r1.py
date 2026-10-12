"""R1 verifier for BB(6) holdout 1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE.
Symbolic run-length prover for the macro rules in RULES.md + raw-vs-abstract cross-check.
Units: TM steps. Run: python verify_r1.py"""
import sys
from fractions import Fraction
TM="1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE"
def parse(s):
    T={}
    for i,g in enumerate(s.split('_')):
        for r in (0,1):
            c=g[3*r:3*r+3]
            if c[0]!='-': T[('ABCDEF'[i],r)]=(int(c[0]),c[1],c[2])
    return T
T=parse(TM)

# ---------- linear expressions: dict var->int, plus key 1 for const ----------
def E(c=0,**v):
    d={1:c}; d.update(v); return norm(d)
def norm(d): return {k:x for k,x in d.items() if x!=0 or k==1} if True else d
def add(a,b):
    d=dict(a)
    for k,x in b.items(): d[k]=d.get(k,0)+x
    d.setdefault(1,0); return {k:x for k,x in d.items() if x!=0 or k==1}
def sub1(a): return add(a,{1:-1})
def iszero(a): return all(x==0 for x in a.values())
def const(a): return a.get(1,0)
def nonneg_vars(a): return all(x>=0 for k,x in a.items() if k!=1)
def show(a):
    s=[];c=a.get(1,0)
    for k in sorted(k for k in a if k!=1):
        x=a[k]; s.append(('' if x==1 else str(x))+k)
    if c or not s: s.append(str(c))
    return '+'.join(s).replace('+-','-')
INF='inf'
# side stack: list of [sym,expr] nearest first, terminated by (0,INF)
def push(st,sym,e):
    if iszero(e): return
    if st and st[0][1]=='REST': st.insert(0,(sym,e))
    elif st and st[0][0]==sym and st[0][1]!=INF: st[0]=(sym,add(st[0][1],e))
    elif st and st[0][0]==sym and st[0][1]==INF: pass
    else: st.insert(0,(sym,e))
def pop(st):
    sym,e=st[0]
    if e==INF: return 0
    if e=='REST': raise Exception('rule touched opaque REST')
    if const(e)<1: raise Exception('case split needed: block %s^%s'%(sym,show(e)))
    st.pop(0); push(st,sym,sub1(e)); return sym
class Halt(Exception): pass
def run(L,state,face,R,stop,maxit=10000):
    """face '>' : head reads R[0]; '<': head reads L[0]. stop(cfg)->bool tested after >=1 step."""
    steps=E(0); it=0
    while True:
        it+=1
        if it>maxit: raise Exception('no stop')
        near = R if face=='>' else L
        # acceleration over 1-blocks
        if near[0][0]==1 and near[0][1] not in (INF,'REST') and (state,1) in T:
            w,d,n=T[(state,1)]
            if w==1 and n==state and ((d=='R')==(face=='>')):
                e=near.pop(0)[1]; other = L if face=='>' else R
                push(other,1,e); steps=add(steps,e)
                if stop(L,state,face,R): return L,state,face,R,steps
                continue
        c=pop(near)
        if (state,c) not in T: raise Halt()
        w,d,n=T[(state,c)]
        if d=='R': push(L,w,E(1)); face='>'
        else: push(R,w,E(1)); face='<'
        state=n; steps=add(steps,E(1))
        if stop(L,state,face,R): return L,state,face,R,steps

def cfg(h,runs,rest=False):
    """config (h; r1..rk): tape 0^inf 1^h [0] 1^r1 0 1^r2 ... 0 1^rk 0^inf, state A reading the bracketed 0.
    Represented as L=[0-cell,1^h,0inf] , '<A' reading L[0]."""
    L=[(0,INF)]; push(L,1,h); push(L,0,E(1))
    R=[(0,INF)] if not rest else [('*','REST')]
    if rest: push(R,0,E(1))
    for i,r in reversed(list(enumerate(runs))):
        push(R,1,r)
        if i>0: push(R,0,E(1))
    return L,'A','<',R
def is_A0(L,s,f,R): return s=='A' and ((f=='<' and L[0][0]==0) or (f=='>' and R[0][0]==0))
def same(st1,st2):
    a=[(s,e if e in (INF,'REST') else tuple(sorted((str(k),v) for k,v in e.items() if v!=0))) for s,e in st1]
    b=[(s,e if e in (INF,'REST') else tuple(sorted((str(k),v) for k,v in e.items() if v!=0))) for s,e in st2]
    return a==b
def prove(name,h,runs,h2,runs2,steps_expected,rest=False):
    L,s,f,R=cfg(h,runs,rest)
    L,s,f,R,st=run(L,s,f,R,is_A0)
    L2,s2,f2,R2=cfg(h2,runs2,rest)
    ok = s==s2 and f==f2 and same(L,L2) and same(R,R2) and same([(1,st)],[(1,steps_expected)])
    print(('PROVED ' if ok else 'FAILED ')+name+'  steps='+show(st))
    if not ok:
        print('  got L',L,'R',R); sys.exit(1)

# parameters: h,x,y,z >= 0 ; rest of tape right of the rule's window is arbitrary:
# we model "rest" by a symbolic run 1^z followed by blank; since no rule reads past the
# first 0 after its window (checked: the window's right delimiter 0 is reached only in
# state D/E which never cross it except E reading it -> covered), this is enough; see RULES.md L0.
h=E(0,h=1); x=E(0,x=1); y=E(0,y=1); z=E(0,z=1)
def P(*a): return add(*a) if len(a)==2 else a[0]
def lin(**kw):
    c=kw.pop('c',0); return E(c,**kw)
# R1: (h; a, b, REST) -> (h+1; a, b-1, REST), a>=0, b>=1, with REST = (r3..): window test with REST = [z+1]
# We prove it for REST nonempty (z+1) and REST empty separately.
print('--- symbolic macro rules (all parameters h,x,y >= 0; REST = opaque, never read) ---')
X1=lin(x=1,c=1); X2=lin(x=1,c=2); Y1=lin(y=1,c=1); Y2=lin(y=1,c=2); H1=lin(h=1,c=1)
for rest in (True,False):
    tag=' | REST' if rest else ' | blank'
    prove('R1  (h; x+1, y+1) -> (h+1; x+1, y)'+tag, h,[X1,Y1], H1,[X1,y], lin(x=2,c=5), rest)
    if not rest: prove('R2  (h; x+2) -> (h+1; x, 0, 1)'+tag, h,[X2], H1,[x,E(0),E(1)], lin(x=2,c=7), rest)
    prove('R3  (h; x+2, 0, y+1) -> (h+1; x, 0, y+2)'+tag, h,[X2,E(0),Y1], H1,[x,E(0),Y2], lin(x=2,c=7), rest)
    prove('R4  (h+1; 1, 0, y+1) -> (0; h, 0, 1, y+2)'+tag, H1,[E(1),E(0),Y1], E(0),[h,E(0),E(1),Y2], lin(h=1,c=8), rest)
    prove('R5  (h; 0, 0, y+1) -> (0; h+y+4)'+tag, h,[E(0),E(0),Y1], E(0),[lin(h=1,y=1,c=4)], lin(h=1,c=5), rest)

# ---------- coverage of the halting case and the excluded shapes (symbolic) ----------
print('--- symbolic: shapes outside the rule set ---')
for rest in (False,True):
    L,s,f,R=cfg(E(0),[E(1),E(0),lin(y=1,c=1)],rest)
    try: run(L,s,f,R,is_A0); print('FAILED: (0;1,0,y+1) did not halt'); sys.exit(1)
    except Halt: print('PROVED HALT (0; 1, 0, y+1, ...) halts', '| REST' if rest else '| blank')

# ---------- rule-level abstract machine ----------
def rule_step(h,r):
    """one macro rule on config (h; r) ; returns (h',r',steps) or 'HALT'"""
    a=r[0]
    if len(r)==1:
        assert a>=2; return h+1,[a-2,0,1],2*a+3                      # R2
    if r[1]>=1:
        assert a>=2; r2=[a,r[1]-1]+r[2:]
        if r2[-1]==0: r2=r2[:-1]
        return h+1,r2,2*a+3                                            # R1
    # r[1]==0
    if a>=2: return h+1,[a-2,0,r[2]+1]+r[3:],2*a+3                      # R3
    if a==1:
        if h==0: return 'HALT'
        return 0,[h-1,0,1,r[2]+1]+r[3:],h+7                            # R4
    return 0,[h+r[2]+3]+r[3:],h+5                                       # R5 (a==0)

def tm_events(maxsteps):
    """raw TM; yields (t, h, runs) at every A-reading-0 event."""
    tape=bytearray(1<<16); off=1<<15; p=off; s=0
    # encode
    tr={}
    for (st,rd),(w,d,n) in T.items(): tr[('ABCDEF'.index(st),rd)]=(w,1 if d=='R' else -1,'ABCDEF'.index(n))
    t=0
    while t<maxsteps:
        rd=tape[p]
        if s==0 and rd==0:
            # decode config
            lo=p
            while tape[lo-1]==1: lo-=1
            hi=len(tape)-1
            while tape[hi]==0 and hi>p: hi-=1
            seg=bytes(tape[p+1:hi+1]).decode('latin1').replace('\x01','1').replace('\x00','0')
            runs=[len(x) for x in seg.split('0')] if seg else []
            yield t,p-lo,runs
        if (s,rd) not in tr: yield t,'HALT',None; return
        w,d,n=tr[(s,rd)]; tape[p]=w; p+=d; s=n; t+=1
        if p<16 or p>len(tape)-16: raise Exception('grow tape')

print('--- raw TM vs rule-level abstract (every A0 event) ---')
N=int(sys.argv[1]) if len(sys.argv)>1 else 3_000_000
h,r,t=0,[],0
ev=tm_events(N); next(ev)            # (0;) blank tape at t=0
# base lemma [Class-B]: blank tape reaches (0; 3) at t=5
t0,h0,r0=next(ev); assert (t0,h0,r0)==(5,0,[3]),(t0,h0,r0)
h,r,t=0,[3],5; cnt=0
for t1,h1,r1 in ev:
    res=rule_step(h,r); h,r,dt=res; t+=dt; cnt+=1
    assert (t,h,r)==(t1,h1,r1),((t,h,r),(t1,h1,r1))
print('MATCH: %d macro steps, all configs and step counts equal up to t=%d'%(cnt,t))

# ---------- top-level map (RULES.md section 5) ----------
def G(h,a,c,S):
    """config (h; a, 0, c, S) [c=0 & S=[] means (h; a) before R2]. returns (newlist, steps) or ('HALT',steps)"""
    st=0
    while True:
        q=a//2; st+=q*(2*a+3)-2*q*(q-1); h+=q
        if a%2==0:
            return [h+c+q+3]+S, st+h+5     # R5: (h;0,0,y+1) with y+1=c+q
        if h==0: return 'HALT',st
        st+=h+7; S=[c+q+1]+S; a=h-1; h=0; c=1                 # R4
def top(L):
    A=L[0]; b=L[1] if len(L)>1 else 0; c=L[2] if len(L)>2 else 0; S=L[3:]
    return G(b,A,c,S)[0], b*(2*A+3)+G(b,A,c,S)[1]
def top_fast(L):
    """same map, closed form via X=A+2b+3 (no step count)"""
    A=L[0]; b=L[1] if len(L)>1 else 0; c=L[2] if len(L)>2 else 0; S=L[3:]
    if A%2==0: return [A+b+c+3]+S
    m=b+(A-3)//2; S=[c+(A+1)//2]+S
    if (m+3)&(m+2)==0: return 'HALT'      # m+3 power of two
    while m%2: S=[(m+3)//2]+S; m=(m-3)//2
    return [m+4]+S

print('--- top-level map vs rule-level abstract ---')
h,r,t=0,[3],5; L=[3]; T_top=5
for n in range(3000):
    L2,dt=top(L); assert top_fast(L)==L2
    T_top+=dt
    while True:
        h,r,d=rule_step(h,r); t+=d
        if h==0 and (len(r)==1 or r[1]!=0): break
    assert (r,t)==(L2,T_top),(n,r,L2,t,T_top)
    L=L2
print('MATCH: 3000 top steps, lists and TM step counts equal (t=%d)'%t)
M=int(sys.argv[2]) if len(sys.argv)>2 else 10_000_000
L=[3]; T_top=5
for n in range(M):
    assert sum(L)==3*n+3
    L2,dt=top(L) if n<200000 else (top_fast(L),0)
    if L2=='HALT': print('HALT at top step',n); sys.exit()
    T_top+=dt; L=L2
    if n==199999: T200=T_top
print('no halt in %d top steps (sum invariant sum(L_n)=3n+3 held); exact TM time after first 200000 top steps = %d'%(M,T200))
