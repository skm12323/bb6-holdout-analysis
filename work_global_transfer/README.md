# General rescue transport and the weight-18 boundary

`PROOF_TRANSFER.md` gives an all-parameter conditional normalizer for
parameter-5 returns from A/B/C origins, with its exact valuation
collision and normal-source hypotheses. It applies to all 20 new
origins at weight 16 and extends conditional safety through weight 18.

It also derives a more general joint-certificate update for copies
of already-rescued sources. An integer local witness shows why the
simpler normalizer cannot be reused without checking its hypotheses.
Canonical reachability of this witness is not claimed.

Run `python -B work_global_transfer/verify_transfer.py`; results are
saved to `checks.json`. This work is not independently reviewed and
does not settle the unbounded-weight/total-loss problem.
