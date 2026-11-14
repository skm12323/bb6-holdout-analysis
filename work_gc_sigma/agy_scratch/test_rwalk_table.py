import sys
from pathlib import Path
sys.path.insert(0, str(Path("work_claude_residual").resolve()))
import rwalk as R

print("Loading Table...")
T = R.Table()
print(f"Table loaded: N = {T.N}")

# Let's inspect what fields are in T
print("Fields in T:", [attr for attr in dir(T) if not attr.startswith('_')])

# We want odd c-crossings:
# In check_r0.py or heights: how is odd c-crossing defined?
# Let's see: for each n < T.N, check if it's odd c-crossing
# What are the arrays in Table?
print("Shape of arrays in T:")
for attr in ['t', 'm', 'c', 'u', 'l', 'w']:
    if hasattr(T, attr):
        arr = getattr(T, attr)
        print(f"  T.{attr}: len={len(arr)}, type={type(arr)}")
