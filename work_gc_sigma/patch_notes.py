"""patch_notes.py -- apply the round-1 review-correction block and body patches to NOTES.md.
Run AFTER the sigma4 re-run; numbers are read from the fresh artifact where possible."""
import json
from fractions import Fraction

ART = json.load(open('work_gc_sigma/sigma4_20000000.json', encoding='utf-8'))
inv = ART['invariants']
nb = inv['rat_<T4']['n_bad']
nres = sum(len(v) for v in ART['sigma']['<T4'].values())
nch = len(ART['sigma']['<T4'])
chmax = max(int(c) for c in ART['sigma']['<T4'])
bvk = len(inv['rat_<T4']['bad_values'])
bvv = len({k.split('|')[0] for k in inv['rat_<T4']['bad_values']})
bve = sum(len(v) for v in inv['rat_<T4']['bad_values'].values())
fbk = len(ART['fire_beyond_cap'])
fbraw = ART['fire_beyond_cap_note']
fv = sorted({Fraction(x[0]) for x in ART['fired_shift_ranges'].values()})
fvd3 = [str(v) for v in fv if v.denominator <= 3]
secs = ART['seconds']

s = open('work_gc_sigma/NOTES.md', encoding='utf-8').read()

CORR = """> **审查更正块（第 1 轮三方审查，2026-11-11；来源：攻击员 2 MEDIUM＋3 LOW、复算员A 2 MEDIUM＋3 LOW、
> agy 1 LOW；覆盖正文；本版全部数字以重跑后的 sigma4_20000000.json 为准）：**
> 1. [MEDIUM·FIRED_SHIFT_RANGE 键覆盖] 原 sigma4.py 以 (num,den) 为键而按 (num,den,lift) 迭代：每次发射
>    的 cs0 无 lift 孪生族（同 num/den）覆盖带 lift 项——17 个发射族的 lifted 形态（范围 [5,N0]/[5,64] 与
>    落点链 lift 位）成死代码，发射剩余类实际只合成了 m∈[5,54) 的无 lift 形态（原 Σ_{<T4} 止于链 53 即此
>    故），10/3 顶发射被误记 deep/[5,54]，scope 字串「m<4096」失实，且 verify V4 对被覆盖表自洽属循环。
>    已改：键＝(num,den,lift)；合成范围＝无 lift/deep 族 m<54、一切带 lift 族 m<64（与分类器 lift 位
>    搜索域一致；链 m≥65 的发射类全为 4/3+2^m 型、在候选表内，故该封顶不丢失任何 Tier-2 剩余类）；
>    [64,N0) 仅以 M_h.fired_range＋族全链认证表述；verify V4 改为对族证书核对（V4a：全部 102 族标量
>    [5,64) 认证且 uncert 与工件一致、带 lift 族全认证；V4b：fired_shift_ranges 结构），V4c 保留合成剩余类
>    出现性仅作结构性子检查。对结论无影响（出表值均为发射精确值；被漏的 lifted 剩余类全在候选表内或与
>    已计值同值；原合成项均有真实无 lift 孪生族＝合法子闭包）；重跑后计数已更新（正文新数字）。
> 2. [MEDIUM·计数语义] 原「953 个不同最小表示值」有误：工件 bad_values 的 953 是 (值, lift 位) 记录键数，
>    不同最小表示值 684 个、见证条目（每键前 6 个）共 2148 条。本版数字见 §5（语义在工件
>    bad_values_note 标明：每键只存最小 6 个见证 ⟹ 样本饱和于链 30，n_bad 为全链扫描总数）。
> 3. [MEDIUM·Tier-2 谓词] 原文未使 4728 可独立复现（复算员A 按 8 种合理变体得 4687–4833）。现明示判定
>    （sigma4.py 的 reps＋in_list/L_INT/L_GW/L_M2，verify_sigma.py 的 in_list_fast 为其精确整数孪生并经
>    全量等价抽样核验）：剩余类 (c,s) 通过 ⟺ 存在 (v,m) 使 v=num/3^e（e≤10，|v|≤64）、m∈{无}∪[5,min(c,64)]、
>    v+2^m·[m≠无]≡s (mod 2^{c+1})，且 (v,m)∈L＝{(k,无)：k 整数，|k|≤16}∪{(4/3,m)：m 任意（含无）}∪
>    {(−7/3,无)}。锚点分解（agy，旧版数据）：237 严格候选＋49 个 4/3 退化项（裸 4/3）＝286 在表内，
>    5014−286=4728；本版同分解见 §5。
> 4. [LOW·FIRE_LOG 去重] 原 18 行日志＝12 个不同族（−177059/59049 支与其后代跨不动点轮次重复记录）；已按
>    (num,den,lift) 去重并记录原始行数（工件 fire_beyond_cap_note）。无界性结论靠 OBST(a) 闭式，不变。
> 5. [LOW·否证语义限定] 补：见证读法下 h≤4 均零出候选表（<T4-core 的 161 个非族剩余类全在候选表内）；
>    一切违反均在闭包/发射读法下成立，其中 r≥2 轨道值的实现依赖 m=N0 深发射这一日历开放分支。
> 6. [LOW·休眠代码路径] sigma4.py 三条休眠路径（本数据 0 触发，复用前须补）：(i) unc_s 发射对 den≠1 丢弃
>    已算好的 lift 修正 δ；(ii) unc_b 分支不添加 REG 后代；(iii) 整数/spec 自由入口仅对链<64 发射。工件
>    实测：无 lift 族带 unc、无族带 unc_b、自由入口恰 (5,5)@5。
> 7. [LOW·记录性更正] 全表运行 %.1f s（原误 572）；verify 26 项检查（原误 25）；§2 候选值为三元
>    {5, −19/9, 7/27}（原漏 7/27；398/81 分支 §8 已披露）；§3 <T4-core 含 ≤D 层聚合（原描述漏）；工件
>    sigma_ints/ints_with_possible['<T4'] 中 −64..16 等为族剩余类规范读数而非值主张（已加 sigma_ints_note；
>    INV 逻辑用 witnessed_core/exact_structural 已正确排除）。
> 8. [LOW·术语] 统一：「无表示」＝e≤10、|v|≤64 下无任何表示；「出候选表」＝Tier-2 无 L 内表示。
> 9. [LOW·(5,5) 记账] 紧构造 unc_spec={(5,5)} 与 R3 更正块 11 对照实验记账不同：同一对象（θ_1=2、D=5、
>    独立实锚 (244875,−1)），R3 因独立实锚不计入 spec uncert；本构造记为单条 unc_spec（status=ceiling）
>    并被 GW 发射化解（非从构造中消失）。
> 10. [LOW·<T1 聚合] sigma[<T1] 聚合并入 sigma_B 的 generic_all_chains=[0]（链 24 处无 0）；值谱不受影响，
>     「逐字段相等」断言对象是层级 B/C/OUT/D 数据且成立。
> 11. [LOW·bad_values 截断] 工件 bad_values 每键只存最小 6 个见证 ⟹ 详细样本饱和于链 30，n_bad 为全链
>     （5..%d）扫描总数（已加 bad_values_note）。
>
""" % (secs, chmax)

anchor = "> **诚实结论（先行）**"
assert anchor in s
s = s.replace(anchor, CORR + "\n" + anchor, 1)

open('work_gc_sigma/NOTES.md', 'w', encoding='utf-8', newline='\n').write(s)
print('correction block inserted; new numbers: n_bad=%d nres=%d nch=%d chmax=%d bvk=%d bvv=%d '
      'bve=%d fbk=%d fv=%d(den3=%d) secs=%.1f' % (nb, nres, nch, chmax, bvk, bvv, bve, fbk,
                                                  len(fv), len(fvd3), secs))

# ---------------- body patches (numbers + LOW wording fixes) ----------------
t1n = inv['tier1_<T4']['n_bad']
fvd3s = '{%s}' % ', '.join(fvd3)

reps_old_new = [
    # honest-conclusion numbers
    ("""    Tier-2：Σ_{<T4} 的 5014 个 (链,剩余类) 中 4728 个无候选表内表示（953 个不同最小表示值）；Tier-1：85
    个发射精确值中 83 个出表（含 1/3、−5/3、13/3（den 3）、28/9（den 9）、…、−295237/59049（den 3^10））。""",
     """    Tier-2：Σ_{<T4} 的 %d 个 (链,剩余类) 中 %d 个出候选表（%d 条 (值,lift 位) 记录、%d 个不同最小表示值、
    见证条目 %d 条）；Tier-1：%d 个发射精确值中 %d 个出表（含 1/3、−5/3、13/3（den 3）、28/9（den 9）、…、
    −295237/59049（den 3^10））。""" % (nres, nb, bvk, bvv, bve, len(fv), t1n)),
    ("""46/9→154/27→478/81→…→den 3^10（r=10，共 102 族全认证），封顶外 18 条发射（den 3^11）入 FIRE_LOG，""",
     """46/9→154/27→478/81→…→den 3^10（r=10，共 102 族全认证），封顶外 %d 个不同族（%s；去重前 %d 行日志）入 FIRE_LOG，"""
     % (fbk, 'den 3^11', 18)),
    # §0.2
    ("""的复现）；族闭包 102 族（封顶 den 3^10）、封顶外 18 条发射；P4 装配＋分类（规范读法 den≤3、|分子|最小；""",
     """的复现）；族闭包 102 族（封顶 den 3^10）、封顶外 %d 个不同族；P4 装配＋分类（规范读法 den≤3、|分子|最小；""" % fbk),
    # §2 scope
    ("""发射入口剩余类对 m<4096 显式合成、m∈[4096,N0) 以族全链认证为范围主张。""",
     """发射入口剩余类：无 lift（含 deep 后代）族 m<54、orbit 发射 lift 族 m<64、顶发射（10/3）lift 族
m<4096 显式合成（含落点链 lift 位）；m∈[4096,N0) 仅以族全链认证＋M_h.fired_range 表述（不合成）。"""),
    # §2 candidates三元
    ("""specific (5,5) 按剩余类＋一切 e≤4 候选小值发射（候选 {5, −19/9}——−19/9≡5
  (mod 64)，与 R3 的分式归属发射 154/27 一致）。""",
     """specific (5,5) 按剩余类＋一切 e≤4 候选小值发射（候选恰三元 {5, −19/9, 7/27}——后两者 ≡5
  (mod 64)；−19/9 与 R3 的分式归属发射 154/27 一致，7/27 发射 398/81 平行分支）。"""),
    # §2 P3 fire log
    ("""族闭包：102 族，封顶外 18 条发射（den 3^11，
  FIRE_LOG）计数""",
     """计数"""),
    # §3 counts
    ("""计数：Σ_{<T3}=21 链 121 剩余类 26 规范族；Σ_{<T4}=49 链（5..53）5014 剩余类 258 规范族，其中 4049 个在
e≤1 下无表示、e≤10 下 0 个无表示（全部可分类为 num/3^e、e≤10、|v|≤64）；Σ_{<T4} 的非族部分
（<T4-core：E 的 spec＋整数走步 a-输出）=21 链 161 剩余类，零出表。""",
     """计数：Σ_{<T3}=21 链 121 剩余类 26 规范族；Σ_{<T4}=%d 链（5..%d）%d 剩余类 %d 规范族（术语：「无表示」＝
e≤10、|v|≤64 下无任何表示，「出候选表」＝Tier-2 无 L 内表示）；e≤10 下 0 个无表示（全部可分类为
num/3^e、e≤10、|v|≤64）；Σ_{<T4} 的非族部分（<T4-core：≤D 层聚合＋E 的 spec/整数走步 a-输出，不含族
与发射合成）=21 链 161 剩余类，零出候选表（见证读法下 h≤4 均零出候选表——一切违反均在闭包/发射读法
下，其中 r≥2 轨道值的实现依赖 m=N0 深发射这一日历开放分支）。""" % (nch, chmax, nres,
                                                                      len(ART['canon_families']['<T4']))),
]
for old, new in reps_old_new:
    if old not in s:
        print('WARN not found:', old[:60].replace('\n', ' '))
    else:
        s = s.replace(old, new)

open('work_gc_sigma/NOTES.md', 'w', encoding='utf-8', newline='\n').write(s)
print('body numbers patched; tier1=%d' % t1n)
