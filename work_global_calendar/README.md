# Exact canonical calendar

`calendar_oracle.py` derives a binary navigation table from a certified
finite set of uniform fire kernels. It answers exact canonical
crossing-time/pointer queries before the first fire above its cutoff,
including indices exponentially larger than that cutoff.

`PROOF_CALENDAR.md` proves the no-skipping rule, binary pointer weights,
inverse navigation, and normalized crossing reconstruction. It states
the boundary explicitly; unresolved higher kernels are not assumed.

Run `python -B work_global_calendar/verify_calendar.py`; results are
in `checks.json`. The B=4096 run includes exact queries near 2^4094.
This work is not independently reviewed and does not close the global
exit/loss problem or enlarge the established non-halting horizon.
