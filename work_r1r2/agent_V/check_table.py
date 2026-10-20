"""Validate the cached crossing table against (a) my own independent pair-map implementation
(vlib.my_small_full) and (b) the accepted fdata.small_full, on a prefix; then check the internal
crossing identities on the whole cached table.  Writes check_table.json.
"""
import json, sys, time
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
sys.path.insert(0, r'D:\math_cc\work_global_ext\route_c')
import vlib
from fdata import small_full as fdata_small_full, v2 as fv2

NS = int(sys.argv[1]) if len(sys.argv) > 1 else 4096
OUT = r'D:\math_cc\work_r1r2\agent_V\check_table.json'
res = {'NS': NS}

t0 = time.time()
mine = vlib.my_small_full(NS)
res['t_my_small'] = round(time.time() - t0, 2)
t0 = time.time()
ref = fdata_small_full(NS)
res['t_fdata_small'] = round(time.time() - t0, 2)

# compare my pair walk with fdata.small_full on every recorded crossing
mism = []
for n in sorted(set(mine) | set(ref)):
    if n not in mine or n not in ref:
        mism.append((n, 'missing')); continue
    a, b = mine[n], ref[n]
    for f in ('typ', 'tau', 'eps', 'odd'):
        if a[f] != b[f]:
            mism.append((n, f, a[f], b[f]))
    if a['typ'] != 'a' and a['odd']:
        if a.get('x') != b.get('x') or a.get('omega') != b.get('omega'):
            mism.append((n, 'x/omega', a.get('x'), b.get('x')))
    if b['typ'] == 'c' and a.get('Y') != b.get('Y'):
        mism.append((n, 'Y', a.get('Y'), b.get('Y')))
res['pair_walk_mismatches'] = len(mism)
res['pair_walk_first_mismatches'] = mism[:10]
print('pair walk', NS, 'mismatches', len(mism), mism[:3])

# compare the cached table fields on the prefix
T = vlib.Tab(r'D:\math_cc_astra\deep1\table_1000000.pkl', NS=NS, small=mine)
mism2 = []
for n in range(NS):
    r = mine.get(n)
    if r is None:
        continue
    if T.typ[n] != (97 if r['typ'] == 'a' else 98 if r['typ'] == 'b' else 99):
        mism2.append((n, 'typ'))
    if T.tau[n] != r['tau']: mism2.append((n, 'tau'))
    if T.eps[n] != r['eps']: mism2.append((n, 'eps'))
    if T.odd[n] != r['odd']: mism2.append((n, 'odd'))
    if r['typ'] == 'c' and T.lY[n] != r['Y'][1]: mism2.append((n, 'lY'))
    if T.lA[n] != r['A'][1]: mism2.append((n, 'lA'))
res['cached_vs_mine_mismatches'] = len(mism2)
res['cached_vs_mine_first'] = mism2[:10]
print('cached table prefix mismatches', len(mism2), mism2[:3])

# internal identities on the WHOLE cached table (loaded once)
T20 = vlib.Tab(r'D:\math_cc_astra\deep1\table_20000000.pkl', NS=NS, small=mine)
badtau = []; badlam = []; badeps = []; bada = []; badomega = []
for n in range(T20.N):
    if not T20.odd[n]:
        continue
    ta = T20.tau[n]; ep = T20.eps[n]
    if T20.typ[n] == 97:
        if ep != 0 or (ta & 1): bada.append(n)
        if T20.lY[n] != 0: badlam.append(n)
    else:
        lam = T20.lam(n)
        if not (0 < T20.eps[n] and T20.eps[n] <= n): badeps.append(n)
        om = vlib.v2(lam)
        if not (om < n - ep): badomega.append(n)
        if T20.typ[n] == 98 and lam != 3 * ta + 4: badlam.append(n)
        if T20.typ[n] == 98 and (ta & 1): badtau.append(n)  # type-b: tau must be even (3tau+4 even)
res['n_odd'] = sum(1 for n in range(T20.N) if T20.odd[n])
res['bad_typea_eps_or_odd_tau'] = len(bada)
res['bad_b_tau_odd'] = len(badtau)
res['bad_bc_lambda'] = len(badlam)
res['bad_bc_eps'] = len(badeps)
res['bad_bc_omega_ge_v2c'] = len(badomega)
res['first_bad'] = dict(a=bada[:5], tau=badtau[:5], lam=badlam[:5], eps=badeps[:5], om=badomega[:5])
print('internal identities:', {k: res[k] for k in ('n_odd', 'bad_typea_eps_or_odd_tau',
      'bad_b_tau_odd', 'bad_bc_lambda', 'bad_bc_eps', 'bad_bc_omega_ge_v2c')})

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print('written', OUT)
