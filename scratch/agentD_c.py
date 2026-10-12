"""
agentD_c.py -- Task C: symbolic execution of the top map T over odd w, and Lemma E(v).

Entries are integer affine forms  a*u + b  with u >= 0 the symbol and w = 2u+1 ranging
over all odd positive integers.  Decisions:
  * parity of a*u+b decided only if a is even (then parity = b mod 2);
  * halving only if both a and b are even (exact);
  * m >= 3 decided only if uniform over all u >= 0;
  * m == 1 decided only if uniform (a==0, or uniform-even).
Any non-uniform decision raises UniformityError (i.e. Lemma E(v) would fail).

Lemma E(v) (v <= 2000 in the original claim; we verify v = 1..100 symbolically for ALL
odd w at once, plus concrete cross-checks): iterating T from
   E(w,v) = (3w+1, 3w, 6w, ..., 3w*2^(v-2), 3w*2^(v-1)-1)
never halts, every decision is uniform, and a singleton is reached after exactly ell(v)
steps, independent of w.
"""
FAILS = []


def fail(msg):
    FAILS.append(msg)
    print("FAIL:", msg)


class UniformityError(Exception):
    pass


DEC = {"parity": 0, "half": 0, "ge3": 0, "eq1": 0}


def parity(x):
    a, b = x
    if a % 2:
        raise UniformityError(("parity", x))
    DEC["parity"] += 1
    return b % 2


def half(x):
    a, b = x
    if a % 2 or b % 2:
        raise UniformityError(("half", x))
    DEC["half"] += 1
    return (a // 2, b // 2)


def ge3(x):
    a, b = x
    if a < 0:
        raise UniformityError(("ge3-negative-slope", x))
    DEC["ge3"] += 1
    if a == 0:
        return b >= 3
    if b >= 3:
        return True
    raise UniformityError(("ge3", x))       # a>0, b<3: not uniform


def eq1(x):
    a, b = x
    DEC["eq1"] += 1
    if a == 0:
        return b == 1
    if a % 2 == 0 and b % 2 == 0:
        return False                          # uniformly even => never 1
    raise UniformityError(("eq1", x))


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def addc(x, c):
    return (x[0], x[1] + c)


def T_sym(L):
    """one top step on a list of affine forms. Returns (newlist, halted)."""
    A = L[0]
    pA = parity(A)
    if len(L) >= 3:
        b, c, S = L[1], L[2], list(L[3:])
    elif len(L) == 2:
        b, c, S = L[1], (0, 0), []
    else:
        b, c, S = (0, 0), (0, 0), []
    if pA == 0:
        return [add(add(add(A, b), c), (0, 3))] + S, False
    m = add(b, half(addc(A, -3)))
    stack = [add(c, half(addc(A, 1)))] + S
    while True:
        if parity(m) == 0:
            break
        if not ge3(m):
            break
        stack = [half(addc(m, 3))] + stack
        m = half(addc(m, -3))
    if eq1(m):
        return None, True
    return [addc(m, 4)] + stack, False


def E_sym(v):
    """E(w,v) with w=2u+1 as affine forms in u."""
    one = (6, 4)                                   # 3w+1 = 6u+4
    mids = [(6 * 2 ** e, 3 * 2 ** e) for e in range(v - 1)]
    last = (6 * 2 ** (v - 1), 3 * 2 ** (v - 1) - 1)
    return [one] + mids + [last]


def T_int(L):
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


def E_int(w, v):
    return [3 * w + 1] + [3 * w * 2 ** e for e in range(v - 1)] + [3 * w * 2 ** (v - 1) - 1]


# ---------------------------------------------------------------- run Lemma E(v)
VMAX = 100
ells_sym = {}
max_steps = 5000
for v in range(1, VMAX + 1):
    L = E_sym(v)
    steps = 0
    try:
        while len(L) > 1:
            L, halted = T_sym(L)
            if halted:
                fail(f"v={v}: symbolic execution took the HALT branch at step {steps+1}")
                break
            steps += 1
            if steps > max_steps:
                fail(f"v={v}: no singleton within {max_steps} steps")
                break
        else:
            ells_sym[v] = steps
    except UniformityError as e:
        fail(f"v={v}: NON-UNIFORM decision at step {steps+1}: {e}")
        ells_sym[v] = None

print("symbolic (all odd w at once), v=1..%d:" % VMAX)
print("  decisions made: parity=%d half=%d ge3=%d eq1=%d (all uniform)"
      % (DEC["parity"], DEC["half"], DEC["ge3"], DEC["eq1"]))
print("  no HALT branch ever taken:", "PASS" if not any('HALT branch' in f for f in FAILS) else "FAIL")

# concrete cross-checks: ell(v) independent of w, full list sequences agree
CONC = [1, 3, 5, 7, 999, 123456789]
ell_ok = True
seq_ok = True
for w in CONC:
    for v in range(1, VMAX + 1):
        Lc = E_int(w, v)
        Ls = E_sym(v)
        steps = 0
        while len(Lc) > 1:
            Lc, h1 = T_int(Lc)
            Ls, h2 = T_sym(Ls)
            steps += 1
            if h1 or h2:
                fail(f"w={w} v={v}: halted at step {steps}")
                ell_ok = False
                break
            u = (w - 1) // 2
            if [a * u + b for (a, b) in Ls] != Lc:
                fail(f"w={w} v={v}: symbolic/concrete list mismatch at step {steps}")
                seq_ok = False
                break
        if ells_sym.get(v) != steps:
            fail(f"w={w} v={v}: concrete ell={steps} != symbolic ell={ells_sym.get(v)}")
            ell_ok = False
print("concrete cross-check (w in %s): ell(v) identical & list sequences identical: %s / %s"
      % (CONC, "PASS" if ell_ok else "FAIL", "PASS" if seq_ok else "FAIL"))

claimed = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16]
mine = [ells_sym[v] for v in range(1, 31)]
print("ell(1..30) computed:", mine)
print("ell(1..20) claimed :", claimed)
print("match:", "PASS" if mine[:20] == claimed else "FAIL")

# bonus: concrete w=1 check of the full lemma range v<=2000 stated in (4)
full_ok = True
for v in range(101, 2001):
    Lc = E_int(1, v)
    steps = 0
    while len(Lc) > 1:
        Lc, h1 = T_int(Lc)
        steps += 1
        if h1:
            fail(f"v={v} (w=1): HALT at step {steps}")
            full_ok = False
            break
        if steps > 5000:
            fail(f"v={v} (w=1): no singleton in 5000 steps")
            full_ok = False
            break
    if v <= 120:
        pass
print("bonus: concrete w=1, v=101..2000 all reach singleton without halting:",
      "PASS" if full_ok else "FAIL")
print("ell(21..40) computed:", [ells_sym[v] for v in range(21, 41)])
print("max ell(v) for v<=100:", max(ells_sym.values()))

print("=" * 78)
if FAILS:
    print("TASK C RESULT: FAIL (%d problems)" % len(FAILS))
else:
    print("TASK C RESULT: PASS")
