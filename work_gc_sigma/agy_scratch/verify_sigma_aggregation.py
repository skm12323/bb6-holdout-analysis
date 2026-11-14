import json

with open("work_claude_residual/levels_20000000.json", "r", encoding="utf-8") as f:
    lev_old = json.load(f)

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

# In levels_20000000.json:
# sigma_A['by_chain'], sigma_B['by_chain'], sigma_C['by_chain'], sigma_D['by_chain']
# What about OUT?
# Let's check how OUT is saved in lev_old.
print("lev_old keys with OUT:", [k for k in lev_old if 'OUT' in k])
print("lev_old['OUT'].keys():", lev_old['OUT'].keys())

# Let's accumulate sigma_A, sigma_B, etc.
def get_by_chain(sk):
    bc = lev_old.get(sk, {}).get('by_chain', {})
    res = {}
    for c, lst in bc.items():
        res[c] = set(lst)
    return res

def merge_chains(*chain_dicts):
    out = {}
    all_c = set()
    for cd in chain_dicts:
        all_c.update(cd.keys())
    for c in all_c:
        s = set()
        for cd in chain_dicts:
            s.update(cd.get(c, set()))
        out[c] = sorted(s)
    return out

bc_A = get_by_chain('sigma_A')
bc_B = get_by_chain('sigma_B')
bc_C = get_by_chain('sigma_C')
bc_D = get_by_chain('sigma_D')

sig_le_N0 = bc_A
sig_lt_T1 = merge_chains(bc_A, bc_B)
sig_lt_T2 = merge_chains(bc_A, bc_B, bc_C)
# Wait, for <T3, does it include OUT?
# In levels.py, OUT was computed, but summary['sigma_OUT'] was not created in levels.py lines 144!
# Let's check!

print("\n--- Compare <=N0 ---")
match_le_N0 = (sig_le_N0 == sig['sigma']['<=N0'])
print("sig_le_N0 == sig['sigma']['<=N0']:", match_le_N0)
if not match_le_N0:
    for c in sorted(set(sig_le_N0.keys()) | set(sig['sigma']['<=N0'].keys()), key=int):
        v1 = sig_le_N0.get(c)
        v2 = sig['sigma']['<=N0'].get(c)
        if v1 != v2:
            print(f"chain {c}: lev_old={v1}, sig4={v2}")

print("\n--- Compare <T1 ---")
match_lt_T1 = (sig_lt_T1 == sig['sigma']['<T1'])
print("sig_lt_T1 == sig['sigma']['<T1']:", match_lt_T1)
if not match_lt_T1:
    for c in sorted(set(sig_lt_T1.keys()) | set(sig['sigma']['<T1'].keys()), key=int):
        v1 = sig_lt_T1.get(c)
        v2 = sig['sigma']['<T1'].get(c)
        if v1 != v2:
            print(f"chain {c}: lev_old={v1}, sig4={v2}")

print("\n--- Compare <T2 ---")
match_lt_T2 = (sig_lt_T2 == sig['sigma']['<T2'])
print("sig_lt_T2 == sig['sigma']['<T2']:", match_lt_T2)
if not match_lt_T2:
    for c in sorted(set(sig_lt_T2.keys()) | set(sig['sigma']['<T2'].keys()), key=int):
        v1 = sig_lt_T2.get(c)
        v2 = sig['sigma']['<T2'].get(c)
        if v1 != v2:
            print(f"chain {c}: lev_old={v1}, sig4={v2}")

print("\n--- Compare <T3 without OUT vs sig4 ---")
sig_lt_T3_no_out = merge_chains(bc_A, bc_B, bc_C, bc_D)
match_lt_T3 = (sig_lt_T3_no_out == sig['sigma']['<T3'])
print("sig_lt_T3_no_out == sig['sigma']['<T3']:", match_lt_T3)
if not match_lt_T3:
    diff_count = 0
    for c in sorted(set(sig_lt_T3_no_out.keys()) | set(sig['sigma']['<T3'].keys()), key=int):
        v1 = set(sig_lt_T3_no_out.get(c, []))
        v2 = set(sig['sigma']['<T3'].get(c, []))
        if v1 != v2:
            diff_count += 1
            if diff_count <= 5:
                print(f"chain {c}: in lev_old not sig4 = {v1 - v2}, in sig4 not lev_old = {v2 - v1}")
    print(f"total diff chains: {diff_count}")
