1. all correct

1. Independently computed all **1,000,000 crossing records**, using the exact formal pair map through **892,136 steps**. Exact coefficient compression agreed with uncompressed bigint evolution for 20,000 steps. Both mass identities held throughout. The requested rows `(n, τ, ε, type, head)` are:
   - `(16,12,0,a,(65536,37))`
   - `(4,2,0,a,(16,7))`
   - `(5,2,1,b,(16,7))`, partner `(16,0)`
   - `(0,0,0,a,(1,1))`

2. Independently regenerated the exit automaton and a-transition output sets: **|A0|=27**, **|A1|=46**, exactly as claimed.

3. COVER contains **68 distinct specific entries**, retained alongside the five any-j families, giving **5,000,063 entries**. Every entry was run. The further-chain distribution is exactly:
   `{0:1892003, 1:2917464, 2:190537, 3:56, 4:3}`.

4. The complete NT-failure list is **(244875,−1), (538715,−1), (832554,−1)**. Each follows `entry → (17,−2) → (5,5)`. No other NT failures occurred.

5. Separate full bigint evolution verified **300 synthetic mass-compatible states**, including **150 with σ=18** and z values exceeding **2^8192**. Every state produced top-level parameters **17,5,6,1** and closed in exactly **21 steps**. Minimum top-level margins were **1,12,10,13**; the minimum over all chains, including inner calls, was **1**.

Independent [Python implementation](D:/math_cc_astra/aud3/blind_audit.py), [results](D:/math_cc_astra/aud3/audit_output.txt), and [complete crossing table](D:/math_cc_astra/aud3/crossings.csv) are saved locally. No existing Python, JSON, or logs under `D:\math_cc` were accessed.