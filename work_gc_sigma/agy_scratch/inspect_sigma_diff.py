import json

with open("work_claude_residual/levels_20000000.json", "r", encoding="utf-8") as f:
    lev_old = json.load(f)

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

for name, old_key, new_key in [
    ('<=N0', 'sigma_A', '<=N0'),
    ('<T1', 'sigma_B', '<T1'),
    ('<T2', 'sigma_C', '<T2'),
    ('<T3', 'sigma_D', '<T3')
]:
    old_val = lev_old.get(old_key, {})
    new_val = sig.get('sigma', {}).get(new_key, {})
    print(f"\n--- {name}: old keys = {list(old_val.keys())[:5]} ... len={len(old_val)}; new keys = {list(new_val.keys())[:5]} ... len={len(new_val)}")
    # compare keys
    k_old = set(old_val.keys())
    k_new = set(new_val.keys())
    if k_old != k_new:
        print(f"  Key diff: old - new = {k_old - k_new}, new - old = {k_new - k_old}")
    diffs = []
    for k in k_old & k_new:
        if old_val[k] != new_val[k]:
            diffs.append((k, old_val[k], new_val[k]))
    print(f"  Matching shared keys: {len(k_old & k_new) - len(diffs)} / {len(k_old & k_new)}")
    if diffs:
        print(f"  Diff count: {len(diffs)}, first 3: {diffs[:3]}")

# Let's check what generic_all_chains is
for sk in ['sigma_A', 'sigma_B', 'sigma_C', 'sigma_D']:
    if 'generic_all_chains' in lev_old.get(sk, {}):
        print(f"{sk}['generic_all_chains'] = {lev_old[sk]['generic_all_chains']}")
