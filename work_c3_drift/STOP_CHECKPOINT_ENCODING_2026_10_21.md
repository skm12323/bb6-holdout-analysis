# Stopping checkpoint: optimal local phase encoding

2026-10-21. **UNREVIEWED; UNCOMMITTED.** Stopped at the completed phase-encoding node at the user's request. This is the latest resume pointer; earlier checkpoints remain historical records.

## Completed node

[OPTIMAL_PHASE_ENCODING.md](OPTIMAL_PHASE_ENCODING.md) and
`optimal_phase_encoding.py` give an exact minimum-cost local encoding
of a phase through m+1 bits, charging 2r+h(c) for reduced c=C/3^r.
Rank m supplies a complete finite search bound. The extra phase bit is
recorded explicitly.

`verify_optimal_phase_encoding.py` checked 8,190 low-phase classes for
m=1..12 with both extra bits. Independent full numerator enumeration
agreed on all 254 classes for m<=7. Results are saved in
`optimal_phase_encoding_checks.json`.

The counting bound shows that reserve m cannot encode every local phase
class at m=64. This is not a failure witness for a canonical reachable
source. Local re-encoding can discard higher phase bits, so affine and
family provenance must be retained for later bare ties.

## Preceding completed work

[EARLY_MIXED_SOURCE_CERTIFICATES.md](EARLY_MIXED_SOURCE_CERTIFICATES.md)
conditionally certifies the first floor(P/(3 floor(log2 P)+7))-4 odd-a
outputs for P>=512, allowing intervening b/c copies. It assumes the
stated smaller-root EXT and source conditions; it does not prove an
unbounded induction. Its finite verifier passed for 7,680 roots,
checking 2,571 a outputs and 2,571 copy drops. The observed histories
have at most two a outputs; the longer-prefix assertion is analytic.

[B_PREFIX_SOURCE_ENCODING.md](B_PREFIX_SOURCE_ENCODING.md) and
[BBBAA_COPY_CERTIFICATE.md](BBBAA_COPY_CERTIFICATE.md) supply conditional
source certificates for their specified families.
[UNBOUNDED_C_PARAMETER_IF_EXT.md](UNBOUNDED_C_PARAMETER_IF_EXT.md)
shows why a fixed universal bound on c-source parameters cannot be
the remaining strict-EXT argument.

## Remaining gap and possible resumption

Global EXT and global non-halting remain open. The accepted K_clock
horizon is unchanged. A possible next task, only after explicit user
continuation, is to relate the locally affordable phase classes to
actual affine source provenance beyond the certified early prefix,
retaining enough precision for subsequent ties. No claim of closure
for arbitrary interruptions or all source histories is made.

All research here remains unreviewed in the untracked `work_c3_drift/`
directory. At this stop, Git reports `main...origin/main [ahead 7]` and
`?? work_c3_drift/`. No commit or publication was made at this node.
