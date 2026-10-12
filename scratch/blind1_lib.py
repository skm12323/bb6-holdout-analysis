# blind1_lib.py -- BLIND AUDITOR 1 independent re-implementation.
# Top map per work_r1/RULES.md section 5 (the audited reduction):
#   lists L = (A, b, c, S), missing entries = 0.
#   A even -> L' = (A+b+c+3, S)
#   A odd  -> m := b + (A-3)/2;  st := [c + (A+1)/2] + S;
#             while m odd and m >= 3: st = [(m+3)/2] + st; m = (m-3)/2
#             m == 1 -> HALT;  else L' = (m+4, st)
# No code from agentB_*/mainline_*/agentG2_* was read.

def v2(n):
    """2-adic valuation, v2(0) undefined (we never call it with 0)."""
    if n == 0:
        raise ValueError("v2(0)")
    return (n & -n).bit_length() - 1


def top_step_loop(L):
    """One audited top-map step, implemented literally with the loop.
    Returns (L', halted)."""
    A = L[0]
    rest = L[1:]
    if len(rest) >= 2:
        b, c = rest[0], rest[1]
        S = rest[2:]
    elif len(rest) == 1:
        b, c, S = rest[0], 0, []
    else:
        b, c, S = 0, 0, []
    if A % 2 == 0:
        return (A + b + c + 3, ) + tuple(S), False
    # A odd (fire)
    m = b + (A - 3) // 2
    st = [c + (A + 1) // 2] + list(S)
    while m % 2 == 1 and m >= 3:
        st.insert(0, (m + 3) // 2)
        m = (m - 3) // 2
    if m == 1:
        return None, True
    return (m + 4, ) + tuple(st), False


def fire_closed(L):
    """Closed form of a fire (A odd). Returns (x, j, u, successor_tuple, halt).
    Claim C1: x = 2^j*u (u odd); halt iff u == 1 (on the top-map domain
    A>=3 odd, b>=0 this forces j>=3); successor (u+1; u,2u,...,2^{j-2}u,
    c+(A+1)/2, S)."""
    A = L[0]
    rest = L[1:]
    if len(rest) >= 2:
        b, c = rest[0], rest[1]
        S = rest[2:]
    elif len(rest) == 1:
        b, c, S = rest[0], 0, []
    else:
        b, c, S = 0, 0, []
    assert A % 2 == 1
    x = A + 2 * b + 3
    assert x > 0
    j = v2(x)
    u = x >> j
    D = c + (A + 1) // 2
    if u == 1 and j >= 3:
        return x, j, u, None, True
    run = [u << a for a in range(j - 1)]        # u, 2u, ..., 2^{j-2}u
    return x, j, u, (u + 1, ) + tuple(run) + (D, ) + tuple(S), False


def top_step_closed(L):
    """One top-map step via the closed form (A even branch identical)."""
    if L[0] % 2 == 0:
        return top_step_loop(L)
    return fire_closed(L)[3], fire_closed(L)[4]


def excursion_state(w, v):
    """E(w,v) = (3w+1; 3w, 6w, ..., 3w*2^{v-2}, 3w*2^{v-1}-1)."""
    entries = [3 * w * (1 << a) for a in range(v - 1)]
    entries.append(3 * w * (1 << (v - 1)) - 1)
    return (3 * w + 1, ) + tuple(entries)


def run_excursion(L, max_steps=10**7):
    """Step until the list is a singleton; return (steps, final, halted)."""
    L = tuple(L)
    steps = 0
    while len(L) > 1:
        L, halted = top_step_closed(L)
        if halted:
            return steps, None, True
        steps += 1
        if steps > max_steps:
            raise RuntimeError(" excursion too long")
    return steps, L, False


# ---------------- event stepper with provenance annotations ---------------
# Used for C2/C3/C4.  Queue entries are [value, ann]; ann is
#   ('run', level, idx)   entry 2^idx * U_level of the run pushed by `level`'s
#                         creating fire (level 0 = the excursion's own run)
#   ('seam', level)       the D pushed by that fire
#   ('defect',)           the excursion's tail defect
# plus for C3 ('hostrun', idx) etc. handled by drivers.

class Level:
    __slots__ = ('base', 'k', 'next_p', 'events', 'nlev')

    def __init__(self, base, nlev):
        self.base = base     # U
        self.k = 1           # current k of the level's chain schedule
        self.next_p = 4      # expected position of next chain event
        self.events = []     # list of (rho, j, k) chain events seen
        self.nlev = nlev


class Stepper:
    """Runs the closed-form top map on an annotated queue, emitting events."""

    def __init__(self, A, queue):
        # queue: list of [value, ann]
        self.A = A
        self.q = [list(e) for e in queue]
        self.levels = []          # Level objects; index = id
        self.n_fires = 0
        self.n_even = 0

    def pop2(self):
        b = self.q.pop(0)
        c = self.q.pop(0) if self.q else [0, None]
        return b, c

    def step(self):
        """One top-map step. Returns event dict:
        {'kind':'even'} or {'kind':'fire', ...} (and halts raise)."""
        if self.A % 2 == 0:
            b, c = self.pop2()
            self.A = self.A + b[0] + c[0] + 3
            self.n_even += 1
            return {'kind': 'even', 'b': b, 'c': c}
        # fire
        b, c = self.pop2()
        x = self.A + 2 * b[0] + 3
        j = v2(x)
        u = x >> j
        if u == 1 and j >= 3:
            return {'kind': 'halt', 'x': x}
        D = c[0] + (self.A + 1) // 2
        newlev = len(self.levels)
        lev = Level(u, newlev)
        self.levels.append(lev)
        pre = [[u << a, ('run', newlev, a)] for a in range(j - 1)]
        self.q = pre + [[D, ('seam', newlev)]] + self.q
        self.A = u + 1
        self.n_fires += 1
        return {'kind': 'fire', 'x': x, 'j': j, 'u': u, 'b': b, 'c': c,
                'newlevel': lev}
