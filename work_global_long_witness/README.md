# A long local return word

The seven productive entries `5,17,5,122436,5,17,5` occur in a
constructed positive safe local continuation using actual canonical
source records. An explicit preceding A return supplies the first
entry. The continuation subsequently ends. The follow-up proof in
`work_global_ancestry` excludes this explicit fixed-clock outer state
canonically; the same word at unbounded clocks remains unresolved.

This rules out extending the fixed-core seven-entry exclusion to
arbitrary compatible local states without a parameter cap. It does
not refute a canonical-orbit stopping theorem or global non-halting.

See `PROOF_LONG_WITNESS.md`. Run
`python -B work_global_long_witness/verify_long_witness.py` to recompute
the sources and pair-return checks; results are in `checks.json`.
