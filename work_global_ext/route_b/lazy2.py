"""Exhaustive lazy enumeration of the beta-walk over ALL generic states (j0, d=X, beta_u=Y),
0<=X<2^BX, Y odd, 0<Y<2^BY.  Every quantity is (pX+qY+r)/2^s.  Bits of X,Y are revealed only when a
valuation needs them; once all BX (BY) bits are revealed the variable is exact.
Reports, per j0, the max number of chains and of non-descending steps over the whole box."""
import sys,time
from collections import Counter
from core import load, v2
T=load(30000)

def run(j0,BX,BY,maxnodes=5*10**6):
    best=(0,0,None); ndc=Counter(); lc=Counter(); nodes=0
    stack=[(0,0,1,1)]   # (MX,Xlow,MY,Ylow) ; Y odd
    while stack:
        MX,Xl,MY,Yl=stack.pop(); nodes+=1
        if nodes>maxnodes: return best,ndc,lc,nodes,'CAP'
        def q(p_,qq,r):
            # valuation of p_*X+qq*Y+r, or ('X'|'Y') if undetermined
            if MX>=BX and MY>=BY:
                w=p_*Xl+qq*Yl+r; return v2(w) if w else 10**9
            PX=10**9 if (p_==0 or MX>=BX) else MX+v2(p_)
            PY=10**9 if (qq==0 or MY>=BY) else MY+v2(qq)
            P=min(PX,PY)
            xs=Xl if MX>=BX else Xl; ys=Yl
            w=(p_*xs+qq*ys+r)
            if P>=10**9: return v2(w) if w else 10**9
            w%=(1<<P)
            if w: return v2(w)
            return 'X' if PX<=PY else 'Y'
        # walk
        j=j0; dp,dq,dr=1,0,0; up,uq,ur,us=0,1,0,0; L=0; nd=0; res=None
        while True:
            n=j-1
            if n not in T: res='OUT'; break
            row=T[n]
            if not row['odd']: res='END'; break
            if row['typ']=='a':
                sh=n-us   # bx = 6d+2+3tau - bu*2^n ;  bu=(up X+uq Y+ur)/2^us
                if sh>=0: P_,Q_,R_,S_=6*dp-(up<<sh),6*dq-(uq<<sh),6*dr+2+3*row['tau']-(ur<<sh),0
                else: P_,Q_,R_,S_=(6*dp<<-sh)-up,(6*dq<<-sh)-uq,((6*dr+2+3*row['tau'])<<-sh)-ur,-sh
            else:
                cxW,lxW,jW=row['W']; P_,Q_,R_,S_=up*cxW,uq*cxW,ur*cxW+(lxW<<us),us
            dr+=1+row['tau']
            vv=q(P_,Q_,R_)
            if isinstance(vv,str): res=vv; break
            jn=vv-S_
            if jn<0 or jn>=10**8: res='BAD'; break
            L+=1
            if jn>=j: nd+=1
            j=jn; up,uq,ur,us=P_,Q_,R_,S_+jn
            if L>400: res='LONG'; break
        if res=='X': stack.append((MX+1,Xl,MY,Yl)); stack.append((MX+1,Xl|(1<<MX),MY,Yl)); continue
        if res=='Y': stack.append((MX,Xl,MY+1,Yl)); stack.append((MX,Xl,MY+1,Yl|(1<<MY))); continue
        ndc[nd]+=1; lc[L]+=1
        if (nd,L)>best[:2]: best=(nd,L,(MX,Xl,MY,Yl,res))
    return best,ndc,lc,nodes,'OK'

if __name__=='__main__':
    BX=int(sys.argv[1]); BY=int(sys.argv[2]); js=[int(a) for a in sys.argv[3].split(',')]
    for j0 in js:
        t0=time.time(); best,ndc,lc,nodes,st=run(j0,BX,BY)
        print('j0=%d BX=%d BY=%d nodes=%d %s  max(nd,L)=%s  nd-dist=%s  L-dist=%s  %.1fs'%(j0,BX,BY,nodes,st,best[:2],dict(sorted(ndc.items())),dict(sorted(lc.items())),time.time()-t0))
        if best[2]: print('   witness',best[2])
