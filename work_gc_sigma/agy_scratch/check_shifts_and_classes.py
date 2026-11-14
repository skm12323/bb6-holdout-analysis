import json

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

fsr = sig['fired_shift_ranges']
for k in list(fsr.keys())[:10]:
    print(f"Key: {k} -> {fsr[k]}")

fv = sig['measurements']['<T4']['fired_values']
print(f"fired_values len = {len(fv)}")
for v in ['1/3', '-5/3', '13/3', '28/9']:
    print(f"'{v}' in fired_values? {v in fv}")

# Let's see what each key in fsr represents: is k a class or a shift?
# In NOTES:
# "按 shift 记账：类 {1/3, -5/3 相关族} 给 shift 值 {-5/3, 1/3, 13/3}"
# If k is class C, shift = C - 2.
# If C = 10/3, shift = 10/3 - 2 = 4/3!
# If C = -1/3, shift = -1/3 - 2 = -7/3!
# If C = 7/3, shift = 7/3 - 2 = 1/3!
# If C = 1/3, shift = 1/3 - 2 = -5/3!
# If C = 19/3, shift = 19/3 - 2 = 13/3!
# If C = 46/9, shift = 46/9 - 2 = 28/9!
print("\n--- Shift = Class - 2 ---")
for c_str in ['10/3', '-1/3', '7/3', '1/3', '19/3', '46/9']:
    from fractions import Fraction
    c_frac = Fraction(c_str)
    s_frac = c_frac - 2
    print(f"Class {c_str} has shift {s_frac}")
