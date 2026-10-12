# Main-line independent checks of agent B's claimed complete proof (2026-10-12/13)

All checks run by the coordinator, independently of agent B's own drivers where possible.

1. **Invariant I(rho) re-run** (`python agentB_run15.py 20000`): 6372 run-chain events,
   rho <= 20000, **0 invariant failures**, max j = 14, k <= (p+4)/2. Matches the report.
   (The report's "50000-position run in flight" DIED with MemoryError — discounted;
   nothing in the assembly depends on rho > 20000 data.)
2. **Per-J abstract verifier sample**: j = 1..80 via agentB_run7.verify: 80/80 OK.
3. **Parity/tie-freeness linchpin** (by hand): at nested levels U = previous chain's
   u = 3*2^{rho'-j'}*U' + (6k+4)/2^{j'} = even + odd = ODD; top level U = 3w odd.
   Hence v2(3*2^rho*U) = rho exactly and v2(x) = j_rho < rho is tie-free. Sound.
4. **Cross-route reconciliation**: agent B's universal (p_i, j_i) = (4,1),(7,4),(11,2),
   (13,1),(16,3),... IDENTICAL to agent G's independently mined R-family fire table
   ((t,i,k) = (2,4,1),(4,7,4),(8,11,2),(10,13,1),(12,16,3) with i = position, k = j).
   Two independent engines, same object.
5. **ell formula** (Theorem 4): with k_b(v) = universal k at the last position p <= v-1:
   ell(v) = 2*k_b(v) + e(v), e in [0,12], **0 violations for v = 3..5000** (exact table).
6. **Spike conservation**: to p = 4*10^5: dK = 16 exactly between consecutive spikes,
   dp >= 37, sup k/p = 0.4464, max j seen = 20 (within table). Matches.
7. **Lemma L0 (queue-determinism)** (by hand): a top-map step reads only the front 3
   entries; successors are determined by them; pushed runs depend only on (u, j).
   Prefix universality follows. Sound.

Pending: the dedicated adversary (extreme-w universality, nested depth, j > 1200 table
extension, mod-3 superset, margins arithmetic, endgame domination, crashed-run impact,
ell edge) + the G'/F'/C' cross-check routes.
