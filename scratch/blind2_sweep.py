"""Blind Auditor 2 — S2/S3/S4 main sweep.

S2: v = 1..2000 (w=1) plus v in {2500,4000} x w in {1,3}: classify every fire
    by b's role (run / seam D / tail T / zero), verify u >= 3 for all, verify
    every excursion reaches a singleton (no halt).
S3: run-chain (rho, j, k) at ALL levels: universal k-sequence, j < rho
    (rho >= 32 and everywhere), k <= 0.4465*rho, j <= 3 log2 rho + 3, nested
    parameter decrease, c-role structure, positions >= 4.
S4: role coverage; spike census (max J, 2^J <= 6k+4, k bound -> margin);
    derived dk/dp table vs the one claimed in agentB_closedform.md.

Writes scratch/blind2_sweep.json (aggregates).
"""
import json
import sys
import time

sys.path.insert(0, '.')
from blind2_lib import Agg, run_orbit, v2

KB = 0.4465


def main():
    t0 = time.time()
    agg = Agg()
    fins = {}
    ells = {}
    nonrun_v = {}
    halts = []
    # --- main sweep v=1..2000, w=1 ---
    for v in range(1, 2001):
        agg.level_seqs = {}
        ex, fires, fin, finA, ell = run_orbit(1, v, agg=agg)
        fins[v] = fin
        ells[v] = ell
        if fin != 'singleton':
            halts.append((1, v, fin))
        # note v's with non-run fires (from this run's role counts delta)
    # --- extras ---
    extras = []
    for v in (2500, 4000):
        for w in (1, 3):
            agg.level_seqs = {}
            ex, fires, fin, finA, ell = run_orbit(w, v, agg=agg)
            extras.append((w, v, fin, ell))
            if fin != 'singleton':
                halts.append((w, v, fin))
    # separate role counts for the extras runs: rerun quickly with fresh agg
    agg_x = Agg()
    for v in (2500, 4000):
        for w in (1, 3):
            agg_x.level_seqs = {}
            run_orbit(w, v, agg=agg_x)

    # ---- universal sequence from host-level fires ----
    host = agg.host_seq  # ordered (rho,k,j) of depth-0 fires, all runs concat
    # rebuild ordered host sequence for the biggest single run (v=4000, w=1)
    agg_h = Agg()
    run_orbit(1, 4000, agg=agg_h)
    host_seq = agg_h.host_seq
    # doc claims (agentB_closedform.md section 3)
    doc_p = [4, 7, 11, 13, 16, 21, 23, 26, 31, 34, 39, 41, 44, 48, 50, 53, 58,
             60, 63, 67, 70]
    doc_k = [1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 16, 17, 18, 20, 21, 22, 24, 25,
             26, 29, 30]
    doc_j = [1, 4, 2, 1, 3, 2, 1, 6, 1, 1, 3, 2, 1, 4, 2, 1, 3, 2, 1, 5, 3]
    my_p = [r[0] for r in host_seq[:21]]
    my_k = [r[1] for r in host_seq[:21]]
    my_j = [r[2] for r in host_seq[:21]]
    my_j_true = [1 + v2(3 * k + 2) for k in doc_k]
    # derived dk/dp tables (finite differences grouped by j)
    dks = {}
    dps = {}
    for i in range(len(host_seq) - 1):
        (p1, k1, j1), (p2, k2, j2) = host_seq[i], host_seq[i + 1]
        if k1 is None or k2 is None:
            continue
        if j1 in dks:
            if dks[j1] != k2 - k1 or dps[j1] != p2 - p1:
                dks.setdefault('BAD', []).append((i, host_seq[i], host_seq[i + 1]))
        else:
            dks[j1] = k2 - k1
            dps[j1] = p2 - p1
    doc_dk = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 4, 9: 4, 10: 5,
              11: 5, 12: 6, 13: 6, 14: 8, 15: 7, 16: 7, 17: 8, 18: 8, 19: 8,
              20: 9}
    doc_dp = {1: 3, 2: 2, 3: 5, 4: 4, 5: 4, 6: 5, 7: 4, 8: 6, 9: 2, 10: 5,
              11: 4, 12: 6, 13: 4, 14: 5, 15: 5, 16: 4, 17: 6, 18: 3, 19: 2,
              20: 5}
    dk_match = {j: (dks.get(j), doc_dk.get(j)) for j in sorted(doc_dk)
                if j in dks and dks[j] != doc_dk[j]}
    dp_match = {j: (dps.get(j), doc_dp.get(j)) for j in sorted(doc_dp)
                if j in dps and dps[j] != doc_dp[j]}
    dks_j_present = sorted(j for j in dks if isinstance(j, int))

    # ---- per-level replay = prefix of universal sequence ----
    useq = [(r[0], r[1]) for r in host_seq]
    lvl_prefix_bad = []
    lvl_prefix_ok = 0
    lvl_lens = []
    a2 = Agg()
    run_orbit(1, 4000, agg=a2)
    for lvl, seq in a2.level_seqs.items():
        if not seq:
            continue
        lvl_lens.append(len(seq))
        for i, (rho, k, j) in enumerate(seq):
            if i < len(useq) and (rho, k) != useq[i]:
                lvl_prefix_bad.append((lvl, i, (rho, k), useq[i]))
                break
        else:
            lvl_prefix_ok += 1

    # ---- spike census (S4b) ----
    spikes = agg.spike_list + agg_x.spike_list
    max_spike = max(spikes, key=lambda s: s[0]) if spikes else None
    # margin identity 2^J <= 6k+4 and k bound
    margin_bad = [s for s in spikes if s[2] is None or 6 * s[2] + 4 < (1 << s[0])]
    kbound_bad = [s for s in spikes if s[2] is not None and 20 * s[2] > 893 * s[1]]
    # margin arithmetic: k <= 0.4465 rho  =>  rho >= (2^J-4)/2.679
    #   => rho - J >= (2^J-4)*1000/2679 - J
    def rho_min_linear(J):
        return -((((4 - (1 << J)) * 1000) // 2679))
    def rho_min_cubic(J):
        r = 1
        while 6 * r * r * r + 4 < (1 << J):
            r += 1
        return r
    margin_tbl = {}
    for J in (32, 40, 50, 60):
        rl = rho_min_linear(J)
        rc = rho_min_cubic(J)
        margin_tbl[J] = {'rho_min_linear_k_bound': rl, 'rho_min_cubic_k<=rho^3': rc,
                         'p_minus_J_linear': rl - J, 'p_minus_J_cubic': rc - J,
                         'ge_900_linear': rl - J >= 900, 'ge_900_cubic': rc - J >= 900}
    # empirical p - J for spikes
    pJ = sorted(set((s[1] - s[0], s[0]) for s in spikes))
    min_pJ_per_J = {}
    for s in spikes:
        J = s[0]
        d = s[1] - s[0]
        if J not in min_pJ_per_J or d < min_pJ_per_J[J]:
            min_pJ_per_J[J] = d

    # ---- S2 role census over the main sweep ----
    out = {
        'sweep': {'v_range': [1, 2000], 'w': 1,
                  'fin_singletons': sum(1 for f in fins.values() if f == 'singleton'),
                  'fin_other': {str(v): f for v, f in fins.items() if f != 'singleton'},
                  'halts': halts,
                  'total_fires': agg.n_fires,
                  'role_counts': agg.role_counts,
                  'role_min_u': {r: [u, ctx] for r, (u, ctx) in agg.role_min_u.items()},
                  'role_max_j': {r: [j, ctx] for r, (j, ctx) in agg.role_max_j.items()},
                  'min_u_all': [agg.min_u_all[0], agg.min_u_all[1]],
                  'ell_1_20': [ells[v] for v in range(1, 21)],
                  'ell_2000': ells[2000]},
        'extras': {'runs': extras,
                   'role_counts': agg_x.role_counts,
                   'role_min_u': {r: [u, ctx] for r, (u, ctx) in agg_x.role_min_u.items()},
                   'total_fires': agg_x.n_fires,
                   'min_u_all': [agg_x.min_u_all[0], agg_x.min_u_all[1]]},
        's3': {
            'universal_rho_count': len(agg.uni),
            'uni_violations': agg.uni_viol[:10], 'uni_violation_count': len(agg.uni_viol),
            'max_j': [agg.max_j[0], agg.max_j[1]],
            'max_j_over_rho': [agg.max_j_over_rho[0], agg.max_j_over_rho[1]],
            'max_k_over_rho': [agg.max_k_over_rho[0], agg.max_k_over_rho[1]],
            'viol_j_ge_rho': agg.viol_j_ge_rho[:10], 'n_j_ge_rho': len(agg.viol_j_ge_rho),
            'viol_k_bound': agg.viol_k_bound[:10], 'n_k_bound': len(agg.viol_k_bound),
            'viol_j_bound': agg.viol_j_bound[:10], 'n_j_bound': len(agg.viol_j_bound),
            'viol_nested': agg.viol_nested[:10], 'n_nested': len(agg.viol_nested),
            'viol_c_role': agg.viol_c_role[:10], 'n_c_role': len(agg.viol_c_role),
            'viol_rho_lt4': agg.viol_rho_lt4[:10], 'n_rho_lt4': len(agg.viol_rho_lt4),
            'viol_k_int': agg.viol_k_int[:10], 'n_k_int': len(agg.viol_k_int),
            'viol_j_formula': agg.viol_j_formula[:10], 'n_j_formula': len(agg.viol_j_formula),
            'host_seq_head': host_seq[:21],
            'host_seq_len': len(host_seq),
            'doc_p_match': my_p == doc_p, 'doc_k_match': my_k == doc_k,
            'doc_j_match': my_j == doc_j,
            'my_p': my_p, 'my_k': my_k, 'my_j': my_j,
            'doc_j_recomputed_from_doc_k': my_j_true,
            'doc_j_row_typos': [i for i in range(21) if doc_j[i] != my_j_true[i]],
            'dk_derived': {str(j): dks[j] for j in dks_j_present},
            'dp_derived': {str(j): dps[j] for j in dks_j_present},
            'dk_mismatch_vs_doc': dk_match, 'dp_mismatch_vs_doc': dp_match,
            'dk_BAD_transitions': dks.get('BAD', [])[:5],
            'level_prefix_ok': lvl_prefix_ok,
            'level_prefix_bad': lvl_prefix_bad[:5],
            'n_level_seq_nonempty': len(lvl_lens),
            'max_level_seq_len': max(lvl_lens) if lvl_lens else 0,
        },
        's4': {
            'role_counts': agg.role_counts,
            'n_spikes_run': len(spikes),
            'n_spikes_nonrun': len(agg.spike_nonrun) + len(agg_x.spike_nonrun),
            'spike_nonrun_sample': (agg.spike_nonrun + agg_x.spike_nonrun)[:10],
            'max_spike': list(max_spike) if max_spike else None,
            'spike_J_hist': {str(J): sum(1 for s in spikes if s[0] == J)
                             for J in sorted({s[0] for s in spikes})},
            'margin_identity_bad': len(margin_bad),
            'kbound_bad': len(kbound_bad),
            'margin_tbl': margin_tbl,
            'min_p_minus_J_per_J': {str(k): v for k, v in sorted(min_pJ_per_J.items())},
        },
    }
    with open('blind2_sweep.json', 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print('elapsed', round(time.time() - t0, 1), 's')
    print('fins non-singleton:', {v: f for v, f in fins.items() if f != 'singleton'})
    print('extras:', extras)
    print('role counts:', agg.role_counts)
    print('role min u:', {r: u for r, (u, _) in agg.role_min_u.items()})
    print('total fires:', agg.n_fires, ' extra fires:', agg_x.n_fires)
    print('universal rho count:', len(agg.uni), 'violations:', len(agg.uni_viol))
    print('max j:', agg.max_j, 'max j/rho:', agg.max_j_over_rho[0],
          'max k/rho:', agg.max_k_over_rho[0])
    for key in ['viol_j_ge_rho', 'viol_k_bound', 'viol_j_bound', 'viol_nested',
                'viol_c_role', 'viol_rho_lt4', 'viol_k_int', 'viol_j_formula']:
        print(key, len(getattr(agg, key)), getattr(agg, key)[:3])
    print('host seq head:', host_seq[:21])
    print('doc p match:', my_p == doc_p, 'k match:', my_k == doc_k,
          'j match:', my_j == doc_j, ' doc-j typos at idx:', 
          [i for i in range(21) if doc_j[i] != my_j_true[i]])
    print('dk derived:', {j: dks[j] for j in dks_j_present})
    print('dk mismatch vs doc:', dk_match)
    print('dp mismatch vs doc:', dp_match)
    print('level prefix ok:', lvl_prefix_ok, 'bad:', len(lvl_prefix_bad),
          'nonempty level seqs:', len(lvl_lens), 'max len:', max(lvl_lens) if lvl_lens else 0)
    print('max spike:', max_spike, 'J hist:', out['s4']['spike_J_hist'])
    print('margin identity bad:', len(margin_bad), 'kbound bad:', len(kbound_bad))
    print('margin table:', margin_tbl)
    print('min p-J per J:', min_pJ_per_J)


if __name__ == '__main__':
    main()
