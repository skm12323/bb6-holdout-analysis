"""Layer enumeration for source histories (Claude, Part A).
For each history w (grammar of work_claude_ext_next), enumerate every way its A letters can be
non-descents ("catapults") at a small odd-a chain (j,k_j) of the canonical calendar, and compute
the minimal descent-layer count l'(w) = 1 + #descent letters (recursive; C(w') counts l'(w')).
A letter can be a non-descent only if v2(6k_j+2d) >= j-1 for the automaton value d before it.
Usage: python -B layers.py [Wmax]"""
import sys, json
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'work_claude_ext_next')); sys.path.insert(0, str(ROOT/'work_ext_roots'))
from grammar import words, show
from search_roots import Calendar
from verify_shift import v2

cal = Calendar(512)
ODD_A = [(j, cal.crossing(j-1)['time']//2) for j in range(3, 400)
         if cal.crossing(j-1)['odd'] and cal.crossing(j-1)['kind'] == 'a']
MAXJ_USED = [0]

def jbound(d):
    """Largest j at which a non-descent with value d is arithmetically possible (C1: 6k<=3(j-1)^2;
    tau(n)>=(n-1)/2: k>=(j-2)/4)."""
    r = 0; den = d.denominator
    while den % 3 == 0: den //= 3; r += 1
    h = abs(d); j = 3
    jb = int(4*h/3) + 3                       # resonance 6k+2d=0 needs k=-d/3 >= (j-2)/4
    while (3**r) * (3*(j-1)**2 + 2*h) >= 2**(j-1) or j <= jb: j += 1
    return j

import math
def Pclock(n): return 2*math.ceil(math.log2(6*n*n+5))**2 + 1345
def catapults(d):
    """All odd-a j<400 are checked with exact calendar k; beyond, CLOCK (6k<=3(j-1)P(j-1)) and
    tau(n)>=(n-1)/2 exclude non-descents (asserted)."""
    out = []; jb = jbound(d)
    r = 0; den = d.denominator
    while den % 3 == 0: den //= 3; r += 1
    assert (3**r)*(3*399*Pclock(399) + 2*abs(d)) < 2**399 and 4*abs(d)/3 + 2 < 399, ('table too short', d)
    MAXJ_USED[0] = max(MAXJ_USED[0], jb)
    for j, k in ODD_A:
        if v2(6*k + 2*d) >= j - 1:
            out.append((j, k, (9 + 6*k - d)/3))
    return out

@lru_cache(None)
def outcomes(w):
    """set of (Phi, layers) over all branches; layers = 1 + #descent letters."""
    states = {(F(1), 1, 0)}            # (d, layers, catapults); 1 = pointer layer
    for L in w:
        new = set()
        for d, l, c in states:
            if L == 'A':
                new.add((3 - d, l + 1, c))
                for j, k, dn in catapults(d):
                    new.add((dn, l, c + 1))
            elif L == 'B':
                new.add((d - 1, l + 1, c))
            else:
                for phi, lw, cw in outcomes(L[1]):
                    new.add((d + phi - 2, l + lw, c + cw))
        states = new
    return frozenset(states)

def main():
    Wmax = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    res = {}; worst = {}
    for W in range(2, Wmax + 1, 2):
        eps = W + 1; cnt = Counter(); low = []
        for w in words(W):
            oc = outcomes(w)
            minl = min(l for _, l, _ in oc); maxc = max(c for _, _, c in oc)
            cnt['min_layers=%d' % minl] += 1
            if maxc: cnt['words_with_possible_catapult'] += 1
            if minl <= 4: low.append(dict(word=show(w), min_layers=minl, max_catapults=maxc,
                                         shifts=sorted({str(p - 2) for p, l, c in oc if l == minl})[:6]))
        res[eps] = dict(words=len(words(W)), counts=dict(cnt), low_layer_words=low[:40], n_low=len(low))
        print(eps, dict(cnt), 'low(<=4):', len(low), flush=True)
    out = dict(odd_a_table=ODD_A[:12], max_j_needed=MAXJ_USED[0], by_eps=res,
               note='l\'(w)>=5 (or >=4 when no catapult) forces n+1>=T4 when omega>=N0; see NOTES.md.')
    HERE.joinpath('layers_checks.json').write_text(json.dumps(out, indent=1) + '\n', encoding='utf-8')

if __name__ == '__main__':
    main()
