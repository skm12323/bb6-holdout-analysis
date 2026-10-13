"""BLIND AUDITOR-1 task 1/2/4: Phi_m census for m in [lo,hi] (default 5..1500).

Per m: locate the crossing (first step reading D_h), classify it, extract the
D-fire (b = D_h) with exact x_D, verify
  (i)   x_D = (39/2)P + 9k_h + 6*K_exit + 8 with K_exit = s_cross/2 (integer),
  (ii)  j_D = 1 + v2(3*K_exit+1) whenever that is < m-1,
  (iii) j_D <= m-2,
  (iv)  second fire (b = the 'd' pushed by the D-fire) j <= m-2,
        mixed fires (c = D_h) j <= m-2, all 'd'-b fires j <= m-2,
plus the (g, j_last) exit-shape census (pure = last sub-fire with b,c both run
entries, g = m-2-rho*; also 'any' = last b-run fire regardless of c).
"""
import sys, json
from collections import Counter, defaultdict
sys.path.insert(0, r'D:\math_cc\work_r10')
from revB2_phi import phi_trace, v2


def analyze(m):
    r = phi_trace(m)
    k = r['k']; P = r['P']; u = r['u']; chains = r['chains']; cross = r['cross']
    rec = {'m': m}
    Rf = [ch for ch in chains if ch[1][0] == 'R']
    for nm, sel in (('p', lambda ch: ch[2][0] == 'R'), ('a', None)):
        sub = Rf if sel is None else [ch for ch in Rf if sel(ch)]
        lf = sub[-1] if sub else None
        if lf is None:
            rec['g_' + nm] = None; rec['jl_' + nm] = None; rec['K_' + nm] = None
            rec['rho_' + nm] = None
        else:
            rho = lf[1][1]
            if lf[2][0] == 'R':
                assert lf[2] == ('R', rho + 1)
            num = lf[4] - 3 * (u << rho) - 4
            assert num >= 0 and num % 6 == 0, (m, nm, num)
            rec['g_' + nm] = m - 2 - rho; rec['jl_' + nm] = lf[3]
            rec['K_' + nm] = num // 6; rec['rho_' + nm] = rho
    D = [ch for ch in chains if ch[1][0] == 'Dh']
    MIX = [ch for ch in chains if ch[2][0] == 'Dh']
    assert len(D) <= 1 and len(MIX) <= 1 and not (D and MIX), (m, len(D), len(MIX))
    rec['ct'] = ('Dfire' if D else 'mixed' if MIX else
                 ('eclean' if cross['clean'] else 'eY'))
    rec['mix_j'] = MIX[0][3] if MIX else None
    rec['mix_btag'] = MIX[0][1][0] if MIX else None
    rec['D'] = bool(D)
    if D:
        sD, tbD, tcD, jD, xD = D[0]
        assert cross['clean'] and cross['s'] == sD and cross['s'] % 2 == 0, (m,)
        assert tcD == ('T', 2), (m, tcD)
        Kex = cross['s'] // 2
        rec['j_D'] = jD; rec['Kex'] = Kex
        rec['xok'] = (2 * xD == 39 * P + 18 * k + 12 * Kex + 16)
        a = v2(3 * Kex + 1)
        rec['form'] = 1 + a
        rec['formula_ok'] = (jD == 1 + a) if (1 + a < m - 1) else None  # None = tie zone
        rec['jd_le_m2'] = (jD <= m - 2)
        rec['delta'] = (Kex - rec['K_p']) if rec['K_p'] is not None else None
        second = [ch for ch in chains if ch[1] == ('d', sD)]
        rec['second'] = [ch[3] for ch in second]
    else:
        rec['second'] = []
    dfires = [ch for ch in chains if ch[1][0] == 'd']
    rec['d_js'] = [ch[3] for ch in dfires]
    Mj = [ch[3] for ch in chains if ch[1][0] == 'M']
    rec['Mmax'] = max(Mj) if Mj else None
    rec['nchain'] = len(chains)
    rec['e_re'] = r['re'][1]; rec['dk_re'] = r['re'][0]; rec['s_re'] = r['re'][2]
    return rec


def run(lo, hi, dump=None):
    recs = []
    shapes_p = Counter(); shapes_ct = Counter(); first_p = {}
    deltas = Counter()
    viol = []
    maxj = defaultdict(int)          # class -> max j
    nD = nDfire = nmix = 0
    maxjD = 0; maxjD_at = None
    maxKex_ov_m = 0.0
    for m in range(lo, hi + 1):
        rec = analyze(m)
        recs.append(rec)
        # ---- global invariant checks ----
        if rec['D']:
            nD += 1
            if not rec['xok']:
                viol.append((m, 'x_D affine form FAILS', rec))
            if rec['formula_ok'] is False:
                viol.append((m, 'j_D != 1+v2(3Kex+1)', rec))
            if not rec['jd_le_m2']:
                viol.append((m, 'j_D > m-2', rec['j_D']))
            if rec['j_D'] > maxjD:
                maxjD = rec['j_D']; maxjD_at = m
            if rec['delta'] is not None:
                deltas[rec['delta']] += 1
            maxKex_ov_m = max(maxKex_ov_m, rec['Kex'] / max(1, m - 1))
        if rec['mix_j'] is not None:
            nmix += 1
            if rec['mix_j'] > m - 2:
                viol.append((m, 'mixed fire j > m-2', rec['mix_j']))
        bad_d = [j for j in rec['d_js'] if j > m - 2]
        if bad_d:
            viol.append((m, "d-fire j > m-2", bad_d))
        if rec['Mmax'] is not None and rec['Mmax'] > m - 2:
            viol.append((m, 'M-fire j > m-2 (outside claim scope, informational)',
                         rec['Mmax']))
        if rec['second']:
            bad_s = [j for j in rec['second'] if j > m - 2]
            if bad_s:
                viol.append((m, 'second fire j > m-2', bad_s))
        # ---- census ----
        key = (rec['g_p'], rec['jl_p'])
        shapes_p[key] += 1
        first_p.setdefault(key, m)
        shapes_ct[(rec['ct'], rec['g_p'], rec['jl_p'])] += 1
        maxj['d'] = max(maxj['d'], max(rec['d_js']) if rec['d_js'] else 0)
        maxj['second'] = max(maxj['second'], max(rec['second']) if rec['second'] else 0)
        maxj['M'] = max(maxj['M'], rec['Mmax'] or 0)
        maxj['D'] = max(maxj['D'], rec.get('j_D', 0))
        maxj['mix'] = max(maxj['mix'], rec['mix_j'] or 0)
    print('=== range m=%d..%d: %d Phi_m runs ===' % (lo, hi, len(recs)))
    print('violations:', len(viol))
    for v in viol[:20]:
        print('   ', v)
    print('D-fires: %d runs; mixed-fires: %d runs; max j_D = %d (at m=%d); '
          'max Kex/(m-1) = %.4f' % (nD, nmix, maxjD, maxjD_at, maxKex_ov_m))
    print('max j by class: %s' % dict(maxj))
    print('delta (=Kex-K_pure) distribution:', dict(sorted(deltas.items())))
    print('--- (g, j_last) census [pure def: b,c both run] ---')
    for key in sorted(shapes_p, key=lambda t: (t[0] is None, t[0] or 0, t[1] or 0)):
        print('   g=%s j_last=%s : count %d, first m=%d' %
              (key[0], key[1], shapes_p[key], first_p[key]))
    print('--- (cross_type, g, j_last) census ---')
    for key in sorted(shapes_ct, key=lambda t: (str(t[0]), t[1] is None, t[1] or 0, t[2] or 0)):
        print('   %s g=%s jl=%s : %d' % (key[0], key[1], key[2], shapes_ct[key]))
    if dump:
        with open(dump, 'w') as f:
            json.dump(recs, f)
        print('wrote', dump)
    return recs, viol


if __name__ == '__main__':
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    dump = sys.argv[3] if len(sys.argv) > 3 else None
    run(lo, hi, dump)
