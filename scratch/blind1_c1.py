# blind1_c1.py -- C1 STEP CLOSED FORM, independent verification.
#
# Derivation (mine, from the audited loop of RULES.md section 5):
#   A odd, x = A+2b+3 = 2^j*u (u odd).  m0 = b+(A-3)/2 = x/2-3 = 2^{j-1}u-3.
#   Loop: m <- (m-3)/2, push (m+3)/2 in front.  By induction
#   m_t = 2^{j-1-t}*u - 3 and the t-th push emits 2^{j-2-t}*u
#   (values 2^{j-2}u, 2^{j-3}u, ..., u, so the queue ends up
#   u, 2u, ..., 2^{j-2}u).  The loop runs while m odd and m>=3:
#     j = 1:      m0 = u-3 even, 0 iters, m = u-3 (even, <>1)  -> no halt,
#                 successor (u+1; D, S).
#     j >= 2, u >= 3: m_t odd for t < j-1 and m_{j-2} = 2u-3 >= 3, so
#                 exactly j-1 iters, m_final = u-3 even >= 0 <> 1 -> no halt,
#                 successor (u+1; u,2u,...,2^{j-2}u, D, S).
#     j >= 3, u = 1:  m_t = 2^{j-1-t}-3; iters while 2^{j-1-t} >= 6, i.e.
#                 t = 0..j-4, ending at m = 1 -> HALT.
#     j = 2, u = 1 (x = 4): m0 = -1 odd but < 3 -> no iters, m = -1 <> 1
#                 -> NO halt, successor (3; D, S)  [exception to the formula;
#                 x = 4 needs A+2b = 1, impossible with A>=3 odd, b>=0].
#   x = 2 (j=1, u=1) similarly needs b < 0; formula successor still exact.
#   On the top-map domain (A odd >= 3, b >= 0) one has x = A+2b+3 >= 6,
#   so "HALT iff u = 1" is exact there.
#
# Verifications below:
#   (a) 10^5 orbit steps from (3): loop implementation vs closed form.
#   (b) 10^4 random states (A odd): loop vs closed form (1 step).
#   (c) crafted halting / non-halting states, incl. off-domain boundary.
import random
from blind1_lib import top_step_loop, v2


def closed_step(L):
    """Exact closed form of one top-map step for A odd, x >= 2.
    Returns (L', halted).  Handles the (u,j)=(1,2) exception exactly."""
    A = L[0]
    rest = L[1:]
    if len(rest) >= 2:
        b, c = rest[0], rest[1]
        S = rest[2:]
    elif len(rest) == 1:
        b, c, S = rest[0], 0, []
    else:
        b, c, S = 0, 0, []
    x = A + 2 * b + 3
    assert x >= 2
    j = v2(x)
    u = x >> j
    D = c + (A + 1) // 2
    if u == 1 and j >= 3:
        return None, True
    if u == 1 and j == 2:          # x = 4: m stays -1
        return (3, ) + ((D, ) + tuple(S)), False
    return (u + 1, ) + tuple(u << a for a in range(j - 1)) + (D, ) \
        + tuple(S), False


def main():
    random.seed(20261013)
    # ---------------- (a) 10^5 orbit steps ----------------
    L = (3, )
    n = 0
    fires = 0
    closed_mism = 0
    sum_bad = 0
    while n < 100000:
        if L[0] % 2 == 1:
            fires += 1
            Lc, hc = closed_step(L)
            Ll, hl = top_step_loop(L)
            if (Ll, hl) != (Lc, hc):
                closed_mism += 1
                if closed_mism <= 3:
                    print("ORBIT MISMATCH at n=%d: loop=%r closed=%r  L=%r"
                          % (n, (Ll, hl), (Lc, hc), L))
            if hl:
                print("ORBIT HALTS at n=%d" % n)
                break
            L = Ll
        else:
            L, _ = top_step_loop(L)
        n += 1
        if sum(L) != 3 * n + 3:
            sum_bad += 1
    print("[C1a] orbit: %d steps, %d fires, loop-vs-closed mismatches=%d, "
          "sum(3n+3) violations=%d, halted=%s"
          % (n, fires, closed_mism, sum_bad, L is None))

    # ---------------- (b) 10^4 random states ----------------
    mism = 0
    halts_seen = 0
    minx = None
    for t in range(10000):
        ln = random.randint(1, 12)
        if t % 5 == 0:
            A = 2 * random.randint(1, 90) + 1   # up to ~2^7
            entries = [random.randint(0, 10 ** 6) for _ in range(ln - 1)]
        elif t % 5 == 1:
            A = 2 * random.getrandbits(190) + 1
            entries = [random.getrandbits(random.randint(1, 200))
                       for _ in range(ln - 1)]
        else:
            A = 2 * random.randint(1, 5000) + 1
            entries = [random.randint(0, 3000) for _ in range(ln - 1)]
        L = (A, ) + tuple(entries)
        x = A + 2 * (entries[0] if entries else 0) + 3
        minx = x if minx is None else min(minx, x)
        Ll, hl = top_step_loop(L)
        Lc, hc = closed_step(L)
        if hl:
            halts_seen += 1
        if (Ll, hl) != (Lc, hc):
            mism += 1
            if mism <= 3:
                print("RANDOM MISMATCH: L=%r loop=%r closed=%r"
                      % (L, (Ll, hl), (Lc, hc)))
    print("[C1b] random states: 10000 tested, mismatches=%d, halts=%d, "
          "min x seen=%d" % (mism, halts_seen, minx))

    # ---------------- (c) crafted states ----------------
    # x = 2^j (u=1): must halt for j>=3; b=0 so A = 2^j-3.
    bad = 0
    for j in range(3, 61):
        L = (2 ** j - 3, 0, 11, 13, 17)
        Ll, hl = top_step_loop(L)
        Lc, hc = closed_step(L)
        if not hl or hl != hc:
            bad += 1
            print("HALT-TEST FAIL j=%d: loop halt=%s closed halt=%s"
                  % (j, hl, hc))
    # x = 2^j * u, u>=3 odd: must not halt.
    for j in range(1, 25):
        for u in (3, 5, 9, 2 ** 61 - 1):
            x = (2 ** j) * u
            # b=0 -> A = x-3 odd (x even), >= 3
            L = (x - 3, 0, 9)
            Ll, hl = top_step_loop(L)
            Lc, hc = closed_step(L)
            if hl or (Ll, hl) != (Lc, hc):
                bad += 1
                print("NOHALT-TEST FAIL j=%d u=%d" % (j, u))
    print("[C1c] crafted halting (x=2^j, j=3..60) and non-halting "
          "(u in {3,5,9,2^61-1}, j=1..24): failures=%d" % bad)

    # off-domain boundary (negative b): document exact behaviour
    edge = []
    for (A, b) in ((3, -1), (1, 0), (1, -1), (3, -2), (5, -3), (7, -4)):
        # x = A+2b+3 in {4,4,2,2,2,2}
        L = (A, b, 5, 9)
        x = A + 2 * b + 3
        Ll, hl = top_step_loop(L)
        Lc, hc = closed_step(L)
        edge.append((L, x, v2(x), (x >> v2(x)), hl, (Ll, hl) == (Lc, hc)))
    for e in edge:
        print("   boundary L=%r x=%d j=%d u=%d halted=%s loop==closed:%s"
              % e)
    nx = sum(1 for e in edge if e[3] == 1 and not e[4])
    print("[C1d] boundary: u=1-with-j<=2 (x in {2,4}) states with no halt: %d "
          "(all off-domain: need b<0 or A=1)" % nx)


if __name__ == '__main__':
    main()
