"""postgate.py -- post-gate continuation sets C_j (Claude, 2026-11-02).

Lemma PG (NOTES.md section 2): after a true NT gate at an odd-a chain j (k=k_j) with output m, every real walk has
    Theta = 2^(j-2) + 3(k+1)  (mod 2^(j-1)),     x = 2^m * odd.
The generic post-gate start is therefore  Theta = 2^(j-2)+3(k+1) + 2^(j-1) X,  x = 2^m (1+2V)  with X, V free.
For every canonical odd-a chain j < JMAX and every m in [j, MMAX) we run the exact branching walk (branch.py),
stopping at the next true NT gate.  Output per (j,m): Haar mass of END / next GATE / CUT, and whether the
continuation is fully determined (single leaf, no split).  A determined END leaf with no gate is a statement about
EVERY real walk through such a gate (no Haar model involved).
Usage: PYTHONUTF8=1 python -B work_claude_cycle/postgate.py JMAX MMAX BITS
Writes postgate_JMAX_MMAX.json."""
import sys, json, time
from fractions import Fraction as F
from collections import Counter, defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from branch import Cal, explore  # noqa


def post_start(j, k, m):
    Th = {1: F(2 ** (j - 2) + 3 * (k + 1)), 'X': F(2 ** (j - 1))}
    x = {1: F(2 ** m), 'V': F(2 ** (m + 1))}
    return Th, x


def main():
    JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    MMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    BITS = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    t0 = time.time()
    cal = Cal()
    gj = [j for j in range(5, JMAX) if cal.k(j) is not None]
    summary = Counter()
    cont = []          # pairs with positive next-gate mass
    first_kind = Counter()
    pgate_by_j = defaultdict(float)   # sum_m 2^-(m-j+1) * P(next gate | j,m)
    det_end_nogate = 0
    next_chain_kind = Counter(); next_chain_val = Counter()
    for j in gj:
        k = cal.k(j)
        for m in range(j, MMAX):
            Th, x = post_start(j, k, m)
            L = explore(cal, m, Th, x, min_bits=BITS, stop_at_gate=True)
            mass = Counter()
            for l in L:
                mass[l['status']] += 2.0 ** -l['bits']
            det = (len(L) == 1 and L[0]['bits'] == 0)
            if det and L[0]['status'] == 'END':
                det_end_nogate += 1
            summary[('det' if det else 'split',) + tuple(sorted(mass))] += 1
            g = mass.get('GATE', 0.0)
            pgate_by_j[j] += 2.0 ** -(m - j + 1) * g
            if g > 0:
                r = cal.row(m - 1)
                nxt = Counter()
                for l in L:
                    if l['status'] == 'GATE':
                        st = l['steps'][-1]
                        nxt[(st[0], st[3])] += 2.0 ** -l['bits']
                top = sorted(nxt.items(), key=lambda t: -t[1])[:6]
                for (gc, gm), p in nxt.items():
                    next_chain_kind['j' if gc == j else ('m' if gc == m else ('below_j' if gc < j else 'other'))] += 1
                    next_chain_val[gc if gc < 50 else 'm' if gc == m else '>=50'] += 1
                cont.append(dict(j=j, k=k, m=m, kind_m=r['kind'], k_m=(r['tau'] // 2 if r['kind'] == 'a' else None),
                                 tau_m=r['tau'], omega_m=r['omega'], det=det, P_gate=g,
                                 P_end=mass.get('END', 0.0), P_cut=mass.get('CUT_BITS', 0.0) + mass.get('CUT_STEPS', 0.0),
                                 next_top=[[a, b, p] for (a, b), p in top],
                                 path=[list(s[:4]) for s in L[0]['steps']] if det else None))
                first_kind[(j, r['kind'])] += 1
    out = dict(JMAX=JMAX, MMAX=MMAX, BITS=BITS, gate_chains=gj, n_pairs=sum(summary.values()),
               det_end_nogate=det_end_nogate,
               summary={'|'.join(k): v for k, v in summary.items()},
               n_cont=len(cont), next_gate_leaf_kinds=dict(next_chain_kind),
               next_gate_leaf_chains={str(kk): v for kk, v in next_chain_val.items()}, cont_by_j=dict(Counter(c['j'] for c in cont)),
               cont_first_kind={'%d%s' % kk: v for kk, v in first_kind.items()},
               P_next_gate_weighted={j: pgate_by_j[j] for j in gj if pgate_by_j[j] > 0},
               cont=cont, seconds=round(time.time() - t0, 1))
    json.dump(out, open(HERE / ('postgate_%d_%d.json' % (JMAX, MMAX)), 'w'), indent=0)
    print({kk: out[kk] for kk in ('n_pairs', 'det_end_nogate', 'summary', 'n_cont', 'next_gate_leaf_kinds',
                                  'next_gate_leaf_chains', 'cont_by_j', 'cont_first_kind',
                                  'P_next_gate_weighted', 'seconds')})


if __name__ == '__main__':
    main()
