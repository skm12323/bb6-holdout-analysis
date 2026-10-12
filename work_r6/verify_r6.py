# R6: top-map simulator + 2-adic invariant search (Class-C evidence only).
import sys
def step(L):
    A=L[0]; b=L[1] if len(L)>1 else 0; c=L[2] if len(L)>2 else 0; S=L[3:]
    if A%2==0: return [A+b+c+3]+S, None
    x=A+2*b+3
    if x&(x-1)==0: return None, x
    m=b+(A-3)//2; st=[c+(A+1)//2]+S   # RULES sec.5 (as in verify_r4.top)
    while m%2==1 and m>=3: st=[(m+3)//2]+st; m=(m-3)//2
    assert m!=1
    return [m+4]+st, None
def run(N):
    L=[3]; mods={}
    for n in range(N):
        A=L[0]; b=L[1] if len(L)>1 else 0
        if A%2:
            for k in range(2,9): mods.setdefault(k,set()).add((A+2*b+3)%(1<<k))
        L,h=step(L)
        if L is None: print("HALT at",n); return
        assert sum(L)==3*(n+1)+3
    print("no halt to",N)
    for k in mods: print(k, len(mods[k]), "of", 1<<k, "residues of A+2b+3 hit; 0 hit:",0 in mods[k])
run(int(sys.argv[1]) if len(sys.argv)>1 else 200000)

def closeness(N):
    # record odd steps where A+2b+3 = 2^k * q, q odd small (q<=7): near-halts
    L=[3]; out=[]
    for n in range(N):
        A=L[0]; b=L[1] if len(L)>1 else 0
        if A%2:
            x=A+2*b+3; k=(x&-x).bit_length()-1; q=x>>k
            if q<=7 and k>=6: out.append((n,k,q))
        L,_=step(L)
    return out
if __name__=='__main__' and len(sys.argv)>2:
    for t in closeness(int(sys.argv[1])): print(t)
