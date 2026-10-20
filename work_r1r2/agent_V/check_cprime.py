"""Verify, from my own independent pair walk (vlib.my_small_full), the crossing data used by A5:
 - X(4) is an odd type-a crossing with tau=2 (k_5=1);
 - every odd type-b crossing n < NS has c'_W = 3*2^(n-1), lambda'_W = 3*tau+4 and omega=v2(lambda');
 - every odd type-c crossing n < NS has omega < v2(c'_W) (S1);
 - the four real crossings used in check_A5.
Writes check_cprime.json.
"""
import json, sys
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
import vlib

NS = 4096
X = vlib.my_small_full(NS)
res = {'NS': NS, 'X4': {}, 'bad_b': [], 'bad_c': [], 'n_odd_b': 0, 'n_odd_c': 0,
       'real_crossings': []}
r = X[4]
res['X4'] = dict(typ=r['typ'], tau=r['tau'], odd=r['odd'])
for n, r in X.items():
    if r['typ'] == 'a' or not r['odd']:
        continue
    cx, lx = r['x']; ta = r['tau']; om = r['omega']
    if r['typ'] == 'b':
        res['n_odd_b'] += 1
        if cx != 3 * (1 << (n - 1)) or lx != 3 * ta + 4 or om != vlib.v2(lx):
            res['bad_b'].append((n, cx, lx, ta))
    else:
        res['n_odd_c'] += 1
        if not (om < vlib.v2(cx)):
            res['bad_c'].append((n, om, vlib.v2(cx)))
for n in (16, 53, 64):
    r = X[n]
    res['real_crossings'].append(dict(n=n, typ=r['typ'], tau=r['tau'], odd=r['odd'],
                                      x=r.get('x'), omega=r.get('omega')))
with open(r'D:\math_cc\work_r1r2\agent_V\check_cprime.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in res.items()}, indent=1))
