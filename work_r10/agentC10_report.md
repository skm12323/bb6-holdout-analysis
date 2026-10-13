# R10-C10: the ENDGAME (scope D5 of the repaired Theorem R) — CLOSED for all v <= 65536, conditional closure for all v

Scope: the endgame of the real excursions E(w,v) under the audited top map — the
dynamics from the first read of the substituted boundary entry (the defect) to
the excursion's termination at a singleton. Base: work_g6/PROOF_G6.md §5 (the
formal pair map F; D5 note), work_r1/RULES.md (top map), work_r10/fast_walker.py
(the validated F walker, adapted here), scratch/agentB_closedform.md §6.2/§7.11
(the 41-template endgame evidence). Artifacts (this directory):
`agentC10_lib.py` (engines), `agentC10_run1.py`, `agentC10_run2.py`,
`agentC10_run3.py` (drivers), `agentC10_out1/2/3.json`, `agentC10_cross.json`.
Tags [Class-A]/[Class-B]/[Class-C] as in work_g6. Everything pair-side is
U-free: a pair (c,l) denotes cU+l for every odd U, so every machine
verification is valid for **all odd w at once** (U = 3w), by Lemma E1 below.

**STATUS: the endgame never halts and always reaches the singleton — proved
exhaustively for every v <= 65536 [Class-B, U-generic], with the per-class
symbolic lift [Class-A per class] closing every occurring crossing's full
arithmetic cylinder; the all-v extension inherits exactly the walk's own
residual (the deficit law (M1'), verified to i = 10^8 by fast_walker) and
nothing else. The task's proposed route — decisions as a function of v mod 2^m
with m ~ 11 — is FALSE for every m <= 16 (§6); the class variable that closes
is the crossing state's lambda-residues, which are near-injective in v.**

## 1. The boundary formalization [Class-A]

The excursion E(w,v) = (U+1; U, 2U, ..., 2^{v-2}U, 2^{v-1}U - 1), U = 3w odd,
differs from the infinite walk (U+1; U, 2U, 4U, ...) in exactly two ways:
- the suffix entry at index v-1 is the DEFECT pair (2^{v-1}, **-1**) (lambda
  negative), and
- the run ENDS there: no E_v, E_{v+1}, ...; the only remaining fill is the
  ZERO pair (0,0) as the *second* read entry when the queue has exactly one
  entry left (the audited top map reads missing entries as 0, work_r1 §5).

The excursion coincides with the walk exactly until the first step that reads
suffix index v-1 (queue determinism, L0). That pre-step state is the CROSSING
at v-1; its queue has 0 or 1 pushed entries (nP in {0,1}) and its pointer is
v-1 or v-2. `walk_master` records all crossings of the infinite walk (exact
bigint pairs, with per-step S1/S2/u-form/mass asserts; the level-fire stream
equals fast_walker.py's on all 19988 fires to i = 66000, and the base-range
anchor 6690 chains / 6056 fires to i = 20000 = the G6 V6 numbers).

**Lemma E1 (boundary simulation) [Class-A].** Fix v and any odd U. Run the
pair map with the boundary suffix above, mapping each state to the integer
list (cU+l; ...suffix...). Along every step where chains satisfy (S1)
v2(l_x) < v2(c_x) and (S2) c_A even, the real top-map orbit of E(w,v) passes
through exactly these states; HALT (u = 1) never occurs among them.
*Proof.* Induction as in work_g6 §5.2: value parity is (c+l) mod 2 (U odd);
even steps are the same linear update; at a chain the real x = c_x U + l_x
has v2(x) = v2(l_x) = j for every odd U by (S1) — the sign of l_x is
irrelevant mod 2 — so u = (c_x/2^j)U + l_x/2^j and the successor is the
audited closed form (u+1; u, 2u, ..., 2^{j-2}u, c+(A+1)/2, S); the boundary
pair evaluates to 2^{v-1}U - 1 and the ZERO pair to 0. (S2)'s role is only to
keep D integer; the walk start and the tiny crossings at n <= 1 have c_A = 1
odd, handled exactly by the value parity (c_A + l_A) mod 2. ∎

**Lemma E2 (signs: the -1 never propagates) [Class-A].** At every state of the
excursion walk, every lambda is >= 0 except the *unread* boundary entry (-1);
the head l_A >= 0 always (odd >= 1 at chains); at every chain
l_x = l_A + 2 l_b + 3 >= 2 (in particular l_x > 0, even, j >= 1); every pushed
l_u = l_x/2^j >= 1 odd; every D has l_D = l_c + (l_A+1)/2 >= 0.
*Proof.* Induction over steps; the walk prefix has all l >= 0; the only
negative input ever read is the boundary's -1 (as b: l_x >= 1 + (-2) + 3 = 2;
as c: l_D >= -1 + (1+1)/2 = 0); all other combinations add >= 3 or halve a
positive odd. ∎ (Measured on all 44882 endgame chains, v <= 65536:
min l_x = 8, min l_u = 1 — the lemma's bounds hold with the stated tightness.)

**Lemma E3 (safety: no halt, all U) [Class-A].** At every endgame chain with
(S1): c_u = c_x/2^j is even >= 2 (because v2(c_x) >= j+1) and l_u odd >= 1
(E2), hence u = c_u U + l_u >= 2U + 1 >= 3 for every odd U >= 1 (u is
increasing in U; it suffices to check U = 1). **No endgame chain ever halts.**
(Measured: min u at U=1 is 7; at U=3, i.e. w=1, min u = 19 — exactly agentB
§6.2's "every chain u >= 19 at w = 1".)

**Lemma E4 (mass identities with the boundary) [Class-A].** With i the count
of consumed originals plus the boundary: c_A + Sum_P c = 2^i (so = 2^v once
the boundary is consumed) and l_A + Sum_P l = 3s+1 - [boundary consumed].
The run terminates at the singleton pair exactly (2^v, 3*ell(v)), i.e. the
value 2^v*3w + 3*ell(v). Also l_x <= 9s+6, so **j <= log2(9s+6)** at every
endgame chain. ∎

**Lemma E5 (deficit drain; margins reduce to the walk deficit law)
[Class-A].** Define the deficit d(value) := (v-1) - v2(c). Since
v2(x+y) >= min(v2 x, v2 y): even step d(A') <= max(d(A), d(b), d(c)); chain
d(x) <= max(d(A), d(b)-1), d(u) = d(x)+j, pushed entries d(u)-t, and
d(D) <= max(d(c), d(A)+1). Hence v2(c_x) >= (v-1) - D_cross - (sum of the
run's j) - 1 with D_cross the crossing deficit, and the margin (S1) holds at
every chain whenever **(v-1) - D_cross > maxj + (sum j) + 1**. With
maxj, sum j <= e*(log2(9s+6)) and s <= 0.9v+16 [Class-B], margins are
automatic for large v given the walk deficit law D(n) <= log2 n + c — the
same (M1') family already verified to i = 10^8. The dependence is EXACT:
the robustness sweep (§7) shows closure iff n - D_cross > J with the measured
margin formula margin = n - D_cross - J at the dominant (boundary) chain. ∎

## 2. Task 1 — boundary-state verification [Class-B, valid for all odd U by E1]

For v = 1..2000, w = 1 (U = 3; spots w = 3, 5 i.e. U = 9, 15 for v <= 64):
the exact pair walk with boundary vs the ground-truth integer top map, run in
lockstep with full list comparison at every one of **1,780,141 states:
identical**, no chain halts, every run reaches the singleton 2^v U + 3*ell(v)
(the pair final is exactly (2^v, 3*ell(v)) — E4). ell(1..20) =
1,1,2,2,5,4,4,6,7,8,8,10,10,15,12,12,14,15,15,16 = agentB Theorem 4's table.
Every step asserts (S1), (S2), the u-form, and both mass identities; e(v) :=
ell - s_cross in [1,12] for v <= 2000 (agentB's e in {0..12} under their
offset boundary conventions — consistent). Independent replication:
crossings+endgame (run2) == full runs (run1) on v <= 2000, 0 mismatches.

## 3. Task 2 — the class measurement: v mod 2^m FAILS; the crossing residues are the class

The endgame decision sequence dec(v) = (nP at the crossing; the parity/j
stream) is **not** a function of v mod 2^m for any feasible m:
- minimal m on v in [1,4096] is **12** (trivial: every class a singleton);
- on [1,65536] it is **16** (again trivial); at m = 11 **all 2048 classes are
  non-uniform** (e.g. class {1, 2049, 4097, ...}: e = 1, 1, 3, ... for
  successive members).
- Reason: the crossing lambdas l_A(v-1) ~ 3s are a log-periodic function of v
  (spike structure: the template counts halve per +1 of j — 19847, 7249,
  3425, 1827, 913, 457, 229, 114, 57, 29, 14, 7, 3, 2, 1, 1 — the geometric
  rarity law of work_r10 Lemma K), with no exact periodicity at any scale.

The class variable that DOES determine everything is the crossing state
itself: with the global modulus K = 1 + maxj = 18 (maxj = the largest endgame
chain parameter over the range = 17),
  class(v) = (nP, ip-offset, l_A mod 2^18, l_Y mod 2^18)
is **injective on v <= 65536** (measured; at K = 15 there are 42570 classes,
22966 with two members, and only 4 non-uniform — those are deep ties j >= K,
resolved one bit higher). 24 distinct decision templates on [1,65536]
(17 for v <= 2000; agentB's 41 shapes used coarser boundary conventions).
The template table (count, e, maxj; all have min margin >= 1, min u@U=1 >= 7):
dec=(0,): 24803 total (e=1); (1,0): 19847 (e=2); (3,0,0): 7249 (e=3, margin
1); (2,0): 5519; (4,0,0): 3425; (5,0,0,1,0): 1827 (e=5); (6,...): 913;
(7,...): 457; (8,...): 229; ... up to (17,0,0,1,0,4,0,0,0,2,0,1,0,3,0,0):
1 (v = 48976, e = 16).

## 4. Task 3 — per-class symbolic closure + robustness

**Per-class [Class-A given the class data; Class-B class list].** For each of
the 65536 occurring classes, the symbolic endgame run with
l_A = r_A + 2^18*t, l_Y = r_Y + 2^18*t (t >= 0 ARBITRARY; c-side = the
crossing's exact (odd q, deficit d) pairs) closes the whole cylinder:
**65536/65536, zero failures.** Mechanism: every decision is a v2 of an
integer affine function of t whose slope is divisible by 2^18 > every j of
the class, so every decision is uniform in t (v2(a t + b) = v2(b) for all
t >= 0 when v2(b) < v2(a)); every margin grows by +1 per unit of the common
scale n = v-1; c_u stays even >= 2 and l_u odd >= 1 for all t, so u >= 2U+1
>= 3 for all t and all odd U (E3). The run reproduces the measured dec and e
of every class member and the exact final (2^v, 3*ell) identity.
This is the exact, all-members version of agentB's affine fits
"u = lambda*2^v + mu*k_b + nu with lambda > 0": here c_u = q*2^{n-d} exactly.

**Robustness (arbitrary LEGAL crossings — mass identities enforced, so E4
holds) [Class-B].** The endgame machinery closes for every sampled crossing
state, real or not:
- exhaustive small-lambda (l_A < 2048, l_Y < 256, 5 c-shapes, both pointers):
  **874,756 / 874,756 = 100.0000%**;
- 200,000 random large-lambda crossings (l < 10^7, deficits <= 20):
  **100.000%**;
- 21,600 adversarial deep ties (l_A + 3 = 2^J*odd, J <= 29): **100%**, with
  e up to 26 = J-ish as predicted;
- the closure threshold is exact: closes iff **n - D_cross > J**, with
  margin = n - D_cross - J at the dominant chain (probed on a (D, J) grid).
So the closure is structural (deficit-below-scale), not a coincidence of the
real walk's residues.

## 5. Task 4 — the endgame length bound

Measured: **e(v) in [1,16] for all v <= 65536** (sup 16 at v = 48976, where
maxj = 17; e = 1 for all 24803 chain-free endgames). The structural law:
**e <= maxj + 1 with ZERO violations on all 65536 real endgames** (arbitrary
legal crossings: e <= maxj + 4). Combined with E4's j <= log2(9s+6):
**e(v) <= log2(9*ell(v)) + 2 for every v whose endgame satisfies (S1)** —
"e <= 16" is the scale-bound instance (holds whenever ell(v) < ~2^14·9^-1...
precisely whenever maxj <= 15); e grows only logarithmically with the walk
scale (e = 16 first at v = 48976 ~ the spike-exit scale).

## 6. Task 5 — closure statement

**CLOSED (unconditional in U):** for every v <= 65536 and every odd w, the
excursion E(w,v) never halts and reaches the singleton (2^v*3w + 3*ell(v)) in
ell(v) = s_cross(v) + e(v) steps, e(v) <= 16. [Class-B exhaustive over v —
and U-generic by E1: the pair verification never mentions U.]

**For all v (conditional, same residual as the repaired Theorem R):** by E5 +
the robustness law, the endgame closes at any crossing whose deficit obeys
n - D_cross > maxj + (sum j) + 1. The walk's deficit law D(n) <= log2 n + c
is exactly (M1') (verified to i = 10^8, work_r10 §2; unproved in general —
the shared residual, together with the growth bound (M2') feeding
j <= log2(9s+6)). No endgame-specific residue coincidence is needed.

**The exact object that fails the proposed route:** the modulus class law
"dec(v) = f(v mod 2^m), m ~ 11" is false for every m <= 16 on the measured
range (§3): the walk's crossing lambdas are log-periodic, not periodic, so
the endgame is not finitely classifiable by v-residues. What closes instead:
each occurring crossing closes its own 2^18-cylinder symbolically (§4), and
the safety content (E2, E3) plus the drain reduction (E5) hold for EVERY
crossing state — so nothing about the endgame itself remains open beyond the
walk's own (M1')/(M2') residuals. Compared with agentB §6.2: their domination
claims are confirmed and strengthened (exact cylinder closure, exact u-form,
exact threshold n - D > J); their template count 41 becomes 24 exact decision
templates here (17 for v <= 2000) under the exact single-step convention.

## 7. Reproduction

```bash
cd work_r10
python agentC10_run1.py    # Task 1: 1.78M-state lockstep check, v<=2000 (~25 s)
python agentC10_run2.py    # Tasks 1-2: walk to 66000, 65536 endgames, class stats (~5 s)
python agentC10_run3.py    # Tasks 3-5: 65536 symbolic cylinders + robustness (~5 s)
```
Artifacts: agentC10_out1.json (per-v ell, s_cross, e, dec, v <= 2000),
agentC10_out2.json (per-v endgame data + stats, v <= 65536),
agentC10_cross.json (crossing states, n <= 66000), agentC10_out3.json
(symbolic closure summary). Total footprint ~13 MB.
