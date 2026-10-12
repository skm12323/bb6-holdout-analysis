"""agentB_run15.py — big invariant run: canonical replay invariant to position N.
Invariant: at every chain whose b is a run entry (any nesting level),
    x = 3*2^rho * U + (6 k_rho + 4),   j = 1 + v2(3 k_rho + 2),
U = level base value, rho = relative run position, k_rho = universal k.
Also: tie-freeness (j != rho) and safety at every event."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
import agentB_mu as mu
from agentB_mu import Walker, Val
from agentB_lib import v2i
from agentB_run7 import verify

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
    TAB = {}
    for j in range(1, 121):
        res, err = verify(j)
        assert not err, (j, err)
        TAB[j] = res[0]
    kpos = {}
    p, k = 4, 1
    kmax = 0
    while p < N + 40:
        j = 1 + v2i(3 * k + 2)
        kpos[p] = k
        kmax = max(kmax, k)
        if k > (p + 4) // 2:
            print('k bound FAIL at p=%d k=%d' % (p, k)); return
        p += TAB[j][1]; k += TAB[j][0]
    w = Walker(N + 50)
    level_base = {None: Val(1, 1, 0)}
    ok = 0; bad = []; jmax = 0
    while w.maxpos < N:
        (b, lb) = w.queue[0]
        (c, lc) = w.queue[1] if len(w.queue) > 1 else (mu.ZERO, ('Z',))
        rest = w.queue[2:]
        for l in (lb, lc):
            if l[0] == 'R':
                w.maxpos = max(w.maxpos, l[1])
        if mu.parity(w.A) == 0:
            w.A = w.A + b + c + Val(0, 0, 3)
            w.queue = rest
        else:
            x = w.A + b * 2 + Val(0, 0, 3)
            j = mu.v2_val(x)
            jmax = max(jmax, j)
            u = x * Fr(1, 1 << j)
            if mu.min_val(u) < 3:
                print('u<3 at', lb); return
            D = c + (w.A + Val(0, 0, 1)) * Fr(1, 2)
            if lb[0] == 'R':
                rho, L = lb[1], None
            elif lb[0] == 'M':
                rho, L = lb[2], lb[1]
            else:
                rho, L = None, None
            if rho is not None and rho in kpos:
                U = level_base[L]
                diff = x - U * (3 << rho)
                kr = kpos[rho]
                if diff.cM == 0 and diff.cmu == 0 and diff.e == 6 * kr + 4:
                    ok += 1
                    if j != 1 + v2i(3 * kr + 2):
                        bad.append(('j mismatch', lb, j, kr))
                else:
                    bad.append((lb, diff, kr))
            w.chain_id += 1
            cid = w.chain_id
            level_base[cid] = u
            w.queue = [(u * (1 << q2), ('M', cid, q2)) for q2 in range(j - 1)] \
                      + [(D, ('D', cid))] + rest
            w.A = u + Val(0, 0, 1)
    print('N=%d: run-chain events: %d, invariant failures: %d, max j: %d, '
          'max k on universal seq: %d (k <= (p+4)/2 OK)' % (N, ok, len(bad), jmax, kmax))
    if bad:
        print('first bad:', bad[0])

if __name__ == '__main__':
    main()
