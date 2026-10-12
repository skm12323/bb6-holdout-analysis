# verify_t1.py -- symbolic proofs + raw-vs-abstract cross-check for BB(6) holdout
# 1RB1LE_1LB1LC_1RD0LE_---0RB_1RF1LA_0RA0RD.  Run: python verify_t1.py [N_raw_steps]
"""Symbolic run-length prover for TM 1RB1LE_1LB1LC_1RD0LE_---0RB_1RF1LA_0RA0RD.

Expressions: affine forms over nonnegative integer variables, dict {var: coef, 1: const}.
Config: (L, s, R).  L = list of runs, nearest-to-head LAST; R = list of runs, head reads
the first cell of R[0].  Beyond the lists the tape is 0^inf ('end' flags) or an opaque
symbolic context (no 'end'): reading past an opaque context end is an error.
A step needs the head run length provably >= 1 (all coefs >= 0 and const >= 1);
otherwise an explicit CaseSplit exception is raised -- no silent assumptions.
"""
TM = {'A': [(1, 1, 'B'), (1, -1, 'E')], 'B': [(1, -1, 'B'), (1, -1, 'C')],
      'C': [(1, 1, 'D'), (0, -1, 'E')], 'D': [None, (0, 1, 'B')],
      'E': [(1, 1, 'F'), (1, -1, 'A')], 'F': [(0, 1, 'A'), (0, 1, 'D')]}


class CaseSplit(Exception):
    pass


class Halt(Exception):
    pass


def E(c=0, **v):
    d = {k: x for k, x in v.items() if x}
    if c:
        d[1] = c
    return d


def add(a, b, k=1):
    r = dict(a)
    for x, y in b.items():
        r[x] = r.get(x, 0) + k * y
        if r[x] == 0:
            del r[x]
    return r


def sub(a, b):
    return add(a, b, -1)


def nonneg(a):
    return all(v >= 0 for v in a.values())


def pos(a):
    return nonneg(a) and a.get(1, 0) >= 1


def mono(x, y):
    if x == 1:
        return y
    if y == 1:
        return x
    t = tuple(sorted((x if isinstance(x, tuple) else (x,)) + (y if isinstance(y, tuple) else (y,))))
    return t


def mul(a, b):
    r = {}
    for x, u in a.items():
        for y, v in b.items():
            r = add(r, {mono(x, y): u * v})
    return r


def subst(a, env):
    """Polynomial substitution; tuple keys are monomials (products of variables)."""
    r = {1: a.get(1, 0)} if a.get(1, 0) else {}
    for k, v in a.items():
        if k == 1:
            continue
        term = {1: v}
        for x in (k if isinstance(k, tuple) else (k,)):
            term = mul(term, env[x] if x in env else {x: 1})
        r = add(r, term)
    return r


def show(a):
    if not a:
        return '0'
    parts = []
    for k, v in sorted(a.items(), key=lambda kv: (kv[0] == 1, str(kv[0]))):
        kk = '*'.join(k) if isinstance(k, tuple) else k
        parts.append(str(v) if k == 1 else (kk if v == 1 else '%d%s' % (v, kk)))
    return '+'.join(parts).replace('+-', '-')


def norm(runs):
    out = []
    for s, e in runs:
        if not e:
            continue
        if out and out[-1][0] == s:
            out[-1] = (s, add(out[-1][1], e))
        else:
            out.append((s, e))
    return out


class Cfg:
    def __init__(s, L, st, R, lend=True, rend=True):
        s.L, s.st, s.R, s.lend, s.rend = norm(L), st, norm(R), lend, rend

    def key(s):
        f = lambda rs: tuple((a, tuple(sorted(e.items(), key=str))) for a, e in rs)
        return (f(s.L), s.st, f(s.R), s.lend, s.rend)

    def __eq__(s, o):
        return isinstance(o, Cfg) and s.key() == o.key()

    def __repr__(s):
        f = lambda rs: ' '.join('%d^%s' % (a, show(e)) for a, e in rs)
        return ('0^inf ' if s.lend else '.. ') + f(s.L) + ' <%s> ' % s.st + f(s.R) + (' 0^inf' if s.rend else ' ..')


def step(c):
    """One concrete TM step on a symbolic config. Returns new config."""
    R = list(c.R)
    if not R:
        if not c.rend:
            raise CaseSplit('read past opaque right context', {})
        R = [(0, {1: 1})]
    sym, e = R[0]
    if not pos(e):
        raise CaseSplit('head run %s may be empty' % show(e), e)
    rest = sub(e, {1: 1})
    R = ([(sym, rest)] if rest else []) + R[1:]
    tr = TM[c.st][sym]
    if tr is None:
        raise Halt(repr(c))
    w, d, ns = tr
    L = list(c.L)
    if d == 1:
        L = L + [(w, {1: 1})]
    else:
        R = [(w, {1: 1})] + R
        if not L:
            if not c.lend:
                raise CaseSplit('move past opaque left context', {})
            L = [(0, {1: 1})]
        s2, e2 = L[-1]
        if not pos(e2):
            raise CaseSplit('left run %s may be empty' % show(e2), e2)
        r2 = sub(e2, {1: 1})
        L = L[:-1] + ([(s2, r2)] if r2 else [])
        R = [(s2, {1: 1})] + R
    return Cfg(L, ns, R, c.lend, c.rend)


class Lemma:
    """lhs/rhs: (Lpat, state, Rpat) runs whose exprs are affine in lemma vars.
    The outermost run of each side pattern may be matched against a longer config run
    only if flagged 'open' (the excess stays as context)."""

    def __init__(s, name, lhs, rhs, cost, lend=False, rend=False):
        s.name, s.lhs, s.rhs, s.cost, s.lend, s.rend = name, lhs, rhs, cost, lend, rend

    def cfg(s, side, env):
        Lp, st, Rp = s.lhs if side == 0 else s.rhs
        f = lambda rs: [(a, subst(e, env)) for a, e in rs]
        return Cfg(f(Lp), st, f(Rp), s.lend, s.rend)


def match_runs(pat, runs, env):
    """pat and runs ordered from head outward. Pattern exprs: const or var+const (var once).
    Last pattern run may be 'open': matched as a prefix (excess returned)."""
    if len(runs) < len(pat):
        return None
    excess = None
    for i, (ps, pe) in enumerate(pat):
        rs, re_ = runs[i]
        if ps != rs:
            return None
        pe = subst(pe, env)
        vs = [k for k in pe if k != 1 and k not in env and not isinstance(k, tuple)]
        last = i == len(pat) - 1
        if vs:
            v = vs[0]
            val = sub(re_, {kk: vv for kk, vv in pe.items() if kk != v})
            coef = pe[v]
            if any(x % coef for x in val.values()):
                return None
            val = {kk: x // coef for kk, x in val.items()}
            if not nonneg(val):
                return None
            env[v] = val
        else:
            diff = sub(re_, pe)
            if diff:
                if not (last and nonneg(diff)):
                    return None
                excess = (rs, diff)
    return env, excess


def apply_lemma(c, lm, allowed=None):
    Lp, st, Rp = lm.lhs
    if c.st != st:
        return None
    if lm.lend and not (c.lend and len(c.L) == len(Lp)):
        return None
    if lm.rend and not (c.rend and len(c.R) == len(Rp)):
        return None
    env = {}
    m = match_runs(Rp, c.R, env)
    if m is None:
        return None
    env, exR = m
    m = match_runs(list(reversed(Lp)), list(reversed(c.L)), env)
    if m is None:
        return None
    env, exL = m
    if allowed is not None and not allowed(env):
        return None
    L2, st2, R2 = lm.rhs
    newL = list(reversed(list(reversed(c.L))[len(Lp):]))
    if exL:
        newL = newL + [exL]
    newL += [(a, subst(e, env)) for a, e in L2]
    newR = [(a, subst(e, env)) for a, e in R2]
    if exR:
        newR.append(exR)
    newR += c.R[len(Rp):]
    for a, e in newL + newR:
        if not nonneg(e):
            return None
    return Cfg(newL, st2, newR, c.lend, c.rend), subst(lm.cost, env)


def run(c, target, lemmas, ih=None, maxsteps=100000, trace=False):
    """Advance until config == target. Returns accumulated step count (affine expr).
    ih = (lemma, allowedfn) for the induction hypothesis."""
    t = {}
    for _ in range(maxsteps):
        if target is not None and c == target:
            return t
        done = False
        for lm, allowed in ([ih] if ih else []) + [(l, None) for l in lemmas]:
            r = apply_lemma(c, lm, allowed)
            if r and r[0] == c:
                r = None  # identity instance (zero-length parameter): never applied
            if r:
                c, k = r
                t = add(t, k)
                done = True
                if trace:
                    print('  [%s] %r' % (lm.name, c))
                break
        if not done:
            c = step(c)
            t = add(t, {1: 1})
            if trace:
                print('   . %r' % c)
    raise RuntimeError('target not reached: %r' % c)


def prove(lm, lemmas, ind=None, trace=False, cases=None):
    """Prove lemma: direct symbolic run if ind is None, else induction on variable ind
    (base ind=0; step ind->ind+1 using the IH only at exactly ind)."""
    if ind is None:
        cases = [(c, None) for c in (cases or [{}])]
    else:
        cases = [({ind: {}}, None), ({ind: {ind: 1, 1: 1}}, (lm, lambda env: env.get(ind) == {ind: 1}))]
    log = []
    work = list(cases)
    while work:
        env, ih = work.pop()
        start, goal = lm.cfg(0, env), lm.cfg(1, env)
        try:
            t = run(start, goal, lemmas, ih, trace=trace)
        except CaseSplit as ex:
            # explicit case split on a variable of the possibly-empty run: v=0 | v=v+1
            e = ex.args[1]
            if not [k for k in e if k != 1]:
                raise
            v = sorted(k for k in e if k != 1)[0]
            if len(log) + len(work) > 64:
                raise
            for val in ({}, {v: 1, 1: 1}):
                work.append(({**{k: subst(x, {v: val}) for k, x in env.items()}, v: subst(env.get(v, {v: 1}), {v: val})}, ih))
            continue
        want = subst(lm.cost, env) if lm.cost is not None else None
        if lm.cost is None:
            print('  case', {k: show(x) for k, x in env.items()}, 'cost', show(t))
        elif t != want:
            raise RuntimeError('%s case %s: cost %s != %s' % (lm.name, {k: show(x) for k, x in env.items()}, show(t), show(want)))
        log.append(env)
    return log


# =====================================================================================
# PART 2.  Sweep lemmas (Class-A, induction), W-rule table (Class-A, symbolic, all cases)
# =====================================================================================
nv = lambda c=0, k=1: E(c, n=k)
LD = Lemma('D-shift', ([], 'D', [(1, nv(2))]), ([(1, nv(1))], 'D', [(1, E(1))]), E(3, n=3))
LE = Lemma('EA-sweep', ([(1, nv(2, 2))], 'E', [(1, E(1))]), ([], 'E', [(1, nv(3, 2))]), E(2, n=2))
LA = Lemma('AE-sweep', ([(1, nv(2, 2))], 'A', [(1, E(1))]), ([], 'A', [(1, nv(3, 2))]), E(2, n=2))
LIB = [LD, LE, LA]


def Wcfg(X, B, opaque):
    """W(X;B) = 0^inf 1^X <E on 0> 1^B0 0 1^B1 0 ... ; opaque: an unknown tail follows
    the '0' after the last listed block (any tail, incl. 0^inf); else 0^inf right after."""
    R = [(0, E(1))]
    for i, b in enumerate(B):
        R += [(1, b)] + ([(0, E(1))] if i < len(B) - 1 else [])
    if opaque:
        R += [(0, E(1))]
    return Cfg([(1, X)], 'E', R, True, not opaque)


def isW(c):
    return (c.st == 'E' and c.R and c.R[0][0] == 0 and c.lend
            and (not c.L or (len(c.L) == 1 and c.L[0][0] == 1)))


def explore(c0, env=None, depth=0):
    """Symbolically run from c0 (under substitution env) to the next W-config,
    splitting v=0 | v->v+1 whenever a possibly-empty run is read. Returns leaves."""
    env = env or {}
    c = Cfg([(a, subst(e, env)) for a, e in c0.L], c0.st, [(a, subst(e, env)) for a, e in c0.R], c0.lend, c0.rend)
    t = {}
    first = True
    try:
        for _ in range(100000):
            if not first and isW(c):
                return [(env, c, t)]
            first = False
            for lm in LIB:
                r = apply_lemma(c, lm)
                if r and not r[0] == c:
                    c, k = r
                    t = add(t, k)
                    break
            else:
                c = step(c)
                t = add(t, {1: 1})
        raise RuntimeError('no W reached')
    except CaseSplit as ex:
        e = ex.args[1]
        vs = sorted(k for k in e if k != 1)
        if not vs or depth > 10:
            raise
        v = vs[0]
        out = []
        for val in ({}, {v: 1, 1: 1}):
            ne = {k: subst(x, {v: val}) for k, x in env.items()}
            ne[v] = subst(env.get(v, {v: 1}), {v: val})
            out += explore(c0, ne, depth + 1)
        return out
    except Halt:
        return [(env, 'HALT', t)]


# classes: X in {X0:0, Xo:2x+1, Xe:2x+2}; Y in {0,1,2,3,4y+4,4y+5,4y+6,4y+7};
# z in {none, 2z+1, 2z+2}; w in {none, w+1 (then an arbitrary tail)}; w only if z present.
XC = {'X0': E(0), 'Xo': E(1, x=2), 'Xe': E(2, x=2)}
YC = {'0': E(0), '1': E(1), '2': E(2), '3': E(3), '4y+4': E(4, y=4), '4y+5': E(5, y=4),
      '4y+6': E(6, y=4), '4y+7': E(7, y=4)}
ZC = {'-': None, 'zo': E(1, z=2), 'ze': E(2, z=2)}
WC = {'-': None, 'w': E(1, w=1)}


def expected(xc, yc, zc, X, Y, z, w):
    """The RULE TABLE (also stated in RULES.md).  Returns (X', B', cost) or 'HALT'.
    z, w are 0 ({}) when absent; the tail beyond w is untouched."""
    W_ = [w] if w is not None else []
    z0 = z if z is not None else {}
    w0 = w if w is not None else {}
    zodd = zc == 'zo'
    if yc == '0':
        if z is not None:
            return add(X, E(1)), [z] + W_, E(3)
        if xc == 'X0':
            return E(0), [E(0), E(1), E(3)], E(18)
        if xc == 'Xo':
            return E(0), [add(X, E(1)), E(3)], add(X, E(15))
        return E(0), [E(0), add(X, E(1)), E(3)], add(X, E(18))
    if yc == '1':
        return 'HALT'
    if yc == '2':
        if xc == 'X0':
            pre = [E(0)] if zodd else []
            return E(0), pre + [add(z0, E(2)), add(w0, E(3))], add(add({}, z0, 4), E(27 if zodd else 24))
        if xc == 'Xo':
            return E(0), [sub(X, E(1)), add(z0, E(4))] + W_, add(X, E(7))
        return E(0), [E(0), sub(X, E(1)), add(z0, E(4))] + W_, add(X, E(10))
    if yc == '3':
        sodd = (xc == 'Xo') != zodd
        s = add(X, z0)
        pre = [E(0)] if sodd else []
        return E(0), pre + [add(s, E(2)), add(w0, E(3))], add(add(X, z0, 4), E(26 if sodd else 23))
    if yc in ('4y+4', '4y+6'):
        return add(X, E(1)), [sub(Y, E(4)), add(z0, E(3))] + W_, sub(add({}, Y, 4), E(3))
    # Y odd >= 5
    if xc == 'Xo':
        return E(0), [add(X, E(1)), sub(Y, E(4)), add(z0, E(3))] + W_, add(add(X, Y, 4), E(1))
    return E(0), [E(0), add(X, E(1)), sub(Y, E(4)), add(z0, E(3))] + W_, add(add(X, Y, 4), E(4))


def prove_table():
    n = 0
    for xc, X in XC.items():
        for yc, Y in YC.items():
            for zc, z in ZC.items():
                for wc, w in WC.items():
                    if z is None and w is not None:
                        continue
                    B = [Y] + ([z] if z is not None else []) + ([w] if w is not None else [])
                    opaque = w is not None
                    start = Wcfg(X, B, opaque)
                    exp = expected(xc, yc, zc, X, Y, z, w)
                    for env, res, t in explore(start):
                        if exp == 'HALT':
                            assert res == 'HALT', (xc, yc, zc, wc, res)
                            assert t == {1: 2}, t   # 2 steps, then D reads 0 (3rd step = halt)
                        else:
                            X2, B2, cost = exp
                            want = Wcfg(subst(X2, env), [subst(b, env) for b in B2], opaque)
                            assert res != 'HALT', (xc, yc, zc, wc, env)
                            assert res == want, (xc, yc, zc, wc, env, res, want)
                            assert t == subst(cost, env), (xc, yc, zc, wc, env, show(t), show(subst(cost, env)))
                        n += 1
    return n


# =====================================================================================
# PART 3.  Abstract map F (integer version of the table) and checks
# =====================================================================================
def F(X, B):
    """One W-rule. State (X, B): X>=0, B nonempty, B[0]>=0, B[i]>=1 (i>=1). None = halts."""
    Y = B[0]; z = B[1] if len(B) > 1 else 0; w = B[2] if len(B) > 2 else 0
    T = B[3:]; R = B[2:]
    if Y == 0:
        if len(B) > 1:
            return X + 1, B[1:], 3
        return (0, [0, X + 1, 3], X + 18) if X % 2 == 0 else (0, [X + 1, 3], X + 15)
    if Y == 1:
        return None
    if Y == 2:
        if X == 0:
            return 0, ([0] if z % 2 else []) + [z + 2, w + 3] + T, 4 * z + (27 if z % 2 else 24)
        return (0, [X - 1, z + 4] + R, X + 7) if X % 2 else (0, [0, X - 1, z + 4] + R, X + 10)
    if Y == 3:
        s = X + z
        return 0, ([0] if s % 2 else []) + [s + 2, w + 3] + T, X + 4 * z + (26 if s % 2 else 23)
    if Y % 2 == 0:
        return X + 1, [Y - 4, z + 3] + R, 4 * Y - 3
    return (0, [X + 1, Y - 4, z + 3] + R, X + 4 * Y + 1) if X % 2 else (0, [0, X + 1, Y - 4, z + 3] + R, X + 4 * Y + 4)


def F_table_consistency():
    """[Class-C support] integer F agrees with the symbolic table on many instances."""
    import itertools
    cnt = 0
    for X, Y, z, w in itertools.product(range(0, 9), range(0, 14), [None, 1, 2, 3, 4, 7], [None, 1, 5]):
        if z is None and w is not None:
            continue
        Bt = [Y] + ([z] if z else []) + ([w] if w else [])
        xc = 'X0' if X == 0 else ('Xo' if X % 2 else 'Xe')
        yc = str(Y) if Y < 4 else ['4y+4', '4y+5', '4y+6', '4y+7'][Y % 4]
        zc = '-' if z is None else ('zo' if z % 2 else 'ze')
        e = expected(xc, yc, zc, E(X), E(Y), E(z) if z else None, E(w) if w else None)
        r = F(X, Bt)
        if e == 'HALT':
            assert r is None
        else:
            X2, B2, c = e
            assert r == (X2.get(1, 0), [b.get(1, 0) for b in B2], c.get(1, 0)), (X, Bt, r, e)
        cnt += 1
    return cnt


TMT = {'A': [(1, 1, 'B'), (1, -1, 'E')], 'B': [(1, -1, 'B'), (1, -1, 'C')],
       'C': [(1, 1, 'D'), (0, -1, 'E')], 'D': [None, (0, 1, 'B')],
       'E': [(1, 1, 'F'), (1, -1, 'A')], 'F': [(0, 1, 'A'), (0, 1, 'D')]}


def raw_W_events(N):
    """[Class-C] direct simulation; list of (t, X, B) at every W-configuration."""
    tape = bytearray(N + 10); p = N // 2; s = 'A'; t = 0; lo = hi = p; out = []
    tr01 = bytes.maketrans(b'\0\1', b'01')
    while t < N:
        r = tape[p]
        if r == 0 and s == 'E':
            a = bytes(tape[lo:p]).translate(tr01).decode().lstrip('0')
            if '0' not in a:
                b = bytes(tape[p + 1:hi + 1]).translate(tr01).decode().rstrip('0')
                out.append((t, len(a), [len(u) for u in b.split('0')] if b else []))
        tr = TMT[s][r]
        if tr is None:
            out.append((t, 'HALT', None)); break
        tape[p] = tr[0]; p += tr[1]; s = tr[2]; t += 1; lo = min(lo, p); hi = max(hi, p)
    return out


def base_lemma():
    """[Class-B] blank tape, state A: the first W-config occurs at exactly t=12 and is W(0;0,3)."""
    ev = raw_W_events(13)
    assert ev[0] == (12, 0, [0, 3]), ev
    return True


def cross_check(N):
    ev = raw_W_events(N)
    st = (ev[0][1], ev[0][2]); t = ev[0][0]; k = 0
    for (t1, X1, B1) in ev[1:]:
        r = F(*st)
        assert r is not None
        t += r[2]; st = (r[0], r[1])
        assert (t1, X1, B1) == (t, st[0], st[1]), ((t1, X1, B1), (t, st))
        k += 1
    return k, t


def halting_predecessor_check(M=40):
    """[Class-C support for the Class-A table argument in RULES.md sec.5]: exhaustive over small
    inputs, checks each predecessor claim used in the halting criterion."""
    import itertools
    for X, Y, z in itertools.product(range(M), range(M), range(1, 12)):
        for B in ([Y], [Y, z], [Y, z, 5]):
            r = F(X, B)
            if r is None:
                continue
            X2, B2, _ = r
            if B2[0] == 1:
                assert Y == 0 and B[1] == 1
            if B2[0] == 0 and len(B2) > 1 and B2[1] == 1:
                assert (X, B) == (0, [0]) or (X == 0 and Y % 2 and Y >= 5) or (X == 2 and Y == 2), (X, B)
            if X2 == 0:
                assert B2[0] % 2 == 0 and B2 != [0]
            if X2 == 2 and B2[0] == 2:
                assert X == 1 and (Y == 6 or B[:2] == [0, 2])
            assert not (X2 == 1 and B2[:2] == [0, 2])
            if X2 == 1 and B2[0] == 6:
                assert (X == 0 and Y == 10) or (X == 0 and B[:2] == [0, 6])
            if X2 == 0 and B2[:2] == [0, 6]:
                assert X == 1 and B[:2] == [2, 2]
            assert not (X2 == 1 and B2[:2] == [2, 2])
    return True


def criterion_check():
    """[Class-C] for every F-output S1 from small inputs: the orbit halts (within 3000 F-steps)
    iff it visits (0,[10,..]) or S1 is one of the non-reachable-again special states."""
    import itertools
    def special(S):
        X, B = S
        return ((X == 1 and B[:2] == [2, 2]) or (X == 0 and B[:2] == [0, 6]) or (X == 1 and B[0] == 6)
                or (X == 2 and B[0] == 2) or B[0] == 1 or (B[0] == 0 and B[1:2] == [1]))
    n = 0
    for X in range(14):
        for B in itertools.chain(([y] for y in range(30)), ([y, z] for y in range(30) for z in range(1, 15))):
            r = F(X, list(B))
            if r is None:
                continue
            S = (r[0], r[1]); first = special(S); hit = halted = False
            for _ in range(3000):
                hit |= S[0] == 0 and S[1][0] == 10
                r = F(*S)
                if r is None:
                    halted = True; break
                S = (r[0], r[1])
                if max(S[1]) > 10 ** 6:
                    break
            assert halted == (hit or first), (X, B)
            n += 1
    return n


def checkpoint_check():
    """[Class-C support] derived rules: R1-chain (1,[Y,z]+T) -> (1,[Y-2,z+6]+T) in 8Y+16 steps (Y odd>=5);
    C(b even; c) := (1,[3,b,c]) -> (1,[3, 3b+c+3]) (c=0 if absent), checked against F."""
    for Y in range(5, 60, 2):
        for z in range(1, 9):
            S = (1, [Y, z, 4]); t = 0
            for _ in range(3):
                r = F(*S); t += r[2]; S = (r[0], r[1])
            assert S == (1, [Y - 2, z + 6, 4]) and t == 8 * Y + 16
    for b in range(2, 80, 2):
        for c in (None, 3, 6):
            S = (1, [3, b] + ([c] if c else [])); c0 = c or 0
            while True:
                r = F(*S); S = (r[0], r[1])
                if S[0] == 1 and S[1][0] == 3:
                    break
            assert S == (1, [3, 3 * b + c0 + 3]), (b, c, S)
    return True


if __name__ == '__main__':
    import sys
    for lm in LIB:
        prove(lm, [], 'n')
    print('[Class-A] sweep lemmas D-shift / EA-sweep / AE-sweep proved by induction')
    print('[Class-A] W-rule table: %d symbolic leaves verified (all parameter values)' % prove_table())
    print('[Class-C] integer F agrees with table on %d instances' % F_table_consistency())
    print('[Class-B] base lemma:', base_lemma())
    print('[Class-C] halting-predecessor table check:', halting_predecessor_check())
    print('[Class-C] halting criterion check on %d small orbits' % criterion_check())
    print('[Class-C] R1-chain / even-checkpoint rule check:', checkpoint_check())
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3 * 10 ** 6
    k, t = cross_check(N)
    print('[Class-C] raw TM vs abstract F: %d consecutive W-transitions identical incl. step counts, up to t=%d' % (k, t))
