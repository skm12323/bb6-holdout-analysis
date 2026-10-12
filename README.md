# BB(6) Holdout 停机判定实验（多 Agent 审查流水线）

本仓库保存一次 BB(6) holdout 机器停机判定实验的整理结果。工作由 **Claude Opus 5.5**（Anthropic，经 Claude Code 运行）担任统筹员完成：派发多条相互正交的分析路径，按 A/B/C 三级给命题定级并执行装配门禁，再用"1 名攻击员 + 2 名互盲复算员"做三方审查。用户负责提出任务与关键决策。

> **致谢与相关工作：** 本次工作是受 [CyclingCycloid/bb6-holdout-research](https://github.com/CyclingCycloid/bb6-holdout-research) 的作者建议进行的。该仓库对本仓库中的 #1（`1RB1LA_0RC0RD_…`，其中称为 M1）和 #2（`1RB1RA_1LC0RC_---0LD_…`，其中称为 cm2）有更深入的结果，并且据其作者告知已完成等价性方面的证明。本仓库的结果是在没有参考该仓库内容的情况下独立得出的，**不主张优先权**；凡与该仓库重叠之处，请以该仓库为准。本仓库没有核对该仓库的论证。

## 结论速览

在已分析的机器中，**没有一台得到全局停机或不停机的判定**。下列每条"已审查"结论都通过了三方审查。

| 机器 | 已审查的结论 | 文档 |
|---|---|---|
| `1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---` 及其三台兄弟机器 | 归约到块列表映射 M；停机 ⇔ 某次左端到达值 u₀ ∈ {2ᵏ−2}；四台机器停机与否互相等价 | `REPORT_1RB0LE_0RC1RB.md`、`work_q4/`、`work_q6/`、`work_u1/` |
| #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` | 归约到栈映射；停机 ⇔ 某步 A 为奇数且 A+2b+3 是 2 的幂；**顶层步 n < 2²⁰⁰¹−2 内不停机**；R8（已经三方审查）：组合式证书 v ≤ 1000 + 模板引擎（2-adic 无障碍、谱系剩余类封闭、sum-类分离——所发现的全部停机族成员均 sum ≢ 0 mod 3，被已审计不变量排除）；三条独立路线各自把 ∀v 化归为明确的有限引理 | `CHECKPOINT_1RB1LA_0RC0RD.md`、`work_r1/`、`work_r4/`、`work_r8/` |
| #2 `1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB` | 归约到 Σ 栈机；定理 H | `REPORT_1RB1RA_1LC0RC.md`、`work_s1/`、`work_s3/` |
| `1RB1LE_1LB1LC_1RD0LE_---0RB_1RF1LA_0RA0RD` | 停机 ⇔ 轨道到达 (0;10,…) | `REPORT_1RB1LE_1LB1LC.md`、`work_t1/` |
| `1RB1LC_1RC1LB_1LD0RB_0LE1RD_---0LF_0LA1LF` | 无（各路径都没走通） | `CHECKPOINT_1RB1LC_1RC1LB.md` |

总报告见 [SUMMARY.md](SUMMARY.md)，里面有文件索引、开放问题和与社区结果的对比。

## 目录结构

- `REPORT_*.md`、`CHECKPOINT_*.md`：每台机器的仲裁记录与阶段性检查点
- `work_*/`：主定理文档（`RULES.md`、`LEMMAS.md`、`PROOF.md`、`EQUIV.md`）与对应的验证脚本 `verify_*.py`
- `work_r5/`、`work_r6/`、`work_r7/`：#1 全局不停机的三次尝试，**未经审查**
- `work_r8/`：#1 的组合式闭合尝试（模板检查 + 谱系封闭）；`scratch/`：研究草稿与子代理报告（agentB/C/D），部分未经审查
- `data/BB6_holdouts_815.txt`：bbchallenge 2026-09-24 版 holdout 清单
- `triage2/scan.txt`：815 台机器各跑 10⁶ 步的初筛数据

## 复现

验证脚本只需要 Python 3 标准库。在对应的 `work_*` 目录下运行，例如：

```bash
cd work_r4 && python verify_r4.py 60
cd work_r8 && python verify_r8.py 1000 300   # check1–6,约 2 分钟
```

注意两处依赖：`verify_q6.py` 依赖 `work_q4`，`verify_s3.py` 依赖 `work_s1`，`verify_u1.py` 依赖 `work_q4`。

## 方法说明与局限

- 命题分级：**A** 为全局符号证明；**B** 为有限的机械穷举，或有限步模拟得到的起点引理；**C** 为数值与经验证据。C 级命题不进入定理。
- "已审查"指通过了攻击员加两名复算员的审查，审查员都是 AI Agent，**不等于同行评审**。
- 多处 A 级结论依赖机械证书，即符号执行程序的输出，例如 #1 的 Lemma E(v)（v ≤ 2000）。这些证书已由独立实现的程序复现。

## 作者

由 Claude Opus 5.5（Anthropic）在用户指导下完成。
