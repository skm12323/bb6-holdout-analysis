"""verify_laws.py -- exact checks of the [A] lemmas of NOTES.md on constructed (SYNTHETIC-start) walks.
Instances: leaves of the branching tree from forced-gate starts G(j) for every odd-a chain j < JMAX (cylinder
depth BITS), concretized and replayed with the exact integer walk, plus post-gate seeds (j,m) for every pair of
postgate_400_5000.json with positive next-gate mass.  At every true NT gate (chain j, k=k_j, output m) we check
  PG    Theta_after = 2^(j-2) + 3(k+1)            (mod 2^(j-1))
  LAND  first landing c after m and its defect D_c = Theta_c - x_c:
        D_c = delta + 2^(j-2)  (mod 2^min(j-1, m-1-eps)),  delta = -3k (a), 3k+2 (b), 3k+2-lambda_Y (c)
        a-type: c = 1 + v2(2^(j-2) o + 3(k+1+k_m)) if this is < m-1 (else c >= m-1), o=(Theta_in+3k)/2^(j-2)
  FREE  c >= j-1  ==>  v2(k+1+k_m) >= j-2 (a)  or  omega(m-1) >= j-1 and 6tau(m-1)+5 >= 2^(j-1) (b/c)
  SELF  a-type landing c = j  ==>  the step at c is again a true NT gate
  NEXT  a/b/c landing c <= j-3: [step at c is a true NT gate]  <=>  v2(delta + 3k_c) = c-2;
        and then (a-type m-1) its output m' = v2(k+3+3k_m+2k_c) whenever that is < j-2
  DETREC if the next gate is determined by (j,m) alone, R_after(next) < R_in(this)   (R = chain + loss)
  CG    consecutive true NT gates at chains g, g': E = (Theta_g' + 3k_g' - Theta_g - 3k_g)/3 is an integer,
        E = (clock sum between the gates) + k_g' - k_g > 0, v2(E) >= min(g,g')-2, with equality iff g != g'
Also the mass identities lambda' = 3tau+4 (b), 3tau+4+lambda_Y (c) at every b/c landing used.
Writes verify_laws.json.  PYTHONUTF8=1 python -B work_claude_cycle/verify_laws.py [JMAX BITS]"""
import sys, json, time
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from branch import Cal, explore, gate_list, lift, evalf  # noqa
from cyc import walk, v2  # noqa

cnt = Counter()
fails = []


def chk(name, cond, info=None):
    cnt[name] += 1
    if not cond:
        cnt[name + '_FAIL'] += 1
        if len(fails) < 20:
            fails.append((name, info))


def check_walk(cal, j0, Th0, x0):
    steps, st = walk(cal, j0, Th0, x0, limit=2000)
    # reconstruct input states
    states = []
    j, Th, x = j0, Th0, x0
    for s in steps:
        states.append((j, Th, x))
        j, Th, x = s['jn'], s['Th'], s['x']
    gates = [i for i, s in enumerate(steps) if s['kind'] == 'a' and s['jn'] >= s['j']]
    for i in gates:
        s = steps[i]; j, Th_in, x_in = states[i]; k = s['k']; m = s['jn']
        o = (Th_in + 3 * k) / F(2) ** (j - 2)
        chk('gate_o_odd', o.denominator == 1 and o.numerator % 2 == 1, (j, k))
        d = (s['Th'] - (2 ** (j - 2) + 3 * (k + 1))) / F(2) ** (j - 1)
        chk('PG', d.denominator == 1, (j, k, m))
        if i + 1 >= len(steps):
            continue
        t = steps[i + 1]          # first step from m
        r = cal.row(m - 1)
        c = t['jn']
        Dc = t['Th'] - t['x']
        if r['kind'] == 'a':
            delta = -3 * k; prec = j - 1
            cf = 1 + v2(2 ** (j - 2) * o + 3 * (k + 1 + r['tau'] // 2))
            if cf < m - 1:
                chk('LAND_c_formula', c == cf, (j, m))
            else:
                chk('LAND_c_high', c >= m - 1, (j, m))
        else:
            lam = r['lam']
            if r['kind'] == 'b':
                chk('MASS_b', lam == 3 * r['tau'] + 4, (m,))
                delta = 3 * k + 2
            else:
                chk('MASS_c', lam == 3 * r['tau'] + 4 + r['lY'], (m,))
                delta = 3 * k + 2 - r['lY']
            prec = min(j - 1, m - 1 - r['eps'])
        z = (Dc - delta - 2 ** (j - 2)) / F(2) ** prec
        chk('LAND_class', z.denominator == 1, (j, k, m, r['kind']))
        if c >= j - 1:
            if r['kind'] == 'a':
                chk('FREE_a', v2(k + 1 + r['tau'] // 2) >= j - 2, (j, m))
            else:
                chk('FREE_bc', r['omega'] >= j - 1 and 6 * r['tau'] + 5 >= 2 ** (j - 1), (j, m))
        if i + 2 < len(steps):
            u = steps[i + 2]
            isgate = (u['kind'] == 'a' and u['jn'] >= u['j'])
            if r['kind'] == 'a' and c == j:
                chk('SELF', isgate, (j, m))
            if c <= j - 3 and u['kind'] == 'a':
                kc = u['k']
                chk('NEXT_crit', isgate == (v2(delta + 3 * kc) == c - 2), (j, m, c, r['kind']))
                if isgate and r['kind'] == 'a':
                    mp = v2(k + 3 + 3 * (r['tau'] // 2) + 2 * kc)
                    if mp < j - 2:
                        chk('NEXT_out', u['jn'] == mp, (j, m, c, mp, u['jn']))
    for a, b in zip(gates, gates[1:]):
        # DETREC: if the next gate is determined by (j, m) alone (single bit-free leaf of the generic post-gate
        # tree), its output record is below the input record of the previous gate
        ja, ka, ma = steps[a]['j'], steps[a]['k'], steps[a]['jn']
        ThP = {1: F(2 ** (ja - 2) + 3 * (ka + 1)), 'X': F(2 ** (ja - 1))}
        xP = {1: F(2 ** ma), 'V': F(2 ** (ma + 1))}
        LP = explore(cal, ma, ThP, xP, min_bits=0, stop_at_gate=True, max_leaves=4)
        det = (len(LP) == 1 and LP[0]['status'] == 'GATE')
        Rin = ja + (steps[a]['G'] - 1)
        Rout2 = steps[b]['jn'] + steps[b]['G']
        if det:
            chk('DETREC', Rout2 < Rin, (ja, ma, steps[b]['j'], steps[b]['jn']))
            cnt['pairs_det'] += 1
        else:
            cnt['pairs_free'] += 1
            cnt['free_after_j_%d' % ja] += 1
        g, Thg, _ = states[a]; g2, Thg2, _ = states[b]
        kg, kg2 = steps[a]['k'], steps[b]['k']
        E = (Thg2 + 3 * kg2 - Thg - 3 * kg) / 3
        clock = sum(1 + steps[t]['tau'] for t in range(a, b))
        chk('CG_int', E.denominator == 1 and E == clock + kg2 - kg and E > 0, (g, g2))
        e = v2(E); mn = min(g, g2) - 2
        chk('CG_val', e >= mn and ((e == mn) == (g != g2)), (g, g2, e))
        cnt['CG_pairs_%s' % ('same' if g == g2 else 'diff')] += 1
        if E < 2 ** (min(g, g2) - 2):
            cnt['CG_size_FAIL'] += 1
    cnt['walks'] += 1
    cnt['gates'] += len(gates)
    cnt['gates_per_walk_%d' % len(gates)] += 1


def main():
    JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    BITS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    t0 = time.time()
    cal = Cal()
    gj = [j for j in range(5, JMAX) if cal.k(j) is not None]
    for j in gj:
        k = cal.k(j)
        Th0 = {1: F(2 ** (j - 2) - 3 * k), 'X': F(2 ** (j - 1))}
        x0 = {1: F(2 ** j), 'V': F(2 ** (j + 1))}
        L = explore(cal, j, Th0, x0, min_bits=BITS if j < 30 else 120, max_leaves=10 ** 5)
        for l in L:
            if l['status'] != 'END':
                continue
            P = l['bits'] + max([s[3] for s in l['steps']] + [j]) + 64
            vals = lift(l, P)
            check_walk(cal, j, evalf(Th0, vals), evalf(x0, vals))
    pg = json.load(open(HERE / 'postgate_400_5000.json'))
    for c in pg['cont']:
        j, k, m = c['j'], c['k'], c['m']
        Th0 = {1: F(2 ** (j - 2) + 3 * (k + 1)), 'X': F(2 ** (j - 1))}
        x0 = {1: F(2 ** m), 'V': F(2 ** (m + 1))}
        # prepend the gate itself: state at chain j forced to gate with output m
        L = explore(cal, m, Th0, x0, min_bits=60, max_leaves=2000)
        for l in L:
            if l['status'] != 'END':
                continue
            P = l['bits'] + max([s[3] for s in l['steps']] + [m]) + 64
            vals = lift(l, P)
            ThA = evalf(Th0, vals); xA = evalf(x0, vals)
            # rebuild a gate input at chain j producing (ThA, xA): Theta_in = ThA - 3 - 6k, x_in from y = xA
            Th_in = ThA - 3 - 6 * k
            x_in = 2 * (2 * Th_in + 6 * k - xA)
            check_walk(cal, j, Th_in, x_in)
    res = dict(counts=dict(cnt), fails=fails, seconds=round(time.time() - t0, 1),
               status='PASS' if not any(kk.endswith('_FAIL') for kk in cnt) else 'FAIL', JMAX=JMAX, BITS=BITS)
    print(res)
    json.dump(res, open(HERE / 'verify_laws.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
