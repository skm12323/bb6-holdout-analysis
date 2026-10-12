"""verify_s1.py -- symbolic macro-rule proofs + raw-vs-abstract cross-check for
BB(6) holdout 1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB.  Units: TM steps.
Run:  python verify_s1.py [N_raw_steps]   (default 3_000_000)
"""
import sys, itertools
from collections import Counter
TM = "1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB"
def parse(s):
    T = {}
    for k, g in enumerate(s.split('_')):
        st = "ABCDEF"[k]
        for r in (0, 1):
            t = g[3*r:3*r+3]
            T[(st, r)] = None if t == '---' else (int(t[0]), 1 if t[1] == 'R' else -1, t[2])
    return T
T = parse(TM)
OK = True
def check(c, msg):
    global OK
    print(("PASS " if c else "FAIL ") + msg)
    OK &= bool(c)

# ---------------------------------------------------------------- 1. halting lemma
predC = [k for k, v in T.items() if v and v[2] == 'C']
predB = [k for k, v in T.items() if v and v[2] == 'B']
undefined = [k for k, v in T.items() if v is None]
check(undefined == [('C', 0)], "only undefined transition is C0")
check(sorted(predC) == [('B', 0), ('B', 1)], "C entered only from B0 (1LC), B1 (0RC)")
check(sorted(predB) == [('A', 0), ('F', 1)], "B entered only from A0 (1RB), F1 (1LB)")
def win(cells, pos, st, maxsteps):
    cells = dict(cells); n = 0
    while n < maxsteps:
        tr = T[(st, cells[pos])]
        if tr is None: return 'halt'
        cells[pos] = tr[0]; pos += tr[1]; st = tr[2]; n += 1
    tr = T[(st, cells[pos])]
    return 'halt' if tr is None else 'run'
for st in "ABCDEF":
    for bits in itertools.product((0, 1), repeat=7):
        cells = {i - 3: b for i, b in enumerate(bits)}
        h = win(cells, 0, st, 2) == 'halt'
        b = lambda k: bits[3 + k]
        pred = (st == 'A' and b(0) == 0 and b(1) == 1 and b(2) == 0) or \
               (st == 'F' and b(0) == 1 and b(-1) == 0 and b(-2) == 0) or \
               (st == 'B' and b(0) == 0 and b(-1) == 0) or \
               (st == 'B' and b(0) == 1 and b(1) == 0) or (st == 'C' and b(0) == 0)
        if h != pred: check(False, f"halt pattern mismatch {st} {bits}")
check(True, "exhaustive: reaches C0 within 2 transitions iff [A]010 | 00[F]1 | 0[B]0 | [B]10 | [C]0")

# ---------------------------------------------------------------- 2. symbolic run-length prover
# tokens: ('c',bit) concrete | ('r',bit,p) run bit^p, p>=0 ARBITRARY | ('?',) unknown cell (reading it = failure)
def lin_add(a, b):
    d = dict(a)
    for k, v in b.items(): d[k] = d.get(k, 0) + v
    return {k: v for k, v in d.items() if v}
def parse_pat(s):
    toks = []; head = None; st = None
    for w in s.split():
        if w.startswith('['):
            st = w[1]; w = w[3:]; head = len(toks)
        if w == '?': toks.append(('?',))
        elif '^' in w: b, p = w.split('^'); toks.append(('r', int(b), p))
        else: toks.append(('c', int(w)))
    return toks, head, st
def prove(lhs, rhs, steps_expected, maxev=500):
    """Run lhs symbolically.  A run token is crossed in one event only if the
    transition on its bit keeps state AND direction (so it is valid for every p>=0,
    including p=0).  Head leaving the window or reading '?' = failure, so the result
    holds in every tape context.  Stops at first arrival on rhs head token in rhs state."""
    toks, h, st = parse_pat(lhs); steps = {}; d = 0
    if rhs != 'HALT': rt, rh, rs = parse_pat(rhs)
    for ev in range(maxev):
        if rhs != 'HALT' and ev > 0 and st == rs and h == rh:
            return (toks == rt and steps == steps_expected), steps
        if h < 0 or h >= len(toks): return False, 'left window'
        tk = toks[h]
        if tk[0] == '?': return False, 'read unknown'
        if tk[0] == 'r':
            tr = T[(st, tk[1])]
            if d == 0 and tr is not None: d = tr[1]   # run under head at start: direction set by it
            if tr is None or tr[2] != st or tr[1] != d: return False, 'non-uniform run'
            toks[h] = ('r', tr[0], tk[2]); steps = lin_add(steps, {tk[2]: 1}); h += d; continue
        tr = T[(st, tk[1])]
        if tr is None: return (rhs == 'HALT' and steps == steps_expected), steps
        toks[h] = ('c', tr[0]); d = tr[1]; h += d; st = tr[2]; steps = lin_add(steps, {'1': 1})
    return False, 'too long'
def S(c, **k):
    d = {'1': c} if c else {}
    d.update({a: b for a, b in k.items() if b}); return d

RULES = [  # name, lhs, rhs, steps (linear form; '1' = constant)
 ('alpha', '1 0 [A]0 0',              '0 [A]0 0 1',               S(5)),
 ('beta',  '0 0 [A]0 0 ?',            '1 1 1 0 [A]?',             S(8)),
 ('crossA', '[A]1^m ?',               '1^m [A]?',                 S(0, m=1)),
 ('Kb',    '1 [A]0 0',                '[F]0 0 1',                 S(5)),
 ('Sa',    '[A]1^m 0 0',              '1^m [A]0 0',               S(0, m=1)),
 ('Sb',    '[A]1^m 0 1 1',            '1^m 0 [A]0 0',             S(5, m=1)),
 ('SH',    '[A]1^m 0 1 0',            'HALT',                     S(2, m=1)),
 ('P1',    '1 1 1 0^i [F]0 0 1',      '0 [A]0 0 0^i 0 0 1',       S(6, i=1)),
 ('P2',    '0 1 1 0^i [F]0 0 1 ?',    '1 1 1 1^i 1 1 0 [A]?',     S(11, i=2)),
 ('PH',    '0 0 1 0^i [F]0 0 1',      'HALT',                     S(3, i=1)),
 ('P3',    '1 1 0 1 0^i [F]0 0 1',    '[F]0 0 1 1 0^i 0 0 1',     S(6, i=1)),
 ('P4',    '1 0 1 0 1 0^i [F]0 0 1',  '0 [A]0 0 1 1 0^i 0 0 1',   S(6, i=1)),
 ('P5_i0', '0 0 1 0 1 [F]0 0 1',      '1 1 1 0 1 [A]0 0 1',       S(10)),        # i = 0
 ('P5_i>0', '0 0 1 0 1 0 0^k [F]0 0 1', '1 1 1 0 1 [A]0 0^k 0 0 1', S(11, k=1)),   # i = k+1
]
for name, l, r, s in RULES:
    ok, got = prove(l, r, s)
    check(ok, f"rule {name}: {l}  ->  {r}   steps={s}")
# Ka(n): 0 1^n 0 [A]0 0 ?  ->  1 1 1 0 1^n [A]?   in 6n+8 steps (all n>=0).
# Proof: alpha is window-closed, so 1^k 1 0[A]00 W -> 1^k 0[A]00 1 W for any k,W; induction
# gives 1^n 0[A]00 -> 0[A]00 1^n (5n); left neighbour is the leading 0 -> beta (8) -> crossA (n).
def concrete(bits, pos, st, until):
    cells = dict(enumerate(bits)); n = 0
    while not until(pos, st, n):
        tr = T[(st, cells[pos])]
        if tr is None: return None
        cells[pos] = tr[0]; pos += tr[1]; st = tr[2]; n += 1
    return cells, n
for n in range(0, 41):
    r = concrete([0] + [1]*n + [0, 0, 0] + [None], n + 2, 'A',
                 lambda p, s, k: p == n + 4 and s == 'A' and k > 0)
    if not (r and [r[0][i] for i in range(n + 4)] == [1, 1, 1, 0] + [1]*n and r[1] == 6*n + 8):
        check(False, f"Ka n={n}")
check(True, "Ka(n) concrete instances n=0..40 = 6n+8 steps (general n: alpha-induction+beta+crossA)")

# ---------------------------------------------------------------- 3. abstract (macro) machine
class Tape(dict):
    def __missing__(s, k): return 0
def macro_run(maxsteps, trace=None, stats=None):
    """Phases: K = A at x reading 0 with x+1=0;  S = A at x moving right;
    P = F at x reading 0 with x+1=0, x+2=1.  Every transition is one of RULES / Ka."""
    tp = Tape(); ph = 'K'; x = 0; t = 0
    while t < maxsteps:
        if trace is not None: trace.append((t, ph, x, {k: v for k, v in tp.items() if v}))
        if ph == 'K':
            assert tp[x] == 0 and tp[x+1] == 0
            if tp[x-1] == 1:                              # Kb
                tp[x-1] = 0; tp[x+1] = 1; ph = 'P'; x -= 1; t += 5; stats['Kb'] += 1
            else:                                         # Ka(n)
                n = 0
                while tp[x-2-n] == 1: n += 1
                L = x - n - 2
                for k, v in enumerate([1, 1, 1, 0] + [1]*n): tp[L+k] = v
                ph = 'S'; x = L + 4 + n; t += 6*n + 8; stats['Ka'] += 1
        elif ph == 'S':
            m = 0
            while tp[x+m] == 1: m += 1
            y = x + m
            if tp[y+1] == 0: ph = 'K'; x = y; t += m; stats['Sa'] += 1
            elif tp[y+2] == 1:
                tp[y+1] = 0; tp[y+2] = 0; ph = 'K'; x = y+1; t += m + 5; stats['Sb'] += 1
            else: return ('HALT', t + m + 2)
        else:
            assert tp[x] == 0 and tp[x+1] == 0 and tp[x+2] == 1
            i = 0
            while tp[x-1-i] == 0:
                i += 1
                if i > 10**6: return ('INF-left', t)
            z = x - 1 - i
            a1, a2, a3, a4 = tp[z-1], tp[z-2], tp[z-3], tp[z-4]
            if a1 == 1 and a2 == 1:
                tp[z-2] = tp[z-1] = tp[z] = 0; ph = 'K'; x = z-1; t += 6 + i; stats['P1'] += 1
            elif a1 == 1:
                for c in range(z-2, x+2): tp[c] = 1
                tp[x+2] = 0; ph = 'S'; x += 3; t += 11 + 2*i; stats['P2'] += 1
            elif a2 == 0: return ('HALT', t + 3 + i)
            elif a3 == 1:
                tp[z-3] = 0; tp[z-2] = 0; tp[z-1] = 1; x = z-3; t += 6 + i; stats['P3'] += 1
            elif a4 == 1:
                tp[z-4] = tp[z-3] = tp[z-2] = 0; tp[z-1] = 1; ph = 'K'; x = z-3; t += 6 + i; stats['P4'] += 1
            else:
                tp[z-4] = tp[z-3] = tp[z-2] = 1; tp[z-1] = 0; ph = 'K'; x = z+1; t += 10 + i; stats['P5'] += 1
    return ('RUN', t)

def raw_snapshots(times):
    want = set(times); end = max(times); tp = {}; p = 0; s = 'A'; t = 0; out = {}
    while True:
        if t in want: out[t] = ({k: v for k, v in tp.items() if v}, p, s)
        if t >= end: return out
        tr = T[(s, tp.get(p, 0))]
        if tr is None: return out
        tp[p] = tr[0]; p += tr[1]; s = tr[2]; t += 1

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
    trace = []; stats = Counter()
    res = macro_run(N, trace, stats)
    raw = raw_snapshots([tt for tt, *_ in trace])
    hs = {'K': 'A', 'S': 'A', 'P': 'F'}
    bad = sum(1 for tt, ph, x, tape in trace if raw.get(tt) != (tape, x, hs[ph]))
    check(bad == 0, f"raw vs abstract: all {len(trace)} macro boundaries up to t={trace[-1][0]} identical (tape, head, state)")
    print("macro result:", res)
    print("[Class-C] rule usage:", dict(stats))
    print("ALL PASS" if OK else "SOME FAIL")
