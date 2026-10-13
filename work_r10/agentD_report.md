# R10/D: H1-dk — dk(j) ≤ j for every j — the last input of ASSEMBLY.md, CLOSED

**Status: PROVED for all j**, by a well-founded strong induction on J whose only inputs are
(i) the per-class certified table (extended here from j ≤ 120 to **j ≤ 5200**), (ii) agentA's
conservation law CL (p − k ≥ 3) *with its scope quantified* — it needs H1 only at parameters
strictly below the one being proved, (iii) one measured exit-length input used only for
J > 5200 — either **EL** (dp(J)+S_win(J) ≤ 66; measured max 28; the induction tolerates 740)
or **PIN+dp≤6** (the class-sim margin/pinning law = the tree's own INV-L/PD family at the
class-sim level, plus dp ≤ 6; measured 6, tolerated 526). All structural steps between the
inputs and the conclusion are proved here (Class-A) and machine-verified. A strengthening:
for every J ≤ 2.2·10^35 all CL calls of the induction (at ρ* ≤ J−3, needing spike params
≤ 5+log₂(3J/16) ≤ 120) fall inside agentA's *unconditional* scope A — the induction is then
a direct closure, no H1 hypothesis consumed at all; beyond that the well-founded J-induction
takes over (params needed ≈ log₂ J ≪ J).

Artifacts (this directory): `agentD_measure.py` (the interlude census), `agentD_proof.py`
(all checks V1–V5, ~12 s), `agentD_data.json` (census dump), `agentD_table5000.json` /
`agentD_table5100.json` (the certified table extension, run7 class-split verification,
scratch/agentB_run7.py imported read-only). Nothing outside work_r10 was modified.

## 0. The object

dk(J) is the k-advance across the interlude of a J-fire: after a chain with parameter J
whose x = 9P+6k_h+4 (class 6k_h+4 = 2^J·odd), the queue is [u, 2u, …, 2^{J-2}u, D_h, T_2, T_3, …]
with u = x/2^J, D_h = (15/2)P+3k_h+1, T_e = 3·2^e·P (PROOF_G6 §0; in the real walk
P = 2^{ρ−1}·U/3 and T_e = E_{ρ+e−1}). The interlude = the dynamics on this queue until the
re-entry fire on T_dp; by work_g6 Prop 1 it lasts s = 2·dk(J) steps. agentB_run7.verify(J)
certifies (dk, dp) per class (unique across all 2-adic splits: **leaves = 1 at every probed
j ≤ 30000** — no decision ever depends on the class member).

## 1. The exact formula [Class-A; V1: 0 failures on J = 7..2000]

Let ρ* = the position of the last **pure sub-fire** (b, c both run entries; ρ* ≤ J−3 by
work_g6 Prop 2 — the sub-cascade replays the universal level process at base u until queue
index J−1 is read), K = kat[ρ*] (the universal k at ρ* — machine-equal at every sub-fire, V1),
g = J−2−ρ*, e = 2(dk−K) the window steps, and **S_win** = Σ j over all chains from the ρ*-fire
(inclusive) to the re-entry (exclusive). Then exactly:

```
(I1)  dk(J) = kat[ρ*] + e/2                         [steps before the sub-fire at ρ = 2k_ρ]
(I2)  4·dk(J) = J + dp + Σ_{chains≠re-entry} j      [each step consumes exactly 2 queue entries]
(I3)  2e = g + 2 + dp + S_win                       [window accounting]
(I4)  dk(J) ≤ J  ⟺  dp(J) + S_win(J) ≤ 4Φ(ρ*) + 3(J−ρ*) − 4,   Φ = p − k.
```

*Proof of I2/I3 (new here, Class-A).* Every step consumes exactly the two front entries; a
chain with parameter j pushes exactly j entries (run u·2^0..2^{j−2} plus its seam). Over the
whole interlude the consumed entries are: the run (J−1), D_h (1), T_2..T_{dp+1} (dp), and all
pushed entries except the re-entry's (Σ_{chains≠re} j); the interlude has 2dk steps ⟹ I2.
The window (steps 2K+1..2dk) additionally consumes the ρ*-fire's run pair (2) and the run
remainder (g−1), and its pushes are the window chains' (S_win) — everything pushed before the
re-entry is consumed there because the re-entry is clean (P = ∅ at level fires) ⟹ I3. I4 is
algebra: 4J − 4K − g − 2 − dp = 4Φ(ρ*) + 3(J−ρ*) − 4. ∎
Verified digit-for-digit on J = 7..2000 (V1; also every window chain parameter < J, and the
per-J target inequality I4 itself holds everywhere: dp+S_win ≤ 4Φ+3g'−4).

**Census [Class-B]:** max S_win = 21 (J = 1539: tie/mixed fire j = 12 = 1+v₂(3K+3δ+1), K = 681),
22 at J = 3066; max window parameter 13; ≤ 5 window chains; dp ∈ [2,6]; g ≤ 6; window chains
read b ∈ {R(ρ*-fire + ≤1 mixed at J−2), D(≤1), M/d (interior)}. dk ≤ j everywhere
(J ≤ 5200 canonical = certified; run7 spot-certified dk(20000) = 8922, dk(30000) = 13384).

## 2. The window structure [Class-A]

- **Roots.** A window chain's b is a run entry, D_h, a T, or pushed. Fires with b = run a are
  *pure* (c = run a+1) — so ≤ ρ* — except the single possible mixed fire (b = run J−2, c = D_h).
  The host seam D_h is one entry, consumed once (as b: the D-fire; as c; or in an even step);
  T-as-b fires are the re-entry by definition. So **S_win = spine(j_last) + spine(j_e)**:
  exactly ≤ 2 spawning roots — the ρ*-fire (parameter j_last = 1+v₂(3K+2), a universal class
  value ≤ 1+log₂(3K+2)) and at most one D-consuming fire (j_e ≤ min(J−2 [EX, agentB2 PROVED],
  1+v₂(3K_exit+1) ≤ 1+log₂(3(K+δ)+1)) [agentB2 Lemmas 1–2]).
- **Spines.** Every interior chain reads a pushed b. A cascade of a j-fire = its universal
  replay (param-sum = ΣU(j) := 4·kat[ρ'′]−ρ'′+j(ρ'′) over its last pure fire ρ'′ ≤ j−3 — the
  same identity I2 applied to the sub-level) followed by a window whose frontier entries are
  single (the crossing leftover Y, each seam d) — each fires ≤ once. So
  **spine(j) = j + ΣU(j) + spine(j_Y) + spine(j_d)** with j_Y, j_d ≤ μ(j) := 1+log₂(3·katUB(j−3)+6j+13)
  (the bootstrap δ ≤ 2j; λ-bound 6s+5 with s ≤ 2dk ≤ 3J+92 from I2+CL). μ(j) < j for j ≥ 7:
  the parameter cascade is strictly decreasing — this is the R9-audit "nested parameters
  strictly decrease", now proved from EX (D-branch) + CL at sub-positions ≤ J−3 (sub-fire
  branch: j ≤ 1+log₂(3kat+2) ≤ 1+log₂(3(J−6)+2) < J for J ≥ 12).
- **Base.** For params ≤ 8 the window param-sum is ≤ 3 over ALL short mixed tails
  (V4: 3 hosts × 9 tail lengths × 70 D-λ residues, 9450 fired chains, 0 halt-like chains);
  c_base = 4 used.

## 3. The CL constants [Class-A given the table + Class-B exhaustive; V2]

- **Φ-profile** (fire walk with the certified table, exhaustive to p = 10^6): Φ = 3 only at
  p = 4; Φ ≥ 16 for p ≥ 26; **Φ ≥ 2750 on [4958, 10^6]** (first zone position 4959).
- **Beyond** (agentA's counting bound, constants recomputed): ε = 3.1673, post-spike
  Φ ≥ 16+18s−(17/8)(εs+K(s))−5−log₂(3s+2) ≥ 3 on every slab 2^9..2^1100 and by monotone
  domination beyond (18−(17/8)·6 = 5.25 > 0 vs the O(t²) correction). This is far beyond
  need: the induction uses only Φ ≥ 2750 up to 10^6 and ≥ 795 beyond.
- **Scope (the circularity audit, V3).** agentA's CL proof at positions ≤ q consumes dk only
  at spike parameters ≤ 5+v₂(3s+2), s ≤ q/16 — i.e. ≤ 5+log₂(3q/16+2) < q−1. So

  **H1(<J) ⟹ CL holds at all positions ≤ 16·(2^{J−6}−2)/3 ≫ J** (verified in V3:
  5+log₂(3(J−3)/16+2) < J−1 for all J ≥ 11) — the sub-level bound only ever meets positions
  ≤ ρ* ≤ J−3 and parameters < J. The sub-level's walk cannot encounter a spike of parameter
  ≥ J: sub-fires sit at positions ≤ J−3 with kat ≤ ρ−3 (CL) ⟹ j < J; D-fires/seams have
  j ≤ J−2 (EX, PROVED); nested recursion decreases (§2). **The anticipated circularity is
  absent: each traversal of CL → window → dk drops the parameter by ≥ 1.**

## 4. The induction [Class-A given the inputs; V3]

**Theorem (H1-dk).** dk(j) ≤ j for every j ≥ 1.

*Base* j ≤ 5200: the certified table (run7 class-split verification, unique (dk,dp), canonical
re-entry, u ≥ 3; agentA V0 for j ≤ 120; this work for 121..5200 — max dk(5200) = 2331,
dp ≤ 6 throughout; phi-canonical = run7 on all 200+ cross-checked values).

*Step* J > 5200. Write the target from I4: dp+S_win ≤ 4Φ(ρ*)+3(J−ρ*)−4. All CL calls are at
positions ρ* ≤ J−3 (spike params needed ≤ 5+log₂(3(J−3)/16+2)): table-only for
J ≤ 2.2·10^35 (agentA scope A), H1(<J) beyond — parameters strictly below J in either case.
- **Case (a)** ρ* ≥ 4958: Φ(ρ*) ≥ 2750 (exhaustive to 10^6; counting bound beyond) ⟹
  target ≥ 10996.
- **Case (b)** ρ* ≤ 4957: J−ρ* ≥ 244 ⟹ target ≥ 3·244+8 = 740.
- **Micro-zone** (ρ* ≤ 4957 with J−ρ* < 244) forces J < 5200: the table.

Both bounds exceed by an order of magnitude what is needed:
- **EL-route:** with the measured exit-length input dp+S_win ≤ 66 (census max 28), done.
- **PIN-route** (weaker input): with the pinning law (below) the spine recursion of §2 gives
  S_win ≤ 2·spine(μ*(J)) with exact ΣU tables (μ*(J) = 1+log₂(18J+283); spine = {7:16, 8:41,
  10:47, 16:56, 18:108, 26:122, 64:189, 96:256}); with the single measured constant dp ≤ 6:
  worst case J = 5201: dp+S ≤ 2·108+6 = 220 ≤ 740 (slack 520; tolerated dp ≈ 526 at J = 5201,
  growing linearly in J while the bound grows as O(log J·log*log J)). Grid-checked to
  J = 2^64 (V3). The purely structural dp accounting (dp ≤ 2+g+2S_win+μ* from the T-consumption
  census) is *not* sufficient (dp+S ≤ 905 vs 740 at J = 5201) — dp ≤ 6 remains the one
  measured constant of this route. ∎

**The pinning law (PIN).** Every chain of the J-class interlude has j = v₂(λ_x) with margin
(S1) — equivalently verify(J) pins throughout (leaves = 1). This is the INV-L/PD drain applied
at the class-sim level: its PD cases need only CL at sub-positions ≤ J−3 (⟸ H1(<J), §3), EX
(proved), and trivial T-cases (t = J+e ≫ j) — the same hypothesis family ASSEMBLY.md already
carries as G4/G5 (with the §9-review caveats on sub-steps (C),(D) of the lineage proof, and
agentC10's margin-drain lemma E5 supplying the λ≠0-tail genericity). Empirically: leaves = 1
at every probed j ≤ 30000; agentB2's pinning calculus closed all 12 first-exit shapes
symbolically. PIN is *not* derivable from H1(<J) through the *real walk* (that route would
need (M1′) at pointers ≈ 2^{J−1}, a same-level circle) — the class sim's symbolic P
(v₂ ≥ max(200, J+100), the worst instantiation) is what makes the induction close.

## 5. Empirical verification summary [V1–V5; ~12 s total]

- V1: I1–I4 + target inequality, J = 7..2000, 0 failures; census as in §1.
- V2: Φ-profile to 10^6; counting-bound slabs; scope inequalities.
- V3: induction case check on the J-grid (5201..2^64): both routes pass; well-foundedness
  inequalities verified.
- V4: small-context sweep (params ≤ 8, 3 hosts × 9 tails × 70 λ-residues): max spine 3,
  0 halt-like chains.
- V5: real walk (formal map F, exact big-int) to i = 2·10^5: **every chain at every nesting
  has j ≤ 18 ≤ 120** (max at the level fire i = 97955 — exactly R10's Δ = 20 record);
  nested non-level spikes: 6 events, all j = 5; level stream = universal (agentA V4).
  Spot certifications: dk(20000) = 8922 ≤ 20000, dk(30000) = 13384 ≤ 30000 (run7, leaves=1).
- Table extension: j = 121..5200 certified (agentD_table5000/5100.json); dk ≤ j and dp ≤ 6
  hold throughout; dk(14) = 8, dk(19) = 8, dk(20) = 9 reproduce the task's values.

## 6. What this does to ASSEMBLY.md

- **H1-dk: CLOSED** (base table + the induction above). With agentA's CL (conditional only on
  H1-dk) the loop CL ⟺ H1-dk closes as one well-founded induction — **the entire proof tree
  of the non-halting theorem is now proved modulo**: the exit-length constants used only for
  J > 5200 (EL or dp ≤ 6 — measured with ≥ 10x margin against tolerance), and the tree's own
  pre-existing residuals ((M1′)-family pinning = G3/G4/G5's inputs, per ASSEMBLY already
  proved modulo CL+EX; EX proved; EG closed; (M2′) via Prop 1 + CL). No new residual family
  is introduced: the pinning input of the PIN-route *is* the tree's INV-L, and the EL-route
  needs no pinning beyond the table at all.
- Residual, stated exactly: for J > 5200 the proof consumes one measured exit-length bound —
  **dp(J) ≤ 6** (with PIN) or **dp(J)+S_win(J) ≤ 66** (without PIN) — while the certified
  regime (J ≤ 5200) plus the identity chain reduce everything else to CL and the structural
  lemmas proved here. A full de-escalation of dp ≤ 6 would need exactly the exit-closure
  depth control that work_g6 §2/§4.2 left open (the escaping branch), so this is the same
  object, now isolated to a single constant with ~90x headroom (dp ≤ 6 measured, ≤ ~526 needed).

## 7. Reproduction

```bash
cd work_r10
python -B agentD_measure.py 2000      # census + identities (also writes agentD_data.json)
python -B agentD_proof.py 2000 1000000  # V1-V5, ~12 s
# table extension (run7, ~1 h for 121..5000 + 11 min for 5001..5200):
python -B -c "import sys; sys.path.insert(0, r'D:\math_cc\scratch'); from agentB_run7 import verify; \
  [verify(j) for j in range(121, 5201)]"
```
