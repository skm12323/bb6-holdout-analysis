import json, sys
from pathlib import Path
ROOT = Path("D:/math_cc")
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
from rwalk import Table, bulk

with open("work_claude_residual/levels_20000000.json", "r", encoding="utf-8") as f:
    t4_data = json.load(f)

with open("work_gc_level_t5/levels_t5_20000000.json", "r", encoding="utf-8") as f:
    t5_data = json.load(f)

levels = ["B", "C", "OUT", "D", "C7"]
all_match = True
for lvl in levels:
    d4 = t4_data[lvl]
    d5 = t5_data[lvl]
    if d4 != d5:
        print(f"Level {lvl} mismatch!")
        all_match = False
    else:
        print(f"Level {lvl}: exact field-by-field match with levels_20000000.json!")

assert all_match, "T4 reproduction mismatch!"

# Independent replay with rwalk:
T = Table()
print("\nReplaying bulk for delta=5 with rwalk:")
res_5 = bulk(T, 5, jlo=5, jhi=100000) # test 5..100000
print(f"delta=5 on 5..100000: uncert={res_5['uncert']}")
assert res_5['uncert'] == [5], f"Expected uncert=[5], got {res_5['uncert']}"

print("Replaying bulk for delta=-11 with rwalk:")
res_m11 = bulk(T, -11, jlo=5, jhi=100000)
print(f"delta=-11 on 5..100000: uncert={res_m11['uncert']}")
assert res_m11['uncert'] == [5], f"Expected uncert=[5], got {res_m11['uncert']}"

print("\nITEM 6 ALL CHECKS PASSED!")
