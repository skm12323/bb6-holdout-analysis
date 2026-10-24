# MANIFEST — work_gateway_trains 全部产物与复算命令

2026-10-24。所有命令在 D:\math_cc 下执行；所有 gate 当前状态 PASS / exit 0。
规范数据：work_global_calendar Calendar(512)（经 sys.path 导入）与只读表
D:/math_cc_astra/deep1/table_1000000.pkl（n<10^6）。合成状态在脚本与 json 中
标 non-canonical。无全局 EXT/不停机声明；K_clock 不变；未 git。

## 根目录

| 文件 | 内容 | 复算 |
|---|---|---|
| CONTEXT.md | 共享背景：链形式体系、gateway/tie 定义、已接受导入、基础设施、诚实性规则、REFUTED 清单 | — |
| NOTES.md | 主笔记：结论、标注、Astra 文档处置、未解决点、下一步、协作/审查记录 | — |
| MANIFEST.md | 本文件 | — |
| RECORD_BUDGET.md | 任务 4：§2 Ledger Theorem [A]（L1–L4 + 支付恒等式 + run/global-paid）；§3 NT 输出界（(C) 注入）；§4 失效模式 (F1)/(F2)/(F3) 与 train 结构；§5 定理 RB（含一步下降扩展）与剩余缺口 | 见下三 gate |
| budget_ledger.py | Ledger 恒等式验证：tie→tie witness (73515,98094)（非规范）、36 坏类代表元（规范 [B] 态）、O2 族（非规范） | `python -B work_gateway_trains/budget_ledger.py` → budget_ledger.json（status PASS；45 走法/46 门/0 失败） |

## B_rank/（任务 2 (B)，coordinator 完成）

| 文件 | 内容 |
|---|---|
| B_RANK.md | B1 内部 A-return 同余 + tie 类 mod 32 交替 [A]；B2 内部 B-return 条件 [A]；B3 规范 label 扫描 [B]；B4 严格 train 秩律 [A]；B5 秩盲性/移动单残基 [A]；B6 m=4+v2(3u+1) [A]；B7 真实可达统计 [B]；B8 (S2*)/(DEPTH) 实测；§8 剩余条件 |
| train_checks.py | T1 表/日历一致性；T2 规范 kernel 扫描（J≤512）；T3 label 扫描 [7,10^6)；T4 36 坏类走法；T5 witness；T6 (S2*)/DEPTH；T7 危险残基轨道；T8 m-非类函数；T9 合成交替验证（非规范） |
| train_checks.json | gate 工件：`python -B work_gateway_trains/B_rank/train_checks.py`（status PASS，0 失败，~0.5 s） |

## C_climb/（任务 3 (C)，外部 agent 完成 + 审查修补）

| 文件 | 内容 |
|---|---|
| C_CLIMB.md | C1 精确输出公式 x''=A''u_y+Z_run [A]；C2 run 内无相消 [A]；C3 S≠0 [A]；C4 爬升界 m<G(y)+log2(3/2)s+2log2(r+1)−10 [A+常数B]；C5 相消=单残基 [A]；C6 C 字母入口 [A-cond]；r=1 退化 Lemma CB（4,396 恒等式）；§9 规范刚性 [B]；§11 假设账；§12 缺口 |
| climb_checks.py | Z.CB.A/BC（Lemma CB 重现）、Z.run.*（恒等式/尺寸/合成 run/规范 run/huge-y）、Z.centry、Z.const、Z.replay 等块 |
| climb_checks.json | gate 工件：`python -B work_gateway_trains/C_climb/climb_checks.py`（STATUS: PASS，115,121 检查 / 0 失败） |

## review_trains/（任务 1，外部 agent 完成）

| 文件 | 内容 |
|---|---|
| REVIEW.md | 四篇主文档逐条判定表（GT-1..13、CF-1..15、TO-1..8、CS-1..9，无 [REFUTED]）；五篇次级文档标签概览；错误清单（MED-1 + LOW 1–4）；隐含假设/诚实性审计；§8 CHECKPOINT 状态行草案（5 条） |
| review_checks.py / review_checks.json | 独立重推与重建（随机恒等式实例、Calendar(256) 图重建、n<10^8 流式 τ/param-3 复算、cross-scale 双路重放、2-adic dlog 见证）：`python -B work_gateway_trains/review_trains/review_checks.py`（exit 0，全 PASS） |
| verify_*.py（10 份拷贝，输出已改路径）+ *_checks.json（10 份） | 四篇 train verifier 与六篇预算 verifier 的复跑（全 PASS，计数与原文档一致） |
| stream_cache.json / review_run.log | 流式复算缓存与运行日志 |

## 交叉引用（外部，只读）

- work_landing_symbolic/THEOREM.md（审查更正块优先）、work_claude_shift/NOTES.md、
  reviews/{landing_symbolic,claude_shift}_review_record.md、
  CHECKPOINT_1RB1LA_0RC0RD.md 末尾四节、work_c3_drift/*.md（被审查对象，未修改）。

## 当前 gate 状态（2026-10-24 本会话最终重跑）

```
python -B work_gateway_trains/budget_ledger.py            # PASS (45/46/0)
python -B work_gateway_trains/B_rank/train_checks.py      # PASS (T1–T9, failures: [])
python -B work_gateway_trains/C_climb/climb_checks.py     # PASS (115121/0)
python -B work_gateway_trains/review_trains/review_checks.py  # PASS (exit 0)
```
