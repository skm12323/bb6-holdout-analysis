"""Independent recomputation for the SHIFT_TRANSPORT review items (checker T).

Writes only inside work_landing_symbolic/reviews/scratch/.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys, json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, first_fire, val   # noqa: E402

OUT = Path(__file__).with_name('checkT_transport.json')


def bounded_walk(cal, x, th, precision, signed=False):
    x, th = F(x), F(th)
    loss = 0
    rows = []
    for _ in range(128):
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

    # ---------- loop 1: four actual AA/earlier-b ancestor pairs ----------
    pairs = []
    stats = Counter()
    matched = 0
    tail_lens = Counter()
    for P in range(5, 257):
        a = cal.crossing(P - 1)
        if not a['odd'] or a['kind'] != 'a':
            continue
        p = val(3 * a['time'] + 2)
        b = cal.crossing(p - 1)
        if not b['odd'] or b['kind'] != 'a':
            continue
        fire = first_fire(cal, P)
        n = fire['pointer'] + 3
        d = cal.crossing(n)
        c = cal.crossing(p)
        assert d['kind'] == 'c' and c['kind'] == 'b'
        xd = 3 * d['time'] + 4 + d['tail_lambda']
        td = 3 * d['time'] + 5
        xc = 3 * c['time'] + 4
        tc = 3 * c['time'] + 5
        sc = p - 1
        sd = n - d['epsilon']
        fact = dict(P=P, p=p, n=n, sc=sc, sd=sd,
                    xc=int(xc), tc=int(tc), xd=int(xd), td=int(td),
                    tau_p=cal.crossing(p)['time'],
                    tau_pm1=cal.crossing(p - 1)['time'],
                    fire_at_pm1_x=3 * cal.crossing(p - 1)['time'] + 4,
                    b_entry_y=3 * cal.crossing(p - 1)['time'] + 4)
        pairs.append(fact)
        for eta in range(-32, 33):
            status, ref = bounded_walk(cal, xc, tc + eta, sc)
            stats[status] += 1
            tail_lens[len(ref)] += 1
            if status != 'end':
                continue
            actual, rows = bounded_walk(cal, xd, td + eta, sc)
            assert actual == 'end'
            assert [(j, g) for j, g, _, _ in rows] == [(j, g) for j, g, _, _ in ref]
            matched += len(rows)
    res['loop1'] = dict(n_pairs=len(pairs), pairs=pairs, reference_status=dict(stats),
                        reference_tail_lengths={str(k): v for k, v in sorted(tail_lens.items())},
                        matched_states=matched)

    # ---------- loop 2: fire-shaped references + synthetic lifts ----------
    syn = Counter()
    syn_len = Counter()
    syn_states = 0
    fire_ref_count = 0
    forced = []
    examples = []
    for p in range(5, 257):
        a = cal.crossing(p - 1)
        if not a['odd'] or a['kind'] != 'a':
            continue
        fire_ref_count += 1
        xc = 3 * a['time'] + 4
        tc = xc + 1          # fire-shaped (x, x+1) --- NOT (y,y)
        q = val(xc)
        nxt = cal.crossing(q - 1)
        shifts = list(range(-32, 33))
        forcing = None
        if nxt['odd'] and nxt['kind'] == 'a':
            forcing = ((1 << (p - 1)) - 2 * tc - 3 * nxt['time'] + xc // 2)
            assert forcing % 2 == 0
            forcing //= 2
            shifts.append(forcing)
            forced.append(dict(p=p, eta=forcing, tau_nxt=nxt['time']))
        for eta in shifts:
            status, ref = bounded_walk(cal, xc, tc + eta, p - 1)
            syn[status] += 1
            syn_len[len(ref)] += 1
            if status != 'end':
                if len(examples) < 8 and eta not in (-32, 32) and len(shifts) > 65:
                    examples.append(dict(p=p, eta=eta, status=status, tail=[r[0] for r in ref]))
                continue
            actual, rows = bounded_walk(cal, xc + (1 << (p - 1)), tc + eta + 3 * (1 << (p - 1)), p - 1)
            assert actual == 'end'
            assert [(j, g) for j, g, _, _ in rows] == [(j, g) for j, g, _, _ in ref]
            for (j, g, x, t), (jj, gg, y, u) in zip(rows, ref):
                assert min(val(x - y), val(t - u)) >= (p - 1) - g
            syn_states += len(rows)
    res['loop2'] = dict(n_fire_shaped_references=fire_ref_count, statuses=dict(syn),
                        tail_lengths={str(k): v for k, v in sorted(syn_len.items())},
                        matched_states=syn_states, forced_shifts=forced,
                        nonend_examples=examples,
                        total_shifts=sum(syn.values()),
                        nontrivial=sum(v for k, v in syn_len.items() if k > 1))

    # ---------- forced controls: next a-numerator equals 2^(p-1) ----------
    ctrl = []
    for f in forced:
        p = f['p']
        a = cal.crossing(p - 1)
        xc = 3 * a['time'] + 4
        tc = xc + 1
        q = val(xc)
        r = cal.crossing(q - 1)
        xnext = 2 * (tc + f['eta']) + 3 * r['time'] - xc / 2
        ctrl.append(dict(p=p, eta=f['eta'], next_x=int(xnext), is_2_pow=bool(xnext == 1 << (p - 1)),
                         eta_bits=int(f['eta']).bit_length()))
    res['forced_controls'] = ctrl

    # ---------- is the loop-1 ancestor the fire or the b-entry? ----------
    anc = []
    for f in pairs:
        p = f['p']
        anc.append(dict(P=f['P'], p=p, tau_p=f['tau_p'], tau_pm1=f['tau_pm1'],
                        tau_equal=f['tau_p'] == f['tau_pm1'],
                        xc=f['xc'], fire_x=f['fire_at_pm1_x'], tc=f['tc'],
                        fire_phi=f['fire_at_pm1_x'] + 1,
                        b_entry=f['b_entry_y'],
                        is_fire_shaped=(f['tc'] - f['xc'] == 1),
                        is_b_entry_shaped=(f['tc'] == f['xc'])))
    res['ancestor_shape'] = anc

    OUT.write_text(json.dumps(res, indent=2, default=str) + '\n', encoding='utf-8')
    print(json.dumps({k: (v if k not in ('loop2',) else {kk: vv for kk, vv in v.items() if kk != 'nonend_examples'})
                      for k, v in res.items()}, indent=1, default=str)[:6000])


if __name__ == '__main__':
    main()
