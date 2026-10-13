2. with simple errors

1. **Crossing data regenerated independently:** all \(X(n)\), \(0\le n<10^6\); 892,136 F steps, 334,550 chains, maximum \(\varepsilon=7\), minimum actual chain margin **3**. There are 326,638 top-level chains before pointer \(10^6\); including its boundary fire gives the stated **326,639**.

2. **LEVEL 2 matches COVER:** raw \(|A_0|=27,\ |A_1|=46\); 68 specific entries reduce to 64 modulo \(2^j\). Total **5,000,059**, versus **5,000,063** before deduplication. Counts for 0–4 further chains:
   **(1,891,999; 2,917,464; 190,537; 56; 3)**.
   Deduplication removes four terminal entries. Exactly the three stated ties occur.

3. **LEVEL 3 entry and termination counts match:** **7,000,101** entries, comprising seven any-j families, 102 specific pairs, and six extended records. Counts for 0–4 further chains:
   **(2,648,803; 4,065,716; 273,657; 11,922; 3)**.
   A-output counts also match: **99 specific pairs and 35,801 extended records**, retaining extended-input provenance.

4. **NT failures are overstated by six:** the correct count is **13,943**, independently obtained from both automata: 13,940 from \(\theta=-2\), three from \(\theta=-1\). All occur at **\((5,\Theta\equiv5\pmod{32})\)**. The claimed 13,949 equals these failures plus the six extended inputs, which are NT-safe: three project to \((5,4)\), three to \((6,45)\); each terminates after one further chain.

5. **Every actual tie resolves with positive margins at every chain.** Zero unresolved cases, zero case-split failures, and zero branches required. Global minimum **\(h=1\)**; minimum immediately after a non-descending step **\(h=10\)**. The three LEVEL 2 tie paths have conservative margins **(1,2,13,11,12)**. Maximum continuation length is **four chains**. Non-descending outputs have \(j'\in\{5,\ldots,19\}\) and satisfy \(3\Theta\equiv10\pmod{2^{j'}}\).

6. Implemented exact a-identities, b/c copying, and exhaustive unknown-bit splits; checked **41,664** concrete bit completions, including **111** zero-residue states. A separate dense-integer implementation matched **20,001 crossings** and both mass identities. No forbidden scripts, JSON, or logs were accessed. The error is accounting only; checked termination and positivity survive. [Verifier](D:/math_cc_astra/aud5/audit.py) · [Audit report](D:/math_cc_astra/aud5/AUDIT.md)