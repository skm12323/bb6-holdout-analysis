`2. with fixable gaps`

1. **Item 6 — C2 data paragraph ("40 collisions")**: contradicts the shipped log. `run_g2.txt` contains exactly 39 `collision r=v2` entries (35 with outer j=2, 4 with j=3), all δ=−1; every companion number (6055/318/159/158, 279/279) matches the log exactly, so the log is the intended source — the file's "40" is off by one. The "(end)" part is fine (F2: hpar[1]=hpar[2]=0, so j∈{2,3} ends the epoch).

2. **Item 3 — Theorem B base**: N_B=10^8 and the V2 citation are right, but the recorded V2 certificate (`work_m/run_main.txt`, verify_m.py V2) asserts only margin j<σ and r∈{0,1,2} — i.e. the "tail bound" arm of the disjunctive hypothesis. Descent/DL for ρ≤10^8 is certified nowhere (PROOF_M §7: descent not proved; this file's own non-descent data covers only J<20000), and the tail-bound arm alone doesn't license the theorem's "strictly descends" conclusion. Fixable by recording a descent readout over the V2 range (such source fires have J≲55, inside V4's J<10^6).

3. **Item 2(iii) — (S1) citation**: "(PROOF_M Lemma 2.1)" covers image/call chains only; for R₀ = the source fire (the typical b-type case) (S1) follows from definedness ⇒ Corollary 3.5. The adjacent "valid because F is defined on that epoch" is the correct reason; amend the citation.

4. **Item 8 — review record**: present, lists exactly the 8 patched items, no overclaim; auditor counts (1,582/22,155/9,498/2,262; 18,978/18,990) have no in-repo artifacts — unverifiable here, not contradicted.

Passing items: 1 (q−1<q≤J−3<J<ρ ✓), 2(i)–(ii) (σ^R_0=v2(c_X)=n−ε(n) definitional; ε=0 at a-steps = Lemma 3.2(a) ✓), 4 (τ(5)=2 ⇒ λ_X(5)=10 ⇒ j₃=1; δ irrelevant ✓), 5 (prefix list matches the ≤2-length C2 rows; c,a and c-parent collisions excluded ✓), 7 (3(J−1)²+4<2^{J−3} for J≥12; "suffices, not equivalent" ✓; J=6,9 data ✓). No new global G2-closure or DL claim appeared; Theorem B and the Consequence remain explicitly conditional.
