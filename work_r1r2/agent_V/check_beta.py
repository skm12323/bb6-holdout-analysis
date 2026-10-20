"""Beta-walk checks: r_1 < J, no EXT-tie, records non-increasing, for J < M (own walk);
and drift recurrence checks on theta-walks at the real crossing table (j >= 1000 analog).
Also the analytic first-chain inequality 6(J-1)^2+5 < 2^(J-1) for J>=10.
Writes check_beta.json.
"""
import json, random, sys, time
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
import vlib

M = 2 * 10**7
t0 = time.time()
T = vlib.Tab(r'D:\math_cc_astra\deep1\table_20000000.pkl', NS=1024)
bad_r1 = []; bad_inc = []; bad_tie = []; nmax = 0; nwalks = 0; maxlen = 0
# full scan is cheap; run over all J
for J in range(5, M):
    out, st = vlib.beta_walk(T, J, limit=100)
    nwalks += 1
    maxlen = max(maxlen, len(out))
    if st == 'TIE':
        bad_tie.append((J, out[-1])); continue
    if st not in ('end', 'nodata'):
        bad_tie.append((J, st, out[-1])); continue
    # chain 1 record
    if len(out) > 1:
        r1 = out[1]['rec']
        if not (r1 < J):
            bad_r1.append((J, r1))
    # records non-increasing from chain 1 on
    for a, b in zip(out[1:], out[2:]):
        if b['rec'] > a['rec']:
            bad_inc.append((J, a['rec'], b['rec'], a['typ'], b['typ']))
            break
    if len(bad_tie) + len(bad_r1) + len(bad_inc) > 10:
        break
res = dict(M=M, nwalks=nwalks, bad_tie=bad_tie[:5], bad_r1=bad_r1[:5],
           bad_inc=bad_inc[:5], maxlen=maxlen, t1=round(time.time() - t0, 1))
print('beta scan', {k: res[k] for k in ('nwalks', 'bad_tie', 'bad_r1', 'bad_inc', 'maxlen')},
      flush=True)

# drift recurrence on theta-walks: for random large J, follow the walk while j>=1000;
# every step there must be a or b (no c can keep j>=1000 in the table range: c lands with
# omega<=24), and theta must follow the exact recurrence.
rng = random.Random(99)
bad_drift = []; steps = 0; walks = 0
for _ in range(3000):
    J = rng.randint(10**6, 2 * 10**7)
    path, st = vlib.theta_walk(T, J, 1, limit=1000)
    walks += 1
    th = 1
    t = 0
    ok = True
    for (j, d, ch) in path:
        if j < 1000 or ch == 'e' or ch == '?':
            break
        # current chain t must carry theta th in the drift set
        if not (1 - t <= th <= t + 1):
            ok = False
            break
        if d != vlib.symres(th, j):
            ok = False
            break
        steps += 1
        if ch == 'A':
            th = 3 - th
        elif ch == 'B':
            th = th - 1
        else:  # C: a c-step; break the drift test
            break
        t += 1
    if not ok:
        bad_drift.append((J, t, th, path[:8]))
        if len(bad_drift) > 5:
            break
res.update(drift_walks=walks, drift_steps=steps, bad_drift=bad_drift[:5])

# first-chain analytic inequality 6(J-1)^2+5 < 2^(J-1) for all J>=10 (sample + monotone ratio)
badJ = []
for J in list(range(10, 5000)) + [10**4, 10**5, 10**6, 10**7, 2 * 10**7, 10**8, 10**100]:
    x = 6 * (J - 1) ** 2 + 5
    if x.bit_length() > J - 1:
        badJ.append(J)
res['bad_first_chain_ineq'] = badJ[:5]

# A5 size inequality: 3*kappa(j)+25 < 2^(j-3) for j>=N0 (bit-length form)
N0 = 2 * 10**7
def P2(n):
    v = 6 * n * n + 5; g = (v - 1).bit_length()
    if (1 << g) < v: g += 1
    return 2 * g * g + 1345
def kappa(j): return (3 * (j - 1) * P2(j - 1)) // 2
badm = []
for j in [N0, N0 + 1, 10**8, 10**9, 10**12, 10**100]:
    x = 3 * kappa(j) + 25
    if x.bit_length() > j - 3:
        badm.append((j, x.bit_length()))
res['bad_A5_a_size'] = badm[:5]
res['t'] = round(time.time() - t0, 1)
with open(r'D:\math_cc\work_r1r2\agent_V\check_beta.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in res.items()}, indent=1))
