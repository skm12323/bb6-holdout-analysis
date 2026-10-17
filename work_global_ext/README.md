# EXT 攻关：四条路径的部分结果

2026-10-17，Claude Opus 5.5。详见 `PROOF_EXT.md`。已通过三方审查（1 攻击 + 2 盲审），记录在其 §8，
审查原文在 `reviews/claude_ext_*.md`。**EXT 本身仍未证明。**

四条路径（报告和脚本在 `route_a` … `route_d`）：
- a：全层塔闭合。结论是否定的：任何生成器型有限证书都不能闭合所有层（定理 O）。但用精确的 Ψ 族
  重做了第 4 层（0 失败），得到定理 S 与推论 4：**EXT 对所有 J < K″ 成立**，原机器的不停机范围
  从 2^{K′} 推进到 2^{K″}，其中 K″ = 2^{K′/2−2}。
- b：exit 长度上界。没有证出 LIN-EXIT，但证明了只有“非下降步”消耗预算（定理 L′，ND-EXIT ⇒ EXT），
  并给出了 β-only 归约（引理 BR）。
- c：反例与结构。J ≤ 10^8 的全部 S(J) 都无 tie，exit 最多 3 条链。证明了路线 a（X(J−1) 为 a 型）
  无条件闭合（定理 RA，不需要 NT 或 EXT），路线 b/c 是实际 epoch 的精确平移拷贝（命题 RB）。
- d：容忍 tie。EXT 可以弱化为 EXT\*：只需排除“精确 tie”，“过度 tie”无害（定理 U\*）。精确 tie 是
  真正的障碍：可解时存在无穷多个 w 让 E(w,J) 停机。

合并后的剩余命题（PROOF_EXT §6）：对所有 J ≥ K″，若 X(J−1) 为 b/c 型且首个参数或被拷贝的 epoch
≥ K′，则 S\*(J) 没有精确 tie。由此即可推出 #1 永不停机。

    python -B work_global_ext/route_a/gen.py 4 4          # 第 4 层证书，约 8 分钟
    python -B work_global_ext/route_c/check_calendar.py   # 引理 K / 定理 RA 检查
    python -B work_global_ext/route_b/e8_budget.py        # L′ / L″ 不等式
