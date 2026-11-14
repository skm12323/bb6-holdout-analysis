import sys, json
from pathlib import Path
ROOT = Path("D:/math_cc")
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
from rwalk import Table, bulk as rwalk_bulk, certify as rwalk_certify
from rational_certifier import certify_rational_scalar, bulk_rational, certify_family_full

T = Table()
with open("work_gc_level_t5/levels_t5_20000000.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

print("=== Part 1: Verify integer special case (den=1) vs rwalk.bulk ===")
# Test delta = 0, delta = 1, delta = -1 on j < 100000
for delta in [0, 1, -1]:
    res_our = bulk_rational(T, delta, 1, lift=False, jlo=64, jhi=100000)
    res_rwalk = rwalk_bulk(T, delta, jlo=64, jhi=100000)
    assert res_our['uncert'] == res_rwalk['uncert'], f"Uncert mismatch for delta={delta}"
    assert res_our['aout'] == res_rwalk['aout'], f"Aout mismatch for delta={delta}"
    print(f"delta={delta} matches rwalk.bulk perfectly on 64..100000!")

print("\n=== Part 2: Verify chain 5 failures ===")
# (5, 5), (5, -11), (5, -1/3), (5, -17/3)
# (5, 5): num=5, den=1, lift=0
res_5_5 = certify_rational_scalar(T, 5, 5, 1, False)
print(f"Chain 5, delta=5: ok={res_5_5['ok']}, status={res_5_5['status']}, word={res_5_5['word']}")
assert not res_5_5['ok'] and res_5_5['status'] == 'ceiling'

# (5, -11): num=-11, den=1, lift=0
res_5_m11 = certify_rational_scalar(T, 5, -11, 1, False)
print(f"Chain 5, delta=-11: ok={res_5_m11['ok']}, status={res_5_m11['status']}, word={res_5_m11['word']}")
assert not res_5_m11['ok'] and res_5_m11['status'] == 'ceiling'

# (5, -1/3): num=-1, den=3, lift=0
res_5_m13 = certify_rational_scalar(T, 5, -1, 3, False)
print(f"Chain 5, delta=-1/3: ok={res_5_m13['ok']}, status={res_5_m13['status']}, word={res_5_m13['word']}")
assert not res_5_m13['ok'] and res_5_m13['status'] == 'ceiling'

# (5, -17/3): num=-17, den=3, lift=0
res_5_m173 = certify_rational_scalar(T, 5, -17, 3, False)
print(f"Chain 5, delta=-17/3: ok={res_5_m173['ok']}, status={res_5_m173['status']}, word={res_5_m173['word']}")
assert not res_5_m173['ok'] and res_5_m173['status'] == 'ceiling'

print("\n=== Part 3: Verify chain 9 (9, (10 - 2^9)/3) passes ===")
# (10 - 2^9)/3: num=10, den=3, lift=True
res_9 = certify_rational_scalar(T, 9, 10, 3, True)
print(f"Chain 9, delta=(10-2^9)/3: ok={res_9['ok']}, status={res_9['status']}, word={res_9['word']}")
assert res_9['ok'] and res_9['status'] == 'end'

print("\n=== Part 4: Compare family status with JSON on 64..300003 ===")
# Test families: 10/3+lift, -1/3, 46/9+lift, 7/3
fams_to_test = [
    (10, 3, True, '10/3/1'),
    (-1, 3, False, '-1/3/0'),
    (46, 9, True, '46/9/1'),
    (7, 3, False, '7/3/0'),
]

for num, den, lift, key in fams_to_test:
    res = certify_family_full(T, num, den, lift, jhi=300003)
    json_status = json_data['family_status'][key]
    print(f"Family {key}:")
    print(f"  Our result:  unc_s={res['unc_s']}, unc_b={res['unc_b']}")
    print(f"  JSON status: unc_s={json_status['unc_s']}, unc_b={json_status['unc_b']}")
    assert res['unc_s'] == json_status['unc_s'], f"unc_s mismatch for {key}"
    assert res['unc_b'] == json_status['unc_b'], f"unc_b mismatch for {key}"

print("\nALL ITEM 3 TEST CHECKS PASSED SUCCESSFULLY!")
