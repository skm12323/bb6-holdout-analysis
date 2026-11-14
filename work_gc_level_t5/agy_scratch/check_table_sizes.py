import sys
from pathlib import Path
ROOT = Path("D:/math_cc")
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
from rwalk import Table
import numpy as np

T = Table()
print(f"Table loaded. N = {T.N}")
print(f"tau: min={T.tau.min()}, max={T.tau.max()}")
print(f"lam: min={T.lam.min()}, max={T.lam.max()}")
print(f"eps: min={T.eps.min()}, max={T.eps.max()}")

# Also check for j >= 64, what are tau values:
odd_idx = np.where(T.odd)[0]
odd_chains = odd_idx + 1
odd_chains_64 = odd_chains[odd_chains >= 64]
print(f"Number of odd chains >= 64: {len(odd_chains_64)}")
tau_64 = T.tau[odd_chains_64 - 1]
print(f"tau for j>=64: min={tau_64.min()}, max={tau_64.max()}")
