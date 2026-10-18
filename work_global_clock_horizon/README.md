# 用更强时钟界扩大 EXT 的有限范围

2026-10-18；**已通过三方审查**（reviews/global_clock_horizon_closure_review_record.md）。

把已审查的近线性时钟界与现有浅层入口定理 S、a 型入口定理 RA
组合，可将参数截止值从 `K''=2^(K'/2-2)` 提高到

    K_clock = floor(2^K' / (64 (K')^2)).

（审查后由 32 改为 64，并加入 Lemma MASS，保证 Theorem S 的第 4 层证书所需的“后续链参数 < K'”范围条件。）

据此推导原机器前 `2^K_clock-2` 个顶层步不停机。证明与依赖审计
见 [PROOF_CLOCK_HORIZON.md](PROOF_CLOCK_HORIZON.md)。本结论已接受，已审查的有限范围由 K'' 提高到 K_clock；全局不停机仍开放，第 5 层证书也未闭合。

更精确的逐点判据为 `3(J-1)P(J-1)+4 < 2^K'`。关键是 type-c
必须约束被复制 epoch 的起始参数，而非仅约束当前链参数。

运行 `python -B work_global_clock_horizon/verify_clock_horizon.py` 可复现
整数界检查和有限真实轨道上的来源核对。无需第三方依赖。
