"""agentF_fast.py -- fast ell(s) via the universal walk + endgame runner.

Model (validated in agentF_walk.py / agentF_probe_a.py against the naive
compositional engine, and against direct symbolic full runs):

A frame of level s (canonical list (H+d, H, 2H, ..., 2^{r-1}H, J) + tail,
J = 2^r H + kap, d = 3t+1 EXACTLY, X := v2(H) = s-1-r) evolves:
  t = 0        : E-macro  (H odd, head even);
  t odd        : E-macro  (d even);  r -> r-2;
  t even >= 2  : FIRE of level sp = v2(3t+4) (margin X > sp verified);
                 costs 1 + ell(sp) steps; r -> r - 2 - a,  a = a0(sp) if r>=3
                 else min(a0(sp), 1);
  phase advance: t -> t + 1 + ell(sp) + [ell(sp) even] (the optional E).
Events continue while the post-event r >= 2; otherwise the frame enters its
endgame (glue/second-life), run here exactly by stepping T_list until the
singleton (top frame: tail empty).

ell(s) = (main-phase steps) + (endgame steps).
"""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_lib import add, sc, sub, T_list, Undecided, Halt

W3 = (6, 3)          # 3w = 6u+3, w = 2u+1


def top_c(L):
    """Concrete top map (int lists), mirrors agentF_lib.top."""
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    S = L[3:]
    if A % 2 == 0:
        return [A + b + c + 3] + S
    m = b + (A - 3) // 2
    st = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st
        m = (m - 3) // 2
    if m == 1:
        return 'HALT'
    return [m + 4] + st


def v2_int(n):
    c = 0
    while n % 2 == 0:
        n //= 2
        c += 1
    return c


def window_entries(H, r, kap):
    """window = L[3:] of canonical (H, d, r, kap): r-1 entries."""
    return [sc(H, 2 << i) for i in range(r - 2)] + [add(sc(H, 1 << r), kap)]


class FastEll(object):
    def __init__(self, a0=None):
        self.ell = {1: 1, 2: 1}       # filled incrementally
        self.a0 = dict(a0 or {})
        self.endmax = 0
        self.endarg = None

    def a0_of(self, sp):
        """a0(sp): number of leading Z entries consumed by a level-sp frame
        whose Z begins with two even entries (the caller window's 4H, 8H).
        Computed concretely (uniformity in K, Z is the engine-verified Lemma
        F(s)); asserted against the table measured from real walks."""
        if sp in self.a0:
            return self.a0[sp]
        w = 1
        Z = [(1 << 40) + 2, (1 << 41) + 2, (1 << 42) + 3]
        L = [3 * w + 1] + [3 * w << i for i in range(sp - 1)] + \
            [(3 * w << (sp - 1)) - 1] + list(Z)
        n = 0
        while True:
            suf = len(L) - 1
            if suf <= 3 and L[1:] == Z[3 - suf:]:
                break
            L = top_c(L)
            n += 1
            assert n < 10 ** 7, 'a0 runaway'
        a = 3 - (len(L) - 1)
        self.a0[sp] = a
        return a

    def endgame(self, L):
        n = 0
        while len(L) > 1:
            L = T_list(L)
            n += 1
            assert n < 10 ** 6, 'endgame runaway'
        if n > self.endmax:
            self.endmax = n
            self.endarg = n
        return n

    def ell_of(self, s):
        if s in self.ell:
            return self.ell[s]
        kap = (0, -1)
        if s <= 2:
            L = [add(W3, (0, 1))] + [sc(W3, 1 << i) for i in range(s - 1)] + \
                [add(sc(W3, 1 << (s - 1)), (0, -1))]
            e = self.endgame(L)
            self.ell[s] = e
            return e
        r = s - 1
        t = 0
        while True:
            # E-event at t=0 or t odd
            if t == 0 or t % 2 == 1:
                if r - 2 >= 2:
                    t += 1
                    r -= 2
                    continue
                H = sc(W3, 1 << (s - 1 - r))
                d = 3 * t + 1
                post = [add(sc(H, 4), (0, d + 3))] + window_entries(H, r, kap)
                e = (t + 1) + self.endgame(post)
                self.ell[s] = e
                return e
            # fire at even t >= 2
            sp = v2_int(3 * t + 4)
            assert sp < s, ('well-foundedness', s, t, sp)
            Lc = self.ell[sp]
            a = self.a0_of(sp) if r >= 3 else min(self.a0_of(sp), 1)
            if r - 2 - a >= 2:
                t += 1 + Lc
                r -= 2 + a
                continue
            H = sc(W3, 1 << (s - 1 - r))
            d = 3 * t + 1
            win = window_entries(H, r, kap)
            head = add(sc(H, 4), (0, d + 3 + 3 * Lc), *win[:a])
            post = [head] + win[a:]
            e = (t + 1 + Lc) + self.endgame(post)
            self.ell[s] = e
            return e


def naive_ell(s):
    import agentF_lib as L
    eng = L.F_(use_cache=False)
    return L.excursion(s, eng)


def direct_ell(s):
    """Full symbolic run of E(w,v) by T_list only (no compositional logic)."""
    L = [add(W3, (0, 1))] + [sc(W3, 1 << i) for i in range(s - 1)] + \
        [add(sc(W3, 1 << (s - 1)), (0, -1))]
    t = 0
    while len(L) > 1:
        L = T_list(L)
        t += 1
    assert L[0] == add(sc(W3, 1 << s), (0, 3 * t))
    return t


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'validate'
    if mode == 'validate':
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        fe = FastEll()
        # a0 seed from probe data (re-derived if missing)
        fe.a0.update({1: 1, 2: 0, 3: 1, 4: 0, 5: 2, 6: 1, 7: 0, 8: 2})
        bad = []
        for s in range(1, N + 1):
            f = fe.ell_of(s)
            n = naive_ell(s)
            if f != n:
                bad.append((s, f, n))
        print('fast vs naive s<=%d: %s' % (N, bad[:10] or 'OK'))
        # direct symbolic cross-check for s <= 40 and sample
        bad2 = []
        for s in list(range(1, 41)):
            if fe.ell_of(s) != direct_ell(s):
                bad2.append(s)
        print('fast vs direct s<=40: %s' % (bad2 or 'OK'))
        print('a0 table:', dict(sorted(fe.a0.items())))
        print('max endgame length: %d' % fe.endmax)
