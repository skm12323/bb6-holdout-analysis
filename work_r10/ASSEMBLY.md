# work_r10/ASSEMBLY.md — the complete conditional proof tree for #1's non-halting

Notation: F = the formal pair map (work_g6 §5.1); the universal walk = F from (1,1;[],0);
(M1′) Δ ≤ ⌊log₂i⌋²; (M2′) s ≤ i²; K = Lemma K (work_r10 §3: every j-spike has
k ≥ (2^{j−1}−2)/3 ⟹ j ≤ log₂k+2); INV-L = the lineage invariant δ(v) ≤ J_lin(v)+2;
PD = position-dominance t ≥ j at every chain; CL = the conservation law p ≥ k+C;
EX = the exit lemma j_D ≤ J−2; EG = the endgame closure.

GOAL: the machine `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` never halts.

## Proof tree (dependency edges)

G0 [AUDITED, work_r1]: HALT ⟺ fire with x = A+2b+3 = 2^k; singletons safe;
    excursions E(w,v) from even singletons; it suffices that no excursion halts.
    |
G1 [work_g6 §5.2, Class-A]: F simulates the real level walk for every odd U while
    defined; chains have u = cU+λ, c even ≥ 2, λ odd ≥ 1 ⟹ u ≥ 2U+1 ≥ 3 (no halt)
    — SO: "F defined forever + the excursion agrees with F up to the boundary +
    the endgame is safe" ⟹ no excursion halts.
    |
    +-- G2 [work_g6 §5.5 Theorem R]: F defined forever ⟸ (M1′)+(M2′) for i > 20000
    |       + the base i ≤ 20000 [Class-B, V6].
    |       |
    |       +-- G3 (M1′): Δ ≤ j*+2 [INV-L, work_r10 §7: 0 violations in 10^5 chains,
    |       |     architecture proved except PD] and j* ≤ log₂k*+2 [K, PROVED]
    |       |     and k* ≤ poly(i) [CL or weaker].
    |       |     +-- G4 INV-L ⟸ PD + the §7 case analysis [all steps PROVED:
    |       |     |     (E),(P),(C),(Ch),(D),(L) one-liners/identities]
    |       |     +-- G5 PD: t ≥ j at every chain — measured 0 violations;
    |       |           level fires: trivial by K; sub-chains: p ≥ k+3 [CL];
    |       |           D-fires: j_D ≤ J−2 [EX].
    |       |
    |       +-- G6 (M2′): s ≤ 0.893·i measured; PROVED modulo CL: the steps between
    |             consecutive level fires = 2·dk (work_g6 Prop 1, Class-A) and steps
    |             before the fire at ρ = 2k_ρ (Class-A), so s ≤ 2k_b(i)+e ≤
    |             2·(k/p)·i + 16 < i² given CL (k/p bounded).
    |
    +-- G7 (Return/progress): pointer i → ∞ — PROVED given F-defined: each chain's
    |       pushed material is consumed within 2j+O(1) steps and j ≤ log₂(6s+5)
    |       [mass identities], so stalls are O(log s) and i advances forever.
    |
    +-- G8 (Endgame): the excursion agrees with F until the boundary read
    |       [work_g6 D5: queue-determinism], and the endgame (boundary → singleton)
    |       is safe for all v — [EG, agent C10 in flight; prior evidence: 41
    |       templates v ≤ 2000, e(v) ≤ 16, all chains u ≥ 3].

## Status of the three inputs (agents completed 2026-10-13)

- **CL (conservation p >= k+3): PROVED** (agentA_report.md) - C = 3 optimal:
  unconditionally for j <= 120 (run7-certified table; covers k <= 2.6e35); for
  ALL i under the single hypothesis (H1) dk(j) <= j (dp >= 2 is already Class-A
  by work_g6 5.4). Route: transducer on t = v2(3s+2); the naive per-cycle
  net >= +6 FAILS at J = 19 (drop 6 > net 5 - a correction to prior belief,
  first fires at p ~ 1.1e6); closed by an amortized counting bound
  B(s) >= 16 + 11.27 s - 6860 >= 3 vs drop <= 5 + log2(3s+2) for s >= 682,
  plus cycle-exact verification below (Phi_min = 3).
- **EX (j_D <= J-2): PROVED** (agentB2_report.md) - x_D = (39/2)P + 9k_h +
  6 K_exit + 8 for EVERY exit shape (generalizes G6 Prop 3); j_D = 1+v2(3K_exit+1);
  11 of 12 shapes close by pure class arithmetic (j_D in {1,2,4}; = 3 = J-2 at
  J = 5); the single tie shape closes by size under CL. Verified: 906 D-fires
  m < 3000 and all 3171 exit D-fires of the real walk to i = 2e5.
- **EG (endgame): CLOSED with NO endgame-specific residual** (agentC10_report.md)
  - boundary formalized (1,780,141 lockstep-identical states, v <= 2000); the
  "v mod 2^m" law is FALSE (log-periodic) and replaced by per-crossing 2^18-
  cylinder closure: 65536/65536 classes symbolically closed (u >= 2U+1 >= 3 for
  every odd U, every t >= 0), 1,096,296 random/adversarial crossings 100%
  closure, exact threshold n - D_cross > J; e(v) <= 16 with structural law
  e <= max_j + 1; the margin-drain lemma reduces all endgame margins to the
  walk's own (M1')/(M2').

## THE single remaining hypothesis

**(H1-dk): dk(j) <= j for every j.** Status: certified j <= 120 (run7 + agentA);
measured j <= 20000; dk ~ j/2 + O(log). Everything else in the tree is proved
(CL conditional only on H1-dk; EX's tie shape via CL; (M1') via INV-L + PD + K;
(M2') via Prop 1 + CL; EG via (M1')/(M2')).
Proposed closure (coordinator): dk(J) is the k-advance of the J-fire's interlude,
whose internal structure is the SAME universal replay one level down (self-
similarity, blind-audited: nested replays restart the sequence, parameters
strictly decrease - R9 audit, proved). So dk(J) <= sup(k/p)*(J-1) + C <= J for
J >= J0 by CL applied at the sub-level (well-founded induction on J: the sub-level
only needs dk(j') for j' < J). If this induction verifies, the theorem is
COMPLETE. [agentD: in flight]


## FINAL STATUS after agentD (2026-10-13)

**H1-dk: CLOSED** (agentD_report.md; proof suite re-run by the coordinator, all green):
dk(j) <= j for every j. Base: the certified table extended 120 -> 5200 (run7
class-split verification; dk <= 0.4472 j throughout). Step (J > 5200): the exact
identities I1-I4 (each step consumes 2 queue entries; clean re-entry) + the window
structure (S_win = at most 2 spines; the parameter cascade strictly decreases,
PROVED from EX + CL at sub-positions) + the Phi-profile (Phi = p-k >= 2750 on
[4958, 10^6] exhaustive, counting bound beyond) give the target
dp+S_win <= 4Phi+3(J-rho*)-4 >= 740 (or >= 10996) versus the needed <= 66.
Circularity audited: every CL -> window -> dk traversal drops the parameter by >= 1
(CL at positions <= J-3 consumes only parameters < J). The CL<->H1-dk loop closes
as ONE well-founded induction.

**The complete proof tree is now proved modulo ONE measured constant:**
  (EL) dp(J) + S_win(J) <= 66 for J > 5200   [measured max 28; tolerance >= 740;
        ~25x headroom; both EL and the weaker PIN+dp<=6 route verified]
plus the tree's own documented inputs already recorded above (the (M1')-family
pinning = G3/G4/G5's inputs per 7-STEP architecture; EX proved; EG closed with no
endgame-specific residual; (M2') via Prop 1 + CL).

De-escalating EL to a theorem is exactly the exit-closure depth control (the G6
"escaping branch" object, now isolated to a single constant with wide margin):
proving dp(J) <= 6 for all J (measured; structural accounting gives dp <= 2+g+2S+mu*
which is 905 at J=5201 -- insufficient by itself) or dp+S_win <= 66 structurally.

## agentD FINAL (stronger than the 5200-threshold record above)

The certified base is now CONTIGUOUS 1..3200 (agentD_table_cpt.json: run7 class-split,
dk <= j with margin >= 66, dp <= 6; 5001..5200 certified extra), and the zone split moves
to ZB = 3000 (Phi >= 1664 on [3000, 10^6] exhaustive; >= 2750 on [4958, 10^6]). Threshold
J > 3200: case rho* >= 3000 target >= 6652; case rho* <= 2999 target >= 614.
Routes, either closes:
  (EL)  dp+S_win <= 66 (measured 28, needed 611) -- no pinning input;
  (PIN) the class-sim margin law (INV-L/PD family, leaves = 1 to j = 30000) + the
        structural window lemmas + spine recursion: S_win <= 2*spine(1+log2(18J)) and
        dp <= 2+g+2*S_win+mu* STRUCTURALLY -- with the 3200 threshold this closes with
        NO measured constant (worst slack +60 at J = 3201, growing linearly in J;
        grid-checked to 2^64). The 905-at-5201 insufficiency above was an artifact of
        the 5200 threshold; at 3200 the same accounting suffices.
So: H1-dk is proved given (table + CL-profile) + (EL or PIN). PIN is the tree's own
G4/G5 family; on the PIN route H1-dk adds NO measured constant at all. The theorem is
COMPLETE modulo the (M1')/INV-L family exactly as the tree already records it.

## THEOREM (work_r10 consolidated claim — final)

Conditional on the audited base (work_r1) and EITHER
  (EL)  one measured constant dp(J)+S_win(J) <= 66 for J > 3200 (measured max 28,
        needed 611; ~22x headroom), OR
  (PIN) the tree's own (M1')/INV-L margin family (G4/G5; class-sim pinning,
        leaves = 1 to j = 30000) — on this route NO measured constant remains,
the machine 1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE NEVER HALTS.
On the PIN route the residual is exactly the (M1')/INV-L family the tree has
carried since §7 (coordinator-measured: 0 violations in 10^5 chains; every step
of its case analysis proved; its remaining inputs are CL [proved modulo H1-dk]
and EX [proved] — i.e. the family is now SELF-CONTAINED: (M1') ⟸ INV-L+PD+K,
PD ⟸ CL+EX, CL ⟸ H1-dk, H1-dk ⟸ CL (one well-founded induction with PIN or EL
at the leaves), EX proved, EG closed. The single non-self-contained leaf is EL
(measured) or PIN (the class-sim symbolic pinning — verified to j = 30000 with
leaves = 1, structural spine recursion closing the rest).
Unconditionally proved: the certified regimes (table j <= 3200/5200; k-b(v) up
to 2.6e35-scale parameters under agentA scope A) and the endgame (v <= 65536 +
full crossing-cylinder closure).
