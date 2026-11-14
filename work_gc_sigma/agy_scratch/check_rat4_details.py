import json

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

# Let's inspect the bad entries and bad_values in rat_<T4
rat4 = sig['invariants']['rat_<T4']
print("n_bad in JSON:", rat4['n_bad'])
print("len of bad:", len(rat4['bad']))
print("len of bad_values (unique values):", len(rat4['bad_values']))

# Check the Tier-1 fired shift ranges
tier1 = sig['fired_shift_ranges']
print("fired_shift_ranges len:", len(tier1))
print("fired_shift_ranges keys:", list(tier1.keys()))

# Check for specific values mentioned in prompt:
# Tier-1: den 3 new values {1/3, -5/3, 13/3} and den 9 28/9
for v in ['1/3', '-5/3', '13/3', '28/9']:
    print(f"Value '{v}' in fired_shift_ranges?", v in tier1)

# Check exact_structural, witnessed_core, union in int_<T4
int4 = sig['invariants']['int_<T4']
print("\nint_<T4 exact_structural:", int4['exact_structural'])
print("int_<T4 witnessed_core:", int4['witnessed_core'])
print("int_<T4 union:", int4['union'])
