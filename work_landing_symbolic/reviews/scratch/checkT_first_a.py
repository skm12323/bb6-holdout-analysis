"""Independent recomputation for the FIRST_A_REDUCTION review items (checker T)."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys, json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, first_fire, val   # noqa: E402

OUT = Path(__file__).with_name('checkT_first_a.json')


def bounded_walk(cal, x, th, precision, signed=False):
    x, th = F(x), F(th)
    loss = 0
    rows = []
    for _ in range(256):
        if x == 0:
            return 'zero', rows
        if x < 0 and not signed:
            return 'nonpositive', rows
        j = val(x)
        if j + loss >= precision:
            return 'ceiling', rows
        rows.append((j, loss, x, th))
        r = cal.crossing(j - 1)
        if not r['odd']:
            return 'end', rows
        if r['kind'] == 'a':
            x = 2 * th + 3 * r['time'] - x / 2
        else:
            x = (r['head_ratio'] + 2 * r['tail_ratio']) * x / 2 + r['head_lambda'] + 2 * r['tail_lambda'] + 3
        th += 3 + 3 * r['time']
        loss += 1 + r['epsilon']
    return 'limit', rows


def main():
    cal = Calendar(512)
    res = {}
    stats = Counter()
    cert = Counter()
    checked = 0
    firstA = []
    collisions = []
    ex_bits = []
    max_extra = 0
    for P in range(5, 257):
        fire = first_fire(cal, P)
        rows = cal.epoch_crossings(fire)
        sources = [(fire['pointer'], 6 * fire['k'] + 4, 6 * fire['k'] + 5, fire['pointer'], 'fire')]
        for n, r in rows.items():
            if r['kind'] == 'c' and r['odd']:
                sources.append((n, 3 * r['time'] + 4 + r['tail_lambda'], 3 * r['time'] + 5,
                                n - r['epsilon'], 'c'))
        for n, x, th, sigma, kind in sources:
            st, real = bounded_walk(cal, x, th, sigma)
            assert st == 'end'
            first = None
            for i, (j, g, xx, tt) in enumerate(real):
                r = cal.crossing(j - 1)
                if not r['odd']:
                    break
                if r['kind'] == 'a':
                    first = (i, j, g, xx, tt, r)
                    break
            for eta in range(-8, 9):
                st, shifted = bounded_walk(cal, x, th + eta, sigma)
                checked += 1
                if eta == 0:
                    stats['zero_shift'] += 1
                    continue
                if first is None:
                    stats['no_A'] += 1
                    continue
                i, j, g, xx, tt, r = first
                yr = 2 * tt + 3 * r['time'] - xx / 2
                tr = tt + 3 + 3 * r['time']
                ys = yr + 2 * eta
                ts = tr + eta
                q = val(yr)
                h = val(2 * eta)
                remaining = sigma - g - 1
                suffix_status, suffix = bounded_walk(cal, ys, ts, remaining)
                assert suffix_status == st
                if st == 'end':
                    assert [(j0, g0 - g - 1) for j0, g0, _, _ in shifted[i + 1:]] == [(j0, g0) for j0, g0, _, _ in suffix]
                s_prime = (tr - 5) / 3
                assert s_prime.denominator == 1
                lam_new = yr - (3 * s_prime + 4)
                firstA.append(dict(P=P, kind=kind, n=n, m=j, s_A=(tt - 5) / 3, x_A=xx,
                                   theta_A=tt, tau=r['time'], y=yr, t_out=tr, s_out=s_prime,
                                   lam_new=lam_new, q=q, eta=eta, h=h,
                                   ys=ys, ts=ts, remaining=remaining,
                                   sigma=sigma, g=g))
                if q != h:
                    assert val(ys) == min(q, h) <= 4
                    stats['valuation_mismatch_closes'] += 1
                else:
                    assert q <= 4 and not cal.crossing(q - 1)['odd']
                    assert i + 2 == len(real)
                    stats['collision_' + st] += 1
                    v = val(ys)
                    delta = int(ts - ys) % (1 << (v + 1))
                    cs, cr = bounded_walk(cal, 1 << v, (1 << v) + delta, v + 1, signed=True)
                    cert['minimal_class_' + cs] += 1
                    K = max(jj + gg for jj, gg, _, _ in suffix) + 1
                    ss, sr = bounded_walk(cal, int(ys) % (1 << K), int(ts) % (1 << K), K, signed=True)
                    assert ss == 'end'
                    assert [(jj, gg) for jj, gg, _, _ in sr] == [(jj, gg) for jj, gg, _, _ in suffix]
                    assert K <= remaining
                    max_extra = max(max_extra, K - v - 1)
                    if cs != 'end':
                        ex_bits.append(dict(P=P, kind=kind, eta=eta, j=v, delta=delta,
                                            minimal_status=cs, K=K,
                                            x_residue=int(ys) % (1 << K),
                                            theta_residue=int(ts) % (1 << K),
                                            word=[jj for jj, _, _, _ in sr],
                                            ys_bits=int(ys).bit_length(),
                                            actual_ys_high=(int(ys) >> K),
                                            actual_ts_high=(int(ts) >> K)))
                    if len(collisions) < 4000:
                        collisions.append(dict(P=P, kind=kind, n=str(n), eta=eta, q=q, h=h,
                                               ys=ys, ts=ts, word=[a[0] for a in suffix],
                                               real_len=len(real), i=i))
    res['counts'] = dict(stats)
    res['cases'] = checked
    res['certificates'] = dict(cert)
    res['max_extra_bits'] = max_extra
    res['extra_examples'] = ex_bits

    # constants from section 2
    mA = [d for d in firstA]
    res['min_m'] = min(d['m'] for d in mA)
    res['min_s_A'] = str(min(d['s_A'] for d in mA))
    res['min_y'] = min(d['y'] for d in mA)
    res['min_y_shifted'] = min(d['ys'] for d in mA)
    res['min_slack_6sA5_minus_xA'] = str(min(6 * d['s_A'] + 5 - d['x_A'] for d in mA))
    res['min_lam_new'] = str(min(d['lam_new'] for d in mA))
    res['lam_new_formula_bad'] = sum(1 for d in mA if d['lam_new'] != 3 * d['s_A'] + 3 - d['x_A'] / 2)
    res['y_lt_3sout4'] = sum(1 for d in mA if d['y'] < 3 * d['s_out'] + 4)
    res['y_lt_28'] = sum(1 for d in mA if d['y'] < 28)
    res['y_lower_bound_from_xA'] = str(min(3 * d['s_A'] + 6 * (d['tau'] // 2) + F(15, 2) for d in mA))
    res['q_dist'] = dict(Counter(d['q'] for d in mA if d['eta'] == -3))
    res['min_q'] = min(d['q'] for d in mA)
    res['n_sources'] = len(set((d['P'], d['kind'], d['n']) for d in mA))
    res['n_sources_c'] = len(set((d['P'], d['n']) for d in mA if d['kind'] == 'c'))
    res['min_chain_param_real'] = min(d['m'] for d in mA)
    res['min_tau_first_a'] = min(d['tau'] for d in mA)

    # P=90 vs P=234 comparison
    pair = [d for d in ex_bits if d['P'] in (90, 234)]
    res['p90_p234'] = pair
    # all four exceptional cases: distinct residue classes and words
    res['exception_classes'] = [(d['P'], d['K'], d['x_residue'], d['theta_residue'], tuple(d['word'])) for d in ex_bits]
    res['exception_distinct'] = len(set((d['K'], d['x_residue'], d['theta_residue'], tuple(d['word'])) for d in ex_bits))
    res['exception_distinct_words'] = len(set(tuple(d['word']) for d in ex_bits))

    # crossing(-1) and base parity
    try:
        r = cal.crossing(-1)
        res['crossing_minus1'] = repr(r)
    except Exception as e:
        res['crossing_minus1'] = 'EXC ' + type(e).__name__ + ': ' + str(e)
    res['base_odd_0_3'] = [cal.crossing(n)['odd'] for n in range(4)]
    res['crossing_0_3_kinds'] = [cal.crossing(n)['kind'] for n in range(4)]

    # lambda nonnegativity over all crossings n<4000
    neg = []
    for n in range(0, 4000):
        r = cal.crossing(n)
        hl = r['head_lambda']
        tl = r['tail_lambda']
        if hl is not None and hl < 0:
            neg.append(('head', n, hl))
        if tl is not None and tl < 0:
            neg.append(('tail', n, tl))
    res['negative_lambda_crossings_n_lt_4000'] = neg[:20]
    res['n_negative_lambda'] = len(neg)

    # collision table: eta -> required q distribution
    ct = {}
    for d in collisions:
        if d['q'] == d['h']:
            ct.setdefault(str(d['eta']), set()).add(d['q'])
    res['collision_table_check'] = {k: sorted(v) for k, v in sorted(ct.items(), key=lambda kv: int(kv[0]))}
    # total collision cases and their real tail length
    res['collision_real_len_dist'] = dict(Counter(d['real_len'] - d['i'] - 1 for d in collisions))

    # the resonance example for HP's x* != 0
    st, rows = bounded_walk(cal, 32, 5, 10)
    res['resonance_x32_theta5_P10'] = (st, [(j, g, str(x), str(t)) for j, g, x, t in rows])

    OUT.write_text(json.dumps(res, indent=2, default=str) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in res.items() if k not in ('p90_p234', 'collision_table_check')}, indent=1, default=str))


if __name__ == '__main__':
    main()
