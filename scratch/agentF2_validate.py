"""agentF2_validate.py -- independent validation of the fast ell-model.

Chain of authority:
  (def) T_list (verbatim copy of the audited top map on affine pairs (u-coeff, const));
  (engine) agentF_lib.F_ = compositional executor with E/F macro-jumps (same T_list);
  (model) agentF_fast.FastEll = universal-walk + endgame runner;
  (this file) checks model == engine == direct on growing ranges, plus the
  structural laws the counting proof needs:
    H1  clean Delta: at EVERY main fire (r >= 2) d = 3t+1 exactly, so
        sp = 1 + v2(3k+2), k = t/2 (fires at even t only);
    H2  fire gaps: t' = t + 1 + ell(sp) + [ell(sp) even];
    H3  r-dynamics: r_1 = s-5, r' = r - (2+a) - 2[ell(sp) even];
    H4  a-table: a_i = a(sp_i) depends only on sp (main-phase, r >= 3);
    H5  margin: v2(H) = s-1-r > sp at every fire (well-foundedness margin);
    SP  splice: the F-branch jump equals literal T_list stepping (checked
        from reconstructed canonical states, children run by pure T_list);
    UNI uniformity probe: child (ell, a) invariant under parity-preserving
        perturbations of o_p and of the window entries.

Modes:  python agentF2_validate.py [SDIRECT] [SNAIVE] [SSPLICE]
"""
import sys, time, random
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_lib import (F_, excursion, TRACE, STATS, add, sc, sub, par,
                        v2f, halfn, T_list, Z0)
from agentF_fast import FastEll, v2_int, direct_ell, W3, window_entries

SDIRECT = int(sys.argv[1]) if len(sys.argv) > 1 else 150
SNAIVE = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
SSPLICE = int(sys.argv[3]) if len(sys.argv) > 3 else 400

t_begin = time.time()
fe = FastEll()
fe.a0.update({1: 1, 2: 0, 3: 1, 4: 0, 5: 2, 6: 1, 7: 0, 8: 2,
              9: 0, 10: 1, 11: 0, 12: 2, 13: 0, 14: 3})


def v2i(n):
    c = 0
    while n % 2 == 0:
        n //= 2
        c += 1
    return c


# ---------- A. model vs direct pure-T_list symbolic runs ----------
badA = []
for s in range(1, SDIRECT + 1):
    if fe.ell_of(s) != direct_ell(s):
        badA.append(s)
print('A. model == direct T_list  s<=%d : %s   (%.1fs)'
      % (SDIRECT, badA[:5] or 'OK', time.time() - t_begin))

# ---------- B. model vs compositional engine ----------
badB = []
for s in range(1, SNAIVE + 1):
    eng = F_(use_cache=False)
    if fe.ell_of(s) != excursion(s, eng):
        badB.append(s)
print('B. model == naive engine   s<=%d : %s   (%.1fs)'
      % (SNAIVE, badB[:5] or 'OK', time.time() - t_begin))
# spot uncached checks at larger levels
spot = []
for s in (1500, 2000, 3000, 5000, 8000):
    fe.ell_of(s)
    eng = F_(use_cache=True)
    if fe.ell_of(s) != excursion(s, eng):
        spot.append(s)
print('B2. model == engine (cached) at %s : %s   (%.1fs)'
      % ('[1500,2000,3000,5000,8000]', spot or 'OK', time.time() - t_begin))

# ---------- C. structural laws H1-H5 from top-frame traces ----------
bad = {'oddfire': [], 'delta': [], 'splaw': [], 'gap': [], 'rdyn': [],
       'atable': [], 'margin': [], 'r1': []}
atable = {}
for s in range(4, SNAIVE + 1):
    eng = F_(use_cache=False, trace_levels={s})
    ell = excursion(s, eng)
    ev = TRACE[s]
    mains = [e for e in ev if e['type'] in ('E', 'F')]
    # r_1 for first fire = s-5 (after E at t=0 and t=1), when both exist
    r_prev = None
    t_prev = None
    e_prev = None
    for e in mains:
        if e['type'] == 'F' and e['r'] >= 2:
            t, sp, r = e['t'], e['sp'], e['r']
            if t % 2:
                bad['oddfire'].append((s, t))
            if e['Delta'] != 0:
                bad['delta'].append((s, t, e['Delta']))
            if sp != 1 + v2i(3 * (t // 2) + 2):
                bad['splaw'].append((s, t, sp))
            if r_prev is None:
                if r != s - 5:
                    bad['r1'].append((s, r))
            else:
                if r != r_prev:
                    bad['rdyn'].append((s, t, r, r_prev))
            if t_prev is not None:
                Lc = e_prev['ell_child']
                gap = t - t_prev
                if gap != 1 + Lc + (1 if Lc % 2 == 0 else 0):
                    bad['gap'].append((s, t_prev, t, Lc))
            if r >= 3:
                if sp in atable and atable[sp] != e['a']:
                    bad['atable'].append((s, t, sp, atable[sp], e['a']))
                atable[sp] = e['a']
            # margin: v2(H) - sp, v2(H) = s-1-r
            if (s - 1 - r) - sp < 1:
                bad['margin'].append((s, t, sp, s - 1 - r))
            r_prev = r - (2 + e['a']) - 2 * (1 if e['ell_child'] % 2 == 0 else 0)
            t_prev, e_prev = t, e
        elif e['type'] == 'E':
            if r_prev is not None:
                r_prev = r_prev - 2
        # note: 'E' events only occur at t=0,1 and as separators after
        # even-ell fires, so the F-branch accounting above is exact.
print('C. H1-H5 over s<=%d: %s' % (SNAIVE, {k: v[:3] for k, v in bad.items()
                                             if v} or 'all OK'))
print('   a-table (main fires, sp -> a): %s' % dict(sorted(atable.items())))

# ---------- D. splice checks (F-branch jump vs literal T_list) ----------
def child_direct(nestL, window):
    """Run the nested excursion by pure T_list; return (ell, a, head)."""
    L = list(nestL) + list(window)
    n = 0
    Z0L = list(window)
    while True:
        if len(L) <= 1 + len(Z0L):
            # final match: largest a with L[1:] == Z0L[len(Z0L)-a:]
            a = None
            for aa in range(len(Z0L), -1, -1):
                if len(L) == 1 + len(Z0L) - aa and L[1:] == Z0L[len(Z0L) - aa:]:
                    a = aa
                    break
            if a is not None:
                return n, a, L[0]
        L = T_list(L)
        n += 1
        assert n < 10 ** 6, 'child runaway'


def splice_at(s, t, r, kap=(0, -1), perturb=None):
    """Reconstruct the canonical pre-fire state of the level-s top frame at
    canonical time t, run length r; verify the compositional jump against
    literal T_list stepping. perturb: optional (du, dwin) parity-preserving
    perturbation for the uniformity probe."""
    H = sc(W3, 1 << (s - 1 - r))
    d = 3 * t + 1
    L = [add(H, (0, d))] + [sc(H, 1 << i) for i in range(r)] + \
        [add(sc(H, 1 << r), kap)]
    q0 = add(sc(H, 3), (0, d + 3))
    sp = v2f(q0)
    o_p = halfn(q0, sp)
    cprime = add(sc(H, 2), half(add(H, (0, d + 1))))  # r >= 2 case
    kap_nest = sub(cprime, sc(o_p, 1 << (sp - 1)))
    if perturb:
        du, dwin = perturb
        o_p = add(o_p, (0, du))
        kap_nest = kap_nest  # keep; window perturbed below
    nestL = [add(o_p, (0, 1))] + [sc(o_p, 1 << i) for i in range(sp - 1)] + \
        [add(sc(o_p, 1 << (sp - 1)), kap_nest)]
    window = window_entries(H, r, kap)
    if perturb:
        du, dwin = perturb
        X = s - 1 - r  # v2(H)
        window = [add(w, (0, dwin << (2 * X))) if i < r - 2 else
                  add(w, (0, dwin << (r + X))) for i, w in enumerate(window)]
    ell_c, a_c, head_c = child_direct(nestL, window)
    # parent: literal 1 + ell_c steps from the pre-fire state
    Lp = list(L)
    for _ in range(1 + ell_c):
        Lp = T_list(Lp)
    target = [head_c] + list(window[a_c:])
    ok = (Lp == target)
    return ok, sp, ell_c, a_c


def half(x):
    return (x[0] // 2, x[1] // 2)


# collect fires (t, r) for a set of levels from engine traces
n_splice = 0
bad_sp = []
for s in list(range(5, SSPLICE + 1, 7)) + [600, 1000]:
    eng = F_(use_cache=False, trace_levels={s})
    excursion(s, eng)
    for e in TRACE[s]:
        if e['type'] == 'F' and e['r'] >= 2:
            ok, sp, ell_c, a_c = splice_at(s, e['t'], e['r'])
            if not ok or sp != e['sp'] or ell_c != e['ell_child'] or \
                    a_c != e['a']:
                bad_sp.append((s, e['t'], sp, e['sp'], ell_c, e['ell_child'],
                               a_c, e['a'], ok))
            n_splice += 1
print('D. splice checks (literal T_list == compositional jump): %d fires, '
      'violations: %s   (%.1fs)' % (n_splice, bad_sp[:3] or 'none',
                                    time.time() - t_begin))

# ---------- E. uniformity probe ----------
random.seed(12345)
bad_u = []
n_u = 0
for s in (60, 200, 500):
    eng = F_(use_cache=False, trace_levels={s})
    excursion(s, eng)
    Fs = [e for e in TRACE[s] if e['type'] == 'F' and e['r'] >= 2]
    for e in random.sample(Fs, min(8, len(Fs))):
        ok0, sp0, ell0, a0v = splice_at(s, e['t'], e['r'])
        # parity-preserving perturbations: o_p += 2^(sp+40) (odd kept),
        # window entries += multiples of 2^(v2(entry)+40)
        ok1, sp1, ell1, a1 = splice_at(s, e['t'], e['r'],
                                       perturb=(1 << (sp0 + 40), 3))
        n_u += 1
        if not (ell1 == ell0 and a1 == a0v):
            bad_u.append((s, e['t'], sp0, ell0, ell1, a0v, a1))
print('E. uniformity probe (perturbed child inputs): %d cases, '
      'violations: %s   (%.1fs)' % (n_u, bad_u[:3] or 'none',
                                    time.time() - t_begin))
print('total %.1fs' % (time.time() - t_begin))
