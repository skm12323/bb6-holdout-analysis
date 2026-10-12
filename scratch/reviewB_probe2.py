"""reviewB_probe2.py -- ATTACK 2: nested-level universality at depth.

(1) Establish the STRUCTURAL fact: at v=4000 the deepest run-chain depth is 1
    (measured); compute the smallest universal position rho with j_rho >= 28
    (the first host spike that would create depth-2 run chains) => minimum v.
(2) Instantiate ARTIFICIAL deep levels (canonical spike states / plain level
    processes) with odd base U and run lengths that DO produce depth-2 and
    depth-3 chains, at several U (small, spike-like, huge), and verify
    Theorem 2's invariant I(rho) at every nesting level present.
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\scratch')
from reviewB_lib import build_kpos, run_labeled, tab
from agentB_lib import v2i

def structural_threshold():
    """smallest universal position with j >= J for J in {5,6,8,9,12,16,20,28,40}."""
    targets = [5, 6, 8, 9, 12, 16, 20, 28, 40]
    found = {}
    p, k = 4, 1
    t0 = time.time()
    while p < 400000000 and len(found) < len(targets):
        j = 1 + v2i(3 * k + 2)
        for T in targets:
            if j >= T and T not in found:
                found[T] = (p, k, j)
        dk, dp = tab(j)
        p += dp
        k += dk
    print('(1) first universal position with j >= J:')
    for T in targets:
        if T in found:
            p, k, j = found[T]
            print('    J=%2d: rho=%d (k=%d, j=%d)  [need v >= ~%d for a host'
                  ' chain with this j]' % (T, p, k, j, p + 2))
        else:
            print('    J=%2d: not found below rho=4e8' % T)
    print('    scan %.1fs' % (time.time() - t0))

def level_state(U, R, dtail=0, dmode='defect'):
    """canonical level: A=U+1, queue [U*2^a (a<R), D, dtail zeros].
    dmode='defect': D = U*2^R - 1 (the natural excursion-like defect)."""
    q = [[U + 1, ('A',)]]
    for a in range(R):
        q.append([U << a, ('R', a, 0)])
    D = ((U << R) - 1) if dmode == 'defect' else 0
    q.append([D, ('D', 0)])
    for i in range(dtail):
        q.append([0, ('T', i)])
    return q

def main():
    kpos, _ = build_kpos(13000)
    print('kpos to 13000 (%d positions)' % len(kpos))
    structural_threshold()
    print('(2) artificial deep levels:')
    Us = [73, 9 * (1 << 30) + 7, (1 << 61) - 1, 999 * (1 << 33) + 5]
    Rs = [30, 60, 200, 1000, 3000, 12000]
    for U in Us:
        for R in Rs:
            t0 = time.time()
            q = level_state(U, R)
            st = run_labeled(1, None, kpos, base0=U, initqueue=q,
                             maxsteps=40 * (2 * R + 600))
            print('U=%-25d R=%-6d: halt=%s done=%s steps=%d runchains=%d '
                  'fails=%d maxdepth=%d minu=%s maxj=%d [%.1fs]'
                  % (U, R, st.get('halt', False),
                     st.get('singleton', st.get('cap', '?')), st['ell'],
                     st['run_chains'], len(st['fails']), st['maxdepth'],
                     st['minu'], st['maxj'], time.time() - t0))
            if st['fails']:
                print('    FAILS:', st['fails'][:6])
            else:
                print('    depth_hist:', dict(sorted(st['depth_hist'].items())))
            sys.stdout.flush()
    print('NOTE: depth counting is relative to the instantiated level; '
          'depth d here = nesting d levels BELOW it, i.e. level d+1 counting '
          'the instantiated run as level 1.')

if __name__ == '__main__':
    main()
