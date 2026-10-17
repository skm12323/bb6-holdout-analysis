# endgame 就是 J=v 的符号 exit

2026-10-17，Claude Opus 5.5。详见 `PROOF_EGX.md`；已通过三方审查（攻击员复核 closed in all states），记录在其 §9。

关键观察：有限 excursion E(w,v) 的 endgame（从 X(v−1) 起，缺陷项 (2^{v−1},−1)，之后补零），在顶层上与
PROOF_M 引理 6.1 的符号 exit S(J)（J=v）逐对相同，只需把 (c,λ) 对应为 (α,β)、U 对应为 λ_u。
`verify_m.sym_exit` 的初值 `u=(1,0); D=(2^{J−1},−1)` 正是缺陷项。

由此：
- endgame 安全 ⇔ S(v) 无 tie；所以已审查的塔式证书（V4、EL 定理 D、PROOF_RESCUE §4、TIE2）
  直接给出**原机器在前 2^{K′}−2 个顶层步内不停机**（此前原机器只到 2^2001−2）。
- **单一开放假设 EXT**：对所有 J ≥ K′，S(J) 无 tie。EXT ⇒ F 永远有定义且 #1 永不停机，
  不再需要 SQRT-EXIT、EG-LEN 或 C2。EG-LEN ⇒ EXT，EXT ⇒（实际 fire 上的）SQRT-EXIT。
- 线性 exit 长度界 LIN-EXIT（≤ J/(3log₂J) 条链）⇒ EXT；S(J) 的前 ⌊J/(3log₂J)⌋+1 条链总是无 tie。

EXT 本身仍未证明，它与 NT、EL_J 是同一个算术核心。

    python -B work_global_egx/verify_egx.py 30000    # 约 4 秒；100000 约 20 秒
