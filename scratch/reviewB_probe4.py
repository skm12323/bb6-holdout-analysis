"""reviewB_probe4.py -- ATTACK 4: mod-3 superset claim (section 5).

(a) Check the sum-mod-3 cancellation arithmetic of the canonical class C(J):
    with-defect queue (agentB_run13 geometry) vs bulk queue (agentB_run7
    geometry, 118 pure T's, NO defect): compute sum mod 3 exactly.
(b) Safety at OFF-SEQUENCE k: instantiate the canonical families concretely
    (k = kappa + m*2^J, m >= 0, arbitrary -- most off the universal sequence)
    at p >= max(200, j+100) (the range the abstract verifier claims) and run
    the TRUE top map for up to 20000 steps or until singleton; record HALTs.
(c) Also probe p BELOW the claimed range (p = J+1..J+12) to see whether the
    p-floor is load-bearing (halts there would show the verified statement's
    p-quantification matters).
"""
import sys, time, random
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_run7 import kappa_for
from agentB_lib import v2i

def top_step(A, q):
    """exact top map on (A, list q); returns (A', q') or 'HALT'."""
    b = q[0] if q else 0
    c = q[1] if len(q) > 1 else 0
    rest = q[2:]
    if A % 2 == 0:
        return A + b + c + 3, rest
    x = A + 2 * b + 3
    j = v2i(x)
    u = x >> j
    if u == 1 and j >= 3:
        return 'HALT'
    assert not (u == 1), 'A=1 special'
    D = c + (A + 1) // 2
    return u + 1, [(u << t) for t in range(j - 1)] + [D] + rest

def canon(J, p, w, k, E=None):
    """canonical post-chain state; E=None -> run7 bulk form (118 T's);
    E=int -> run13 endgame form (T at 2..E-1, then T* = 3*2^(E-1)P - 1)."""
    P = (1 << p) * w
    assert (6 * k + 4) % (1 << J) == 0 and ((6 * k + 4) >> J) % 2 == 1
    u = (9 * P + 6 * k + 4) >> J
    A = u + 1
    q = [(u << a) for a in range(J - 1)]
    q.append((15 * P) // 2 + 3 * k + 1)
    if E is None:
        for e in range(2, 120):
            q.append(3 * (1 << e) * P)
    else:
        for e in range(2, E):
            q.append(3 * (1 << e) * P)
        q.append(3 * (1 << (E - 1)) * P - 1)
    return A, q

def run(A, q, cap=20000):
    n = 0
    while q:
        r = top_step(A, q)
        if r == 'HALT':
            return ('HALT', n)
        A, q = r
        n += 1
        if n > cap:
            return ('cap', n)
    return ('singleton', n)

def main():
    t0 = time.time()
    # ---------- (a) mod-3 arithmetic ----------
    print('(a) sum mod 3 of the canonical families:')
    bad_a = 0
    rnd = random.Random(12345)
    for J in list(range(1, 31)) + [60, 100]:
        kap = kappa_for(J)
        for m in (0, 1, 7, 12345, 1 << 20, (1 << 37) + 3):
            k = kap + m * (1 << J)
            for E in (2, 3, 8, 20):
                A, q = canon(J, max(200, J + 100) + 37, 1, k, E)
                s3 = (A + sum(q)) % 3
                if s3 != 0:
                    bad_a += 1
                    if bad_a < 4:
                        print('   WITH-DEFECT sum%%3=%d at J=%d m=%d E=%d'
                              % (s3, J, m, E))
                A2, q2 = canon(J, max(200, J + 100) + 37, 1, k, None)
                s3b = (A2 + sum(q2)) % 3
                if s3b != 1:
                    print('   BULK sum%%3=%d (!=1) at J=%d m=%d' % (s3b, J, m))
    print('   with-defect family: sum = 12P+6k+3 => %%3 == 0 for ALL members;'
          ' violations: %d' % bad_a)
    print('   bulk family (no defect): sum = 12P+6k+4 => %%3 == 1 for ALL'
          ' members (no cancellation!)')
    # ---------- (b) off-sequence safety, claimed range ----------
    print('(b) off-sequence k, p >= max(200,j+100): run true dynamics')
    halts = []
    nruns = 0
    for J in list(range(1, 31)) + [45, 60]:
        kap = kappa_for(J)
        ms = list(range(0, 12)) + [97, 1000, 12345, 1 << 16, (1 << 16) + 1,
                                   1 << 30, (1 << 30) + 7, (1 << 40) + 11]
        for m in ms:
            k = kap + m * (1 << J)
            for E in (2, 3, 8, 20):
                for ds in (0, 37):
                    A, q = canon(J, max(200, J + 100) + ds, 1, k, E)
                    r = run(A, q)
                    nruns += 1
                    if r[0] == 'HALT':
                        halts.append(('end', J, m, E, ds, r[1]))
            # bulk form
            A, q = canon(J, max(200, J + 100), 1, k, None)
            r = run(A, q)
            nruns += 1
            if r[0] == 'HALT':
                halts.append(('bulk', J, m, None, 0, r[1]))
        sys.stdout.flush()
    print('   %d runs, halts: %s' % (nruns, halts if halts else 'NONE'))
    # ---------- (c) below the p-floor ----------
    print('(c) p below the claimed floor (p = J+1 .. J+12):')
    halts_c = []
    nc = 0
    for J in range(2, 25):
        kap = kappa_for(J)
        for p in range(J + 1, min(J + 13, 200)):
            for m in range(0, 40):
                k = kap + m * (1 << J)
                for E in (2, 8):
                    try:
                        A, q = canon(J, p, 1, k, E)
                    except AssertionError:
                        continue
                    r = run(A, q, cap=4000)
                    nc += 1
                    if r[0] == 'HALT':
                        halts_c.append((J, p, m, E, r[1]))
        sys.stdout.flush()
    print('   %d runs, halts below floor: %s' % (nc, halts_c[:10] if halts_c
                                                 else 'NONE'))
    print('total %.1fs' % (time.time() - t0))

if __name__ == '__main__':
    main()
