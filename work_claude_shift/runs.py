"""Longest run of consecutive catapult letters (flattened, top level) over histories; certified automaton."""
import sys
from fractions import Fraction as F
from layers import catapults, outcomes, words, show
from collections import Counter
def runs(w):
    best = 0
    states = {(F(1), 0)}
    for L in w:
        new = set()
        for d, run in states:
            if L == 'A':
                new.add((3 - d, 0))
                for j, k, dn in catapults(d): new.add((dn, run + 1))
            elif L == 'B': new.add((d - 1, 0))
            else:
                for phi, lw, cw in outcomes(L[1]): new.add((d + phi - 2, 0))
        states = new
        best = max([best] + [r for _, r in states])
    return best
W = int(sys.argv[1]); c = Counter(); ex = {}
for w in words(W):
    r = runs(w); c[r] += 1; ex.setdefault(r, show(w))
print(W + 1, dict(c), ex)
