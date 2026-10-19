"""Defect calculus for c-source histories and outer b entries (UNREVIEWED).

Checks: grammar enumeration; one-step shift lemma on actual crossings; canonical
c sources (calendar) against the G_delta reduction; canonical outer b entries;
finite scans of reference families. Finite checks do not prove EXT.
Usage: python -B verify_defect.py [B] [range_max]
"""
import sys,json,time
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'work_ext_roots'))
sys.path.insert(0,str(ROOT/'work_global_ext'/'route_c'))
from grammar import words,phi_seq,show,classify
from verify_low_deficit import Calendar,val,first_fire
from fdata import lam_walk,small_full,v2
T0=time.time();RES={}
# 1. grammar ------------------------------------------------------------
g={};seen=set()
for eps in range(3,16,2):
    ws=words(eps-1);cnt=Counter();opens=Counter();ainit=sum(1 for w in ws if w[0]=='A')
    for w in ws:
        c=classify(w)
        if c.startswith('open'):cnt['open']+=1;opens[int(c.split('_')[1])]+=1
        else:cnt[c.split(' ')[0]]+=1
    new=sorted(set(opens)-seen);seen|=set(opens)
    g[eps]=dict(words=len(ws),A_initial=ainit,classes=dict(cnt),open_deltas=dict(sorted(opens.items())),
               new_deltas=new,
               bc_first_words={show(w):classify(w) for w in ws if w[0]!='A'} if eps<=11 else None)
assert [g[e]['words'] for e in range(3,16,2)]==[1,2,5,14,42,132,429]
RES['grammar']=g
# 2. one-step shift lemma on actual crossings ------------------------------
X=small_full(1024);step=0
for n in range(4,1024):
    r=X[n]
    if not r['odd']:continue
    j=n+1
    if r['typ']=='a':
        k=r['tau']//2;Rx,Rt,sig=6*k+4,6*k+5,n
    else:
        c,lam=r['x'];Rx,Rt,sig=lam,3*r['tau']+5,n-r['eps']
        assert v2(c)==sig and r['omega']<sig
    for d in range(-12,13):
        for u in (1,3,5,(1<<40)+7):
            for hi in (0,1,-3):
                x=(1<<j)*u;th=x+d+hi*(1<<(j+1))
                if r['typ']=='a':xn=2*th+3*r['tau']-x//2;sx=2*(d-2)
                else:xn=c*(x>>j)+lam;sx=0
                tn=th+3+3*r['tau']
                assert (xn-Rx-sx)%(1<<sig)==0 and (tn-Rt-(d-2))%(1<<sig)==0
                step+=1
RES['one_step_shift_checks']=step
# 3. canonical c sources and outer b entries -------------------------------
B=int(sys.argv[1]) if len(sys.argv)>1 else 512
NMAX=int(sys.argv[2]) if len(sys.argv)>2 else 20000
cal=Calendar(B);memo={}
def history(n):
    if n in memo:return memo[n]
    fire=cal.preceding_fire_by_pointer(n);J=fire['J'];a=n-fire['pointer']-1
    K=cal.kernels[J];w=[];cnt=0;pos=None
    for t,(j,L) in enumerate(zip(K['word'],K['types'])):
        w.append('A' if L=='a' else 'B' if L=='b' else ('C',history(j-1)[0]))
        if L=='a':
            cnt+=1
            if cnt==a:pos=t;break
    assert pos is not None and pos<len(K['word'])-1
    memo[n]=(tuple(w),K['word'][pos],J);return memo[n]
def weight(w):return sum(2 if isinstance(L,str) else 2+weight(L[1]) for L in w)
def walk(j,x,th,lim=60):
    out=[];G=0
    for _ in range(lim):
        if x<=0:return out,'nonpositive'
        assert val(x)==j;out.append((j,G))
        r=cal.crossing(j-1)
        if not r['odd']:return out,'end'
        if r['kind']=='a':x=2*th+3*r['time']-x/2
        else:x=(r['head_ratio']+2*r['tail_ratio'])/2*x+r['head_lambda']+2*r['tail_lambda']+3
        th+=3+3*r['time'];G+=1+r['epsilon'];j=val(x)
    return out,'limit'
cstat=Counter();hist=Counter();ex={}
def check_c(n):
    row=cal.crossing(n)
    if row['kind']!='c' or not row['odd']:return
    w,p,J=history(n);assert row['epsilon']==weight(w)+1
    Phi=phi_seq(w)[-1];lam=row['tail_lambda'];om=row['omega']
    assert (1-lam-Phi)%(1<<(om+1))==0          # real defect = Phi mod 2^(j+1)
    th=F(3*row['time']+4);x=th+lam;delta=Phi-1
    fin=cal.crossing(p-1);assert fin['kind']=='a' and fin['odd']
    z=6*(fin['time']//2)+4-2*delta
    assert min(val(x-z),val(th-z-delta))>=p-1 and n-row['epsilon']>=p
    a,sa=walk(om,x,th);r,sr=walk(val(F(z)),F(z),F(z+delta))
    assert [q[0] for q in a]==[q[0] for q in r] and sa==sr=='end'
    assert max(q[0]+q[1] for q in r)<p-1
    cstat['eps=%d %s'%(row['epsilon'],classify(w))]+=1;hist[show(w)]+=1
    ex.setdefault(show(w),dict(n_bits=n.bit_length(),J_source=J,p=p,delta=delta,tail=[q[0] for q in a]))
bstat=Counter();bres=Counter();bex=[]
def check_b(n):
    row=cal.crossing(n)
    if row['kind']!='b' or not row['odd']:return
    s=row['time'];xF=3*s+4;om=val(xF);assert om==row['omega']
    if om<5:bstat['omega<5 (ends)']+=1;return
    K=cal.kernels[om];js,ty=K['word'],K['types']
    a,sa=walk(om,F(xF),F(xF));oj=[q[0] for q in a]
    assert all(q[0]+q[1]+2<n+1 for q in a)      # strict EXT margin of S(n+1)
    d=1;t=None
    for i,(j,L) in enumerate(zip(js,ty)):
        if i==len(js)-1:break
        if L=='a':t=i;break
        if L=='b':d-=1
        else:d+=phi_seq(history(j-1)[0])[-1]-2
    if t is None:
        assert oj==list(js);bstat['E_F has no a-step: exact copy to end']+=1;return
    if js[t+1]>=2:
        assert oj==list(js[:t+1])+[1];bstat['dies (j=1) at first a-step']+=1;return
    bstat['climbs: E_F ends at its first a-step']+=1
    m=js[t];k=cal.crossing(m-1)['time']//2;delta=4-d;z=6*k+6-2*delta
    xx,tt=F(xF),F(xF)
    for j in js[:t+1]:
        r=cal.crossing(j-1)
        if r['kind']=='a':xx=2*tt+3*r['time']-xx/2
        else:xx=(r['head_ratio']+2*r['tail_ratio'])/2*xx+r['head_lambda']+2*r['tail_lambda']+3
        tt+=3+3*r['time']
    assert min(val(xx-z),val(tt-z-delta))>=m-1
    rr,_=walk(val(F(z)),F(z),F(z+delta))
    assert oj[t+1:]==[q[0] for q in rr]
    bres['H_delta delta=%d (d=%d)'%(delta,d)]+=1
    if len(bex)<8:bex.append(dict(n_bits=n.bit_length(),omega=om,E_F_word=list(js),E_F_types=ty,
                                  outer_word=oj,delta=delta,ref_tail=[q[0] for q in rr]))
for n in range(4,NMAX):check_c(n);check_b(n)
for P in range(5,B+1):
    try:fire=first_fire(cal,P)
    except AssertionError:continue
    rho=fire['pointer'];check_b(rho+1)
    for a in range(1,cal.kernels[P]['types'][:-1].count('a')+1):check_c(rho+1+a)
RES['canonical']=dict(B=B,range_max=NMAX,c_classes=dict(cstat),c_histories=dict(hist),c_examples=ex,
                      b_cases=dict(bstat),b_residual=dict(bres),b_examples=bex)
print('canonical done',round(time.time()-T0,1),flush=True)
# 4. finite scans of reference families -------------------------------
N=10**6;D=lam_walk(N);T=small_full(1024)
def follow(C,x,th):
    G=0;word=[];rec=0
    for _ in range(200):
        if x<=0:return 'nonpositive',word,rec
        j=v2(x);word.append(j);rec=max(rec,j+G)
        if j+G>=C:return 'ceiling',word,rec
        r=T[j-1]
        if not r['odd']:return 'end',word,rec
        if r['typ']=='a':x=2*th+3*r['tau']-x//2
        else:c,l=r['x'];x=c*(x>>j)+l
        th+=3+3*r['tau'];G+=1+r['eps']
    return 'limit',word,rec
fam={}
specs=[('G_%d=(6k+4-2d,6k+4-d)'%dl,(lambda k,dl=dl:(6*k+4-2*dl,dl))) for dl in range(-7,10) if dl not in (0,1,2)]
specs+=[('H_%d=(6k+6-2d,6k+6-d)'%dl,(lambda k,dl=dl:(6*k+6-2*dl,dl))) for dl in range(-6,10) if dl not in (1,2)]
for name,f in specs:
    st=Counter();longest=[];minmargin=None;fails=[]
    for m in range(5,N):
        if D['typ'][m-1]!=97 or not D['odd'][m-1]:continue
        z,dl=f(D['tau'][m-1]//2);s,wd,rec=follow(m-1,z,z+dl);st[s]+=1
        if s!='end':
            if len(fails)<5:fails.append(dict(m=m,status=s,word=wd))
            continue
        mg=m-1-rec;minmargin=mg if minmargin is None else min(minmargin,mg)
        if len(wd)>len(longest):longest=wd
    fam[name]=dict(status=dict(st),longest=longest,min_margin=minmargin,non_end_examples=fails)
RES['family_scans_m_lt_1e6']=fam
RES['seconds']=round(time.time()-T0,1)
RES['result']='PASS';RES['review_status']='UNREVIEWED'
RES['scope']='Finite checks of exact identities and of reference families; no all-scale family property or EXT is claimed.'
HERE.joinpath('defect_checks.json').write_text(json.dumps(RES,indent=1)+'\n',encoding='utf-8')
print(json.dumps({k:RES[k] for k in ('canonical','family_scans_m_lt_1e6','seconds')},indent=1))
