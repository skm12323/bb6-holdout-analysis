"""Fast skeleton of F: epochs only, small (lambda) data.  Small-index crossing data
(typ,hpar,tau,lamX) are taken from an exact F run (fdata) for n < NSMALL.
For every odd-head crossing n, computes the exit of a hypothetical fire J=n+1
(depends only on X(n) data, M Lemma 6.1) using residues: valid while all j stay
well below J (checked)."""
import sys
from fdata import crossings, v2
NSMALL=200
tauS,typS,hparS,XS=crossings(NSMALL+40)

def exit_from(Th, x, s_unused=None):
    # exit recursion on actual small values, small-index data only
    js=[]
    while True:
        j=v2(x); js.append(j); n=j-1
        if n>=NSMALL: return js,'big'
        if not hparS[n]: return js,'stop'
        if typS[n]=='a':
            k=tauS[n]//2; x=2*Th-x//2+6*k; Th=Th+3+6*k
        else:
            cX,lX,_=XS[n]; x=((cX*x)>>j)+lX; Th=Th+3*tauS[n]+3

def first_state(t, s, lamX):
    # (Theta_1, x_1) residues for a fire J=n+1 with J huge, crossing n of type t at time s
    if t=='a':
        k=s//2; return 4+6*k, 2+6*k
    return 4+3*s, lamX

def run(PMAX, check=None, report=1):
    s=0; rho=0
    cross=[] if check is not None else None
    rmax=0; rec={}
    def on_cross(n, t, s_, h, lamX):
        nonlocal rmax
        if cross is not None: cross.append((n,t,s_,h))
        if not h: return
        Th,x=first_state(t,s_,lamX)
        js,why=exit_from(Th,x)
        r=len(js)  # chains after the fire
        # precision: every j_t must stay below J-1 minus the coefficient loss (<= 8 per chain under C2, eps<=7 here)
        if max(js)+8*len(js)+2>=n: why='prec'
        if r>rmax or why not in('stop',):
            rec.setdefault((r,why),(n,t,s_,js))
            if r>rmax:
                rmax=r
                if report: print("new max r=%d at n=%d type %s s=%d js=%s %s"%(r+0,n,t,s_,js,why),flush=True)
    while rho<PMAX:
        if s&1 or s==0:
            on_cross(rho,'a',s,0,None); on_cross(rho+1,'b',s,0,None)
            rho+=2; s+=1; continue
        on_cross(rho,'a',s,1,None); on_cross(rho+1,'b',s,1,3*s+4)
        i=rho+2
        Th=3*s+5; x=3*s+4; st=s
        while True:
            j=v2(x); n=j-1
            ret=st+1+tauS[n]
            if not hparS[n]:
                if typS[n]=='a':
                    on_cross(i,'c',ret,0,None); i+=1
                s=ret+1; break
            if typS[n]=='a':
                # return state P=[D]: type-c crossing at index i, time ret, odd head
                k=tauS[n]//2; xn=2*Th-x//2+6*k; Thn=Th+3+6*k
                on_cross(i,'c',ret,1,xn); i+=1
            else:
                cX,lX,_=XS[n]; xn=((cX*x)>>j)+lX; Thn=Th+3*tauS[n]+3
            x,Th,st=xn,Thn,ret
        rho=i
    return cross, rmax, rec

if __name__=="__main__":
    PMAX=int(sys.argv[1])
    _,rmax,rec=run(PMAX)
    print("rmax",rmax)
    for k,v in sorted(rec.items()): print(k,v)
