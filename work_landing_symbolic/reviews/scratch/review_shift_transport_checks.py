"""Reviewer scratch checks for work_c3_drift/SHIFT_TRANSPORT.md.

Independent re-run of the verifier's loops with additional diagnostics:
 - canonical-pair ancestor distribution and reference tail lengths;
 - forced-shift controls: exact next numerator and record ceiling;
 - rational-eta probes on the same canonical AA pairs (not claimed by the
   document, which states only integer eta);
 - a small direct test of the transport lemma's HP hypothesis on rational eta.
Writes JSON next to this file.  Does not modify any non-work_landing_symbolic file.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys, json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, first_fire, val


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
    out = {}

    # ---- first loop: canonical AA pairs, integer eta ----
    pairs = []
    states = 0
    ref_lens = Counter()
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
        assert sd > sc and min(val(xd - xc), val(td - tc)) >= sc
        pairs.append(dict(P=P, p=p, source_index=str(n), ancestor_index=p,
                          precision=sc, sigma_D=sd,
                          x_diff_val=val(xd - xc), theta_diff_val=val(td - tc)))
        for eta in range(-32, 33):
            status, ref = bounded_walk(cal, xc, tc + eta, sc)
            assert status == 'end', (P, eta, status)
            ref_lens[len(ref)] += 1
            actual, rows = bounded_walk(cal, xd, td + eta, sc)
            assert actual == 'end'
            assert [(j, g) for j, g, _, _ in rows] == [(j, g) for j, g, _, _ in ref]
            for (j, g, x, t), (jj, gg, y, u) in zip(rows, ref):
                assert min(val(x - y), val(t - u)) >= sc - g
                states += 1
    out['canonical_pairs'] = pairs
    out['ancestor_p_values'] = sorted(set(p['p'] for p in pairs))
    out['ancestor_precisions'] = sorted(set(p['precision'] for p in pairs))
    out['integer_eta_cases'] = sum(ref_lens.values())
    out['reference_tail_lengths'] = dict(sorted(ref_lens.items()))
    out['matched_states'] = states

    # ---- second loop: canonical fire references, integer eta + forced controls ----
    synthetic = Counter()
    synthetic_states = 0
    synthetic_lens = Counter()
    forced = []
    nfire = 0
    for p in range(5, 257):
        a = cal.crossing(p - 1)
        if not a['odd'] or a['kind'] != 'a':
            continue
        nfire += 1
        xc = 3 * a['time'] + 4
        tc = xc + 1
        sc = p - 1
        shifts = list(range(-32, 33))
        q = val(xc)
        nxt = cal.crossing(q - 1)
        if nxt['odd'] and nxt['kind'] == 'a':
            forcing = (1 << sc) - 2 * tc - 3 * nxt['time'] + xc // 2
            assert forcing % 2 == 0
            shifts.append(forcing // 2)
        for eta in shifts:
            status, ref = bounded_walk(cal, xc, tc + eta, sc)
            synthetic[status] += 1
            synthetic_lens[len(ref)] += 1
            if status != 'end':
                # verify the forced numerator exactly when this is the forced shift
                xn = F(2 * (tc + eta) + 3 * nxt['time']) - F(xc, 2)
                forced.append(dict(p=p, eta=int(eta), status=status,
                                   next_x=int(xn) if xn.denominator == 1 else str(xn),
                                   next_x_is_2sc=(xn == (1 << sc)),
                                   q=q, sc=sc, ref_rows=[(j, g) for j, g, _, _ in ref]))
                continue
            actual, rows = bounded_walk(cal, xc + (1 << sc), tc + eta + 3 * (1 << sc), sc)
            assert actual == 'end'
            assert [(j, g) for j, g, _, _ in rows] == [(j, g) for j, g, _, _ in ref]
            for (j, g, x, t), (jj, gg, y, u) in zip(rows, ref):
                assert min(val(x - y), val(t - u)) >= sc - g
                synthetic_states += 1
    out['fire_references'] = nfire
    out['synthetic_status'] = dict(synthetic)
    out['synthetic_reference_tail_lengths'] = dict(sorted(synthetic_lens.items()))
    out['synthetic_matched_states'] = synthetic_states
    out['forced_controls'] = forced

    # ---- rational eta probes (document states integer eta only) ----
    probes = []
    rat_etas = [F(-7, 3), F(1, 3), F(-5) + F(8, 3), F(-5) + F(8, 9), F(5, 9), F(-1, 27)]
    for pr in out['canonical_pairs']:
        P, p = pr['P'], pr['p']
        a = cal.crossing(P - 1)
        fire = first_fire(cal, P)
        n = fire['pointer'] + 3
        d = cal.crossing(n)
        c = cal.crossing(p)
        xd = 3 * d['time'] + 4 + d['tail_lambda']
        td = 3 * d['time'] + 5
        xc = 3 * c['time'] + 4
        tc = 3 * c['time'] + 5
        sc = p - 1
        for eta in rat_etas:
            rstatus, ref = bounded_walk(cal, xc, tc + eta, sc)
            astatus, rows = bounded_walk(cal, xd, td + eta, sc)
            same = (rstatus == astatus and
                    [(j, g) for j, g, _, _ in rows] == [(j, g) for j, g, _, _ in ref])
            prec_ok = True
            if same:
                for (j, g, x, t), (jj, gg, y, u) in zip(rows, ref):
                    if min(val(x - y), val(t - u)) < sc - g:
                        prec_ok = False
            probes.append(dict(P=P, p=p, eta=str(eta), ref_status=rstatus,
                               actual_status=astatus, same_word=same,
                               precision_ok=prec_ok, ref_len=len(ref),
                               actual_len=len(rows)))
    out['rational_eta_probes'] = probes

    out['status'] = 'PASS'
    out['scope'] = ('Reviewer recomputation. Rational-eta probes are diagnostics only; '
                    'the document claims integer eta only. Counts must agree with '
                    'work_c3_drift/transport_checks.json.')
    path = Path(__file__).with_name('review_shift_transport_checks.json')
    path.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in out.items() if k not in ('canonical_pairs', 'rational_eta_probes')}, indent=2))
    print('rational probes:', len(probes), 'all same_word=',
          all(x['same_word'] for x in probes), 'all precision_ok=',
          all(x['precision_ok'] for x in probes))


if __name__ == '__main__':
    main()
