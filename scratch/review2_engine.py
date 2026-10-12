"""Auditor-2 independent engine for the R8 review (written from scratch).

Exact top-map dynamics (from the audited R1 rules), no imports from work_r8:

  T on L = (A, b, c, S):
    A even -> [A + b + c + 3] + S
    A odd  -> m = b + (A-3)//2, st = [c + (A+1)//2] + S
              while m odd and m >= 3: st = [(m+3)//2] + st; m = (m-3)//2
              m == 1 -> HALT ; else [m + 4] + st

Compositional frame tracking (mirrors the prover's excursion recursion):
  - a frame = a nested excursion; created at a "fire" (odd head) with its
    window W = L[3:] (the entries handed to the nested excursion);
  - frames are pushed at fires where the state is canonically parseable:
      'enc'   : greedy run parse (H, 2H, 4H, ..., 2^{r-1}H, J) succeeds, r >= 2
      'short' : r in {0,1} short canonical states produced by an E-macro at
                r in {2,3} (state [4H+d+3, 4H+kap, Z..] resp. [.., 4H, 8H+kap, Z..]),
                or (for stats only) fires reached there;
  - a frame returns when the state first equals [head] + W[a:] with the
    contract head  2^s0*H0 + d0 + 3*ell + kap0 + sum(W[:a])  (ell = all steps
    of the frame's segment, nested ones included); shape matches with a wrong
    head are 'coinc' and skipped (as in verify_r8.F);
  - j = number of entries of W already absorbed; the state always ends with
    W[j:] (asserted as an invariant every iteration).
"""
import sys


def top(L):
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    if A % 2 == 0:
        return [A + b + c + 3] + L[3:]
    m = b + (A - 3) // 2
    st = [c + (A + 1) // 2] + L[3:]
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st
        m = (m - 3) // 2
    if m == 1:
        return None                     # HALT
    return [m + 4] + st


def v2(x):
    if x == 0:
        return 1 << 30
    n = 0
    while not (x & 1):
        x >>= 1
        n += 1
    return n


def encode(L):
    """Greedy canonical parse: returns (H, d, r, kap) for
    [H+d, H, 2H, ..., 2^{r-1}H, J=2^r H+kap, ...] with r >= 2 and a J entry,
    else None.  (Same greedy rule as verify_r8.encode.)"""
    if len(L) < 3:
        return None
    H = L[1]
    if L[2] != 2 * H:
        return None
    r = 1
    while r + 1 < len(L) and L[r + 1] == (1 << r) * H:
        r += 1
    if r + 1 >= len(L):
        return None
    return (H, L[0] - H, r, L[r + 1] - (1 << r) * H)


def excursion_start(w, v):
    """E(w, v) = Phi_v(3w; 0; empty)."""
    return [3 * w + 1] + [3 * w << i for i in range(v - 1)] + [(3 * w << (v - 1)) - 1]


class Frame(object):
    __slots__ = ('W', 'j', 't0', 'ell', 'H0', 'd0', 'kap0', 's0', 'Xlen', 'root', 'tag')

    def __init__(self, W, t0, H0, d0, kap0, s0, Xlen=0, root=False, tag=''):
        self.W = W            # window handed to this excursion
        self.j = 0            # entries of W absorbed so far
        self.t0 = t0          # tree-time of this frame's start state
        self.ell = 0          # steps inside this frame's segment (nested incl.)
        self.H0 = H0          # contract: H at frame start
        self.d0 = d0          # contract: d at frame start
        self.kap0 = kap0      # contract: kap of the frame's J slot
        self.s0 = s0          # level of the excursion
        self.Xlen = Xlen      # parent-stuff entries contained in W (for j update)
        self.root = root
        self.tag = tag


def _delta_j(L, slen):
    """Number of window entries consumed by one top() step on L (stuff len slen)."""
    dj = 0
    if slen == 1 and len(L) >= 2:
        dj += 1
    if slen <= 2 and len(L) >= 3:
        dj += 1
    return dj


def run_tracked(L0, H0, d0, kap0, s0, sink=None, max_steps=1000000):
    """Run the exact concrete dynamics with frame tracking.

    Emits to sink: ('step', {'cls': 'E'|'G'|('C',sp)}), ('fire', {...}),
    ('pop', {...}), ('coinc', {...}), ('reclass', {...}), ('end', {...}).
    fire info: L, W, j (pre-step), j_after, H, d, r, kap, q0, sp, t, tag, root.
    Returns {'end': 'done'|'halt'|'timeout', 'steps': n, 'head': ...}."""
    L = list(L0)
    stack = [Frame([], 0, H0, d0, kap0, s0, 0, True, 'root')]

    def emit(kind, info):
        if sink is not None:
            sink(kind, info)

    nsteps = 0
    pending = None            # (r_short, H, d, kap) after an E-macro at r in {2,3}
    while True:
        # invariant: state ends with the innermost frame's unconsumed window
        fr = stack[-1]
        rem = len(fr.W) - fr.j
        assert rem >= 0 and len(L) >= rem + 1, 'invariant length broken'
        if rem:
            assert L[len(L) - rem:] == fr.W[fr.j:], 'invariant tail broken'
        # ---- return detection (cascade, contract-checked) ----
        popped = False
        while True:
            fr = stack[-1]
            W = fr.W
            mrem = len(L) - 1
            if mrem <= len(W) and L[1:] == W[len(W) - mrem:]:
                a = len(W) - mrem
                expect = (1 << fr.s0) * fr.H0 + fr.d0 + 3 * fr.ell + fr.kap0 + sum(W[:a])
                if L[0] == expect:
                    popped = True
                    stack.pop()
                    emit('pop', {'a': a, 'ell': fr.ell, 'root': fr.root, 'tag': fr.tag,
                                 'kap0': fr.kap0, 's0': fr.s0, 'H0': fr.H0})
                    if not stack:
                        return {'end': 'done', 'steps': nsteps, 'head': L[0]}
                    stack[-1].j += max(0, a - fr.Xlen)
                    continue
                emit('coinc', {'a': a, 'ell': fr.ell})
            break
        if popped and pending is not None:
            pending = None    # stale: the E-product state was consumed by a return
        if nsteps >= max_steps:
            return {'end': 'timeout', 'steps': nsteps}
        fr = stack[-1]
        t = fr.t0 + fr.ell
        A = L[0]
        short = pending
        pending = None
        if short is not None:
            r_s, H_s, d_s, kap_s = short
            assert L[0] == H_s + d_s and L[1] == (H_s + kap_s if r_s == 0 else H_s), \
                'short-state assert failed'
            if r_s == 1 and len(L) > 2:
                assert L[2] == 2 * H_s + kap_s, 'short r=1 assert failed'
        enc = encode(L)
        if short is not None and enc is not None:
            emit('reclass', {'r_short': short[0]})
            short = None      # the greedy parse wins (this is the prover's view)
        child = None
        cls = 'G'
        q0 = sp = None
        if A % 2 == 1 and (enc is not None or short is not None):
            if enc is not None:
                H, d, r, kap = enc
                tag = 'enc'
            else:
                r, H, d, kap = short
                tag = 'short'
            q0 = A + 2 * L[1] + 3
            sp = v2(q0)
            slen = len(L) - (len(fr.W) - fr.j)
            j_after = fr.j + _delta_j(L, slen)
            emit('fire', {'L': L, 'W': fr.W, 'j': fr.j, 'j_after': j_after,
                          'H': H, 'd': d, 'r': r, 'kap': kap, 'q0': q0, 'sp': sp,
                          't': t, 'tag': tag, 'root': fr.root})
            c = L[2] if len(L) > 2 else 0
            o_p = q0 >> sp
            child = Frame(L[3:], t + 1, o_p, 1, c + (A + 1) // 2 - (q0 >> 1), sp,
                          max(0, slen - 3), False, tag)
            cls = ('C', sp)
            fr.j = j_after
        else:
            if A % 2 == 0 and enc is not None and enc[2] >= 2:
                cls = 'E'
                if enc[2] in (2, 3):        # E-macro lands on an r-2 short state
                    pending = (enc[2] - 2, 4 * enc[0], enc[1] + 3, enc[3])
            slen = len(L) - (len(fr.W) - fr.j)
            fr.j += _delta_j(L, slen)
        L2 = top(L)
        nsteps += 1
        for f in stack:
            f.ell += 1
        if L2 is None:
            emit('end', {'end': 'halt', 'steps': nsteps})
            return {'end': 'halt', 'steps': nsteps}
        emit('step', {'cls': cls})
        if child is not None:
            o = child.H0
            assert L2[0] == o + 1, 'nested head'
            for i in range(1, child.s0):
                assert L2[i] == (o << (i - 1)), 'nested run'
            assert len(L2) > child.s0 and L2[child.s0] == child.kap0 + (q0 >> 1), 'nested c-prime'
            stack.append(child)
        L = L2


if __name__ == '__main__':
    # self-test on hand-computed examples
    ev = []
    res = run_tracked(excursion_start(1, 5), 3, 1, -1, 5, lambda k, i: ev.append((k, i)))
    assert res == {'end': 'done', 'steps': 5, 'head': 111}, res
    fires = [i for k, i in ev if k == 'fire']
    assert len(fires) == 1 and fires[0]['r'] == 0 and fires[0]['tag'] == 'short' \
        and fires[0]['sp'] == 3, fires
    assert res['head'] == (3 << 5) + 3 * res['steps']
    res = run_tracked(excursion_start(1, 3), 3, 1, -1, 3, None)
    assert res == {'end': 'done', 'steps': 2, 'head': 30}, res
    res = run_tracked(excursion_start(3, 4), 9, 1, -1, 4, None)
    assert res == {'end': 'done', 'steps': 2, 'head': 150}, res
    # cross-check ell against the plain direct run for a batch
    import random
    for (w, v) in [(1, 12), (3, 17), (5, 23), (7, 31), (1, 60), (3, 90)]:
        L = excursion_start(w, v)
        t = 0
        while len(L) > 1:
            L = top(L)
            assert L is not None
            t += 1
        res = run_tracked(excursion_start(w, v), 3 * w, 1, -1, v, None)
        assert res['steps'] == t and res['head'] == L[0] and res['head'] == (3 * w << v) + 3 * t, (w, v, res, t)
    print('engine self-test OK')
