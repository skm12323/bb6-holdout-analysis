import json

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

bad_vals = sig['invariants']['rat_<T4']['bad_values']
# Look at some entries of bad_vals:
for i, (k, v) in enumerate(list(bad_vals.items())[:10]):
    print(f"bad_val[{k}] (len {len(v)}): {v[:5]}")

# Wait, are there chains in sigma['<T4'] that are not in bad_values?
# How many total chains are in sigma['<T4']?
print("Chains in sigma['<T4']:", len(sig['sigma']['<T4']))
# How many total residues in sigma['<T4']?
total_res = sum(len(r_list) for r_list in sig['sigma']['<T4'].values())
print("Total residues in sigma['<T4']:", total_res)

# Why did bad_values have 2148?
# Could bad_values only include chains up to some limit (like chain <= 24, or something)?
# Let's check max chain in bad_values:
max_c_bad = max(max(c for c, r in v) for v in bad_vals.values() if v)
print("Max chain in bad_values:", max_c_bad)
# Min chain in bad_values:
min_c_bad = min(min(c for c, r in v) for v in bad_vals.values() if v)
print("Min chain in bad_values:", min_c_bad)

# Chains present in bad_values:
chains_in_bad_vals = set()
for v in bad_vals.values():
    for c, r in v:
        chains_in_bad_vals.add(c)
print("Chains present in bad_values:", sorted(chains_in_bad_vals))

# What is n_bad = 4728?
# If total_res = 5014, and n_bad = 4728:
# 5014 - 4728 = 286!
# That means 286 residues are "good", and 4728 residues are "bad"!
# But why does bad_values only have 2148 pairs?
# Does bad_values truncate chains > 24 or something?
print("Chains in sigma['<T4']:", sorted(int(c) for c in sig['sigma']['<T4'].keys()))
