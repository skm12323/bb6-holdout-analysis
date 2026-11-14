import json
from fractions import Fraction

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

cf4 = sig['canon_families']['<T4']

# Candidate table:
# Integer in [-16, 16] with None lift
# 4/3 with any lift
# -7/3 with None lift

cand_n = 0
bad_n = 0
bad_fams = []
cand_fams = []

for fam_key, info in cf4.items():
    v_str, lift_str = fam_key.split('|')
    n = info['n']
    
    # Check if candidate
    is_cand = False
    if lift_str == 'None':
        # Can be integer in [-16, 16] or -7/3
        try:
            val_int = int(v_str)
            if -16 <= val_int <= 16:
                is_cand = True
        except ValueError:
            if v_str == '-7/3':
                is_cand = True
    else:
        # Has lift: must be 4/3
        if v_str == '4/3':
            is_cand = True
            
    if is_cand:
        cand_n += n
        cand_fams.append((fam_key, n))
    else:
        bad_n += n
        bad_fams.append((fam_key, n))

print(f"Candidate families: {len(cand_fams)}, total count: {cand_n}")
print(f"Bad families: {len(bad_fams)}, total count: {bad_n}")
print(f"Total count cand + bad: {cand_n + bad_n}")
print("\nFirst 10 bad families:", bad_fams[:10])
print("\nCandidate families:", cand_fams)
