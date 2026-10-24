#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""budget_ledger.py -- exact record-budget ledger for gateway walks (Task 4 groundwork).

Coordinator script (work_gateway_trains root). It does NOT overlap the subagents'
deliverables: it implements and verifies the *ledger identities* behind the record
budget theorem:

  (L1) within a run (no NT gate) the record R = j + Gamma is non-increasing, and each
       step drops R by exactly  j - j' - 1 - eps  (a-step: eps=0);
  (L2) an NT gate (a-step with j' >= j) raises the record to  R_after = j' + Gamma + 1,
       i.e. by  j' - j + 1  (tie at j=5: climb m - 4);
  (L3) with y = run peak (previous gate output, or j_0 for the first run) and
       toll = Gamma(gate) - Gamma(peak):   R_after - R_peak = j' + 1 + toll - y,
       so the gate is *paid* (R_after <= R_peak) iff  j' <= y - toll - 1;
  (L4) consequently max_t R_t <= R_0  iff every NT gate of the walk is paid
       (within runs R is non-increasing, and R_peak(gate t) = R_after(gate t-1)).

Runs on: the tie->tie refutation witness (73515, 98094); all 36 bad-class
representatives (j=5,8,12,14,17,22,24,27); the O2 family u=(2^(m-4)-1)/3 at (5,5).
Canonical crossings come from work_global_calendar Calendar(512); the initial states
of the witness / O2 family are synthetic (non-canonical), the 36 representatives are
the accepted [B] representative states.

Writes budget_ledger.json. Exit 0 iff all identity checks pass.
"""
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from work_global_calendar.calendar_oracle import Calendar  # noqa: E402

OUT = Path(__file__).with_name("budget_ledger.json")


def v2(x):
    if x == 0:
        return None
    x = abs(int(x))
    return (x & -x).bit_length() - 1


def read_cross(cal, n):
    r = cal.crossing(n)
    d = {"kind": r["kind"], "odd": bool(r["odd"]), "tau": r["time"],
         "eps": r["epsilon"], "omega": r["omega"], "cW": None, "lam": None}
    if d["odd"] and d["kind"] != "a":
        cw = (r["head_ratio"] + 2 * r["tail_ratio"]) * (1 << n)
        assert cw.denominator == 1, ("nonintegral cW", n)
        d["cW"] = int(cw)
        d["lam"] = r["head_lambda"] + 2 * r["tail_lambda"] + 3
        d["omega"] = v2(d["lam"])
    return d


def ledger_walk(cal, x, T, ceiling, label, canonical, limit=100000):
    """Exact walk with full record ledger. Returns trace + identity check results."""
    G = 0
    rows = []
    gates = []
    peak_j = v2(x)          # run peak parameter
    peak_G = 0              # Gamma at the run peak (peak is the run's first chain)
    R0 = peak_j
    maxrec = -1
    ok = True
    fails = []
    for _ in range(limit):
        if x == 0 or x < 0:
            break
        j = v2(x)
        if j is None or j + G >= ceiling:
            break
        R = j + G
        if R > maxrec:
            maxrec = R
        if j <= 4:
            rows.append(dict(j=j, G=G, R=R, kind="end"))
            break
        cr = read_cross(cal, j - 1)
        kind = cr["kind"] if cr["odd"] else "e"
        rows.append(dict(j=j, G=G, R=R, kind=kind))
        if not cr["odd"]:
            break
        # exact step
        if cr["kind"] == "a":
            k = cr["tau"] // 2
            xn = 2 * T + 6 * k - x // 2
            eps = 0
        else:
            xn = cr["cW"] * (x >> j) + cr["lam"]
            eps = cr["eps"]
        Tn = T + 3 + 3 * cr["tau"]
        jn = v2(xn)
        Gn = G + 1 + eps
        Rn = (jn + Gn) if jn is not None else None
        if jn is None:
            # NT gate with x' = 0 (virtual resonance): walk undefined beyond here
            gates.append(dict(j=j, jp=None, G_before=G, R=R, R_after=None,
                              climb=None, y=peak_j, toll=G - peak_G, paid=None,
                              R_after_minus_peak=None, zero=True))
            rows.append(dict(j=j, G=G, R=R, kind="zero"))
            break
        # ledger identities
        drop = R - Rn
        if cr["kind"] == "a" and jn >= j:
            # NT gate (p = j-1): j' >= j
            climb = Rn - R
            gates.append(dict(j=j, jp=jn, G_before=G, R=R, R_after=Rn, climb=climb,
                              y=peak_j, toll=G - peak_G,
                              slack0=R0 - (peak_j + peak_G),
                              paid=bool(jn <= peak_j - (G - peak_G) - 1),
                              paid0=bool(Rn <= R0),
                              R_after_minus_peak=Rn - (peak_j + peak_G)))
            if Rn != jn + G + 1:
                fails.append((label, "gate R_after", j, jn, Rn))
            if Rn - (peak_j + peak_G) != jn + 1 + (G - peak_G) - peak_j:
                fails.append((label, "L3 identity", j, jn))
            peak_j, peak_G = jn, Gn
        else:
            if cr["kind"] == "a":
                exp_drop = j - jn - 1
            else:
                exp_drop = j - jn - 1 - eps
            if cr["kind"] == "a" and jn == j - 1:
                if drop != 0:
                    fails.append((label, "one-step drop", j, jn, drop))
            elif drop < 1:
                fails.append((label, "run drop>=1", j, jn, drop))
            if drop != exp_drop:
                fails.append((label, "L1 exact drop", j, jn, drop, exp_drop))
        x, T, G = xn, Tn, Gn
    real_gates = [g for g in gates if not g.get("zero")]
    all_paid0 = all(g["paid0"] for g in real_gates)
    verdict_R0 = maxrec <= R0
    if real_gates and all_paid0 != verdict_R0:
        fails.append((label, "L4 paid0<=>maxrec<=R0", all_paid0, verdict_R0))
    # maxrec is attained either at the start or right after a gate
    maxgate = max((g["R_after"] for g in real_gates), default=None)
    if real_gates and max(maxrec, maxgate) != maxrec and maxgate is not None:
        fails.append((label, "L4b maxrec at gate", maxrec, maxgate))
    return dict(label=label, canonical=canonical, R0=R0, maxrec=maxrec,
                n_chains=len(rows), gates=gates, all_paid0=all_paid0,
                word=[r["j"] for r in rows], status="ok"), fails


def main():
    t0 = time.time()
    cal = Calendar(512)
    walks = []
    fails = []

    # 1. tie->tie refutation witness (synthetic): (j_p, D_p) = (73515, 98094), u = 1
    j0, D0 = 73515, 98094
    x = 1 << j0
    w, f = ledger_walk(cal, x, x + D0, j0 + 60, "witness_73515_98094", False)
    walks.append(w); fails += f

    # 2. the 36 bad-class representatives (accepted [B] states)
    bad = {5: [5, 21, -27, -11],
           8: [58, 186, -198, -70],
           12: [1012, 3060, -3084, -1036],
           14: [4081, 12273, -12303, -4111],
           17: [32702, 32750, 98238, 98286, -98370, -98332, -32834, -32786],
           22: [1048552, 3145704, 5242856, 7340008],
           24: [4194277, 12582885, 20971493, 29360101],
           27: [33554402, 100663266, 167772130, 234880994]}
    for j in sorted(bad):
        for delta in bad[j]:
            x = 1 << j
            w, f = ledger_walk(cal, x, x + delta, j + 60,
                               "bad_%d_%d" % (j, delta), True)
            walks.append(w); fails += f

    # 3. O2 family at (5,5): u = (2^(m-4)-1)/3, even m >= 6 (synthetic)
    for m in (6, 8, 10, 12, 16, 24, 32, 64):
        u = ((1 << (m - 4)) - 1) // 3
        x = 32 * u
        w, f = ledger_walk(cal, x, x + 5, m + 60, "O2_m%d" % m, False)
        walks.append(w); fails += f

    n_gates = sum(len(w["gates"]) for w in walks)
    n_paid = sum(1 for w in walks for g in w["gates"] if g.get("paid"))
    n_paid0 = sum(1 for w in walks for g in w["gates"] if g.get("paid0"))
    out = dict(
        status="PASS" if not fails else "FAIL",
        scope=("Record-budget ledger identities L1-L4 on exact walks: "
               "tie->tie witness (synthetic), 36 bad-class representatives "
               "(canonical [B] states), O2 family (synthetic). Canonical crossings "
               "from Calendar(512). Not a global EXT proof; K_clock unchanged."),
        identities={"L1": "within-run per-step record drop = j-j'-1-eps, >=1 "
                          "(one-step descent: =0)",
                    "L2": "NT gate record climb = j'-j+1 (j=5 tie: m-4)",
                    "L3": "R_after - R_peak = j' + 1 + toll - y; run-paid <=> "
                          "j' <= y-toll-1; global-paid <=> R_after <= R0",
                    "L4": "all gates globally-paid <=> maxrec <= R0; maxrec is "
                          "attained at the start or immediately after a gate"},
        counts=dict(walks=len(walks), gates=n_gates, run_paid=n_paid,
                    globally_paid=n_paid0, failures=len(fails)),
        maxrec_over_R0={w["label"]: w["maxrec"] - w["R0"] for w in walks},
        unpaid_gates=[dict(label=w["label"], **g) for w in walks for g in w["gates"]
                      if not g["paid"]],
        walks=walks,
        failures=fails[:50],
        timing=round(time.time() - t0, 2),
    )
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("status", "counts",
                                          "maxrec_over_R0", "timing")}, indent=1))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
