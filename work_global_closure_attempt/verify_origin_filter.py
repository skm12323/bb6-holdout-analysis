"""Exact phase-offset projection and independent long-word pair lifts."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import random
import sys

ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_global_clock_words','work_global_calendar'):
    sys.path.insert(0,str(ROOT/folder))
from clock_words import clock_projection, v2
from calendar_oracle import Calendar
from fast_a_words import Cylinder


def centred(r,bits):
    m=1 << bits
    return r if r<=m//2 else r-m


def phase_residue(projection):
    h=projection['theta_bits']
    mask=(1 << h)-1
    return ((1-projection['anchor_slope'])*projection['theta_residue']
            -projection['anchor_offset']) & mask,h


def main():
    calendar=Calendar(64)
    broad=json.loads(Path(__file__).with_name('a_cylinders_broad.json').read_text())
    previous=(5,367354,5,17,5,122436,5,17,5)
    words=[previous,tuple(broad['longest_free'])]
    blocks={}
    for q in set(sum((list(w) for w in words),[])) | {8,14}:
        rec=calendar.crossing(q-1)
        assert rec['kind']=='a' and rec['odd'] and rec['head_ratio']==1
        k=rec['time']//2
        blocks[q]=dict(alpha=F(1),B=F(0),d=0,G=0,k=k,T=1+2*k)
    checks=0
    rng=random.Random(20261018)
    for _ in range(500):
        word=tuple(rng.choice((5,8,14,17)) for _ in range(rng.randrange(1,6)))
        p=clock_projection(word,blocks)
        if p is None:
            continue
        r,h=phase_residue(p)
        for defect in range(-64,65):
            m=1 << p['anchor_bits']
            theta=((p['anchor_offset']+defect)*pow(1-p['anchor_slope'],-1,m)) & (m-1)
            direct=((theta-p['theta_residue']) & ((1 << h)-1))==0
            assert direct==(((defect-r) & ((1 << h)-1))==0)
            checks+=1
    records=[]
    for word in words:
        p=clock_projection(word,blocks)
        assert p is not None
        state=Cylinder()
        for q in word:
            state=state.append(q,blocks[q]['k'])
            assert state is not None
        assert state.bits==p['anchor_bits'] and state.r==p['anchor_offset']
        assert state.p & ((1 << state.bits)-1)==p['anchor_slope']
        assert (state.clock,state.clock_bits)==(p['theta_residue'],p['theta_bits'])
        r,h=phase_residue(p)
        delta=centred((r-1)&((1 << h)-1),h)
        assert delta!=0
        if word==previous:
            assert h==122439
            assert delta==-(1 << 122438)+3244676
        # Positive lift, followed by independent physical pair macro checks.
        mod=1 << p['anchor_bits']
        theta=p['theta_residue']+8*mod
        while theta%3!=2:
            theta+=1 << p['theta_bits']
        residue=(p['anchor_slope']*theta+p['anchor_offset']) & (mod-1)
        x=residue+((theta+1-residue+mod-1)//mod)*mod
        assert theta-1<x<2*theta-5
        sigma=max(word)+len(word)+4
        gap=2*max(word)+1
        pointer=sigma+gap
        H=(((1 << gap)-1) << sigma,2*theta-x-5)
        D=(1 << sigma,x-theta+1)
        margins=[]
        for q in word:
            assert v2(x)==q and x==H[1]+2*D[1]+3
            assert H[0]+D[0]==1 << pointer and H[1]+D[1]==theta-4
            assert min(H+D)>0
            coefficient=H[0]+2*D[0]
            margins.append(v2(coefficient)-q)
            assert margins[-1]>0
            k=blocks[q]['k']
            newH=((1 << (q-1))*(coefficient >> q),
                  (1 << (q-1))*(x >> q)+6*k+1)
            D=((1 << pointer)+H[0]//2,(H[1]+1)//2)
            H=newH
            pointer+=1
            x,theta=2*theta-x//2+6*k,theta+6*k+3
            assert theta-1<x<2*theta-5
        magnitude=abs(delta)
        records.append(dict(word=word,clock_bits=h,root_bits=p['anchor_bits'],
                            minimum_abs_shift_bit_length=magnitude.bit_length(),
                            minimum_abs_shift_sha256=hashlib.sha256(magnitude.to_bytes((magnitude.bit_length()+7)//8,'big')).hexdigest(),
                            fire_compatible=False,positive_pair_macro_checks=len(word),
                            productive_a_output_entries=len(word)-1,
                            minimum_margin=min(margins),following_parameter=v2(x)))
    result=dict(result='PASS',phase_projection_comparisons=checks,
                old_word_minimum_abs_shift='2^122438 - 3244676',
                records=records,review_status='unreviewed',
                scope='Exact local phase congruences and safe pair lifts; no canonical reachability or global word bound proved.')
    Path(__file__).with_name('origin_filter_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
