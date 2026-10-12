"""Blind Auditor 2 — S2 family fits: x = alpha*w + gamma (w = 1,3,5).

For every v in 1..2000 (plus 2500, 4000) run the excursion at w = 1, 3, 5;
align fires by index; verify structural identity (role, rho, j) across w;
fit alpha = (x3-x1)/2, gamma = x1-alpha; verify x5 = 5*alpha+gamma; check
v2(gamma) < v2(alpha) (which forces u >= 3 for every odd w); verify
u(w) >= 3 and v2(x(w)) = v2(gamma) for odd w up to 31.  Families keyed by
(role, alpha, gamma).  Writes scratch/blind2_fits.json.
"""
import json
import sys
import time

sys.path.insert(0, '.')
from blind2_lib import Proc, brole, cinfo, run_orbit, v2


def fire_records(w, v):
    """Full fire records for one excursion."""
    ex, fires, fin, finA, ell = run_orbit(w, v, full=True)
    return fires, fin


def main():
    t0 = time.time()
    vs = list(range(1, 2001)) + [2500, 4000]
    fams = {}
    n_fitted = 0
    viol_struct = []
    viol_affine = []
    viol_v2 = []
    viol_safety = []
    alpha0 = []
    fin_bad = []
    max_j_by_role = {}
    for v in vs:
        F = {}
        fins = {}
        for w in (1, 3, 5):
            f, fin = fire_records(w, v)
            F[w] = f
            fins[w] = fin
        if not (fins[1] == fins[3] == fins[5] == 'singleton'):
            fin_bad.append((v, fins))
        if not (len(F[1]) == len(F[3]) == len(F[5])):
            viol_struct.append((v, 'fire-count', len(F[1]), len(F[3]), len(F[5])))
            continue
        for i, (f1, f3, f5) in enumerate(zip(F[1], F[3], F[5])):
            # structural identity across w
            if (f1[2], f1[3], f1[4]) != (f3[2], f3[3], f3[4]) or \
               (f1[2], f1[3], f1[4]) != (f5[2], f5[3], f5[4]):
                viol_struct.append((v, i, f1[2:5], f3[2:5], f5[2:5]))
                continue
            role, rho, j = f1[2], f1[3], f1[4]
            x1, x3, x5 = f1[5], f3[5], f5[5]
            if (x3 - x1) % 2 != 0:
                viol_affine.append((v, i, 'odd-diff', role, rho, j))
                continue
            alpha = (x3 - x1) // 2
            gamma = x1 - alpha
            if x5 != 5 * alpha + gamma:
                viol_affine.append((v, i, 'w5-mismatch', role, rho, j))
                continue
            n_fitted += 1
            if role not in max_j_by_role or j > max_j_by_role[role][0]:
                max_j_by_role[role] = (j, v, i)
            if alpha == 0 or gamma == 0:
                alpha0.append((v, i, role, rho, j, alpha, gamma))
                continue
            va, vg = v2(alpha), v2(gamma)
            if vg >= va:
                viol_v2.append((v, i, role, rho, j, alpha, gamma, va, vg))
                continue
            # safety for odd w in 1..31
            for w in range(1, 32, 2):
                x = alpha * w + gamma
                if v2(x) != vg:
                    viol_safety.append((v, i, 'v2', w, role, rho, j))
                    break
                u = x >> vg
                if u < 3 or u % 2 == 0:
                    viol_safety.append((v, i, 'u', w, role, rho, j, u))
                    break
            key = (role, alpha, gamma)
            d = fams.setdefault(key, {'n': 0, 'rho': set(), 'j': set(), 'vs': set()})
            d['n'] += 1
            d['rho'].add(rho)
            d['j'].add(j)
            d['vs'].add(v)
    fam_summary = []
    for (role, alpha, gamma), d in fams.items():
        fam_summary.append({
            'role': role, 'alpha': alpha, 'gamma': gamma,
            'v2alpha': v2(alpha), 'v2gamma': v2(gamma),
            'n': d['n'], 'n_rho': len(d['rho']), 'n_j': len(d['j']),
            'n_v': len(d['vs']), 'j_set': sorted(d['j'])[:4],
            'u_at_w1': (alpha + gamma) >> v2(gamma),
        })
    fam_summary.sort(key=lambda r: -r['n'])
    out = {
        'n_v': len(vs), 'n_fitted': n_fitted,
        'n_families': len(fams),
        'families_per_role': {},
        'viol_struct': viol_struct[:10], 'n_struct': len(viol_struct),
        'viol_affine': viol_affine[:10], 'n_affine': len(viol_affine),
        'viol_v2': viol_v2[:10], 'n_v2': len(viol_v2),
        'viol_safety': viol_safety[:10], 'n_safety': len(viol_safety),
        'alpha_or_gamma_zero': alpha0[:10], 'n_alpha0': len(alpha0),
        'fin_bad': fin_bad[:10], 'n_fin_bad': len(fin_bad),
        'max_j_by_role': {r: list(x) for r, x in max_j_by_role.items()},
        'top_families': fam_summary[:25],
    }
    fr = {}
    for r in ('run', 'seam', 'tail', 'zero'):
        fr[r] = {'n_families': sum(1 for f in fam_summary if f['role'] == r),
                 'n_fires': sum(f['n'] for f in fam_summary if f['role'] == r)}
    out['families_per_role'] = fr
    with open('blind2_fits.json', 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print('elapsed', round(time.time() - t0, 1))
    print('fitted fires:', n_fitted, ' families:', len(fams))
    print('per role:', fr)
    print('viol struct/affine/v2/safety/alpha0/fin:',
          len(viol_struct), len(viol_affine), len(viol_v2), len(viol_safety),
          len(alpha0), len(fin_bad))
    print('max j by role:', max_j_by_role)
    print('top families:')
    for f in fam_summary[:15]:
        print('  ', f['role'], 'alpha=2^%d*%d gamma=2^%d*%d n=%d #rho=%d #j=%d j=%s u(w=1)=%d'
              % (f['v2alpha'], f['alpha'] >> f['v2alpha'], f['v2gamma'],
                 f['gamma'] >> f['v2gamma'], f['n'], f['n_rho'], f['n_j'],
                 f['j_set'], f['u_at_w1']))


if __name__ == '__main__':
    main()
