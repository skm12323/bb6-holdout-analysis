import json

with open("work_claude_residual/levels_20000000.json", "r", encoding="utf-8") as f:
    lev_old = json.load(f)

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

for k in ['B', 'C', 'OUT', 'D']:
    print(f"\nLevel {k} in lev_old:")
    old_data = lev_old.get(k, {})
    new_data = sig.get('levels', {}).get(k, {})
    print("Match?", old_data == new_data)
    if old_data != new_data:
        print("old:", old_data)
        print("new:", new_data)

print("\nsigma comparisons:")
# In levels.py:
# sigma_A is <=N0
# sigma_B is <T1 (A + B)
# sigma_C is <T2 (A + B + C)
# sigma_D is <T3 (A + B + C + D + OUT)
# Let's check how levels.py defines sigma_A, sigma_B, sigma_C, sigma_D!
print("sigma_A == sig['sigma']['<=N0']?", lev_old.get('sigma_A') == sig.get('sigma', {}).get('<=N0'))
print("sigma_B == sig['sigma']['<T1']?", lev_old.get('sigma_B') == sig.get('sigma', {}).get('<T1'))
print("sigma_C == sig['sigma']['<T2']?", lev_old.get('sigma_C') == sig.get('sigma', {}).get('<T2'))
print("sigma_D == sig['sigma']['<T3']?", lev_old.get('sigma_D') == sig.get('sigma', {}).get('<T3'))

if lev_old.get('sigma_D') != sig.get('sigma', {}).get('<T3'):
    old_d = lev_old.get('sigma_D')
    new_d = sig.get('sigma', {}).get('<T3')
    print("sigma_D diff:")
    for chain in sorted(set(old_d.keys()) | set(new_d.keys()), key=lambda x: int(x)):
        if old_d.get(chain) != new_d.get(chain):
            print(f"  chain {chain}: old={old_d.get(chain)}, new={new_d.get(chain)}")
