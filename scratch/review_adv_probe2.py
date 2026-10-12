"""ADVERSARY probe 2 (TemplateChecker):
 (a) at what nesting depth do DEEP branches fire? (the shipped code unpacks
     ('DEEP', ell, None) as (ell_n, a_n, head_n) in recursive callers ->
     latent TypeError/corruption at depth >= 1; run_all does not catch TypeError)
 (b) if we ENFORCE the nested-frame contract (d0 = 1) that verify_r8.py
     silently skips (d0=None at every recursive call), does it ever fail?
 (c) count suffix-match returns by frame kind (top d0!=None / nested / glue).
Run: python -B review_adv_probe2.py
"""
import sys
sys.path.insert(0, r'D:\math_cc\work_r8')
import verify_r8 as V

DEEP_STATS = {'deep_total': 0, 'deep_depth': [], 'contract_bad': 0,
              'ret_top': 0, 'ret_nested': 0, 'ret_glue': 0, 'nested_calls': 0}

class ProbeChecker(V.TemplateChecker):
    def F(self, L, level, Z0L, s0, H0, kap0, ell0=0, d0=None, depth=0):
        K = self.K
        L = list(L); ell = ell0
        while True:
            a = V._final_match(L, Z0L)
            if a is not None:
                head = L[0]
                if d0 is not None:
                    expect = V._add(V._sc(H0, 1 << s0), d0, V._C(3 * ell), kap0, *Z0L[:a])
                    if head == expect:
                        if depth == 0: DEEP_STATS['ret_top'] += 1
                        else: DEEP_STATS['ret_nested'] += 1
                        return ell, a, head
                    DEEP_STATS['contract_bad'] += 1
                    if DEEP_STATS['contract_bad'] <= 3:
                        print('  CONTRACT VIOLATION at depth %d: head=%s expect=%s'
                              % (depth, head, expect))
                else:
                    DEEP_STATS['ret_glue'] += 1   # top glue frame: unchecked return
                    return ell, a, head
            enc = V._encode_run(L)
            if enc is not None:
                H, r = enc
                d = V._sub(L[0], H)
                if V._par(V._add(H, d)) == 0:
                    L = [V._add(V._sc(H, 4), d, V._C(3))] + L[3:]; ell += 1
                    continue
            A = L[0]
            if V._par(A) == 1:
                b = L[1] if len(L) > 1 else V._M0
                c = L[2] if len(L) > 2 else V._M0
                q0 = V._add(A, b, b, V._C(3))
                window = L[3:]
                sp = V._v2f(q0)
                if sp >= 1:
                    if sp < K:
                        o_p = V._halfn(q0, sp)
                        cprime = V._add(c, V._half(V._add(A, V._C(1))))
                        kap_nest = V._sub(cprime, V._sc(o_p, 1 << (sp - 1)))
                        nestL = [V._add(o_p, V._C(1))] + [V._sc(o_p, 1 << i) for i in range(sp - 1)] \
                                + [V._add(V._sc(o_p, 1 << (sp - 1)), kap_nest)] + list(window)
                        DEEP_STATS['nested_calls'] += 1
                        # *** the fix under test: enforce the nested contract (d0 = 1) ***
                        ell_n, a_n, head_n = self.F(nestL, sp, window, sp, o_p, kap_nest,
                                                    0, V._C(1), depth + 1)
                        L = [head_n] + list(window[a_n:])
                        ell += 1 + ell_n
                        continue
                    else:
                        Hb = L[1] if len(L) > 1 else V._M0
                        for a_n in (0, 1, 2):
                            rest = window[a_n:]
                            i = 0
                            while i < len(rest) and rest[i] == V._sc(Hb, 1 << (i + 2)):
                                i += 1
                            for x in rest[i:]:
                                if self.zlike(x) is None:
                                    raise V.MFail('deep continuation not in family: %s' % (x,))
                        DEEP_STATS['deep_total'] += 1
                        DEEP_STATS['deep_depth'].append(depth)
                        return ('DEEP', ell + 1, None)
            L = V._Tm(L); ell += 1

tc = ProbeChecker(KK=8)
ok = 0; fails = []
for r0 in (1, 2, 3, 4, 5):
    for rho in range(256):
        for tp in tc.tails:
            try:
                tc.run_canonical(rho, r0, tp); ok += 1
            except (V.Undecided, V.Halt, V.MFail) as e:
                fails.append(('canon', r0, rho, tuple(tp), repr(e)))
for rho in range(256):
    for tp in tc.tails:
        try:
            tc.run_glue(rho, tp); ok += 1
        except (V.Undecided, V.Halt, V.MFail) as e:
            fails.append(('glue', rho, tuple(tp), repr(e)))
print('probe2a/2b (check5 family with nested contracts ENFORCED):')
print('  runs ok=%d fails=%d' % (ok, len(fails)))
if fails: print('  first fails:', fails[:5])
print('  deep branches: %d, depths seen: %s' % (DEEP_STATS['deep_total'], sorted(set(DEEP_STATS['deep_depth']))))
print('  nested contract violations: %d' % DEEP_STATS['contract_bad'])
print('  returns: top(checked)=%d nested(now-checked)=%d glue(never-checkable)=%d; nested calls=%d'
      % (DEEP_STATS['ret_top'], DEEP_STATS['ret_nested'], DEEP_STATS['ret_glue'], DEEP_STATS['nested_calls']))
