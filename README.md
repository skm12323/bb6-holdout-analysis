# BB(6) Holdout 停机判定实验（多 Agent 审查流水线）

本仓库保存一次 BB(6) holdout 机器停机判定实验的整理结果。工作由多个 AI 模型在用户指导下协作完成（见文末"作者"）。统筹员的工作方式是：派发多条相互正交的分析路径，按 A/B/C 三级给命题定级并执行装配门禁，再用"1 名攻击员 + 2 名互盲复算员"做三方审查。用户负责提出任务与关键决策。

> **致谢与相关工作：** 本次工作是受 [CyclingCycloid/bb6-holdout-research](https://github.com/CyclingCycloid/bb6-holdout-research) 的作者建议进行的。该仓库对本仓库中的 #1（`1RB1LA_0RC0RD_…`，其中称为 M1）和 #2（`1RB1RA_1LC0RC_---0LD_…`，其中称为 cm2）有更深入的结果，并且据其作者告知已完成等价性方面的证明。本仓库的结果是在没有参考该仓库内容的情况下独立得出的，**不主张优先权**；凡与该仓库重叠之处，请以该仓库为准。本仓库没有核对该仓库的论证。

## 结论速览

在已分析的机器中，**尚无一台得到全局停机或不停机的判定**。#1 已得到最强的有限范围结论（原机器在前 2^K′−2 个顶层步内不停机，通用轨道在 s < (2^K′−4)/3、K′ = 2^(2^(2^499997−3)−2) 内不停机，已审查），全局证明归结为"任意深层 2-adic 平局控制"这一开放问题。截至 2026-10-17，经已审查的时钟界（work_global_clock）与终局引理 E1–E5（work_global_endgame），#1 的全局不停机曾归约为两个开放命题 SQRT-EXIT 与 EG-LEN；同日的 work_global_egx（已审查）证明 endgame 就是 J=v 的符号 exit，于是**原机器在前 2^K′−2 个顶层步内不停机**，且全局不停机只剩**一个开放命题 EXT**（对所有 J ≥ K′，符号 exit S(J) 无 tie），SQRT-EXIT 与总装配的基础缺口不再需要。同日的 work_global_ext（已审查）把 EXT 的成立范围推进到 J < K″ = 2^{K′/2−2}（**原机器在前 2^{K″}−2 个顶层步内不停机**），证明 a 型入口无条件无 tie、过度 tie 无害（EXT 可弱化为 EXT\*，只需排除精确 tie），剩余开放命题收缩为：J ≥ K″ 且 X(J−1) 为深层 b/c 型时 S\*(J) 无精确 tie。下列每条"已审查"结论都通过了三方审查。

| 机器 | 已审查的结论 | 文档 |
|---|---|---|
| `1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---` 及其三台兄弟机器 | 归约到块列表映射 M；停机 ⇔ 某次左端到达值 u₀ ∈ {2ᵏ−2}；四台机器停机与否互相等价 | `REPORT_1RB0LE_0RC1RB.md`、`work_q4/`、`work_q6/`、`work_u1/` |
| #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` | 归约到栈映射：停机 ⇔ 某步 A 为奇数且 A+2b+3 是 2 的幂；顶层步 n < 2²⁰⁰¹−2 内不停机；形式化对映射 F 与条件定理 R（work_g6）、定理 M（work_m）；**通用轨道 F 在 s < (2^K′−4)/3（K′ = 2^(2^(2^499997−3)−2)）内有定义且不停机**（work_el、work_tie、work_tie2）。未证明：全局永不停机。两条独立的条件化路线——(NT) 路线（work_nt + Astra 研究，发现 NT 可能不成立）与 GLM 的 work_r10 证明树（以测量常数 EL 或未证的 PIN、以及平局深度无界的结尾阶段为前提）——归结为同一核心：任意深层 2-adic 平局控制（类 Collatz）。R9 的完整证明宣称已撤回。严格下降目标 DL 已被反驳（work_g2_obstruction：实际 r=6 epoch）。**2026-10-17 新增（已审查）：** 无条件时钟界 τ(n) ≤ n·P(n) = O(n log² n)，使"F 永远有定义" ⇐ SQRT-EXIT（每个 epoch 在 ⌊√ρ⌋+1 条退出链内结束）；精确规范日历（可查询到约 2^4096）；终局引理 E1–E5，把终局归约为 EG-LEN（任意终局前缀 Σj < 3(v−1)/4）。**work_global_egx（已审查）：** endgame(v) 等于 J=v 的符号 exit S(v)，原机器在前 2^K′−2 个顶层步内不停机；EXT（S(J) 对 J ≥ K′ 无 tie）⇒ #1 永不停机。**work_global_ext（已审查）：** EXT 对 J < K″ 成立（原机器 2^{K″} 有限范围）；a 型入口无条件闭合（定理 RA）；EXT 可弱化为 EXT\*（定理 U\*）；只有非下降步消耗预算（定理 L′）；有限塔证书无法闭合所有层（定理 O）。当前唯一开放：J ≥ K″ 的深层 b/c 型入口无精确 tie | `CHECKPOINT_1RB1LA_0RC0RD.md`、`work_r1/`、`work_r4/`、`work_g6/`、`work_m/`、`work_el/`、`work_nt/`、`work_r10/ASSEMBLY.md` |
| #2 `1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB` | 归约到 Σ 栈机；定理 H | `REPORT_1RB1RA_1LC0RC.md`、`work_s1/`、`work_s3/` |
| `1RB1LE_1LB1LC_1RD0LE_---0RB_1RF1LA_0RA0RD` | 停机 ⇔ 轨道到达 (0;10,…) | `REPORT_1RB1LE_1LB1LC.md`、`work_t1/` |
| `1RB1LC_1RC1LB_1LD0RB_0LE1RD_---0LF_0LA1LF` | 无（各路径都没走通） | `CHECKPOINT_1RB1LC_1RC1LB.md` |

总报告见 [SUMMARY.md](SUMMARY.md)，里面有文件索引、开放问题和与社区结果的对比。

### 最新进展（2026-10-18，已通过三方审查）

[work_global_clock_horizon](work_global_clock_horizon/README.md) 将已审查的近线性时钟界与浅层入口定理组合，推导出更大的有限截止值 `K_clock = floor(2^K′ / (64(K′)^2))`（审查后由 32 改为 64，并补充保证后续链参数 < K′ 的 Lemma MASS），对应原机器前 `2^K_clock−2` 个顶层步不停机。整数界及有限真实轨道来源检查通过；**已通过三方审查（见 reviews/global_clock_horizon_closure_review_record.md），已接受的有限范围由 K″ 提高到 K_clock**。全局不停机与第 5 层证书仍未完成。

后续 [work_global_closure_attempt](work_global_closure_attempt/README.md) 将最小反例的相关参数上界压到约 `log2 J + 2log2log2 J`，并推导出一个全局闭合的充分条件：全尺度生产性返回词长度不超过 `2^ceil(Q/2)`。**该长度界尚未证明**（其余部分作为条件性/局部结果已接受）。另构造了含 8 个连续生产性 a-output 入口的安全局部路径，其起始 fire 约束不成立（相对于精确 true-fire 投影；非规范祖先未排除）；它不构成原轨道反例。

同日继续：扩大到 64 个来源参数的精确搜索发现长度 11 的安全局部纯 a 路径，而满足 fire 起点约束的纯 a 词最多长 2（仅限该参数集合）。[相位起点过滤引理](work_global_closure_attempt/PROOF_ORIGIN_FILTER.md) 给出所有词的精确初始相位同余；原九项词需要至少 `2^122438-3244676` 的实 fire 平移量。尚无任意混合历史的平移量或总长度上界，全局证明仍开放。

## 目录结构

2026-10-18（2026-10-19 已通过三方审查）：[work_ext_roots](work_ext_roots/README.md) 直接保留 EXT 的真实入口条件（b 型 `Theta=x`，c 型 `Theta-x=-lambda_Y`），并给出固定首个 tie 候选词的有限外层指标界：若 M 为累计块损失加末参数，则 b 型 `J<=M+2`，最小反例归纳下 c 型 `J<=2M`。所选混合来源的零相位差搜索与入口检查通过；**候选词族仍无全局界，EXT 未闭合**。最小反例归纳下已排除 ε=3、5 的 c 源及全部 A 起始源 epoch（A-SOURCE）；剩余前沿为 b/c 起始源 epoch 中 ε≥7 的 c 源（含 MINUS/PLUS 族）与全部外层 b 型入口。

- `REPORT_*.md`、`CHECKPOINT_*.md`：每台机器的仲裁记录与阶段性检查点
- `work_*/`：主定理文档（`RULES.md`、`LEMMAS.md`、`PROOF.md`、`EQUIV.md`）与对应的验证脚本 `verify_*.py`
- `work_r5/`、`work_r6/`、`work_r7/`：#1 全局不停机的三次尝试，**未经审查**
- `work_r8/`：#1 的组合式闭合尝试（模板检查 + 谱系封闭）；`work_r9/`：永不停机定理的宣称与锚点驱动（`THEOREM.md`、`verify_r9.py`）；`scratch/`：研究草稿与子代理报告（agentB/C/D/E/G、审查报告），部分未经审查
- `work_g6/`、`work_m/`、`work_el/`：#1 的条件定理 R、定理 M、退出自动机与有限范围定理（已审查）；`work_nt/`：(NT) 攻关（未审查）；`work_tie/`：救援宏与再推一层的有限范围（已审查）；`work_tie2/`：扩展自动机与第 3 层定理（已审查）；`work_tie_extension/`：Astra 的同层扩展（补充）；`work_g2/`：G2 部分结果（已审查）；`work_g2_obstruction/`：fire 谱与 DL 反驳（已审查）；`work_r10/`：GLM 的条件证明树与五方审查（`ASSEMBLY.md`）；`work_g2_*/`（13 份，GPT Astra）：两块返回恒等式、b/a 局部障碍等 G2 分支结果（已审查）；`work_global_*/`：全局路线笔记，其中 `work_global_core` 与 11 份 GPT Astra 笔记（clock、calendar、root_phase、rescue_ladder、period 等）已审查，`work_global_shadow`、`work_global_compression` 未审查；`work_claude_global/`：J=50148477 处的 r=3 退出与严格下降目标 DL（已审查，DL 后被反驳）；`work_global_clock/`：无条件时钟界与 SQRT-EXIT 归约（已审查）；`work_global_calendar_survey/`：深层退出的规范日历普查，r=4 首现于 m=6131（已审查，B 级证据）；`work_global_endgame/`：终局引理 E1–E5 与 EG-LEN 问题陈述（已审查）；`work_global_egx/`：endgame = 符号 exit、原机器 2^K′ 有限范围、单一归约 EXT（已审查）；`work_global_ext/`：EXT 四路攻关（Ψ 族第 4 层证书与 K″、定理 RA、EXT\*、ND-EXIT、定理 O），已审查；`work_global_clock_horizon/`：K_clock 有限范围（已审查）；`work_global_closure_attempt/`：条件闭合目标（已审查）；`work_ext_roots/`：最小 EXT 反例归纳、A-SOURCE（已审查）；`reviews/`：外部审查原文（GPT Astra / codex）
- `data/BB6_holdouts_815.txt`：bbchallenge 2026-09-24 版 holdout 清单
- `triage2/scan.txt`：815 台机器各跑 10⁶ 步的初筛数据

## 复现

验证脚本只需要 Python 3 标准库。在对应的 `work_*` 目录下运行，例如：

```bash
cd work_r4 && python verify_r4.py 60
cd work_r8 && python verify_r8.py 1000 300   # check1–6,约 2 分钟
cd work_r9 && python verify_r9.py            # 定理锚点,约 1 分钟
```

注意两处依赖：`verify_q6.py` 依赖 `work_q4`，`verify_s3.py` 依赖 `work_s1`，`verify_u1.py` 依赖 `work_q4`。

## 方法说明与局限

- 命题分级：**A** 为全局符号证明；**B** 为有限的机械穷举，或有限步模拟得到的起点引理；**C** 为数值与经验证据。C 级命题不进入定理。
- "已审查"指通过了攻击员加两名复算员的审查，审查员都是 AI Agent，**不等于同行评审**。
- 多处 A 级结论依赖机械证书，即符号执行程序的输出，例如 #1 的 Lemma E(v)（v ≤ 2000）。这些证书已由独立实现的程序复现。

## 作者

在用户指导下，由以下模型协作完成：

- Claude Opus 5.5（Anthropic）
- GLM 5.3
- GPT Astra（OpenAI）

具体分工见 commit 历史。
