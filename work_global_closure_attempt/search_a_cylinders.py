"""Bounded exact search comparing free and true-fire pure-A words."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
for name in ('work_global_ext/route_c', 'work_global_clock_words', 'work_global_calendar'):
    sys.path.insert(0, str(ROOT/name))
from fdata import lam_walk
from clock_words import clock_projection, fire_projection
from calendar_oracle import Calendar
from fast_a_words import Cylinder, val


def main():
    mode = sys.argv[1] if len(sys.argv)>1 else 'small'
    assert mode in ('small', 'broad')
    started = time.monotonic()
    data = lam_walk(1000000)
    ks = {}
    for q in range(5, 1000000):
        if data['typ'][q-1] != 97 or not data['odd'][q-1]:
            continue
        k = data['tau'][q-1]//2
        selected = q in (5,8,14,17,27,48979,122436,367354)
        if mode == 'broad':
            selected = q<=128 or val(3*k-2)>=15 or val(k+7)>=15 or q==367354
        if selected:
            ks[q] = k
    calendar = Calendar(64)
    for q, k in ks.items():
        row = calendar.crossing(q-1)
        assert row['kind']=='a' and row['odd'] and row['time']==2*k
        assert row['epsilon']==0 and row['head_ratio']==1
    blocks = {q:dict(alpha=Fraction(1), B=Fraction(0), d=0, G=0,
                     k=k, T=1+2*k) for q,k in ks.items()}
    counts, rooted = Counter(), Counter()
    longest, longest_root = (), ()
    comparisons = 0
    attempts = 0
    capped = False
    depth = 14
    stack = [((), Cylinder())]
    last = time.monotonic()
    while stack:
        word, state = stack.pop()
        if len(word) == depth:
            capped = True
            continue
        for q,k in ks.items():
            attempts += 1
            nxt = state.append(q,k)
            newword = word+(q,)
            if mode == 'small' and (attempts % 37 == 0 or max(newword)<=128):
                old = clock_projection(newword, blocks)
                assert (nxt is None) == (old is None)
                if nxt is not None:
                    assert nxt.bits == old['anchor_bits']
                    assert nxt.p % (1 << nxt.bits) == old['anchor_slope']
                    assert nxt.r == old['anchor_offset']
                    assert (nxt.clock, nxt.clock_bits) == (old['theta_residue'], old['theta_bits'])
                    f = fire_projection(old)
                    assert (nxt.fire() is None) == (f is None)
                    if f is not None:
                        assert nxt.fire() == (f['step_residue'],f['bits'])
                comparisons += 1
            if nxt is None:
                continue
            counts[len(newword)] += 1
            if len(newword)>len(longest):
                longest = newword
            if nxt.fire() is not None:
                rooted[len(newword)] += 1
                if len(newword)>len(longest_root):
                    longest_root = newword
            stack.append((newword, nxt))
        if attempts > 2000000:
            capped = True
            break
        if time.monotonic()-last > 15:
            print('progress', attempts, dict(counts), 'longest', longest, flush=True)
            last = time.monotonic()
    if mode=='small':
        expected = {2:64,3:66,4:49,5:27,6:21,7:12,8:2,9:1}
        assert {k:v for k,v in counts.items() if k>=2} == expected
    result = dict(result='BOUNDED' if capped else 'EXHAUSTED_SELECTED_ALPHABET',
                  mode=mode, alphabet=list(ks), source_calendar_checks=len(ks),
                  depth_limit=depth, attempts=attempts, reference_comparisons=comparisons,
                  free_counts=dict(sorted(counts.items())),
                  fire_counts=dict(sorted(rooted.items())),
                  longest_free=longest, longest_fire=longest_root,
                  unresolved_stack_nodes=len(stack),
                  seconds=round(time.monotonic()-started,2),
                  scope='Pure-A words in the selected alphabet only; other parameters and mixed b/c returns remain open. Fire-compatible does not mean canonically reachable.')
    Path(__file__).with_name('a_cylinders_'+mode+'.json').write_text(
        json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    main()
