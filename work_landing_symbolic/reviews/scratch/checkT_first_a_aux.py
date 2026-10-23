"""Auxiliary exact checks for FIRST_A constants and source counts (checker T)."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys, json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, first_fire, val   # noqa: E402

OUT = Path(__file__).with_name('checkT_first_a_aux.json')


def bounded_walk(cal, x, th, precision):
    x, th = F(x), F(th)
    loss = 0
    rows = []
    for _ in range(64):
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
    fires = 0
    cs = 0
    firstA = []
    lam_mass = []
    for P in range(5, 257):
        fire = first_fire(cal, P)
        fires += 1
        rows = cal.epoch_crossings(fire)
        sources = [(fire['pointer'], 6 * fire['k'] + 4, 6 * fire['k'] + 5, fire['pointer'], 'fire')]
        for n, r in rows.items():
            if r['kind'] == 'c' and r['odd']:
                cs += 1
                sources.append((n, 3 * r['time'] + 4 + r['tail_lambda'], 3 * r['time'] + 5,
                                n - r['epsilon'], 'c'))
        for n, x, th, sigma, kind in sources:
            st, real = bounded_walk(cal, x, th, sigma)
            assert st == 'end'
            for i, (j, g, xx, tt) in enumerate(real):
                r = cal.crossing(j - 1)
                if not r['odd']:
                    break
                if r['kind'] == 'a':
                    sA = (tt - 5) / 3
                    assert sA.denominator == 1
                    lam = xx - (3 * sA + 4)
                    lam_mass.append(dict(P=P, kind=kind, n=n, s_A=str(sA), x_A=int(xx),
                                         lam_cur=str(lam), mass_bound=str(3 * sA + 1),
                                         below0=lam < 0, above_mass=lam > 3 * sA + 1,
                                         m=j, tau=r['time']))
                    break

    def fmax(key):
        return max(lam_mass, key=lambda z: F(z[key]))

    res = dict(n_fire_sources=fires, n_c_sources=cs, n_sources=fires + cs,
               n_first_a_sources=len(lam_mass),
               kind_dist=dict(Counter(z['kind'] for z in lam_mass)),
               n_lam_below0=sum(z['below0'] for z in lam_mass),
               n_lam_above_mass=sum(z['above_mass'] for z in lam_mass),
               min_lam=str(min(F(z['lam_cur']) for z in lam_mass)),
               max_lam=str(max(F(z['lam_cur']) for z in lam_mass)),
               max_slack_mass=str(min(F(z['mass_bound']) - F(z['lam_cur']) for z in lam_mass)),
               min_sA=str(min(F(z['s_A']) for z in lam_mass)),
               n_xA_le_6sA5=sum(1 for z in lam_mass if z['x_A'] <= 6 * F(z['s_A']) + 5),
               n_first_a=len(lam_mass),
               m_values=sorted(set(z['m'] for z in lam_mass)),
               tau_values=sorted(set(z['tau'] for z in lam_mass)))
    OUT.write_text(json.dumps(res, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
