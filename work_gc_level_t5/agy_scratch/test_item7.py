import sys
from pathlib import Path
ROOT = Path("D:/math_cc")
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
from rwalk import Table
import numpy as np

T = Table()
js = np.arange(64, T.N + 1, dtype=np.int64)
n = js - 1
od = T.odd[n].astype(bool)
isa = T.typ[n] == 97
sel = od & isa

js_a = js[sel]
n_a = n[sel]
tau_a = T.tau[n_a]
k_a = tau_a // 2

# Inequality: 3 * 3^9 * k + 3^11 < 2^(j - 2)
# To avoid overflow in 2^(j - 2), note for j >= 64, 2^(j - 2) >= 2^62.
# In float / log2 or 128-bit:
lhs = 3 * (3**9) * k_a.astype(np.float64) + (3**11)
# rhs = 2^(j - 2)
# Since lhs is at most ~5.3 * 10^11 < 2^39, and j - 2 >= 62, log2(lhs) <= 39 < 62 <= j - 2
log2_lhs = np.log2(lhs)
margin = (js_a - 2) - log2_lhs

min_margin = margin.min()
worst_idx = np.argmin(margin)
worst_j = js_a[worst_idx]
worst_k = k_a[worst_idx]

print(f"Total odd a-chains tested: {len(js_a)}")
print(f"Minimum margin (in bits): {min_margin:.2f}")
print(f"Worst j={worst_j}, k={worst_k}, log2(lhs)={log2_lhs[worst_idx]:.2f}, j-2={worst_j - 2}")
assert min_margin > 0, "REG size inequality violated!"
print("REG SIZE INEQUALITY STRICTLY HOLDS FOR ALL CHAINS 64 <= j < 2*10^7!")
