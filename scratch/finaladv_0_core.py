"""finaladv_0_core.py — FINAL ADVERSARY shared core.

Fully INDEPENDENT re-implementation (written from the audited top-map spec in
agentB_lib.py's docstring, not from agentB's engine code) of:

  * the top map on top lists, with LINEAGE LABELS on every queue entry:
        ('H', a)       host-level run entry at relative position a
        ('m', cid, q)  entry at relative position q of the run pushed by
                       chain number cid
        ('d', cid)     the defect pushed by chain cid
        ('Z',)         beyond-end-of-list zero (b or c missing)
    A is carried separately; state = (A, queue).

  * a pure-integer "universal walk" with base value U (odd): initial state
    (U+1; U, 2U, 4U, ...), used to derive the universal fire sequence
    (position rho -> k_rho) WITHOUT any symbolic frame and WITHOUT agentB's
    transition table.

Machine: 1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE.  Top map (audited spec):
  A even: T = (A+b+c+3, S)                     [consumes b, c]
  A odd : x = A+2b+3 = 2^j u;  HALT iff u=1 (j>=3);
          T = (u+1; u, 2u, ..., 2^{j-2}u, c+(A+1)/2, S)
"""
from collections import deque


def v2(x):
    if x == 0:
        return 1 << 60
    c = 0
    while (x & 1) == 0:
        x >>= 1
        c += 1
    return c


class Engine(object):
    """Labeled concrete top-map engine.  values / labels are parallel deques."""

    def __init__(self, A0, entries=()):
        self.A = A0
        entries = list(entries)
        self.vals = deque(v for v, _ in entries)
        self.labs = deque(l for _, l in entries)
        self.chain_id = 0
        self.chain_u = {}        # cid -> u of that chain (level base value)
        self.chain_j = {}        # cid -> j of that chain
        self.chain_bclass = {}   # cid -> b-label class of that chain
        self.maxpos = -1
        self.steps = 0
        self.fires = 0

    # -- helpers ---------------------------------------------------------
    def _b(self):
        return (self.vals[0], self.labs[0]) if self.vals else (0, ('Z',))

    def _c(self):
        return (self.vals[1], self.labs[1]) if len(self.vals) > 1 else (0, ('Z',))

    def _touch(self, lab):
        if lab[0] == 'H':
            self.maxpos = max(self.maxpos, lab[1])
        elif lab[0] == 'm':
            self.maxpos = max(self.maxpos, lab[2])

    def done(self):
        return len(self.vals) == 0

    # -- one top-map step --------------------------------------------------
    def step(self):
        """Returns an event dict.  Raises AssertionError on HALT-config."""
        self.steps += 1
        bv, bl = self._b()
        cv, cl = self._c()
        self._touch(bl)
        self._touch(cl)
        if (self.A & 1) == 0:
            self.A = self.A + bv + cv + 3
            if self.vals:
                self.vals.popleft()
                self.labs.popleft()
            if self.vals:
                self.vals.popleft()
                self.labs.popleft()
            return {'type': 'E', 'bl': bl, 'cl': cl}
        # A odd: chain
        x = self.A + 2 * bv + 3
        j = v2(x)
        u = x >> j
        ev = {'type': 'C', 'bl': bl, 'cl': cl, 'A': self.A, 'b': bv, 'c': cv,
              'x': x, 'j': j, 'u': u}
        assert u >= 3, 'HALT configuration reached: x=%d j=%d u=%d' % (x, j, u)
        D = cv + (self.A + 1) // 2
        self.chain_id += 1
        cid = self.chain_id
        self.chain_u[cid] = u
        self.chain_j[cid] = j
        self.chain_bclass[cid] = bl[0]
        # pop b and c
        if self.vals:
            self.vals.popleft()
            self.labs.popleft()
        if self.vals:
            self.vals.popleft()
            self.labs.popleft()
        # push run (u, 2u, ..., 2^{j-2}u) then D, in front
        self.vals.appendleft(D)
        self.labs.appendleft(('d', cid))
        for q in range(j - 2, -1, -1):
            self.vals.appendleft(u << q)
            self.labs.appendleft(('m', cid, q))
        self.A = u + 1
        self.fires += 1
        ev['cid'] = cid
        return ev


def E_entries(w, v):
    """Excursion E(w,v) initial queue entries (after A)."""
    assert w % 2 == 1 and v >= 1
    out = []
    for a in range(v - 1):
        out.append(((3 * w) << a, ('H', a)))
    out.append((((3 * w) << (v - 1)) - 1, ('T', v - 1)))   # defect-tail entry
    return out


def excursion_labeled(w, v, cap=10 ** 7):
    """Run E(w,v) to singleton; returns (engine, events, ell, result)."""
    eng = Engine(3 * w + 1, E_entries(w, v))
    events = []
    while not eng.done() and eng.steps < cap:
        ev = eng.step()
        if ev['type'] == 'C':
            events.append(ev)
    return eng, events, eng.steps, ('singleton' if eng.done() else 'cap')


def universal_walk(U, nrun, cap_steps=None):
    """Pure-integer walk on the infinite run [U*2^a]; returns (engine, fires)
    where fires is the list of 'C' step events (labels 'H')."""
    eng = Engine(U + 1, ((U << a, ('H', a)) for a in range(nrun)))
    fires = []
    cap = cap_steps if cap_steps else 40 * nrun + 10000
    while eng.maxpos < nrun - 1 and eng.steps < cap:
        ev = eng.step()
        if ev['type'] == 'C':
            fires.append(ev)
    return eng, fires


def fire_position(bl):
    """relative run position if bl is a run entry else None."""
    if bl[0] == 'H':
        return bl[1]
    if bl[0] == 'm':
        return bl[2]
    return None


def level_base_of(bl, eng, U0):
    """base value U of the level a run-entry label belongs to."""
    if bl[0] == 'H':
        return U0
    if bl[0] == 'm':
        return eng.chain_u[bl[1]]
    return None


# ---- the (dk, dp) table AS PRINTED in agentB_closedform.md section 3 ------
# (independent hard-copy of the report's claim; used by finaladv_3)
REPORT_TABLE = {
    1: (1, 3), 2: (1, 2), 3: (2, 5), 4: (2, 4), 5: (3, 4), 6: (3, 5),
    7: (3, 4), 8: (4, 6), 9: (4, 2), 10: (5, 5), 11: (5, 4), 12: (6, 6),
    13: (6, 4), 14: (8, 5), 15: (7, 5), 16: (7, 4), 17: (8, 6), 18: (8, 3),
    19: (8, 2), 20: (9, 5),
}
