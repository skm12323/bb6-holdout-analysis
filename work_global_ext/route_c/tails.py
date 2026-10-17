"""tails.py N th1,th2,... : exit tails of the (j,theta) automaton (PROOF_EL A1/A2) from every entry (m,theta),
5<=m<N, using REAL crossing data X(n), n<N (lam_walk).  NT failures are reported (not resolved).
Route a of S(J) enters at (j_1,2), route b at (J_F,0) (PROOF_EL Thm D); other theta model shifted entries."""
import sys,time,json
from collections import Counter
from fdata import lam_walk, v2

def build(N):
    D=lam_walk(N)
    return D

def make_tail(D):
    typ=D['typ']; tau=D['tau']; odd=D['odd']; lA=D['lA']; lY=D['lY']
    memo={}
    def step(j,th):
        """one transition; returns ('end',) | ('tie',) | (j',th') ; th centered mod 2^j"""
        n=j-1
        if n<4 or not odd[n]: return ('end',)
        T=tau[n]; t=typ[n]
        if t==97:
            v=th+3*(T//2)
            if v==0: jn=n
            elif abs(v).bit_length()<n-1: jn=1+v2(v)
            else:
                M=1<<n; rem=(v-(M>>1))%M
                if rem==0: return ('tie',)
                jn=1+v2(rem)
            thn=3-th
        else:
            lam=lA[n]+3 if t==98 else lA[n]+2*lY[n]+3
            jn=v2(lam); thn=th+3*T+3
        M=1<<jn; thn%=M
        if thn>M//2: thn-=M
        return (jn,thn,chr(t))
    def tail(j,th):
        key=(j,th)
        if key in memo: return memo[key]
        r=step(j,th)
        if r[0]=='end': res=((j,),'',True)
        elif r[0]=='tie': res=((j,),'T',False)
        else:
            sub=tail(r[0],r[1]) if r[0]<64 else tail_nomemo(r[0],r[1])
            res=((j,)+sub[0],r[2]+sub[1],sub[2])
        if j<64: memo[key]=res
        return res
    def tail_nomemo(j,th):
        return tail(j,th)
    return tail,step

if __name__=='__main__':
    N=int(sys.argv[1]); ths=[int(x) for x in sys.argv[2].split(',')]
    t0=time.time(); D=build(N); print('data %.0fs'%(time.time()-t0),flush=True)
    tail,step=make_tail(D)
    out={}
    for th in ths:
        lens=Counter(); first={}; ties=[]; longest=[]
        for m in range(5,N):
            if abs(th)<(1<<min(m,62))//2: t=th
            else:
                M=1<<m; t=th%M
                if t>M//2: t-=M
            w,ty,ok=tail(m,t)
            if not ok: ties.append((m,w)); continue
            r=len(w)
            lens[r]+=1
            if r not in first: first[r]=(m,w,ty)
            if r>=4 and len(longest)<40: longest.append((m,w,ty))
        out[th]=dict(len_dist=dict(sorted(lens.items())),first=first,nties=len(ties),ties=ties[:30],longest=longest)
        print('theta',th,'lens',dict(sorted(lens.items())),'ties',len(ties),ties[:5],'first',first,flush=True)
    json.dump({str(k):v for k,v in out.items()},open('tails_%d.json'%N,'w'),indent=1,default=str)
    print('time %.0fs'%(time.time()-t0))
