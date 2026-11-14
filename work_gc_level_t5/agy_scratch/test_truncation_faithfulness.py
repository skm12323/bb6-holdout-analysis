import json, sys
from pathlib import Path
ROOT = Path("D:/math_cc")
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
from rwalk import Table
import numpy as np

with open("work_gc_level_t5/levels_t5_20000000.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fams = data["families"]
parsed_fams = []
for k in fams.keys():
    parts = k.split('/')
    num = int(parts[0])
    den = int(parts[1])
    lift = int(parts[2]) == 1
    parsed_fams.append((num, den, lift))

print(f"Loaded {len(parsed_fams)} families.")

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

max_k = int(k_a.max())
print(f"Number of odd a-chains >= 64: {len(js_a)}")
print(f"Max k among odd a-chains >= 64: {max_k}")

max_val = 0
worst_fam = None
for num, den, lift in parsed_fams:
    # |3 * k * den + num|
    # Since k >= 0, den > 0:
    val1 = abs(3 * 0 * den + num)
    val2 = abs(3 * max_k * den + num)
    v = max(val1, val2)
    if v > max_val:
        max_val = v
        worst_fam = (num, den, lift)

print(f"Max |3*k*den + num| across all families: {max_val} (log2 = {np.log2(max_val):.2f})")
print(f"Worst family: {worst_fam}")
assert max_val < (1 << 53), f"Faithfulness bound violated: {max_val} >= 2^53"
print(f"TRUNCATION FAITHFULNESS VERIFIED: {max_val} < 2^53 ({1 << 53}) for ALL odd a-chains and ALL families!")
