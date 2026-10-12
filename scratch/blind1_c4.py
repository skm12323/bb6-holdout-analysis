# blind1_c4.py -- C4 ell FORMULA verification (independent).
# ell(v) := number of top-map steps from E(w,v) until the list first
# becomes a singleton (definition validated: reproduces the claimed
# ell(1..20) = 1,1,2,2,5,4,4,6,7,8,8,10,10,15,12,12,14,15,15,16).
# Claim under test: ell(v) = 2*k_b(v) + e(v), 0 <= e <= 16, where k_b(v)
# is the universal k at the last master position p <= v-1.
from collections import deque
from blind1_lib import v2, top_step_loop, excursion_state

MY_TABLE = {  # j: (dk, dp)   [derived independently in blind1_c3.py]
    1: (1, 3), 2: (1, 2), 3: (2, 5), 4: (2, 4), 5: (3, 4), 6: (3, 5),
    7: (3, 4), 8: (4, 6), 9: (4, 2), 10: (5, 5), 11: (5, 4), 12: (6, 6),
    13: (6, 4), 14: (8, 5), 15: (7, 5), 16: (7, 4), 17: (8, 6), 18: (8, 3),
    19: (8, 2), 20: (9, 5), 21: (9, 4), 22: (10, 6), 23: (10, 4),
    24: (11, 4), 25: (11, 5), 26: (11, 4), 27: (12, 6), 28: (13, 3),
    29: (13, 2), 30: (14, 5),
}


def master_schedule(pmax):
    out = []
    p, k = 4, 1
    while p <= pmax:
        j = 1 + v2(3 * k + 2)
        out.append((p, j, k))
        dk, dp = MY_TABLE[j]
        k += dk
        p += dp
    return out


def ell_fast(w, v, cap=None):
    """Steps from E(w,v) to first singleton, via a deque stepper
    (same map; O(1) queue ops). Returns (steps, halted, A_final)."""
    U = 3 * w
    q = deque((U << a) for a in range(v - 1))
    q.append((U << (v - 1)) - 1)
    A = U + 1
    steps = 0
    cap = cap if cap is not None else 20 * v + 5000
    while q:
        steps += 1
        if steps > cap:
            raise RuntimeError("runaway")
        if A % 2 == 0:
            b = q.popleft() if q else 0
            c = q.popleft() if q else 0
            A = A + b + c + 3
        else:
            b = q.popleft() if q else 0
            c = q.popleft() if q else 0
            x = A + 2 * b + 3
            j = v2(x)
            u = x >> j
            if u == 1 and j >= 3:
                return steps, True, None
            D = c + (A + 1) // 2
            add = [(u << a) for a in range(j - 1)]
            add.append(D)
            q.extendleft(reversed(add))
            A = u + 1
    return steps, False, A


def validate_fast_vs_loop(nv=250):
    """Step-by-step agreement of the deque stepper with the audited loop."""
    import blind1_lib as bl
    bad = 0
    for v in range(1, nv + 1):
        for w in (1, 3):
            # replay with both engines step by step
            L = excursion_state(w, v)
            U = 3 * w
            q = deque((U << a) for a in range(v - 1))
            q.append((U << (v - 1)) - 1)
            A = U + 1
            steps = 0
            while len(L) > 1 and q:
                # one step both engines
                L2, hl = top_step_loop(L)
                # deque engine step
                if A % 2 == 0:
                    b = q.popleft() if q else 0
                    c = q.popleft() if q else 0
                    A2 = A + b + c + 3
                else:
                    b = q.popleft() if q else 0
                    c = q.popleft() if q else 0
                    x = A + 2 * b + 3
                    jj = v2(x)
                    uu = x >> jj
                    if uu == 1 and jj >= 3:
                        A2 = None
                    else:
                        D = c + (A + 1) // 2
                        add = [(uu << a) for a in range(jj - 1)]
                        add.append(D)
                        q.extendleft(reversed(add))
                        A2 = uu + 1
                L = L2
                A = A2
                steps += 1
                if (A is None) != hl:
                    bad += 1
                    break
                if A is not None and (A != L[0] or list(q) != list(L[1:])):
                    bad += 1
                    print("fast-vs-loop mismatch w=%d v=%d step %d" %
                          (w, v, steps))
                    break
    return bad


def main():
    bad = validate_fast_vs_loop()
    print("[C4] deque stepper vs audited loop, step-by-step, v=1..250, "
          "w in {1,3}: mismatches=%d" % bad)

    VMAX = 3000
    master = master_schedule(VMAX + 10)
    # k_b(v): k at last master position p <= v-1
    kb = {}
    mi = 0
    lastk = 0
    for v in range(1, VMAX + 1):
        while mi < len(master) and master[mi][0] <= v - 1:
            lastk = master[mi][2]
            mi += 1
        kb[v] = lastk

    es = {}
    halted = False
    for v in range(1, VMAX + 1):
        s, hl, _ = ell_fast(1, v)
        if hl:
            halted = True
            print("HALT at v=%d" % v)
            break
        es[v] = s
    claim20 = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15,
               15, 16]
    m20 = [es[v] for v in range(1, 21)] == claim20
    print("[C4] ell(1..20) matches claimed list:", m20)
    ok16 = True
    out_of_range = []
    for v in range(1, VMAX + 1):
        e = es[v] - 2 * kb[v]
        if not (0 <= e <= 16):
            ok16 = False
            out_of_range.append((v, es[v], kb[v], e))
    emax = max(es[v] - 2 * kb[v] for v in range(1, VMAX + 1))
    emin = min(es[v] - 2 * kb[v] for v in range(1, VMAX + 1))
    ecount = {}
    for v in range(1, VMAX + 1):
        ecount[es[v] - 2 * kb[v]] = ecount.get(es[v] - 2 * kb[v], 0) + 1
    print("[C4] v=1..3000 (w=1): halted=%s, all e in [0,16]: %s, "
          "e range [%d, %d]" % (halted, ok16, emin, emax))
    print("     e-value histogram:", dict(sorted(ecount.items())))
    print("     violations:", out_of_range[:5])
    print("     ell(3000)=%d k_b(3000)=%d e=%d" %
          (es[3000], kb[3000], es[3000] - 2 * kb[3000]))
    # w-independence spot check
    diffw = 0
    for v in list(range(1, 120)) + list(range(200, 3001, 97)):
        for w in (3, 5, 7, 2 ** 31 - 1):
            s, hl, _ = ell_fast(w, v)
            if hl or s != es[v]:
                diffw += 1
                print("     w-dependence! w=%d v=%d ell=%d vs %d" %
                      (w, v, s, es[v]))
    print("[C4] w-independence spot check (w in {3,5,7,2^31-1}, "
          "437 v-values): differences=%d" % diffw)


if __name__ == '__main__':
    main()
