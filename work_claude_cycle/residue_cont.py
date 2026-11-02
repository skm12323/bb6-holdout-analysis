"""residue_cont.py -- all a-type post-gate continuations at once, with the output's label as a free residue.
(Claude, 2026-11-02.)  SYNTHETIC/uniform: covers every output chain m >= MB with X(m-1) odd a, whatever k_m is.

After a true NT gate at odd-a chain j (k = k_j) with output m and X(m-1) odd a with label K = k_m, the state at the
first landing is exactly (Lemma PG/LAND, o = 1+2X odd):
    Theta_c = 2^(j-2) o + 3(k+1) + 3 + 6K,     x_c = 2^(j-1) o + 6(k+1+K) - 2^(m-1) u'.
We take K and X as free 2-adic variables and represent the last term by a free 2^MB * W (any m >= MB+1).
The branching tree over (K, X, W) is explored to depth BITS; leaves record the number of further true NT gates.
Only walks whose valuations stay below MB are faithful (asserted: every split valuation < MB-8).
Label restrictions (K must be an actual odd-a label, density ~0.68 per residue class) can only remove leaves,
so the maximum is an upper bound for real outputs m >= MB of type a.
Writes residue_cont_JMAX_BITS.json.  PYTHONUTF8=1 python -B work_claude_cycle/residue_cont.py JMAX BITS"""
import sys, json, time
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from branch import Cal, explore, gate_list  # noqa


def main():
    JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    BITS = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    t0 = time.time()
    cal = Cal()
    gj = [j for j in range(5, JMAX) if cal.k(j) is not None]
    res = {}; overall = Counter(); best = []
    for j in gj:
        k = cal.k(j)
        MB = 4 * j + 2 * BITS + 64
        Th = {1: F(2 ** (j - 2) + 3 * (k + 1) + 3), 'X': F(2 ** (j - 1)), 'K': F(6)}
        x = {1: F(2 ** (j - 1) + 6 * (k + 1)), 'X': F(2 ** j), 'K': F(6), 'W': F(2) ** MB}
        # the landing chain is v2(x); start the walk there: explore() needs a starting chain, so we first
        # split until v2(x) is determined, by exploring from a virtual a-step.  Simplest: wrap as one step.
        L = []
        stack = [(Th, x, 0)]
        from branch import fval, fsub_expr
        while stack:
            T1, x1, b = stack.pop()
            vc, vs, var = fval(x1)
            if vc < vs:
                c = vc
                LL = explore(cal, c, T1, x1, min_bits=BITS - b, max_leaves=10 ** 5)
                for l in LL:
                    l['bits'] += b; l['c'] = c
                L.extend(LL); continue
            if b >= BITS:
                L.append(dict(status='CUT_LAND', bits=b, steps=[], c=None)); continue
            up = x1[var] / F(2) ** vs
            expr = {var: 1 / up}
            for kk, vv in x1.items():
                if kk != 1 and kk != var:
                    expr[kk] = -(vv / F(2) ** vs) / up
            T2 = fsub_expr(T1, var, expr); x2 = fsub_expr(x1, var, expr)
            for e in (0, 1):
                sub = {1: F(e), var: F(2)}
                stack.append((fsub_expr(T2, var, sub), fsub_expr(x2, var, sub), b + 1))
        h = Counter(); mass = Counter(); mx = 0
        for l in L:
            g = len(gate_list(l['steps']))
            h[(l['status'], g)] += 1; mass[g] += 2.0 ** -l['bits']; mx = max(mx, g)
            assert all(s[3] < MB - 8 for s in l['steps'])
            if g >= 2 and len(best) < 30:
                best.append(dict(j=j, c=l['c'], word=[[s[0], s[1], s[3]] for s in l['steps']], bits=l['bits']))
        res[j] = dict(k=k, leaves=len(L), max_further_gates=mx, mass={g: mass[g] for g in sorted(mass)})
        overall[mx] += 1
    out = dict(JMAX=JMAX, BITS=BITS, per_j=res, hist_max=dict(overall), examples=best,
               seconds=round(time.time() - t0, 1))
    json.dump(out, open(HERE / ('residue_cont_%d_%d.json' % (JMAX, BITS)), 'w'), indent=0)
    print(dict(overall), out['seconds'])
    for j in gj[:40]:
        print(j, res[j]['k'], res[j]['leaves'], res[j]['max_further_gates'],
              {g: '%.3g' % p for g, p in res[j]['mass'].items()})


if __name__ == '__main__':
    main()
