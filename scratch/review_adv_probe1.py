"""ADVERSARY probe 1: does the compositional engine ever verify o' >= 3
(i.e. q0 not a power of 2) at chain/nested constructions?  And do the
constructed nested lists ever carry negative coefficients?

Instruments the SINGLE-SYMBOL engine (verify_r8.F) at every chain fire:
  - o_p = q0/2^sp : record min constant term, whether any coeff is negative,
    whether ge3(o_p) would hold uniformly (all coeffs >= 0 and const >= 3),
    and whether o_p could evaluate to 1 for some u >= 0.
  - same for nestL entries.
Run: python -B review_adv_probe1.py [VMAX=300]
"""
import sys
sys.path.insert(0, r'D:\math_cc\work_r8')
import verify_r8 as V

VMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 300

stats = {'chains': 0, 'min_const': 10**9, 'neg_coeff': 0, 'o_ge3_unif': 0,
         'o_could_be_1': 0, 'min_value_u0': 10**9}

orig_F = V.F

def F_instrumented(L, level, Z0L, s0, H0, kap0, t0=0):
    L = list(L); ell = 0
    while True:
        a = V.final_match(L, Z0L)
        if a is not None:
            head = L[0]
            expect = V.add(V.sc(H0, 1 << s0), (0, 3 * ell), (0, 1), kap0, *Z0L[:a])
            if head == expect:
                return ell, a, head
            V.STATS['coinc'] += 1
        enc = V.encode(L) if len(L) >= 3 else None
        if enc is not None:
            H, d, r, kap = enc
            A = V.add(H, d)
            pA = V.par(A)
            if pA == 0 and r >= 2:
                L = [V.add(V.sc(H, 4), d, (0, 3))] + L[3:]; ell += 1
                continue
            if pA == 1:
                if r >= 2:
                    q0 = V.add(V.sc(H, 3), d, (0, 3))
                    cprime = V.add(V.sc(H, 2), V.half(V.add(H, d, (0, 1))))
                elif r == 1:
                    q0 = V.add(V.sc(H, 3), d, (0, 3))
                    cprime = V.add(V.sc(H, 2), kap, V.half(V.add(H, d, (0, 1))))
                else:
                    q0 = V.add(V.sc(H, 3), V.sc(kap, 2), d, (0, 3))
                    cprime = V.add(L[2] if len(L) > 2 else V.Z0, V.half(V.add(H, d, (0, 1))))
                window = L[3:]
                sp = V.v2f(q0)
                if sp >= 1:
                    o_p = V.halfn(q0, sp)
                    kap_nest = V.sub(cprime, V.sc(o_p, 1 << (sp - 1)))
                    nestL = [V.add(o_p, (0, 1))] + [V.sc(o_p, 1 << i) for i in range(sp - 1)] \
                            + [V.add(V.sc(o_p, 1 << (sp - 1)), kap_nest)] + list(window)
                    # ---- instrumentation ----
                    stats['chains'] += 1
                    co, cn = o_p
                    stats['min_const'] = min(stats['min_const'], cn)
                    if co < 0: stats['neg_coeff'] += 1
                    if not (co >= 0 and cn >= 3): stats['o_ge3_unif'] += 0
                    if co >= 0 and cn >= 3: stats['o_ge3_unif'] += 1
                    # o_p(u) = cn + co*u; with co >= 0, min over u>=0 is at u=0
                    val_u0 = cn
                    stats['min_value_u0'] = min(stats['min_value_u0'], val_u0)
                    # could o_p == 1 for some u >= 0?
                    if co != 0:
                        if (1 - cn) % co == 0 and (1 - cn) // co >= 0 and co > 0:
                            stats['o_could_be_1'] += 1
                    elif cn == 1:
                        stats['o_could_be_1'] += 1
                    # any negative coefficient in the nested list?
                    for e in nestL:
                        if e[0] < 0: stats['neg_coeff'] += 1
                    # ---- end instrumentation ----
                    assert sp < level
                    ell_n, a_n, head_n = F_instrumented(nestL, sp, window, sp, o_p, kap_nest, t0 + ell + 1)
                    L = [head_n] + list(window[a_n:])
                    ell += 1 + ell_n
                    continue
        L = V.T_list(L); ell += 1

V.F = F_instrumented
for v in range(1, VMAX + 1):
    F_instrumented.__dict__.setdefault('_depth', 0)
    # excursion uses V.F? no: excursion() calls F directly -> patch module-level name
    V.excursion(v)

print('probe1 (single-symbol chains, v = 1..%d):' % VMAX)
print('  chain fires            : %d' % stats['chains'])
print('  min const of o_p       : %d' % stats['min_const'])
print('  min o_p at u=0         : %d   (o_p = 1 there would mean REAL HALT for that u)' % stats['min_value_u0'])
print('  chains with o_p >= 3 uniformly (coeffs>=0, const>=3): %d / %d' % (stats['o_ge3_unif'], stats['chains']))
print('  chains where o_p CAN equal 1 for some u >= 0        : %d' % stats['o_could_be_1'])
print('  negative coefficients seen (o_p or nestL entries)    : %d' % stats['neg_coeff'])
