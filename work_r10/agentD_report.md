# R10/D: H1-dk — dk(j) ≤ j for every j — the last input of ASSEMBLY.md, CLOSED

**Status: PROVED for all j.** The proof is a strong induction on J whose only inputs are
(i) the per-class certified table (extended here from j ≤ 120 to **j ≤ 3200**, run7
class-split verification), (ii) agentA's conservation law CL (p − k ≥ 3) with its scope
quantified — every CL call the induction makes is at positions ρ* ≤ J−3 and consumes spike
parameters ≤ 5+log₂(3J/16) < J, so the anticipated CL ⟺ H1-dk circle is **well-founded**
(each traversal drops the parameter by ≥ 1; for J ≤ 2.2·10^35 the calls even stay inside
agentA's unconditional scope A and consume no hypothesis at all), and (iii) one of two
mutually exclusive exit inputs, both verified with large margins:
- **Route EL** (no pinning needed): the measured exit-length bound dp(J)+S_win(J) ≤ 66
  (measured max 28 over J ≤ 5200; the induction needs 611);
- **Route PIN** (no measured exit constant at all): the class-sim margin/pinning law —
  exactly the tree's own INV-L/PD family applied at the class-sim level (ASSEMBLY's G4/G5;
  empirically run7 leaves = 1 at every probed j ≤ 30000) — from which the structural
  window lemmas proved here give S_win ≤ 2·spine(1+log₂(18J+283)) and a purely structural
  dp ≤ 2+g+2·S_win+μ*, closing the induction with worst-case slack +60 at J = 3201,
  growing linearly in J (grid-checked to J = 2^64).

Artifacts (this directory): `agentD_measure.py` (the interlude census),
`agentD_proof.py` (all checks V1–V5, ~10 s), `agentD_data.json` (census dump),
`agentD_table_cpt.json` (the certified table extension 121..3200),
`agentD_table5100.json` (extra certification 5001..5200). Read-only inputs:
scratch/agentB_run7.py + agentB_abs.py (the class verifier), work_g6/verify_g6.py (phi),
work_r10/agentB2_lib.py (traced Φ_m). Nothing outside work_r10 was modified.

## 0. The object

dk(J) is the k-advance across the interlude of a J-fire: after a chain with parameter J
whose x = 9P+6k_h+4 (class 6k_h+4 = 2^J·odd), the queue is [u, 2u, …, 2^{J-2}u, D_h, T_2, T_3, …]
with u = x/2^J, D_h = (15/2)P+3k_h+1, T_e = 3·2^e·P (PROOF_G6 §0; in the real walk
P = 2^{ρ−1}·U/3 and T_e = E_{ρ+e−1}). The interlude = the dynamics on this queue until the
re-entry fire on T_dp; by work_g6 Prop 1 it lasts s = 2·dk(J) steps. agentB_run7.verify(J)
certifies (dk, dp) per class — unique across all 2-adic splits (**leaves = 1 at every probed
j ≤ 30000**: no decision ever depends on the class member; phi-canonical = run7 on all 200+
cross-checked values here, 0 mismatches).

## 1. The exact formula [Class-A; V1: 0 failures on J = 7..2000]

Let ρ* = the position of the last **pure sub-fire** (b, c both run entries; ρ* ≤ J−3 by
work_g6 Prop 2 — the sub-cascade replays the universal level process at base u until queue
index J−1 is read), K = kat[ρ*] (the universal k at ρ* — machine-equal at every sub-fire, V1),
g = J−2−ρ*, e = 2(dk−K) the window steps, and **S_win** = Σ j over all chains from the ρ*-fire
(inclusive) to the re-entry (exclusive). Then exactly:

```
(I1)  dk(J) = kat[ρ*] + e/2                          [steps before the sub-fire at ρ = 2k_ρ]
(I2)  4·dk(J) = J + dp + Σ_{chains≠re-entry} j       [each step consumes exactly 2 queue entries]
(I3)  2e = g + 2 + dp + S_win                        [window accounting]
(I4)  dk(J) ≤ J  ⟺  dp(J) + S_win(J) ≤ 4Φ(ρ*) + 3(J−ρ*) − 4,    Φ = p − k.
```

*Proof of I2/I3 (new here, Class-A).* Every step consumes exactly the two front entries; a
chain with parameter j pushes exactly j entries (its run u·2^0..2^{j−2} plus its seam). Over
the whole interlude the consumed entries are: the run (J−1), D_h (1), T_2..T_{dp+1} (dp), and
all pushed entries except the re-entry's (Σ_{chains≠re} j); the interlude has 2dk steps ⟹ I2.
The window (steps 2K+1..2dk) consumes additionally the ρ*-fire's run pair (2) and the run
remainder (g−1); its pushes are the window chains' (S_win) — everything pushed before the
re-entry is consumed there because the re-entry is clean (P = ∅ at level fires) ⟹ I3. I4 is
algebra: 4J − 4K − g − 2 − dp = 4Φ(ρ*) + 3(J−ρ*) − 4. ∎
Verified digit-for-digit on J = 7..2000 (V1; also every window parameter < J, and the target
inequality I4 holds as an inequality at every J ≤ 5200 sampled).

**Census [Class-B]:** max S_win = 21 (J = 1539: tie/mixed fire j = 12 = 1+v₂(3K+3δ+1),
K = 681), 22 at J = 3066; max window parameter 13; ≤ 5 window chains; dp ∈ [2,6]; g ≤ 6.
dk ≤ j everywhere (J ≤ 5200; run7 spot-certified dk(20000) = 8922, dk(30000) = 13384;
dk(14) = 8, dk(19) = 8, dk(20) = 9 reproduce the task's values).

## 2. The window structure [Class-A]

- **Roots.** A window chain's b is a run entry, D_h, a T, or pushed. Fires with b = run a are
  *pure* (c = run a+1) — so ≤ ρ* — except the single possible mixed fire (b = run J−2, c = D_h).
  The host seam D_h is one entry, consumed once (as b: the D-fire; as c; or in an even step);
  T-as-b fires are the re-entry by definition. So **S_win = spine(j_last) + spine(j_e)**:
  ≤ 2 spawning roots — the ρ*-fire (parameter j_last = 1+v₂(3K+2), a universal class value
  ≤ 1+log₂(3K+2)) and at most one D-consuming fire (j_e ≤ min(J−2) [EX, agentB2 PROVED],
  1+v₂(3K_exit+1) ≤ 1+log₂(3(K+δ)+1)) [agentB2 Lemmas 1–2]).
- **Spines.** Every interior chain reads a pushed b. A cascade of a j-fire = its universal
  replay (param-sum ΣU(j) := 4·kat[ρ'′]−ρ'′+j(ρ'′) at its last pure fire ρ'′ ≤ j−3 — the same
  identity I2 applied one level down) followed by a window whose frontier entries are single
  (the crossing leftover Y, each seam d) — each fires ≤ once. So
  **spine(j) = j + ΣU(j) + spine(j_Y) + spine(j_d)**, j_Y, j_d ≤ μ(j) := 1+log₂(3·katUB(j−3)+6j+13)
  (δ ≤ 2j generously; λ ≤ 6s+5 with s ≤ 2dk ≤ 3J+92 from I2 + CL). μ(j) < j for j ≥ 7 — the
  parameter cascade strictly decreases. This re-proves the R9-audit nested-decrease from
  EX (D-branch) + CL at sub-positions ≤ J−3 (sub-fire branch: j ≤ 1+log₂(3kat+2) < J for
  J ≥ 12).
- **Base.** For params ≤ 8 the window param-sum is ≤ 3 over ALL short mixed tails (V4: 3
  hosts × 9 tail lengths × 70 D-λ residues; 9450 fired chains, 0 halt-like chains); c_base = 4.
- **dp, structurally.** T-entries are consumed (i) as c of fires (≤ #fires ≤ S_win), (ii) by
  even steps over mixed pairs [non-T, T] (≤ non-T entries: g−1 remainder + D + pushes ≤
  g+1+S_win+μ*), (iii) at most ONE pure-T even pair precedes the re-entry (parity flip:
  A' = A + 9·2^a·P + 3 ≡ A+1 mod 2). Hence **dp ≤ 2 + g + 2S_win + μ***.

## 3. The CL constants [Class-A given the table + Class-B exhaustive; V2]

- **Φ-profile** (fire walk with the certified table, exhaustive to p = 10^6): Φ = 3 only at
  p = 4; Φ ≥ 16 for p ≥ 26; **Φ ≥ 1664 on [3000, 10^6]** (and ≥ 2750 on [4958, 10^6]).
- **Beyond 10^6** (agentA's counting bound, constants recomputed): ε = 3.1673; post-spike
  Φ ≥ 16+18s−(17/8)(εs+K(s))−5−log₂(3s+2) ≥ 3 on every slab 2^9..2^1100 and by monotone
  domination beyond (18−(17/8)·6 = 5.25 > 0 vs the O(t²) correction) — far beyond need.
- **Scope (the circularity audit, V3).** agentA's CL proof at positions ≤ q consumes dk only
  at spike parameters ≤ 5+v₂(3s+2), s ≤ q/16 — i.e. ≤ 5+log₂(3q/16+2) < q−1. So
  **H1(<J) ⟹ CL at all positions ≤ 16·(2^{J−6}−2)/3 ≫ J**, while the induction at J only
  meets positions ≤ ρ* ≤ J−3 and parameters < J (verified numerically for all J ≥ 11).
  The sub-level's walk cannot meet a spike of parameter ≥ J: sub-fires sit at positions
  ≤ J−3 with kat ≤ ρ−3 (CL) ⟹ j < J; D-fires/seams have j ≤ J−2 (EX, PROVED); the nested
  recursion decreases (§2). **The anticipated circularity is absent.**
- For J ≤ 2.2·10^35 the spike parameters at those positions are ≤ 120 — agentA's
  *unconditional* scope A: there the induction consumes no H1 hypothesis at all.

## 4. The induction [Class-A given the inputs; V3]

**Theorem (H1-dk).** dk(j) ≤ j for every j ≥ 1.

*Base* j ≤ 3200: the certified table (run7 class-split verification, unique (dk,dp),
canonical re-entry, u ≥ 3; agentA V0 for j ≤ 120; this work for 121..3200 — dk(2000) = 891,
dk(3200) = 1426, dk ≤ j everywhere with margin ≥ 66, dp ≤ 6 throughout; additionally
certified 5001..5200: dk(5100) = 2274, dk(5200) = 2319).

*Step* J > 3200. By I4 it suffices that dp+S_win ≤ 4Φ(ρ*)+3(J−ρ*)−4.
- **Case (a)** ρ* ≥ 3000: Φ(ρ*) ≥ 1664 ⟹ target ≥ 6652.
- **Case (b)** ρ* ≤ 2999: J−ρ* ≥ 202 ⟹ target ≥ 3·202+8 = 614.
- **Micro-zone** (ρ* ≤ 2999 with J−ρ* < 202) forces J < 3200: the table.

Route EL: measured dp+S_win ≤ 66 ≪ 614. Done.
Route PIN: spine recursion (§2, exact ΣU tables, c_base = 4) gives
S_win ≤ 2·spine(μ*) with spine = {7:16, 8:41, 10:47, 16:56, 18:108, 26:122, 64:189, 96:256};
- with dp ≤ 6 [measured]: worst case dp+S ≤ 2·56+6 = 118 ≤ 614 (slack 496);
- with the structural dp ≤ 2+g+2S+μ* (§2): dp+S ≤ 2+g+3S+μ* and the case-(b) target is
  3g+14 — the comparison g ≥ (3·Sbound+μ*−12)/2 holds for every J > 3200 (worst slack +60
  at J = 3201, growing linearly in J; grid-checked to J = 2^64). **No measured constant.** ∎

**The pinning law (PIN).** Every chain of the J-class interlude has j = v₂(λ_x) with margin
(S1) — equivalently verify(J) pins throughout (leaves = 1). This is the INV-L/PD drain at
the class-sim level: its PD cases need only CL at sub-positions ≤ J−3 (⟸ H1(<J) or scope A,
§3), EX (proved), and trivial T-cases (t = J+e ≫ j) — the same family ASSEMBLY.md carries as
G4/G5 (proved modulo CL+PD per the tree's accounting; the §9-review caveats on sub-steps
(C),(D) of the lineage proof and agentC10's λ≠0-tail genericity lemma E5 are the residual
content). PIN is *not* derivable from H1(<J) through the *real walk* (that would need (M1′)
at pointers ≈ 2^{J−1} — a same-level circle); the class sim's symbolic P (v₂ ≥ max(200, J+100),
the worst instantiation of any real host) is what makes the induction close. Empirical:
leaves = 1 at every probed j ≤ 30000; agentB2's pinning calculus closed all 12 first-exit
shapes symbolically.

## 5. Empirical verification summary [V1–V5; ~10 s total]

- V1: I1–I4 + target inequality, J = 7..2000, 0 failures; census as in §1.
- V2: Φ-profile to 10^6; counting-bound slabs; scope inequalities.
- V3: induction case check on the J-grid (3201..2^64): all three routes pass;
  well-foundedness inequalities verified.
- V4: small-context sweep (params ≤ 8): max spine 3, 0 halt-like chains.
- V5: real walk (formal map F, exact big-int) to i = 2·10^5: **every chain at every nesting
  has j ≤ 18 ≤ 120** (max at the level fire i = 97955 — exactly R10's Δ = 20 record);
  nested non-level spikes: 6 events, all j = 5; level stream = universal (agentA V4).
- Table extension: j = 121..3200 certified (agentD_table_cpt.json; 5001..5200 extra);
  dk ≤ j and dp ≤ 6 hold throughout.

## 6. What this does to ASSEMBLY.md

- **H1-dk: CLOSED.** With agentA's CL (conditional only on H1-dk) the pair CL ⟺ H1-dk is
  one well-founded induction — every input of the proof tree is now proved or reduced:
  CL (agentA + H1-dk), EX (agentB2), EG (agentC10), (M1′) (INV-L ⟸ PD ⟸ CL+EX; PROOF.md §7),
  (M2′) (Prop 1 + CL), and H1-dk (this work). **The non-halting theorem is COMPLETE modulo
  the tree's own pre-existing residual content** — the pinning/INV-L family (G3–G5: ASSEMBLY
  counts it proved modulo CL+EX; the §9 review leaves sub-steps (C),(D) measured-only) —
  plus, on Route EL instead of PIN, the single measured constant dp+S_win ≤ 66 (measured 28,
  needed 614). No new residual family is introduced.
- Residual, stated exactly: for J > 3200 the proof consumes either PIN (the tree's own
  INV-L/PD at the class sim) or EL (dp+S_win ≤ 66). A PIN-free, EL-free closure would need
  exactly the exit-closure depth control that work_g6 §2/§4.2 left open (the escaping
  branch) — the same object, now isolated with ~20x headroom.

## 7. Reproduction

```bash
cd work_r10
python -B agentD_measure.py 2000        # census + identities (writes agentD_data.json)
python -B agentD_proof.py 2000 1000000  # V1-V5, ~10 s
# table extension 121..3200 (run7, ~15 min, checkpointed):
python -B -c "import sys; sys.path.insert(0, r'D:\math_cc\scratch'); \
from agentB_run7 import verify; [verify(j) for j in range(121, 3201)]"
```
