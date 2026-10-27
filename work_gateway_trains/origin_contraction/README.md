# 2026-10-27：利用规范质量恒等式加强下一 NT 门的控制

**已三方审查（2026-10-27，reviews/origin_contraction_review_record.md）：数学部分接受；PROOF.md 文首的审查更正给出与已接受结果的精确关系。全局不停机仍未证明，K_clock 不变。**

证明见 [PROOF.md](PROOF.md)，复算见
[verify_origin_contraction.py](verify_origin_contraction.py) 和 [checks.json](checks.json)。

本轮取得的具体推进：

1. 从已接受的质量与正性引理推出：b 步倍率为 3/4，c 步倍率在 (1/2,1)，
   且 0<lambda'_W<=6tau+5。因此旧 C4 的 D2 不必另作计算假设。
2. 建立固定祖先的精确仿射不变量 beta=qD+b，0<=q<=2、0<=b<=6t。
   新的大小界不再含随 b/c 步数增长的 (3/2)^s。
3. 推出一个全参数、附明确条件的局部定理：y>=65536，参考相位的高度
   与奇分母预算满足条件，来源亏损有界，则任意长度的非空强下降/b/c 段后，
   下一 a 门输出非零且记录严格低于入口 y。包括参数 >=6 的非裸 NT 门。
   对整数参考相位，分母预算自动成立；允许 |D|<=y/4。
4. 证明整个已认证块可转移到相位模 2^y 相同的整数状态，保留对 lift 的控制。

剩余缺口：真实轨道是否总能提供这种有理参考相位与预算；一步 a 下降、
空 run、小入口，以及任意后续门/嵌套 c 复制的统一控制。不能把局部定理
升级为 EXT 或全局排名函数。

复算命令：

```text
python -B work_gateway_trains/origin_contraction/verify_origin_contraction.py
```

全部检查通过。测试中的祖先状态均标记为合成状态，不冒充实际 S(J) 可达状态。
没有改动既有审查结论、README 或主检查点，也没有提交 Git。
