# Adversary (Claude subagent) — PROOF_EGX — verdict: 2. with fixable gaps
Probes: scratchpad/rev_adv/probes. EGX holds (essentially an identity: (3n+3) = 2^v U - 3 is a fire state with lambda_u = U); U and L follow with no circularity.
1. [fixable] C2-log false at t=0 (crossing on the fire's own type-a return, eps=3 > 2J_W-1 for J_W=1); 21,730 of 40,527 type-c crossings to n=2e5. Fix eps <= max(3,2J_W-1); tight after fix. L and §7 unaffected.
2. [fixable] I-4 transfer to non-fire J asserted, not shown: EL B/A1/A2, RESCUE (AA), TIE2 §2 are written with real Theta=3s+5 and real valuations. Fix (a) dictionary lemma: symbolic mass (Sum alpha=2^J, Sum beta=3d-3), Theta_t -> 2^J lambda_u+3d_t+1, lambda_u -> beta_u; with h>=1 alpha-components have v2>=n so NT tests/valuations agree; or (b) PROOF_SPECTRUM §3: every J<K'-4 is an actual fire parameter.
3. [fixable] I-3 lists (C1) but the audit needs (C2) at J-1; "X(v-1) reached" needs s<=i^2 argument.
4. [wording] r <= J-2 fails at J=1: write max(0,J-2); confirmed on 60,575 epochs.
5. [wording] indexing off by one (endgame chain t vs exit chain t+1); for non-fire J replace Lemma 2.2-2.3 appeals for S(J) by "by definition".
6. [wording] Theorem L persistence needs an analytic line; C5 docstring mismatch; 7 vs 7.2 harmless.
7. [wording] mention the actual r=6 epoch of work_g2_obstruction (so the endgame of E(.,p3) has 6 chains); EG-LEN V0<=K'.
Verified: verify_egx reproduced; N=300000 0 mismatches (200,731 chains, exit counts {0:113,517;1:172,233;2:14,249}); integer top map vs sym_exit prediction 3<=v<=12000 (w=1,3) and v<=1500 (w=1,5), 26,992 runs, 0 mismatches; walk n<=2e5: sigma=rho-Gamma, min h=1, r<=max(0,J-2).

## Targeted re-review of the patched note: 1. closed in all states
All seven findings closed; Lemma TR sound (Theta_t = 2^J lambda_u + 3d_t + 1 consistent; symbolic mass replaces real mass; b/c copy identity algebraic; valuations under h_t >= 1); reached-crossing argument works; data label 15,118/4,744/210 recomputed exactly. One slip: f(10) = 204.8 - 67.2 = 137.6 (not 409.6) — fixed.
