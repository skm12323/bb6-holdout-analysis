"""End-phase template checker via multi-symbol exact symbolic runs (G2 closure engine).

For every residue class rho of d mod 2^K, start run-length r0 in 1..5, tail
pattern pi: the end phase of the excursion from canonical
  (H+d, H, 2H, ..., 2^{r0-1}H, 2^{r0}H - 1, tail)
with H = 6*2^{K+3} u + 3*2^{K+3} + 2^{K+4} h, d = rho + 2^K tt  (symbols u,h,tt >= 0)
is run exactly and symbolically; every decision must be uniform in all symbols.
Tail entries: 2^{K+3}(z+1) - t, t in {0,1} (clean / J-type residue mod 2^K).
Nested calls with sp = v2(q0) <= K recurse directly (small level); sp > K branch
over a in {0,1,2} with ell = fresh e-symbol (>= 0), head = q0 + 3(1+e) + (c' - q0/2 + 1)
+ sum(window[:a])  [the F-contract head with K' = c' - q0/2 + 1].
A run PASSES if all branches reach the verified F-contract end without
Undecided/Halt/Fail.
"""
import sys
sys.setrecursionlimit(100000)

NS = 12   # 0:u 1:h 2:tt 3:e1 4:e2 5:e3 6..11: z1..z6
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

def encode(L):
    if len(L) < 3: return None
    H = L[1]
    if L[2] != sc(H, 2): return None
    r = 1
    while r + 1 < len(L) and L[r + 1] == sc(H, 1 << r): r += 1
    if r + 1 >= len(L): return None
    return (H, sub(L[0], H), r, sub(L[r + 1], sc(H, 1 << r)))

def final_match(L, Z0L):
    if not Z0L:
        return 0 if len(L) == 1 else None
    n = len(Z0L)
    for k in range(n, -1, -1):
        if len(L) == 1 + n - k and L[1:] == Z0L[k:]:
            return k
    return None

class Branch(Exception):
    def __init__(self, conts):
        self.conts = conts   # list of (newL, ell_consumed)

K = 8
def F(L, level, Z0L, s0, H0, kap0, ell0=0, d0=None):
    L = list(L); ell = ell0
    while True:
        a = final_match(L, Z0L)
        if a is not None:
            head = L[0]
            if d0 is None:
                expect = add(sc(H0, 1 << s0), C(3 * ell), C(1), kap0, *Z0L[:a])
            else:
                expect = add(sc(H0, 1 << s0), d0, C(3 * ell), kap0, *Z0L[:a])
            if head == expect:
                return ell, a, head
        enc = encode(L) if len(L) >= 3 else None
        if enc is not None:
            H, d, r, kap = enc
            pA = par(add(H, d))
            if pA == 0 and r >= 2:
                L = [add(sc(H, 4), d, C(3))] + L[3:]; ell += 1
                continue
            if pA == 1:
                if r >= 2:
                    q0 = add(sc(H, 3), d, C(3))
                    cprime = add(sc(H, 2), half(add(H, d, C(1))))
                elif r == 1:
                    q0 = add(sc(H, 3), d, C(3))
                    cprime = add(sc(H, 2), kap, half(add(H, d, C(1))))
                else:
                    q0 = add(sc(H, 3), sc(kap, 2), d, C(3))
                    cprime = add(L[2] if len(L) > 2 else Z0, half(add(H, d, C(1))))
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
                        # deep branch: sp >= K. The continuation [head] + window[a:]
                        # (head residue unknown = any class, since ell(sp) is unknown)
                        # is covered by the outer start enumeration PROVIDED its
                        # structure belongs to the start family; verify that here.
                        for a_n in (0, 1, 2):
                            rest = window[a_n:]
                            check_family(rest, H)
                        return ('DEEP', ell + 1)
        L = T_list(L); ell += 1
F.esym = [0]

def check_family(rest, H):
    """continuation rest (= window[a:]) must be: canonical run + J + z-tail, or J + z-tail,
    or z-tail only -- all covered by the start enumeration (canonical or glue starts)."""
    def is_mult(x, i):
        return x == sc(H, 1 << i)
    def is_big_clean(x):
        f = x
        return all(a % (1 << (K + 3)) == 0 for a in f[0]) and f[1] >= 0
    def is_Jtype(x):
        f = sub(x, C(-1))
        return all(a % (1 << (K + 3)) == 0 for a in f[0]) and f[1] >= (1 << (K + 3)) - 1
    i = 0
    while i < len(rest) and is_mult(rest[i], i + 2):
        i += 1
    # rest[:i] canonical run entries 4H..2^{i+1}H
    if i < len(rest):
        if not is_Jtype(rest[i]):
            raise Fail('continuation not in family: entry %d not J-type: %s' % (i, rest[i]))
        for x in rest[i + 1:]:
            if not (is_Jtype(x) or is_big_clean(x)):
                raise Fail('continuation tail entry not family: %s' % (x,))
    return True

def run_template(rho, r0, tailpat):
    Hp = 1 << (K + 3)
    H = add(C(3 * Hp), sym(0, 6 * Hp), sym(1, 1 << (K + 4)))
    d = add(C(rho), sym(2, 1 << K))
    kap = C(-1)
    tail = []
    for i, t in enumerate(tailpat):
        tail.append(add(C((1 << (K + 3)) - t), sym(6 + i, 1 << (K + 3))))
    L = [add(H, d)] + [sc(H, 1 << i) for i in range(r0)] + [add(sc(H, 1 << r0), kap)] + tail
    F.esym[0] = 0
    stack = [(L, 0)]
    while stack:
        Lt, e0 = stack.pop()
        try:
            F(Lt, r0 + 1, tail, r0 + 1, H, kap, e0, d)
        except Branch as br:
            for (nl, ne) in br.conts:
                stack.append((nl, ne))
    return True

if __name__ == '__main__':
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    globals()['K'] = K
    tails = [[], [0], [1], [0, 0], [1, 0], [0, 1], [1, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
    ok = 0; fails = []
    import time
    t0 = time.time()
    for r0 in (1, 2, 3, 4, 5):
        for rho in range(1 << K):
            for tp in tails:
                try:
                    run_template(rho, r0, tp)
                    ok += 1
                except (Undecided, Halt, Fail) as e:
                    fails.append((r0, rho, ''.join(map(str, tp)), str(e)))
    print('K=%d: %d template runs OK, %d failures [%.1fs]' % (K, ok, len(fails), time.time() - t0))
    for f in fails[:25]: print('  FAIL', f)
