"""finaladv_3_table.py — ANGLE 3 ((dk,dp) table completeness) + ANGLE 5 data.

Sweep E(1,v) for v = 1..VMAX with a fast unlabeled deque engine:
  * every fire's j is recorded (the occurring-j set over ALL fires);
  * every TOP-LEVEL fire (odd part of b == 3w) must satisfy
        x == 3w*2^rho + 6*kpos[rho] + 4   and   j == jpos[rho]
    with kpos/jpos from the independent U=1 pure walk — this subsumes the
    consecutive-transition check dk(j), dp(j) vs the table for EVERY j that
    actually occurs at the top level (positions and k pinned to the walk);
  * ell(v) recorded: finiteness (singleton reached), ell <= 2*k_b + 16;
  * w-spot checks E(3,v), E(5,v), E(7,v), v <= 400.
Runtime-guarded; prints progress.
"""
import sys, time
from collections import deque
sys.path.insert(0, r'D:\math_cc\scratch')
import finaladv_0_core as C
import finaladv_1_levels as F1

VMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6000


def v2f(x):
    return (x & -x).bit_length() - 1


def fast_engine(w, v, kpos, jpos, jset, form_bad):
    """Run E(w,v); record j of every fire; check top-level form.  Returns
    ('singleton', ell) or ('HALT', step)."""
    A = 3 * w + 1
    q = deque(((3 * w) << a for a in range(v - 1)))
    q.append(((3 * w) << (v - 1)) - 1)
    steps = 0
    while q:
        steps += 1
        b = q[0]
        c = q[1] if len(q) > 1 else 0
        if (A & 1) == 0:
            A = A + b + c + 3
            q.popleft()
            if q:
                q.popleft()
            continue
        x = A + 2 * b + 3
        j = v2f(x)
        u = x >> j
        if u == 1:
            return ('HALT', steps)
        D = c + (A + 1) // 2
        q.popleft()
        if q:
            q.popleft()
        q.appendleft(D)
        for t in range(j - 2, -1, -1):
            q.appendleft(u << t)
        A = u + 1
        if jset is not None:
            jset.add(j)
        if form_bad is not None and (b >> v2f(b)) == 3 * w:
            rho = v2f(b)
            if rho in kpos:
                if x != (9 * w << rho) + 6 * kpos[rho] + 4 or j != jpos[rho]:
                    form_bad.append((w, v, rho, 'FORM', j, jpos[rho],
                                     x, (9 * w << rho) + 6 * kpos[rho] + 4))
            else:
                form_bad.append((w, v, rho, 'OFFPOS', x))
    return ('singleton', steps)


def main():
    t0 = time.time()
    kpos, jpos, _, _ = F1.build_kpos()
    print('kpos built: %d positions to %d' % (len(kpos), max(kpos)))
    ps = sorted(kpos)
    bad = []
    for a, b in zip(ps, ps[1:]):
        j = jpos[a]
        if j in C.REPORT_TABLE:
            dk, dp = C.REPORT_TABLE[j]
            if kpos[b] - kpos[a] != dk or b - a != dp:
                bad.append((a, b, j))
        else:
            bad.append((a, b, j, 'no-table-entry(j>20)'))
    print('U=1-walk gaps vs REPORT_TABLE (j<=20): %s'
          % ('ALL MATCH' if not bad else bad[:5]))

    jset = set()
    form_bad = []
    ells = {}
    v = 1
    halted = []
    while v <= VMAX and time.time() - t0 < 500:
        r = fast_engine(1, v, kpos, jpos, jset, form_bad)
        if r[0] != 'singleton':
            halted.append((v, r))
            break
        ells[v] = r[1]
        if v % 1000 == 0:
            print('  v=%d (%.0fs) form_bad=%d' % (v, time.time() - t0,
                                                  len(form_bad)))
        v += 1
    print('excursions v=1..%d: %s; max ell=%d'
          % (v - 1, 'ALL SINGLETON, no halt' if not halted else halted,
             max(ells.values())))
    print('occurring j set over ALL fires (all levels): %s' % (sorted(jset),))
    print('top-level form failures vs independent kpos: %d %s'
          % (len(form_bad), form_bad[:3]))
    # ell bound with prefix-max k
    kmax = {}
    kb = 0
    for p in ps:
        kb = max(kb, kpos[p])
        kmax[p] = kb
    viol = []
    for vv, e in ells.items():
        kb_v = 0
        for p in reversed(ps):
            if p <= vv - 1:
                kb_v = kmax[p]
                break
        if e > 2 * kb_v + 16:
            viol.append((vv, e, kb_v))
    ratio = max((ells[vv] / vv) for vv in ells if vv >= 100)
    print('ell > 2*k_b+16 violations: %d %s; max ell/v = %.4f'
          % (len(viol), viol[:5], ratio))
    # w spot checks
    for w in (3, 5, 7):
        fb = []
        halted_w = []
        for vv in range(1, 401):
            r = fast_engine(w, vv, kpos, jpos, None, fb)
            if r[0] != 'singleton':
                halted_w.append((vv, r))
                break
        print('w=%d: v<=400 %s; top-level form failures: %d %s'
              % (w, 'ALL SINGLETON' if not halted_w else halted_w,
                 len(fb), fb[:2]))
    print('elapsed %.1fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
