# Symbolic run-length prover. Lengths are linear forms: dict {var:coef, 1:const}; vars >= 0.
import re
TM='1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---'
def parse(s):
    T={}
    for i,g in enumerate(s.split('_')):
        for r in (0,1):
            t=g[3*r:3*r+3]
            T[(chr(65+i),r)]=None if t[2]=='-' else (int(t[0]),'R' if t[1]=='R' else 'L',t[2])
    return T
INF='inf'
def L(s):
    # parse "a+2" / "3" / "inf"
    if s==INF: return INF
    d={}
    for term in s.replace('-','+-').split('+'):
        if not term: continue
        if re.fullmatch(r'-?\d+',term): d[1]=d.get(1,0)+int(term)
        else:
            c=1
            if term.startswith('-'): c=-1;term=term[1:]
            d[term]=d.get(term,0)+c
    return {k:v for k,v in d.items() if v}
def add(a,b):
    if a==INF or b==INF: return INF
    d=dict(a)
    for k,v in b.items(): d[k]=d.get(k,0)+v
    return {k:v for k,v in d.items() if v}
def ge1(a):
    if a==INF: return True
    return a.get(1,0)>=1 and all(v>0 for k,v in a.items() if k!=1)
def iszero(a): return a!=INF and not a
def nonneg(a): return a==INF or (a.get(1,0)>=0 and all(v>0 for k,v in a.items() if k!=1))
def parse_cfg(s):
    # tokens: "1^a+2", "0", "0^inf", "S>" (head facing right, reads next), "<S"
    toks=s.split(); left=[];right=[];head=None
    for t in toks:
        if t.endswith('>') or t.startswith('<'):
            head=(t.strip('<>'), 'R' if t.endswith('>') else 'L'); continue
        if '^' in t: sym,ln=t.split('^',1)
        else: sym,ln=t,'1'
        (right if head else left).append([int(sym),L(ln)])
    return norm(left),head,norm(right)
def norm(runs):
    out=[]
    for sym,ln in runs:
        if iszero(ln): continue
        assert nonneg(ln),ln
        if out and out[-1][0]==sym: out[-1][1]=add(out[-1][1],ln)
        else: out.append([sym,ln])
    return out
def push(lst,sym,end):  # end: 'back' of list
    if end=='back': lst.append([sym,{1:1}])
    else: lst.insert(0,[sym,{1:1}])
def fmt(lf):
    if lf==INF: return 'inf'
    return '+'.join(([str(k) if v==1 else f'{v}{k}' for k,v in lf.items() if k!=1])+([str(lf[1])] if 1 in lf else [])) or '0'
def show(c):
    l,h,r=c
    f=lambda rs:' '.join(f'{s}^{fmt(n)}' for s,n in rs)
    return f(l)+' '+(h[0]+'>' if h[1]=='R' else '<'+h[0])+' '+f(r)
T=parse(TM)
def step(cfg):
    """one macro step: returns new cfg, or ('HALT'), raises if needs case split / out of segment"""
    l,(S,D),r=cfg
    l=[x[:] for x in l]; r=[x[:] for x in r]
    src = r if D=='R' else l
    if not src: raise Exception('OUT')
    run = src[0] if D=='R' else src[-1]
    c,n=run
    tr=T[(S,c)]
    if tr is None: return 'HALT'
    w,d,ns=tr
    if d==D and ns==S:   # sweep whole run (rewriting c->w)
        if n==INF: raise Exception('INFSWEEP')
        if D=='R': r.pop(0); l.append([w,n])
        else: l.pop(); r.insert(0,[w,n])
        return (norm(l),(S,D),norm(r)),n
    if not ge1(n): raise Exception('SPLIT needed on '+fmt(n)+' in '+show(cfg))
    if n!=INF: run[1]=add(n,{1:-1})
    if D=='R': r=r if n==INF else r
    # remove one cell from src
    if D=='R':
        if n!=INF and iszero(run[1]): r.pop(0)
    else:
        if n!=INF and iszero(run[1]): l.pop()
    # place written cell: cell is between l and r; head moves d
    if d=='R': l.append([w,{1:1}])
    else: r.insert(0,[w,{1:1}])
    return (norm(l),(ns,d),norm(r)),{1:1}
# ---------------- Q4 additions. Prover core above is copied from work_q1 and is independently
# ---------------- re-checked below by concrete raw-TM simulation of every rule instance (params 0..7).
def prove(lhs,rhs,maxsteps=100000):
    """Symbolic: run LHS until it equals RHS. Raises on OUT (left window) / SPLIT (case split needed)."""
    c=parse_cfg(lhs); tgt=parse_cfg(rhs); steps={}
    for i in range(maxsteps):
        if i>0 and show(c)==show(tgt): return True,fmt(steps)
        res=step(c)
        if res=='HALT': return 'HALT',fmt(steps)
        c,k=res; steps=add(steps,k)
    return False,show(c)
def prove_halt(lhs,maxsteps=1000):
    c=parse_cfg(lhs); steps={}
    for i in range(maxsteps):
        res=step(c)
        if res=='HALT': return True,fmt(steps)   # = number of executed TM steps before reaching (F,1)
        c,k=res; steps=add(steps,k)
    return False,show(c)

RULES=[ # name, LHS, RHS, TM steps
 ("R1",  "0 1^p 0 <A 0 1^n+2 0 0 1^j",          "0 1^p+1 0 <A 0 1^n 0 0 1^j+1",          "2n+17"),
 ("R1'", "0^inf 0 <A 0 1^n+2 0 0 1^j",          "0^inf 1 0 <A 0 1^n 0 0 1^j+1",          "2n+17"),
 ("R2",  "0 1^p+1 0 <A 0 0 0",                  "0 <A 0 1^p 0 0 1 0",                    "p+10"),
 ("R2'", "0^inf 0 <A 0 0 0 1^j+2",              "0^inf 1^3 0 1 D> 1^j+1",                "13"),
 ("R3",  "0 1^p 0 <A 0 1 0 0 1^j 0 1^k+2",      "0 1^p+1 0 1^j+3 0 1 D> 1^k+1",          "j+7"),
 ("R3'", "0^inf 0 <A 0 1 0 0 1^j 0 1^k+2",      "0^inf 1 0 1^j+3 0 1 D> 1^k+1",          "j+7"),
 ("R3''","0 1^p 0 <A 0 1 0 0 1^j 0^inf",        "0 1^p+1 0 <A 0 1^j+1 0 0 1 0^inf",      "2j+15"),
 ("R3k", "0 1^p 0 <A 0 1 0 0 1^j 0 1 0^inf",    "0 1^p+3 0 <A 0 1^j 0 0 1^3 0 1^2 0^inf","6j+105"),
 ("R4",  "0 1 D> 1^a+1 0 1^b+2",                "0 1^a+2 0 1 D> 1^b+1",                  "a+7"),
 ("R5",  "0 1^q 0 1 D> 1^a+1 0^inf",            "0 1^q 0 <A 0 1^a 0 0 1 0^inf",          "2a+14"),
 ("R6",  "0 1 D> 1^a+1 0 1 0^inf",              "0 1^a+4 0 <A 0 0 0 1^2 0^inf",          "a+53"),
]
HALTS=[ # name, LHS, executed TM steps until state F reads 1
 ("H1  A,i=0,B0=0,B1=1,m>=3",       "0^inf 0 <A 0 0 0 1 0 1^c+1",          "14"),
 ("H2  A,B[i]=1,B[i+2]=1,i+2<=m-2", "0 1^p 0 <A 0 1 0 0 1^j 0 1 0 1^c+1",  "j+8"),
 ("H2' same with i=0",              "0^inf 0 <A 0 1 0 0 1^j 0 1 0 1^c+1",  "j+8"),
 ("H3  D,B[i+1]=1,i+1<=m-2",        "0 1 D> 1^a+1 0 1 0 1^c+1",            "a+8"),
]

# ---------- encoding ----------
def render(B,ph):
    """encode(B,phase) -> (cells, head index, state). 4 zero cells of padding each side."""
    kind,i=ph; cells=[0]*4; head=None
    for k,b in enumerate(B):
        if k==0 and kind=='A' and i==0: head=len(cells)-2
        if k>0:
            if kind=='A' and k==i: head=len(cells)
            cells+=[0]*(2 if kind=='A' and k in (i,i+1) else 1)
        if kind=='D' and k==i: head=len(cells)+1
        cells+=[1]*b
    return cells+[0]*4,head,kind
def canon(cells,head):
    ones=[k for k,x in enumerate(cells) if x]; a=min(ones+[head]); b=max(ones+[head])
    return ''.join(map(str,cells[a:b+1])),head-a
def inv(B,ph):
    kind,i=ph; m=len(B)
    if m<2: return False
    if kind=='A': return 0<=i<=m-2 and B[i]>=0 and all(b>=1 for k,b in enumerate(B) if k!=i)
    return 1<=i<=m-1 and B[i]>=2 and all(b>=1 for b in B)

# ---------- raw TM ----------
T2={k:(None if v is None else (v[0],1 if v[1]=='R' else -1,v[2])) for k,v in T.items()}
def raw_run(cells,head,state,nsteps,stop=None):
    tape=dict(enumerate(cells)); p=head; s=state; t=0
    while t<nsteps:
        tr=T2[(s,tape.get(p,0))]
        if tr is None: return 'HALT',t,tape,p,s
        w,d,s=tr; tape[p]=w; p+=d; t+=1
        if stop and stop(tape,p,s,t): break
    return 'RUN',t,tape,p,s
def tape_canon(tape,p):
    ks=[k for k,v in tape.items() if v]+[p]; a,b=min(ks),max(ks)
    return ''.join(str(tape.get(k,0)) for k in range(a,b+1)),p-a
def decode(tape,p,s):
    """all family configs whose encoding equals the raw tape (used for X0 only)"""
    st,off=tape_canon(tape,p); out=[]
    runs=[len(x) for x in re.findall('1+',st)]
    if s=='D': cands=[(runs,('D',len(re.findall('1+',st[:off]))-1))]
    elif s=='A':
        idx=len(re.findall('1+',st[:off])); cands=[(runs,('A',idx)),(runs[:idx]+[0]+runs[idx:],('A',idx))]
    else: cands=[]
    for B,ph in cands:
        if inv(B,ph) and canon(*render(B,ph)[:2])==(st,off): out.append((B,ph))
    return out

# ---------- abstract map M ----------
class Halt(Exception): pass
X0_RESULT=([3,1,1],('A',1),25)   # established (Class A, concrete) in section 3 below
def macro(B,ph):
    """one step of M: (B',ph',TM steps), or raises Halt(name, TM steps until F reads 1)"""
    kind,i=ph; B=B[:]; m=len(B)
    if kind=='A':
        n=B[i]
        if n>=2:                                             # R1 / R1' (i=0: p=0, new block)
            if i==0: B.insert(0,0); i=1
            B[i-1]+=1; B[i]-=2; B[i+1]+=1; return B,('A',i),2*(n-2)+17
        if n==0:
            if i>=1:                                         # R2
                p=B[i-1]-1; B[i-1]=p; B[i]=1; return B,('A',i-1),p+10
            if B[1]>=2: B[0]=3; return B,('D',1),13          # R2'
            if m>=3: raise Halt('H1',14)
            return X0_RESULT                                 # B==[0,1]
        j=B[i+1]                                             # n==1
        if i+1==m-1:                                         # R3''
            if i==0: B.insert(0,0); i=1
            return B[:i-1]+[B[i-1]+1,j+1,1],('A',i),2*j+15
        k=B[i+2]
        if k>=2:                                             # R3 / R3'
            if i==0: B.insert(0,0); i=1
            return B[:i-1]+[B[i-1]+1,j+3]+B[i+2:],('D',i+1),j+7
        if i+2==m-1:                                         # R3k
            if i==0: B.insert(0,0); i=1
            return B[:i-1]+[B[i-1]+3,j,3,2],('A',i),6*j+105
        raise Halt('H2',j+8)
    L=B[i]
    if i==m-1: return B[:i]+[L-2,1],('A',i),2*(L-2)+14     # R5
    M=B[i+1]
    if M>=2: return B,('D',i+1),(L-2)+7                     # R4
    if i+1==m-1: return B[:i]+[L+2,0,2],('A',i+1),(L-2)+53 # R6
    raise Halt('H3',(L-2)+8)

if __name__=='__main__':
    import itertools,sys
    print('== 1. Macro rules: symbolic proof (all params>=0) + concrete raw re-check (params 0..7) ==')
    for name,l,r,cnt in RULES:
        ok,st=prove(l,r); good=(ok is True and st==cnt)
        vs=sorted(set(re.findall(r'\^([a-z])(?!nf)',l))); bad=0
        for vals in itertools.product(range(8),repeat=len(vs)):
            env=dict(zip(vs,vals))
            def conc(s):
                s=re.sub(r'\^([a-z])(?!nf)(\+(\d+))?',lambda mm:'^'+str(env[mm.group(1)]+int(mm.group(3) or 0)),s)
                cells=[];h=None;sx=None
                for tk in s.replace('0^inf','').split():
                    if tk.endswith('>'): h=len(cells); sx=tk[0]; continue
                    if tk.startswith('<'): h=len(cells)-1; sx=tk[1]; continue
                    sym,_,ln=tk.partition('^'); cells+=[int(sym)]*int(ln or 1)
                return cells,h,sx
            (c1,h1,s1),(c2,h2,s2)=conc(l),conc(r)
            n=eval(re.sub(r'(\d)([a-z])',r'\1*\2',cnt),{},env)
            # right-anchored (0^inf on left): align right ends; else align left ends
            if l.startswith('0^inf'):
                off1=0; off2=len(c1)-len(c2); pad=n+5
            else: off1=0; off2=0; pad=n+5
            res=raw_run([0]*pad+c1+[0]*pad,pad+h1,s1,n)
            ok2=(res[0]=='RUN' and res[1]==n and res[4]==s2 and res[3]==pad+off2+h2
                 and all(res[2].get(pad+off2+x,0)==c2[x] for x in range(len(c2)))
                 and all(res[2].get(x,0)==0 for x in range(0,pad+off2)) if l.startswith('0^inf') or r.endswith('0^inf') else
                 res[0]=='RUN' and res[1]==n and res[4]==s2 and res[3]==pad+h2 and all(res[2].get(pad+x,0)==c2[x] for x in range(len(c2))))
            if r.endswith('0^inf') and not l.startswith('0^inf'):
                ok2=ok2 and all(res[2].get(x,0)==0 for x in range(pad+len(c2),2*pad+len(c1)+5))
            bad+= not ok2
        print(f'  {name:5s} {l:38s} -> {r:42s} [{cnt}] symbolic={good} concrete_fail={bad}/{8**len(vs)}')
        assert good and bad==0
    print('== 2. Halting lemmas (symbolic, all params>=0) ==')
    for name,l,cnt in HALTS:
        ok,st=prove_halt(l); print(f'  {name:32s} {l:38s} halts: TM reaches (F,1) after {st} steps'); assert ok is True and st==cnt
    print('== 3. Concrete cases (symbolic prover, no variables) + raw re-check ==')
    for nm,l,r_,c_ in [('BASE blank -> [1,1],A@0','0^inf <A 0^inf','0^inf 0 <A 0 1 0 0 1 0^inf','21'),
                       ('X0 [0,1],A@0 -> [3,1,1],A@1','0^inf 0 <A 0 0 0 1 0^inf','0^inf 1^3 0 <A 0 1 0 0 1 0^inf','25')]:
        ok,st=prove(l,r_); print(f'  {nm:30s} {l} -> {r_}  [{st}]'); assert ok is True and st==c_
    c,h,s=render([0,1],('A',0))
    r=raw_run(c,h,s,10**5,lambda tape,p,s,t: bool(decode(tape,p,s)))
    d=decode(r[2],r[3],r[4]); assert r[0]=='RUN' and len(d)==1
    print('  first family config after',r[1],'TM steps:',d[0]); assert (d[0][0],d[0][1],r[1])==X0_RESULT
    print('== 4. Exhaustive sanity of coverage + invariants: all valid configs with m<=6, blocks<=5 ==')
    cnt=0; names={}
    for m in range(2,7):
        for B in itertools.product(range(6),repeat=m):
            for ph in [('A',i) for i in range(m-1)]+[('D',i) for i in range(1,m)]:
                B=list(B)
                if not inv(B,ph): continue
                cnt+=1; c,hd,s=render(B,ph)
                try:
                    B2,ph2,dt=macro(B,ph); assert inv(B2,ph2),(B,ph,B2,ph2)
                    rr=raw_run(c,hd,s,dt)
                    assert rr[0]=='RUN' and rr[4]==ph2[0] and tape_canon(rr[2],rr[3])==canon(*render(B2,ph2)[:2]),(B,ph)
                except Halt as e:
                    rr=raw_run(c,hd,s,e.args[1]+1); assert rr[0]=='HALT' and rr[1]==e.args[1],(B,ph,e.args)
    print('  ',cnt,'configs: each -> invariant-satisfying successor equal to raw TM after stated steps, or raw halt at stated step')
    print('== 5. Base lemma + raw-vs-abstract cross-check (units: TM steps) ==')
    N=int(sys.argv[1]) if len(sys.argv)>1 else 3*10**6
    B0=[1,1]; ph0=('A',0); T0=21
    r=raw_run([0],0,'A',T0); assert r[0]=='RUN' and r[4]=='A' and tape_canon(r[2],r[3])==canon(*render(B0,ph0)[:2])
    first=raw_run([0],0,'A',T0,lambda tape,p,s,t: bool(decode(tape,p,s)))
    assert first[1]==T0
    print('  blank tape, t=',T0,'(first time in family): equals encode',B0,ph0)
    B,ph,t=B0,ph0,T0; cps={}
    while t<=N:
        cps[t]=(B,ph)
        if t==1466: assert (B,ph)==([10,9,11,0,4,2],('A',3))
        try: B,ph,dt=macro(B,ph)
        except Halt as e: print('  abstract halt',e.args,'at',t); break
        t+=dt
    tape=bytearray(1<<16); p=1<<15; s='A'; ok=0
    for tt in range(N+1):
        if tt in cps:
            Bc,phc=cps[tt]; bt=bytes(tape); a=min(bt.find(1),p); b=max(bt.rfind(1),p)
            got=(''.join(map(str,tape[a:b+1])),p-a,s); want=canon(*render(Bc,phc)[:2])+(phc[0],)
            assert got==want,('MISMATCH',tt,Bc,phc); ok+=1
        tr=T2[(s,tape[p])]
        if tr is None: print('  TM HALT at',tt); break
        w,d,s=tr; tape[p]=w; p+=d
    print(f'  {ok} macro checkpoints matched exactly, t in [{T0},{N}] TM steps, no halt; blocks at end: {len(B)}')
