# 最终独立审计（当前文件；第二轮）

日期：2026-10-23。审计者：最终独立审计者（workflow subagent）。
对象（本次实际读取的 mtime）：`NOTES.md` 14:14、`THEOREM.md` 13:58、`landing_checks.json` 14:08、
`verify_landing.py` 13:56、`gateway/checks.json` 14:10、`rational/checks.json` 14:09、
`affine/checks.json` 14:09。只读审计；除本文件外本次未写任何文件。

**结论：`issues`。** 上一轮审计的绝大多数问题已修复，原挑错 P1–P12 仍全部解决，数值/范围
基本全部能在当前 json/脚本输出中找到；没有全局 EXT/不停机/K_clock 的过度声称。剩下的问题
是 **THEOREM 的三处标签/J 表残留** 和 **NOTES “已修”表的少量过度乐观**：

1. §2.4/§5.2 标题仍 `[A|(L1),(L2)]`，未写 (L3) `[B]`（正文与 §7 item 4 已写）；
2. §6.1 gateway(i) 行仍写“无 J”，但绝对块记录 `ρ_2=j_2+Γ_p+2` 含 `Γ_p=J−j_p`；
3. §5.6 表列头仍写“为什么不是参数上界”，而 S4/DEEP 行明确说它们是参数/horizon 上界；
4. §6.1 AFF A4 行（及 NOTES §4.4）只写 `j=J−Γ`，漏了 A4 的直接记录天花板 `≤J`；
5. THEOREM 头部/§8.2 的方向 timing 仍是旧运行；NOTES §7.2 已给出当前值，但头部未改。
NOTES §2.4 表把这些中的 #1/#8 写成“已修”，略过 §5.6 列头/头部 timing；#12 与 #4 已如实
列为未解决点。

---

## 1. 当前 gate 与必需文件

`landing_checks.json`（当前）只读结果：

```
status = PASS
counts.total_checks = 903945
counts.total_fail = 0
failures = []
refuted_claims = 5
not_run = 5
counts.B_canonical_bc = 1273
checks.B.bc.lambda_bound.checked = 1273
checks.B.bc.exact.checked = 122208
checks.Z.X5 = {tag:B, checked:1, failed:0}
checks.Z.small_base_even = {tag:B, checked:1, failed:0}
canonical.small_j_bad = {5:4, 8:4, 12:4, 14:4, 17:8}   (24)
canonical.shift_ties = 5
canonical.bad_graph = {vertices:36, edges:4, max_parameter:29}
```

与当前 `THEOREM.md:5/910-916`、`NOTES.md:51-54/715-731` 的 `903,945`、1,273/122,208 一致。
`THEOREM.md` 头部/§8.1 的旧 `556,900`/`560,523` 已全部替换；`B.bc` 的旧 381/36,576 已不再
作为当前值（NOTES §2.4 明确标为历史）。

必需文件仍齐全：`NOTES.md`、`THEOREM.md`、`landing_checks.json`、`verify_landing.py`、
`reviews/theorem_adversary.md`、四份审阅（`rational_mode.md`、`odd_denominator.md`、
`shift_transport.md`、`first_a.md`）、两份复核（`check_R.md`、`check_T.md`）、三个方向的
`RESULT.md`/`checks.json`/verifier。主 gate 按任务要求**没有重跑**（exit 0 给定）。

`git status --porcelain` 只有 `?? work_landing_symbolic/`；没有已跟踪文件改动、没有提交。

---

## 2. 本次运行的复算命令

### 2.1 Rational（全量，json 写入抑制）

```
python -B -c "import pathlib,runpy,sys; pathlib.Path.write_text=lambda *a,**k: 0;
sys.argv=['work_landing_symbolic/rational/verify_rational.py'];
runpy.run_path(sys.argv[0],run_name='__main__')"
```

输出：

```
{"status": "PASS", "total_checks": 1337300, "total_fail": 0,
 "canonical": 581524, "synthetic": 755776, "elapsed_s": 5.81}
SystemExit 0
```

与 `rational/checks.json` 的 `total_checks=1337300`、`total_fail=0`、`canonical_checks=581524`、
`synthetic_checks=755776`（json 记录 6.14 s）一致。NOTES §1.9 的 6.14 s、1,337,300/0 成立
（本次 5.81 s，wall-clock 波动）。

### 2.2 Affine（全量，json 写入抑制）

同一 runpy 方法，`sys.argv=['work_landing_symbolic/affine/verify_affine.py']`。输出摘要：

```
status PASS
canonical: fires=252 chains=419 c_sources=84 step_checks=167 shift_cases=5712
criterion_holds=503 criterion_hold_unsafe=0 anchor_failures=0 shift_tie_safe=5
O2: cases=126 tie_cases=252 threshold_ok=126
O1: cases=504 identity_cases=504 dangerous_H=5 dangerous_ok=5
failures=0  elapsed_s=2.37
SystemExit 0
```

与 `affine/checks.json` 的 `counts`/`elapsed_s=2.34` 及 NOTES §4.2/§7.2 的关键计数一致
（本次 2.37 s）。

### 2.3 Gateway

本次**没有重跑** gateway verifier（任务只要求抽查 1–2 条；rational/affine 已满足）。
读取当前 `gateway/checks.json`：`status=PASS`、`failures=0`、`timing={"canonical":93.7,"total":94.5}`、
`Bad_j_counts={5:4,8:4,12:4,14:4,17:8,22:4,24:4,27:4}`、`bad_graph.bad_graph` 36/4/29、
`X6132` 四 lift `j2=6,5,5,12`、`delta2=110,30,4110,62`、`omega5_family` 28 交叉/112 例/0 fail。
NOTES §1.9 的 gateway 94.5 s 与当前 json 一致。`gateway/verify_gateway.py:928-929` 会无条件
重写 `gateway/checks.json`；当前 §8.2/§7.2 已如实说明 timing/字节不保证（不是语义断言）。

### 2.4 关键算术（本次实际重算）

```
P1 A4 Z[1/3]: j=40 -> v2=38=j-2, e=2, record 42; j=61 -> 59/1/62; j=100 -> 98/1/101
P4: C=7 -> ht'=4 (A=7/2 preserved)
P5: (j,k,C,b)=(8,2,122,1): p=8, ht'=119, old bound 175/3, new bound 133
P6: C=37 -> 2(C+3k)+3*2^(j-1) = 128 != 0 mod 64; C=-27 -> 0
P11: C=-27 -> C'=42 (3|42); C=21 -> C'=-6
O3 sum = 8338590849833250 < 2^64
r_min = 657306078883964; 5*(sigma-5) < 240+8*r_min; not for r_min-1 (tight)
kappa(49)=125064; kappa(19)=42849; kappa(18)=80937/2
n<4000 odd b/c: 1273 (c-type 63), |lambda|<cW violations 0
```

这些与 `THEOREM.md` 的 P1/P4/P5/P6/P11、O3、O1 阈值、RAT-C 常数一致。

---

## 3. 数值与范围核对（当前）

| NOTES 项 | 当前值 | 证据 | 结果 |
|---|---|---|---|
| gate 总计数 | 903,945 / 0 | `landing_checks.json.counts` | match |
| gate 运行 | 9.8 s（本会话） | `counts.elapsed_seconds=9.77`；§8.1 8–18 s | match（wall-clock） |
| rational | 1,337,300/0，6.14 s | `rational/checks.json counts`；本次 5.81 s | match |
| affine | 0 failures，2.34 s | `affine/checks.json elapsed_s=2.34`；本次 2.37 s | match |
| gateway | 0 failed，94.5 s | `gateway/checks.json timing.total=94.5` | match |
| B 规范 b/c | 1,273 交叉 / 122,208 状态 | `counts.B_canonical_bc=1273`、`B.bc.exact=122208` | match |
| B lambda 界 | 1,273 | `B.bc.lambda_bound.checked=1273`；本次 1,273/0 | match |
| D 锚点 | 15,817 | `counts.D_cases=15817` | match |
| E 252/419/84/167/503 | — | `counts.E_*` | match |
| E 5,712/5/5 | — | `counts.E_shift_*` | match |
| E 185 类 | 179+6 | `E.landing_class_certified` + `E.c_landing_class_certified` | match |
| 24 例外 | 4,4,4,4,8 | `canonical.small_j_bad` | match |
| 36 坏类 | 24 + 22/24/27 各 4 | `gateway/checks.json Bad_j_counts` | match |
| C 状态/计数 | 48,504 / 23,978 | `C.gateway.*=48504`；6,000+5,999+6,000+5,979 | match |
| RAT-C 三族 | 968+14、969+13、981+1 | `counts.F_RATC_families` | match |
| O1 源/阈值 | k=469124961184426，σ=1051689726214394，r_min=657306078883964 | `canonical.O1_fire`、`F.O1.threshold`、本次算术 | match |
| O3 | 8,338,590,849,833,250 < 2^64 | `F.O3.count`、本次算术 | match |
| 24/36、内部链、shift_tie、bad_graph | — | `canonical.*` | match |

当前 `NOTES §2.4` 的“审计旧数”说明（556,900/560,523、381/36,576 是旧稿；当前 903,945、
1,273/122,208）与当前 json 一致；未发现把旧数当当前值的错误。`B.bc.lambda_bound` 现在是
1,273（`verify_landing.py:481-489` 的循环 `n<4000`），上一轮的 381 引用问题已真正修复；
`Z.X5`/`Z.small_base_even` 新增并分别在入口完备性/小基中使用。

---

## 4. 挑错 P1–P12 的当前状态

当前 `THEOREM.md` 已吸收上一轮的全部修订；逐条核对（打开当前小节 + 当前 json/算术）：

| # | 当前落点 | 当前证据 | 状态 |
|---|---|---|---|
| P1 | `§0.3 纠正 3`、`§2.7 [REFUTED]`、`§5.6 A4-int` | `R.I1.*`；本次重算 j=40/61/100 的 v2/e/record | 解决 |
| P2 | `§0.3 纠正 4`、`§2.4/§5.2`、`§6.1` `R_0=J` | `R.I2`；`canonical.internal_record_examples` | 解决 |
| P3 | `§2.7 [C]-归约`、`§7 item 24` | `not_run` 第 4 条；4 条前提 | 解决 |
| P4 | `§0.3 纠正 5`、`§2.3` | `R.I4`；本次 C=7→4 | 解决 |
| P5 | `§0.3 纠正 6`、`§2.3` | `R.I5`；本次 8/122 反例 | 解决 |
| P6 | `§2.1` 同余 | `R.I6`；本次 C=37→128、C=−27→0 | 解决 |
| P7 | `§5.6/§5.7` 分类 | 当前 §5.6 已分类 S4/DEEP/H4（列头问题见 I3） | 主体解决 |
| P8 | `§4.1` | `R.I8`；`data.O1_sharpened` | 解决 |
| P9 | `§3.3` `d≤r_t` | 文本 + Theorem B | 解决 |
| P10 | `§2.2 |λ'|<c'` | 当前 `B.bc.lambda_bound=1273` | 解决 |
| P11 | `§2.5 r=0` | `R.I11`；本次 C=−27→42、C=21→−6 | 解决 |
| P12 | `§1.4` 最小代表 | `R.I12` | 解决 |

挑错 §4 的仍然成立结论（2,880 Theorem D、24/36、O1 算术、O2 族、O3 计数）与当前
json/本次算术一致。**没有发现“挑错已解决”的假声明。**

---

## 5. 上一轮审计项的处置

当前 `NOTES §2.4` 有一张“最终审计处置”表；逐项核对，绝大多数属实：

* **已真正修复**：S4/DEEP 的分类与 DEEP 定义（`THEOREM.md:401-407`、§5.6 DEEP 行、
  §7 item 27）；A5 的“对 J 无上界”限定（`394-398/769`）；Theorem F 的 (H2)
  （`332-339`）；B 1,273/122,208（`verify_landing.py:481-489`）；S4 整数 `δ_*`
  （`783`）；`h(s+2)` 定义（`377-380`）；A5 的 two-chain 限定（`394-398`）；
  `§7 item 4` 的 L3 标签；入口完备性 `Z.X5`（`495-500`）；23,978（`873`）。
* **未解决（notes 已列）**：§2.4/§5.2 标题 `[A|(L1),(L2)]` 未写 (L3)（I1）；
  §6.1 gateway(i) 行“无 J”（I2）。notes 明确把它们列为未解决点，未冒充已修。
* **notes 未列、但仍是问题**：§5.6 表列头“为什么不是参数上界”（I3）；
  §6.1 AFF A4 行漏记录 `≤J`（I4）；THEOREM 头部/§8.2 的旧 timing（I5）；
  notes §2.4 表 #1/#8 的“已修”因此略过度（I6）。

---

## 6. 诚实性与标签

* 未发现“全局 EXT/机器不停机”的过度声称；`NOTES.md:8,830`、`THEOREM.md:9,32` 和三方向
  RESULT 的声明一致；`landing_checks.json.scope` 也写明不是全局 EXT。
* `K_clock` 未被改动：`git status` 只有未跟踪的 `work_landing_symbolic/`；脚本中出现
  `K_clock` 只是声明/审计文字。
* `[C]`→`[A]` 的明显误标没有发现；A4 `Z[1/3]` 仍 `[REFUTED]`，`N_Q` 仍 `[C]/归约`。
* `[A]`/`[B]` 的标签仍有 I1 的标题残留（§2.4/§5.2 标题少 (L3) `[B]`）；正文与 §7 正确。
* 条件结果的写法总体正确：A5/DEEP/Theorem F 的“对 J 无上界”/H2/S4 整数/`h(s+2)` 都已在
  正文中限定；§5.6 列头（I3）是最后一个“参数上界”措辞残留。
* 有限范围没有被写成所有 j：S4 窗口、全残基 24 例外、36 坏类、RAT-C 的 m 范围都写明；
  `B.bc` 的 1,273 写明 n<4000。

---

## 7. Issues

### I1 [THEOREM, minor] §2.4/§5.2 标题缺少 (L3) `[B]`

`THEOREM.md:269` 与 `THEOREM.md:721` 的标题仍写 `[A | (L1),(L2)]`；正文在
`THEOREM.md:277`/`727` 已列 `(L3) 规范小基 X(0..3) 全偶（[B]，Z.small_base_even）`，
§7 item 4（`THEOREM.md:868`）也写 `[A | L1,L2; L3 小基 [B]]`。标题与正文/状态表不一致，
是一个 `[A]` 标签少列 `[B]` 假设的错误。NOTES §4.5/§2.4 #12 已如实列为未解决点，未冒充 [A]。

### I2 [THEOREM, minor] §6.1 gateway(i) 行“无 J”与绝对块记录矛盾

`THEOREM.md:830` 的 `gateway（i）类映射/块下降 | 无`。类映射/高度/深度的**差值**确实无 J，
但块记录 `ρ_2=j_2+Γ_p+2` 含 `Γ_p=J−j_p`（`THEOREM.md` §3.2 的 A 型记录；
`NOTES.md:554,574` 已写明）。该行应写成“类映射/高度/深度无 J；块记录含 Γ_p=J−j_p”，
或把它指向 `THEOREM.md:824` 的 RAT-4 “有”行。NOTES 已把它列为未解决点，但 THEOREM 行本身
仍是错误的 J 表项。

### I3 [THEOREM, minor] §5.6 表列头“为什么不是参数上界”与 S4/DEEP 行矛盾

`THEOREM.md:778` 的列头仍是“为什么不是参数上界”；但同一表的 S4 行（`783`）写
`5≤j_*<2e7` **是参数上界**，DEEP 行（`784`）写 `J<T_h` **是 horizon 上界**。
§5.6 的总标题已经改成“逐条分类”，但列头没有同步；这是上一轮 I1 的最后一个残留。
NOTES §2.4 表 #1 把 §5.6 标成“已修”，但列头不在其中；应改列头为
“类型/是否来源-相位（含 [B]/horizon 上界说明）”。

### I4 [THEOREM, minor] §6.1 AFF A4 行漏掉直接记录天花板 `≤J`

`THEOREM.md:827` 的 AFF A4 行只写“只通过 `j=J−Γ`”；但 A4 的结论在
`THEOREM.md:423` 明确写“所有记录 `≤ J`”（resonance 链记录为 `J`）。`NOTES.md:558`
的 A4-int 行同样只写 `j=J−Γ`。J 通过 `j=J−Γ` 进入参数是对的，但记录天花板也是直接的
J 依赖；该行应写“参数通过 j=J−Γ；记录 ≤J（resonance 记录 J）”。这不是“所有记录都无 J”
的反向错误，而是 J 表少了一项。

### I5 [THEOREM, minor] 头部/§8.2 的方向 timing 仍是旧运行

`THEOREM.md:6-7` 仍写 rational 15.79 s、affine 4.63 s、gateway 168.1 s；当前
`rational/checks.json` 是 6.14 s、`affine/checks.json` 是 2.34 s、`gateway/checks.json`
是 94.5 s。`THEOREM.md` §8.2（`938-955`）说那些是“更早运行”，但头部的句子没有限定；
§8.2 的“本会话见过 rational 9.58–15.79、affine 2.69–4.63”也不含当前 6.14/2.34。
`NOTES.md` §7.2 已给出当前值并说明 timing 不作为断言；但 THEOREM 头部/§8.2 的范围仍与
当前 json 不一致。建议在头部加“早前运行”限定，并把 §8.2 的范围更新为
6.14–15.79 / 2.34–4.63 / 83.6–168.1。

### I6 [NOTES, minor] §2.4 表 #1/#8 的“已修”略过度

`NOTES.md:225`（#1）把 §5.6/DEEP 标成“已修”，但 §5.6 列头仍是 I3 的旧措辞；
`NOTES.md:232`（#8）把 timing 标成“已修（以当前为准）”，但 THEOREM 头部第 7 行仍是
I5 的旧 timing。notes 的 #12/#4 已正确列为未解决点；#1/#8 应补一句“列头/头部仍待改”，
否则“已修”表本身略过度。该条不影响 notes 的总体诚实性：它没有声称全局 EXT，且明确
列出两个未解决点。

---

## 8. 本次未运行/无法验证

* 未重跑 `verify_landing.py`（按任务给定 gate exit=0）；只读当前 `landing_checks.json`。
* 未重跑 gateway verifier（本次用 rational/affine 两条满足抽查要求）；只读当前 `gateway/checks.json`。
* 未全枚举 j=22/24/27 的 `Bad_j`（只读 `Bad_j_counts` 与 4 lift）；未复现 8,712 坏对
  （缺 `table_100000000.pkl`）。
* 未重跑 A4 深段解析证明（`[A-imp]`；Calendar 需 B≥N0）；未重跑 j 接近 2e7 的窗口证书。
* 未重跑 reviews/scratch 下的全部脚本；读取其 json 并核对关键数字。

---

## 9. 判定

**`issues`。** 当前文件已修复上一轮的大多数问题，数值层与 P1–P12 均通过；没有全局 EXT/
不停机/K_clock 的过度声称。剩余问题集中在 **THEOREM 的三处标签/J 表残留**（§2.4/§5.2 标题、
§6.1 gateway(i) 行、§5.6 列头）、**A4 行漏记录 `≤J`**，以及 **头部/§8.2 的旧 timing**；
NOTES §2.4 的“已修”表对其中两处略过度。这些都是可修的文字/标签项，不影响已证明的
[A]/[B] 内容，但按“标签必须准确、J 依赖必须逐项说明”的标准，仍不能判 `pass`。
