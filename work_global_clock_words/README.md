# Arbitrary-word clock projection

`PROOF_CLOCK_WORDS.md` proves an exact projection of a return word to
one clock congruence and one initial-value congruence. It gives
nonperiodic recurrence spacing, an exact initial-height filter, and
a necessary quadratic-seed test for a first safety failure.

`PROOF_FAILURE_BUDGET.md` adds an analytic finite bound on every
possible unsafe last parameter, and exponential coefficient-loss
safety budgets in the fire parameter. It does not assert that the
epoch stops within those budgets. The stronger budget imports the
new global-clock lemma explicitly.

`clock_words.py` implements the projection and filters. Run
`python -B work_global_clock_words/verify_clock_words.py` to compare
them with the existing independent lattice solver; see `checks.json`.
Run `python -B work_global_clock_words/verify_failure_budget.py` for
the budget inequalities and their generated check record.

All-parameter scope comes from the algebraic proofs. The tests have
their explicitly stated finite ranges. A surviving arithmetic word
is not a canonical trajectory. Global exclusion of the remaining
first-failure candidates has not been proved; this work is not
independently reviewed.
