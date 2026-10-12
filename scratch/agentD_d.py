"""
agentD_d.py -- Task D: structural fact about "canonical moments" inside excursions.

Setting: iterate the top map T from E(w,v) (t = 0,1,2,... top steps; t counts steps since
excursion start).  A moment is CANONICAL if the list has the form
    (H+d, H, 2H, ..., 2^(r-1)H, tail)      with H = 3w*2^j (j >= 0), r >= 1,
i.e. entry2 equals H = 3w*2^j exactly, entries 2..r+1 keep doubling, d = entry1 - H.
At a canonical moment put s' = v2(d+3).  Claims:
 (i)  during the excursion's "middle phase" (list has >= 3 entries beyond the first two,
      i.e. length >= 5) at every odd-d canonical moment:  j > s';
 (ii) d = 3t + 1 with t = number of top steps since excursion start.

Checked for v = 1..120, all odd w at once (symbolic affine forms, w = 2u+1) and
concretely for w in {1,3,5,7}.  We record margins j - s', their minimum and growth, and
any odd-d canonical moment with j <= s'.
"""
FAILS = []


def fail(msg):
    FAILS.append(msg)
    print("FAIL:", msg)


class UniformityError(Exception):
    pass


def v2i(n):
    v = 0
    while n % 2 == 0:
        v += 1
        n //= 2
    return v


# ---------------- symbolic forms (a,b) = a*u + b, u>=0, w=2u+1 ----------------
def parity(x):
    a, b = x
    if a % 2:
        raise UniformityError(("parity", x))
    return b % 2


def v2_form(x):
    """uniform 2-adic valuation of a*u+b; requires it not to depend on u"""
    a, b = x
    va = v2i(a) if a else 1 << 30
    vb = v2i(b) if b else 1 << 30
    if va == vb:
        raise UniformityError(("v2", x))
    return min(va, vb)


def T_sym(L):
    A = L[0]
    pA = parity(A)
    if len(L) >= 3:
        b, c, S = L[1], L[2], list(L[3:])
    elif len(L) == 2:
        b, c, S = L[1], (0, 0), []
    else:
        b, c, S = (0, 0), (0, 0), []
    if pA == 0:
        return [((A[0] + b[0] + c[0]), (A[1] + b[1] + c[1] + 3))] + S, False
    # A odd -> a_A even, b_A odd
    m = (b[0] + A[0] // 2, b[1] + (A[1] - 3) // 2)
    stack = [(c[0] + A[0] // 2, c[1] + (A[1] + 1) // 2)] + S
    while True:
        a, bb = m
        if a % 2:
            raise UniformityError(("parity-m", m))
        if bb % 2 == 0:
            break
        # m odd; m>=3 uniform?
        if a < 0:
            raise UniformityError(("ge3", m))
        if a == 0:
            if bb < 3:
                break
        elif bb < 3:
            raise UniformityError(("ge3", m))
        stack = [(a // 2, (bb + 3) // 2)] + stack
        m = (a // 2, (bb - 3) // 2)
    a, bb = m
    if a == 0:
        if bb == 1:
            return None, True
    elif a % 2 == 0 and bb % 2 == 0:
        pass
    else:
        raise UniformityError(("eq1", m))
    return [(m[0], m[1] + 4)] + stack, False


def E_sym(v):
    return [(6, 4)] + [(6 * 2 ** e, 3 * 2 ** e) for e in range(v - 1)] \
        + [(6 * 2 ** (v - 1), 3 * 2 ** (v - 1) - 1)]


def canon_sym(L):
    """returns (j, r, d-form) or None"""
    if len(L) < 2:
        return None
    a2, b2 = L[1]
    if a2 <= 0 or a2 % 6 or 2 * b2 != a2:
        return None
    q = a2 // 6
    if q & (q - 1):
        return None
    j = q.bit_length() - 1
    if b2 != 3 * q:
        return None
    r = 1
    i = 1
    while i + 1 < len(L) and L[i + 1] == (2 * L[i][0], 2 * L[i][1]):
        r += 1
        i += 1
    d = (L[0][0] - 6 * q, L[0][1] - 3 * q)
    return j, r, d


# ---------------- concrete ----------------
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


def canon_int(L, w):
    if len(L) < 2:
        return None
    e2 = L[1]
    q, rem = divmod(e2, 3 * w)
    if rem or q < 1 or (q & (q - 1)):
        return None
    j = q.bit_length() - 1
    r = 1
    i = 1
    while i + 1 < len(L) and L[i + 1] == 2 * L[i]:
        r += 1
        i += 1
    return j, r, L[0] - 3 * w * q


# ---------------- symbolic scan v=1..120 ----------------
VMAX = 120
records = []          # (v, t, len, r, j, d(3t+1?), odd, s', middle, margin)
viol_i = []           # (i) violations: odd & middle & j <= s'
viol_ii = []          # (ii) violations: d != 3t+1 (affine (0,3t+1))
nonuni = []
max_t_reached = 0
ells = {}

for v in range(1, VMAX + 1):
    L = E_sym(v)
    t = 0
    while True:
        # analyse current list
        cn = canon_sym(L)
        if cn is not None:
            j, r, d = cn
            dd = d[1] if d[0] == 0 else None
            try:
                odd = parity(d)
                sp = v2_form((d[0], d[1] + 3))
            except UniformityError as e:
                nonuni.append((v, t, e.args[0]))
                odd = sp = None
            middle = len(L) >= 5
            records.append((v, t, len(L), r, j, dd, odd, sp, middle,
                            (j - sp) if sp is not None else None))
            if dd != 3 * t + 1:
                viol_ii.append((v, t, d, "expected (0,%d)" % (3 * t + 1)))
            if odd and middle and sp is not None and j <= sp:
                viol_i.append((v, t, len(L), r, j, dd, sp, j - sp))
        # advance
        if len(L) == 1:
            ells[v] = t
            break
        L, halted = T_sym(L)
        if halted:
            fail(f"v={v}: HALT during excursion at t={t+1}")
            break
        t += 1
        max_t_reached = max(max_t_reached, t)
        if t > 5000:
            fail(f"v={v}: excursion too long")
            break

print("symbolic scan v=1..%d done; max excursion length ell = %d (at v=%d)"
      % (VMAX, max(ells.values()), max(ells, key=ells.get)))
print("canonical moments recorded: %d ; non-uniform d-parity/v2 events: %d"
      % (len(records), len(nonuni)))
print("(ii) violations (d != 3t+1):", len(viol_ii), viol_ii[:5])
print("(i)  violations (odd d, middle phase, j <= s'):", len(viol_i))
for x in viol_i[:20]:
    print("     v=%d t=%d len=%d r=%d j=%d d=%d s'=%d margin=%d" % x)

odd_mid = [rec for rec in records if rec[6] and rec[8] and rec[9] is not None]
margins = [rec[9] for rec in odd_mid]
if margins:
    mn = min(margins)
    where = [rec for rec in odd_mid if rec[9] == mn]
    print("odd-d middle-phase canonical moments: %d ; margin j-s' min = %d"
          % (len(odd_mid), mn))
    print("min-margin attained at (v,t,len,j,d,s'):",
          [(w[0], w[1], w[2], w[4], w[5], w[7]) for w in where][:12], "..." if len(where) > 12 else "")
    ex_t0 = [rec for rec in odd_mid if rec[1] > 0]
    if ex_t0:
        mn2 = min(r[9] for r in ex_t0)
        print("excluding t=0: min margin = %d at %s"
              % (mn2, [(r[0], r[1], r[4], r[5], r[7]) for r in ex_t0 if r[9] == mn2][:8]))
# margin as a function of t (min over v), to show growth
by_t = {}
for rec in odd_mid:
    if rec[1] > 0:
        by_t.setdefault(rec[1], []).append(rec[9])
crit = {}
for t in sorted(by_t):
    crit[t] = min(by_t[t])
print("min margin per t (t>0):", {t: crit[t] for t in sorted(crit) if t <= 40})
print("margins at the 'critical' t (3t+4 = 2^k):")
for t in (4, 20, 84):
    ms = by_t.get(t)
    print("   t=%d: %s" % (t, sorted(set(ms)) if ms else "not reached / no odd-d canonical moment"))
allmar = sorted(set(margins)) if margins else []
print("distinct margins observed:", allmar[:25], "..." if len(allmar) > 25 else "")

# j nondecreasing along each excursion's canonical moments?
mono_ok = True
for v in range(1, VMAX + 1):
    js = [rec[4] for rec in records if rec[0] == v]
    if js != sorted(js):
        mono_ok = False
print("j nondecreasing along each excursion's canonical moments:", mono_ok)

# sample table for a few v
for v in (4, 5, 8, 16, 120):
    tab = [(r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[9]) for r in records if r[0] == v]
    print(f"v={v} (ell={ells[v]}): canonical moments (t, len, r, j, d, odd, s', margin):")
    for row in tab:
        print("   ", row)

# ---------------- concrete cross-check w in {1,3,5,7} ----------------
conc_ok = True
for w in (1, 3, 5, 7):
    for v in range(1, VMAX + 1):
        L = E_int(w, v)
        t = 0
        while True:
            cn = canon_int(L, w)
            if cn is not None:
                j, r, d = cn
                if d != 3 * t + 1:
                    conc_ok = False
                    fail(f"[w={w} v={v}] concrete d={d} != 3t+1 at t={t}")
                sp = v2i(d + 3) if d % 2 == 1 else None
                if d % 2 == 1 and len(L) >= 5 and j <= sp:
                    viol_i.append((v, t, len(L), r, j, d, sp, j - sp))
            if len(L) == 1:
                if ells.get(v) != t:
                    conc_ok = False
                    fail(f"[w={w} v={v}] concrete ell={t} != symbolic {ells.get(v)}")
                break
            L, halted = T_int(L)
            if halted:
                conc_ok = False
                fail(f"[w={w} v={v}] HALT")
                break
            t += 1
print("concrete cross-check w in {{1,3,5,7}}, v=1..%d: %s"
      % (VMAX, "PASS (matches symbolic: same canonical t's, d=3t+1, same ell)" if conc_ok else "FAIL"))

print("=" * 78)
vI = len([x for x in viol_i])
vII = len(viol_ii)
if FAILS or nonuni:
    print("TASK D RESULT: FAIL (fails=%d nonuniform=%d)" % (len(FAILS), len(nonuni)))
else:
    print("TASK D RESULT: (i) %s (%d violations, see above), (ii) %s (%d violations)"
          % ("PASS" if vI == 0 else "FAIL", vI, "PASS" if vII == 0 else "FAIL", vII))
