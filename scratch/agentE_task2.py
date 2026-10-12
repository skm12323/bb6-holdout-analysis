"""agentE_task2.py -- Task 2: corrected template family (L-sum architecture).

Family: starts (r0 in 1..5, rho in R(r0+1) ONLY [R from agentE_task1's reachable
scan, v <= 600 symbolic], kap in {-1 mod 2^11} U {-2 mod 2^7}), 11 tail patterns,
via the hardened TemplateCheckerE (agentE_lib).

A) Symbolic: every start must complete with a verified contract or hand off at
   a deep branch with in-family continuation (0 failures expected).
B) Sum constraint, concretely: each start additionally instantiated with
   concrete symbol assignments (u, h, tt, kappa/m, z_i) filtered to
   sum(start) = 0 mod 3 (the audited orbit sum invariant), run as FULL orbits
   (past singletons) to 20000 top steps -- no HALT allowed.
   Sanity anchors: the adversary's three sum-INVALID halters must reproduce.

Writes agentE_task2out.json (incl. the symbolic deep contexts for task 3).
"""
import os
import sys
import json
import time
import random
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from agentE_lib import (TemplateCheckerE, MFail, Undecided, Halt,
                        build_start_sym, build_start_conc, eval_sym_list,
                        gen_sumvalid_envs, run_orbit)

CAP = 20000


def sanity_anchors():
    """The adversary's sum-invalid halters must reproduce (halt-detector check)."""
    res = []
    for L0, expect in ([[2301, 2048, 4095], 8108], [[2301, 2048, 4094], None],
                       [[2301, 2048], 1280]):
        st, steps, _ = run_orbit(L0, 200000)
        assert st == 'HALT', (L0, st)
        assert sum(L0) % 3 != 0      # both known halters are sum-invalid
        res.append((L0, steps, sum(L0) % 3))
        print('  anchor %s -> HALT at t=%d (sum %% 3 = %d)' % (L0, steps, sum(L0) % 3))
    # call-number convention: HALT on the n-th top() call; the adversary's
    # "[2301,2048] halts after 1280 top steps" counts the 1280 successful
    # steps before the 1281st (halting) call.
    assert res[0][1] == 8108 and res[1][1] == 2647 and res[2][1] == 1281, res
    return res


def main():
    t00 = time.time()
    data = json.load(open(os.path.join(HERE, 'agentE_R.json')))
    rho_sets = {int(k): set(v) for k, v in data['rho_sets'].items()}
    tc = TemplateCheckerE(8)
    TAILS = tc.tails

    print('== TASK 2: corrected template family ==')
    print('sanity anchors (adversary halters, sum-invalid):')
    sanity_anchors()

    # ---------------- A) symbolic sweep over the restricted family ----------------
    configs = []
    for r0 in (1, 2, 3, 4, 5):
        L = r0 + 1
        for rho in sorted(rho_sets.get(L, ())):
            for kapgen in (0, 1):
                for ti in range(len(TAILS)):
                    configs.append((r0, rho, kapgen, ti))
    n_ok = n_deep = 0
    fails = []
    t0 = time.time()
    for cfg in configs:
        r0, rho, kapgen, ti = cfg
        try:
            res = tc.run_canonical_gen(rho, r0, TAILS[ti], kapgen, cfg)
            if isinstance(res, tuple) and res[0] == 'DEEP':
                n_deep += 1
            else:
                n_ok += 1
        except (Undecided, Halt, MFail, AssertionError) as e:
            fails.append((cfg, repr(e)[:120]))
    print('A) symbolic: %d configs (%d rho-pairs, 2 kapgen, 11 tails): '
          '%d contract-complete, %d DEEP hand-offs, %d FAILURES [%.1fs]'
          % (len(configs), len(configs) // 22, n_ok, n_deep, len(fails), time.time() - t0))
    for f in fails[:10]:
        print('   FAIL', f)
    print('   engine stats:', tc.stats)

    # ---------------- B) concrete sum-valid full orbits ----------------
    rng = random.Random(20261012)
    triples = sorted({(c[0], c[1], c[2]) for c in configs})
    BUDGET = 12000
    per = max(1, min(11, BUDGET // len(triples)))
    deep_cfgs = {tuple(e['cfg']) if e['cfg'] is not None else None for e in tc.deep_log}
    t0 = time.time()
    conc_runs = conc_ok = 0
    total_steps = 0
    max_len = 0
    deeps_seen = defaultdict(int)      # (r0, rho) -> deep fires inside concrete runs
    failures = []
    stop_at = t0 + 2700
    done = True
    for (r0, rho, kapgen) in triples:
        if time.time() > stop_at:
            done = False
            break
        base = (r0 * 7 + rho * 3 + kapgen) % 11
        for k in range(per):
            ti = (base + k) % 11
            cfg = (r0, rho, kapgen, ti)
            kw = 3 if cfg in deep_cfgs else 1
            # builder consistency check (symbolic vs concrete), once per cfg
            Ls, _, _, _, _ = build_start_sym(r0, rho, kapgen, TAILS[ti])
            envs = gen_sumvalid_envs(r0, rho, kapgen, TAILS[ti], kw, rng)
            if not envs:
                failures.append((cfg, 'NO SUM-VALID ENV FOUND', None, None))
                continue
            ce = eval_sym_list(Ls, envs[0])
            assert ce == build_start_conc(r0, rho, kapgen, TAILS[ti], envs[0]), \
                'symbolic/concrete builder mismatch'
            for env in envs:
                L0 = build_start_conc(r0, rho, kapgen, TAILS[ti], env)
                assert sum(L0) % 3 == 0
                dl = []
                st, steps, Lend = run_orbit(L0, CAP, dl)
                conc_runs += 1
                total_steps += steps
                max_len = max(max_len, len(Lend))
                if dl:
                    deeps_seen[(r0, rho)] += len(dl)
                if st != 'CAP':
                    failures.append((cfg, st, steps, list(env)))
                else:
                    conc_ok += 1
    print('B) concrete sum-valid full orbits (cap %d): %d runs, %d no-halt, '
          '%d FAILURES; %d top steps total; max final list len %d; '
          'deep fires inside runs: %d [%.1fs]%s'
          % (CAP, conc_runs, conc_ok, len(failures), total_steps, max_len,
             sum(deeps_seen.values()), time.time() - t0,
             '' if done else '  [TRUNCATED BY TIME GUARD]'))
    for f in failures[:10]:
        print('   FAIL', f)

    # ---------------- persist ----------------
    def ser_form(f):
        return [list(f[0]), f[1]]

    deep_out = [{'cfg': e['cfg'], 'depth': e['depth'], 'sp': e['sp'],
                 'o_ok': e['o_ok'],
                 'nestL': [ser_form(x) for x in e['nestL']],
                 'window': [ser_form(x) for x in e['window']]}
                for e in tc.deep_log]
    out = {'n_configs': len(configs), 'sym_ok': n_ok, 'sym_deep': n_deep,
           'sym_fails': fails, 'stats': tc.stats,
           'conc_runs': conc_runs, 'conc_ok': conc_ok,
           'conc_fails': [list(map(str, f)) if not isinstance(f[0], tuple) else
                          [str(x) for x in f[0]] + [f[1], f[2], f[3]] for f in failures],
           'conc_steps': total_steps, 'deep_in_concrete': {str(k): v for k, v in deeps_seen.items()},
           'deep_log': deep_out}
    with open(os.path.join(HERE, 'agentE_task2out.json'), 'w') as f:
        json.dump(out, f)
    print('wrote agentE_task2out.json  [%.1fs total]' % (time.time() - t00))


if __name__ == '__main__':
    main()
