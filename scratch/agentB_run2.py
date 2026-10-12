"""agentB_run2.py — tagged symbolic traces: track provenance of every entry."""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import *

def step_tagged(L, tags, cc):
    """One top step, maintaining tags. Returns (newL, newtags, info, newcc)."""
    aA, bA = L[0]
    assert aA % 2 == 0
    btag = tags[1] if len(tags) > 1 else 'ZERO'
    ctag = tags[2] if len(tags) > 2 else 'ZERO'
    if bA % 2 == 0:
        b = L[1] if len(L) > 1 else (0, 0)
        c = L[2] if len(L) > 2 else (0, 0)
        newA = (aA + b[0] + c[0], bA + b[1] + c[1] + 3)
        return ([newA] + L[3:], [tags[0]] + tags[3:],
                ('E', btag, ctag), cc)
    else:
        b = L[1] if len(L) > 1 else (0, 0)
        c = L[2] if len(L) > 2 else (0, 0)
        ax = aA + 2 * b[0]; bx = bA + 2 * b[1] + 3
        assert ax == 0 or v2i(ax) > v2i(bx), (ax, bx)
        j = v2i(bx)
        au = ax >> j; bu = bx >> j
        assert au >= 0 and bu >= 3, (au, bu)
        D = (c[0] + (aA >> 1), c[1] + ((bA + 1) >> 1))
        newL = ([(au, bu + 1)] + [(au << k, bu << k) for k in range(j - 1)] + [D] + L[3:])
        newtags = (['A#%d' % cc] + [('U%d.%d' % (cc, k)) for k in range(j - 1)] + [('D%d' % cc)] + tags[3:])
        info = ('C', j, (au, bu), D, btag, ctag)
        return (newL, newtags, info, cc + 1)

def fmt_pair(p):
    return '(%d)t+%d' % p if p[0] != 0 else str(p[1])

def tagged_trace(v, out):
    L = E_sym(v)
    tags = ['A0'] + [('T%d' % i) for i in range(v - 1)] + [('T%d*' % (v - 1))]
    lines = []
    cc = 1
    t = 0
    lines.append('v=%d  E_sym tail tags T0..T%d, T%d*=defect(-1)' % (v, v - 2, v - 1))
    while len(L) > 1:
        A = L[0]
        b = L[1] if len(L) > 1 else (0, 0)
        c = L[2] if len(L) > 2 else (0, 0)
        lines.append('step %3d  A=%s [%s]  b=%s [%s]  c=%s [%s]  len=%d' %
                     (t, fmt_pair(A), tags[0], fmt_pair(b), tags[1] if len(tags)>1 else '-',
                      fmt_pair(c), tags[2] if len(tags)>2 else '-', len(L)))
        L, tags, info, cc = step_tagged(L, tags, cc)
        if info[0] == 'E':
            lines.append('          -> E  consumed (%s, %s)' % (info[1], info[2]))
        else:
            _, j, u, D, btag, ctag = info
            lines.append('          -> C  j=%d u=%s D=%s  consumed b=%s c=%s' %
                         (j, fmt_pair(u), fmt_pair(D), btag, ctag))
        t += 1
    lines.append('final singleton A=%s after %d steps (ell=%d)' % (fmt_pair(L[0]), t, t))
    out.write('\n'.join(lines) + '\n\n')
    return t

def main():
    with open(r'D:\math_cc\scratch\agentB_traces.txt', 'w') as f:
        for v in (12, 24, 40):
            e = tagged_trace(v, f)
            print('v=%d ell=%d' % (v, e))

if __name__ == '__main__':
    main()
