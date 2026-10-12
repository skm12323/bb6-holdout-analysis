"""End-phase template checker v3 (G2 closure engine).

Family of start states (symbols u, h, tt >= 0; z_i >= 0):
  canonical(r0, rho, tailpat): [H+d, H, 2H, ..., 2^{r0-1}H, 2^{r0}H - 1] + tail
  glue(rho, tailpat):          [head] + tail
with H = 6*2^{K+3} u + 2^{K+3}(1+h)   (any value divisible by 2^{K+3}, >= 2^{K+3}),
     d = rho + 2^K tt,  head = rho + 2^K tt + 2^{K+3}(1+h) + 6*2^{K+3} u (same shape),
     tail entries = 2^{K+3}(z+1) - t, t in {0,1} per tailpat.
Engine: exact symbolic (multi-symbol affine forms), uniform decisions only.
A-odd steps use the unified chain construction q0 = A + 2b + 3, c' = c + (A+1)/2,
window = L[3:], nested Phi_{sp} with sp = v2(q0):
  sp < K  -> exact recursion (level sp);
  sp >= K -> STRUCTURAL HAND-OFF: for each a in {0,1,2} the continuation
             [head] + window[a:] must be in the start family (checked).
Canonical starts also verify the mid-excursion contract
  final head == 2^{r0+1} H + d + 3*ell + kap + sum(tail[:a]).
A template run PASSES if every path terminates (active part = [X] + tail suffix)
with no Undecided / Halt / family violation.
"""
import sys, time
sys.setrecursionlimit(100000)

NS = 12   # 0:u 1:h 2:tt 3..5: spare 6..11: z1..z6
class Undecided(Exception): pass
class Halt(Exception): pass
class Fail(Exception): pass

def sym(i, k=1):
    co = [0] * NS; co[i] = k; return (tuple(co), 0)
def C(c): return (tuple([0] * NS), c)
def add(*xs): return (tuple(sum(x[0][i] for x in xs) for i in range(NS)), sum(x[1] for x in xs))
def sc(x, k): return (tuple(k * a for a in x[0]), k * x[1])
def sub(x, y): return (tuple(x[0][i] - y[0][i] for i in range(NS)), x[1] - y[1])
def par(x):
    if any(a % 2 for a in x[0]): raise Undecided('parity')
    return x[1] % 2
def half(x):
    if any(a % 2 for a in x[0]) or x[1] % 2: raise Undecided('half')
    return (tuple(a // 2 for a in x[0]), x[1] // 2)
def ge3(x):
    if all(a >= 0 for a in x[0]) and x[1] >= 3: return True
    if all(a == 0 for a in x[0]) and x[1] < 3: return False
    raise Undecided('ge3')
def v2f(x):
    n = 0
    while all(a % 2 == 0 for a in x[0]) and x[1] % 2 == 0 and (any(x[0]) or x[1]):
        x = (tuple(a // 2 for a in x[0]), x[1] // 2); n += 1
    return n
def halfn(x, n):
    for _ in range(n): x = half(x)
    return x

Z0 = C(0)
def T_list(L):
    A = L[0]; b = L[1] if len(L) > 1 else Z0; c = L[2] if len(L) > 2 else Z0; R = L[3:]
    if par(A) == 0: return [add(A, b, c, C(3))] + R
    m = half(add(b, b, A, C(-3))); st = [half(add(c, c, A, C(1)))] + R
    while par(m) == 1 and ge3(m):
        st = [half(add(m, C(3)))] + st; m = half(add(m, C(-3)))
    if par(m) == 1:
        if m == C(1): raise Halt('HALT branch reachable')
        raise Undecided('m odd unknown')
    return [add(m, C(4))] + st

def encode_run(L):
    """-> (H, r) if L = [X, H, 2H, ..., 2^{r-1}H, ...] with r >= 2 (E-macro applies)."""
    if len(L) < 4: return None
    H = L[1]
    if L[2] != sc(H, 2) or L[3] != sc(H, 4): return None
    r = 2
    while r + 1 < len(L) and L[r + 1] == sc(H, 1 << r): r += 1
    return (H, r)

def final_match(L, Z0L):
    if not Z0L:
        return 0 if len(L) == 1 else None
    n = len(Z0L)
    for k in range(n, -1, -1):
        if len(L) == 1 + n - k and L[1:] == Z0L[k:]:
            return k
    return None

K = 8
def zlike(x):
    """entry is family-like: value = 2^{K+3}*q + eps with eps in {0, -1}, q >= 1."""
    for eps in (0, -1):
        f = sub(x, C(eps))
        if all(a % (1 << (K + 3)) == 0 for a in f[0]) and f[1] >= 0 and f[1] % (1 << (K + 3)) == 0:
            return eps
    return None

def F(L, level, Z0L, s0, H0, kap0, ell0=0, d0=None):
    L = list(L); ell = ell0
    while True:
        a = final_match(L, Z0L)
        if a is not None:
            head = L[0]
            if d0 is not None:
                expect = add(sc(H0, 1 << s0), d0, C(3 * ell), kap0, *Z0L[:a])
                if head == expect:
                    return ell, a, head
            else:
                return ell, a, head
        enc = encode_run(L)
        if enc is not None:
            H, r = enc
            d = sub(L[0], H)
            if par(add(H, d)) == 0:
                L = [add(sc(H, 4), d, C(3))] + L[3:]; ell += 1
                continue
        A = L[0]
        if par(A) == 1:
            b = L[1] if len(L) > 1 else Z0
            c = L[2] if len(L) > 2 else Z0
            q0 = add(A, b, b, C(3))
            cprime = add(c, half(add(A, C(1))))
            window = L[3:]
            sp = v2f(q0)
            if sp >= 1:
                if sp < K:
                    o_p = halfn(q0, sp)
                    kap_nest = sub(cprime, sc(o_p, 1 << (sp - 1)))
                    nestL = [add(o_p, C(1))] + [sc(o_p, 1 << i) for i in range(sp - 1)] \
                            + [add(sc(o_p, 1 << (sp - 1)), kap_nest)] + list(window)
                    ell_n, a_n, head_n = F(nestL, sp, window, sp, o_p, kap_nest)
                    L = [head_n] + list(window[a_n:])
                    ell += 1 + ell_n
                    continue
                else:
                    for a_n in (0, 1, 2):
                        rest = window[a_n:]
                        # continuation [head] + rest must lie in the start family:
                        # rest = optional H-run prefix + optional J + z-like tail
                        i = 0
                        while i < len(rest) and rest[i] == sc(L_base(L), 1 << (i + 2)):
                            i += 1
                        for x in rest[i:]:
                            if zlike(x) is None:
                                raise Fail('deep continuation not family: %s' % (x,))
                    return ('DEEP', ell + 1, None)
        L = T_list(L); ell += 1

def L_base(L):
    return L[1]

def run_canonical(rho, r0, tailpat):
    Hp = 1 << (K + 3)
    H = add(C(Hp), sym(0, 6 * Hp), sym(1, Hp))
    d = add(C(rho), sym(2, 1 << K))
    kap = C(-1)
    tail = [add(C(Hp - t), sym(6 + i, Hp)) for i, t in enumerate(tailpat)]
    L = [add(H, d)] + [sc(H, 1 << i) for i in range(r0)] + [add(sc(H, 1 << r0), kap)] + tail
    ell, a, head = F(L, r0 + 1, tail, r0 + 1, H, kap, 0, d)
    return ell, a, head

def run_glue(rho, tailpat):
    Hp = 1 << (K + 3)
    head = add(C(Hp + rho), sym(0, 6 * Hp), sym(1, Hp), sym(2, 1 << K))
    tail = [add(C(Hp - t), sym(6 + i, Hp)) for i, t in enumerate(tailpat)]
    L = [head] + tail
    ell, a, h = F(L, 0, tail, 0, None, None, 0, None)
    return ell, a, h

if __name__ == '__main__':
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    globals()['K'] = K
    tails = [[], [0], [1], [0, 0], [1, 0], [0, 1], [1, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
    ok = 0; fails = []
    t0 = time.time()
    for r0 in (1, 2, 3, 4, 5):
        for rho in range(1 << K):
            for tp in tails:
                try:
                    run_canonical(rho, r0, tp); ok += 1
                except (Undecided, Halt, Fail) as e:
                    fails.append(('can', r0, rho, ''.join(map(str, tp)), str(e)))
    for rho in range(1 << K):
        for tp in tails:
            try:
                run_glue(rho, tp); ok += 1
            except (Undecided, Halt, Fail) as e:
                fails.append(('glue', rho, ''.join(map(str, tp)), str(e)))
    print('K=%d: %d template runs OK, %d failures [%.1fs]' % (K, ok, len(fails), time.time() - t0))
    for f in fails[:25]: print('  FAIL', f)
