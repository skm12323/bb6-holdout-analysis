"""reviewB_probe1.py -- ATTACK 1 (+2): extreme-w universality of Theorem 2.

Run concrete excursions E(w,v) at extreme odd w for v in {200,500,1539,2500,4000}
and verify at EVERY chain consuming a run entry (any nesting level present):
    x - 3*2^rho*U == 6*k_rho + 4   (same universal k as w=1),
    j == 1 + v2(3*k_rho+2),  j < rho,  U odd,  no halt, singleton reached.
Also records run-chain depth histogram (attack 2) and ell / k_b(v).
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\scratch')
from reviewB_lib import build_kpos, run_labeled, kb_of

def main():
    t0 = time.time()
    kpos, jmax_tab = build_kpos(4400)
    print('kpos built: %d universal positions, max j needed %d (%.1fs)'
          % (len(kpos), jmax_tab, time.time() - t0))
    print('sanity: positions->k first 8:',
          [(p, kpos[p]) for p in sorted(kpos)[:8]])
    grid = []
    for v in (200, 500, 1539, 2500, 4000):
        for w in (1, (1 << 61) - 1, 10**12 + 1, 10**18 + 1):
            grid.append((w, v))
    grid.append((999, 4000))          # attack-2 extra
    grid.append((999, 2500))
    results = {}
    for (w, v) in grid:
        t1 = time.time()
        st = run_labeled(w, v, kpos)
        kb = kb_of(v, kpos)
        results[(w, v)] = st
        print('w=%-22d v=%-5d: halt=%s singleton=%s ell=%d (2kb=%d e=%d) '
              'runchains=%d nonrun=%d nonuniv=%d fails=%d maxdepth=%d '
              'minu=%s maxj=%d sum3=%d [%.1fs]'
              % (w, v, st.get('halt', False), st.get('singleton', False),
                 st['ell'], 2 * kb, st['ell'] - 2 * kb, st['run_chains'],
                 st['nonrun_chains'], st['nonuniv'], len(st['fails']),
                 st['maxdepth'], st['minu'], st['maxj'], st['sum3'],
                 time.time() - t1))
        sys.stdout.flush()
        if st['fails']:
            print('   FIRST FAILS:', st['fails'][:5])
        if st.get('depth_hist'):
            print('   depth_hist:', dict(sorted(st['depth_hist'].items())))
    # aggregate
    allf = [(wv, s['fails'][:3]) for wv, s in results.items() if s['fails']]
    halts = [wv for wv, s in results.items() if s.get('halt')]
    nonuniv = sum(s['nonuniv'] for s in results.values())
    print('==== AGGREGATE: runs=%d halts=%s total_fails=%d nonuniv=%d'
          % (len(results), halts, len(allf), nonuniv))
    if allf:
        for a in allf[:10]:
            print('   ', a)
    print('total %.1fs' % (time.time() - t0))

if __name__ == '__main__':
    main()
