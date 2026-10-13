REDUCED — new sufficient residual: at every a-step input, the unfolded copy ancestry has at most three fire leaves. This remains unproved.

**1. A provable potential.** Work before the first NT failure, inside Theorem M’s induction. Define an integer \(L\), counting leaves with multiplicity in the unfolded ancestry tree:

\[
L=1\text{ at fires},\qquad L'=L\text{ at a-steps},\qquad
L'=L+L^W\text{ at b/c-steps}.
\]

Put \(q=2\tilde\theta-3\). The audited recurrences become

\[
q_{\rm fire}=-1,\qquad q'_a=-q,\qquad q'_{b/c}=q+q^W-1.
\]

Consequently, induction on the ancestry tree proves

\[
|q|\le 2L-1,\qquad 2-L\le\tilde\theta\le L+1.
\]

Thus the following **stronger, sufficient replacement for NT** works:

> **(A3)** Every chain followed by an a-step has \(L\le3\).

Indeed, A3 gives \(\tilde\theta\in[-1,4]\), so Lemma C excludes a first NT failure. Combined with the audited finite certificate and Theorem B, this closes Theorem M **conditionally on A3**.

This is a structural proof strategy, not a proof of A3. Unlike the signed representative, \(L\) only increases during copying; proving A3 requires a restriction on which ancestries can reach an a-step.

**2. Numerical tests and a realized negative value.** I reused the exact crossing table in `aud2`, propagated \(L\), and tested the certified automata:

| Tested family | Representatives observed | Largest \(L\) at an a-step input |
|---|---:|---:|
| Real epochs with fire position below \(10^6\) | \(\{0,1,2\}\) | 2 |
| All fire inputs \(2\le J<10^6\) | \([-1,3]\) | 2 |
| Theorem D’s level-1 entry families | \([-2,4]\) | 3 |

Level-1 paths can reach \(L=4\), but the tested occurrences terminate without another a-step. Thus bounding ancestry **at a-step inputs**, rather than everywhere, matters.

The stronger empirical conjecture \(\tilde\theta\in\{0,1,2\}\) on all real paths is **false**. Exact fire-increment arithmetic gives the first \(J=28\) fire at

\[
\rho=100296962,\qquad k=44739242.
\]

Its exit is
\[
(28,1)\xrightarrow b(6,0)\xrightarrow b(1,-1).
\]

I verified the position both by arithmetic-progression counting and independently by advancing all \(30{,}377{,}959\) preceding fires using the exact increments. The negative representative occurs at step \(89478508\). This disproves the smaller empirical invariant, **not** the requested interval \([-10,4]\).

Code and results: [ancestry tests](D:/math_cc_astra/nt/probe_ancestry.py), [independent check](D:/math_cc_astra/nt/check_first_negative.py), [level-1 results](D:/math_cc_astra/nt/level1_ancestry_results.json).

**3. Can drift be unbounded?** For consecutive b-steps, exactly

\[
\tilde\theta_m=\tilde\theta_0-m.
\]

The transition rules therefore permit arbitrarily large negative drift across arbitrarily large starting parameters. Strict descent bounds each individual chain’s length; it supplies no uniform bound over all epochs.

Earlier-time self-reference does not itself prevent this: every copied fire already has \(\tilde\theta^W=1\). Induction merely validates another subtraction of one. For c-copies, the ancestry potential measures the additional contribution precisely.

**Unbounded drift in actual F remains unproved.** Realizability requires correlated fire positions and parameters; arbitrary acyclic copy trees do not establish it.

**4. What arithmetic must exclude.** Define the partial map

\[
B(h)=1+v_2(3k_{h-2}+2)
\]

when \(h-2\) is a level-fire position. This is exactly the b-transition parameter map. The table confirms

\[
B(244875)=B(538715)=B(832554)=17.
\]

Any realized fire parameter \(J\) with \(B^3(J)=17\) produces

\[
(J,1)\xrightarrow{bbb}(17,-2)\xrightarrow a(5,5),
\]

followed by NT failure, since \(k_{16}=6\) and \(k_4=1\).

This yields a further **proved conditional obstruction**: NT is incompatible with every positive integer occurring as a level-fire parameter. Starting with a known fire of parameter \(17\), repeatedly take its position plus two; universal parameter occurrence would realize the three b-copies above.

Thus a proof of NT must establish genuine restrictions on the fire spectrum and its position–parameter correlations.

I obtained **no reduction to congruences at a fixed small set of k-indices**. The terminal indices \(16,4\) are already settled; the missing information concerns unbounded ancestral indices. Lemma K labels a fire’s valuation class but does not decide whether those linked fires occur.

No equivalence to a recognized open problem has been established. The concrete remaining strategy is A3, or a weaker signed-cancellation bound when \(L>3\); neither currently has a closed induction.