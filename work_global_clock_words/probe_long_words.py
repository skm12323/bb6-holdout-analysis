"""Stream exact mixed-block word search without allocating all initial pairs.

This is an arithmetic overapproximation. Surviving words do not assert
positivity, physical safety or canonical reachability. Escapes remain open.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json,time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
sys.path.insert(0,str(ROOT/'work_g2_core_words'))
import verify_m as vm
from word_search import constrain,val

def search(cap,target):
    table=vm.Xdata(cap+1,SMALL=cap+1)
    tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
    blocks={}
    for q in range(5,cap+1):
        j=q;alpha=F(1);B=F(0);d=G=0
        while True:
            typ,H,Y,e=table[j-1]
            if sum(H)%2==0:break
            if typ=='a':
                k=tau[j-1]//2
                assert B.denominator==1 and int(B)%2==0
                blocks[q]=(alpha,B,d,k,G,int(B)//2+6*k,6+6*k+6*d-int(B)//2)
                break
            ratio=F(H[0]+2*Y[0],1<<j);constant=H[1]+2*Y[1]+3
            alpha*=ratio;B=ratio*B+constant;d+=1+tau[j-1];G+=1+e;j=val(constant)
    alphabet=sorted(blocks);counts=Counter();escapes=Counter();processed=Counter()
    witnesses=[];initial_pruned=0;start=time.monotonic();last=start
    long_shapes=Counter();nonalternating=[];sixth_outputs=Counter();long_first=Counter()
    def descend(node):
        nonlocal last
        stack=[node]
        while stack:
            word,x0,x1,base,cols=stack.pop();length=len(word);counts[length]+=1
            if length>=5:
                alternating=word[0]==word[2] and word[1]==word[3] and word[0]<word[1]
                long_shapes[(length,alternating)]+=1
                if not alternating and len(nonalternating)<12:nonalternating.append(word)
            if length==6:long_first[word[0]]+=1
            if length>=target:
                if len(witnesses)<10:
                    witnesses.append(dict(word=word,base=base,cols=cols))
                continue
            processed[length]+=1
            a,B,d,k,*_=blocks[word[-2]];b,E,f,l,*_=blocks[word[-1]]
            C=B/2+6+6*k+6*l+6*f-E/2
            xx=tuple(a*x0[z]/2+(1-b/2)*x1[z]+(C if z==0 else 0) for z in range(3))
            den=max(v.denominator for v in xx);shift=val(den)
            c,A,H=(int(v*den) for v in xx)
            constant=c+A*base[0]+H*base[1]
            slopes=[A*v[0]+H*v[1] for v in cols]
            vv=val(constant);s=min(map(val,slopes))
            if vv<s:
                possible=[vv-shift] if vv-shift in blocks else []
                if length==6:sixth_outputs[vv-shift]+=1
                if vv-shift>cap:escapes[length]+=1
            else:
                if length==6:sixth_outputs['unbounded']+=1
                possible=[q for q in alphabet if q>=s-shift];escapes[length]+=1
            for q in reversed(possible):
                ans=constrain(base,cols,A,H,den*(1<<q)-c,den*(1<<(q+1)))
                assert ans is not None
                nb,nc=ans;stack.append((word+(q,),x1,xx,nb,nc))
            now=time.monotonic()
            if now-last>20:
                print(json.dumps(dict(seconds=round(now-start),counts=dict(counts),
                                      target_witnesses=len(witnesses))),flush=True);last=now
    for q in alphabet:
        bq=blocks[q]
        for r in alphabet:
            br=blocks[r]
            # Exact cheap pruning for a unique least-valuation summand.
            vals=[q-bq[4]-1,r-br[4]-1,val(bq[5]+br[6])]
            low=min(vals)
            if vals.count(low)==1 and low not in blocks and low<=cap:
                counts[2]+=1;processed[2]+=1;initial_pruned+=1;continue
            descend(((q,r),(F(0),F(1<<q),F(0)),(F(0),F(0),F(1<<r)),(1,1),[(2,0),(0,2)]))
    result=dict(cap=cap,target_length=target,productive=len(alphabet),counts=dict(sorted(counts.items())),
                processed=dict(sorted(processed.items())),escape_depths=dict(sorted(escapes.items())),
                initial_pairs_pruned=initial_pruned,target_witnesses=witnesses,
                long_shapes=[dict(length=k[0],starts_small_large_small_large=k[1],count=v)
                             for k,v in sorted(long_shapes.items())],
                nonalternating_samples=nonalternating,
                sixth_entry_first_parameters=dict(sorted(long_first.items())),
                outputs_after_six_entries=dict(sixth_outputs),
                exhausted_below_cap=counts[target]==0,
                seconds=round(time.monotonic()-start,2),
                scope='All ordered initial pairs, exact necessary lattices; escapes and canonical reachability unresolved')
    Path(__file__).with_name(f'long_words_{cap}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    search(int(sys.argv[1]) if len(sys.argv)>1 else 4095,int(sys.argv[2]) if len(sys.argv)>2 else 8)
