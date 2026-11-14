import json

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

# In sig['invariants']['rat_<T4']:
# Notice sig has bad: list of [c, r, reading, lift]
# Let's extract all (c, r) in sig['invariants']['rat_<T4']['bad']:
bad_sig = set()
for item in sig['invariants']['rat_<T4']['bad']:
    bad_sig.add((item[0], item[1]))

print("Bad in sig['invariants']['rat_<T4']['bad'] len:", len(sig['invariants']['rat_<T4']['bad']))
# Wait! In the earlier print, len(bad) was 16 because it only printed a sample or is bad_values having all of them?
# Let's check bad_values:
bad_vals = sig['invariants']['rat_<T4']['bad_values']
total_bad_in_values = sum(len(pairs) for pairs in bad_vals.values())
print("Total bad pairs in bad_values:", total_bad_in_values)

# Let's collect all (c, r) across all bad_values:
all_bad_pairs = set()
for v_str, pairs in bad_vals.items():
    for c, r in pairs:
        all_bad_pairs.add((c, r))
print("Unique bad (c, r) in bad_values:", len(all_bad_pairs))

# All (c, r) in sigma['<T4']:
all_t4_pairs = set()
for c_str, r_list in sig['sigma']['<T4'].items():
    c = int(c_str)
    for r in r_list:
        all_t4_pairs.add((c, r))
print("Total pairs in sigma['<T4']:", len(all_t4_pairs))

good_pairs = all_t4_pairs - all_bad_pairs
print("Good pairs count:", len(good_pairs))

# Let's inspect the good pairs:
print("First 20 good pairs:", sorted(list(good_pairs))[:20])
