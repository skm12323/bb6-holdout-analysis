"""work_r10/agentD_measure.py -- (H1-dk) task 1: the exact relation dk(J) <-> sub-level.

For each spike parameter J = 5..N (canonical class host, phi_traced of agentB2_lib):
  - the pure sub-fires (universal replay) with positions rho, universal k = kat[rho];
  - rho* = last pure sub-fire, g = J-2-rho*, j_last, K = kat[rho*];
  - the WINDOW = chains from the rho*-fire (inclusive) to the re-entry (exclusive);
  - identities checked:
      (I1) dk(J) = kat[rho*] + e/2,  e = 2*(dk - kat[rho*])   [work_g6 Prop 2]
      (I2) 4*dk = J + dp + Sum_{chains != re-entry} j         [queue accounting]
      (I3) 2*e  = g + 2 + dp + S_win,  S_win = Sum_{window chains != re} j
      (I4) dk(J) <= J  <=>  S_win <= 4*Phi(rho*) + 3*(J-rho*) - dp
  - census of (g, j_last, dp), S_win, max window-chain param, nesting structure.

Usage: python agentD_measure.py [N=2000] [Jspots]
"""
import sys, time, json, collections
sys.path.insert(0, r'D:\math_cc\work_r10')
from agentB2_lib import phi_traced, universal

def v2(x): return (x & -x).bit_length() - 1


def analyse(m, kat):
    r = phi_traced(m)
    st = r['steps']
    u = r['u']
    dk, dp = r['dk'], r['dp']
    s_tot = len(st)
    # pure sub-fires: b,c both run originals ('R',a)
    pure = [i for i, s in enumerate(st)
            if s[0] == 'C' and s[1][0] == 'R' and s[2][0] == 'R']
    # all chains and the re-entry (last step is the re-entry chain, b = T)
    chains = [i for i, s in enumerate(st) if s[0] == 'C']
    reentry = chains[-1]
    assert st[reentry][1][0] == 'T'
    jsum_all_ex_re = sum(st[i][3] for i in chains if i != reentry)
    # rho* and K
    if pure:
        i_last = pure[-1]
        rho = st[i_last][1][1]
        K = (st[i_last][4] - 3 * (1 << rho) * u - 4) // 6
        jlast = st[i_last][3]
    else:
        i_last = None
        rho = None
        K = 0
        jlast = None
    g = (m - 2 - rho) if rho is not None else m - 4  # no sub-fire: whole run is exit
    # window: steps [i_last, s_tot) if pure else all steps; window chains except re-entry
    w0 = i_last if i_last is not None else 0
    win_chains = [i for i in chains if i >= w0 and i != reentry]
    S_win = sum(st[i][3] for i in win_chains)
    e = s_tot - 2 * K
    # identities
    errs = []
    if 2 * dk != s_tot: errs.append('s=2dk')
    if e != 2 * (dk - K): errs.append('I1')
    if 4 * dk != (m - 1) + 1 + dp + jsum_all_ex_re: errs.append('I2: %d vs %d' %
        (4 * dk, (m - 1) + 1 + dp + jsum_all_ex_re))
    if 2 * e != g + 2 + dp + S_win: errs.append('I3: %d vs %d' % (2 * e, g + 2 + dp + S_win))
    # universal agreement of sub-fire k's
    for i in pure:
        rho_i = st[i][1][1]
        K_i = (st[i][4] - 3 * (1 << rho_i) * u - 4) // 6
        if kat.get(rho_i) != K_i:
            errs.append('kat mismatch at rho=%d: %d vs %d' % (rho_i, K_i, kat.get(rho_i)))
    # window chain detail (label kinds, j's, params)
    win_detail = [(st[i][1][0] if st[i][1][0] != 'M' else 'M',
                   st[i][2][0], st[i][3]) for i in win_chains]
    maxj_win = max([st[i][3] for i in win_chains]) if win_chains else 0
    Phi_r = (rho - kat[rho]) if rho is not None else None
    S_target = 4 * (Phi_r if Phi_r is not None else 0) + 3 * (m - (rho if rho is not None else 3)) - dp
    return {'m': m, 'dk': dk, 'dp': dp, 'steps': s_tot, 'rho': rho, 'g': g,
            'jlast': jlast, 'K': K, 'Phi_r': Phi_r, 'e': e, 'S_win': S_win,
            'maxj_win': maxj_win, 'n_win_chains': len(win_chains),
            'S_target': S_target, 'errs': errs, 'win': win_detail}


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    # universal kat table: needs phi() for j up to ~1+log2(3*N) -- build lazily via universal()
    t0 = time.time()
    kat, fires = universal(N + 50)
    t1 = time.time()
    print('universal table: %d fires to p<%d [%.1fs]; Phi_min=%d at p=%d; Phi(p>=26)min=%d'
          % (len(fires), N + 50, t1 - t0,
             min(p - k for p, k, j in fires),
             [p for p, k, j in fires if p - k == min(q - kk for q, kk, jj in fires)][0],
             min(p - k for p, k, j in fires if p >= 26)))
    rows = []
    all_err = []
    t0 = time.time()
    for m in range(5, N + 1):
        r = analyse(m, kat)
        rows.append(r)
        if r['errs']:
            all_err.append((m, r['errs']))
    t1 = time.time()
    print('analysed J=5..%d [%.1fs]; identity failures: %d' % (N, t1 - t0, len(all_err)))
    for m, e in all_err[:10]:
        print('   J=%d: %s' % (m, e))
    # census
    maxS = max(rows, key=lambda r: r['S_win'])
    maxe = max(rows, key=lambda r: r['e'])
    maxj = max(rows, key=lambda r: r['maxj_win'])
    maxg = max(rows, key=lambda r: r['g'])
    print('max S_win = %d at J=%d (rho=%d,g=%d,jlast=%s,K=%d,e=%d,win=%s)'
          % (maxS['S_win'], maxS['m'], maxS['rho'] or -1, maxS['g'], maxS['jlast'],
             maxS['K'], maxS['e'], maxS['win']))
    print('max e    = %d at J=%d (rho=%d,g=%d)' % (maxe['e'], maxe['m'], maxe['rho'] or -1, maxe['g']))
    print('max win-param = %d at J=%d ; max gap = %d at J=%d ; max dp = %d'
          % (maxj['maxj_win'], maxj['m'], maxg['g'], maxg['m'], max(r['dp'] for r in rows)))
    print('max dk-J slack: %d ; count dk>J: %d'
          % (max(r['dk'] - r['m'] for r in rows), sum(1 for r in rows if r['dk'] > r['m'])))
    # shape census (g, jlast, dp) and S_win stats
    shp = collections.Counter((r['g'], r['jlast'], r['dp']) for r in rows)
    print('shapes (g, j_last, dp) -> count, max S_win:')
    shS = {}
    for r in rows:
        key = (r['g'], r['jlast'], r['dp'])
        shS[key] = max(shS.get(key, 0), r['S_win'])
    for k_, c in shp.most_common():
        print('   %-18s x%-5d maxS=%d' % (str(k_), c, shS[k_]))
    # slack analysis: S_target - S_win min (the binding constraint)
    mins = min(rows, key=lambda r: r['S_target'] - r['S_win'])
    print('min slack S_target-S_win = %d at J=%d (rho=%d, Phi=%s, g=%d, S_win=%d)'
          % (mins['S_target'] - mins['S_win'], mins['m'], mins['rho'] or -1,
             mins['Phi_r'], mins['g'], mins['S_win']))
    # S_win vs J: the biggest S_win/(4Phi+3g'-dp) users
    rows.sort(key=lambda r: -(r['S_win'] / max(1, r['S_target'])))
    print('worst S_win/S_target ratios:')
    for r in rows[:10]:
        print('   J=%d: S=%d/target=%d (rho=%d Phi=%d g=%d e=%d win=%s)'
              % (r['m'], r['S_win'], r['S_target'], r['rho'] or -1,
                 r['Phi_r'] or 0, r['g'], r['e'], r['win']))
    # window param max vs jlast
    big = [r for r in rows if r['maxj_win'] > 4]
    print('J with window chain param > 4: %d (max %d at J=%d)'
          % (len(big), maxj['maxj_win'], maxj['m']))
    # dump for the report
    with open(r'D:\math_cc\work_r10\agentD_data.json', 'w') as f:
        json.dump({'rows': [{k: v for k, v in r.items() if k != 'win'} | {'win': r['win']}
                            for r in rows],
                   'fires_head': fires[:40]}, f)
    print('wrote agentD_data.json')


if __name__ == '__main__':
    main()
