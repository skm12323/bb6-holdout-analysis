# MANIFEST — `work_landing_symbolic/` 产物清单

日期：2026-10-23。工作流 run：`dwfrun-e527efb9-6123-4162-9e53-6e38fa4a73e7`（13h47m，6 阶段，85 步）。
**本目录是本次任务的唯一写入目录**：`git status --porcelain` 只显示未跟踪的 `work_landing_symbolic/`；
`work_c3_drift/`、`reviews/` 等输入目录只读（四个基线验证脚本的 json 若被重写，内容与 HEAD 一致，git 无差异）。
未做 git 提交。

## 1. 先读什么

| 顺序 | 文件 | 用途 |
|---|---|---|
| 1 | `NOTES.md` | **主交付物**：中文摘要、四份文档审阅处置、合并定理、附加条件、J 依赖审计、未解决点与下一步 |
| 2 | `THEOREM.md` | 统一定理全文（§1 正规形、§2 可认证类、§3 gateway 链、§4 障碍、§5 条件形式、§6 J 审计、§7 状态表、§8 复算） |
| 3 | `RUN_REPORT.json` | 本次运行的机器可读总结（结论、条件、计数、gate、未覆盖项） |
| 4 | `landing_checks.json` | 决定性 gate 的逐项结果（903,945 次检查，0 失败） |

## 2. 审阅与复核（输入：`work_c3_drift/` 四份未审文档）

| 文件 | 内容 |
|---|---|
| `reviews/rational_mode.md` | `RATIONAL_MODE.md` 的逐条 `[A]/[B]/[C]` 审阅 |
| `reviews/odd_denominator.md` | `ODD_DENOMINATOR.md` 的审阅 |
| `reviews/shift_transport.md` | `SHIFT_TRANSPORT.md` 的审阅 |
| `reviews/first_a.md` | `FIRST_A_REDUCTION.md` 的审阅 |
| `reviews/check_R.md` | 前两篇的独立复核（confirmed / refuted / uncertain，逐条重算） |
| `reviews/check_T.md` | 后两篇的独立复核 |
| `reviews/theorem_adversary.md` | 未参与起草者的独立挑错（P1–P12） |
| `reviews/final_audit.md` | 最终独立审计（数值核对、P1–P12 状态、诚实性与标签） |
| `reviews/scratch/` | 复核者/挑错者/审计者的临时脚本与 json（可复算证据） |

统计：37 条被声称的错误，32 条经独立复核确认，5 条被推翻（见 `NOTES.md` §2.1、§2.3）。
挑错 12 条全部被吸收，其中 5 条把初稿的 `[A]` 陈述改为 `[REFUTED]`（`landing_checks.json → refuted_claims`）。

## 3. 三个表示方向

| 目录 | 内容 | 决定性 gate |
|---|---|---|
| `rational/` | `PLAN.md`、`RESULT.md`、`verify_rational.py`、`checks.json`；Z[1/3] 正规形、高度/秩、gateway 分母增长、certify/lift | exit 0；1,337,300 次检查，0 失败，6.14 s |
| `affine/` | `PLAN.md`、`RESULT.md`、`verify_affine.py`、`checks.json`；`x=A·U+β, Θ=2^J U+3d+1` 的一步递推与判据 | exit 0；0 failures，2.34 s；5,712 canonical shift cases，252 火 / 419 链 / 84 c 源 |
| `gateway/` | `PLAN.md`、`RESULT.md`、`verify_gateway.py`、`checks.json`；a/b 两型类映射、块记录、深度/高度、36 坏类图 | exit 0；49,952 次检查，0 失败，94.5 s |

每个方向的 `checks.json` 都含 `status`、`scope`、`canonical_tests`、`synthetic_tests`、`failures`；
合成状态逐条标 non-canonical，规范实例来自 `work_global_calendar/calendar_oracle.py` 的 `Calendar(512)`
（必要时 `D:/math_cc_astra/deep1/table_1000000.pkl`）。

## 4. 汇总与确定性门

| 文件 | 内容 |
|---|---|
| `verify_landing.py` | 不 import 三个方向脚本的独立跨方向重算；exit 0 当且仅当全部硬检查通过 |
| `landing_checks.json` | `status: PASS`；903,945 次检查、0 失败；含 `refuted_claims`、`not_run`、`canonical.small_j_bad`、`canonical.internal_record_examples` 等 |
| `directions_status.json` | 三个方向的 gate 状态、检查数、失败数、耗时与文件路径（控制台表格的落盘版本） |
| `_workflow/landing.dwf.ts` | 工作流源码（拓扑、阶段、提示词、gate） |
| `_workflow/landing.run.mjs` | 本次运行的编译产物（harness 生成，供追溯） |

## 5. 复算

在仓库根目录 `D:/math_cc` 下运行：

```
python -B work_landing_symbolic/verify_landing.py
python -B work_landing_symbolic/rational/verify_rational.py
python -B work_landing_symbolic/affine/verify_affine.py
python -B work_landing_symbolic/gateway/verify_gateway.py
```

本次运行的实际结果：`verify_landing.py` exit 0（903,945 次检查 / 0 失败，9.8 s）；
rational 1,337,300 / 0（6.14 s）；affine 0 failures（2.34 s）；gateway 49,952 / 0（94.5 s）。
脚本会重写各自的 `checks.json`，`timing` 字段随运行变化；`status`/计数/失败数在本会话多次运行保持一致。
`THEOREM.md` 头部与 §8.2 的 timing 是较早一次运行的值，最终审计已把这一点列为 I5；以本清单与
`landing_checks.json` 的当前值为准。

## 6. 范围与诚实性

- **未证明全局 EXT，未声称机器不停机，`K_clock` 未改。**
- 目标的无条件形式**未证明**；已证明的是 `THEOREM.md` §5.2/§5.4 的条件形式。
  严格按“附加条件必须是来源/相位条件”的标准，`(S4)` 的 `5≤j_*<2·10^7` 是 `[B]` 有限参数上界，
  `(DEEP)` 的 `J<T_h` 是 horizon 上界，`(H4)` 的 `j≥N0+1` 是深段下界；见 `NOTES.md` §3.5。
- `[A]` = 对所有参数证明（假设列全）；`[B]` = 有限精确计算（范围写明）；`[C]` = 猜想/开放。
  有限范围没有被写成“所有 j”：S4 窗口、24 例外、36 坏类、RAT-C 的秩/高度限制都写明。
- 规范实例只覆盖 `Calendar(512)`/小表可达范围；合成状态不可规范。未复现 8,712 坏对
  （缺 `table_100000000.pkl`）；`Bad_j` 的 `j=22/24/27` 只抽验 4 个 lift，`j>27` 未计算；
  A4 深段解析证明未重跑（`Calendar` 需 `B≥N0`，不可行）。
- 最终审计判定 `issues`（6 条文字/标签残留，其中 I1/I2 在 `THEOREM.md` 内，按任务约束未改
  `THEOREM.md`，已在 `NOTES.md` §2.4 明确列为未解决）。
