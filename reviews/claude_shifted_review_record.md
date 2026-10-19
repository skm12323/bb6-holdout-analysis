# Three-way review of work_claude_shifted (Claude subagent), 2026-10-19/20
Reviewers: adversary = Claude subagent (scratch aud56; verify_shifted.py rerun on a copy, json identical apart from
timing; own checks of all 1,116,397 window NT failures, 3,329 gateways, 20,000 resonant states); auditor 1 = agy
gemini-3.8-flash-high (blind, aud54); auditor 2 = cmdc deepseek-v4.1-flash (blind, aud55). Patches were written by
the note's author (Claude subagent) at the coordinator's request and checked by the adversary.
- Adversary: `2. with fixable gaps`. Stands: Lemma 1.3 (= PROOF_EL A2's NT case), Theorem SC, Prop 3.2, gateway
  lemma, WITNESS analysis, "DH fails at actually arising A letters", the [B] certificate, Theorem W as stated (no EXT
  below J, no J_W, no DH), Cor 4.1. Fixes: lift bit 3−d+2^{j′} after a one-step descent (§4 Consequence, DEEP); Cor 1.4
  exceptions (DR final letter, OB's DH_out), P2 HP variant, LOW ">=1"; gateway tags ([A+B] via V2; C2-log hypothesis
  for c gateways); (v2(z),δ)-dependence scope; log* conditions; DEEP sufficient only; §2 wording.
- Auditor 1 (gemini): `1. all correct` (Lemma 1.3 50k cases, WITNESS, SC 20k, gateways, certificate subset j<=12/14).
- Auditor 2 (deepseek): `2. with simple errors`: WITNESS crossing types (resolved: the c crossing with history BBBAA
  is X(ρ+3), recorded at the return after chain 4; the read entries X(4), X(5) are a, b — §2 rewritten with exact
  indices; DR failure explicit: chain 1 of S(ρ+4) j=6 vs G_{−3}(5) v2(z)=4, harmless since ρ+4<K″); c-gateway Φ≡2
  mod 64; DEEP must not rely on the log* count at resonances (proof rewritten with NT + SC + Lemma 1.3).
  Recomputation (all matching): Lemma 1.3 11,300; SC 4,000; WITNESS; gateways; j<=18 uncertified sets; window
  83,858/2 uncertified; 2·10^7 structure counts.
- Targeted re-reviews (adversary): three rounds; final two LOW wording leftovers (X(6132) index; log* condition in §6)
  applied verbatim by the coordinator.
VERDICT: ACCEPTED. Key results: the defect calculus is PROOF_EL's θ̃ automaton; DH weakens to NT (except DR's final
letter and OB's DH_out); "no non-descent in shifted copies" is false (WITNESS), the right target is "records below
precision, ties resolved"; Theorem SC; gateway-tie lemma; finite certificate to 2·10^7 (window [−12,15]; only
(5,5),(5,−11) uncertified); Theorem W. Remaining sufficient condition DEEP: on the deep segment (parameters
>= 2·10^7) the θ̃ drift stays bounded and the first chain below 2·10^7 lands in the certified set. EXT open; K_clock
unchanged.
