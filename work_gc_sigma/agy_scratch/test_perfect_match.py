import json

with open("work_claude_residual/levels_20000000.json", "r", encoding="utf-8") as f:
    lev_old = json.load(f)

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

def get_by_chain(sk):
    bc = lev_old.get(sk, {}).get('by_chain', {})
    return {c: sorted(set(lst)) for c, lst in bc.items()}

def merge_chains(*chain_dicts):
    all_c = sorted(set().union(*(cd.keys() for cd in chain_dicts)), key=int)
    out = {}
    for c in all_c:
        s = set()
        for cd in chain_dicts:
            s.update(cd.get(c, []))
        out[c] = sorted(s)
    return out

bc_A = get_by_chain('sigma_A')
bc_B = get_by_chain('sigma_B')
bc_C = get_by_chain('sigma_C')
bc_D = get_by_chain('sigma_D')

sig_le_N0 = bc_A
sig_lt_T1 = merge_chains(bc_A, bc_B)
sig_lt_T2 = merge_chains(bc_A, bc_B, bc_C)
sig_lt_T3 = merge_chains(bc_A, bc_B, bc_C, bc_D)

print("<=N0 match:", sig_le_N0 == sig['sigma']['<=N0'])
print("<T1 match :", sig_lt_T1 == sig['sigma']['<T1'])
print("<T2 match :", sig_lt_T2 == sig['sigma']['<T2'])
print("<T3 match :", sig_lt_T3 == sig['sigma']['<T3'])
