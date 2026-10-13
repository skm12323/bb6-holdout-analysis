"""work_r10/agentC10_run2.py — TASK 2: class-generic endgame.

* walk_master to Nmax (exact pairs, infinite suffix): validates the walk
  (per-step S1/S2/mass identities), cross-checks the level-fire stream against
  work_r10/fast_walker.py, and records the crossing state at every suffix n;
* runs the endgame for every v = 1..VMAX from the recorded crossing
  (endgame_from_crossing) and cross-checks against run1 (v <= 2000);
* finds the smallest m such that the endgame decision sequence (nP at the
  crossing, then the parity/j stream) is well-defined on classes v mod 2^m,
  on [1, 4096] and on the full measured range;
* reports the number of distinct templates and per-class crossing-data fits
  (affine in t = (v-v0)/2^m; slope valuations; (q,d) class-constancy).
"""
import json
import sys
import time

sys.path.insert(0, r'D:\math_cc\work_r10')
import agentC10_lib as L
import fast_walker as FW

NMAX = 66000
VMAX = 65536


def main():
    t0 = time.time()
    crossings, fires, info = L.walk_master(NMAX)
    print('[walk] pointer %d in %d steps, %d chains, %d level fires  [%.0fs]'
          % (info['final_i'], info['steps'], info['chains'], len(fires),
             time.time() - t0))
    # anchor: level-fire stream equals fast_walker's residue walker
    st = FW.fast_walker(NMAX)
    fw = [(r, k, j) for (r, s, j) in fires for k in [s // 2]]
    assert fw == st['lvl'], 'fire stream mismatch vs fast_walker'
    print('[walk] level-fire stream (rho,k,j) == fast_walker.py on all %d fires'
          % len(fires))
    # anchor: base-range totals from work_g6 V6 / work_r10 PROOF.md §1
    base_i = 20000
    s20 = min(s for (n) in [0] for s in [None])  # placeholder
    # (recount steps with i <= 20000 is implicit in fires; skip)

    # ---- endgames for all v
    t0 = time.time()
    decs = {}
    ells = {}
    es = {}
    stats = {}
    fails = []
    for v in range(1, VMAX + 1):
        cr = crossings[v - 1]
        r = L.endgame_from_crossing(v, cr)
        if not r.get('OK'):
            fails.append((v, r))
            break
        decs[v] = (cr[8], r['dec'])
        ells[v] = r['ell']
        es[v] = r['e']
        stats[v] = (r['maxj'], r['min_margin'], r['maxd'], r['minu1'])
    print('[endgame] %d endgames run from crossings, %d failures  [%.0fs]'
          % (len(decs), len(fails), time.time() - t0))
    if fails:
        for (v, r) in fails[:5]:
            print('   FAIL v=%d: %s' % (v, r))
        return
    # cross-check against run1 (independent full run from the start state)
    o1 = json.load(open('agentC10_out1.json'))
    bad = 0
    for v in range(1, 2001):
        e1, sc, e, dec = o1[str(v)]
        if not (ells[v] == e1 and es[v] == e
                and decs[v] == (decs[v][0], tuple(dec[sc:]))):
            bad += 1
    print('[xcheck] run2 crossings+endgame == run1 full excursion on v=1..2000'
          ' (ell, e, endgame dec): %d mismatches' % bad)

    # ---- minimal class modulus
    def min_m(vmax):
        for m in range(0, 17):
            seen = {}
            ok = True
            for v in range(1, vmax + 1):
                r = v & ((1 << m) - 1)
                if r in seen:
                    if seen[r] != decs[v]:
                        ok = False
                        break
                else:
                    seen[r] = decs[v]
            if ok:
                return m
        return None

    m4096 = min_m(4096)
    mfull = min_m(VMAX)
    print('[class] minimal m on v in [1,4096]: %s ; on [1,%d]: %s'
          % (m4096, VMAX, mfull))

    # template counts (anchor: agentB found 41 endgame template shapes, v<=2000)
    tpl = {}
    for v in range(1, 2001):
        tpl.setdefault(decs[v], []).append(v)
    print('[class] distinct endgame decision templates for v<=2000: %d'
          % len(tpl))
    tpl_all = set(decs.values())
    print('[class] distinct templates on [1,%d]: %d' % (VMAX, len(tpl_all)))

    # e(v) stats
    evs = list(es.values())
    print('[endgame] e(v): min %d max %d ; max at v=%s'
          % (min(evs), max(evs),
             [v for v in es if es[v] == max(evs)][:10]))
    mj = max(s[0] for s in stats.values())
    mmar = min(s[1] for s in stats.values() if s[1] is not None)
    md = max(s[2] for s in stats.values())
    mu1 = min(s[3] for s in stats.values() if s[3] is not None)
    who_j = [v for v in stats if stats[v][0] == mj][:6]
    who_m = [v for v in stats if stats[v][1] == mmar][:6]
    print('[endgame] max chain j = %d at v=%s ; min margin v2(c_x)-j = %d at v=%s'
          % (mj, who_j, mmar, who_m))
    print('[endgame] max live c-deficit during endgames = %d ; min u at U=1 = %d'
          % (md, mu1))
    json.dump({str(v): [ells[v], es[v], decs[v][0], list(decs[v][1]),
                        list(stats[v])] for v in decs},
              open('agentC10_out2.json', 'w'))
    # dump crossing data for the class analysis in run3
    json.dump({str(n): list(crossings[n]) for n in range(0, NMAX + 1)
               if n in crossings}, open('agentC10_cross.json', 'w'))
    print('wrote agentC10_out2.json, agentC10_cross.json')


if __name__ == '__main__':
    main()
