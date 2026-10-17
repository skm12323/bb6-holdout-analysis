# Rooted ancestry cost

`PROOF_ANCESTRY.md` bounds the coefficient loss needed for a genuine
fire history to approach x/Theta=4/3. The fire coefficient has an odd
numerator and a power-of-two denominator; its separation from 4/3
supplies the bound.

The explicit long local witness requires prior loss at least 244913,
but its fixed clock forces its fire into the certified J<10^6 range,
where loss is at most six. That state and its coefficient lifts are
therefore excluded canonically. The same word at unbounded clocks
is not excluded by this argument.

Run `python -B work_global_ancestry/verify_ancestry.py`; see `checks.json`.
This is new unreviewed work. Global stopping/loss control remains open.

`PROOF_LOCAL_REALIZATION.md` additionally proves that positivity is
automatic along a consistent fire-rooted finite word, and sufficient
coefficient margin gives a safe local realization. Canonical origin
is still a separate requirement. Its checks are reproduced with
`python -B work_global_ancestry/verify_positive_lifts.py`.
