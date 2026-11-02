"""verify_3g.py -- exact check of the three-gate identity (3G) and the j-train orbit law (JT) on constructed
(SYNTHETIC-start) multi-gate walks.

Notation (NOTES.md section 3.6).  Gate i at chain g_i (k_i = k_{g_i}) with input phase Theta_i and output
y_i (v2 y_i = m_i).  The path from the output to the next gate input is affine:
    x_{g_{i+1}} = alpha_i y_i + beta_i Theta_i + gamma_i,   Theta_{i+1} = Theta_i + delta_i.
Put a_i = 2 - beta_i/2, c_i = 2 delta_i + 6 k_{i+1} - gamma_i/2.  Then exactly
    y_{i+1} + (alpha_i/2) y_i = a_i Theta_i + c_i                                         (2G)
    a_i y_{i+2} + (a_i alpha_{i+1}/2 - a_{i+1}) y_{i+1} - (a_{i+1} alpha_i/2) y_i = K_i,
    K_i = a_i a_{i+1} delta_i + a_i c_{i+1} - a_{i+1} c_i                                  (3G)
For a direct-return all-a j-train (g_i = j, one a-step m_i -> j):
    4 y_{i+2} - 5 y_{i+1} + y_i = 12 (2 + 2k_j - k_{m_i} + 3 k_{m_{i+1}})                     (JT)
Writes verify_3g.json.  PYTHONUTF8=1 python -B work_claude_cycle/verify_3g.py [BITS]"""
import sys, json, time
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from branch import Cal, explore, gate_list, lift, evalf  # noqa
from cyc import walk, v2  # noqa


def path_coeffs(cal, steps, a, b, k_a):
    """affine coefficients of the path from the output of gate a to the input of gate b (indices in steps)."""
    # state after gate a: x = y (coefficient form in (y, Theta_a)), Theta = Theta_a + 3 + 6k_a
    al, be, ga = F(1), F(0), F(0)            # x = al*y + be*Theta_a + ga
    dl = F(3 + 6 * k_a)                       # Theta = Theta_a + dl
    for t in range(a + 1, b):
        s = steps[t]
        r = cal.row(s['j'] - 1)
        if s['kind'] == 'a':
            k = s['k']
            al, be, ga = -al / 2, 2 - be / 2, 2 * dl + 6 * k - ga / 2
            dl = dl + 3 + 6 * k
        else:
            al, be, ga = al * r['R'], be * r['R'], ga * r['R'] + r['lam']
            dl = dl + 3 + 3 * r['tau']
    return al, be, ga, dl


def main():
    BITS = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    t0 = time.time()
    cal = Cal()
    cnt = Counter(); fails = []; examples = []
    for j in [5, 8]:
        k = cal.k(j)
        Th0 = {1: F(2 ** (j - 2) - 3 * k), 'X': F(2 ** (j - 1))}
        x0 = {1: F(2 ** j), 'V': F(2 ** (j + 1))}
        L = explore(cal, j, Th0, x0, min_bits=BITS, max_leaves=10 ** 6)
        for l in L:
            if l['status'] != 'END' or len(gate_list(l['steps'])) < 2:
                continue
            P = l['bits'] + max(s[3] for s in l['steps']) + 64
            vals = lift(l, P)
            steps, st = walk(cal, j, evalf(Th0, vals), evalf(x0, vals), limit=1000)
            states = []; jj, Th, x = j, evalf(Th0, vals), evalf(x0, vals)
            for s in steps:
                states.append((jj, Th, x)); jj, Th, x = s['jn'], s['Th'], s['x']
            G = [i for i, s in enumerate(steps) if s['kind'] == 'a' and s['jn'] >= s['j']]
            Y = {i: steps[i]['x'] for i in G}
            TH = {i: states[i][1] for i in G}
            KK = {i: steps[i]['k'] for i in G}
            co = {}
            for a, b in zip(G, G[1:]):
                al, be, ga, dl = path_coeffs(cal, steps, a, b, KK[a])
                # check the affine path reproduces the actual next gate input
                ok = (al * Y[a] + be * TH[a] + ga == states[b][2]) and (TH[a] + dl == TH[b])
                cnt['path'] += 1
                if not ok:
                    cnt['path_FAIL'] += 1
                aa = 2 - be / 2; cc = 2 * dl + 6 * KK[b] - ga / 2
                co[a] = (al, aa, cc, dl, b)
                lhs = Y[b] + al / 2 * Y[a]; rhs = aa * TH[a] + cc
                cnt['2G'] += 1
                if lhs != rhs:
                    cnt['2G_FAIL'] += 1
            for a, b, c in zip(G, G[1:], G[2:]):
                al0, a0, c0, d0, _ = co[a]; al1, a1, c1, d1, _ = co[b]
                K = a0 * a1 * d0 + a0 * c1 - a1 * c0
                lhs = a0 * Y[c] + (a0 * al1 / 2 - a1) * Y[b] - (a1 * al0 / 2) * Y[a]
                cnt['3G'] += 1
                if lhs != K:
                    cnt['3G_FAIL'] += 1
                    if len(fails) < 10:
                        fails.append(('3G', [steps[i]['j'] for i in (a, b, c)]))
                # valuation consequence
                vals3 = [v2(a0) + v2(Y[c]), v2(a0 * al1 / 2 - a1) + v2(Y[b]), v2(a1 * al0 / 2) + v2(Y[a])]
                cnt['3G_val'] += 1
                if K != 0 and v2(K) < min(vals3):
                    cnt['3G_val_FAIL'] += 1
                if K == 0:
                    cnt['3G_K_zero'] += 1
                # JT for direct-return all-a j-trains
                gj = steps[a]['j']
                if steps[b]['j'] == gj and steps[c]['j'] == gj and b == a + 2 and c == b + 2 and \
                        steps[a + 1]['kind'] == 'a' and steps[b + 1]['kind'] == 'a':
                    kj = KK[a]; km0 = steps[a + 1]['k']; km1 = steps[b + 1]['k']
                    cnt['JT'] += 1
                    if 4 * Y[c] - 5 * Y[b] + Y[a] != 12 * (2 + 2 * kj - km0 + 3 * km1):
                        cnt['JT_FAIL'] += 1
                    if len(examples) < 8:
                        examples.append(dict(j=gj, labels=[steps[i]['jn'] for i in (a, b, c)], k_m=[km0, km1],
                                             K=int(2 + 2 * kj - km0 + 3 * km1)))
                if len(examples) < 16 and not (steps[b]['j'] == gj and steps[c]['j'] == gj):
                    examples.append(dict(gates=[(steps[i]['j'], steps[i]['jn']) for i in (a, b, c)],
                                         K=str(K), vK=v2(K) if K else None, vals=vals3))
    res = dict(counts=dict(cnt), fails=fails, examples=examples, BITS=BITS, seconds=round(time.time() - t0, 1),
               status='PASS' if not any(kk.endswith('_FAIL') for kk in cnt) else 'FAIL')
    print(res)
    json.dump(res, open(HERE / 'verify_3g.json', 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
