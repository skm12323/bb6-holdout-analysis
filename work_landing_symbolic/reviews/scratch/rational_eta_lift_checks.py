"""Rational-eta diagnostics on the synthetic congruent lifts of
work_c3_drift/verify_shift_transport.py.

The document's lemma is stated for integer eta only.  This script checks
whether the same 2-adic shadowing conclusion survives for rational eta with
odd denominators on the *synthetic* lifts (which are explicitly not claimed
canonical).  A failure would show the integer-only restriction is essential;
agreement is only diagnostic, not a proof.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys, json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, val


def bounded_walk(cal, x, th, precision):
    x, th = F(x), F(th)
    loss = 0
    rows = []
    for _ in range(256):
        if x == 0:
            return 'zero', rows
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
    etas = [F(-7, 3), F(1, 3), F(-5) + F(8, 3), F(-5) + F(8, 9),
            F(5, 9), F(-1, 27), F(2, 3), F(-2, 3)]
    cases = []
    status = Counter()
    for p in range(5, 257):
        a = cal.crossing(p - 1)
        if not a['odd'] or a['kind'] != 'a':
            continue
        xc = 3 * a['time'] + 4
        tc = xc + 1
        sc = p - 1
        # only references with a nontrivial continuation under integer shifts
        for eta in etas:
            rstatus, ref = bounded_walk(cal, xc, tc + eta, sc)
            astatus, rows = bounded_walk(cal, xc + (1 << sc), tc + eta + 3 * (1 << sc), sc)
            same = (rstatus == astatus and
                    [(j, g) for j, g, _, _ in rows] == [(j, g) for j, g, _, _ in ref])
            prec_ok = True
            if same:
                prec_ok = all(min(val(x - y), val(t - u)) >= sc - g
                              for (j, g, x, t), (jj, gg, y, u) in zip(rows, ref))
            status[(rstatus, astatus, same, prec_ok, len(ref))] += 1
            if (len(ref) >= 2 or not same or not prec_ok) and len(cases) < 40:
                cases.append(dict(p=p, eta=str(eta), ref_status=rstatus,
                                  lift_status=astatus, same_word=same,
                                  precision_ok=prec_ok,
                                  ref_rows=[(j, g) for j, g, _, _ in ref],
                                  lift_rows=[(j, g) for j, g, _, _ in rows]))
    out = dict(status='PASS' if all(s[2] and s[3] for s in status) else 'FAIL',
               counts=[dict(ref_status=k[0], lift_status=k[1], same=k[2],
                            precision_ok=k[3], ref_len=k[4], n=v)
                       for k, v in sorted(status.items())],
               nontrivial_cases=cases)
    Path(__file__).with_name('rational_eta_lift_checks.json').write_text(
        json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in out.items() if k != 'nontrivial_cases'}, indent=2))
    print('nontrivial examples:', len(cases))


if __name__ == '__main__':
    main()
