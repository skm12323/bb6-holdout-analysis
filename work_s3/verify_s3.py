"""verify_s3.py -- block-level (Sigma-machine) reduction of BB(6) holdout
1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB, built on S1's phase system (D:/math_cc/work_s1).
Run:  python verify_s3.py [N_raw_steps=3e6] [N_macro_events=2e6]
Sections: 1 linear forms + symbolic run-length tape  2 S1 phase rules executed symbolically
3 abstract Sigma-machine  4 Sigma-step theorem (exhaustive symbolic case split)
5 integer machine / raw TM  6 checks.   Units: TM steps.
"""
import sys
sys.path.insert(0, 'D:/math_cc/work_s1')
import verify_s1 as V1          # importing re-runs all of S1's symbolic rule proofs (PASS lines)
T = V1.T
if not V1.OK: raise SystemExit("S1 rule proofs failed")

# =====================================================================================
# 1-2.  Symbolic engine
# =====================================================================================
class Lin(dict):
    def __init__(s, *a, **k):
        super().__init__(*a, **k)
        for kk in [kk for kk, v in s.items() if v == 0]: del s[kk]
    @staticmethod
    def c(v): return Lin({'': v})
    def __add__(s, o):
        if isinstance(o, int): o = Lin.c(o)
        d = dict(s)
        for k, v in o.items(): d[k] = d.get(k, 0) + v
        return Lin(d)
    __radd__ = __add__
    def __sub__(s, o):
        if isinstance(o, int): o = Lin.c(o)
        return s + Lin({k: -v for k, v in o.items()})
    def __mul__(s, m): return Lin({k: v*m for k, v in s.items()})
    __rmul__ = __mul__
    def const(s): return s.get('', 0)
    def isconst(s): return all(k == '' for k in s)
    def subst(s, p, e):
        if p not in s: return Lin(s)
        return Lin({k: v for k, v in s.items() if k != p}) + e * s[p]
    def __hash__(s): return hash(tuple(sorted(s.items())))
    def __repr__(s):
        ks = sorted(s, key=lambda k: (k == '', k))
        out = ''
        for k in ks:
            v = s[k]
            t = str(v) if k == '' else (k if v == 1 else f"{v}{k}")
            out += ('+' + t) if out and v > 0 else t
        return out.replace('+-', '-') or '0'

class Split(Exception):
    def __init__(s, p): s.p = p
class Expand(Exception): pass
class Fail(Exception): pass

def ge(L, k):
    """decide L>=k for all parameter values >= 0 (each param has lower bound 0 after shifting)."""
    if any(v < 0 for kk, v in L.items() if kk != ''): raise Fail(f"negative coefficient in {L}")
    if L.const() >= k: return True
    if L.isconst(): return False
    raise Split(sorted(kk for kk in L if kk != '')[0])
def zero(L): return not ge(L, 1)
ONE = Lin.c(1)
INF = 'INF'

class Tape:
    """hb = head bit; Lt, Rt = token lists nearest-first. token: ('r',bit,Lin) | ('B',) blank | ('T',) unknown stack."""
    def __init__(s, Lt, hb, Rt): s.Lt, s.hb, s.Rt = list(Lt), hb, list(Rt)
    def copy(s): return Tape(s.Lt, s.hb, s.Rt)
    def subst(s, p, e):
        f = lambda t: ('r', t[1], t[2].subst(p, e)) if t[0] == 'r' else t
        s.Lt = [f(t) for t in s.Lt]; s.Rt = [f(t) for t in s.Rt]
    @staticmethod
    def norm(lst):
        out = []
        for t in lst:
            if t[0] == 'r' and t[2].isconst() and t[2].const() == 0: continue
            if out and t[0] == 'r' and out[-1][0] == 'r' and out[-1][1] == t[1]:
                out[-1] = ('r', t[1], out[-1][2] + t[2]); continue
            if out and t[0] == 'B' and out[-1][0] == 'r' and out[-1][1] == 0:
                out[-1] = t; continue
            out.append(t)
        return out
    def normalize(s): s.Lt = Tape.norm(s.Lt); s.Rt = Tape.norm(s.Rt)
    @staticmethod
    def expose(lst, k, start=0):
        """make lst[start..k-1] single cells"""
        i = start
        while i < k:
            t = lst[i]
            if t[0] == 'T': raise Expand()
            if t[0] == 'B': lst[i:i+1] = [('r', 0, ONE), t]
            else:
                if not ge(t[2], 1): raise Fail("empty token")
                if not (t[2].isconst() and t[2].const() == 1):
                    rem = t[2] - 1
                    lst[i:i+1] = [('r', t[1], ONE)] + ([] if (rem.isconst() and rem.const() == 0) else [('r', t[1], rem)])
            i += 1
    @staticmethod
    def scan(lst, j, b):
        """maximal run of bit b from index j outward; returns (length Lin|INF, index of first other token)"""
        L = Lin.c(0)
        while True:
            t = lst[j]
            if t[0] == 'T': raise Expand()
            if t[0] == 'B': return (INF if b == 0 else L), j
            if t[1] != b:
                if t[2].isconst() and t[2].const() == 0: j += 1; continue
                ge(t[2], 1); return L, j      # possibly-empty run of the other bit: decide first
            L = L + t[2]; j += 1
    def move_left(s, j):   # head to cell Lt[j] (must be single)
        s.Rt = list(reversed(s.Lt[:j])) + [('r', s.hb, ONE)] + s.Rt
        s.hb = s.Lt[j][1]; s.Lt = s.Lt[j+1:]
    def move_right(s, j):
        s.Lt = list(reversed(s.Rt[:j])) + [('r', s.hb, ONE)] + s.Lt
        s.hb = s.Rt[j][1]; s.Rt = s.Rt[j+1:]
    def show(s):
        def tk(t):
            if t[0] == 'B': return '..'
            if t[0] == 'T': return 'W'
            L = t[2]
            return f"{t[1]}" if (L.isconst() and L.const() == 1) else f"{t[1]}^{{{L}}}"
        return ' '.join([tk(t) for t in reversed(s.Lt)] + [f"[{s.hb}]"] + [tk(t) for t in s.Rt])

def bit(t): return t[1]
def setb(lst, i, b): lst[i] = ('r', b, ONE)

def step(tp, ph):
    """apply one S1 phase rule symbolically. returns (new phase, rule name, steps Lin)."""
    tp.normalize()
    L, R = tp.Lt, tp.Rt
    if ph == 'K':
        Tape.expose(R, 1); Tape.expose(L, 1)
        assert tp.hb == 0 and bit(R[0]) == 0
        if bit(L[0]) == 1:                                   # Kb
            setb(L, 0, 0); setb(R, 0, 1); tp.move_left(0)
            return 'P', 'Kb', Lin.c(5)
        n, j = Tape.scan(L, 1, 1)                            # Ka(n)
        Tape.expose(L, j + 1, j)                              # L[j] = p (a 0)
        assert bit(L[j]) == 0
        Tape.expose(R, 2)
        hb = bit(R[1])
        tp.Lt = [('r', 1, n), ('r', 0, ONE), ('r', 1, Lin.c(3))] + L[j+1:]
        tp.hb = hb; tp.Rt = R[2:]
        return 'S', 'Ka', 6*n + 8
    if ph == 'S':
        if tp.hb == 1:
            m0, j = Tape.scan(R, 0, 1); m = m0 + 1
            Tape.expose(R, j + 3, j); tp.move_right(j)
        else:
            m = Lin.c(0); Tape.expose(R, 2)
        R = tp.Rt; Tape.expose(R, 2)
        if bit(R[0]) == 0: return 'K', 'Sa', m
        if bit(R[1]) == 1:
            setb(R, 0, 0); setb(R, 1, 0); tp.move_right(0)
            return 'K', 'Sb', m + 5
        return 'HALT', 'SH', m + 2
    if ph == 'P':
        Tape.expose(R, 2)
        assert tp.hb == 0 and bit(R[0]) == 0 and bit(R[1]) == 1
        i, j = Tape.scan(L, 0, 0)
        if i == INF: return 'INFLEFT', 'INF', Lin.c(0)
        Tape.expose(L, j + 3, j)                              # L[j]=z (a 1), L[j+1], L[j+2] = z-1, z-2
        c1, c2 = bit(L[j + 1]), bit(L[j + 2])
        if c1 == 1 and c2 == 1:                               # P1
            for k in (0, 1, 2): setb(L, j + k, 0)
            tp.move_left(j + 1); return 'K', 'P1', i + 6
        if c1 == 1:                                           # P2
            Tape.expose(R, 3)
            nh = bit(R[2])
            tp.Lt = [('r', 0, ONE), ('r', 1, i + 5)] + L[j+3:]
            tp.hb = nh; tp.Rt = R[3:]
            return 'S', 'P2', 2*i + 11
        if c2 == 0: return 'HALT', 'PH', i + 3
        Tape.expose(L, j + 4, j + 3); c3 = bit(L[j + 3])
        if c3 == 1:                                           # P3
            setb(L, j+3, 0); setb(L, j+2, 0); setb(L, j+1, 1)
            tp.move_left(j + 3); return 'P', 'P3', i + 6
        Tape.expose(L, j + 5, j + 4); c4 = bit(L[j + 4])
        if c4 == 1:                                           # P4
            for k in (2, 3, 4): setb(L, j + k, 0)
            setb(L, j+1, 1); tp.move_left(j + 3); return 'K', 'P4', i + 6
        for k in (2, 3, 4): setb(L, j + k, 1)                 # P5
        setb(L, j+1, 0)
        if zero(i): return 'K', 'P5', i + 10                  # head stays on x
        # head to z+1 = farthest cell of the i-run
        run = L[:j]; tot = i
        new = [('r', 0, tot - 1)] if not zero(tot - 1) else []
        tp.Lt = new + [('r', 0, ONE)] + L[j:]
        tp.move_left(len(new)); return 'K', 'P5', i + 10
    raise Fail(ph)

def is_one(t, b, L=None):
    return t[0] == 'r' and t[1] == b and (L is None or (t[2].isconst() and t[2].const() == L))

def parse_stack(R):
    """R = token list (nearest first) after the m-run; returns (stack, tail) or None"""
    st = []; k = 0
    while True:
        t = R[k]
        if t[0] in 'BT':
            return (st, t[0]) if k == len(R) - 1 else None
        if not (t[0] == 'r' and t[1] == 0 and t[2].isconst() and t[2].const() in (1, 2)): return None
        if k + 1 >= len(R): return None
        u = R[k+1]
        if not (u[0] == 'r' and u[1] == 1): return None
        st.append((t[2].const(), u[2])); k += 2

def match_S(tp):
    """Sigma(p,N,m;stack) := .. 1^p 0 1^N [A]1^m stack   (phase S)"""
    tp.normalize(); L = tp.Lt
    for t in L + Tape.norm([('r', tp.hb, ONE)] + tp.Rt):
        if t[0] == 'r': ge(t[2], 1)          # every run must be decided non-empty (else Split)
    if len(L) == 4 and L[0][0] == 'r' and L[0][1] == 1 and is_one(L[1], 0, 1) and L[2][0] == 'r' and L[2][1] == 1 and L[3][0] == 'B':
        N, p = L[0][2], L[2][2]
    elif len(L) == 3 and is_one(L[0], 0, 1) and L[1][0] == 'r' and L[1][1] == 1 and L[2][0] == 'B':
        N, p = Lin.c(0), L[1][2]
    else: return None
    R = Tape.norm([('r', tp.hb, ONE)] + tp.Rt)
    if R[0][0] == 'r' and R[0][1] == 1: m = R[0][2]; R = R[1:]
    else: m = Lin.c(0)
    ps = parse_stack(R)
    if ps is None: return None
    return dict(p=p, N=N, m=m, stack=ps[0], tail=ps[1])

def substitute(tp, p, e):
    tp = tp.copy(); tp.subst(p, e); return tp

def Stape(p, N, m, stack=(), tail='T'):
    Lt = ([('r', 1, N)] if not (N.isconst() and N.const() == 0) else []) + [('r', 0, ONE), ('r', 1, p), ('B',)]
    R = [('r', 1, m)] if not (m.isconst() and m.const() == 0) else []
    for g, d in stack: R += [('r', 0, Lin.c(g)), ('r', 1, d)]
    R.append((tail,))
    R = Tape.norm(R)
    Tape.expose(R, 1)
    return Tape(Lt, R[0][1], R[1:])

# =====================================================================================
# 3.  The abstract Sigma-machine (rules G0..Gs2, SH, PH), generic over int and Lin
# =====================================================================================
class Undecided(Exception): pass
def GE(x, k):
    if isinstance(x, int): return x >= k
    try: return ge(x, k)
    except Split: raise Undecided(f"{x}>={k}")
def EQ(x, k):
    if isinstance(x, int): return x == k
    if x.isconst(): return x.const() == k
    if GE(x, k + 1): return False
    raise Undecided(f"{x}=={k}")

def sigma_rule(p, N, m, W):
    """One macro step of the abstract machine.  W = stack, TOP FIRST, list of (g,d) with g in {1,2},
    d>=1; the blank below the stack acts as a top (2,0).  Returns (rule, (p',N',m',W') or None, steps)."""
    s = N + m
    if W: (g, d), rest = W[0], list(W[1:])
    else: (g, d), rest = (2, 0), []
    if g == 1:
        if EQ(d, 1): return 'SH', None, m + 2
        return 'G2', (p + 3, s, d - 2, rest), m + 6*s + 13
    if GE(s, 4): return 'G1', (p + 3, s - 4, 0 * s, [(2, d + 1)] + rest), m + 6*s - 5
    if EQ(s, 0): return 'G0', (3 + 0 * p, p, d, rest), 6*p + 8
    if EQ(s, 3): return 'Gs3', (p + 5, 0 * p, d, rest), m + 16
    if EQ(s, 1):
        if GE(p, 7): return 'Gs1', (6 + 0 * p, p - 7, 0 * p, [(2, 1), (1, d + 1)] + rest), m + 12*p - 21
        if EQ(p, 6): return 'Gs1_6', (8, 0, 0, [(1, d + 1)] + rest), m + 54
        if EQ(p, 5): return 'PH', None, m + 46
        if EQ(p, 4): return 'Gs1_4', (3, 3, 0, [(1, 1), (1, d + 1)] + rest), m + 72
        if EQ(p, 3): return 'Gs1_3', (3, 3, 0, [(1, d + 1)] + rest), m + 46
    if EQ(s, 2):
        if GE(p, 5): return 'Gs2', (3 + 0 * p, p - 5, 0 * p, [(2, 2), (2, d + 1)] + rest), m + 6*p - 5
        if EQ(p, 4): return 'Gs2_4', (5, 0, 1, [(2, d + 1)] + rest), m + 22
        if EQ(p, 3): return 'PH', None, m + 14
    raise Undecided(f"no rule for p={p} s={s}")

def L_(x): return x if isinstance(x, Lin) else Lin.c(x)
def leq(a, b): return Lin(L_(a) - L_(b)) == Lin()

# =====================================================================================
# 4.  Proof of the Sigma-step theorem: exhaustive symbolic exploration
# =====================================================================================
def explore_S(tp0, maxev=60, maxsubs=40):
    """Run S1's phase system symbolically from a Sigma tape until the next Sigma tape (after >=1 rule)
    or a halt.  Undecided comparisons split a parameter (q=0 | q->q+1); reading the unknown stack
    tail splits it (blank | 0 1^(d+1) W | 0 0 1^(d+1) W).  Leaves: (kind, start, final, steps, path)."""
    fresh = [0]; leaves = []; work = [tp0]
    while work:
        start = work.pop()
        tp = start.copy(); ph = 'S'; t = Lin.c(0); path = []
        try:
            while True:
                if len(path) > maxev: leaves.append(('TOOLONG', start, tp, t, path)); break
                if path and ph == 'S':
                    r = match_S(tp.copy())
                    if r: leaves.append(('S', start, r, t, path)); break
                nph, name, dt = step(tp, ph)
                path.append(name); t = t + dt; ph = nph
                if ph in ('HALT', 'INFLEFT'): leaves.append((ph, start, name, t, path)); break
        except Split as e:
            q = e.p
            work.append(substitute(start, q, Lin.c(0)))
            work.append(substitute(start, q, Lin({q: 1, '': 1})))
        except Expand:
            fresh[0] += 1; d = f"d{fresh[0]}"
            k = next(i for i, x in enumerate(start.Rt) if x[0] == 'T')
            for seq in ([('B',)], [('r', 0, ONE), ('r', 1, Lin({d: 1, '': 1})), ('T',)],
                        [('r', 0, Lin.c(2)), ('r', 1, Lin({d: 1, '': 1})), ('T',)]):
                work.append(Tape(start.Lt, start.hb, start.Rt[:k] + seq + start.Rt[k+1:]))
    return leaves

def check_leaf(kind, start, fin, t):
    s0 = match_S(start.copy())
    if s0 is None: return False, "start not Sigma"
    try: rule, out, steps = sigma_rule(s0['p'], s0['N'], s0['m'], s0['stack'])
    except Undecided as e: return False, f"undecided {e}"
    if not leq(steps, t): return False, f"steps {steps} vs {t}"
    if kind == 'HALT':
        want = {'SH': 'SH', 'PH': 'PH'}[rule] if rule in ('SH', 'PH') else None
        return (want == fin), rule
    if kind != 'S' or out is None: return False, f"{kind} vs rule {rule}"
    p2, N2, m2, W2 = out
    if not (leq(p2, fin['p']) and leq(N2, fin['N']) and leq(m2, fin['m'])): return False, f"{rule}: pNm {out} vs {fin}"
    if fin['tail'] != s0['tail']: return False, "tail"
    if len(W2) != len(fin['stack']): return False, f"{rule}: stack {W2} vs {fin['stack']}"
    for (g, d), (g2, d2) in zip(W2, fin['stack']):
        if g != g2 or not leq(d, d2): return False, f"{rule}: entry {(g, d)} vs {(g2, d2)}"
    return True, rule

# =====================================================================================
# 5.  Integer abstract machine, rendering, raw TM
# =====================================================================================
def render(p, N, m, W):
    """Sigma tape as a string from the leftmost 1, with the head cell marked '|'."""
    right = '1' * m
    for g, d in W: right += '0' * g + '1' * d
    right += '000'
    return '1' * p + '0' + '1' * N + '|' + right

def raw_strings(times):
    want = sorted(set(times)); tp = {}; pos = 0; st = 'A'; t = 0; out = {}; wi = 0
    while wi < len(want):
        if t == want[wi]:
            ones = [k for k, v in tp.items() if v]
            lo = min(ones + [pos]); hi = max(ones + [pos]) + 3
            out[t] = (st, ''.join(('|' if k == pos else '') + str(tp.get(k, 0)) for k in range(lo, hi + 1)))
            wi += 1; continue
        tr = T[(st, tp.get(pos, 0))]
        if tr is None: break
        tp[pos] = tr[0]; pos += tr[1]; st = tr[2]; t += 1
    return out

def trunc(s):
    """strip trailing zeros beyond head"""
    h = s.index('|'); body = s.rstrip('0')
    return body if len(body) > h + 1 else s[:h + 2]

# =====================================================================================
# 6.  Main
# =====================================================================================
OK = True
def check(c, msg):
    global OK
    print(("PASS " if c else "FAIL ") + msg); OK &= bool(c)
V = lambda n, k=0: Lin({n: 1, '': k})

def accel_run(n_macro, want_trace=False):
    """integer Sigma-machine from Sigma(3,0,0;[]) at t=8, with G1 bursts accelerated (closed form).
    yields per macro event (rule, p, N, m, W(top first), t)."""
    p, N, m, W, t = 3, 0, 0, [], 8
    for _ in range(n_macro):
        s = N + m; top = W[0] if W else (2, 0)
        if top[0] == 2 and s >= 4:
            k = s // 4
            t += m + 6*k*s - 12*k*(k - 1) - 5*k
            p += 3*k; N, m = s - 4*k, 0
            W = [(2, top[1] + k)] + W[1:]
            yield ('G1^%d' % k, p, N, m, W, t); continue
        rule, out, st = sigma_rule(p, N, m, W)
        t += st
        if out is None: yield (rule, None, None, None, None, t); return
        p, N, m, W = out
        yield (rule, p, N, m, W, t)

if __name__ == '__main__':
    NRAW = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
    NMAC = int(sys.argv[2]) if len(sys.argv) > 2 else 2_000_000
    # ---- 6.1 engine = S1 phase system (Class-C validation of the implementation)
    names = []
    class Rec(dict):
        def __missing__(s, k): return 0
        def __setitem__(s, k, v): names.append(k); dict.__setitem__(s, k, v)
    V1.macro_run(400_000, None, Rec())
    tp = Stape(Lin.c(3), Lin.c(0), Lin.c(0), [], 'B'); ph = 'S'; got = []
    # S1's run starts at K on a blank tape; its first rule is Ka(0) giving Sigma(3,0,0) at t=8
    while len(got) < len(names) - 1:
        ph, nm, _ = step(tp, ph)
        got.append({'P5': 'P5'}.get(nm, nm))
    check(got == names[1:len(got) + 1], f"symbolic engine on concrete tapes reproduces S1 macro_run rule sequence ({len(got)} rules)")

    # ---- 6.2 Sigma-step theorem
    allrules = set(); nleaves = 0; bad = []
    for N in (Lin.c(0), V('N', 1)):
        for m in (Lin.c(0), V('m', 1)):
            for top in ('B', 1, 2):
                st = [] if top == 'B' else [(top, V('d', 1))]
                lv = explore_S(Stape(V('p', 3), N, m, st, 'B' if top == 'B' else 'T'))
                for kind, start, fin, t, path in lv:
                    nleaves += 1
                    ok, info = check_leaf(kind, start, fin, t)
                    if ok: allrules.add(info)
                    else: bad.append((kind, start.show(), info, path))
    for b in bad[:5]: print("   ", b)
    check(not bad, f"Sigma-step theorem: {nleaves} symbolic leaves (12 start shapes, all p>=3,N,m,d>=0) all equal sigma_rule; rules hit: {sorted(allrules)}")

    # ---- 6.3 base
    raw8 = raw_strings([8])[8]
    check(raw8[0] == 'A' and trunc(raw8[1]) == trunc(render(3, 0, 0, [])), "base: raw TM at t=8 is Sigma(3,0,0;[])")

    # ---- 6.4 G1^k closed form (induction step = rule G1 with m'=0; sum checked)
    okk = all(sum(((m if j == 0 else 0) + 6*(s - 4*j) - 5) for j in range(k)) == m + 6*k*s - 12*k*(k-1) - 5*k
              for s in range(4, 80) for k in range(1, s // 4 + 1) for m in (0, 3))
    check(okk, "G1^k: (p,s,0|m,(2,d)) -> (p+3k, s-4k, 0, (2,d+k)), steps m+6ks-12k(k-1)-5k")

    # ---- 6.5 invariants (finite enumeration complementing the symbolic argument in RULES.md)
    Pset = lambda p: p in (3, 6) or p >= 8
    inv_ok = True; three_two = False; new11 = []
    for p in [x for x in range(3, 120) if Pset(x)]:
        for s in range(0, 12):
            if p == 3 and s == 2: continue                 # excluded by the invariant itself
            for W in ([], [(2, 1)], [(2, 5)], [(1, 2)], [(1, 7)]):
                for N in range(0, s + 1):
                    r, out, _ = sigma_rule(p, N, s - N, W)
                    if r in ('PH', 'Gs1_4', 'Gs2_4'): inv_ok = False
                    if out is None: continue
                    if not Pset(out[0]): inv_ok = False
                    if out[0] == 3 and out[1] + out[2] == 2: three_two = True
                    if (1, 1) in out[3][:2] and (1, 1) not in W: new11.append((r, p, s, W))
    check(inv_ok and not three_two, "Inv := p in P={3,6,8,9,..} and (p,s)!=(3,2) is closed under every rule; PH, Gs1_4, Gs2_4 never fire under Inv")
    check(all(r[0] in ('Gs1', 'Gs1_6', 'Gs1_3') and r[2] == 1 and r[3] == [] for r in new11) and new11,
          "a (1,1) entry is created only by Gs1/Gs1_6/Gs1_3 at s=1 with EMPTY stack")

    # ---- 6.6 raw TM vs abstract machine (Class-A for the finite range)
    ev = []
    p, N, m, W, t = 3, 0, 0, [], 8
    ev.append((t, render(p, N, m, W)))
    while t < NRAW:
        rule, out, st = sigma_rule(p, N, m, W); t += st
        if out is None: break
        p, N, m, W = out; ev.append((t, render(p, N, m, W)))
    raw = raw_strings([x[0] for x in ev if x[0] <= NRAW])
    mism = [x for x in ev if x[0] <= NRAW and not (raw.get(x[0], ('?', ''))[0] == 'A' and trunc(raw[x[0]][1]) == trunc(x[1]))]
    check(not mism, f"raw TM == abstract Sigma-machine at all {len([x for x in ev if x[0] <= NRAW])} macro boundaries, t <= {NRAW}")

    # ---- 6.7 long accelerated run [Class-C]
    from collections import Counter
    cnt = Counter(); Z = 0; smallZ = []; halted = None; lastZs = None; maxdepth = 0
    for rule, p, N, m, W, t in accel_run(NMAC):
        cnt[rule.split('^')[0]] += 1
        if p is None: halted = (rule, t); break
        maxdepth = max(maxdepth, len(W))
        if not W:
            Z += 1
            if N + m <= 15: smallZ.append((Z, p, N + m))
    print(f"[Class-C] {NMAC} accelerated macro events, reached t = {t:.3e} TM steps; halted: {halted}")
    print(f"[Class-C] rule counts {dict(cnt)}; max stack depth {maxdepth}; empty-stack (Z) states {Z}")
    print(f"[Class-C] Z states with s<=15 (index, p, s): {smallZ}")
    print("ALL PASS" if OK else "SOME FAIL")
