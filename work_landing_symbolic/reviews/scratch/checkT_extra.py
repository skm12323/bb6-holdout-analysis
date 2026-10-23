"""Extra checks: (i) source-shift classes for A/AA/BA, (ii) deep first-a lambda mass."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys, json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, first_fire, val   # noqa: E402

OUT = Path(__file__).with_name('checkT_extra.json')


def bw(cal, x, th, prec):
    x, th = F(x), F(th)
    loss = 0
    rows = []
    for _ in range(64):
        if x == 0:
            return 'zero', rows
        j = val(x)
        if j + loss >= prec:
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
    shifts = Counter()
    deep = []
    for P in range(5, 257):
        f0 = cal.crossing(P - 1)
        if not f0['odd']:
            continue
        fire = first_fire(cal, P)
        rho = fire['pointer']
        cat = None
        if f0['kind'] == 'a':
            cat = 'A'
        elif f0['kind'] == 'b':
            y = 3 * f0['time'] + 4
            p = val(y)
            s2 = cal.crossing(p - 1)
            if s2['odd'] and s2['kind'] == 'a':
                cat = 'BA'
        if cat is None:
            continue
        n = rho + 2
        r = cal.crossing(n)
        if r['kind'] != 'c' or not r['odd']:
            continue
        q = r['omega']
        lam = r['tail_lambda']
        s = -1 - lam
        shifts[(cat, r['epsilon'], s % (1 << (q + 1)))] += 1
        # first a-step for the fire source
        fire = first_fire(cal, P)
        x0 = F(6 * fire['k'] + 4)
        th = x0 + 1
        sigma = fire['pointer']
        st, rows = bw(cal, x0, th, sigma)
        for i, (j, g, xx, tt) in enumerate(rows):
            rr = cal.crossing(j - 1)
            if not rr['odd']:
                break
            if rr['kind'] == 'a':
                sA = (tt - 5) / 3
                lam_in = xx - (3 * sA + 4)
                deep.append(dict(P=P, i=i, g=g, m=j, s_A=int(sA), x_A=int(xx),
                                 lambda_chain=int(lam_in),
                                 minusslash=str(lam_in),
                                 below0=lam_in < 0,
                                 eq_1_minus_x0_over_4=(lam_in == 1 - x0 / 4),
                                 xA_le_6sA5=(xx <= 6 * sA + 5)))
                break
    # AA histories
    aa = []
    for P in range(5, 257):
        fire = first_fire(cal, P)
        x0 = F(6 * fire['k'] + 4)
        x, th = x0, x0 + 1
        kinds = ''
        for _ in range(3):
            j = val(x)
            r = cal.crossing(j - 1)
            if not r['odd']:
                break
            kinds += r['kind']
            if r['kind'] == 'a':
                x = 2 * th + 3 * r['time'] - x / 2
            else:
                x = (r['head_ratio'] + 2 * r['tail_ratio']) * x / 2 + r['head_lambda'] + 2 * r['tail_lambda'] + 3
            th += 3 + 3 * r['time']
        if len(kinds) >= 2 and kinds[:2] == 'aa':
            r = cal.crossing(fire['pointer'] + 3)
            if r['kind'] == 'c' and r['odd']:
                q = r['omega']
                lam = r['tail_lambda']
                s = -1 - lam
                aa.append(dict(P=P, n=fire['pointer'] + 3, eps=r['epsilon'], omega=q,
                               lam=str(lam), s_class=str(s % (1 << (q + 1)))))
    res = dict(source_shifts={f'{k[0]}/{k[1]}': str(v) for k, v in shifts.items()},
               AA_samples=aa[:6], n_AA=len(aa),
               n_first_a=len(deep),
               deep_negative=[d for d in deep if d['below0']],
               all_bound_ok=all(d['xA_le_6sA5'] for d in deep),
               min_lambda=str(min(d['lambda_chain'] for d in deep)),
               same_formula=all(d['eq_1_minus_x0_over_4'] for d in deep if d['below0']))
    OUT.write_text(json.dumps(res, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in res.items() if k != 'deep_negative'}, indent=1))
    print('deep negative count', len(res['deep_negative']))
    for d in res['deep_negative']:
        print({k: d[k] for k in ('P', 'i', 'g', 'm', 'lambda_chain', 'xA_le_6sA5')})


if __name__ == '__main__':
    main()
