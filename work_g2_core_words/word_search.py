"""Exhaustive bounded-alphabet word search with exact accumulated lattices.
No feasibility result asserts positivity, physical safety, or orbit reachability.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
def val(z):return (abs(z)&-abs(z)).bit_length()-1 if z else 10**9
def constrain(base,cols,A,B,target,mod):
    cs=[A*v[0]+B*v[1] for v in cols]
    rhs=(target-A*base[0]-B*base[1])%mod
    s=min(val(cs[0]),val(cs[1]),val(mod));g=1<<s
    if rhs%g:return None
    M=mod//g
    if M==1:return base,cols
    p=0 if val(cs[0])==s else 1;o=1-p
    inv=pow((cs[p]//g)%M,-1,M)
    off=rhs//g*inv%M;adj=-(cs[o]//g)*inv%M
    nb=tuple(base[i]+off*cols[p][i] for i in range(2));nc=[None,None]
    nc[p]=tuple(M*x for x in cols[p]);nc[o]=tuple(cols[o][i]+adj*cols[p][i] for i in range(2))
    return nb,nc
def search(cap,depth):
    table=vm.Xdata(cap+1,SMALL=cap+1)
    tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
    blocks={};costs={};terminal_costs={};losses={};terminal_losses={}
    for q in range(5,cap+1):
        j=q;a=F(1);B=F(0);d=G=0
        while True:
            typ,H,Y,e=table[j-1]
            if sum(H)%2==0:
                terminal_costs[q]=d+tau[j-1]+2;terminal_losses[q]=G;break
            if typ=='a':
                blocks[q]=(a,B,d,tau[j-1]//2)
                costs[q]=d+tau[j-1]+1;losses[q]=G+1;break
            c=H[0]+2*Y[0];l=H[1]+2*Y[1]+3;r=F(c,1<<j)
            a*=r;B=r*B+l;d+=1+tau[j-1];G+=1+e;j=val(l)
    for q in range(1,5):terminal_costs[q]=tau[q-1]+2;terminal_losses[q]=0
    alphabet=sorted(blocks)
    frontier=[((q,r),(F(0),F(1<<q),F(0)),(F(0),F(0),F(1<<r)),(1,1),[(2,0),(0,2)])
              for q in alphabet for r in alphabet]
    counts={2:len(frontier)};samples={};edges=[];escapes=0;prune_checks=0;processed=0;escape_depths={}
    for length in range(2,depth):
        following=[]
        for word,x0,x1,base,cols in frontier:
            processed+=1
            a,B,d,k=blocks[word[-2]];b,E,f,l=blocks[word[-1]]
            C=B/2+6+6*k+6*l+6*f-E/2
            x=tuple(a*x0[z]/2+(1-b/2)*x1[z]+(C if z==0 else 0) for z in range(3))
            den=max(v.denominator for v in x);shift=val(den)
            c,A,H=[int(v*den) for v in x]
            c0=c+A*base[0]+H*base[1]
            slopes=[A*v[0]+H*v[1] for v in cols]
            s=min(map(val,slopes));v=val(c0)
            escape=False
            if v<s:
                possible=[v-shift] if v-shift in blocks else []
                if v-shift>cap:escapes+=1;escape=True
            else:
                possible=[q for q in alphabet if q>=s-shift]
                escapes+=1;escape=True # this coset also permits values above the cap
            if cap<=63 or prune_checks<128:
                unpruned=[q for q in alphabet if constrain(base,cols,A,H,den*(1<<q)-c,den*(1<<(q+1))) is not None]
                assert possible==unpruned;prune_checks+=1
            children=[]
            for q in possible:
                ans=constrain(base,cols,A,H,den*(1<<q)-c,den*(1<<(q+1)))
                assert ans is not None
                nb,nc=ans;children.append(q)
                following.append((word+(q,),x1,x,nb,nc))
            if escape:escape_depths[length]=escape_depths.get(length,0)+1
            if children or escape:
                edges.append(dict(word=word,children=children,can_escape=escape,
                                  escape_minimum=max(cap+1,s-shift) if escape and v>=s else v-shift if escape else None))
        frontier=following;counts[length+1]=len(frontier)
        print('length',length+1,'feasible',len(frontier),flush=True)
        if frontier:samples[length+1]=[list(v[0]) for v in frontier[:5]]
        if not frontier:break
    result=dict(cap=cap,depth_limit=depth,productive_parameters=len(alphabet),
                alphabet=alphabet,counts=counts,exhausted=not frontier,
                max_feasible_length=max(k for k,v in counts.items() if v),
                samples=samples,escape_nodes=escapes,
                escape_depths=escape_depths,processed_nodes=processed,
                omitted_terminal_nodes=processed-len(edges),
                unpruned_crosschecks=prune_checks,
                max_block_steps=max(costs.values()),max_block_loss=max(losses.values()),
                max_terminal_steps=max(terminal_costs.values()),max_terminal_loss=max(terminal_losses.values()),
                caveat='Necessary arithmetic constraints only; exits above cap are not ruled out',edges=edges)
    Path(__file__).with_name(f'words_{cap}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('edges','alphabet','samples')},indent=2))
if __name__=='__main__':search(int(sys.argv[1]) if len(sys.argv)>1 else 255,int(sys.argv[2]) if len(sys.argv)>2 else 16)
