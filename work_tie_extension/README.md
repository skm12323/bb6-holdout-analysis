# 更深一层的复制状态分析

**状态：Supplementary to the audited work_tie2 Theorem TIE2 (same horizon K′); contribution = exact b/c margin gain + bigint kernel checks + information-loss construction.**
（对抗审查 2026-10-14：「有可修补的缺口」，无结构性缺陷；结果与已审定的 TIE2 相同，修补已写入。）

本目录是本次新建的独立工作目录。原有 `work_tie`、`work_tie2` 和仓库总报告均未修改。

**取得的扩展：** 保留平局之后的高位余数和安全余量，完成第三层覆盖证书。
在已有定理与基例的基础上，新推导将参数范围由 `J<T2` 推到 `J<T3`，退出链数上界由 6 增至 7，其中

```
T0 = 1,000,000
T(d+1) = 2^(T(d)/2 - 2)
```

相应的通用轨道 F 有限不停机范围为 `s < (2^T3 - 4)/3`。
**这不是原图灵机的全局不停机证明。**

验证摘要：

- 第三层检查 7,000,101 个入口；13,949 次扩展余数运行全部闭合，其中 13,943 个是真正的 NT 平局（'pair' 入口），另 6 个是 NT 安全的扩展输入（'X' 复制记录）。
- 没有未决分支；最小安全余量至少为 1；进入有限表后最多再有 4 条链。
- 另用完整大整数系数核对 n<2048 的 2,048 个交叉时刻与 651 个奇 b/c 交叉；
  抽样 3,012 个具体高位取值，其中 152 个被跳过（x≤0 或超出 n<2048 的数据），其余 2,860 个全部吻合。
  注意：只有 b/c 步使用完整大整数系数；a 步与引擎使用同一符号公式 x=2θ+3τ−u·2^(j−1)，
  仅通过头部恒等式 λ=3τ+1 与大整数数据相连。
- 精确增益恒等式 σ_W=n−ε(n) 仅在 n<2048 用大整数核验；n<10^6 依赖 PROOF_M 引理 3.2 与行走的内部一致性
  （审查者另在全部 318,728 个 n<10^6 的奇 b/c 交叉上按行走自身递推核对过）。
- 构造并验证了 508 个质量恒等式相容的状态，说明仅有 `(j,θ)=(5,5)` 时，下一参数可以任意大。
  这些状态不被宣称在真实轨道上可达；它们说明后续证明不能丢弃高位与来源限制。

文件：

- [完整推导及尚未解决的问题](PROOF_EXTENSION.md)
- [第三层计算证书](certificate_layers.json)
- [主运行记录](run_layers.txt)
- [扩展余数与入口覆盖程序](explore_layers.py)
- [独立算式核对](verify_kernel.py)、[结果](kernel_checks.json)
- [无界跳升构造验证](verify_unbounded_lift.py)、[结果](unbounded_lift_checks.json)

`explore_layers.py` 以 `work_tie2/verify_tie2.py`（已在 d38aa62 提交）的只读快照为基础改进；
没有声称它是独立重写。文件头的快照哈希 DA278B… 已过时：该文件在快照后被编辑，当前哈希为 67bd2b…；
审查确认 make_ext 核心除下列改动外未变。核心改动是精确计算 b/c 安全余量增益、
严格拒绝非正余量、显式限制未决搜索，以及导出完整的后继状态族。

复现（Python 标准库，建议使用 `-B`）：

```
python -B work_tie_extension/explore_layers.py 3
python -B work_tie_extension/verify_kernel.py
python -B work_tie_extension/verify_unbounded_lift.py
```

运行时间与内存：第三层在 Windows 上每个 θ 需 1 小时以上、内存超过 5 GB；
在 WSL/Linux 上全程约 6.6 分钟。建议在 Linux（如 WSL Ubuntu-22.04）上运行。

尚未在本目录计算第四层，也未得到任意层深度的封闭归纳。
第三层已导出 35,801 个扩展后继记录，直接重复枚举的规模明显增长；
后续需要压缩这些记录，并证明保留的高位信息与安全余量足以在任意深度维持。
有限行程读取边界缺陷后的结尾阶段仍是另一项未闭合的证明义务。
