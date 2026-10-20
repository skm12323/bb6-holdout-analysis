"""Cross-validate vlib (theta-walk, exact walk, certificate, beta-walk) against the accepted
implementations work_claude_shifted/shiftlib.py and work_deep/verify_deep.py's deep_lib.py on
random inputs.  Writes check_cert.json.
"""
import json, random, sys, time
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
sys.path.insert(0, r'D:\math_cc\work_claude_shifted')
sys.path.insert(0, r'D:\math_cc_astra\deep1')
import vlib
import shiftlib
import deep_lib

random.seed(20261020)
res = {}
t0 = time.time()

# ---- shiftlib tables on a small prefix (recomputed by lam_walk) ----------------------------
N = 200000
Ts = shiftlib.Tables(N, NS=1024)
Ts.N = N
DT = shiftlib.DefectTable(Ts)
res['t_shift_tables'] = round(time.time() - t0, 1)

# my table on the cached pickle restricted to N
T = vlib.Tab(r'D:\math_cc_astra\deep1\table_1000000.pkl', NS=1024)
T.N = N

# 1. theta-walk equality
mism = []
for _ in range(30000):
    j = random.randint(5, 5000)
    d = random.randint(-1000, 1000) + random.getrandbits(80) * random.choice([0, 1, -1])
    p1, s1 = vlib.theta_walk(T, j, d, limit=500)
    p2, s2 = shiftlib.dw(DT, j, d, limit=500)
    if s1 != s2 or p1 != p2:
        mism.append((j, d, p1[:5], s1, p2[:5], s2))
        if len(mism) > 5: break
res['theta_walk_mismatch'] = len(mism); res['theta_first'] = mism[:2]

# 2. exact walk equality (random states built from small j and bases)
mism = []
for _ in range(3000):
    j = random.randint(5, 200)
    u = random.getrandbits(60) | 1
    x = (1 << j) * u
    d = random.randint(-50, 50)
    th = x + d
    ceil = j + 1 + random.randint(0, 5)
    a = vlib.exact_walk(T, x, th, ceil, 200)
    b = shiftlib.exact_tail(T, x, th, ceil, 200)
    if a != b:
        mism.append((j, d, ceil, a, b))
        if len(mism) > 5: break
res['exact_walk_mismatch'] = len(mism); res['exact_first'] = mism[:2]

# 3. certificate equality
mism = []; fast_mism = []
for _ in range(20000):
    j = random.randint(5, 20000)
    delta = random.randint(-(1 << 20), 1 << 20)
    a = vlib.certify_fast(T, j, delta)
    b = shiftlib.certify(T, j, delta)
    if (a[0], a[1]) != (b[0], b[1]):
        mism.append((j, delta, a[:2], b[:2]))
        if len(mism) > 5: break
    if j <= 1200:
        c = vlib.certify_slow(T, j, delta)
        if (c[0], c[1]) != (a[0], a[1]):
            fast_mism.append((j, delta, a[:2], c[:2]))
            if len(fast_mism) > 5: break
res['cert_fast_vs_shiftlib'] = len(mism); res['cert_first'] = mism[:2]
res['cert_fast_vs_slow'] = len(fast_mism); res['cert_slow_first'] = fast_mism[:2]

# 4. beta-walk equality with shiftlib.sym_beta for random J
mism = []
for _ in range(2000):
    J = random.randint(5, N - 2)
    a, sa = vlib.beta_walk(T, J)
    b, sb = shiftlib.sym_beta(T, J, limit=200)
    # compare (j,d,beta,G) of each chain recorded in both
    aa = [(r['j'], r['d'], r['beta'], r['G'], r['typ']) for r in a]
    bb = [(r[0], r[1], r[2], r[3], r[4]) for r in b]
    ok = sa == sb and len(aa) == len(bb) and aa == bb
    if not ok:
        mism.append((J, sa, sb, aa[:4], bb[:4]))
        if len(mism) > 5: break
res['beta_walk_mismatch'] = len(mism); res['beta_first'] = mism[:2]

# 5. deep_lib certificate equality on the cached 1e6 table (independent accepted code)
Td = deep_lib.Table(r'D:\math_cc_astra\deep1\table_1000000.pkl', NS=1024)
mism = []
for _ in range(20000):
    j = random.randint(5, 900000)
    delta = random.randint(-1000, 1000) if random.random() < .5 else random.randint(-(1 << 30), 1 << 30)
    a = vlib.certify_fast(T, j, delta) if j < N else None
    if a is None: continue
    b = deep_lib.certify(Td, j, delta)
    if (a[0], a[1]) != (b[0], b[1]):
        mism.append((j, delta, a[:2], b[:2]))
        if len(mism) > 5: break
res['cert_vs_deep_lib'] = len(mism); res['deep_lib_first'] = mism[:2]

res['t_total'] = round(time.time() - t0, 1)
with open(r'D:\math_cc\work_r1r2\agent_V\check_cert.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items() if 'first' not in k}, indent=1))
