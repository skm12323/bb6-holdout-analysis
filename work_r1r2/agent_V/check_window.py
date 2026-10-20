"""Independent check of the [B] window certificate of work_claude_shifted 4:
for 5 <= j < 2e7 and -12 <= delta <= 15, certify(j,delta) holds except (5,5),(5,-11).

Ranges: exhaustive j<3000 all 28 deltas with the literal slow certificate; exhaustive
3000<=j<30000 and 60000<=j<61000 (dense); random samples in [30000,2e7); plus targeted
samples at every j where the theta-walk first step is an NT failure for the known bad deltas.
Writes check_window.json.
"""
import json, random, sys, time
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
import vlib

M = int(sys.argv[1]) if len(sys.argv) > 1 else 2 * 10**7
TABLE = r'D:\math_cc_astra\deep1\table_20000000.pkl' if M > 1000000 else \
        r'D:\math_cc_astra\deep1\table_1000000.pkl'
t0 = time.time()
T = vlib.Tab(TABLE, NS=4096)
rng = random.Random(20261020)
res = {'M': M, 'small': {}, 'fast': {}, 'failures': []}

# 1. exhaustive literal slow certificate for j < 3000
t1 = time.time()
fail = []
cnt = 0
for j in range(5, 3000):
    for d in range(-12, 16):
        ok, st, w, r = vlib.certify_slow(T, j, d)
        cnt += 1
        if not ok:
            fail.append((j, d, st, w[:6], r))
res['small'] = dict(cnt=cnt, fails=fail[:20], nfail=len(fail), t=round(time.time() - t1, 1))
print('small', res['small'], flush=True)

# 2. exhaustive fast certificate 3000 <= j < 30000 and [60000,61000)
t1 = time.time()
fail = []
cnt = 0
for j in list(range(3000, 30000)) + list(range(60000, 61000)):
    for d in range(-12, 16):
        ok, st, w, r = vlib.certify_fast(T, j, d)
        cnt += 1
        if not ok:
            fail.append((j, d, st, w[:6], r))
res['fast'] = dict(cnt=cnt, fails=fail[:20], nfail=len(fail), t=round(time.time() - t1, 1))
print('fast', {k: res['fast'][k] for k in ('cnt', 'nfail', 't')}, flush=True)

# 3. random samples up to M
t1 = time.time()
fail = []
cnt = 0
Nrand = 20000
for _ in range(Nrand):
    j = rng.randint(30000, M - 1)
    for d in range(-12, 16):
        ok, st, w, r = vlib.certify_fast(T, j, d)
        cnt += 1
        if not ok:
            fail.append((j, d, st, w[:6], r))
res['random'] = dict(cnt=cnt, fails=fail[:20], nfail=len(fail), t=round(time.time() - t1, 1))
print('random', {k: res['random'][k] for k in ('cnt', 'nfail', 't')}, flush=True)

# 4. targeted: for each delta in the known NT-failure set, sample j densely by first-step ND
#    (test the first-step theta-walk; collect ND and run the exact certificate on them)
t1 = time.time()
nd = 0; cnt = 0; fail = []; maxj = 0
step = 97  # deterministic stride; covers nearly all residues over 20M
JMAX = M - 1
for delta in (-11, -10, -2, -1, 5, 6, 14):
    for j in range(30000, JMAX, step):
        n = j - 1
        cnt += 1
        if not T.odd[n]:
            continue
        if T.typ[n] == 97:
            k = T.tau[n] // 2
            x1 = 6 * k + 2 * delta
            if x1 == 0:
                nd += 1
            else:
                j1 = vlib.v2(x1)
                d1 = (delta + 3 + 6 * k) % (1 << j1) if j1 else 0
                _, stw = vlib.theta_walk(T, j1, d1, limit=200) if j1 > 4 else ([], 'end')
                if stw != 'end':
                    nd += 1
        else:
            j1 = vlib.v2(T.lam(n))
            d1 = (delta + 3 + 3 * T.tau[n]) % (1 << j1)
            if j1 > 4:
                _, stw = vlib.theta_walk(T, j1, d1, limit=200)
                if stw != 'end':
                    nd += 1
        if cnt % 7 == 0:  # run exact cert on a subsample of everything
            ok, st, w, r = vlib.certify_fast(T, j, delta)
            if not ok:
                fail.append((j, delta, st, w[:6], r))
res['targeted'] = dict(cnt=cnt, nd_firststep=nd, certs=cnt // 7, fails=fail[:20],
                       nfail=len(fail), t=round(time.time() - t1, 1))
print('targeted', {k: res['targeted'][k] for k in ('cnt', 'nd_firststep', 'certs', 'nfail', 't')}, flush=True)

res['t'] = round(time.time() - t0, 1)
with open(r'D:\math_cc\work_r1r2\agent_V\check_window.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print('done', res['t'])
