# Blind auditor 1 (Claude subagent) — PROOF_EGX — verdict: 2. with simple errors
Own code: scratchpad/rev_aud1 (aud1.py, test_*.py). Did not read verify_egx.py.
1. Lemma C2-log false for J_W=1 at t=0 (fire chain, eps=3 > 2J_W-1=1); 43,462 instances to n=4e5, all (J_W,t,eps)=(1,0,3). Fix: eps(i) <= max(3, 2J_W-1) < 2log2(3i^2+4)-1 (i>=2). t>=1: bound holds (max eps-(2J_W-1) = -4, 9,133 crossings); eps = 3+a_t+Gamma_t exact at all 81,053 type-c crossings. Theorem L unaffected.
2. EGX §2 proof: no gap (start state, return lemma, induction step, S2, item 3, d_t = s_t+1).
3. Theorem L correct; tie condition impossible for J >= 327; exact checks J=2^10..2^199 and 2^256..2^4096, 20,000 random J.
4. Adversarial perturbed starts (~29,000, v<=3000): identity structural; 5 unsafe endgames all coincide with S-ties at the same chain.
Computed: EGX pair-for-pair 3<=v<=400,000 (267,637 chains, a/b/c 133,819/127,479/6,339, exit counts {0:151,357;1:229,645;2:18,996}); D5 v<=2500; integer top map v<=400 for 9 w (incl. 2^127+1, 3^60); Lemma 6.1 on real walk n<=2e5 (60,575 epochs).
