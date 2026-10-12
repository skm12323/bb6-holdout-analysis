"""Compositional symbolic prover for excursions of the top map (machine #1).

States:
  CS  = (H, d, r, kap, Z): list = [H+d] + [2^i*H for i in range(r)] + [2^r*H + kap] + Z
        (H, kap: affine forms (c0, c1) meaning c0*u + c1; d: form; r: int >= 0; Z: list of forms)
  GLUE = plain list of forms (short).
One top-map step on CS either stays CS (E-step with r>=2) or fires a nested excursion
(A odd: Lemma-R-style chain) which is executed RECURSIVELY (that's the compositionality),
or falls to GLUE.  GLUE lists are stepped directly by the symbolic engine and re-encoded
as CS whenever they develop a doubling run.

Every F(cs) run VERIFIES its conclusion:
  final singleton/suffix form == 2^s*o + 3*ell + (kap0+1) + sum(Z[:a])   [s = r0+1]
and returns (ell, a, head).  All decisions must be uniform in u (w = 2u+1).
"""
import sys
sys.setrecursionlimit(100000)
v2 = lambda x: (x & -x).bit_length() - 1

class Undecided(Exception): pass
class Halt(Exception): pass

# ---- affine forms over single symbol u >= 0 ----
def F_(c0, c1=0): return (c0, c1)
def add(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def sc(x, k): return (x[0] * k, x[1] * k)
def sub(x, y): return (x[0] - y[0], x[1] - y[1])
def par(x):
    if x[0] % 2: raise Undecided('parity(u)')
    return x[1] % 2
def half(x):
    if x[0] % 2 or x[1] % 2: raise Undecided('half')
    return (x[0] // 2, x[1] // 2)
def ge3(x):  # x >= 3 for ALL u >= 0 ?
    if x[0] >= 0 and x[1] >= 3: return True
    if x[0] == 0 and x[1] < 3: return False
    raise Undecided('ge3')
def v2f(x):
    """number of uniform halvings of form x (== min over u of v2(x(u)) if coeff pattern allows)."""
    n = 0
    while (x[0] % 2 == 0 and x[1] % 2 == 0) and (x[0] != 0 or x[1] != 0):
        x = (x[0] // 2, x[1] // 2); n += 1
    return n
def halfn(x, n):
    for _ in range(n): x = half(x)
    return x

# ---- direct symbolic top map on a plain list (GLUE / leaf engine) ----
Z0 = (0, 0)
def T_list(L):
    A = L[0]; b = L[1] if len(L) > 1 else Z0; c = L[2] if len(L) > 2 else Z0; R = L[3:]
    if par(A) == 0: return [add(A, b, c, (0, 3))] + R
    m = half(add(b, b, A, (0, -3))); st = [half(add(c, c, A, (0, 1)))] + R
    while par(m) == 1 and ge3(m):
        st = [half(add(m, (0, 3)))] + st; m = half(add(m, (0, -3)))
    if par(m) == 1:
        if m == (0, 1): raise Halt('HALT branch')
        raise Undecided('m odd, value unknown')
    return [add(m, (0, 4))] + st

class CS:
    __slots__ = ('H', 'd', 'r', 'kap', 'Z')
    def __init__(self, H, d, r, kap, Z):
        self.H, self.d, self.r, self.kap, self.Z = H, d, r, kap, Z
    def expand(self):
        L = [add(self.H, self.d)] + [sc(self.H, 1 << i) for i in range(self.r)] \
            + [add(sc(self.H, 1 << self.r), self.kap)] + list(self.Z)
        return L

def encode(L):
    """list of forms -> CS if it has a doubling run of length >=1 after the head, else None."""
    if len(L) < 3: return None
    H = L[1]
    if L[2] != sc(H, 2): return None
    r = 1
    while r + 1 < len(L) and L[r + 1] == sc(H, 1 << r): r += 1
    # r entries 2^0..2^{r-1} * H matched; next entry (if any) is the J-slot
    d = sub(L[0], H)
    if r + 1 < len(L):
        kap = sub(L[r + 1], sc(H, 1 << r)); Z = list(L[r + 2:])
    else:  # run reaches the end: no J slot; degenerate, treat as J with Z empty, kap = -? not sound; bail
        return None
    return CS(H, d, r, kap, Z)

EVENTS = []
def F(cs, level=None, trace=None):
    """Run the excursion to completion. Returns (ell, a, head, absorbed_list).
    Conclusion (asserted): expanded final list == [head] + original Z[a:], with
    head == 2^s*H0 + 3*ell + (kap0 + 1) + sum(Z0[:a]), s = r0 + 1."""
    if level is None: level = cs.r + 1
    H0, kap0, Z0L = cs.H, cs.kap, list(cs.Z)
    s0 = cs.r + 1
    ell = 0; absorbed = []
    state = cs
    guard = 0
    while True:
        guard += 1
        if guard > 200000: raise Undecided('runaway')
        if isinstance(state, CS):
            H, d, r, kap, Z = state.H, state.d, state.r, state.kap, state.Z
            A = add(H, d)
            if par(A) == 0:
                # E-step
                if r >= 2:
                    state = CS(sc(H, 4), add(d, (0, 3)), r - 2, kap, Z); ell += 1
                elif r == 1:
                    L = [add(sc(H, 4), d, kap, (0, 3))] + list(Z); ell += 1
                    state = _glue_or_cs(L)
                else:
                    z1 = Z[0] if Z else Z0
                    L = [add(sc(H, 2), d, kap, z1, (0, 3))] + list(Z[1:]); ell += 1
                    state = _glue_or_cs(L)
            else:
                # A odd: chain; construct nested CS and recurse.
                if r >= 2:
                    q0 = add(sc(H, 3), d, (0, 3)); cprime = add(sc(H, 2), half(add(H, d, (0, 1))))
                    window = [sc(H, 1 << i) for i in range(2, r)] + [add(sc(H, 1 << r), kap)] + list(Z)
                elif r == 1:
                    q0 = add(sc(H, 3), d, (0, 3))
                    cprime = add(sc(H, 2), kap, half(add(H, d, (0, 1))))
                    window = list(Z)
                else:
                    q0 = add(sc(H, 3), sc(kap, 2), d, (0, 3))
                    z1 = Z[0] if Z else Z0
                    cprime = add(z1, half(add(H, d, (0, 1))))
                    window = list(Z[1:])
                sp = v2f(q0)
                if sp == 0:
                    # no chain: single step (m even): result = [q0/2 + 1, c'] + window
                    L = [add(half(q0), (0, 1)), cprime] + window; ell += 1
                    state = _glue_or_cs(L)
                else:
                    o_p = halfn(q0, sp)
                    # J_nest must equal c': c' = 2^{sp-1} o' + kap_nest
                    kap_nest = sub(cprime, sc(o_p, 1 << (sp - 1)))
                    nest = CS(o_p, (0, 1), sp - 1, kap_nest, window)
                    assert sp < level, 'well-foundedness violated: sp=%d level=%d' % (sp, level)
                    ell_n, a_n, head_n, absorbed_n = F(nest, sp)
                    EVENTS.append((level, ell, r, sp, a_n))
                    ell += 1 + ell_n
                    absorbed.extend(absorbed_n)
                    rest = window[a_n:]
                    L = [head_n] + list(rest)
                    state = _glue_or_cs(L)
                # termination check for CS-as-list:
                if isinstance(state, CS):
                    st = state
                    # done if list == [X] + suffix(Z0L): i.e., st.r == 0, kap-Z empty and Z matches suffix, head arbitrary?
                    lst = None
                    if not st.Z and st.r == 0 and len(Z0L) == 0:
                        # singleton list [H+d, J]: 2 entries -> not done unless... fall through
                        pass
                    continue
        else:
            # GLUE: step directly
            L = state
            if len(L) >= 1 and _endswith(L, Z0L):
                a = len(L) - 1 - len(Z0L) if len(Z0L) else len(L) - 1
                # original-Z suffix reached: [X] + Z0L[a:] with nothing else
                break
            L = T_list(L); ell += 1
            state = _glue_or_cs(L)
            if isinstance(state, CS):
                st = state
                if not st.Z and st.r == 0 and not Z0L:
                    lst = st.expand()
                    if len(lst) == 1:
                        break
                continue
    # conclude: state is GLUE list [X] + Z0L[a:] (or singleton when Z0L empty)
    L = state if not isinstance(state, CS) else state.expand()
    # find a: L[1:] must equal Z0L[a:] for some a, and L must be exactly head + that suffix
    a = None
    if not Z0L:
        assert len(L) == 1, ('end state not singleton', L)
        a = 0
    else:
        for k in range(len(Z0L), -1, -1):
            if len(L) == 1 + len(Z0L) - k and L[1:] == Z0L[k:]:
                a = k; break
        assert a is not None, ('end state not head+Zsuffix', L, Z0L)
    head = L[0]
    expect = add(sc(H0, 1 << s0), (0, 3 * ell), (0, 1), kap0, *Z0L[:a]) if False else \
             add(sc(H0, 1 << s0), add((0, 3 * ell), add((0, 1), add(kap0, *Z0L[:a]))))
    assert head == expect, ('conclusion form mismatch', head, expect)
    return ell, a, head, Z0L[:a]

def _glue_or_cs(L):
    cs = encode(L)
    return cs if cs is not None else L

def _endswith(L, suffix):
    return len(L) >= len(suffix) + 1 and L[len(L) - len(suffix):] == suffix if suffix else False

# ---- driver: F(v) for the excursion E(w, v) (K=0, Z empty) and cross-check vs direct ----
def direct_E(v):
    """R4-style direct symbolic run; returns ell."""
    w3 = (6, 3)
    L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
    t = 0
    while len(L) > 1:
        L = T_list(L); t += 1
    assert L[0] == add(sc(w3, 1 << v), (0, 3 * t))
    return t

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    ok = 0
    for v in range(1, N + 1):
        w3 = (6, 3)
        cs = CS(w3, (0, 1), v - 1, (0, -1), [])
        ell, a, head, absorbed = F(cs, v)
        assert a == 0 and absorbed == []
        assert head == add(sc(w3, 1 << v), (0, 3 * ell))
        ell_d = direct_E(v)
        assert ell == ell_d, (v, ell, ell_d)
        ok += 1
    print('compositional F(v) == direct ell(v) for v = 1..%d  (all conclusions verified)' % N)
    print('events sample:', EVENTS[:6])
    print('total nested calls:', len(EVENTS))
    mx = max(e[3] for e in EVENTS) if EVENTS else 0
    print('max nested level used:', mx)
