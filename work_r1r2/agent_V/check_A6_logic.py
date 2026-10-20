"""Validate the A6 scan logic on the range where the literal slow certificate is affordable:
exact delta, exact first step, j1/d1 formulas, theta-walk NT-goodness, truncated tie resolution.
Writes check_A6_logic.json.
"""
import json, random, sys, time
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
sys.path.insert(0, r'D:\math_cc_astra\deep1')
import vlib

T = vlib.Tab(r'D:\math_cc_astra\deep1\table_1000000.pkl', NS=4096)
rng = random.Random(7)
res = {'bad_d1': [], 'bad_sc': [], 'bad_tie5': [], 'bad_slow': [], 'counts': {}}
cnt = res['counts']

def dclass(m, D):
    M = 1 << (m + 1)
    d = ((D - (1 << m)) * pow(3, -1, M)) % M
    return vlib.symres(d, m + 1)

def trunc_walk(x, th, ceiling, K=192, limit=200):
    mask = (1 << K) - 1
    G = 0; rec = -1; maxj = 0
    for _ in range(limit):
        if x & mask == 0:
            return False, 'zero', rec, maxj
        jj = vlib.v2(x & mask)
        if jj >= K - 1:
            return False, 'overflow', rec, maxj
        maxj = max(maxj, jj)
        rec = max(rec, jj + G)
        if jj + G >= ceiling:
            return False, 'ceiling', rec, maxj
        n = jj - 1
        if n < 0 or not T.odd[n]:
            return True, 'end', rec, maxj
        t_ = T.tau[n]
        if T.typ[n] == 97:
            x = (2 * th + 3 * t_ - (x >> 1)) & mask
        else:
            x = (T.cW[n] * (x >> jj) + T.lam(n)) & mask
        th = (th + 3 + 3 * t_) & mask
        G += 1 + T.eps[n]
    return False, 'limit', rec, maxj

# exhaustive m in [5, 2500]
t0 = time.time()
for m in range(5, 2501):
    for D, c in ((10, 1), (26, 17)):
        d = dclass(m, D)
        ok, st, w, r = vlib.certify_slow(T, m, d)
        cnt['slow'] = cnt.get('slow', 0) + 1
        if not ok:
            res['bad_slow'].append((m, D, st, w[:6], r)); continue
        n = m - 1
        if not T.odd[n]:
            continue
        if T.typ[n] == 97:
            k = T.tau[n] // 2
            x1 = 3 * (1 << (m - 1)) + 2 * d + 6 * k
            j1 = vlib.v2(x1)
            th1 = (d + 3 + 6 * k) % (1 << j1) if j1 > 0 else (d + 3 + 6 * k)
            want = (-c * pow(3, -1, 1 << j1)) % (1 << j1) if j1 >= 1 else 0
            if th1 != want:
                res['bad_d1'].append((m, D, j1, th1, want))
            if j1 == 5:
                ok2, st2, rec2, mj2 = trunc_walk(x1, d + 3 + 6 * k, m - 1)
                cnt['tie5'] = cnt.get('tie5', 0) + 1
                if not ok2:
                    res['bad_tie5'].append((m, D, st2, rec2, mj2))
            elif j1 >= 6:
                _, stw = vlib.theta_walk(T, j1, th1, limit=200)
                cnt['sc'] = cnt.get('sc', 0) + 1
                if stw != 'end':
                    res['bad_sc'].append((m, D, j1, th1, stw))
        else:
            j1 = vlib.v2(T.lam(n))
            th1 = d + 3 + 3 * T.tau[n]
            P = m - 1 - T.eps[n]
            ok2, st2, rec2, mj2 = trunc_walk(T.lam(n), th1, P)
            cnt['bc'] = cnt.get('bc', 0) + 1
            if not ok2:
                res['bad_tie5'].append(('bc', m, D, st2, rec2, mj2, P))
res['t_small'] = round(time.time() - t0, 1)

# random larger m with the literal slow certificate (big numbers, few samples)
t0 = time.time()
for _ in range(120):
    m = rng.randint(5000, 200000)
    D, c = rng.choice([(10, 1), (26, 17)])
    n0 = m - 1
    if T.odd[n0] and T.typ[n0] != 97:
        cnt['slow_big_skip_bc'] = cnt.get('slow_big_skip_bc', 0) + 1
        continue
    d = dclass(m, D)
    ok, st, w, r = vlib.certify_slow(T, m, d)
    cnt['slow_big'] = cnt.get('slow_big', 0) + 1
    if not ok:
        res['bad_slow'].append((m, D, st, w[:6], r)); continue
    n = m - 1
    if T.odd[n] and T.typ[n] == 97:
        k = T.tau[n] // 2
        x1 = 3 * (1 << (m - 1)) + 2 * d + 6 * k
        j1 = vlib.v2(x1)
        th1 = (d + 3 + 6 * k) % (1 << j1)
        want = (-c * pow(3, -1, 1 << j1)) % (1 << j1)
        if th1 != want:
            res['bad_d1'].append((m, D, j1, th1, want))
        if j1 >= 6:
            _, stw = vlib.theta_walk(T, j1, th1, limit=200)
            if stw != 'end':
                res['bad_sc'].append((m, D, j1, th1, stw))
res['t_big'] = round(time.time() - t0, 1)
res['counts'] = cnt
res = {k: (v[:10] if isinstance(v, list) else v) for k, v in res.items()}
with open(r'D:\math_cc\work_r1r2\agent_V\check_A6_logic.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1)[:3000])
