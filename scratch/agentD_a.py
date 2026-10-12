"""
agentD_a.py -- Task A (independent re-derivation, all code written from scratch).

Machine M = "1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE"
bbchallenge convention: tape infinite in both directions, all 0, head at cell 0, state A.
Transitions (state,read)->(write,move,next); '---' = HALT.

Verified here:
 (1) HALT iff F reads 0 (definitional); F only entered leftward from E0; every halt is
     preceded by a leftward E/F sweep; halting <=> an A0-event configuration of the form
     (0; 1, 0, y+1, REST) in the encoding
        (h; r1..rk) = tape 0^inf 1^h [0]_A 1^r1 0 1^r2 0 ... 0 1^rk 0^inf.
 (2) Macro rules R1..R5 + HALT row (one A0-event to the next), invariant I, coverage,
     uniqueness.  Plus derived per-rule TM step costs (needed for Task B times):
        R1/R2/R3 cost 2*r1+3 ; R4 cost h+7 ; R5 cost h+5 ; HALT fires after 9 steps.

Run from blank tape for 500,000 TM steps; also synthetic exhaustive + random I-configs.
"""
import random

NAME = "1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE"


def parse_machine(s):
    parts = s.split('_')
    assert len(parts) == 6, parts
    T = {}
    for si, st in enumerate('ABCDEF'):
        p = parts[si]
        assert len(p) == 6
        for sym, chunk in ((0, p[:3]), (1, p[3:])):
            if chunk == '---':
                T[(st, sym)] = None            # halting transition
            else:
                w, mv, ns = chunk
                assert w in '01' and mv in 'LR' and ns in 'ABCDEF'
                T[(st, sym)] = (int(w), mv, ns)
    return T


TBL = parse_machine(NAME)
# double-entry bookkeeping: hand-transcribed table from the problem statement
HAND = {('A', 0): (1, 'R', 'B'), ('A', 1): (1, 'L', 'A'),
        ('B', 0): (0, 'R', 'C'), ('B', 1): (0, 'R', 'D'),
        ('C', 0): (1, 'L', 'C'), ('C', 1): (1, 'L', 'A'),
        ('D', 0): (1, 'R', 'E'), ('D', 1): (1, 'R', 'D'),
        ('E', 0): (1, 'L', 'F'), ('E', 1): (0, 'L', 'A'),
        ('F', 0): None,        ('F', 1): (0, 'L', 'E')}
assert TBL == HAND, "machine parse mismatch"

FAILS = []


def fail(msg):
    FAILS.append(msg)
    print("FAIL:", msg)


# ---------------------------------------------------------------- raw TM (dict tape)
class TM:
    __slots__ = ('tape', 'head', 'state', 't', 'halted')

    def __init__(self):
        self.tape = {}
        self.head = 0
        self.state = 'A'
        self.t = 0
        self.halted = False

    def read(self):
        return self.tape.get(self.head, 0)

    def step(self):
        tr = TBL[(self.state, self.read())]
        if tr is None:
            self.halted = True
            return False
        w, mv, ns = tr
        self.tape[self.head] = w
        self.head += 1 if mv == 'R' else -1
        self.state = ns
        self.t += 1
        return True


# ---------------------------------------------------------------- config parsing
def parse_config(tape, head, support):
    """support = sorted list of cells holding 1. Returns (h, blocks) with blocks=None
    if there is no 1 strictly right of head (k=0). Canonical: trailing 0-blocks dropped
    (they are merged into the 0^inf tail)."""
    h = 0
    p = head - 1
    while tape.get(p, 0) == 1:
        h += 1
        p -= 1
    ones_right = [q for q in support if q > head]
    if not ones_right:
        return h, None
    R = ones_right[-1]
    blocks = []
    cur = 0
    p = head + 1
    while p <= R:
        if tape.get(p, 0) == 1:
            cur += 1
        else:
            blocks.append(cur)
            cur = 0
        p += 1
    blocks.append(cur)
    # hygiene: left support must be exactly the h cells head-1..head-h
    if support and support[0] < head - h:
        raise ValueError("stray 1 far left")
    return h, blocks


def encoding_anomaly(blocks):
    """encoding allows r2=0 (double zero) only; r_i=0 for i>=3 is not representable"""
    for i in range(2, len(blocks)):
        if blocks[i] == 0:
            return f"r{i+1}=0 (consecutive zeros deep in list)"
    return None


def check_I(h, blocks):
    """invariant I: k>=1, rk>=1, ri>=1 for i>=3, (r1>=2 or r2=0), k=1 => r1>=2"""
    k = len(blocks)
    if k < 1:
        return False, "k=0"
    if blocks[-1] < 1:
        return False, "rk=0"
    for i in range(2, k):
        if blocks[i] < 1:
            return False, f"r{i+1}=0"
    r1 = blocks[0]
    r2 = blocks[1] if k >= 2 else None
    if not (r1 >= 2 or (r2 == 0)):
        return False, "not(r1>=2 or r2=0)"
    if k == 1 and r1 < 2:
        return False, "k=1 & r1<2"
    return True, ""


def match_rules(h, blocks):
    """which macro rows match this canonical config"""
    k = len(blocks)
    r1 = blocks[0]
    r2 = blocks[1] if k >= 2 else None
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


def normalize(blocks):
    """drop trailing empty blocks (canonical form, rk>=1); keeps tape meaning."""
    b = list(blocks)
    while len(b) >= 2 and b[-1] == 0:
        b.pop()
    return b


def apply_rule(h, blocks):
    """returns (rule, h', blocks', cost); HALT row -> ('HALT', None, None, 9).
    Input must be a canonical I-config matching exactly one row."""
    ms = match_rules(h, blocks)
    assert len(ms) == 1, (h, blocks, ms)
    rule = ms[0]
    k = len(blocks)
    r1, r2 = blocks[0], (blocks[1] if k >= 2 else None)
    if rule == 'R1':
        nb = normalize([r1, r2 - 1] + blocks[2:])
        return rule, h + 1, nb, 2 * r1 + 3
    if rule == 'R2':
        return rule, h + 1, [r1 - 2, 0, 1], 2 * r1 + 3
    if rule == 'R3':
        nb = [r1 - 2, 0, blocks[2] + 1] + blocks[3:]
        return rule, h + 1, nb, 2 * r1 + 3
    if rule == 'R4':
        nb = [h - 1, 0, 1, blocks[2] + 1] + blocks[3:]
        return rule, 0, nb, h + 7
    if rule == 'R5':
        nb = normalize([h + blocks[2] + 3] + blocks[3:])
        return rule, 0, nb, h + 5
    return 'HALT', None, None, 9


# ================================================================ main orbit
print("=" * 78)
print("TASK A: raw TM from blank tape, 500000 steps")
MAX_STEPS = 500_000
tm = TM()
events = []            # (t, h, blocks) at every A0-read configuration
while tm.t < MAX_STEPS:
    if tm.state == 'A' and tm.read() == 0:
        support = sorted(q for q, v in tm.tape.items() if v == 1)
        h, blocks = parse_config(tm.tape, tm.head, support)
        events.append((tm.t, h, blocks))
    if not tm.step():
        break
print("ran %d steps, halted=%s, #A0-events=%d" % (tm.t, tm.halted, len(events)))

# --- anchor events (hand-derived twice, independent of any rule code)
ANCHORS = [(0, 0, None), (5, 0, [3]), (14, 1, [1, 0, 1]), (22, 0, [0, 0, 1, 2]),
           (27, 0, [4, 2]), (38, 1, [4, 1]), (49, 2, [4]), (60, 3, [2, 0, 1]),
           (67, 4, [0, 0, 2]), (76, 0, [9])]
anchor_ok = True
for i, (t, h, b) in enumerate(ANCHORS):
    got = events[i] if i < len(events) else "missing"
    if got != (t, h, b):
        anchor_ok = False
        fail(f"anchor event {i}: expected {(t, h, b)} got {got}")
print("first 10 A0 events:", events[:10])
print("anchors:", "OK" if anchor_ok else "MISMATCH")
print("claim 'blank tape reaches (0;3) at t=5':", "PASS" if events[1] == (5, 0, [3]) else "FAIL")
if events[1] != (5, 0, [3]):
    fail("blank tape anchor")

# --- verify invariant I + rules + costs on every consecutive event pair
n_I_ok = n_rule_ok = n_cost_ok = n_haltrow = 0
rule_histogram = {}
for i in range(1, len(events) - 1):
    t, h, b = events[i]
    if b is None:
        fail(f"event {i} t={t}: no blocks")
        continue
    anom = encoding_anomaly(b)
    if anom:
        fail(f"event t={t}: encoding anomaly {anom} config=({h};{b})")
        continue
    good, why = check_I(h, b)
    if not good:
        fail(f"event t={t}: invariant I violated: {why} config=({h};{b})")
        continue
    n_I_ok += 1
    if h == 0 and b[0] == 1 and len(b) >= 3 and b[1] == 0:
        n_haltrow += 1   # would have halted; must not happen since run continued
        fail(f"event t={t}: HALT-row config occurred but machine did not halt: (0;{b})")
        continue
    ms = match_rules(h, b)
    if len(ms) != 1:
        fail(f"event t={t}: matched {ms} for config ({h};{b})")
        continue
    rule, h2, b2, cost = apply_rule(h, b)
    rule_histogram[rule] = rule_histogram.get(rule, 0) + 1
    tn, hn, bn = events[i + 1]
    if (hn, normalize(bn)) != (h2, b2):
        fail(f"event t={t}: rule {rule} predicted ({h2};{b2}) but actual next is ({hn};{bn})")
        continue
    n_rule_ok += 1
    if tn - t != cost:
        fail(f"event t={t}: rule {rule} cost {cost} != actual delta {tn - t}")
    else:
        n_cost_ok += 1
print("invariant I held at %d/%d in-orbit events; rule predictions OK %d; cost formulas OK %d"
      % (n_I_ok, len(events) - 2, n_rule_ok, n_cost_ok))
print("rule histogram:", rule_histogram)

# ================================================================ synthetic tests
def synth(h, blocks):
    tm = TM()
    p = tm.head - 1
    for _ in range(h):
        tm.tape[p] = 1
        p -= 1
    q = 1
    for b in blocks:
        for _ in range(b):
            tm.tape[q] = 1
            q += 1
        q += 1                      # separator stays 0
    return tm


def run_to_next_A0(tm, cap=3_000_000):
    """execute the pending A0 transition, then run to the next A0-read or halt.
    Returns (kind, delta_t, (h, blocks)) with kind in {'EVT','HALT','CAP'}."""
    t0 = tm.t
    seq = [tm.state]
    tm.step()
    while True:
        if tm.halted:
            return 'HALT', tm.t - t0, (seq, None)
        if tm.state == 'A' and tm.read() == 0:
            support = sorted(q for q, v in tm.tape.items() if v == 1)
            h, blocks = parse_config(tm.tape, tm.head, support)
            return 'EVT', tm.t - t0, (h, blocks)
        if tm.t - t0 > cap:
            return 'CAP', tm.t - t0, (None, None)
        seq.append(tm.state)
        tm.step()


def verify_config(h, blocks, tag):
    good, why = check_I(h, blocks)
    if not good:
        return True      # claim only covers I-configs
    ms = match_rules(h, blocks)
    if len(ms) != 1:
        fail(f"[{tag}] coverage: ({h};{blocks}) matched {ms}")
        return False
    rule, h2, b2, cost = apply_rule(h, blocks)
    tm = synth(h, blocks)
    kind, dt, (hh, bb) = run_to_next_A0(tm)
    if rule == 'HALT':
        # 8 transitions execute (A,B,D,E,F,E,F,E), then F reads 0 and halts (9th read)
        if kind != 'HALT':
            fail(f"[{tag}] ({h};{blocks}) HALT row but run gave {kind}")
        elif dt != 8:
            fail(f"[{tag}] ({h};{blocks}) halt took {dt} transitions, not 8")
        return kind == 'HALT' and dt == 8
    if kind == 'HALT':
        fail(f"[{tag}] ({h};{blocks}) matched {rule} but machine halted after {dt} steps")
        return False
    if kind != 'EVT':
        fail(f"[{tag}] ({h};{blocks}) run hit cap")
        return False
    if (hh, normalize(bb)) != (h2, b2):
        fail(f"[{tag}] ({h};{blocks}) rule {rule} predicted ({h2};{b2}) got ({hh};{bb})")
        return False
    if dt != cost:
        fail(f"[{tag}] ({h};{blocks}) rule {rule} cost {cost} != {dt}")
        return False
    good2, why2 = check_I(h2, b2)
    if not good2:
        fail(f"[{tag}] output ({h2};{b2}) violates I ({why2})")
        return False
    return True


# exhaustive box over the decision boundary
box = 0
box_ok = 0
for h in range(0, 4):
    for k in range(1, 5):
        r1s = range(0, 6)
        r2s = [0, 1, 2, 3]
        r3s = range(1, 4)
        import itertools
        for r1 in r1s:
            for r2 in (r2s if k >= 2 else [None]):
                for rest in itertools.product(r3s, repeat=max(0, k - 2)):
                    blocks = [r1] + ([r2] if k >= 2 else []) + list(rest)
                    good, _ = check_I(h, blocks)
                    if not good:
                        continue
                    box += 1
                    if verify_config(h, blocks, "box"):
                        box_ok += 1
print("exhaustive small box: %d I-configs, %d fully verified (rules+costs+I of output)"
      % (box, box_ok))

# random larger configs, biased to the boundaries r1 in {0,1,2,3}, r2 in {0,1}
random.seed(20261012)
rnd = rnd_ok = 0
for _ in range(400):
    h = random.randint(0, 12)
    k = random.randint(1, 6)
    r1 = random.choice([0, 1, 2, 3] + list(range(0, 11)))
    r2 = random.choice([0, 1] + [random.randint(0, 9) for _ in range(3)])
    blocks = [r1, r2][:k] if k <= 2 else [r1, r2] + [random.randint(1, 9) for _ in range(k - 2)]
    good, _ = check_I(h, blocks)
    if not good:
        # nudge into I: keep r2>=1 or make r2=0 with k>=3
        blocks = [max(r1, 2), 0, 1] + [random.randint(1, 9) for _ in range(k - 1)]
        good, _ = check_I(h, blocks)
        if not good:
            continue
    rnd += 1
    if verify_config(h, blocks, "rand"):
        rnd_ok += 1
print("random configs: %d tested, %d fully verified" % (rnd, rnd_ok))

# ================================================================ claim (1)
print("-" * 78)
halting_rows = [k for k, v in TBL.items() if v is None]
print("halting transitions:", halting_rows, "-> HALT happens iff state F reads 0:",
      "PASS (definitional)" if halting_rows == [('F', 0)] else "FAIL")
into = {}
for (st, sym), v in TBL.items():
    if v:
        into.setdefault(v[2], []).append((st, sym, v[1]))
print("transitions into F:", into.get('F'))
print("=> F is entered only from E reading 0, moving Left (start of leftward E/F sweep):",
      "PASS" if into.get('F') == [('E', 0, 'L')] else "FAIL")

# forward direction of the equivalence: every config (0; 1,0,y+1,REST) halts
fwd_ok = True
fwd_n = 0
for y in range(0, 7):
    for REST in ([], [3], [2, 5], [1, 1, 1]):
        blocks = [1, 0, y + 1] + REST
        tm = synth(0, blocks)
        t0 = tm.t
        seq = [tm.state]
        heads = [tm.head]
        while not tm.halted and tm.t - t0 < 100:
            tm.step()
            seq.append(tm.state)
            heads.append(tm.head)
        fwd_n += 1
        # 8 transitions, states read A,B,D,E,F,E,F,E,F, halt on the 9th read (F reads 0);
        # the last four transitions E,F,E,F all move left (leftward E/F sweep)
        expect_states = list("ABDEFEFEF")
        if (not tm.halted or tm.t - t0 != 8 or seq[:9] != expect_states
                or any(heads[i + 1] != heads[i] - 1 for i in range(4, 8))):
            fwd_ok = False
            fail(f"(0;1,0,{y+1},{REST}) unexpected halt run: dt={tm.t-t0} seq={seq} heads={heads}")
print("forward: %d configs of HALT-row shape (0;1,0,y+1,REST): all halted after exactly 8"
      " transitions, tail of run is a leftward E/F sweep (E,F,E,F)" % fwd_n,
      "PASS" if fwd_ok else "FAIL")

# backward direction: every halting run's last A0-event has that shape,
# and every non-HALT-row I-config reaches its next A0 event without halting
# (this is exactly what the box+random+orbit rule verification establishes).
print("backward: covered by %d box + %d random + %d orbit configs: from every I-config "
      "the run reaches the next A0-event without halting unless the config is exactly "
      "the HALT row (0;1,0,y+1,REST) (see failures above if any)" % (box, rnd, n_I_ok))

print("=" * 78)
if FAILS:
    print("TASK A RESULT: FAIL (%d problems)" % len(FAILS))
else:
    print("TASK A RESULT: PASS")
