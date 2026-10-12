"""reviewB_lib.py -- shared machinery for the adversary review of agentB's proof.

Provides:
  * tab(j)         : (dk, dp) from agentB_run7.verify (the abstract per-J verifier)
  * build_kpos(N)  : universal sequence  pos -> k  (positions 4,7,11,...)
  * kb_of(v,kpos)  : boundary k (universal k when the pointer crosses v-1)
  * run_labeled(w, v, kpos, base0=None, initqueue=None) : exact top-map run of
    E(w,v) (or a custom level state) with queue labels; checks Theorem 2's
    invariant I(rho) at EVERY chain consuming a run entry, at every nesting
    level present, and monitors for HALT.
"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import v2i
from agentB_run7 import verify as _verify_j

_TAB = {}


def tab(j):
    if j not in _TAB:
        res, err = _verify_j(j)
        assert not err, (j, err)
        _TAB[j] = res[0]
    return _TAB[j]


def build_kpos(N):
    kpos = {}
    p, k = 4, 1
    jmax = 0
    while p < N + 200:
        kpos[p] = k
        j = 1 + v2i(3 * k + 2)
        jmax = max(jmax, j)
        dk, dp = tab(j)
        p += dp
        k += dk
    return kpos, jmax


def kb_of(v, kpos):
    lastk = None
    for p in sorted(kpos):
        if p <= v - 1:
            lastk = kpos[p]
        else:
            break
    return lastk


def run_labeled(w, v, kpos, maxsteps=None, base0=None, initqueue=None):
    """Exact top map on E(w,v) (or a custom level state via base0/initqueue).

    Level 0's run entries must be labeled ('R', pos, 0); its base value is 3w
    (or base0).  A chain pushes a mini-run of level cid (base = its u, depth =
    depth of the level of the entry it consumed + 1) followed by its D (owned
    by cid).  At every chain consuming a run entry (any level) we check
        x - 3*2^rho*U == 6*k_rho + 4,   j == 1+v2(3*k_rho+2),   j < rho,
        U odd;  run-chain positions must be universal (rho in kpos);
    and monitor HALT (u == 1) globally.
    """
    U0 = 3 * w if base0 is None else base0
    if initqueue is not None:
        A = initqueue[0][0]
        queue = [list(e) for e in initqueue[1:]]
    else:
        A = U0 + 1
        queue = [[U0 << a, ('R', a, 0)] for a in range(v - 1)]
        queue.append([(U0 << (v - 1)) - 1, ('D', 0)])
    base = {0: U0}
    depth = {0: 0}
    fails = []
    stats = {'run_chains': 0, 'nonrun_chains': 0, 'nonuniv': 0,
             'maxdepth': -1, 'minu': None, 'maxj': 0, 'tie': 0,
             'depth_hist': {}, 'uodd_bad': 0}
    steps = 0
    if maxsteps is None:
        maxsteps = 40 * (2 * (v if v is not None else len(queue)) + 400)
    while queue:
        if steps > maxsteps:
            stats['cap'] = True
            break
        b_val, b_lab = queue[0]
        if len(queue) > 1:
            c_val, c_lab = queue[1]
        else:
            c_val, c_lab = 0, ('Z',)
        rest = queue[2:]
        if A % 2 == 0:
            A = A + b_val + c_val + 3
            queue = rest
        else:
            x = A + 2 * b_val + 3
            j = v2i(x)
            u = x >> j
            stats['maxj'] = max(stats['maxj'], j)
            if u == 1 and j >= 3:
                stats['halt'] = True
                stats['halt_step'] = steps
                stats['halt_x_bits'] = j
                break
            assert not (u == 1), ('A=1 special case hit', A, b_val)
            D = c_val + (A + 1) // 2
            # level of the consumed entry b (for depth bookkeeping)
            if b_lab[0] == 'R':
                d_lev = 0
            elif b_lab[0] == 'M':
                d_lev = depth[b_lab[2]]
            elif b_lab[0] == 'D':
                d_lev = depth[b_lab[1]]
            else:
                d_lev = 0
            if b_lab[0] in ('R', 'M'):
                rho = b_lab[1]
                lev2 = b_lab[2] if b_lab[0] == 'M' else 0
                stats['run_chains'] += 1
                d = depth[lev2]
                stats['depth_hist'][d] = stats['depth_hist'].get(d, 0) + 1
                stats['maxdepth'] = max(stats['maxdepth'], d)
                if stats['minu'] is None or u < stats['minu']:
                    stats['minu'] = u
                U = base[lev2]
                if U % 2 == 0:
                    stats['uodd_bad'] += 1
                    fails.append(('even-base', rho, d, U))
                if rho in kpos:
                    kr = kpos[rho]
                    diff = x - 3 * (1 << rho) * U
                    if diff != 6 * kr + 4:
                        fails.append(('diff', rho, d, diff - (6 * kr + 4)))
                    jj = 1 + v2i(3 * kr + 2)
                    if j != jj:
                        fails.append(('j', rho, d, j, jj))
                    if j >= rho:
                        stats['tie'] += 1
                        fails.append(('tie', rho, d, j))
                else:
                    stats['nonuniv'] += 1
                    fails.append(('nonuniv-pos', rho, d, j))
            else:
                stats['nonrun_chains'] += 1
            cid = len(base)
            base[cid] = u
            depth[cid] = d_lev + 1
            queue = ([[u << q, ('M', q, cid)] for q in range(j - 1)]
                     + [[D, ('D', cid)]] + rest)
            A = u + 1
        steps += 1
    stats['ell'] = steps
    stats['final_A'] = A if not queue else None
    stats['singleton'] = (not queue) and 'halt' not in stats
    stats['fails'] = fails
    stats['sum3'] = (A + sum(e[0] for e in queue)) % 3 if queue else A % 3
    return stats
