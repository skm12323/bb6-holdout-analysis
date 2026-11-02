"""maxgates.py -- constructed multi-gate instances on canonical calendar data (Claude, 2026-11-02).

SYNTHETIC starts (not canonical-reachable): the start state is a free 2-adic cylinder; only the crossing data
(kinds, tau, eps, R, lambda) are canonical Calendar(512) data.
Two start families:
  G(j):    a forced true-NT-gate state at odd-a chain j:  Theta = 2^(j-2) - 3k_j + 2^(j-1) X,  x = 2^j (1+2V).
  A(y,D):  an anchor at chain y with defect class D:      x = 2^y (1+2V),  Theta = x + D + 2^(y+1) W.
The full branching tree (branch.explore, unimodular splits) is explored to cylinder depth BITS.  Per start we
record: number of leaves, Haar mass by number of true NT gates, the max number of gates, and the best walks.
Every reported best walk is concretized (lift mod 2^P) and replayed with the exact integer walk (cyc.walk);
the replay must reproduce the leaf's parameter word exactly (status PASS).
Usage: PYTHONUTF8=1 python -B work_claude_cycle/maxgates.py BITS  -> maxgates_BITS.json"""
import sys, json, time
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from branch import Cal, explore, gate_list, lift, evalf  # noqa
from cyc import walk, v2  # noqa


def replay(cal, leaf, j0, Th0, x0):
    P = leaf['bits'] + max([s[3] for s in leaf['steps']] + [j0]) + 200
    vals = lift(leaf, P)
    Th = evalf(Th0, vals); x = evalf(x0, vals)
    steps, st = walk(cal, j0, Th, x, limit=len(leaf['steps']) + 5)
    w1 = [s['jn'] for s in steps][:len(leaf['steps'])]
    w0 = [s[3] for s in leaf['steps']]
    ok = (w1 == w0) and (leaf['status'] != 'END' or (st == 'END' and len(steps) == len(leaf['steps'])))
    return ok, int(Th), int(x), steps


def gate_profile(steps):
    """per true NT gate: (j, k, m, G_after); consecutive-gate clock increments E and their valuations."""
    gl = gate_list(steps)
    return [[g[1], g[2], g[3], g[4]] for g in gl]


def run_start(cal, name, j0, Th0, x0, BITS, nbest=4):
    t = time.time()
    L = explore(cal, j0, Th0, x0, min_bits=BITS, max_leaves=2 * 10 ** 6)
    mass = Counter(); cnt = Counter(); stat = Counter()
    for l in L:
        g = len(gate_list(l['steps']))
        mass[g] += 2.0 ** -l['bits']; cnt[g] += 1; stat[l['status']] += 1
    L.sort(key=lambda l: (-len(gate_list(l['steps'])), l['bits']))
    best = []
    for l in L[:nbest]:
        ok, Th, x, steps = replay(cal, l, j0, Th0, x0)
        best.append(dict(word=[[s[0], s[1], s[3]] for s in l['steps']], status=l['status'], bits=l['bits'],
                         gates=gate_profile(l['steps']), replay=('PASS' if ok else 'FAIL'),
                         start_Theta_bits=Th.bit_length(), start_x_bits=x.bit_length()))
    return dict(name=name, j0=j0, leaves=len(L), status=dict(stat), max_gates=max(cnt),
                mass_by_gates={g: mass[g] for g in sorted(mass)}, leaves_by_gates={g: cnt[g] for g in sorted(cnt)},
                best=best, seconds=round(time.time() - t, 1))


def main():
    BITS = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    cal = Cal()
    res = []
    for j in [5, 8, 12, 14, 17, 22, 24, 27, 32, 42, 61, 152]:
        k = cal.k(j)
        Th0 = {1: F(2 ** (j - 2) - 3 * k), 'X': F(2 ** (j - 1))}
        x0 = {1: F(2 ** j), 'V': F(2 ** (j + 1))}
        r = run_start(cal, 'G(%d)' % j, j, Th0, x0, BITS)
        print(r['name'], r['leaves'], r['max_gates'], r['leaves_by_gates'], r['seconds'],
              [b['replay'] for b in r['best']], flush=True)
        res.append(r)
    for y in [19, 30, 64, 128, 200]:
        for D in [-1, 0, 1, 2, 3]:
            Th0 = {1: F(2 ** y + D), 'V': F(2 ** (y + 1)), 'W': F(2 ** (y + 1))}
            x0 = {1: F(2 ** y), 'V': F(2 ** (y + 1))}
            r = run_start(cal, 'A(%d,%d)' % (y, D), y, Th0, x0, BITS)
            print(r['name'], r['leaves'], r['max_gates'], r['leaves_by_gates'], r['seconds'],
                  [b['replay'] for b in r['best']], flush=True)
            res.append(r)
    allpass = all(b['replay'] == 'PASS' for r in res for b in r['best'])
    json.dump(dict(BITS=BITS, results=res, replay_status='PASS' if allpass else 'FAIL'),
              open(HERE / ('maxgates_%d.json' % BITS), 'w'), indent=0)
    print('replay', 'PASS' if allpass else 'FAIL')


if __name__ == '__main__':
    main()
