import json

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

# Search for 4728 in sig
def search_num(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            search_num(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            search_num(v, f"{path}[{i}]")
    elif obj == 4728:
        print(f"Found 4728 at {path}")

search_num(sig)

# Let's inspect rat_<T4> in full
r4 = sig['invariants']['rat_<T4']
print("Keys of rat_<T4>:", r4.keys())
print("n_bad:", r4['n_bad'])
print("len of bad:", len(r4['bad']))
print("bad first 5:", r4['bad'][:5])
print("len of bad_values:", len(r4['bad_values']))

# Wait, why did NOTES say:
# "Tier-2：Σ_{<T4} 的 5014 个 (链,剩余类) 中 4728 个无候选表内表示（953 个不同最小表示值）"
# Notice: 953 matches len(r4['bad_values']) == 953!
# But how many (c, r) pairs are there?
# Let's see: why did sum(len(pairs)) give 2148?
# Let's check what pairs are in bad_values!
