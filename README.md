# BB(6) Holdout 停机判定实验（多 Agent 审查流水线）

本仓库保存一次 BB(6) holdout 机器停机判定实验的整理结果。工作由多个 AI 模型在用户指导下协作完成（见文末"作者"）。统筹员的工作方式是：派发多条相互正交的分析路径，按 A/B/C 三级给命题定级并执行装配门禁，再用"1 名攻击员 + 2 名互盲复算员"做三方审查。用户负责提出任务与关键决策。

> **致谢与相关工作：** 本次工作是受 [CyclingCycloid/bb6-holdout-research](https://github.com/CyclingCycloid/bb6-holdout-research) 的作者建议进行的。该仓库对本仓库中的 #1（`1RB1LA_0RC0RD_…`，其中称为 M1）和 #2（`1RB1RA_1LC0RC_---0LD_…`，其中称为 cm2）有更深入的结果，并且据其作者告知已完成等价性方面的证明。本仓库的结果是在没有参考该仓库内容的情况下独立得出的，**不主张优先权**；凡与该仓库重叠之处，请以该仓库为准。本仓库没有核对该仓库的论证。

## 结论速览

**#1 从空白纸带出发永不停机。** 2026 年 11 月 22 日，仓库接受了这台六状态二符号图灵机的全局证明。新论证给出了任意尺度上的混合返回词长度界，结合此前已审查的机器归约，排除了符号退出过程在任何深度首次失去严格安全余量的可能。其余机器的阶段性结果见下表。

[中文论文（PDF，7 页）](output/pdf/holdout1-zh.pdf) · [LaTeX 源稿](output/pdf/holdout1-zh.tex) · [完整证明](work_mixed_bridge/PROOF.md) · [最终审查记录](reviews/final_mixed_bridge_review_record.md)

| 机器 | 已审查的结论 | 文档 |
|---|---|---|
| `1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---` 及其三台兄弟机器 | 归约到块列表映射 M；停机 ⇔ 某次左端到达值 u₀ ∈ {2ᵏ−2}；四台机器停机与否互相等价 | `REPORT_1RB0LE_0RC1RB.md`、`work_q4/`、`work_q6/`、`work_u1/` |
| #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` | **空白带上全局不停机。** 对每个深度 J，符号退出过程 S(J) 在所需源行已定义时均严格安全；定理 U 将此结论转回原机器。 | [小基例与全局归纳](work_mixed_bridge/SMALL_BASE.md) · [定理 U](work_global_egx/PROOF_EGX.md) |
| #2 `1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB` | 归约到 Σ 栈机；定理 H | `REPORT_1RB1RA_1LC0RC.md`、`work_s1/`、`work_s3/` |
| `1RB1LE_1LB1LC_1RD0LE_---0RB_1RF1LA_0RA0RD` | 停机 ⇔ 轨道到达 (0;10,…) | `REPORT_1RB1LE_1LB1LC.md`、`work_t1/` |
| `1RB1LC_1RC1LB_1LD0RB_0LE1RD_---0LF_0LA1LF` | 无（各路径都没走通） | `CHECKPOINT_1RB1LC_1RC1LB.md` |

早期各条研究路线的索引和阶段性结论见 [SUMMARY.md](SUMMARY.md)。#1 的完整进展按时间记录在[检查点](CHECKPOINT_1RB1LA_0RC0RD.md)中。

## #1 的证明思路

一次符号退出可以离开已经穷举的低链号区间，随后再返回。证明把相邻两次高链访问之间的整段路径合在一起，称为一座“桥”。前一座桥的终点就是后一座桥的起点，两者共享同一个时钟。消去这个时钟后得到一个整数：它能被一个很大的二次幂整除，绝对值却小于这个二次幂，因此只能为零。由此得到的等式迫使一个非负有理数在每次重访时至少减半，从而限制了重访次数。[桥接引理](work_mixed_bridge/PROOF.md#2-a-bridge-between-two-high-entries)

有限枚举表明，入口链号不超过 1023 时，连续生产性混合返回词最长为 6。桥接引理将其推广为：对每个整数 Q ≥ 64，若全部入口链号在 [5, Q] 内，则词长至多为 Q。另从原始配对轨道逐项验证 J = 1 到 1023 的符号退出，再从 J = 1024 开始强归纳，即可排除任意深度的首次平局。[有限证书与归纳](work_mixed_bridge/SMALL_BASE.md)

此前的有限步界、条件证明和已撤回路线均保留在仓库中。例如，2026 年 10 月的工作给出了近线性时钟界，将全局问题归约为混合返回词的长度控制，并分析了最小反例的入口条件。[有限时钟界](work_global_clock_horizon/README.md) · [条件归约](work_global_closure_attempt/PROOF_CLOSURE_TARGET.md) · [入口分析](work_ext_roots/README.md)

## 目录结构

- `REPORT_*.md`、`CHECKPOINT_*.md`：每台机器的仲裁记录与阶段性检查点
- `work_*/`：主定理文档（`RULES.md`、`LEMMAS.md`、`PROOF.md`、`EQUIV.md`）与对应的验证脚本 `verify_*.py`
- `work_r5/`、`work_r6/`、`work_r7/`：#1 全局不停机的三次尝试，**未经审查**
- `work_r8/`：#1 的组合式闭合尝试（模板检查 + 谱系封闭）；`work_r9/`：永不停机定理的旧宣称（已撤回）与锚点驱动（`THEOREM.md`、`verify_r9.py`）；`scratch/`：研究草稿与子代理报告（agentB/C/D/E/G、审查报告），部分未经审查
- `work_g6/`、`work_m/`、`work_el/`：#1 的条件定理 R、定理 M、退出自动机与有限范围定理（已审查）；`work_nt/`：(NT) 攻关（未审查）；`work_tie/`：救援宏与再推一层的有限范围（已审查）；`work_tie2/`：扩展自动机与第 3 层定理（已审查）；`work_tie_extension/`：Astra 的同层扩展（补充）；`work_g2/`：G2 部分结果（已审查）；`work_g2_obstruction/`：fire 谱与 DL 反驳（已审查）；`work_r10/`：GLM 的条件证明树与五方审查（`ASSEMBLY.md`）；`work_g2_*/`（13 份，GPT Astra）：两块返回恒等式、b/a 局部障碍等 G2 分支结果（已审查）；`work_global_*/`：全局路线笔记，其中 `work_global_core` 与 11 份 GPT Astra 笔记（clock、calendar、root_phase、rescue_ladder、period 等）已审查，`work_global_shadow`、`work_global_compression` 未审查；`work_claude_global/`：J=50148477 处的 r=3 退出与严格下降目标 DL（已审查，DL 后被反驳）；`work_global_clock/`：无条件时钟界与 SQRT-EXIT 归约（已审查）；`work_global_calendar_survey/`：深层退出的规范日历普查，r=4 首现于 m=6131（已审查，B 级证据）；`work_global_endgame/`：终局引理 E1–E5 与 EG-LEN 问题陈述（已审查）；`work_global_egx/`：endgame = 符号 exit、原机器 2^K′ 有限范围、单一归约 EXT（已审查）；`work_global_ext/`：EXT 四路攻关（Ψ 族第 4 层证书与 K″、定理 RA、EXT\*、ND-EXIT、定理 O），已审查；`work_global_clock_horizon/`：K_clock 有限范围（已审查）；`work_global_closure_attempt/`：条件闭合目标（已审查）；`work_ext_roots/`：最小 EXT 反例归纳、A-SOURCE（已审查）；`reviews/`：外部审查原文（GPT Astra / codex）
- `data/BB6_holdouts_815.txt`：bbchallenge 2026-09-24 版 holdout 清单
- `triage2/scan.txt`：815 台机器各跑 10⁶ 步的初筛数据

## 复现

在仓库根目录使用 Python 3 运行以下命令，均只需标准库：

```bash
python -B work_mixed_bridge/verify_source_prefix.py
python -B work_mixed_bridge/verify_bridge.py
python -B work_mixed_bridge/audit_bridge.py
```

第一项核对 1023 个源行与符号退出，根后有 0、1、2 条链的情形分别为 389、586、48 个。第二项枚举混合返回词：长度为 6 的有 504 个，长度为 7 的有 0 个。第三项检查桥接恒等式和尺度不等式。全尺度结论的归纳证明见论文第 5、6 节。

注意两处依赖：`verify_q6.py` 依赖 `work_q4`，`verify_s3.py` 依赖 `work_s1`，`verify_u1.py` 依赖 `work_q4`。

## 方法说明与局限

- 命题分级：**A** 为全局符号证明；**B** 为有限的机械穷举，或有限步模拟得到的起点引理；**C** 为数值与经验证据。C 级命题不进入定理。
- “已审查”指仓库内的模型审查。#1 的新增证明先经 GLM 小组审查和修补，最终由两名 Claude Opus 5.5 攻击员与两名 DeepSeek v4.1 flash 互盲复核员审查通过；底层机器归约沿用此前的审查结果。该论文尚未经外部同行评审。[GLM 审查与修补记录](reviews/gc_mixed_bridge_review_record.md) · [最终审查范围与结论](reviews/final_mixed_bridge_review_record.md)
- 多处 A 级结论依赖机械证书，即符号执行程序的输出，例如 #1 的 Lemma E(v)（v ≤ 2000）。这些证书已由独立实现的程序复现。

## 作者

在用户指导下，由以下模型协作完成：

- Claude Opus 5.5（Anthropic）
- GLM 5.3
- GPT Astra（OpenAI）

具体分工见 commit 历史。
