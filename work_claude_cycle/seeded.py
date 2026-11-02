"""seeded.py -- deep constructed instances via the NEXT criterion (Claude, 2026-11-02).  SYNTHETIC starts.

(1) Refutation of "the next gate after a true NT gate is always at chain 5 or 8" ([B] in postgate for j<400,
    m<5000): choose odd-a chains j (gate) and m (output) with v2(k_c - k_j) = c-2 and v2(k_j+1+k_m) = c-1 for
    c = 14; the NEXT lemma predicts a determined gate at 14 with output v2(k_j+3+3k_m+2k_c).
(2) Long seeded sequences: a big gate (j, k_j = 9 mod 16) whose determined continuation lands on a 5-gate with
    output m' in C_5 = {m : X(m-1) odd a, k_m = 6 mod 16}; the 5-gate then has a FREE continuation.  We solve the
    label congruences, locate the chains with the calendar (fire half-time -> pointer), and explore the full
    branching tree from the post-gate state (j, m).  Every reported walk is replayed exactly.
Writes seeded.json.  PYTHONUTF8=1 python -B work_claude_cycle/seeded.py"""
import sys, json, time
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from branch import Cal, explore, gate_list, lift, evalf  # noqa
from cyc import walk, v2  # noqa


def chain_of_label(cal, k):
    """odd-a chain j with k_j = k, or None (fire half-time k at pointer j-1)."""
    try:
        f = cal.C.preceding_fire_by_time(2 * k)
    except ValueError:
        return None
    if f['k'] != k:
        return None
    j = f['pointer'] + 1
    return j if cal.k(j) == k else None


def first_label_in_class(cal, r, M, lo=0, tries=64):
    t = (lo - r + M - 1) // M if lo > r else 0
    for i in range(t, t + tries):
        k = r + i * M
        j = chain_of_label(cal, k)
        if j is not None:
            return k, j
    return None


def post_explore(cal, j, m, bits, max_leaves=200000):
    k = cal.k(j)
    Th = {1: F(2 ** (j - 2) + 3 * (k + 1)), 'X': F(2 ** (j - 1))}
    x = {1: F(2 ** m), 'V': F(2 ** (m + 1))}
    L = explore(cal, m, Th, x, min_bits=bits, max_leaves=max_leaves)
    return Th, x, L


def replay_post(cal, j, m, Th0, x0, leaf):
    """replay from the gate input at chain j (prepending the gate) with the exact integer walk."""
    k = cal.k(j)
    P = leaf['bits'] + max([s[3] for s in leaf['steps']] + [m]) + 64
    vals = lift(leaf, P)
    ThA = evalf(Th0, vals); xA = evalf(x0, vals)
    Th_in = ThA - 3 - 6 * k
    x_in = 2 * (2 * Th_in + 6 * k - xA)
    steps, st = walk(cal, j, Th_in, x_in, limit=len(leaf['steps']) + 5)
    w = [s['jn'] for s in steps]
    ok = w[0] == m and w[1:1 + len(leaf['steps'])] == [s[3] for s in leaf['steps']]
    gates = [(s['j'], s['k'], s['jn']) for s in steps if s['kind'] == 'a' and s['jn'] >= s['j']]
    return ok, w, gates


def main():
    t0 = time.time()
    cal = Cal()
    out = dict(refute_5_or_8=[], seeded=[])
    # (1) next gate at c=14
    kc = cal.k(14)
    found = 0
    for (c, kc) in [(14, cal.k(14))]:
        Mj = 1 << (c - 1)
        rj = (kc + (1 << (c - 2))) % Mj
        for i in range(0, 8):
            kj = rj + i * Mj
            j = chain_of_label(cal, kj)
            if j is None:
                continue
            Mm = 1 << c
            rm = ((1 << (c - 1)) - 1 - kj) % Mm
            got = first_label_in_class(cal, rm, Mm, lo=kj)
            if got is None:
                continue
            km, m = got
            pred = v2(kj + 3 + 3 * km + 2 * kc)
            Th0, x0, L = post_explore(cal, j, m, 20)
            leaf = L[0]
            ok, w, gates = replay_post(cal, j, m, Th0, x0, leaf)
            out['refute_5_or_8'].append(dict(j=j, k_j=kj, m=m, k_m=km, c=c, predicted_output=pred,
                                             det=(len(L) == 1 and L[0]['bits'] == 0), word=w, gates=gates,
                                             replay='PASS' if ok else 'FAIL'))
            print('refute', out['refute_5_or_8'][-1], flush=True)
            found += 1
            if found >= 2:
                break
    # (2) seeded long sequences: big gate j (k_j = 9 mod 16) -> determined 5-gate with output mp in C_5
    C5 = [m for m in range(17, 400) if cal.k(m) is not None and cal.k(m) % 16 == 6]
    gj = [j for j in range(20, 200) if cal.k(j) is not None and cal.k(j) % 16 == 9]
    for j in gj[:6]:
        kj = cal.k(j)
        for mp in C5:
            if mp >= j - 2:
                break
            M = 1 << (mp + 1)
            r = (((1 << mp) - kj - 5) * pow(3, -1, M)) % M        # 3k_m + k_j + 5 = 2^mp (mod 2^(mp+1))
            got = None
            for i in range(0, 4):
                km = r + i * M
                if v2(kj + 1 + km) != 4:
                    continue
                jm = chain_of_label(cal, km)
                if jm is not None and jm >= j:
                    got = (km, jm); break
            if got is None:
                continue
            km, m = got
            Th0, x0, L = post_explore(cal, j, m, 200)
            hist = Counter(len(gate_list(l['steps'])) for l in L)
            L.sort(key=lambda l: (-len(gate_list(l['steps'])), l['bits']))
            best = []
            for l in L[:3]:
                ok, w, gates = replay_post(cal, j, m, Th0, x0, l)
                best.append(dict(word=w, gates=gates, bits=l['bits'], status=l['status'],
                                 replay='PASS' if ok else 'FAIL'))
            rec = dict(j=j, k_j=kj, m=m, k_m=km, mp=mp, leaves=len(L),
                       gates_after_first_hist={g: hist[g] for g in sorted(hist)},
                       max_total_gates=1 + max(hist), best=best)
            out['seeded'].append(rec)
            print('seeded', j, kj, m, km, mp, rec['gates_after_first_hist'], [b['gates'] for b in best][:1],
                  [b['replay'] for b in best], flush=True)
            break
    out['seconds'] = round(time.time() - t0, 1)
    out['replay_status'] = 'PASS' if all(r['replay'] == 'PASS' for r in out['refute_5_or_8']) and \
        all(b['replay'] == 'PASS' for s in out['seeded'] for b in s['best']) else 'FAIL'
    json.dump(out, open(HERE / 'seeded.json', 'w'), indent=0)
    print('done', out['seconds'], out['replay_status'])


if __name__ == '__main__':
    main()
