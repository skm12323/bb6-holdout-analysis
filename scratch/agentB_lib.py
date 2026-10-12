"""agentB_lib.py — Library for the top-map / excursion analysis of the machine
1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE (halt F reading 0).

Audited top map on top lists (missing entries = 0):
  A even: T(A; b, c, S) = (A+b+c+3, S)
  A odd : m := b+(A-3)/2 ; stack := (c+(A+1)/2, S)
          while m odd and m>=3: stack = [(m+3)/2]+stack ; m = (m-3)/2
          if m=1: HALT ; else T = (m+4, stack)

Derived closed form for the A-odd branch (tested equivalent):
  x := A+2b+3 = 2^j * u  (u odd).  HALT iff u=1 (and j>=3, i.e. x>=8; the only
  other possibility x=4 needs A=1 which never occurs since A>=4 always).
  T = (u+1, u, 2u, ..., 2^{j-2}u, c+(A+1)/2, S)     [run of j-1 entries]

Excursion start: E(w,v) = (3w+1, 3w, 6w, ..., 3w*2^{v-2}, 3w*2^{v-1}-1), w odd.

Symbolic engine: parameter t >= 0 with w = 2t+1; entries are integer pairs
(a,b) meaning a*t+b.  Facts used:
  * parity of a*t+b is t-independent iff a even (then = b mod 2)
  * v2(a*t+b) is t-independent iff a==0 or v2(a) > v2(b) (then = v2(b))
"""

INF = 1 << 60

def v2i(x):
    if x == 0:
        return INF
    c = 0
    while (x & 1) == 0:
        x >>= 1
        c += 1
    return c

# ---------------- numeric top map ----------------

def top_step_ref(L):
    """Exactly the audited spec."""
    A = L[0]
    rest = list(L[1:])
    b = rest[0] if len(rest) > 0 else 0
    c = rest[1] if len(rest) > 1 else 0
    S = rest[2:]
    if A % 2 == 0:
        return [A + b + c + 3] + S, ('E',)
    m = b + (A - 3) // 2
    stack = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        stack.insert(0, (m + 3) // 2)
        m = (m - 3) // 2
    if m == 1:
        return None, ('HALT',)
    return [m + 4] + stack, ('C',)

def top_step_fast(L):
    """Closed form of the audited spec (assert-equivalent in tests)."""
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    S = L[3:]
    if A % 2 == 0:
        return [A + b + c + 3] + list(S), ('E',)
    x = A + 2 * b + 3
    j = v2i(x)
    u = x >> j
    if u == 1 and j >= 3:
        return None, ('HALT',)
    if u == 1 and j <= 2:
        # only possible with A=1,b=0 (x=4): m_0=-1, no loop, T=(3, c+1, S)
        assert A == 1 and b == 0, (A, b, x)
        return [3] + [c + 1] + list(S), ('C', j, u)
    return [u + 1] + [u << k for k in range(j - 1)] + [c + ((A + 1) >> 1)] + list(S), ('C', j, u)

def E_list(w, v):
    assert w % 2 == 1 and w >= 1 and v >= 1
    return [3 * w + 1] + [(3 * w) << i for i in range(v - 1)] + [((3 * w) << (v - 1)) - 1]

def excursion(w, v, cap=10**7, stepfn=top_step_fast):
    L = E_list(w, v)
    descs = []
    for t in range(cap):
        if len(L) == 1:
            return {'result': 'singleton', 'ell': len(descs), 'descs': descs, 'final': L}
        L, d = stepfn(L)
        descs.append(d)
        if d[0] == 'HALT':
            return {'result': 'HALT', 'ell': None, 'descs': descs, 'final': None}
    return {'result': 'cap', 'ell': None, 'descs': descs, 'final': L}

# ---------------- symbolic top map (t-parameter, w=2t+1) ----------------

def top_step_sym(L):
    A = L[0]; aA, bA = A
    if aA % 2 != 0:
        return None, ('UNSAFE', 'A-parity t-dependent: (%d,%d)' % (aA, bA))
    if bA % 2 == 0:
        b = L[1] if len(L) > 1 else (0, 0)
        c = L[2] if len(L) > 2 else (0, 0)
        newA = (aA + b[0] + c[0], bA + b[1] + c[1] + 3)
        return [newA] + list(L[3:]), ('E',)
    b = L[1] if len(L) > 1 else (0, 0)
    c = L[2] if len(L) > 2 else (0, 0)
    S = list(L[3:])
    ax = aA + 2 * b[0]
    bx = bA + 2 * b[1] + 3
    if ax == 0 or v2i(ax) > v2i(bx):
        j = v2i(bx)
    else:
        return None, ('UNSAFE', 'v2(x) t-dependent: x=(%d,%d)' % (ax, bx))
    au = ax >> j
    bu = bx >> j
    if au < 0:
        return None, ('UNSAFE', 'u decreasing: u=(%d,%d)' % (au, bu))
    halt_t = None
    if au == 0:
        if bu == 1:
            halt_t = 0
    else:
        if (1 - bu) >= 0 and (1 - bu) % au == 0:
            halt_t = (1 - bu) // au
    if halt_t is not None:
        return None, ('HALT_SYM', (au, bu), halt_t)
    if bu < 3:
        # u=1 with j<=2 (A=1 special case) never occurs in real orbits (A>=4);
        # treat as unsafe if it ever appeared
        return None, ('UNSAFE', 'u(0)<3: u=(%d,%d)' % (au, bu))
    newL = [(au, bu + 1)] + [(au << k, bu << k) for k in range(j - 1)] \
           + [(c[0] + (aA >> 1), c[1] + ((bA + 1) >> 1))] + S
    return newL, ('C', j, (au, bu))

def E_sym(v):
    L = [(6, 4)]                     # 3w+1
    for i in range(v - 1):
        L.append((3 << (i + 1), 3 << i))   # 3w*2^i = 3*2^{i+1} t + 3*2^i
    L.append((3 << v, (3 << (v - 1)) - 1)) # 3w*2^{v-1} - 1
    return L

def eval_pair(pr, t):
    return pr[0] * t + pr[1]

def excursion_sym(v, cap=10**7):
    L = E_sym(v)
    descs = []
    chains = []
    for t in range(cap):
        if len(L) == 1:
            return {'result': 'singleton', 'ell': len(descs), 'descs': descs,
                    'final': L, 'chains': chains}
        L, d = top_step_sym(L)
        descs.append(d)
        if d[0] == 'UNSAFE':
            return {'result': 'UNSAFE', 'where': len(descs) - 1, 'msg': d,
                    'descs': descs, 'chains': chains}
        if d[0] == 'HALT_SYM':
            return {'result': 'HALT_SYM', 'where': len(descs) - 1, 'msg': d,
                    'descs': descs, 'chains': chains}
        if d[0] == 'C':
            chains.append((len(descs) - 1, d[1], d[2]))
    return {'result': 'cap', 'descs': descs, 'chains': chains}
