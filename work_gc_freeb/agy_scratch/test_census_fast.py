import sys, time
from collections import Counter
sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2, INF
from fractions import Fraction as F

cal = Cal()

# Precompute gj < 400
gj = [j for j in range(5, 400) if cal.k(j) is not None]
print(f"Number of odd-a chains j < 400: {len(gj)}")

# Fast check of pair counts and first step outcomes
t0 = time.time()
n_pairs = 0
n_odd_pairs = 0
n_even_pairs = 0

for j in gj:
    for m in range(j, 5000):
        n_pairs += 1
        r_m = cal.row(m - 1)
        if r_m['odd']:
            n_odd_pairs += 1
        else:
            n_even_pairs += 1

print(f"Total pairs: {n_pairs}")
print(f"Odd pairs: {n_odd_pairs}")
print(f"Even pairs: {n_even_pairs}")
print(f"Time: {time.time() - t0:.2f}s")
