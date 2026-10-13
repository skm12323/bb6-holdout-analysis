# ADVERSARY-1 review of agentA's conservation-law proof (CL: p_i - k_i >= 3)

Target: `work_r10/agentA_report.md` + `agentA_proof.py` (+ `agentA_data.json`),
against `scratch/agentB_run7.py` (+ `agentB_abs.py`), `work_r10/fast_walker.py`,
`work_g6/{PROOF_G6.md, verify_g6.py}`, `work_r10/ASSEMBLY.md`.
My scripts: `work_r10/revA_1_transducer.py`, `revA_2_j19.py`, `revA_3_bound.py`,
`revA_4_scope.py`, `revA_6_independent.py`, log `revA_rerun_agentA.log`.
Everything re-run from scratch (own table re-certification, own D/G/B0, own walkers);
stdlib only, total runtime ~2.5 min, footprint a few MB.

**OVERALL VERDICT: PROOF STANDS** (unconditional scope A given the run7 table;
conditional all-i theorem given H1), with 4 minor documentation-level gaps listed
in §G — none of them affects the truth of CL or the soundness of any proof step;
two are constants/prose errors in the safe direction, one is a scope sentence that
agentD quotes too literally, one is a prose-only (but correct, and here
machine-verified) final step of the H1 branch.

---

## 1. Transducer mining — CONFIRMED

- run7.verify re-certified j = 1..120 (0.3 s, all classes split, all leaves agree);
  j = 1..20 digit-equal to the task table; `dk(j) <= j` for all 120 (no violation);
  `min dp = 2`; equals `agentA_data.json`'s stored table 120/120.
- Independent fire-level walk from (4,1); inter-spike (dk,dp) segments mined for
  ALL 16384 spikes s in [0, 2^14). Grouping by t = v2(3s+2): every class has a
  single segment — **zero s-pairs with equal t and different segments**. The
  claim is in fact structural (segment = [(J,dk,dp)] + fixed residue-walk from
  r0 = 10+dk(J), and J = 5+t), so it cannot fail while the table holds; the
  mining confirms it anyway. Classes seen: t = 0..13, 15 (t = 14 first occurs at
  s = 27306 > 2^14, exactly as the report notes).
- All report class-map rows t = 0..14 re-derived independently (d, g, net, drop,
  m) — exact match; the only (dk,dp)-collision is t in {0,2}, as reported.

## 2. The J=19 event — CONFIRMED

- First block with v2(3s+2) = 14 is **s = 27306** (formula + scan), k = 436906,
  **p = 979473** at the spike (the report's "p ~ 1.1e6" is the V3 run cap, not
  the event's p — cosmetic).
- At the event: B = 542567, drop = dk-dp = 8-2 = **6**, V = B-6 = 542561,
  net = dp-dk+g(2) = 2-8+11 = **5**, and the walk's next spike satisfies
  B_next = B+5 exactly. **drop 6 > net 5 confirmed** — the naive per-cycle
  repair bound fails exactly as claimed.
- Per-cycle minima over the whole walk: min net = 5, min dp_total = 21, both
  J = 19 (report's numbers exact). "net >= 6 and dp_total >= 22" holds for all
  11151 cycles with p < 4e5 (in fact up to p = 979473 — the report's "only for
  p < 4e5" is conservative).
- Deeper table facts re-verified: 2*drop > g for ALL J in [23,120]; first
  net < 0 at J = 28; empty walks (dk = 0 mod 16) exactly at J = 35,36,37
  (then 71..73, 106..108); first block-skippers m >= 2 exactly J = 38..41;
  J = 120: drop 48, net -34, m = 4.

## 3. The amortized counting bound — CONFIRMED

- Constants recomputed exactly: eps = 3.167276778..., K = 3228, c = 18-(17/8)eps
  = 11.269537 (all match); sum_{t>=0}(5+t)/2^{t+1} = 6 exactly, so the worst-case
  coefficient 18 - (17/8)*6 = **5.25 > 0** is right.
- Algebra re-derived and every intermediate inequality verified per-cycle on the
  trajectory to s = 1e7: m-1 <= dk/16 (d <= 15), g+d >= 2d (g >= d+1 off rho=10,
  0=0 at rho=10), dp >= 2, sum(dk+d) = 16s, B = B0 + sum(dp+g) - sum dk, and the
  resulting B(s) >= B0 + 18s - (17/8) sum_visited dk at every checkpoint.
- AP counting: class-count formula (root c_t = (2^t-2)*3^{-1} mod 2^{t+1},
  N_t = floor((s-1-c_t)/mod)+1) verified against direct counting; the "+1 per
  class" bound N_t <= s/2^{t+1}+1 is proved; visited-sum <= all-block sum <=
  eps*s + K verified at s = 682, 1e3..1e7 (visited == all-block here since m = 1
  throughout this range).
- Slab logic: I scanned **every** s (not just slab starts) with exact integer
  arithmetic: the pointwise threshold is s = 610; agentA's 682 is the first slab
  START (t = 11) — conservative, and the slab argument (rhs constant, bound
  increasing within a slab) is valid. Verified for all s in [682, 2e5), s = 1e6,
  1e7, and all 116 slab starts up to t = 116. rhs(s) = 11 + bitlen(3s+2) >=
  3 + drop <= 8 + v2(3s+2) <= 8 + log2(3s+2) — conservative by 3.
- H1 branch: slab checks t < 2000 re-run independently — all pass (threshold 682).
  The beyond-2^2000 majorant (the report's prose step) I machine-verified exactly:
  5.25*slab_start(t) - (17/8)(K + (t+1)(t+10)/2) - (13+t) > 0 for t = 2000..3000,
  strictly monotone, and the step-gain 5.25*(2^t/3) dwarfs the O(t) step cost for
  all t >= 2000. The **O(t^2) correction claim is CORRECT**: K_H1(t) = 3228 +
  sum_{116<=t'<=t}(5+t') = O(t^2), dominated by 5.25 s ~ 2^t. (But see gap G4:
  agentA's own script does not execute this step.)

## 4. Scope claim (circularity resolution) — CONFIRMED with one inexact sentence (G1)

What agentD needs: *CL at positions <= q consumes dk only at parameters < q.*
Findings from a line-by-line consumption audit (revA_4_scope.py):

- **V3 fire walk** (p < 1.1e6): max fire j = 20 (my walk) — it NEVER meets j > 120,
  and `assert j in TAB` makes it crash rather than assume anything beyond the
  table. **V5 cycle sim** (s < 1e7): max spike J = 28. Neither leaks scope.
- Per-s reading of the proof: for s <= 681 the cycle-exact branch consumes only
  params {1..4} U {5+v2(3n+2) : n <= s} — max 14 for s <= 681; for s >= 682 the
  counting-bound branch consumes, via the CONSTANTS eps and K, the table entries
  dk(5+t) for ALL t <= 115, i.e. parameters up to j = 120 (plus class params
  5+v2(3n+2) < 5+tmax(s)).
- Consequence: the literal sentence "consumes dk only at spike parameters <=
  5+v2(3s+2) with s <= q/16" is **inexact for q >= 24494** (first position where
  the counting branch is invoked; eps/K consume j <= 120 regardless of q).
  However the needed scope still holds everywhere: for q >= 24494, 120 < q-1;
  for 17 <= q < 24494 only the cycle-exact branch is needed (params <= 14 <
  q-1); for 11 <= q < 17 only the pre-spike segment (params <= 4). Verified by
  simulation for q = 11..1e4-spike events, and the analytic bound
  max_{s <= (q-10)/16}(5+v2(3s+2)) < q-1 holds for all q >= 11 (checked
  exhaustively q = 11..3000, floor version to 2e5). **No violation of params < q
  for any q >= 11.**
- Crucially, the j <= 120 entries are **unconditionally certified**: run7 +
  agentB_abs import only `fractions` and `agentB_lib.v2i` (grep-verified: no
  reference to CL, the walkers, agentA, work_r10/g6), they simulate the audited
  top map on symbolic k = kappa + 2^m s with class-splitting (leaves partition
  the full class; failures are loud: cap-exceeded/ambiguity -> None, and agentA
  asserts not-None for all j <= 120), and a SECOND engine (verify_g6.phi,
  concrete big-int cascades) agrees with run7 on all 61 sampled j. So even the
  parameters <= 120 consumed out-of-order carry no CL/H1 circularity. The H1
  part (dk <= j for j > 120) is consumed only at params <= 5+tmax(s) < q.
- One caveat agentD should keep: to know WHICH spikes have p_s <= q, one needs
  k_s <= p_s, i.e. a fragment of CL itself. agentA's proof avoids this by
  proving B(s) >= 3+drop for ALL s < S1 simultaneously (cycle-exact sweep +
  global inequality — no induction on s), so the restriction to p <= q is a
  post hoc projection of a global (table-unconditional) fact. That is the right
  way to consume it; an agentD-style joint induction that derives s <= q/16
  from CL-in-progress would be circular — the current write-up does not do that.

## 5. Unconditional scope arithmetic — CONFIRMED, one wrong constant (G2)

- First k with fire-parameter >= 121: class {v2(3k+2) >= 120} has root
  (2^121-2)/3 = 886151997189943915269204706853563050 (~8.9e35, j = 122 there;
  first j = 121 exactly at (5*2^120-2)/3 ~ 2.2e36). Note 2^120-2 is NOT
  divisible by 3 (2^120 = 1 mod 3), so "(2^120-2)/3" is not the boundary.
- agentA's S1 = (2^116-2)//3 is valid as a block threshold (every s < S1 has
  3s+2 < 2^116, hence J_s <= 120 — verified: 3*S1+2 = 2^116-2, v2 = 1, S1
  itself is not even a deep block) but conservative by ~5.03x vs the true
  first out-of-table block (5*2^116-2)/3.
- The report's formula 16*(2^116-2)/3 + 10 evaluates to **4.43e35**, not
  "~= 2.6e35" — the quoted constant is wrong arithmetic (off ~1.7x) but in the
  SAFE direction (understates coverage; the true coverage extends to ~8.9e35).
  ASSEMBLY.md repeats "2.6e35". Boundary nit: the covered set should be stated
  with strict inequality at the class boundary. V8's "~2^119" is likewise loose.

## 6. Re-run + independent verification — CONFIRMED

- `agentA_proof.py` re-run: all V0-V8 green, 12 s, stdlib only (log:
  `revA_rerun_agentA.log`); output identical in substance to the report's log
  (incl. Phi_min = 3 at i = 0, min net 5 / min dp_total 21 at J = 19).
- Independent walker (own table, own bookkeeping): **605759 fires to p >= 2e6**
  (vs agentA's 333167 to 1.1e6): Phi >= 3 at EVERY fire, Phi_min = 3 at (4,1,1),
  worst post-spike V = 18, worst slack B-3-drop = 15; 55758 spike cycles.
- Full (p,k,j) stream == `fast_walker.exact_walker` level fires on all 60575
  fires with i <= 2e5 — the object is the audited walk F (and fast_walker itself
  has no CL dependency).
- Cycle-level sim extended to **s = 1e8** (k ~ 1.6e9; 10x agentA's run):
  invariant B >= 3+drop and V >= 3 at every cycle, sum(dk+d) = 16s identity.

## 7. Measured-for-proved substitutions — none load-bearing; 2 label gaps (G3, G4)

- L1/L3 (fire classes, residue flow): genuine arithmetic — nothing measured.
- L2/L4/L5 and B0 = 16: honest finite computations, but they CONSUME the
  certified table entries j = 1..4 — i.e. they are Class-A GIVEN V0, not
  unconditionally Class-A. The report's §2 header "[Class-A; V1, V2]" should be
  read as "Class-A given the certified table" (V0's [Class-B] machine
  certification is a genuine input). No unsoundness — the theorem's statement
  already says "given the table" — but the label is imprecise.
- The transducer (V6) and V6b parity closure are mined/measured remarks and are
  NOT load-bearing (V7 covers s >= 682 within the table unconditionally; V5
  covers s < 1e7 exhaustively).
- The only "measured" fact load-bearing beyond the table is (H1) itself
  (dk <= j for j > 120), and it is used only in the explicitly-conditional
  theorem; "measured to j = 20000 by prior runs" is motivation, not re-run here
  (only j <= 120 re-certified in this script; agentD later certifies 1..3200
  contiguous + 5001..5200).
- V4's stream-agreement (i <= 2e5) identifies the object (Class-B evidence);
  the CL inequality itself never leans on it.
- One prose-vs-script mismatch: the H1 branch's "beyond s ~ 2^2000: majorant,
  c >= 5.25 > 0" step is NOT executed in agentA_proof.py (slab checks stop at
  t = 2000); it is asserted in the print string. I verified it exactly here
  (item 3) — it is true — but as delivered the machine certificate covers
  s < 2^2000 only, with the last stretch argued by hand.

## G. Gap list (all minor; none refutes)

- **G1 (scope wording, matters for agentD).** The counting-bound branch of CL
  consumes the table constants dk(5+t), t <= 115 (via eps, K) — parameters up
  to j = 120 — for EVERY q >= 24494, not only "parameters <= 5+v2(3s+2),
  s <= q/16". The needed scope (params < q for q >= 11) still holds, and those
  parameters are unconditionally certified, so the circularity resolution
  survives; agentD should quote the corrected consumption profile.
- **G2 (constants).** "k <= 16(2^116-2)/3+10 ~ 2.6e35" should read ~4.43e35
  (and the true table coverage extends to (2^121-2)/3 ~ 8.9e35); "first J=19 at
  p ~ 1.1e6" should read p = 979473; boundary should be strict. All errors are
  in the conservative direction.
- **G3 (labels).** §2's "[Class-A]" is really "Class-A given the V0 table";
  V6b and the j=20000 prior-run remark are context, not proof.
- **G4 (script coverage).** The H1-conditional all-i claim's final segment
  (s >= ~2^2000) is a correct but prose-only majorant argument in the delivered
  script; machine-checked here by the reviewer.

## Conclusion

The reduction of CL to spike-exit minima is airtight (off-spike Phi strictly
increases by certified table entries; residue flow enters every block's spike
exactly, never skipping); the J=19 obstruction is real and correctly handled by
switching from per-cycle to amortized accounting; the counting bound's algebra,
constants, AP counting, slab logic and (after my extension) the beyond-2^2000
majorant are all correct; the certification chain (run7 class-split symbolic
sim, cross-checked by a second concrete engine) is independent of CL; and the
invariant holds cycle-exactly under three independent engines to s = 1e8 and
fire-by-fire to p = 2e6 with Phi_min = 3 at i = 0 (so C = 3 is optimal).

**CL: PROOF STANDS** — unconditionally for every fire with j <= 120 (covers all
k < 4.43e35 by agentA's conservative bound, in truth k < 8.9e35), and for all i
under (H1) dk(j) <= j, dp(j) >= 2 — with the documentation gaps G1-G4 to be
folded into ASSEMBLY.md before the final write-up.
