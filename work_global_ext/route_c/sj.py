"""sj.py -- exact symbolic exit S(J) via its beta-parts (route C).

State after chain t>=1: (j_t, beta_u (odd integer), d_t, Gamma_t).  Identities (PROOF_EL A1/A2, Lemma T):
  a-step at n=j-1, tau(n)=2k:  beta_x' = 2(3d+1+3k) - 2^n beta_u
  b/c-step:                     beta_x' = c'_x * beta_u + lambda'_x   (W-chain x' at tau(n))
  d' = d+1+tau(n),  Gamma' = Gamma+1+eps(n),  j' = v2(beta_x'), tie iff j' >= J-Gamma'.
Chain 0 (fire): beta_u=0, d=0, Gamma=0.
"""
from fdata import v2

def sym_beta(J, LD, SM, NS):
    """returns dict(js, types, h, theta, status) ; theta_t = (3d_t+1) mods 2^j_t (centered)."""
    j=J; bu=0; d=0; G=0; js=[J]; types=''; hs=[0]; ths=[1]; status='end'
    while True:
        n=j-1
        if n<NS:
            R=SM[n]; t=R['typ']; od=R['odd']; T=R['tau']; e=R['eps']
        else:
            t='abc'[LD['typ'][n]-97]; od=LD['odd'][n]; T=LD['tau'][n]; e=LD['eps'][n]
        if not od: break
        types+=t
        if t=='a':
            assert T%2==0
            bx=2*(3*d+1+3*(T//2))-(bu<<n)
        else:
            if n<NS:
                cx,lx=R['x']; bx=cx*bu+lx
            else:
                assert bu==0, ('large b/c index after chain 0',J,n)
                la=LD['lA'][n]
                bx=(la+3) if t=='b' else (la+2*LD['lY'][n]+3)
        d+=1+T; G+=1+e
        jn=v2(bx)
        if jn>=J-G: status='TIE'; js.append(jn); break
        j=jn; bu=bx>>j; js.append(j); hs.append(J-G-j)
        M=1<<j; th=(3*d+1)%M
        if th>M//2: th-=M
        ths.append(th)
    return dict(js=js,types=types,h=hs,theta=ths,status=status,G=G,d=d)
