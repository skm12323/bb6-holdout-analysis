"""Exact mixed-block word search at fixed EXT-entry phase defect.

One shared integer root clock is retained. Missing output parameters are
reported as escapes, never treated as termination. Standard library only.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_global_calendar'))
sys.path.insert(0,str(ROOT/'work_global_clock_words'))
from calendar_oracle import Calendar, val
from clock_words import clock_projection


def build(calendar,q):
    j=q;alpha=F(1);B=F(0);d=G=0;types=''
    while True:
        row=calendar.crossing(j-1)
        if not row['odd']:
            return None
        kind=row['kind'];types+=kind
        if kind=='a':
            k=row['time']//2
            assert alpha.denominator==1 << G
            c=6*d+6*k-B/2
            assert c.denominator==1
            return dict(alpha=alpha,B=B,d=d,G=G,k=k,T=d+1+2*k,
                        numerator=alpha.numerator,constant=int(c),types=types)
        ratio=(row['head_ratio']+2*row['tail_ratio'])/2
        lam=row['head_lambda']+2*row['tail_lambda']+3
        alpha*=ratio;B=ratio*B+lam
        d+=1+row['time'];G+=1+row['epsilon'];j=val(lam)


def constrain(N,C,E,r,h,q):
    bits=E+q+1
    modulus=1 << bits
    wanted=(((1 << (bits-1))-C)*pow(N,-1,modulus)) & (modulus-1)
    if (wanted-r) & ((1 << min(h,bits))-1):
        return None
    return (wanted,bits) if bits>h else (r,h)


def search(blocks,known,defect,cap=18):
    alphabet=sorted(blocks)
    count=Counter();escapes=[];longest=();comparisons=0
    stack=[((q,),1,-defect,0,0,defect+(1 << q),q+1) for q in alphabet]
    # theta initial residue must be canonical, even for negative defect.
    stack=[(w,N,C,E,t,r & ((1 << h)-1),h) for w,N,C,E,t,r,h in stack]
    while stack:
        word,N,C,E,t,r,h=stack.pop()
        count[len(word)]+=1
        if len(word)>len(longest):longest=word
        if len(word)>=cap:
            escapes.append(dict(word=word,reason='depth cap'));continue
        b=blocks[word[-1]];loss=b['G']+1;En=E+loss
        Nn=-b['numerator']*N+(1 << (En+1))
        Cn=-b['numerator']*C+(6*t+b['constant'])*(1 << En)
        tn=t+b['T']
        assert Nn%2
        v=val(Nn*r+Cn)
        if v<h:
            q=int(v-En)
            possible=[q] if q in blocks else []
            if q not in known:
                escapes.append(dict(word=word,reason='missing fixed parameter',q=q))
        else:
            minimum=max(1,h-En)
            possible=[q for q in alphabet if q>=minimum]
            escapes.append(dict(word=word,reason='unbounded valuation branch',minimum=minimum))
        for q in possible:
            answer=constrain(Nn,Cn,En,r,h,q)
            assert answer is not None
            rn,hn=answer
            newword=word+(q,)
            # Cross-check the complete projected root against the general solver.
            if max(newword)<=128 or comparisons<40:
                p=clock_projection(newword,blocks)
                assert p is not None
                mod=1 << p['anchor_bits']
                theta=((p['anchor_offset']+defect)*pow(1-p['anchor_slope'],-1,mod)) & (mod-1)
                assert not ((theta-p['theta_residue']) & ((1 << p['theta_bits'])-1))
                assert (theta,p['anchor_bits'])==(rn,hn)
                comparisons+=1
            stack.append((newword,Nn,Cn,En,tn,rn,hn))
    return dict(defect=defect,counts=dict(sorted(count.items())),longest=longest,
                escape_count=len(escapes),escapes=escapes[:30],
                projection_comparisons=comparisons)


def main():
    calendar=Calendar(64)
    selected=set(range(1,8192))
    for p in (48979,122436,244875,367354,661128,857036,954967):
        selected.update(range(p-2,p+3))
    known={q:build(calendar,q) for q in sorted(selected)}
    blocks={q:b for q,b in known.items() if b is not None}
    results=[]
    for defect in (0,1,2,-1,-2):
        result=search(blocks,known,defect)
        results.append(result)
        print(json.dumps(result),flush=True)
    output=dict(source_cutoff=64,consecutive_parameter_max=8191,
                additional_parameters=sorted(selected-set(range(1,8192))),
                productive_parameters=len(blocks),results=results,
                scope='All root-clock lifts with fixed defect, selected actual mixed-block kernels; escapes and canonical source correlation unresolved.')
    Path(__file__).with_name('root_search.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
