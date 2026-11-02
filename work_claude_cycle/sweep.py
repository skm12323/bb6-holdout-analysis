"""sweep.py -- gate-count sweep over ALL forced-gate starts G(j), j odd-a < JMAX (Claude, 2026-11-02).

G(j): Theta = 2^(j-2) - 3k_j + 2^(j-1) X, x = 2^j (1+2V), X, V free.  Every exact walk on canonical calendar data
whose first true NT gate is at chain j lies in G(j) (gate condition v2(Theta+3k)=j-2, x=2^j*odd).
The branching tree is explored to cylinder depth BITS.  Leaves are END (fully resolved), or CUT (unresolved at
depth BITS: total Haar mass <= #CUT * 2^-BITS).  Reported: max number of true NT gates over END leaves and over
all leaves, gate-count histogram, total CUT mass, and the walks attaining the maximum (replayed exactly).
Usage: PYTHONUTF8=1 python -B work_claude_cycle/sweep.py JMAX BITS -> sweep_JMAX_BITS.json"""
import sys, json, time
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from branch import Cal, explore, gate_list  # noqa
from maxgates import replay  # noqa


def main():
    JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    BITS = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    t0 = time.time()
    cal = Cal()
    gj = [j for j in range(5, JMAX) if cal.k(j) is not None]
    hist = Counter(); cutmass = 0.0; ncut = 0; maxg = 0; best = []; per_j = {}
    for j in gj:
        k = cal.k(j)
        Th0 = {1: F(2 ** (j - 2) - 3 * k), 'X': F(2 ** (j - 1))}
        x0 = {1: F(2 ** j), 'V': F(2 ** (j + 1))}
        L = explore(cal, j, Th0, x0, min_bits=BITS, max_leaves=5 * 10 ** 6)
        mj = 0
        for l in L:
            g = len(gate_list(l['steps']))
            hist[(l['status'], g)] += 1
            if l['status'] != 'END':
                cutmass += 2.0 ** -l['bits']; ncut += 1
            mj = max(mj, g)
            if g > maxg:
                maxg = g; best = []
            if g == maxg and len(best) < 12:
                ok, _, _, _ = replay(cal, l, j, Th0, x0)
                best.append(dict(j=j, word=[[s[0], s[1], s[3]] for s in l['steps']], status=l['status'],
                                 bits=l['bits'], replay='PASS' if ok else 'FAIL'))
        per_j[j] = dict(leaves=len(L), max_gates=mj)
    out = dict(JMAX=JMAX, BITS=BITS, n_starts=len(gj), max_gates=maxg,
               hist={'%s|%d' % kk: v for kk, v in sorted(hist.items())}, n_cut=ncut, cut_mass_upper=cutmass,
               per_j_max={j: v['max_gates'] for j, v in per_j.items()}, best=best,
               replay_status='PASS' if all(b['replay'] == 'PASS' for b in best) else 'FAIL',
               seconds=round(time.time() - t0, 1))
    json.dump(out, open(HERE / ('sweep_%d_%d.json' % (JMAX, BITS)), 'w'), indent=0)
    print({kk: out[kk] for kk in ('n_starts', 'max_gates', 'hist', 'n_cut', 'cut_mass_upper', 'replay_status',
                                  'seconds')})
    print(Counter(out['per_j_max'].values()))


if __name__ == '__main__':
    main()
