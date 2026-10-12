2. with fixable gaps

The conditional strategy may be repairable, but §4 does **not** presently prove Theorem R. In particular, clean re-entry requires a substantive additional lemma.

1. **(M), literally required at every chain, is false already at the first chain.** Starting from the universal level,
   \[
   (U+1;U,2U,\ldots)\to(4U+4;4U,8U,\ldots)
   \to(16U+7;16U,32U,\ldots).
   \]
   Here \(s=2\), \(x=48U+10\), and
   \[
   v_2(c_x)=4<\log_2(17).
   \]
   The chain is nevertheless margin-safe: \(v_2(\lambda_x)=1<4\). Repair: require actual margin-safety on a finite prefix and (M) afterward. A verified safe prefix does not establish literal (M) on that prefix.

2. **The small parts do not follow the ordinary top map.** Continuing the preceding calculation gives
   \[
   (24U+6;40U+4,64U,\ldots)
   \to(128U+13;128U,256U,\ldots).
   \]
   At \(s=4\), \(x=384U+16\), so the full chain has \(j=4\) and \(u=24U+1>1\). But its small-part list begins \((13;0,0,\ldots)\), whose ordinary top map **halts**, because \(\lambda_x=16\).

   A valid replacement is a **formal closed-form update** that allows \(\lambda_u=1\) and still emits the prescribed head and stack. This is a different map, requiring its own definition and verification. The initial step also needs separate treatment: \(c_A=1\), so initial parity is not determined by \(\lambda_A=1\).

3. **The local margin calculation is sound, but the full simulation invariant is unstated.** With positive integral components and \(j=v_2(\lambda_x)<v_2(c_x)\),
   \[
   u=(c_x/2^j)U+\lambda_x/2^j\ge2U+1.
   \]
   Thus \(u\ge3\) for positive odd \(U\). At intermediate chain stages,
   \[
   m_t+3=2^{j-1-t}u;
   \]
   consequently every required push has \(m_t\ge3\), and the final \(m=u-3\) is nonnegative and even. This supplies the missing inequality-test justification.

   However, induction must also establish integral components, the parity invariant, and identical stack lengths. Merely saying operations add and halve dyadic rationals does not establish these properties. Also, \(u\ge2U+1\) alone does not imply the stated \(u\ge7U/3\) for \(U>3\).

4. **The crossing classification omits an original-entry partner.** At the crossing of \(E_1\), the initial queue is \([E_0,E_1,\ldots]\); its partner \(E_0\) is not pushed material. The same issue occurs whenever one step first reads two consecutive original entries. Allow the partner \(Y\) to be either pushed or original, and specify the consumed-index convention.

   The mass identities are valid with this bookkeeping: sum over the head and pushed material, excluding the untouched original suffix. Under the repaired formal update, \(\sum\lambda=3s+1\), hence \(\lambda_x\le6s+5\). The infinite queue itself cannot be included in either finite sum.

5. **§4.5’s “iff” is false as valuation algebra.** Write \(h=\rho-j'>0\), \(t=\lambda_{u'}\) odd, and suppose \(v_2(c')=v_2(\lambda')=r\). A tie only implies
   \[
   v_2(c't+\lambda')\ge r+1;
   \]
   it need not reach the scale valuation \(r+h\). For example, \(c'=\lambda'=4\), \(t=1\), \(h=3\) gives small valuation \(3\), scale valuation \(5\): a tie **with a safe U-margin**. This disproves the unrestricted algebraic equivalence; reachability restrictions would need separate proof.

   The valid implication is “unequal valuations imply U-margin.” Identifying the sub-process with the universal process also applies only before its first substituted boundary entry is read, not throughout a mixed exit.

6. **Progress does not supply the claimed clean re-entry.** Proposition 1 assumes clean re-entry; §4.1 classifies a boundary crossing. Neither proves that pushed material eventually disappears. Passing every original index permits, logically, successive crossings with a surviving pushed partner. Excluding such behavior requires a return lemma.

   Likewise, queue determinism transfers a finite level to the universal walk only until the substituted \(D_h\) is read. Subsequent behavior needs an embedding or a separate uniform argument. Bounds on the universal walk cannot simply be assigned to every modified-tail process.

   Therefore \(dk\ge1\), \(dp\ge2\), and \(k_\rho=s_\rho/2\) remain valid **conditional on the relevant clean fires**, not established consequences of the cited crossing lemma. The identity alone supplies no polynomial bound. Moreover, \(I(\rho)\) is not explicitly defined in the supplied target, preventing a complete audit of that assertion.

For Task 2, the most promising approach is a **tagged formal small-part walk with dyadic coefficient certificates**, rather than a finite catalogue of coefficient shapes.

**Proved algebraic facts.** Coefficient updates use positive sums and binary divisions. Thus
\[
v_2(a+b)\ge\min(v_2(a),v_2(b)),
\]
and division by \(2^j\) loses exactly \(j\) valuation units. At a clean boundary, conservation resets the head coefficient to \(2^i\). These are natural reset points for a potential measuring valuation loss since the last clean boundary.

**Candidate invariant, conjectural.** Maintain a stack of unresolved cascades, assigning each frame a division debt. Seek a bound
\[
i-v_2(c_x)\le C+\text{pointer advance since reset}
+\sum_{\text{active frames}}(j_{\text{frame}}+1).
\]
Positive addition cannot worsen the minimum valuation; the difficult obligations are bounding pointer advance and proving frames return, including exits inside exits. Binary carries should be retained: tracking individual original contributions without regrouping can give excessively pessimistic bounds.

A useful target is strict descent of nested parameters, \(j_{\rm child}<j_{\rm parent}\), together with bounded branching and a return certificate. Stronger contraction would support (M1); strict descent alone may yield quadratic accumulated debt in the outer parameter.

**Relax (M1) initially.** With (M2), even
\[
\Delta_x=O((\log i)^2)
\]
suffices for eventual (M). Proving the sharper logarithmic deficit is unnecessary for non-halting.

The complete tagged small-part **history** determines coefficient updates, so reduction to that history is plausible. The current untagged λ-list alone discards essential provenance and boundary information. No such reduction is proved here.

Finally, a global bound \(s\le\operatorname{poly}(i)\), valid at every state of an infinite safe walk, already implies progress. A bound checked only at crossings does not exclude an infinite stall between them.