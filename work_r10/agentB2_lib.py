"""agentB2_lib.py -- machinery for the EXIT CLASS LEMMA (j_D <= J-2 at every spike exit).

Objects (work_g6 PROOF_G6.md ss0 / work_r10 PROOF.md ss7):
  Phi_m: after a host chain with parameter m whose x = 9P+6k_h+4 and class
         6k_h+4 = 2^m*odd, the queue is [u, 2u, .., 2^{m-2}u, D_h, T_2, T_3, ..]
         with u = (9P+6k_h+4)/2^m (odd), D_h = (15/2)P+3k_h+1, T_e = 3*2^e P.
         A spike is m >= 5.  The sub-cascade (fires on the pure run) is the
         universal level process with base u until queue index m-1 is read
         (Prop 2).  The EXIT = everything from the last pure sub-fire rho*
         to the D-fire (b = D_h) and any follow-up fire on the pushed 'd' seam.

Self-contained (python stdlib only); exact integer arithmetic.
Read-only import of work_g6.verify_g6.phi for the universal (dk,dp) tables.
"""
import sys
from fractions import Fraction as Fr

sys.path.insert(0, r'D:\math_cc\work_g6')
from verify_g6 import phi, kappa, v2  # noqa: E402  (read-only use)


# ---------------------------------------------------------------------------
# traced version of phi(): records every step with the labels of b and c,
# the chain value x, and u; tags pushed seams ('d', stepindex) so the seam
# pushed by the D-fire is identifiable.
# ---------------------------------------------------------------------------
def phi_traced(m, p=None, kh=None, tail=60):
    """Run Phi_m exactly; return dict with the step trace and re-entry data.

    steps: list of (kind, lb, lc, j, x, u)  (kind 'E' even / 'C' chain;
    x,u None for even steps).  Re-entry (fire with b = T_e) ends the run.
    """
    if kh is None:
        kh = kappa(m)
    assert (6 * kh + 4) % (1 << m) == 0 and ((6 * kh + 4) >> m) % 2 == 1, 'k_h class'
    p = p if p is not None else m + 60
    P = 1 << p
    x0 = 9 * P + 6 * kh + 4
    assert v2(x0) == m
    u = x0 >> m
    A = u + 1
    Q = [(u << a, ('R', a)) for a in range(m - 1)]
    Q.append((15 * P // 2 + 3 * kh + 1, ('D',)))
    Q += [(3 * (1 << e) * P, ('T', e)) for e in range(2, tail)]
    steps = []
    while True:
        (b, lb), (c, lc) = Q[0], Q[1]
        if A % 2 == 0:
            steps.append(('E', lb, lc, None, None, None))
            A = A + b + c + 3
            Q = Q[2:]
            continue
        x = A + 2 * b + 3
        j = v2(x)
        uu = x >> j
        assert uu >= 3, ('halt-like chain', m)
        if lb[0] == 'T':
            dk = (x - 9 * (1 << lb[1]) * P - 4 - 6 * kh) // 6
            steps.append(('C', lb, lc, j, x, uu))
            return {'m': m, 'p': p, 'kh': kh, 'u': u, 'P': P, 'steps': steps,
                    'dk': dk, 'dp': lb[1], 'K_exit_total': None}
        sidx = len(steps)
        steps.append(('C', lb, lc, j, x, uu))
        rest = Q[2:]
        Q = [(uu << a, ('M', sidx)) for a in range(j - 1)] + \
            [(c + (A + 1) // 2, ('d', sidx))] + rest
        A = uu + 1


def subfire_k(x, rho, u):
    """k of a pure sub-fire: x = 3*2^rho*u + 6K+4."""
    K = (x - 3 * (1 << rho) * u - 4)
    assert K % 6 == 0
    return K // 6


def classify(m, p=None, kh=None):
    """Classify the exit of Phi_m.  Returns None if no D-touch before re-entry."""
    r = phi_traced(m, p=p, kh=kh)
    st = r['steps']
    u = r['u']
    # pure sub-fires: b,c both run originals
    pure = [i for i, s in enumerate(st)
            if s[0] == 'C' and s[1][0] == 'R' and s[2][0] == 'R']
    mixedD = [i for i, s in enumerate(st)
              if s[0] == 'C' and (s[1][0] == 'R' or s[1][0] == 'M') and s[2][0] == 'D']
    Dfire = [i for i, s in enumerate(st) if s[0] == 'C' and s[1][0] == 'D']
    if not pure and not mixedD and not Dfire:
        return {'m': m, 'type': 'noD', 'tr': r}
    i_last = pure[-1] if pure else -1
    rho = st[i_last][1][1] if pure else None
    jlast = st[i_last][3] if pure else None
    K = subfire_k(st[i_last][4], rho, u) if pure else None
    # everything from just after the last pure sub-fire up to re-entry:
    exit_steps = st[i_last + 1:] if pure else st[:len(st)]
    # fires in the exit window with their b/c labels
    fires = [(s[1], s[2], s[3]) for s in exit_steps if s[0] == 'C']
    # the D-fire and any fire on the seam pushed by the D-fire
    dseam = None
    dfire = None
    dfire_seam = None
    for i, s in enumerate(exit_steps):
        if s[0] == 'C' and s[1][0] == 'D' and dfire is None:
            dfire = i
            dfire_seam = ('d', st.index(s)) if False else None
    # index of the D-fire in the full step list:
    iD = [i for i, s in enumerate(st) if s[0] == 'C' and s[1][0] == 'D']
    iD = iD[0] if iD else None
    # seam pushed by the D-fire carries tag ('d', iD)
    seamfire = None
    if iD is not None:
        seamfire = [i for i, s in enumerate(st)
                    if s[0] == 'C' and s[1] == ('d', iD) and i > iD]
        seamfire = seamfire[0] if seamfire else None
    return {'m': m, 'type': 'D', 'rho': rho, 'jlast': jlast, 'K': K,
            'gap': (m - 2 - rho) if rho is not None else None,
            'i_last': i_last, 'iD': iD, 'seamfire': seamfire,
            'jD': st[iD][3] if iD is not None else None,
            'jseam': st[seamfire][3] if seamfire is not None else None,
            'x_D': st[iD][4] if iD is not None else None,
            'exit_fires': fires, 'tr': r, 'steps': st}


# ---------------------------------------------------------------------------
# universal sequence from the phi table (as V3/V5 in verify_g6)
# ---------------------------------------------------------------------------
def universal(N):
    """(pos->k) map and the fire list [(p,k,j)] for universal positions < N."""
    tab = {}

    def T(j):
        if j not in tab:
            dk, dp, _, _ = phi(j)
            tab[j] = (dk, dp)
        return tab[j]
    fires = []
    kat = {}
    p, k = 4, 1
    while p < N:
        jj = 1 + v2(3 * k + 2)
        fires.append((p, k, jj))
        kat[p] = k
        dk, dp = T(jj)
        k += dk
        p += dp
    return kat, fires
