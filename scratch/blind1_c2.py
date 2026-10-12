# blind1_c2.py -- C2 UNIVERSAL SEQUENCE verifier (independent).
# Level-tracking stepper over the excursion E(w,v): every entry carries its
# provenance; a fire whose consumed b is a run entry of level L at run
# position rho must satisfy
#     x = 3*2^rho*U_L + 6*k + 4   with k = L's current schedule value,
#     j = v2(x) = 1 + v2(3k+2),
#     u = 3*2^{rho-j}*U_L + odd,  u >= 9,
# and (rho, j, k) must continue L's universal schedule (4,1,1),(7,4,2),...
# The (dk,dp) advance table below is MY OWN, derived numerically by
# blind1_c3.derive_table() and proved per-class by blind1_c3's symbolic
# verifier (see report).
from blind1_lib import v2, Stepper, Level

MY_TABLE = {  # j: (dk, dp)   [derived independently in blind1_c3.py]
    1: (1, 3), 2: (1, 2), 3: (2, 5), 4: (2, 4), 5: (3, 4), 6: (3, 5),
    7: (3, 4), 8: (4, 6), 9: (4, 2), 10: (5, 5), 11: (5, 4), 12: (6, 6),
    13: (6, 4), 14: (8, 5), 15: (7, 5), 16: (7, 4), 17: (8, 6), 18: (8, 3),
    19: (8, 2), 20: (9, 5), 21: (9, 4), 22: (10, 6), 23: (10, 4),
    24: (11, 4), 25: (11, 5), 26: (11, 4), 27: (12, 6), 28: (13, 3),
    29: (13, 2), 30: (14, 5),
}


def master_schedule(pmax):
    """(p, j, k) triples of the universal sequence with p <= pmax,
    from j = 1+v2(3k+2), k += dk(j), p += dp(j)."""
    out = []
    p, k = 4, 1
    while p <= pmax:
        j = 1 + v2(3 * k + 2)
        out.append((p, j, k))
        dk, dp = MY_TABLE[j]
        k += dk
        p += dp
    return out


def check_excursion(w, v, master, max_steps=None, collect_levels=False):
    """Run E(w,v); check every run-chain event. Returns dict of stats."""
    U0 = 3 * w
    A = 3 * w + 1
    queue = [[U0 << a, ('run', 0, a)] for a in range(v - 1)]
    queue.append([(U0 << (v - 1)) - 1, ('defect',)])
    st = Stepper(A, queue)
    lev0 = Level(U0, 0)
    st.levels.append(lev0)
    if max_steps is None:
        max_steps = 20 * v + 4000
    mism = []
    n_chain = 0
    n_nonchain = 0
    steps = 0
    while len(st.q) > 0:
        ev = st.step()
        steps += 1
        if steps > max_steps:
            mism.append(('RUNAWAY', steps))
            break
        if ev['kind'] == 'halt':
            mism.append(('HALT', ev['x']))
            break
        if ev['kind'] != 'fire':
            continue
        ann = ev['b'][1]
        if ann is None or ann[0] != 'run':
            n_nonchain += 1
            continue
        lev = st.levels[ann[1]]
        rho = ann[2]
        x = ev['x']
        j = ev['j']
        n_chain += 1
        # position must continue the level's schedule
        if rho != lev.next_p:
            mism.append(('POS', ann[1], rho, lev.next_p, lev.k))
            continue
        # k-form
        t = x - 3 * (lev.base << rho) - 4
        if t % 6:
            mism.append(('FORM', ann[1], rho, t % 6))
            continue
        kx = t // 6
        if kx != lev.k:
            mism.append(('KVAL', ann[1], rho, kx, lev.k))
            continue
        # j-form
        if j != 1 + v2(3 * lev.k + 2):
            mism.append(('JVAL', ann[1], rho, j, 1 + v2(3 * lev.k + 2)))
            continue
        # u-form
        u = ev['u']
        if rho - j < 1:
            mism.append(('URANGE', ann[1], rho, j))
        else:
            r = u - 3 * (lev.base << (rho - j))
            if r % 2 == 0 or r < 1 or u < 9:
                mism.append(('UFORM', ann[1], rho, j, r))
        lev.events.append((rho, j, kx))
        dk, dp = MY_TABLE[j]
        lev.k += dk
        lev.next_p += dp
    # every level's stream must be a prefix of the master
    nlev_with_events = 0
    maxdepth = 0
    for lev in st.levels:
        if lev.events:
            nlev_with_events += 1
            maxdepth = max(maxdepth, len(lev.events))
            n = len(lev.events)
            if tuple(lev.events) != tuple(master[:n]):
                # find first divergence
                for i, (a, b) in enumerate(zip(lev.events, master)):
                    if a != b:
                        mism.append(('SEQ', lev.nlev, i, a, b))
                        break
    res = {
        'steps': steps, 'chain': n_chain, 'nonchain_fires': n_nonchain,
        'levels_total': len(st.levels),
        'levels_with_events': nlev_with_events,
        'max_chain_len': maxdepth, 'mismatches': mism,
        'final_singleton_A': st.q == [] and st.A,
    }
    if collect_levels:
        res['level0_events'] = lev0.events
    return res


def main():
    WS = [1, 3, 5, 7, 2 ** 31 - 1, 10 ** 12 + 1]
    VS = [300, 1000, 2000]
    master = master_schedule(2500)
    print("master schedule length (p<=2500): %d; first 9: %s"
          % (len(master), master[:9]))
    claim_rho_j = [(4, 1), (7, 4), (11, 2), (13, 1), (16, 3), (21, 2),
                   (23, 1), (26, 6)]
    claim_k = [1, 2, 4, 5, 6, 8, 9, 10, 13]
    ok1 = [(p, j) for (p, j, k) in master[:8]] == claim_rho_j
    ok2 = [k for (p, j, k) in master[:9]] == claim_k
    print("master matches claimed (rho,j) prefix (4,1),(7,4),(11,2),(13,1),"
          "(16,3),(21,2),(23,1),(26,6): %s" % ok1)
    print("master k-prefix 1,2,4,5,6,8,9,10,13: %s" % ok2)

    total_chain = 0
    total_levels = 0
    total_mm = 0
    base0 = None
    for w in WS:
        for v in VS:
            r = check_excursion(w, v, master, collect_levels=True)
            total_chain += r['chain']
            total_levels += r['levels_with_events']
            total_mm += len(r['mismatches'])
            l0 = r['level0_events']
            if base0 is None:
                base0 = (v, l0)
            same = l0 == base0[1]
            status = "OK" if not r['mismatches'] else "MISMATCH"
            print("w=%-12d v=%4d: steps=%-6d chain-events=%-5d (top %d) "
                  "nonchain-fires=%-4d levels=%-4d maxdepth=%-3d %s "
                  "top-stream-same-as-first=%s"
                  % (w, v, r['steps'], r['chain'], len(l0),
                     r['nonchain_fires'], r['levels_with_events'],
                     r['max_chain_len'], status, same))
            for m in r['mismatches'][:4]:
                print("    MISMATCH:", m)
    print("TOTALS over 18 runs: chain events=%d, levels with events=%d, "
          "mismatches=%d" % (total_chain, total_levels, total_mm))

    # extra: one big excursion per extreme w, positions up to ~20000
    master20k = master_schedule(20000)
    for w in (1, 2 ** 31 - 1):
        r = check_excursion(w, 20000, master20k)
        print("big w=%-12d v=20000: steps=%d chain=%d (top %d) nonchain=%d "
              "levels=%d mismatches=%d  master-len=%d"
              % (w, r['steps'], r['chain'], 0, r['nonchain_fires'],
                 r['levels_with_events'], len(r['mismatches']),
                 len(master20k)))
        for m in r['mismatches'][:4]:
            print("    MISMATCH:", m)


if __name__ == '__main__':
    main()
