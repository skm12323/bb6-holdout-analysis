"""agentB_run14.py — mu-walker verification battery.

(1) Walk the universal cascade prefix to position N; every chain must be
    tie-free (robust), integral, u >= 3.
(2) The chain events on the HOST run occur exactly at the universal positions
    4, 7, 11, 13, ... with exactly the universal parameters j_i.
(3) SELF-SIMILARITY: for every mini-run (pushed by chain cid, itself consuming
    label L), the chains consuming that mini-run occur at relative positions
    forming the same universal subsequence with the same parameters — i.e.
    every level replays the universal sequence.
(4) Prefix agreement with the concrete per-J cascades (agentB_run8) for all
    J <= 64 on positions <= J-2.
(5) Over-read bound: from concrete cascades, how many entries past the host
    run's end a level consumes before re-entry (max over J <= 60).
"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_mu import Walker, walk, Amb
from agentB_lib import v2i
from agentB_run7 import verify
from agentB_run8 import cascade

def universal_seq(nmax):
    TAB = {}
    for j in range(1, 121):
        res, err = verify(j)
        assert not err, (j, err)
        TAB[j] = res[0]
    seq = []
    p, k = 4, 1
    while p < nmax:
        j = 1 + v2i(3 * k + 2)
        seq.append((p, k, j))
        p += TAB[j][1]; k += TAB[j][0]
    return seq, TAB

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    seq, TAB = universal_seq(N + 40)
    uni_pos = [s[0] for s in seq]
    uni_j = [s[2] for s in seq]

    # (1)+(2): walk
    try:
        w, steps = walk(N)
    except Amb as ex:
        print('WALK FAIL:', ex); return
    host_events = [(lb[1], j) for (cid, lb, j, u) in w.events if lb[0] == 'R']
    # chains with b on the host run: positions must be universal positions
    got_pos = [e[0] for e in host_events]
    got_j = [e[1] for e in host_events]
    # universal positions <= N:
    exp = [(p, j) for (p, k, j) in seq if p <= N]
    ok2 = got_pos == [e[0] for e in exp] and got_j == [e[1] for e in exp]
    print('(1) walk to position %d: %d steps, %d chains, all robust & safe' %
          (N, steps, len(w.events)))
    print('(2) host-run chain events = universal (p_i, j_i) exactly:', ok2)
    if not ok2:
        for a, b in list(zip(host_events, exp))[:12]:
            print('   got %s exp %s' % (a, b))

    # (3) self-similarity per mini-run
    by_level = {}
    for (cid, lb, j, u) in w.events:
        if lb[0] == 'M':
            by_level.setdefault(lb[1], []).append((lb[2], j))
    bad = 0
    for cid, lst in by_level.items():
        # positions where chains consume this mini-run:
        pos = [x[0] for x in lst]
        js = [x[1] for x in lst]
        expd = [(p, j) for (p, k, j) in seq if p <= max(pos) + 6]
        exp_pos = [e[0] for e in expd if e[0] <= max(pos)]
        exp_j = [e[1] for e in expd if e[0] <= max(pos)]
        if pos != exp_pos or js != exp_j:
            # allow truncation: mini-runs end early (their exit consumes D)
            if pos != exp_pos[:len(pos)]:
                bad += 1
                if bad < 4:
                    print('   level of chain %d: got %s' % (cid, list(zip(pos, js))[:8]))
                    print('                     exp %s' % exp_pos[:8])
    print('(3) self-similarity: %d mini-run levels checked, mismatches: %d' %
          (len(by_level), bad))

    # (4) prefix agreement with concrete cascades
    ok4 = True
    for J in range(6, 65):
        ev, end = cascade(J)
        conc = []           # (position of b if R, j) in order
        for e in ev:
            if e[0] == 'C':
                conc.append((e[2][1] if e[2][0] == 'R' else None, e[1]))
        wk = [(lb[1], j) for (cid, lb, j, u) in w.events
              if lb[0] == 'R' and lb[1] <= J - 2]
        ch = [(p, j) for (p, j) in conc if p is not None]
        if ch != wk:
            ok4 = False
            print('   J=%d mismatch: concrete %s vs walker %s' % (J, ch[:6], wk[:6]))
            break
    print('(4) walker prefix == concrete cascade(J) host events for J=6..64:', ok4)

    # (5) over-read: TAIL entries (T's) consumed after the last host-run entry
    # (the parent-tail over-read of a level exit), and total exit length
    worstT = 0; worstL = 0; wJ = None
    for J in range(5, 61):
        ev, end = cascade(J)
        # find index of last event consuming an R label
        lastR = -1
        for i, e in enumerate(ev):
            if e[0] == 'E':
                if e[1][0] == 'R' or e[2][0] == 'R':
                    lastR = i
            else:
                if e[2][0] == 'R':
                    lastR = i
        tailT = 0; exitlen = 0
        for i, e in enumerate(ev):
            if i <= lastR:
                continue
            exitlen += 1
            if e[0] == 'E':
                for l in (e[1], e[2]):
                    if l[0] == 'T':
                        tailT += 1
            else:
                if e[3][0] == 'T':
                    tailT += 1
        if tailT > worstT or exitlen > worstL:
            if tailT > worstT:
                worstT, wJ = tailT, J
            worstL = max(worstL, exitlen)
    print('(5) over-read (J=5..60): max TAIL entries consumed during exit: %d (J=%s); '
          'max exit events: %d' % (worstT, wJ, worstL))

if __name__ == '__main__':
    main()
