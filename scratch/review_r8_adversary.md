# ADVERSARY REVIEW — work_r8 (compositional closure of Lemma E(v))

Reviewer role: adversary. Scope: `work_r8/PROOF.md`, `work_r8/verify_r8.py`, against the stated
bases `work_r1/RULES.md` (audited) and `work_r4/PROOF.md`. Everything below was checked by
running code: `python verify_r8.py 60 20` and a full `python verify_r8.py 1000 300`
(reproduces PROOF.md's numbers exactly: 153558 nested calls, margin 3, a(s)<=2,
max ell(v)/v = 1.0714, 16896 + 28160 template runs, 0 reported failures), plus adversarial
probes `scratch/review_adv_probe1..8.py` written for this review.

## 0. EXECUTIVE SUMMARY — THE CENTRAL REFUTATION

**The end-phase template checker (check5/check5b) certifies halting configurations as safe.**
At a "deep branch" (`v2(q0) >= K = 8`), `TemplateChecker.F` returns `('DEEP', ell+1, None)`
*without simulating the nested excursion*. The nested excursion can HALT. Concrete,
triple-verified counterexamples (verified by verify_r8's own `top`, by an independent
re-implementation of T from RULES.md §5, and by the R1–R5 macro rules of RULES.md §3 run to
the HALT row):

| family | exact symbolic start (symbol assignment) | concrete list | outcome |
|---|---|---|---|
| check5b, kapgen=1 (class −2) | `run_canonical_gen(253, 1, (), 1)` at u=h=tt=m=0 | `(2301, 2048, 4094)` | T-step → `[26, 25, 50, 100, 200, 400, 800, 1600, 5245]` → **HALT after 2647 top steps**; firing config `(16381)`, x = 16381+3 = **16384 = 2^14**; macro engine: 19,910,703 macro steps to the HALT row |
| check5, kap = −1 | `run_canonical(253, 1, ())` at u=h=tt=0 | `(2301, 2048, 4095)` | child `[26, 25, ..., 1600, 5246]` → **HALT after 8108 top steps** (macro-verified) |
| check5 glue starts | `run_glue(253, (0,))` at u=h=tt=z=0 | `(2301, 2048)` | **HALT after 1280 top steps** (macro-verified) |

The symbolic checker "passes" all three (`('DEEP', 1)` returned; counted in the 16896/28160
"0 failures"). A scan of check5's own family at the deep residue rho=253
(`r0 ∈ 1..5`, `H = 2048·k`, `k ≤ 12`, `tt ∈ 0..3`, tail empty; 240 instances): **142/240 HALT**
(cap 4·10^5 top steps), including every 3-divisible H tested (H = 6144, 12288, 18432, 24576)
and every r0 ∈ 1..5. The deep residue is not exotic: `d` grows by 3 per macro step, so any
long excursion sweeps through `d ≡ 253 (mod 256)`; whenever the head is odd there, the branch
is deep and the engine stops simulating.

**Where the halts happen.** The halting child excursion `[26,25,...,5246]` never reaches the
template family at all: its maximum canonical `v2(H)` before the halt is **9 < 11**
(highest canonical frame: head 2582, H 2560, J 10239 — still kap = −1 class). I.e. the halt
occurs *during the prefix of the deep excursion*, in the segment that the hand-off skips and
that L-coverage's "post-prefix frame in the lineage family" does not cover. The template
family's `v2(H) >= 2^{K+3}` requirement is load-bearing, and the prefix below it is unsafe
for the family's own d-residues.

**What survives.** The *machine-level* conjecture is not refuted: the true orbit from `(3)`
runs 6·10^6 top steps with no halt; all 469 canonical `2^11 | H` frames seen are class
−1 mod 2^11; no −2-class frame appears. Also unrefuted: check1–check4 (the compositional
re-proof of Lemma E(v) for v ≤ 1000, single-symbol engine) — internally consistent,
contract-checked at every frame, 0 suffix coincidences, cross-validated by check2/check3 and
by R4's independent v ≤ 2000 run. What is refuted is the §2 template machinery, the §2/§3
lineage-closure story, and the C5 reduction built on them.

## 1. VERDICTS ON (C1)–(C5)

- **(C1) compositional prover + mid-excursion contract: GAP.**
  The contract formula itself is correct (it is exactly R1's sum lemma: at the frame
  `(H+d, H, 2H, ..., 2^{r0}H+kap, Z)` the end head must be `2^{r0+1}H + d + 3·ell + kap +
  ΣZ[:a]`; derived and verified against the code's `expect`). But:
  (i) in `TemplateChecker.F` the contract is checked **only when `d0 is not None`**, and
  `d0` is passed **only for top canonical frames**. Every nested frame (recursive call at
  `sp < K`) and every glue frame returns at the *first* suffix match with **no verification
  whatever** (measured: 19712 nested + 2816 glue returns in check5's space; when I enforced
  the nested contract by passing `d0 = 1`, 0 violations — the shipped code simply never
  checks).
  (ii) the stopping criterion (`_final_match`, largest-k-first) can in principle return
  early on a suffix coincidence with a wrong `a`, silently corrupting the caller's resume;
  the single-symbol engine at least counts this (`STATS['coinc'] = 0` at N=1000 — clean),
  the multi-symbol engine does not count anything.
  (iii) most importantly, the chain construction has an **unchecked halting precondition**:
  it is valid only if `o' = q0/2^{s'} >= 3`. If `q0 = 2^{s'}` exactly, T HALTS, but `F`
  builds `nestL = [2, 1, 2, 4, ...]` and simulates a fictional non-halting continuation.
  No engine (single- or multi-symbol) asserts `o' >= 3`. Direct steps are conservative
  (`ge3`/`Undecided`/`Halt`), which makes the asymmetry sharp: the one step where halting
  actually happens is the one step with no check. (Measured min `o'` at u=0 over v ≤ 300:
  73 — benign in the audited runs, but the Class-A wording claims uniform non-halting the
  engine cannot detect violations of.)

- **(C2) check5: REFUTED.** "16896 runs … zero failures — no HALT … for **all symbol
  values**" is false: 142/240 sampled concrete members of the kap = −1 family at rho = 253
  halt (§0), and the glue family contains halters too. The zero-failure count is an artifact
  of the DEEP early-return. Additionally, the side claims "also verified at K = 10 (101376
  runs) and r0 ∈ 6..8 (25344 runs)" (PROOF §2) are **computations that verify_r8.py does not
  contain** — `run_all` only scans r0 ∈ 1..5 at K = 8; no K = 10 code path exists. (A third
  party later re-ran approximations of these in `scratch/review1_extra.py`; the artifact as
  shipped does not perform them.)

- **(C3) check5b: REFUTED, twice.**
  (a) *Empirically*: the −2-generator family has halting members (kap = −2, rho = 253:
  H = 2048, 6144, 12288, 20480, 61440 halt at various tt; see probe5/probe6 output).
  (b) *Logically*: the closure claim is a non sequitur by the artifact's own arithmetic.
  PROOF states `kap_child = H + kap_parent − 1` at r = 1 deep branches; from a −2-class
  parent this is class **−3 mod 2^7**, which is *outside* the claimed generator set
  `{−1 + 2^{11}κ} ∪ {−2 + 2^7 m}` (symbolic check: at `(253, r0=1, kapgen=1)`,
  `kap_child = (12288, 2048, 0, 128, 0…) + 2045`, i.e. −3 mod 2^7, indeed −3 mod 2^11 at
  const — "child class in claimed generator set? False"). Likewise at r = 0 deep branches
  `kap_child = Z1 − H − kap − 1` (classes +1 mod 2^7 or 2^7·j mod 2^11 from a −2 parent).
  The "28160 runs, zero new residue classes" result is **vacuous with respect to all of
  this**: the child J (class `kap_child`) lives *inside the unsimulated deep excursion* and
  is never inspected — the deep-branch check only inspects the outer `window[a:]`, whose
  entries keep the parent's classes. The lineage closure was never actually exercised at
  the point where new classes are generated. The "robustness variant (45056 runs)" is also
  absent from verify_r8.py.

- **(C4) check6: CONFIRMED as a finite check; GAP as evidence.** The check is non-vacuous
  (instrumented: the `jmax >= K+3` assert fires at t = 8 with jmax = 11 for r0 = 30/40/50)
  and the 9-step decision traces are indeed identical. But it samples 3 values of r0, 20
  steps, one J class; and it covers only the *initial* excursion's prefix. The halting
  counterexamples of §0 halt in *children* prefixes — a regime check6 says nothing about.

- **(C5) reduction to two by-hand lemmas: REFUTED.**
  - *L-coverage is insufficient even if true*: "post-prefix frame in the lineage family"
    does not certify the segment between the deep branch and the post-prefix frame. The
    counterexample children halt before ever reaching `v2(H) >= 11` (max canonical v2(H) = 9).
    The induction has a hole exactly one segment wide — and the machine falls through it.
  - *The family it reduces to is not safe* (C2/C3 refutations): "the family is closed under
    the deep-branch hand-off" is a statement about a family that contains halters.
  - *L-middle's quantitative sketch is wrong as stated*: `s' = v2(3t+4+Δ) <= log2(3·ell+4)`
    with `ell <= 2s` yields `s' <= log2(6s+4)`, which is **not** `< r` for end-phase frames
    (small r at large level s — e.g. r = 6, s = 1000 gives bound 12.8 > 6). The uniform
    `ell <= 2s` is itself Class-B (verified to s = 1000 only).
  - *A third, unacknowledged lemma is needed*: prefix-safety of nested excursions — which
    is not merely unproven but **false** for the family as defined (all §0 counterexamples).
  - The real-orbit evidence points the other way: in 6·10^6 top steps, all 23437 deep
    moments (`v2(q0) >= 8`) occur at *non-canonical* (glue) shapes — the r ∈ {0,1,≥2}
    canonical-frame case analysis of §2 analyzes branches the real orbit does not take and
    does not analyze the ones it does.

## 2. DETAILED FINDINGS (F1–F12)

- **F1 (fatal).** Deep-branch hand-off skips simulation; concrete family members halt
  (§0). This kills PROOF §2's check5/check5b interpretation, §3 claims 1–2, and §4's G2
  "reduction".
- **F2 (fatal for the closure claim).** Lineage arithmetic does not close: −2 → −3 (r=1),
  −2 → {+1, 2^7·j} (r=0 with Z1 ≡ 0 resp. −1). Derivations independently recomputed and
  confirmed symbolically (probe3b). "Zero new residue classes" never tests the generative
  step.
- **F3 (soundness gap).** `o' >= 3` never asserted at chain constructions (both engines).
  `q0 = 2^{s'}` is silently mis-simulated. (Measured min o' = 73 for v ≤ 300; benign there.)
- **F4 (verification gap).** Contracts skipped on all `d0=None` returns (nested + glue
  frames) in the template engine; no coincidence counting in the multi-symbol engine.
- **F5 (latent bug).** A deep branch at nesting depth ≥ 1 returns `('DEEP', ell, None)`,
  which the recursive caller unpacks as `(ell_n, a_n, head_n)` → `L = [None] +
  window[ell+1:]` → `TypeError` on the next `_par` (uncaught: `run_all` catches only
  `Undecided/Halt/MFail`). Measured: all 154 deep branches fire at depth 0 — the bug is
  untriggered in the shipped enumeration, but nothing prevents depth ≥ 1, and the general
  argument needs it (deep branches inside shallow nested excursions).
- **F6 (dead code).** Single-symbol `encode()` can never return r ∈ {0,1} (the `L[2]==2H`
  precheck forces r ≥ 2); F's `r==1`/`r==0` branches are dead (they are, however,
  formula-correct: I re-derived q0 = 3H+2kap+d+3 and c' for r=0 and both agree with T).
  The TemplateChecker's unified chain uses raw `b = L[1], c = L[2]` — faithful by
  construction. E-macro and window `L[3:]` formulas: verified faithful.
- **F7 (notational).** PROOF.md line 17 says `K' = c' − q0/2 + 1` while the code's
  `kap_nest = c' − q0/2`; consistent only because the Φ convention writes the J-slot as
  `2^{s−1}o − 1 + K'`. Two different "K" conventions one line apart invite transcription
  error (I initially read it as an off-by-one; it is not, but it should be fixed).
- **F8 (claims not in the verifier).** K = 10 (101376), r0 ∈ 6..8 (25344), robustness
  variant (45056), 512-class scan (2464/7.2M): none are performed by verify_r8.py.
- **F9 (attack #4 resolved in the artifact's favor).** The head-residue dimension of the
  hand-off is sound *by over-approximation*: `d' = d + 3·ell(sp) + 3` (independent of `a`,
  since `Σ_{i<a} 2^{i+2}H = (2^{a+2}−4)H` cancels the continuation base), and `rho` ranges
  over all of `[0,2^8)` — so no surjectivity of `3·ell(sp) mod 2^K` is needed. The hand-off
  enumerates more than reachable in the residue dimension (sound direction). Its failure is
  the skipped simulation, not the residues.
- **F10 (attack #6 resolved in the artifact's favor).** `tail_i = 2^{11}(z_i+1) − pi_i`,
  z ≥ 0 covers all real tails (≥ 2^11 − 1, ≡ 0/−1): over-approximation, sound.
- **F11 (attack #3 resolved in the artifact's favor).** `H = 6·2^{11}u + 2^{11}(1+h)`
  covers every positive multiple of 2^11 (u=0, h = m−1); real bases `3w·2^j`, j ≥ 11 are
  covered. H-forms fine.
- **F12 (numbers that do check out).** Full N=1000/NC=300 run reproduces every quantitative
  claim of §1: 153558 nested calls, margin 3, a(s) ≤ 2, ell ≤ 1.0714·v, coinc = 0;
  check1–4 internally consistent; `spmax = 10 < level` always. PROOF §5's citations of
  scratch/agentD_verify.md match that file's verdicts.

## 3. ANSWERS TO THE ASSIGNED ATTACK LIST

1. *Contract at every exit?* No — see C1(i): nested and glue returns skip it; DEEP returns
   can't check it by design (and that design is the fatal flaw). Single-symbol engine does
   check everywhere and counted 0 coincidences. `final_match` largest-k-first is a real
   (unrealized) risk in the template engine.
2. *Unified chain q0 = A+2b+3?* Faithful in all shapes (raw b,c in the template engine;
   re-derived the r ≥ 2 / r = 1 / r = 0 specializations in the single-symbol engine —
   correct, the latter two dead). The r=1 q0 is right: b = L[1] = H; J sits at c.
3. *H-family coverage?* Sound (F11). The failure is not the family's H-symbol structure.
4. *Head-residue surjectivity?* Moot/sound (F9): rho enumerates all residues, so the
   hand-off over-covers (sound direction) — no surjectivity of 3·ell(sp) needed.
5. *Lineage arithmetic?* r ≥ 2 → kap_child = H − 1 ✓ (confirmed). r = 1 → H + kap − 1 ✓
   (confirmed) but generates −3 from −2 → closure claim false (F2). r = 0 → Z1 − H − kap − 1
   (my derivation; not in PROOF) → classes +1 / 2^7·j from −2 parents → also open. The
   empirical closure never covers these: children are inside the black box (F2), and
   check5b's enumeration contains no glue/r = 0 starts at all.
6. *zlike smallness?* Sound over-approximation (F10).
7. *m ≥ 3/HALT logic?* Direct steps conservative; the nested construction is not — no
   `o' >= 3` check anywhere (F3). The engine *cannot* see q0 = 2^k at exactly the step
   where halting is decided.
8. *check6 statement?* Right statement for the initial excursion, non-vacuous (fires at
   t = 8), but 3 sample r0's, and irrelevant to children prefixes where the counterexamples
   live.
9. *Hidden uniformity steps?* Yes: middle-phase s-independence is checked nowhere for
   r ∈ 6..s−6 (the r0 ∈ 6..8 runs claimed in PROOF are not even in the code — F8);
   L-middle's bound fails for small r at large s (C5); ell ≤ 2s is Class-B to s = 1000.
10. *Code bugs?* F5 (deep-at-depth TypeError), F6 (dead branches), F7 (K' convention),
    F8 (phantom computations), missing memoization irrelevant; `assert`-style checks
    present and effective where they exist; STATS accumulation only covers check1's runs
    (fine, as documented).

## 4. REQUIRED FIXES (in order of severity)

1. **Remove or repair the deep-branch hand-off.** Either recurse at every sp (as the
   single-symbol engine does, with `assert sp < level` — this catches the counterexamples:
   feeding `[2301, 2048, 4095]` to a no-cutoff engine raises Halt), or prove prefix-safety
   for nested excursions — currently false, so the family must first be redefined (e.g.
   excluding rho ≡ 253 mod 256 — but then closure under d-evolution must be reproved; d
   drifts by +3 per macro, so this is not a small repair).
2. Assert `o' >= 3` (nonnegative coefficients, const ≥ 3) at every chain construction in
   both engines.
3. Pass `d0` at nested calls and check the contract at glue returns (or document why they
   are uncheckable); count suffix coincidences in the multi-symbol engine.
4. Redo the lineage arithmetic honestly: r = 1 from −2 gives −3; r = 0 gives Z-classes;
   glue-shape deep branches (the only kind the real orbit exhibits) are unanalyzed. Either
   exhibit the true closed class set and certify *it*, or prove the exotic classes
   unreachable.
5. Handle deep branches at nesting depth ≥ 1 (currently a latent TypeError, F5).
6. Put the K = 10 / r0 ∈ 6..8 / robustness / 512-class computations into verify_r8.py or
   delete the claims from PROOF.md (F8).
7. Restate L-middle with a correct inequality (bound must hold for small r at large level;
   `log2(6s+4) < r` fails there) and mark `ell <= 2s` as Class-B (s ≤ 1000).
8. Retag §2/§3: check5/check5b results are not "Class-A per run / closed lineage" — they
   are refuted as stated (C2, C3); the non-halting status reverts to R4's verified range
   (v ≤ 2000, i.e. top steps n < 2^2001 − 2) plus check1's independent v ≤ 1000 re-proof.

## 5. PROBE ARTIFACTS

- `scratch/review_r8_fullrun.txt` — full verify_r8.py 1000 300 output.
- `scratch/review_adv_probe1.py` — o' ≥ 3 / negative-coefficient instrumentation
  (13371 chains, v ≤ 300: min o' = 73, no negatives, no o' = 1 possible).
- `scratch/review_adv_probe2.py` — deep-branch depths (all 154 at depth 0); nested
  contracts enforced → 0 violations over 19712 nested frames; 2816 unchecked glue returns.
- `scratch/review_adv_probe3.py` — deep-branch shape census; symbolic kap_child = −3 class
  at (253, r0=1, kapgen=1); concrete halting child of the −2-class frame.
- `scratch/review_adv_probe4.py` — triple-engine halt verification of (2301, 2048, 4094).
- `scratch/review_adv_probe5.py` — corrected macro engine (cross-checked step-by-step vs
  T2 for 2645 top steps to the halt); −2-class family halt scan; 3M-step orbit scan
  (no −2-class frames, no halt).
- `scratch/review_adv_probe6.py` — check5 (kap = −1) family halt scan at rho = 253:
  142/240 halt; 6M-step orbit: deep moments all at non-canonical shapes, canonical
  2^11|H frames all class 2047.
- `scratch/review_adv_probe7.py` — check6 non-vacuity instrumentation.
- `scratch/review_adv_probe8.py` — macro verification of the kap = −1 halter
  [2301, 2048, 4095]; prefix analysis of the halting child (max v2(H) = 9 < 11); glue
  member [2301, 2048] halts (1280 steps).

Bottom line: the artifact's own base (R1/R4) and its check1–check4 component stand; the
§2 end-phase template certificate, the lineage closure, and the C5 reduction are refuted
by concrete, macro-verified halting members of the very families they certify. The
all-v non-halting claim remains open, and this artifact does not advance it.
