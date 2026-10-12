"""Blind Auditor 2 — S4 assembly details.

(a) role coverage of every fire;
(b) spike census: k = 16s+10 class, j = 5+v2(3s+2), 2^J <= 6k+4,
    k <= 0.4465*rho, margin arithmetic forcing p-J large for big J;
(c) nested parameter decrease (j < par_j, rho <= par_j-2), plus
    extra stats for the report (j vs 3log2(rho)+3, seam/tail j stats).
Reads blind2_sweep.json; reruns targeted excursions.
"""
import json
import sys

sys.path.insert(0, '.')
from blind2_lib import Agg, run_orbit, v2


def main():
    with open('blind2_sweep.json') as f:
        sw = json.load(f)

    # fresh aggregate over the full audited range with spike details kept
    agg = Agg()
    for v in range(1, 2001):
        agg.level_seqs = {}
        run_orbit(1, v, agg=agg)
    for v in (2500, 4000):
        for w in (1, 3, 5):
            agg.level_seqs = {}
            run_orbit(w, v, agg=agg)

    spikes = [s for s in agg.spike_list]          # (J, rho, k, v, w, depth)
    cls_bad = [s for s in spikes
               if s[2] is None or (s[2] - 10) % 16 != 0
               or s[0] != 5 + v2(3 * ((s[2] - 10) // 16) + 2)]
    ident_bad = [s for s in spikes if s[2] is None or 6 * s[2] + 4 < (1 << s[0])]
    kb_bad = [s for s in spikes if 20 * s[2] > 893 * s[1]]
    # max j among run fires with rho >= 32 and the 3log2 bound
    maxj32 = (0, None)
    log_bad = []
    # rebuild (rho, j, k) stream: use agg.uni (rho -> (k, j)) over rhos>=32
    for rho, (k, j) in sorted(agg.uni.items()):
        if rho >= 32:
            if j > maxj32[0]:
                maxj32 = (j, (rho, k))
            if j > 3 * (rho - 1).bit_length() + 3:  # >= 3*log2(rho)+3 (crude up)
                log_bad.append((rho, k, j))
    # nested decrease stats
    nested = [s for s in spikes if s[5] >= 1]
    # seam/tail j distributions
    seam_j = {}
    tail_j = {}
    # quick rerun census (v<=2000,w=1 already in agg.role_max_j)
    print('=== S4 assembly ===')
    print('total fires:', agg.n_fires, 'roles:', agg.role_counts,
          'sum:', sum(agg.role_counts.values()))
    print('(a) role coverage: every fire in {run,seam,tail,zero}:',
          set(agg.role_counts) == {'run', 'seam', 'tail', 'zero'})
    print('(b) spikes (run, j>=5):', len(spikes),
          ' k=16s+10 class violations:', len(cls_bad),
          ' 2^J<=6k+4 violations:', len(ident_bad),
          ' k<=0.4465*rho violations:', len(kb_bad))
    print('    max J:', max(s[0] for s in spikes),
          ' at rho:', max(spikes, key=lambda s: s[0])[1])
    print('    max j among run fires rho>=32:', maxj32,
          ' viol of j<=3log2(rho)+3:', len(log_bad))
    print('    (c) nested spike fires (depth>=1):', len(nested))
    # margin arithmetic (exact integers)
    for J in (33, 40, 60):
        rl = -(((4 - (1 << J)) * 1000) // 2679)   # ceil((2^J-4)/2.679)
        r = 1
        while 6 * r ** 3 + 4 < (1 << J):
            r += 1
        print('    J=%d: linear-bound rho_min-J=%d (>=900: %s); '
              'cubic-bound rho_min-J=%d (>=900: %s)'
              % (J, rl - J, rl - J >= 900, r - J, r - J >= 900))
    print('nested-decrease violations (all run fires):',
          len(agg.viol_nested))
    print('min u by role:', {r: u for r, (u, _) in agg.role_min_u.items()})
    print('role max j:', {r: j for r, (j, _) in agg.role_max_j.items()})
    # dump extras for report
    extra = {
        'spike_class_bad': len(cls_bad), 'spike_identity_bad': len(ident_bad),
        'spike_kbound_bad': len(kb_bad),
        'maxj_rho32': list(maxj32), 'log_bad': len(log_bad),
        'nested_spikes': len(nested),
        'n_spikes': len(spikes),
        'max_spike': max(spikes, key=lambda s: s[0]),
        'min_u_by_role': {r: u for r, (u, _) in agg.role_min_u.items()},
        'role_max_j': {r: j for r, (j, _) in agg.role_max_j.items()},
        'uni_rho_count': len(agg.uni),
        'uni_viol': len(agg.uni_viol),
        'viol_counts': {k: len(getattr(agg, k)) for k in
                        ['viol_j_ge_rho', 'viol_k_bound', 'viol_j_bound',
                         'viol_nested', 'viol_c_role', 'viol_rho_lt4',
                         'viol_k_int', 'viol_j_formula']},
        'halts': len(agg.halts),
        'total_fires': agg.n_fires,
        'role_counts': agg.role_counts,
    }
    with open('blind2_s4.json', 'w') as f:
        json.dump(extra, f, indent=1, default=str)


if __name__ == '__main__':
    main()
