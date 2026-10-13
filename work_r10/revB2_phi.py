"""BLIND AUDITOR-1 (revB2) -- independent Phi_m tracer, written from scratch.

Semantics (work_g6/PROOF_G6.md sect.0 + the audited top map of work_r1):
  state L = (A; b, c, S), b/c = first two queue entries.
  A even -> (A+b+c+3; S)
  A odd  -> x = A+2b+3 = 2^j*u; (u+1; u,2u,...,2^{j-2}u, c+(A+1)/2, S); HALT iff u=1.
  Phi_m: k_h = kappa(m) = unique k mod 2^m with 6k+4 = 2^m*odd, P = 2^(m+60),
         u = (9P+6k_h+4)/2^m, A = u+1,
         queue = [u*2^a : a=0..m-2] + [D_h=(15/2)P+3k_h+1] + [T_e=3*2^e*P : e>=2].
  Run until the first chain with b = T_e (canonical re-entry); that re-entry is
  verified to be canonical (x = 9*2^e*P + 6(k_h+dk)+4, D' canonical, pure T left).

Chain classification by b-role: R = run entry (level entry of Phi_m),
Dh = host seam, T = tail (stop), M = pushed multiple u'*2^t, d = pushed seam
(tagged with the step s of the pushing chain for provenance).
"""
from collections import deque


def v2(x):
    return (x & -x).bit_length() - 1


def kappa(j):
    mod = 1 << j
    k = ((1 << (j - 1)) - 2) * pow(3, -1, mod) % mod
    assert ((6 * k + 4) >> j) & 1 == 1          # class condition 6k+4 = 2^j*odd
    return k


def phi_trace(m, p=None):
    """Returns dict with chains, crossing info, canonical re-entry data."""
    k = kappa(m)
    p = m + 60 if p is None else p
    P = 1 << p
    x0 = 9 * P + 6 * k + 4
    assert v2(x0) == m
    u = x0 >> m
    A = u + 1
    Dh = (15 * P) // 2 + 3 * k + 1
    tmax = 2 * m + 120
    Q = deque((u << a, ('R', a)) for a in range(m - 1))
    Q.append((Dh, ('Dh',)))
    for e in range(2, tmax):
        Q.append((3 * (1 << e) * P, ('T', e)))
    s = 0
    cap = 8 * m + 3000
    chains = []                                  # (s, tb, tc, j, x)
    cross = None
    while s < cap:
        assert len(Q) >= 2
        b, tb = Q.popleft()
        c, tc = Q.popleft()
        if cross is None and (tb[0] == 'Dh' or tc[0] == 'Dh'):
            cross = dict(s=s, clean=(tb[0] == 'Dh'), A=A, tb=tb, tc=tc,
                         odd=(A % 2 == 1))
        if A % 2 == 0:
            A = A + b + c + 3
        else:
            x = A + 2 * b + 3
            j = v2(x)
            uu = x >> j
            assert uu >= 3, ('halting chain', m, s, tb)
            if tb[0] == 'T':
                # canonical re-entry: verify the audited canonical form, then stop
                assert tc == ('T', tb[1] + 1) and c == 3 * (1 << (tb[1] + 1)) * P
                assert all(t[0] == 'T' for _, t in Q), (m, s)
                num = x - 9 * (1 << tb[1]) * P - 4 - 6 * k
                assert num >= 0 and num % 6 == 0, (m, s, num)
                dk = num // 6
                Dp = c + (A + 1) // 2
                assert Dp == (15 * (1 << tb[1]) * P) // 2 + 3 * (k + dk) + 1
                return dict(m=m, k=k, P=P, u=u, chains=chains, cross=cross,
                            re=(dk, tb[1], s))
            chains.append((s, tb, tc, j, x))
            d = c + (A + 1) // 2
            pushes = [(uu << t, ('M', s)) for t in range(j - 1)] + [(d, ('d', s))]
            for ent in reversed(pushes):
                Q.appendleft(ent)
            A = uu + 1
        s += 1
    raise RuntimeError('no canonical re-entry within cap, m=%d' % m)
