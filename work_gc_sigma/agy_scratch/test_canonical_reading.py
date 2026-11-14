import json
from fractions import Fraction

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

for sk in ['<=N0', '<T1', '<T2', '<T3']:
    s = sig['sigma'][sk]
    print(f"\n--- {sk} ---")
    for c in ['5', '6', '7']:
        if c in s:
            print(f"  chain {c}: {s[c]}")

# Let's inspect chain 5, 6, 7 in <T3:
# Chain 5 (M = 2^6 = 64):
# Notice: 12@5 means residue 12 mod 64.
# Is 12 = 4/3 + 2^5?
# Let's check 4/3 mod 64:
# 3 * 43 = 129 = 2 * 64 + 1 = 1 mod 64.
# So 3^(-1) mod 64 = 43.
# 4/3 = 4 * 43 = 172 = 44 mod 64.
# 4/3 + 2^5 = 44 + 32 = 76 = 12 mod 64!
# Exactly 12!

# Chain 6 (M = 2^7 = 128):
# -20@6 means residue -20 = 108 mod 128.
# Is 4/3 + 2^6 mod 128 = -20?
# 3 * 85 = 255 = 2*128 - 1 = -1 mod 128 => 3^(-1) mod 128 = 43.
# 4/3 = 4 * 43 = 172 = 44 mod 128.
# 4/3 + 2^6 = 44 + 64 = 108 = -20 mod 128!
# Exactly -20!

# Chain 7 (M = 2^8 = 256):
# 83@7 means residue 83 mod 256.
# Is -7/3 mod 256 = 83?
# 3 * 171 = 513 = 2*256 + 1 = 1 mod 256 => 3^(-1) mod 256 = 171.
# -7/3 = -7 * 171 = -1197 = -1197 + 5*256 = -1197 + 1280 = 83 mod 256!
# Exactly 83!
