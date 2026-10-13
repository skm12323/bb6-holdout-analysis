2. with simple errors

1. **Minor transcription error.** EL §5’s displayed “27 a-step pairs” formula describes 29 pairs. The actual 27 omit \((4,3)\) and \((20,2)\). I independently recovered those 27. This does not invalidate Theorem D; both extra shifted entries also terminate safely.

2. **Bounds and earlier-epoch dependence.** Put \(n=J-1\). Route a gives \(j_1=v_2(3\tau(n)+2)\); routes b/c give \(j_1\le\log_2(6\tau(n)+5)\). Therefore (C1) implies
   \[
   j_1\le\log_2(6(J-1)^2+5)<10^6.
   \]
   For integer \(J<2^{499998}\), the sharper bound is \(j_1\le999998\). A route-c crossing is a type-a return in an earlier W-epoch. Its fire time satisfies \(s_0''\le\tau(n)\le n^2\), hence
   \[
   J''\le\log_2(3(J-1)^2+4)\le999997.
   \]
   Since \(n<\rho\), that epoch precedes the current fire, and its parameter lies in the certified level-0 range. No circular dependence occurs.

3. **The \(d_4\) dependency is valid.** Since \(d_t=\sum_{q<t}(1+\tau(j_q-1))\), the first call uses (C1), while the next three specifically use the stronger finite-table bound \(\tau(n)\le n\). Thus
   \[
   d_4\le4+(J-1)^2+3\cdot10^6\le2J^2.
   \]
   At \(J=10^6\), the first bound is \(1{,}000{,}001{,}000{,}005\). Together with \(\Gamma_t\le25+(J-1)/4\), this establishes the size margin. At \(J=10^6\), \(\log_2(12J^2)=43.44810<749975=3J/4-25\).

4. **Full requested coverage achieved.** Independent exact F computation reached \(X(1{,}000{,}000)\) in 892,138 steps: all S1/S2 checks passed, \(\tau(n)\le n\), maximum \(\epsilon=7\). A separate unscaled computation matched all crossings through \(n=20{,}000\). Every \((j,2)\), \((j,0)\), \(1\le j<10^6\), plus all 27 route-c entries passed with no NT failure and at most three further chains. Distribution:
   \[
   \{0:756803,\;1:1148292,\;2:94874,\;3:56\}.
   \]
   Example: \((6131,2)\to(14,1)\to(5,2)\to(1,1)\). Hence \(r\le4\).

5. **Lemma T passed.** All 669,099 symbolic exit chains for \(2\le J<10^6\) satisfied \(v_2(\alpha_x)=J-\Gamma_t\), \(1\le\beta_x\le6d_t-1\), and strict valuation separation. Maximum \(\Gamma=6\); maximum exit \(j=21\). For \(J=14\), the exits have \((v_2\alpha_x,\beta_x,d_t,\Gamma_t)=(13,32,11,1)\), then \((12,58,14,2)\). The non-strict size condition suffices because \(\beta_x\le6d_t-1<2^{J-\Gamma_t}\). The proposed equality boundary itself is impossible for positive integer \(d_t\): \(6d_t\) is divisible by 3.

6. **Corollary E’s arithmetic is correct.** The strict horizon gives \(3s+4<2^{T_1}\), hence \(J<T_1\) at every fire. At the endpoint, equality gives \(J=T_1\). The stated deficit bound \(42.5+2.5\log_2 i\) also checks. I did not recompute the larger \(10^8\) V2 base. All runs stayed below 7.2 minutes. [Saved audit](D:/math_cc_astra/aud2/AUDIT.md).