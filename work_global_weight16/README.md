# Weighted return analysis through 16

New conditional proof work, not independently reviewed.

- `PROOF_WEIGHT16.md`: rooted phase inclusion and safe returns whose
  resulting weight is at most 16, assuming the stated earlier source
  hypotheses. The main new lemma handles A/B/C origins of the second
  phase-5 resonance and retains a common joint congruence.
- `verify_weight16.py`: exact finite grammar, provenance, small-source,
  and algebra checks. Run from the repository with
  `python -B work_global_weight16/verify_weight16.py`.
- `checks.json`: generated results and next-layer diagnostics.

Weight 16 departures and unbounded total weight remain open. This
does not prove global G2 or global non-halting, and does not modify
the accepted proof notes.
