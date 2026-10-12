"""agentG_lib.py -- annotated closed-form top map for machine
"1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE", plus fire-record extraction.

State: (head, ents) with ents = list of (role, value), front = index 0.
Roles: 'R' run entry (value = beta*2^a, beta odd), 'T' tail (value = 2*rho-1),
'S' seam (value = c + (A+1)/2 pushed by a fire), 'X' used only in fire records
for singleton-parent fires (ents empty at the fire).

Top map (audited, RULES.md par.5): L=(A,b,c,S):
  A even: T(L) = (A+b+c+3, S)
  A odd : m := b+(A-3)/2; stack := (c+(A+1)/2, S); while m odd and m>=3:
          stack = (m+3)/2 :: stack; m := (m-3)/2;  m=1 -> HALT;
          else T(L) = (m+4, stack).
Closed form (agentB Lemma 1, cross-checked here against the literal loop):
  A odd, x = A+2b+3 = 2^k q (q odd): HALT iff q==1; else
  T(L) = (q+1; q, 2q, ..., q*2^(k-2), c+(A+1)/2, S).

Fire coordinates (agentC par.3): sigma = e1 (R/S) or e1+1 (T); D = A - sigma;
i = v2(sigma); t = (D-1)/3 when (D-1) % 3 == 0 ("integral t");
x_res = x - 3*sigma;  k = v2(x) = v2(x_res) iff v2(x_res) < i (no deep tie);
Delta = x_res - (3t+4)  (defined when t integral).
"""
import sys

def v2(n):
    if n <= 0:
        raise ValueError("v2 of non-positive %d" % n)
    return (n & -n).bit_length() - 1

def is_pow2(n):
    return n > 0 and (n & (n - 1)) == 0


def top_step_literal(head, ents):
    """Literal audited loop; ents = plain values. Returns (state, halted)."""
    A = head
    if A % 2 == 0:
        b = ents[0] if len(ents) >= 1 else 0
        c = ents[1] if len(ents) >= 2 else 0
        return (A + b + c + 3, ents[2:]), False
    b = ents[0] if len(ents) >= 1 else 0
    c = ents[1] if len(ents) >= 2 else 0
    m = b + (A - 3) // 2
    stack = [c + (A + 1) // 2] + list(ents[2:])
    while m % 2 == 1 and m >= 3:
        stack = [(m + 3) // 2] + stack
        m = (m - 3) // 2
    if m == 1:
        return None, True
    return (m + 4, stack), False


def top_step_annot(head, ents):
    """Closed-form annotated step. Returns ((head', ents'), fire) ;
    fire is a dict (None if even step); fire['HALT'] True if q==1."""
    if head % 2 == 0:
        e1 = ents[0][1] if ents else 0
        e2 = ents[1][1] if len(ents) > 1 else 0
        return (head + e1 + e2 + 3, ents[2:]), None
    # fire
    e1 = ents[0][1] if ents else 0
    role = ents[0][0] if ents else 'X'
    x = head + 2 * e1 + 3
    k = v2(x)
    q = x >> k
    if q == 1:
        return None, {'HALT': True, 'x': x, 'k': k, 'role': role}
    c = ents[1][1] if len(ents) > 1 else 0
    seam_role = 'T' if not ents else 'S'   # singleton-parent seam = excursion tail
    seam = c + (head + 1) // 2
    run = [('R', q << a) for a in range(k - 1)]
    sigma = e1 if role in ('R', 'S') else e1 + 1
    D = head - sigma
    xr = x - 3 * sigma
    ok_t = ((D - 1) % 3 == 0)
    t = (D - 1) // 3 if ok_t else None
    fire = {
        'role': role, 'A': head, 'e1': e1, 'sigma': sigma, 'D': D,
        'i': v2(sigma) if sigma > 0 else None,
        'x': x, 'k': k, 'q': q, 'x_res': xr,
        't': t, 'ok_t': ok_t,
        'Delta': (xr - (3 * t + 4)) if ok_t else None,
    }
    return (q + 1, run + [(seam_role, seam)] + ents[2:]), fire


def make_E(w, v):
    """Excursion E(w,v) = (3w+1; 3w, 6w, ..., 3w*2^(v-2), 3w*2^(v-1)-1)."""
    ents = [('R', 3 * w << a) for a in range(v - 1)]
    ents.append(('T', (3 * w << (v - 1)) - 1))
    return (3 * w + 1, ents)


def fire_family(f):
    """Classify a fire per agentC's grammar."""
    if f is None:
        return None
    if f.get('HALT'):
        return 'HALT'
    if f['role'] == 'X':
        return 'X'
    if f['role'] == 'R':
        return 'R'
    if f['role'] == 'T':
        return 'T'
    # S: split by integrality of t (6.1/6.2 style vs 6.3 deep)
    return 'S64' if f['ok_t'] else 'S63'


def run_orbit(nsteps, collect_from=0, on_fire=None, check_sum=True):
    """Run the top map from L0=(3). Returns (fires, final_state).
    fires: list of dicts with added 'n' (step index) and 'fam'."""
    head, ents = 3, []
    fires = []
    for n in range(nsteps):
        (head, ents), f = top_step_annot(head, ents)
        if f is not None:
            if f.get('HALT'):
                f['n'] = n
                fires.append(f)
                return fires, None, True
            f['n'] = n
            f['fam'] = fire_family(f)
            if on_fire is not None:
                on_fire(n, f)
            if n >= collect_from:
                fires.append(f)
        if check_sum and n % 1000000 == 0:
            s = head + sum(v for (r, v) in ents)
            assert s == 3 * n + 3, (n, s)
    return fires, (head, ents), False


def run_excursion(w, v, cap=None):
    """Run E(w,v) until it returns to a singleton (ents empty).
    Returns (fires, ell, end_head, halted)."""
    head, ents = make_E(w, v)
    if cap is None:
        cap = 40 * v + 200
    fires = []
    for n in range(cap):
        (head, ents), f = top_step_annot(head, ents)
        if f is not None:
            if f.get('HALT'):
                f['n'] = n
                f['fam'] = 'HALT'
                fires.append(f)
                return fires, n + 1, None, True
            f['n'] = n
            f['fam'] = fire_family(f)
            f['v'] = v
            fires.append(f)
        if not ents:
            return fires, n + 1, head, False
    raise RuntimeError("excursion E(%d,%d) did not end within %d steps" % (w, v, cap))
