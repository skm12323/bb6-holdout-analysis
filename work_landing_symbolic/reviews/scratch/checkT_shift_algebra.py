"""Exact algebra check: transport shift eta vs accepted source-shift class s.

An outer chain T with parameter j=n+1 reads the source D's c crossing X(n).
x_T = 2^j u (we take u=1), Theta_T = x_T + theta.
"""
from pathlib import Path
from fractions import Fraction as F
import sys, json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, first_fire, val   # noqa: E402

OUT = Path(__file__).with_name('checkT_shift_algebra.json')


def main():
    cal = Calendar(512)
    rows = []
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
        if d['kind'] != 'c' or not d['odd'] or d['epsilon'] != 5:
            continue
        if n > 200000:
            continue
        lam = d['tail_lambda']
        tau = d['time']
        xD = 3 * tau + 4 + lam
        thD = 3 * tau + 5
        thetaD = thD - xD
        s = thetaD - 2
        sd = n - d['epsilon']
        j = n + 1
        cD = (d['head_ratio'] + 2 * d['tail_ratio']) / 2 * (1 << j)
        for theta in (0, 1, 2, 5, -3):
            xT = F(1 << j)
            thT = xT + theta
            u = F(1)
            xU = cD * u + xD
            thU = thT + thD - 2
            eta = theta - 2
            rows.append(dict(P=P, p=p, n=n, j=j, lam=str(lam), tau=tau, sigmaD=sd,
                             v2_cD=val(cD), cD_eq_sigma=(val(cD) == sd),
                             theta=theta, eta=eta, s_bits=int(abs(s)).bit_length(),
                             xU_minus_xD_v2=val(xU - xD),
                             xU_minus_xC_v2=val(xU - 10),
                             phase_minus_thD_eta_v2=val(thU - (thD + eta)),
                             phase_minus_thC_eta_v2=val(thU - (11 + eta)),
                             thetaU_landing_v2=val(thU - xU - (theta + s)),
                             thetaU_defect_is_theta_plus_s=(val(thU - xU - (theta + s)) >= sd),
                             record_RT=j,
                             record_successor_bound=sd + (1 + d['epsilon'])))
    res = dict(n=len(rows), samples=rows[:10],
               all_cD_sigma=all(r['cD_eq_sigma'] for r in rows),
               all_x_agree=all(r['xU_minus_xD_v2'] >= r['sigmaD'] for r in rows),
               all_phase_agree=all(r['phase_minus_thD_eta_v2'] >= r['j'] for r in rows),
               all_ancestor_agree=all(r['xU_minus_xC_v2'] >= 4 and r['phase_minus_thC_eta_v2'] >= 4 for r in rows),
               all_landing=all(r['thetaU_defect_is_theta_plus_s'] for r in rows),
               eta_is_theta_minus_2=all(r['eta'] == r['theta'] - 2 for r in rows))
    OUT.write_text(json.dumps(res, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in res.items() if k != 'samples'}, indent=1))
    print(json.dumps(rows[:5], indent=1))


if __name__ == '__main__':
    main()
