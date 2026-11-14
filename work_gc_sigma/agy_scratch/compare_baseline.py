import json

with open("work_claude_residual/levels_20000000.json", "r", encoding="utf-8") as f:
    lev_old = json.load(f)

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

print("Old levels keys:", list(lev_old.keys()))
print("Old sigma keys:", list(lev_old.get("sigma", {}).keys()))

print("\n--- Compare levels in old vs new ---")
for k in ['B', 'C', 'OUT', 'D']:
    old_data = lev_old.get('levels', {}).get(k, {})
    new_data = sig.get('levels', {}).get(k, {})
    match = (old_data == new_data)
    print(f"Level {k} match: {match}")
    if not match:
        print(f"  old: {old_data}")
        print(f"  new: {new_data}")

print("\n--- Compare sigma keys <=N0, <T1, <T2, <T3 ---")
for sk in ['<=N0', '<T1', '<T2', '<T3']:
    old_s = lev_old.get('sigma', {}).get(sk, {})
    new_s = sig.get('sigma', {}).get(sk, {})
    match = (old_s == new_s)
    print(f"sigma[{sk}] match: {match}")
    if not match:
        old_keys = set(old_s.keys())
        new_keys = set(new_s.keys())
        print(f"  keys diff: old - new = {old_keys - new_keys}, new - old = {new_keys - old_keys}")
        for c in old_keys & new_keys:
            if old_s[c] != new_s[c]:
                print(f"  chain {c} diff: old={old_s[c]}, new={new_s[c]}")

print("\n--- Baseline ok in sigma4 ---")
print("baseline_ok:", sig.get("baseline_ok"))
print("measurements:", sig.get("measurements"))
print("ints_witnessed:", sig.get("ints_witnessed"))
print("M_h:", sig.get("M_h"))
