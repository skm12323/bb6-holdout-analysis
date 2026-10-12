"""agentB_run3.py — extract phase/chain tables for large v; find bulk pattern."""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import *

def phase_run(v, maxsteps=10**7):
    """Tagged symbolic run; returns list of events with tag bookkeeping."""
    L = E_sym(v)
    tags = ['A0'] + [('T%d' % i) for i in range(v - 1)] + [('T%d*' % (v - 1))]
    cc = 1
    events = []   # (step, kind, payload)
    t = 0
    while len(L) > 1 and t < maxsteps:
        A = L[0]
        btag = tags[1] if len(tags) > 1 else 'Z'
        ctag = tags[2] if len(tags) > 2 else 'Z'
        if A[1] % 2 == 0:
            b = L[1] if len(L) > 1 else (0, 0)
            c = L[2] if len(L) > 2 else (0, 0)
            events.append((t, 'E', btag, ctag))
            L = [(A[0] + b[0] + c[0], A[1] + b[1] + c[1] + 3)] + L[3:]
            tags = [tags[0]] + tags[3:]
        else:
            b = L[1] if len(L) > 1 else (0, 0)
            c = L[2] if len(L) > 2 else (0, 0)
            ax = A[0] + 2 * b[0]; bx = A[1] + 2 * b[1] + 3
            j = v2i(bx)
            au = ax >> j; bu = bx >> j
            D = (c[0] + (A[0] >> 1), c[1] + ((A[1] + 1) >> 1))
            events.append((t, 'C', j, (au, bu), D, btag, ctag, A))
            L = ([(au, bu + 1)] + [(au << k, bu << k) for k in range(j - 1)] + [D] + L[3:])
            tags = (['A%d' % cc] + [('U%d.%d' % (cc, k)) for k in range(j - 1)] + [('D%d' % cc)] + tags[3:])
            cc += 1
        t += 1
    return events, t

def tagtail(tag):
    """tail pointer info in a tag"""
    if tag.startswith('T'):
        return tag
    return tag

def main():
    v = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    events, ell = phase_run(v)
    # compact: chain list with (step, j, u_beta, D_beta, btag, ctag, Esteps since prev chain)
    chains = []
    last_c = -1
    for ev in events:
        if ev[1] == 'C':
            t, _, j, u, D, btag, ctag, A = ev
            chains.append((t, j, u[1], D[1], btag, ctag, t - last_c - 1, A[1]))
            last_c = t
    print('v=%d ell=%d nchains=%d' % (v, ell, len(chains)))
    print('idx step   j        u_b      D_b   btag     ctag    Esteps  A_before')
    for i, c in enumerate(chains):
        print('%3d %5d %3d %12d %10d  %-7s %-7s %4d %15d' % (i, c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]))
    # also j-sequence and (btag,ctag) sequence
    print('jseq:', [c[1] for c in chains])
    print('pairs:', [(c[4], c[5]) for c in chains])

if __name__ == '__main__':
    main()
