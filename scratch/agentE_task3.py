"""agentE_task3.py -- Task 3: child-prefix coverage (L-coverage architecture).

For every deep branch hit in the corrected runs (the symbolic hand-offs of
task 2, each with its full symbolic context: child level sp = v2f(q0)
(guaranteed valuation), o' = q0/2^sp, K' = kap_nest, window), concretely
instantiate the child with SUM-VALID symbol assignments and run FULL orbits
to 20000 top steps -- no HALT allowed.

FAITHFULNESS (new, load-bearing): the symbolic engine divides q0 by the
guaranteed-for-all-u valuation sp = v2f(q0).  At a concrete env the TRUE
valuation may be higher (o'(env) even); there the symbolic child is a
fictional composite the dynamics never visits (its head is odd at t = 0),
and the true child is obtained by dividing further: ts = sp + v2(o'(env)),
o'' = odd part of o'(env), same c' (= J value) and window.  This script
 - classifies each instantiation faithful / fictional;
 - runs the TRUE child in both cases (faithful: eval(nestL); fictional:
   re-divided child);
 - runs the TRUE parent orbit at every env as ground truth;
 - separately records any HALTING fictional composite (a sum-valid halting
   STATE, though unreachable from the family by true dynamics) -- these probe
   exactly the child-prefix segment where the adversary's sum-invalid halts
   lived.
"""
import os
import sys
import json
import time
import random
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from agentE_lib import (TemplateCheckerE, gen_sumvalid_envs, run_orbit,
                        build_start_conc, v2i)

CAP = 20000
TARGET = 200


def main():
    t00 = time.time()
    out2 = json.load(open(os.path.join(HERE, 'agentE_task2out.json')))
    deep = out2['deep_log']
    tc = TemplateCheckerE(8)
    TAILS = tc.tails
    print('== TASK 3: child-prefix coverage ==')
    print('deep contexts from the corrected runs: %d' % len(deep))

    k_each = 3                     # 154 * 3 = 462 instantiations planned
    children = []
    groups = defaultdict(list)
    for i, e in enumerate(deep):
        r0, rho, kapgen, ti = e['cfg']
        groups[(r0, rho)].append(i)
    order = []
    gi = list(groups)
    while any(groups[g] for g in gi):
        for g in gi:
            if groups[g]:
                order.append(groups[g].pop(0))
    for idx in order:
        e = deep[idx]
        r0, rho, kapgen, ti = e['cfg']
        rng = random.Random(1000000 + 7919 * idx)
        for env in gen_sumvalid_envs(r0, rho, kapgen, TAILS[ti], k_each, rng):
            children.append((idx, e, env))

    n_faith = n_fict = 0
    true_runs = true_ok = 0
    fict_halters = []
    fict_runs = fict_halt = 0
    parent_runs = parent_ok = 0
    total_steps = 0
    true_fail = []
    parent_fail = []
    deep_in_child = 0
    for (idx, e, env) in children:
        r0, rho, kapgen, ti = e['cfg']
        sp = e['sp']
        nest = e['nestL']
        vals = [sum(a * env[i] for i, a in enumerate(f[0])) + f[1] for f in nest]
        assert sum(vals) % 3 == 0, 'child must inherit sum = 0 mod 3'
        o_p = vals[0] - 1
        # consistency: run entries are powers of o_p, J slot = c'
        for i in range(sp - 1):
            assert vals[1 + i] == o_p << i, 'nestL shape'
        if o_p % 2 == 1:
            n_faith += 1
            child = vals                       # faithful: symbolic == true
        else:
            n_fict += 1
            ts = sp + v2i(o_p)
            opp = o_p >> v2i(o_p)
            jval = vals[sp]                    # J slot value = c'(env)
            window = vals[sp + 1:]
            child = [opp + 1] + [opp << i for i in range(ts - 1)] + [jval] + window
            assert sum(child) % 3 == 0
            # the fictional composite: run it too, separately classified
            fst, fsteps, _ = run_orbit(vals, CAP)
            fict_runs += 1
            if fst != 'CAP':
                fict_halt += 1
                fict_halters.append({'cfg': e['cfg'], 'env': env,
                                     'o_p': o_p, 'halt_at': fsteps,
                                     'child': vals})
        dl = []
        st, steps, Lend = run_orbit(child, CAP, dl)
        true_runs += 1
        total_steps += steps
        deep_in_child += len(dl)
        if st != 'CAP':
            true_fail.append((e['cfg'], env, st, steps, child))
        else:
            true_ok += 1
        # ground truth: the true parent orbit at this env
        L0 = build_start_conc(r0, rho, kapgen, TAILS[ti], env)
        assert sum(L0) % 3 == 0
        pst, psteps, _ = run_orbit(L0, CAP)
        parent_runs += 1
        total_steps += psteps
        if pst != 'CAP':
            parent_fail.append((e['cfg'], env, pst, psteps))
        else:
            parent_ok += 1

    print('instantiations: %d (faithful %d, fictional %d)' % (len(children), n_faith, n_fict))
    print('TRUE children (cap %d): %d runs, %d no-halt, %d FAILURES; '
          'deep fires inside: %d' % (CAP, true_runs, true_ok, len(true_fail),
                                     deep_in_child))
    for f in true_fail[:5]:
        print('  TRUE-CHILD FAIL', f)
    print('true parents (ground truth, cap %d): %d runs, %d no-halt, %d FAILURES'
          % (CAP, parent_runs, parent_ok, len(parent_fail)))
    for f in parent_fail[:5]:
        print('  PARENT FAIL', f)
    print('FICTIONAL composites (separate class): %d runs, %d HALT '
          '(sum-valid halting STATES, unreachable from the family by true '
          'dynamics)' % (fict_runs, fict_halt))
    for h in fict_halters[:10]:
        print('  fict halter cfg=%s env=%s o_p=%d halt_at=%d child[:4]=%s'
              % (h['cfg'], h['env'], h['o_p'], h['halt_at'], h['child'][:4]))
    spread = defaultdict(int)
    for (idx, e, env) in children:
        r0, rho, kapgen, ti = e['cfg']
        spread[(rho, r0)] += 1
    print('spread across (rho, r0):', dict(sorted(spread.items())))
    print('total top steps (children + parents): %d [%.1fs]' % (total_steps, time.time() - t00))

    res = {'planned': len(children), 'faithful': n_faith, 'fictional': n_fict,
           'true_runs': true_runs, 'true_ok': true_ok,
           'true_fail': [[str(x) for x in f[:4]] for f in true_fail],
           'parent_runs': parent_runs, 'parent_ok': parent_ok,
           'parent_fail': [[str(x) for x in f[:4]] for f in parent_fail],
           'fict_runs': fict_runs, 'fict_halt': fict_halt,
           'fict_halters': [{k: (v if not isinstance(v, list) else v)
                             for k, v in h.items()} for h in fict_halters],
           'steps': total_steps, 'deep_in_child': deep_in_child,
           'spread': {'%d,%d' % k: v for k, v in spread.items()}}
    with open(os.path.join(HERE, 'agentE_task3out.json'), 'w') as f:
        json.dump(res, f)
    print('wrote agentE_task3out.json  [%.1fs]' % (time.time() - t00))


if __name__ == '__main__':
    main()
