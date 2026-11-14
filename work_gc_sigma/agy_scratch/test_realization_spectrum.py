import sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path("work_claude_residual").resolve()))
import rwalk as R

t0 = time.time()
print("Loading Table...")
T = R.Table()
print(f"Table loaded in {time.time() - t0:.2f} s")

t1 = time.time()
n = np.arange(4, T.N)
# odd c-crossings: T.odd[n] == 1 and T.typ[n] == 99 (ord('c') == 99)
mask = (T.odd[n] == 1) & (T.typ[n] == 99)
n_c = n[mask]
print(f"Total odd c-crossings: {len(n_c)}")

lam = T.lam[n_c]
# om = v2(lam)
om = np.rint(np.log2((lam & -lam).astype(np.float64))).astype(np.int64)
mod = np.int64(1) << (om + 1)
s = np.mod(-1 - T.lY[n_c], mod)

# Symmetrize s into [-2^om, 2^om)
s_sym = np.where(s > (mod // 2), s - mod, s)

# Build contingency table of (om, s_sym)
unique_pairs, counts = np.unique(np.column_stack((om, s_sym)), axis=0, return_counts=True)

table_res = {}
for (w, s_val), count in zip(unique_pairs, counts):
    table_res[(int(w), int(s_val))] = int(count)

print("Contingency table of (omega, s_sym):")
for k, v in sorted(table_res.items()):
    print(f"  (omega={k[0]}, s={k[1]}): {v}")

print(f"Total counted: {sum(counts)}")
print(f"Time taken: {time.time() - t1:.2f} s")

# Check realized_ge5
ge5_shifts = {s_val for (w, s_val), count in table_res.items() if w >= 5}
print(f"Realized shifts for omega >= 5: {ge5_shifts}")
