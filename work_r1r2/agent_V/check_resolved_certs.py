"""Compare my certificate on the A5 resolved classes with the accepted implementations
deep_lib.certify / shiftlib.certify, for random m < 1e6.  Uses the closed form for 3^-1 mod 2^K.
Writes check_resolved_certs.json.
"""
import json, random, sys
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
sys.path.insert(0, r'D:\math_cc_astra\deep1')
import vlib, deep_lib

def inv3(K):
    return (1 + (1 << K)) // 3 if K % 2 == 1 else (1 + (1 << (K + 1))) // 3

T = vlib.Tab(r'D:\math_cc_astra\deep1\table_1000000.pkl', NS=1024)
Tt = deep_lib.Table(r'D:\math_cc_astra\deep1\table_1000000.pkl', NS=1024)
rng = random.Random(3)
mism = []; fails = []; n = 0
for _ in range(400):
    m = rng.randint(64, 20000)
    for D in (10, 26):
        K = m + 1
        M = 1 << K
        d = ((D - (1 << m)) * inv3(K)) % M
        d = vlib.symres(d, K)
        a = vlib.certify_fast(T, m, d)
        b = deep_lib.certify(Tt, m, d)
        n += 1
        if (a[0], a[1]) != (b[0], b[1]):
            mism.append((m, D, a[:2], b[:2]))
        if not a[0]:
            fails.append((m, D, a[1], a[2][:6]))
out = dict(n=n, mismatch=len(mism), failures=len(fails), first_mismatch=mism[:3],
           first_fail=fails[:3])
with open(r'D:\math_cc\work_r1r2\agent_V\check_resolved_certs.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1)[:1000])
