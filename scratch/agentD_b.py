"""
agentD_b.py -- Task B (independent re-derivation).

Three independent implementations of the "top map" dynamics and their cross-checks:
  (i)  raw TM (fast list-based tape) from the blank tape, recording every A0-event and
       every h=0 top config (k=1 or r2>=1), with exact TM times;
  (ii) macro-rule iterator: applies R1..R5 (+canonicalisation) from (0;[3])@t=5, with
       per-event costs 2*r1+3 / h+7 / h+5 (all verified against the raw TM in Task A);
  (iii) closed-form "top map" T from claim (3):
         A even -> (A+b+c+3, S)
         A odd  -> m:=b+(A-3)/2, stack:=(c+(A+1)/2,S); while m odd and m>=3:
                   stack=[(m+3)/2]+stack, m:=(m-3)/2; m==1 -> HALT else (m+4,stack)
       (missing entries read as 0).

Checks:
  * lists agree across (i)/(ii)/(iii); times agree across (i)/(ii), on ~3000 top steps
    (raw TM coverage limited by a step budget; exact counts reported).
  * sum(L_n) == 3n+3 from L_0=(3), over 3000 (formula vs macro) and over n<2^16 (formula).
  * HALT criterion reformulation: T halts on L <=> (A odd and A+2b+3 = 2^k), verified
    exhaustively over A<=601 odd, b<=300, over the whole n<2^16 orbit, and constructively
    on the raw TM for criterion-true configs.
  * excursion-entry formula: for every singleton L_n with n<2^16 (n even: n+2=2^v*w,
    w odd => L_{n+1}=(3w+1,3w,6w,...,3w*2^(v-2),3w*2^(v-1)-1); n odd: L_{n+1}=(A+3,)).
"""
import time

NAME = "1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE"


def parse_machine(s):
    T = {}
    for si, st in enumerate('ABCDEF'):
        p = s.split('_')[si]
        for sym, chunk in ((0, p[:3]), (1, p[3:])):
            T[(st, sym)] = None if chunk == '---' else (int(chunk[0]), chunk[1], chunk[2])
    return T


TBL = parse_machine(NAME)
FAILS = []


def fail(msg):
    FAILS.append(msg)
    print("FAIL:", msg)


# ---------------------------------------------------------------- fast raw TM
class FastTM:
    """list tape: R[j] = cell j (j>=0); L[i] = cell -1-i (i>=0)."""
    __slots__ = ('L', 'R', 'j', 'st', 't', 'halted', 'Rmax', 'Lmax')

    def __init__(self):
        self.L = [0]
        self.R = [0]
        self.j = 0
        self.st = 'A'
        self.t = 0
        self.halted = False
        self.Rmax = -1     # max index with R[idx]==1 (conservative, never shrinks)
        self.Lmax = -1     # max index with L[idx]==1

    def cell(self):
        j = self.j
        return self.R[j] if j >= 0 else self.L[-j - 1]

    def step(self):
        j = self.j
        if j >= 0:
            s = self.R[j]
        else:
            s = self.L[-j - 1]
        tr = TBL[(self.st, s)]
        if tr is None:
            self.halted = True
            return False
        w, mv, ns = tr
        if j >= 0:
            if self.R[j] != w:
                self.R[j] = w
                if w == 1 and j > self.Rmax:
                    self.Rmax = j
        else:
            i = -j - 1
            if self.L[i] != w:
                self.L[i] = w
                if w == 1 and i > self.Lmax:
                    self.Lmax = i
        if mv == 'R':
            j += 1
            if j == len(self.R):
                self.R.append(0)
        else:
            j -= 1
            if -j - 1 == len(self.L):
                self.L.append(0)
        self.j = j
        self.st = ns
        self.t += 1
        return True


def cell_at(tm, pos):
    if pos >= 0:
        return tm.R[pos] if pos < len(tm.R) else 0
    i = -pos - 1
    return tm.L[i] if i < len(tm.L) else 0


def parse_fast(tm):
    """parse the FastTM config at an A0-read into (h, blocks) canonical."""
    j = tm.j
    h = 0
    p = j - 1
    while cell_at(tm, p) == 1:
        h += 1
        p -= 1
    # rightmost cell that can hold a 1 to the right of the head:
    # ones at positions >=0 live in R (max index Rmax); ones at negative positions
    # live in L and are all at positions <= -1.
    limit = tm.Rmax
    if j < 0:
        limit = max(limit, -1)
    blocks = []
    cur = 0
    p = j + 1
    while p <= limit:
        if cell_at(tm, p) == 1:
            cur += 1
        else:
            blocks.append(cur)
            cur = 0
        p += 1
    blocks.append(cur)
    # drop trailing zero blocks (canonical)
    while len(blocks) >= 2 and blocks[-1] == 0:
        blocks.pop()
    if blocks == [0]:
        blocks = None      # k=0 (blank right side)
    return h, blocks


def is_top(h, blocks):
    return h == 0 and blocks is not None and (len(blocks) == 1 or blocks[1] >= 1)


# ---------------------------------------------------------------- macro iterator
def match_rules(h, b):
    k = len(b)
    r1, r2 = b[0], (b[1] if k >= 2 else None)
    out = []
    if k == 1:
        out.append('R2')
    if k >= 2 and r2 >= 1:
        out.append('R1')
    if k >= 3 and r2 == 0 and r1 >= 2:
        out.append('R3')
    if k >= 3 and r2 == 0 and r1 == 1:
        out.append('HALT' if h == 0 else 'R4')
    if k >= 3 and r2 == 0 and r1 == 0:
        out.append('R5')
    return out


def normalize(b):
    b = list(b)
    while len(b) >= 2 and b[-1] == 0:
        b.pop()
    return b


def apply_rule(h, b):
    ms = match_rules(h, b)
    assert len(ms) == 1
    rule = ms[0]
    k = len(b)
    r1 = b[0]
    if rule == 'R1':
        return 'R1', h + 1, normalize([b[0], b[1] - 1] + b[2:]), 2 * r1 + 3
    if rule == 'R2':
        return 'R2', h + 1, [r1 - 2, 0, 1], 2 * r1 + 3
    if rule == 'R3':
        return 'R3', h + 1, [r1 - 2, 0, b[2] + 1] + b[3:], 2 * r1 + 3
    if rule == 'R4':
        return 'R4', 0, [h - 1, 0, 1, b[2] + 1] + b[3:], h + 7
    if rule == 'R5':
        return 'R5', 0, normalize([h + b[2] + 3] + b[3:]), h + 5
    return 'HALT', None, None, 8


def macro_top_steps(n_top):
    """iterate macro rules from (0;[3])@t=5; return list of (list, t) of length n_top+1"""
    h, b, t = 0, [3], 5
    tops = [(list(b), t)]
    n_events = 0
    for n in range(1, n_top + 1):
        while True:
            rule, h2, b2, cost = apply_rule(h, b)
            n_events += 1
            if rule == 'HALT':
                return tops, n_events, True
            h, b, t = h2, b2, t + cost
            if is_top(h, b):
                tops.append((list(b), t))
                break
    return tops, n_events, False


# ---------------------------------------------------------------- formula T
def T_formula(L):
    A = L[0]
    if len(L) >= 3:
        b, c, S = L[1], L[2], list(L[3:])
    elif len(L) == 2:
        b, c, S = L[1], 0, []
    else:
        b, c, S = 0, 0, []
    if A % 2 == 0:
        return [A + b + c + 3] + S, False
    m = b + (A - 3) // 2
    stack = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        stack = [(m + 3) // 2] + stack
        m = (m - 3) // 2
    if m == 1:
        return None, True
    return [m + 4] + stack, False


def halt_criterion(L):
    A = L[0]
    if A % 2 == 0:
        return False
    b = L[1] if len(L) >= 2 else 0
    s = A + 2 * b + 3
    return s >= 4 and (s & (s - 1)) == 0


def E_list(w, v):
    """excursion entry list from claim (3)"""
    return [3 * w + 1] + [3 * w * 2 ** e for e in range(v - 1)] + [3 * w * 2 ** (v - 1) - 1]


# ================================================================ run everything
print("=" * 78)
N_TOP = 3000
tops_macro, n_ev, halted_macro = macro_top_steps(N_TOP + 1)
print("macro iterator: %d top steps (L_0..L_%d), %d macro events, halted=%s"
      % (len(tops_macro) - 1, len(tops_macro) - 1, n_ev, halted_macro))
print("t_0..t_5 =", [t for _, t in tops_macro[:6]])
print("t_%d = %d" % (N_TOP, tops_macro[N_TOP][1]))

# formula vs macro lists
ok = True
L = [3]
formula_lists = [L]
for n in range(1, N_TOP + 1):
    L, h = T_formula(L)
    if h:
        ok = False
        fail(f"formula halted at step {n}")
        break
    formula_lists.append(L)
for n in range(min(len(formula_lists), len(tops_macro))):
    if formula_lists[n] != tops_macro[n][0]:
        ok = False
        fail(f"top step {n}: formula {formula_lists[n]} != macro {tops_macro[n][0]}")
        if n > 20:
            break
print("formula-vs-macro on %d top steps: %s"
      % (min(len(formula_lists), len(tops_macro)) - 1, "PASS (lists identical)" if ok else "FAIL"))

# sum invariant over the 3000 macro steps
sum_ok = all(sum(bl) == 3 * n + 3 for n, (bl, _) in enumerate(tops_macro))
print("sum(L_n)==3n+3 for n=0..%d (macro): %s" % (len(tops_macro) - 1, "PASS" if sum_ok else "FAIL"))
if not sum_ok:
    for n, (bl, _) in enumerate(tops_macro):
        if sum(bl) != 3 * n + 3:
            fail(f"sum mismatch at n={n}: {sum(bl)} vs {3*n+3}")
            break

# ---------------------------------------------------------------- raw TM run
print("-" * 78)
import os
RAW_BUDGET = int(os.environ.get('AGENTD_RAW', 250_000_000))
WALL_LIMIT = 600.0            # seconds

# self-test: FastTM must agree with a dict-tape TM (independent implementations)
def _selftest(nsteps=200_000):
    tape = {}
    head, st, t = 0, 'A', 0
    ftm = FastTM()
    for _ in range(nsteps):
        s = tape.get(head, 0)
        assert s == ftm.cell(), (t, head)
        assert st == ftm.st and head == ftm.j
        tr = TBL[(st, s)]
        if tr is None:
            break
        w, mv, ns = tr
        tape[head] = w
        head += 1 if mv == 'R' else -1
        st = ns
        t += 1
        ftm.step()
    return t


_st = _selftest()
print("FastTM self-test vs dict-TM over %d steps: OK" % _st)

tm = FastTM()
raw_tops = []
t_start = time.time()
check_every = 1_000_000
next_check = check_every
while not tm.halted and tm.t < RAW_BUDGET and len(raw_tops) <= N_TOP:
    if tm.st == 'A':
        j = tm.j
        s = tm.R[j] if j >= 0 else tm.L[-j - 1]
        if s == 0:
            h, bl = parse_fast(tm)
            if bl is None:
                if tm.t != 0:
                    fail(f"raw: A0 event with no blocks at t={tm.t}")
            elif is_top(h, bl):
                raw_tops.append((tm.t, list(bl)))
    tm.step()
    if tm.t >= next_check:
        next_check += check_every
        if time.time() - t_start > WALL_LIMIT:
            print("raw run wall-limit hit at t=%d" % tm.t)
            break
raw_elapsed = time.time() - t_start
print("raw TM: %d steps in %.1fs (%.2f Msteps/s), halted=%s, #tops=%d, last top t=%d"
      % (tm.t, raw_elapsed, tm.t / raw_elapsed / 1e6, tm.halted, len(raw_tops), raw_tops[-1][0]))

# raw vs macro (lists + times)
n_cmp = min(len(raw_tops), len(tops_macro))
ok2 = n_cmp >= 2
for i in range(n_cmp):
    if raw_tops[i][0] != tops_macro[i][1] or raw_tops[i][1] != tops_macro[i][0]:
        ok2 = False
        fail(f"top {i}: raw (t={raw_tops[i][0]}, {raw_tops[i][1]}) vs macro (t={tops_macro[i][1]}, {tops_macro[i][0]})")
        if i > 20:
            break
if n_cmp < 2:
    fail("raw-vs-macro: no top steps compared (raw coverage failure)")
print("raw-vs-macro on %d top steps (lists AND TM times): %s"
      % (n_cmp - 1, "PASS" if ok2 else "FAIL"))

# ---------------------------------------------------------------- long formula run
print("-" * 78)
NN = 1 << 16
L = [3]
singletons = []
sum_bad = crit_true = 0
exc_ok = True
exc_checked = 0
pending = None
for n in range(0, NN + 1):
    if sum(L) != 3 * n + 3:
        sum_bad += 1
        if sum_bad == 1:
            fail(f"long run: sum at n={n}: {sum(L)} != {3*n+3}")
    if halt_criterion(L):
        crit_true += 1
        fail(f"long run: halting criterion TRUE at n={n}: {L}")
    if pending is not None:
        if L != pending:
            exc_ok = False
            fail(f"excursion-entry formula wrong: at n={n} got {L}, want {pending}")
        pending = None
    if len(L) == 1:
        singletons.append(n)
        A = L[0]
        assert A == 3 * n + 3
        if n % 2 == 1:
            pending = [A + 3]
        else:
            m = n + 2
            v = 0
            while m % 2 == 0:
                m //= 2
                v += 1
            w = m
            assert w % 2 == 1 and v >= 1
            pending = E_list(w, v)
        exc_checked += 1
    Ln, hh = T_formula(L)
    if hh:
        fail(f"long run: formula halted at n={n}")
        break
    L = Ln
print("long formula run n=0..%d: sum-violations=%d, criterion-true steps=%d" % (NN, sum_bad, crit_true))
print("singleton steps found: %d (first 12: %s ... last: %s)"
      % (len(singletons), singletons[:12], singletons[-1]))
even_sing = [s for s in singletons if s % 2 == 0]
print("of which even n: %d ; excursion-entry predictions made %d, verified %s"
      % (len(even_sing), exc_checked, "PASS" if exc_ok else "FAIL"))

# ---------------------------------------------------------------- halt criterion
print("-" * 78)
crit_ok = True
cnt = 0
for A in range(3, 602, 2):
    for b in range(0, 301):
        for tail in ([], [4], [2, 7]):
            Lx = [A, b] + tail
            _, h1 = T_formula(Lx)
            h2 = halt_criterion(Lx)
            cnt += 1
            if h1 != h2:
                crit_ok = False
                fail(f"criterion mismatch on {Lx}: T-halts={h1} criterion={h2}")
print("criterion equivalence over %d synthetic lists (A odd<=601, b<=301): %s"
      % (cnt, "PASS" if crit_ok else "FAIL"))

# constructive raw check: criterion-true top configs really halt on the TM
def build_top(L):
    """FastTM whose tape is 0^inf [0]_A 1^{L[0]} 0 1^{L[1]} 0 ... (a top config)"""
    tmx = FastTM()
    R = tmx.R
    q = 1
    for b in L:
        for _ in range(b):
            while q >= len(R):
                R.append(0)
            R[q] = 1
            tmx.Rmax = max(tmx.Rmax, q)
            q += 1
        q += 1
    while len(R) <= q:
        R.append(0)
    return tmx


def synth_top(L):
    """tape for (0; L) and run raw TM; return (halted, steps)"""
    tmx = build_top(L)
    while not tmx.halted and tmx.t < 10 ** 6:
        tmx.step()
    return tmx.halted, tmx.t


print("constructive halts on raw TM (criterion-true configs, A+2b+3=2^k):")
for (A, b) in [(7, 11), (7, 27), (3, 29), (15, 1015), (9, 506), (29, 16)]:
    Lx = [A, b]
    assert halt_criterion(Lx)
    halted, steps = synth_top(Lx)
    tag = "PASS" if halted else "FAIL"
    if not halted:
        fail(f"criterion-true {Lx} did not halt on raw TM")
    print("  (0; %s): A+2b+3=%d halted=%s after %d steps %s"
          % (Lx, A + 2 * b + 3, halted, steps, tag))
# ---------------------------------------------------------------- orbit-level halt checks
print("-" * 78)
print("orbit-level halting checks: iterate macro rules (with costs) from (0;L) until the")
print("HALT row or a step cap, and compare with the raw TM (same total step counts):")


def macro_run(L0, max_steps=2_000_000):
    """from top config (0;L0): iterate macro rules; returns (halted, total_steps,
    halting_list). total_steps counts TM transitions incl. the 8 of the halt segment."""
    h, b, t = 0, list(L0), 0
    crit_step = None
    while True:
        if is_top(h, b):
            if halt_criterion(b):
                crit_step = (list(b), t)
        rule, h2, b2, cost = apply_rule(h, b)
        if rule == 'HALT':
            # b must be exactly the HALT-row shape (0; 1, 0, y+1, REST)
            assert h == 0 and b[0] == 1 and b[1] == 0 and len(b) >= 3 and b[2] >= 1
            assert halt_criterion(b), (b,)
            return True, t + 8, list(b), crit_step
        t += cost
        if t > max_steps:
            return False, t, None, crit_step
        h, b = h2, b2


for Lx in [[15, 1], [21, 5], [7, 11], [3, 29], [9, 506], [29, 16], [15, 1015],
           [9], [3], [33], [21]]:
    halted_m, tm_macro, halting_list, crit = macro_run(Lx)
    tmx = build_top(Lx)
    while not tmx.halted and tmx.t < 2_000_000:
        tmx.step()
    same = (tmx.halted == halted_m) and (not halted_m or tmx.t == tm_macro)
    if halted_m:
        # the halting list must satisfy the criterion, and be the FIRST top step that does
        tag = "PASS" if (same and halt_criterion(halting_list)) else "FAIL"
        if not (same and halt_criterion(halting_list)):
            fail(f"orbit-level mismatch on {Lx}: macro=({halted_m},{tm_macro},{halting_list}) raw=({tmx.halted},{tmx.t})")
        print("  (0;%s): HALT after %d steps; halting top config (0;%s) has A+2b+3=%d; "
              "raw agrees: %s %s" % (Lx, tm_macro, halting_list,
                                     halting_list[0] + 2 * (halting_list[1] if len(halting_list) >= 2 else 0) + 3,
                                     same, tag))
    else:
        tag = "PASS" if (not tmx.halted and tmx.t >= 2_000_000) else "FAIL"
        if tmx.halted:
            fail(f"orbit-level: {Lx} raw halted at {tmx.t} but macro did not halt within cap")
        print("  (0;%s): no halt within %d macro steps; raw ran %d steps no halt %s"
              % (Lx, 2_000_000, tmx.t, tag))

print("=" * 78)
if FAILS:
    print("TASK B RESULT: FAIL (%d problems)" % len(FAILS))
else:
    print("TASK B RESULT: PASS")
