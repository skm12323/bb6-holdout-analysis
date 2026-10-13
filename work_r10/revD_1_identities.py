"""revD_1_identities.py -- ADVERSARY-2 attack 1: re-derive I1-I4 from scratch.

Independent Phi_J tracer built directly from PROOF_G6 par0 (no agentB2/agentD code):
  queue = [u*2^0..2^{J-2}, D_h, T_2, T_3, ...], A=u+1, u=(9P+6k_h+4)/2^J odd,
  D_h = (15/2)P+3k_h+1, T_e = 3*2^e*P, k_h = canonical class rep mod 2^J.
Step: read front pair (b,c); A even -> A+=b+c+3; A odd -> x=A+2b+3=2^j*uu,
push uu*2^0..2^{j-2} (j-1 entries) + seam c+(A+1)/2 (1 entry) => a j-chain pushes
EXACTLY j entries. Re-entry: b=T_e -> dk=(x-9*2^e P-4-6k_h)/6, dp=e.

Identities under test (hand re-derivation by the reviewer):
  (I1) dk = K + e/2,  e = steps from the rho*-fire (inclusive) to the end;
       K = k of the last pure sub-fire, extracted from x = 3*2^rho*u + 6K+4,
       must equal kat[rho*] (universal) and the fire sits at step index 2K.
  (I2) 4 dk = J + dp + Sum_{chains != re-entry} j    [2 entries consumed/step]
  (I3) 2 e = g + 2 + dp + S_win,  g = J-2-rho*, S_win = Sum_{window chains != re} j
  (I4-mine)  dk <= J  <=>  dp + S_win <= 3J + rho* - 4K      (exact threshold)
  (I4-theirs) target_used = 4*Phi(rho*) + 3*(J-rho*) - 4 = 3J + rho* - 4K - 4
       (the report's stated "<=>" is off by 4, conservative direction)

Usage: python -B revD_1_identities.py [N=500]
"""
import sys

def v2(x): return (x & -x).bit_length() - 1

_TC = {}   # J -> (dk, dp) from THIS tracer


def interlude(J, p_extra=60, tail=90):
    mod = 1 << J
    kh = ((1 << (J - 1)) - 2) * pow(3, -1, mod) % mod
    assert ((6 * kh + 4) >> J) % 2 == 1, 'class rep'
    p = J + p_extra
    P = 1 << p
    x0 = 9 * P + 6 * kh + 4
    assert v2(x0) == J
    u = x0 >> J
    A = u + 1
    # entries: (value, label); labels: ('R',a) host run, ('D',) host seam,
    # ('T',e) tail, ('M', sidx) pushed run of chain sidx, ('d', sidx) its seam
    Q = [(u << a, ('R', a)) for a in range(J - 1)]
    Q.append((15 * P // 2 + 3 * kh + 1, ('D',)))
    Q += [(3 * (1 << e) * P, ('T', e)) for e in range(2, tail)]
    steps = []  # (kind, blab, clab, j, npush, x)
    while True:
        (b, bl), (c, cl) = Q[0], Q[1]
        if A % 2 == 0:
            steps.append(('E', bl, cl, None, 0, None))
            A = A + b + c + 3
            Q = Q[2:]
            continue
        x = A + 2 * b + 3
        j = v2(x)
        uu = x >> j
        assert uu >= 3, ('halt-like chain', J)
        if bl[0] == 'T':
            dk = (x - 9 * (1 << bl[1]) * P - 4 - 6 * kh) // 6
            steps.append(('C', bl, cl, j, 0, x))
            _TC[J] = (dk, bl[1])
            return {'steps': steps, 'dk': dk, 'dp': bl[1], 'u': u, 'kh': kh, 'P': P}
        sidx = len(steps)
        steps.append(('C', bl, cl, j, (j - 1) + 1, x))
        Q = [(uu << a, ('M', sidx)) for a in range(j - 1)] + \
            [(c + (A + 1) // 2, ('d', sidx))] + Q[2:]
        A = uu + 1


def T(j):
    if j not in _TC:
        interlude(j)
    return _TC[j]


def univ_kat(N):
    """universal fire stream kat[p]=k using THIS tracer's table."""
    kat = {}
    p, k = 4, 1
    while p <= N:
        kat[p] = k
        j = 1 + v2(3 * k + 2)
        dk, dp = T(j)
        k += dk
        p += dp
    return kat


def main(N=500):
    print('== revD attack 1: independent I1-I4 re-derivation, J = 7..%d ==' % N)
    kat = univ_kat(N + 60)
    bad = []
    kat_mismatch = 0
    stat = {'maxSw': 0, 'maxSw_at': None, 'maxwinj': 0, 'maxdp': 0, 'mindp': 99,
            'maxg': 0, 'min_margin': 10**9, 'eq_marg_min': 10**9}
    for j, exp in ((14, 8), (19, 8), (20, 9)):
        dk, dp = T(j)
        print('  spot dk(%d)=%d (report %d) %s' % (j, dk, exp, 'OK' if dk == exp else 'MISMATCH'))
    for J in range(7, N + 1):
        r = interlude(J)
        st = r['steps']
        dk, dp, u = r['dk'], r['dp'], r['u']
        n = len(st)
        for si, s in enumerate(st):
            if s[0] == 'C' and s[4] != 0:
                assert s[4] == s[3], ('push count', J, si)
        chains = [i for i, s in enumerate(st) if s[0] == 'C']
        re_ = chains[-1]
        assert st[re_][1][0] == 'T', ('re-entry is T-fire', J)
        pure = [i for i in chains if st[i][1][0] == 'R' and st[i][2][0] == 'R']
        assert pure, 'no pure sub-fire at J=%d' % J
        # every pure sub-fire: k extracted from x equals the universal kat[rho]
        for i in pure:
            rho = st[i][1][1]
            x = st[i][5]
            num = x - 3 * (1 << rho) * u - 4
            assert num % 6 == 0, ('K integrality', J, i)
            K_i = num // 6
            if kat.get(rho) != K_i:
                kat_mismatch += 1
        i_last = pure[-1]
        rho = st[i_last][1][1]
        K = (st[i_last][5] - 3 * (1 << rho) * u - 4) // 6
        errs = []
        if i_last != 2 * K:
            errs.append('I1-stepindex: %d != 2K=%d' % (i_last, 2 * K))
        e = n - 2 * K
        if e != 2 * (dk - K):
            errs.append('I1: e=%d != 2(dk-K)=%d' % (e, 2 * (dk - K)))
        if n != 2 * dk:
            errs.append('s=2dk: %d vs %d' % (n, 2 * dk))
        jsum = sum(st[i][3] for i in chains if i != re_)
        if 4 * dk != J + dp + jsum:
            errs.append('I2: 4dk=%d vs J+dp+sumj=%d' % (4 * dk, J + dp + jsum))
        g = J - 2 - rho
        win = [i for i in chains if i >= i_last and i != re_]
        Sw = sum(st[i][3] for i in win)
        if 2 * e != g + 2 + dp + Sw:
            errs.append('I3: 2e=%d vs g+2+dp+Sw=%d' % (2 * e, g + 2 + dp + Sw))
        thr_mine = 3 * J + rho - 4 * K
        tgt_used = 4 * (rho - K) + 3 * (J - rho) - 4
        if tgt_used != thr_mine - 4:
            errs.append('I4-shift: tgt_used=%d thr_mine=%d' % (tgt_used, thr_mine))
        if (dk <= J) != (dp + Sw <= thr_mine):
            errs.append('I4-equiv FAIL: dk=%d J=%d dp+Sw=%d thr=%d' % (dk, J, dp + Sw, thr_mine))
        if dp + Sw <= tgt_used and dk > J:
            errs.append('I4-suff FAIL (fatal direction)')
        for i in win:
            if st[i][3] >= J:
                errs.append('window param >= J at step %d' % i)
        if errs:
            bad.append((J, errs))
            if len(bad) < 8:
                print('  FAIL J=%d: %s' % (J, errs))
        if Sw > stat['maxSw']:
            stat['maxSw'], stat['maxSw_at'] = Sw, (J, rho, K, g, dp)
        stat['maxwinj'] = max(stat['maxwinj'], max([st[i][3] for i in win]))
        stat['maxdp'] = max(stat['maxdp'], dp)
        stat['mindp'] = min(stat['mindp'], dp)
        stat['maxg'] = max(stat['maxg'], g)
        stat['min_margin'] = min(stat['min_margin'], J - dk)
        stat['eq_marg_min'] = min(stat['eq_marg_min'], thr_mine - (dp + Sw))
    print('  identity failures: %d / %d J-values ; kat mismatches: %d'
          % (len(bad), N - 6, kat_mismatch))
    print('  census: maxSw=%d at (J,rho,K,g,dp)=%s ; maxwinj=%d ; dp in [%d,%d] ;'
          ' maxg=%d ; min(J-dk)=%d ; min(thr-(dp+Sw))=%d'
          % (stat['maxSw'], stat['maxSw_at'], stat['maxwinj'], stat['mindp'],
             stat['maxdp'], stat['maxg'], stat['min_margin'], stat['eq_marg_min']))
    print('  I4 exact threshold = 3J+rho*-4K; report target = that MINUS 4 (conservative).')
    return len(bad) == 0 and kat_mismatch == 0


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    ok = main(N)
    print('VERDICT attack1:', 'CONFIRMED' if ok else 'REFUTED/GAP')
