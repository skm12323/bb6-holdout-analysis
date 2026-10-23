/*
拓扑（在写任何代码前定下）
- 审阅：4 个独立审阅者（每人一篇未审文档），按 2 篇一组串到 1 个独立复核者；两组并行，最后一次 join。
- 探索：3 个持久上下文的探索者（有理模式 / 仿射来源 / 重复 gateway 链），每个跑 计划→实现→结论 三轮；
  每个方向的脚本由 world.run 作决定性 gate，失败回喂同一探索者修复（<=2 轮）。
- 汇总：1 个汇总者写 THEOREM.md + verify_landing.py；1 个未参与起草的挑错者攻击；汇总者逐条修订。
- 交付：1 个笔记作者写 NOTES.md；1 个独立最终审计者核对挑错是否解决与笔记诚实性。
- 确定性 gate：4 个基线验证脚本、3 个方向脚本、verify_landing.py 的退出码。
*/

interface DocSpec {
  /** 文档短名，用于子代理命名。 */
  short: string;
  /** 仓库相对路径。 */
  file: string;
  /** 审阅报告写到哪个仓库相对路径。 */
  report: string;
}

interface ReviewFinding {
  /** 文档中的行号或行段，如 "L42-L48"。 */
  loc: string;
  /** 一句话：问题是什么（不是怎么改）。 */
  what: string;
  /** critical = 结论错误或前提缺失；major = 范围/常量/精度错误；minor = 表述。 */
  severity: "critical" | "major" | "minor";
  /** 修正后的表述，或需要补充的假设。 */
  correction: string;
}

interface ReviewResult {
  /** 被审阅文档的仓库相对路径。 */
  docFile: string;
  /** 审阅报告写到的仓库相对路径。 */
  reportPath: string;
  /** 该文档自带验证脚本的结论（工作流已运行一次）。 */
  verifier: string;
  /** 主要结论逐条列表，每条带 [A]/[B]/[C] 标注。 */
  claims: string[];
  /** 发现的问题，最多 10 条（其余写进报告文件）。 */
  errors: ReviewFinding[];
  /** 文中依赖 N0=2e7、窗口 [-12,15]、参数上界或 log* J 的位置。 */
  scaleDependence: string[];
  /** 三到五句话的总体判断。 */
  verdict: string;
}

interface CheckItem {
  /** 被复核问题的定位，必须与输入错误顺序一一对应。 */
  loc: string;
  /** confirmed = 复核成立；refuted = 复核不成立；uncertain = 证据不足。 */
  verdict: "confirmed" | "refuted" | "uncertain";
  /** 复核证据：重算的式子、命令输出或反例。 */
  evidence: string;
}

interface CheckResult {
  /** 复核报告写到的仓库相对路径。 */
  reportPath: string;
  /** 逐条复核结果，顺序与输入错误列表一致。 */
  items: CheckItem[];
  /** 复核者独立发现的额外问题（没有就给空数组）。 */
  extra: string[];
}

interface PlanResult {
  /** 精确的定理陈述（含所有假设），三到六行。 */
  statement: string;
  /** 假设列表，逐条说明它是不是参数上界。 */
  hypotheses: string[];
  /** 计划写的脚本、json 和结果文件路径。 */
  artifacts: string[];
  /** 计划验证的精确恒等式与测试范围。 */
  testPlan: string[];
}

interface ImplResult {
  /** 已写的脚本、json 与报告路径。 */
  artifacts: string[];
  /** 自己运行脚本的退出码与输出摘要。 */
  runSummary: string;
  /** 仍未解决的检查失败。 */
  failures: string[];
}

interface DirectionResult {
  /** 方向名：rational / affine / gateway。 */
  direction: string;
  /** 该方向证明的定理，含所有假设与 [A]/[B]/[C] 标注。 */
  theorem: string;
  /** 哪些部分与 J 无关，哪些仍依赖 J、N0 或 log* J（必须明说）。 */
  jDependence: string;
  /** 决定性 gate 的退出码与检查计数。 */
  gate: "pass" | "fail";
  /** 脚本检查计数与失败数。 */
  checks: string;
  /** 未解决点。 */
  open: string[];
  /** 结果文件路径。 */
  resultPath: string;
}

interface TheoremDraft {
  /** 统一定理的精确陈述。 */
  statement: string;
  /** 附加条件（必须是来源/相位条件，不是参数上界），逐条。 */
  conditions: string[];
  /** 逐部分的标注与状态。 */
  parts: string[];
  /** 需要的脚本和 json 路径。 */
  artifacts: string[];
  /** 未解决点。 */
  open: string[];
}

interface RevisionResult {
  /** 修订后的统一定理陈述。 */
  statement: string;
  /** 修订后的附加条件。 */
  conditions: string[];
  /** 修订后逐部分状态。 */
  parts: string[];
  /** 脚本与 json 路径。 */
  artifacts: string[];
  /** 未解决点。 */
  open: string[];
  /** 对挑错报告 I1..In 的逐条回应。 */
  responses: string[];
}

interface AdversaryResult {
  /** 挑错报告路径。 */
  reportPath: string;
  /** 逐条问题。 */
  issues: ReviewFinding[];
  /** 攻击后仍然成立的结论。 */
  survived: string[];
}

interface FinalAudit {
  /** 审计报告路径。 */
  reportPath: string;
  /** pass = 笔记与证据一致且无过度声称；issues = 有问题。 */
  verdict: "pass" | "issues";
  /** 逐条问题，每条以 NOTES:/THEOREM:/SCRIPT: 开头。 */
  issues: string[];
  /** 抽查了哪些文件/命令。 */
  checked: string[];
}

interface Finding {
  /** 文件与位置，如 "work_c3_drift/RATIONAL_MODE.md:L42"。 */
  where: string;
  /** 一句话：发现了什么。 */
  what: string;
  /** 证据：复核者重算的行、命令输出或反例。 */
  evidence: string;
  /** verified = 独立复核或确定性检查确认；unconfirmed = 未确认。 */
  status: "verified" | "unconfirmed";
  /** 影响程度。 */
  severity: "low" | "medium" | "high";
}

const OUT = "work_landing_symbolic";

const BRIEF = `共同背景（所有子代理必须遵守）
仓库 D:/math_cc 是 BB(6) holdout #1（1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE）全局不停机证明的工作区。
本轮不证明全局 EXT、不声称机器不停机、不改变 K_clock。已接受结论以 CHECKPOINT_1RB1LA_0RC0RD.md 末尾
（work_deep / work_r1r2 / work_c3_drift 三节）为准。

链与游走：链 (j,Theta,x)，x=2^j u（u 奇），n=j-1，读交叉 X(n)。a 步（tau(n)=2k）：x'=2Theta+6k-x/2，
Theta'=Theta+3+6k；b/c 步（W 的链 (c'_W,lambda'_W)）：x'=c'_W u+lambda'_W，j'=omega(n)=v2(lambda'_W)，
Theta'=Theta+3+3tau(n)。缺陷 theta=Theta-x mod 2^j；a: theta'=3-theta；b: theta'=theta-1；
c: theta'=theta+Phi-2，Phi=3tau+5-lambda'_W=1-lambda_Y。记录 = j+Gamma，Gamma 累计 1+epsilon。
certify(j,delta)（work_claude_shifted Prop 3.2）：从代表元 (2^j, 2^j+delta) 出发的精确游走无 x=0、终止、
所有记录 <= j。[B] 窗口证书：5<=j<2*10^7、delta in [-12,15] 全部成立，只有 (5,5)、(5,-11) 失败。
c 步对漂移加一个来源移位 s：epsilon=3 -> 0，AA -> -1，BA -> +1，BBBAA -> +4/3；一般 s in Z[1/3]，
分母 3^r，高度 h 是参数（另一位研究者在推一般公式，本轮只把 s 当参数）。

必须正面处理的障碍（不许绕开）
(O1) work_c3_drift/ORBIT_SHIFT_OBSTRUCTION.md：P=49 规范源，位移 eta_r=-5+8/3^r（高度<=5、2-adic 单位）
     对 r>=657306078883964 在首个输出就使严格安全失败。因此"所有有界高度位移都安全"是假的；
     必须把实际分母深度 r 与祖先精度 sigma 关联，或排除危险剩余类。
(O2) work_c3_drift/STOP_CHECKPOINT_2026_10_21.md：联合预算 W 不能在任意小二步 gateway 处局部闭合；
     必须保留实际仿射来源 x=A*U+beta，Theta=2^J U+3d+1，v2(A)=J-Gamma，判据形如 v2(beta')<J-Gamma-1。
(O3) work_c3_drift/OPTIMAL_PHASE_ENCODING.md：只用局部相位类、预留 S 位的编码不能覆盖所有类
     （S=m=64 时上界 8,338,590,849,833,250 < 2^64）；必须使用实际来源/相位限制，不能靠扩大有限扫描。
已接受但不得重开的反例：CAL-C 假、R1 与 H3 在 [K_clock,T4) 失败（CONGRUENCE_TARGET_NOTE.md）。
所以任何"参数上界"型条件（CAL-C/R1/H3）不能当统一目标；H5/C7 是 J<T4 的条件归约但 H5 仍含 N0。

本轮目标：给 c/a/b 着陆建立与尺度无关的符号论证。输入相位 theta+s（s in Z[1/3]，高度<=h）时，
着陆类可认证，或经有限步 gateway 化解且每步记录严格下降，界不依赖 J。若做不到，精确写出所需附加条件，
必须是来源/相位条件，不能是参数上界。必须说明每一部分对 J 的依赖（含 log* J、N0、2*10^7、T_h）。

标注：[A] 对所有参数证明（假设列全）；[B] 有限精确计算（范围写明）；[C] 猜想/数据。
每个结论要有可复算脚本与 json。规范实例用 work_global_calendar/calendar_oracle.py（Calendar(B)，B<=1024），
可用 D:/math_cc_astra/deep1/table_1000000.pkl；合成状态必须显式标 non-canonical。脚本用 python -B，
单次 <10 分钟，打印 PASS/FAIL 与计数，写 json。
只允许在 D:/math_cc/work_landing_symbolic/ 下写文件；不得修改其他目录；不得 git 提交。
不得把未证明的东西写成 [A]；不得声称本轮已证明全局 EXT。`;

const REVIEWER_PERSONA =
  "你是这个 2-adic 动力系统证明项目的审稿人，擅长逐行核对精确恒等式、精度位（mod 2^j 与 2^{j+1}）、" +
  "常数界与假设范围。你的标准是：每条结论要么有完整的假设清单与证明，要么明确标 [B] 并写清计算范围，" +
  "要么标 [C]；范围外推、隐藏的参数上界、循环使用的假设都必须指出。如果无法判定，就写不确定并给出缺失的证据，不要猜。";

const CHECKER_PERSONA =
  "你是独立复核者，不参与起草。你只相信自己的重算：对每条被声称的错误，打开原文对应行，独立重推导或写精确计算，" +
  "再判定成立与否。审阅者说的不算证据。你尤其检查 modulus 与 lifting bit、常数比较、有限范围的越界外推、" +
  "以及把参数上界伪装成结构条件的地方。";

const EXPLORER_PERSONA =
  "你是这个项目的主力研究者，擅长精确整数/有理游走、2-adic 估值与 HP 影子论证。你的工作必须可复算：" +
  "每一条断言要么给出完整证明，要么给出脚本与 json 的有限精确检验并写明范围，要么标 [C]。你不为了通过检查而删断言；" +
  "反例和失败必须原样保留。你清楚本轮的边界：不证明全局 EXT，不改 K_clock。";

const ASSEMBLER_PERSONA =
  "你是汇总者，负责把不同表示的结果合并成一个精确、可审计的定理。你特别警惕三件事：把条件结果写成无条件、" +
  "把有限范围写成所有参数、把参数上界伪装成来源条件。你对每一处对 J 的依赖都要么证明没有，要么写明。";

const ADVERSARY_PERSONA =
  "你是独立挑错者，没有参与起草，目标是让定理失败。你优先构造最小反例、找隐藏的参数上界、检查精度位与假设循环；" +
  "审阅时先假设作者错了。你不在对方文件里改东西，只写自己的报告。";

const NOTES_PERSONA =
  "你是这个项目的笔记作者，写出的东西要让下一个研究者能复算、能接着做。你先写结论，再写证据；" +
  "每个数值都指到 json 或脚本；条件结果绝不写成无条件；未解决点写得具体。";

const AUDITOR_PERSONA =
  "你是最终独立审计者，只对证据负责。你逐条核对笔记里的数值与标注能否在 json/脚本中找到，" +
  "逐条核对挑错是否真的被解决，并检查有没有全局 EXT/不停机的过度声称。你不修改任何文件。";

const DOCS: DocSpec[] = [
  {
    short: "rational-mode",
    file: "work_c3_drift/RATIONAL_MODE.md",
    report: "work_landing_symbolic/reviews/rational_mode.md",
  },
  {
    short: "odd-denominator",
    file: "work_c3_drift/ODD_DENOMINATOR.md",
    report: "work_landing_symbolic/reviews/odd_denominator.md",
  },
  {
    short: "shift-transport",
    file: "work_c3_drift/SHIFT_TRANSPORT.md",
    report: "work_landing_symbolic/reviews/shift_transport.md",
  },
  {
    short: "first-a",
    file: "work_c3_drift/FIRST_A_REDUCTION.md",
    report: "work_landing_symbolic/reviews/first_a.md",
  },
];

interface DirectionSpec {
  direction: string;
  label: string;
  persona: string;
  dir: string;
  script: string;
  task: string;
}

const DIRECTIONS: DirectionSpec[] = [
  {
    direction: "rational",
    label: "有理模式",
    persona: EXPLORER_PERSONA,
    dir: "work_landing_symbolic/rational",
    script: "work_landing_symbolic/rational/verify_rational.py",
    task: `方向 R：有理模式（Z[1/3] 状态、高度记账、gateway 的分母增长）。
必读：work_c3_drift/RATIONAL_MODE.md、ODD_DENOMINATOR.md、BBBAA_COPY_CERTIFICATE.md、
work_c3_drift/UNBOUNDED_C_PARAMETER_IF_EXT.md §4、ORBIT_SHIFT_OBSTRUCTION.md、work_r1r2/NOTES.md §5
（Lemma 5.1 与 5.3）、C5_EXTENSION.md §1-2、work_claude_shifted/NOTES.md §5。

要建立的东西：
(R1) 正规形：状态缺陷 D=C/Q+b*2^j（Q=3^r，gcd(C,Q)=1，高度 ht=|C|/Q，b in {0,1}）。精确验证
     a 步 j'=1+v2(3Qk+C)、C'=3Q-C、b'=0（条件 q<=j-2），以及低亏损 b/c 步 C'=C+Q(Phi-2)、b'=0；
     每一步写清 modulus 与 lifting bit。特别检查 Q 大于 2^j 时代表元怎么取。
(R2) 高度递推：a 反射保 |C/Q-3/2|；低亏损 b/c（Phi-2 in {-1,0,1}）使高度至多 +1；
     参数 5 的 gateway 在 Q=3^r 时 Q->3Q，且 ht' <= 5 + ht/3。显式求出 t 步 gateway 后的
     高度与分母，判断哪些量与 J 无关。
(R3) 有理证书 certify_Q(j,C/Q)：定义成精确游走，说明它与 Prop 3.2 的关系，证明或在有限范围 [B] 检验
     well-defined 性；特别处理 x=0 与 lift bit。给出它与整数 certify(j,delta) 何时一致。
(R4) 目标定理候选：固定 h>0，对所有 j、所有 Q=3^r、所有 |C|/Q<=h，着陆类要么 certify_Q 成立，
     要么有限步 gateway 后 certify_Q 成立且记录严格下降；给出链长上界 N(h) 的候选公式，
     并检查它是否真的不含 J、N0、log* J。若做不到，给出精确的来源条件（例如 r <= sigma-5-c(h)
     或排除某个危险剩余类），并证明在该条件下定理成立。
(R5) 障碍：把 ORBIT_SHIFT_OBSTRUCTION 的 P=49 源与 eta_r 放进你的表示，说明它违背哪条假设；
     用 OPTIMAL_PHASE_ENCODING 的计数说明为什么"按高度枚举类"不可能。`,
  },
  {
    direction: "affine",
    label: "仿射来源",
    persona: EXPLORER_PERSONA,
    dir: "work_landing_symbolic/affine",
    script: "work_landing_symbolic/affine/verify_affine.py",
    task: `方向 A：仿射来源（保留 x=A*U+beta，Theta=2^J U+3d+1，v2(A)=J-Gamma）。
必读：work_c3_drift/STOP_CHECKPOINT_2026_10_21.md、AFFINE_REACHABLE_CATAPULTS.md、
BBBAA_COPY_CERTIFICATE.md、B_PREFIX_SOURCE_ENCODING.md、SHIFT_TRANSPORT.md、FIRST_A_REDUCTION.md、
work_claude_shifted/NOTES.md §5、work_global_ext/PROOF_EXT.md §2（HP/AB）。

要建立的东西：
(A1) 从仿射表示精确推导 a/b/c 一步后的 (beta',d',A')，标出系数估值 J-Gamma 的变化与精度余量；
     特别验证五输入 a 步的 beta'=6d+8-beta/2 与 v2(beta')<J-Gamma-1 判据。
(A2) 把输入相位 theta+s 写成对 beta 或 d 的变形（s in Z[1/3]）；给出着陆类在仿射坐标下的表达式，
     并说明它只依赖 (beta,d,A,sigma) 中的哪些量。
(A3) 目标：一个判据 C(beta,d,A,sigma)，只依赖来源量（不依赖 U 的具体大小，或只依赖 J-Gamma 的差），
     使 C 成立时着陆类 certify。逐条检查每个条件是不是伪装成来源条件的参数上界；若是，改写或标注。
(A4) 在真实符号出口上检验：用 Calendar(512) 的 P<=256 火，构造实际 epoch/S(J) 的仿射数据，
     运行判据并与精确游走比较；合成状态标 non-canonical。保留判据失败的例子。
(A5) 说明为什么 W 联合预算不够（STOP_CHECKPOINT 的 m>=8 构造），以及仿射判据在哪一步补上；
     写出它仍需要的来源条件。`,
  },
  {
    direction: "gateway",
    label: "重复 gateway 链",
    persona: EXPLORER_PERSONA,
    dir: "work_landing_symbolic/gateway",
    script: "work_landing_symbolic/gateway/verify_gateway.py",
    task: `方向 G：重复 gateway 链（tie 化解的迭代）。
必读：work_claude_shifted/NOTES.md §5、work_r1r2/NOTES.md §5（Lemma 5.3）、C5_EXTENSION.md §2-3、
FIRST_A_REDUCTION.md §2-3、ORBIT_SHIFT_OBSTRUCTION.md、work_r1r2/agent_C/NOTES.md。

要建立的东西：
(G1) 把 a-gateway 与 b/c-gateway 写成类映射 G，显式给出新参数 m=v2(...)、新类 delta' 与新分母 Q'；
     检查 Lemma 5.3 的 Q 与 work_claude_shifted §5 的 Q 是同一个量（或差在哪里）。
(G2) 迭代：t 次后 (j_t,C_t,Q_t) 的公式；证明记录 r_{t+1} <= r_t-1；高度递推；Q=3^r 时 r 每次 +1。
(G3) 终止判据：第 t 步不终止的精确同余条件（modulus 与量）；若链长 > N(h) 会强制 r 超过什么来源界。
     这是把"重复 gateway"变成来源条件的关键。给出链长上界或精确的无限链条件。
(G4) 在规范数据上检验：Calendar(512) 的 tie 实例（X(6132) 的 omega=5 坏类；work_r1r2 的 8,712 坏对），
     可用 D:/math_cc_astra/deep1/table_1000000.pkl；合成链标 non-canonical。测链长分布、终止率、记录下降。
(G5) 把 ORBIT_SHIFT_OBSTRUCTION 解释为 gateway 链无限/长时的危险类，写出排除它的来源条件，
     并说明该条件不是参数上界。`,
  },
];

function firstLine(s: string): string {
  const t = s.trim().split("\n")[0];
  return t.length > 280 ? t.slice(0, 280) : t;
}

function reviewerPrompt(d: DocSpec, baseLine: string): string {
  return `${BRIEF}

你的任务：逐条审阅 ${d.file}（本轮四份未审文档之一；全文都要读）。
先读背景：CHECKPOINT_1RB1LA_0RC0RD.md 第 614-681 行；reviews/c3_drift_review_record.md；
work_r1r2/NOTES.md §0-5；work_claude_shifted/NOTES.md §1-5；work_global_ext/PROOF_EXT.md §2；
work_c3_drift/C5_EXTENSION.md §1-4；work_c3_drift/CONGRUENCE_TARGET_NOTE.md §4-5；以及三份障碍
ORBIT_SHIFT_OBSTRUCTION.md、STOP_CHECKPOINT_2026_10_21.md、OPTIMAL_PHASE_ENCODING.md。

该文档自带的验证脚本已由工作流运行一次（不要重复运行同一个脚本；如需额外计算，自己写临时脚本放在
${OUT}/reviews/scratch/ 下）：
${baseLine}

要求：
1. 逐条标注：为每个实质结论（引理、恒等式、界、常数、范围声明）给出 行号或行段 + 一句话 + [A]/[B]/[C] + 是否正确。
   行号以文件实际行号为准。
2. 找错：代数错误、缺失假设、精度位错误（mod 2^j vs 2^{j+1}、lifting bit）、未证明的常数界
   （3 因子、log 常数、B 与 2^j 的比较）、范围外推、循环论证、把有限证书当成对所有 j、
   把条件写成参数上界却声称统一。每条给 severity 与修正。
3. 标出文中所有依赖 N0=2*10^7、窗口 [-12,15]、j<2*10^7、T_h、log* J 或任何参数上界的位置。
4. 写报告到 ${d.report}（用 mkdir -p 建目录；只写 ${OUT}/ 下）。报告含：验证命令与输出、逐条表格、
   错误清单（行号+严重度+修正）、范围依赖、总评。
5. 返回 ReviewResult：docFile=${d.file}，reportPath=${d.report}；claims 最多 20 条；
   errors 最多 10 条（其余写进报告）；scaleDependence 写明行号。

不要修改 ${d.file} 或其他目录的文件。不要 git 提交。不要声称全局 EXT。`;
}

function checkerPrompt(g: { name: string; docs: DocSpec[] }, reviews: ReviewResult[]): string {
  const blocks = reviews
    .map((r, i) => {
      const list = r.errors
        .map((e, j) => `  E${j}: ${e.loc} | ${e.severity} | ${e.what} | 修正: ${e.correction}`)
        .join("\n");
      return `【${g.docs[i].file}】审阅报告 ${r.reportPath}\n${list}`;
    })
    .join("\n\n");
  return `${BRIEF}

你是独立复核者。下面两篇审阅报告声称了若干错误。你要逐条独立复核，而不是相信审阅者：
${blocks}

要求：
1. 对每条错误：打开原文对应行，独立重推导或写精确计算（临时脚本放 ${OUT}/reviews/scratch/），
   判定 confirmed / refuted / uncertain，并给证据（重算的式子、命令输出、反例）。
   items 的顺序必须与上面的错误顺序严格一致：先第一篇文档的 E0..En，再第二篇文档的 E0..En。
2. 额外检查审阅者是否漏掉：modulus/精度位错误、把有限范围写成 all-j、隐藏参数上界、循环假设。
3. 写复核报告到 ${OUT}/reviews/check_${g.name}.md。返回 CheckResult。
不要修改任何原文档；不要 git 提交。`;
}

function planPrompt(spec: DirectionSpec, reviewPaths: string): string {
  return `${BRIEF}

你负责的方向：${spec.label}（${spec.direction}）。工作目录：${spec.dir}/（需要时用 mkdir -p 创建）。
审阅阶段的报告（可读，作为输入；但你必须自己重推导）：
${reviewPaths}

${spec.task}

本轮只做计划，不写验证脚本：
1. 写 ${spec.dir}/PLAN.md：精确陈述草稿（含全部假设）、与已有文献的关系、要验证的精确恒等式清单、
   测试范围（规范 vs 合成；规范实例用 Calendar 怎么取）、以及一个 falsification test（什么结果会杀死该陈述）。
2. 返回 PlanResult。statement 要能直接放进最终定理；hypotheses 逐条说明为什么不是参数上界（或明说它就是）。
不要修改其他目录；不要 git 提交；不要声称全局 EXT。`;
}

function implPrompt(spec: DirectionSpec, plan: PlanResult): string {
  return `按你刚写的 ${spec.dir}/PLAN.md 实现并测试（陈述若有修正，先改 PLAN.md 并说明）。
必须产出：
- ${spec.script}：python -B 可运行，精确整数/有理运算，打印 PASS/FAIL 与计数，写 ${spec.dir}/checks.json。
  json 必须含：status、scope、canonical_tests、synthetic_tests、failures、每条结论的计数。
  规范实例用 work_global_calendar/calendar_oracle.py 的 Calendar(B<=1024)；合成状态逐条标 non-canonical。
- ${spec.dir}/RESULT.md 的初稿（定理、假设、[A]/[B]/[C]、对 J 的依赖、未解决点）。
运行它，覆盖 PLAN 的测试清单；把失败原样保留（不要为了让脚本通过而删测试或放宽断言）。
计划里的陈述：${plan.statement}
返回 ImplResult：已写文件、运行输出摘要、仍失败的检查。
不要声称 gate 已通过（工作流会再运行一次作为决定性 gate）。`;
}

function fixPrompt(spec: DirectionSpec, feedback: string, round: number): string {
  return `工作流对 ${spec.script} 的决定性运行失败（第 ${round} 轮修复）。输出：
${feedback}
修脚本或修测试范围：只修真正错的断言；不得删除失败的硬检查来制造 PASS。如果失败揭示了定理陈述是错的，
改 ${spec.dir}/RESULT.md 与 PLAN.md，把该情形写成反例或附加条件。返回一段话说明改了什么。`;
}

function resultPrompt(spec: DirectionSpec, gate: WorldRunResult, rounds: number): string {
  return `收尾。决定性 gate 的退出码：${gate.exitCode}（修复轮数 ${rounds}）。stdout 末尾：
${gate.stdout.slice(-1400)}
stderr 末尾：
${gate.stderr.slice(-800)}

写 ${spec.dir}/RESULT.md 的最终版：
1. 精确定理（所有假设、[A]/[B]/[C] 逐条）；2. 证明或证明骨架，关键恒等式给行内公式；
3. 与目标形式（theta+s, s in Z[1/3], 高度<=h；认证或有限步 gateway + 严格记录下降；界与 J 无关）的差距：
   明确写出每一处对 J、N0、2*10^7、T_h、log* J 的依赖，或证明没有；
4. 需要的附加条件（若做不到无条件）：必须是来源/相位条件，写成可检验的数学陈述；
5. 未解决点与下一步；6. 复算命令与 json 路径。
返回 DirectionResult。gate 失败时如实写"脚本未通过"，不要粉饰。`;
}

function assemblerPrompt(dirs: DirectionResult[], reviewPaths: string): string {
  const blocks = dirs
    .map(
      (d) =>
        `【${d.direction}】gate=${d.gate}\n定理：${d.theorem}\nJ 依赖：${d.jDependence}\n检查：${d.checks}\n结果：${d.resultPath}\n未解决：${d.open.join("; ")}`,
    )
    .join("\n\n");
  return `${BRIEF}

你是汇总者。三个方向的最终结果：
${blocks}

审阅与复核报告：
${reviewPaths}

任务：写 ${OUT}/THEOREM.md 与 ${OUT}/verify_landing.py（写 ${OUT}/landing_checks.json）。
1. THEOREM.md 结构：
   §0 范围与诚实声明（不证明全局 EXT，K_clock 不变）；
   §1 正规形与定义（链、缺陷、certify、Z[1/3] 状态、高度 h、来源移位 s）；
   §2 可认证类（把三个方向中真正 [A] 的部分合并；每个引理列全假设）；
   §3 gateway 链（映射、记录严格下降、高度/分母递推、链长上界或终止条件）；
   §4 障碍 O1/O2/O3：为什么"所有有界高度 s 都安全"是假的，为什么任何参数上界/局部类预算不够；
   §5 目标定理的精确形式：theta+s（s in Z[1/3]，高度<=h）-> 认证 或 有限步 gateway + 严格记录下降，
       界与 J 无关；若只能在附加条件下成立，逐条写出条件，并证明它们不是参数上界；
   §6 J 依赖审计：逐条列出 log* J、N0、2*10^7、T_h 的出现位置，或证明没有；
   §7 标注与状态表（[A]/[B]/[C]、已证/条件/未决）；
   §8 复算命令。
2. verify_landing.py：独立重算（不要只 import 三个脚本）关键的跨方向恒等式与计数：
   有理转移与 gateway 恒等式、仿射判据在规范出口上的表现、gateway 链的记录下降、
   O1 的群论/估值结论的小范围复现、O3 的计数不等式；写 landing_checks.json。
   打印 PASS/FAIL 与计数；只在所有硬检查通过时 exit 0；运行 <10 分钟。
3. 不要把未证明的命题写成 [A]；不要把有限范围写成所有 j；不要引入新的参数上界而不标注。
返回 TheoremDraft。`;
}

function adversaryPrompt(draft: TheoremDraft): string {
  return `${BRIEF}

你是独立挑错者，没有参与起草。读 ${OUT}/THEOREM.md、${OUT}/verify_landing.py、三个方向的 RESULT.md、
四份审阅与两份复核报告、以及 O1/O2/O3 原文。目标：让定理失败。
起草者自述的陈述（供你对照，不当作正确）：
${draft.statement}

逐项攻击：
1. 伪装成来源条件的参数上界：每条假设都问"它是否等价于 j<N 或 omega<N 或 r<r(N)？"
2. 与 J 无关的声称：找 log* J、N0、2*10^7、T_h、有限表大小的隐藏使用；要求反例或明确标注。
3. 有理模式：Q=3^r 可能大于 2^j；|C|/Q<=h 但模 2^{j+1}Q 的代表元很大；x=0/lift bit 是否处理正确。
4. gateway 链：链长上界是否真的有限；若无限，是否等于 O1 的危险族；记录下降是否每步严格。
5. O1：把 P=49 源与 eta_r 代入定理假设；若满足却失败，定理被反驳；若不满足，指出哪条假设拦住它。
6. O2：m>=8 的构造是否被某条假设排除，还是被忽略。
7. O3：定理是否暗中依赖"枚举所有类"？若是，指出计数上界。
8. 标注：[A] 是否真的对所有参数成立？[B] 范围是否写明？
对每条问题给 loc、what、severity、correction（最小反例或缺失假设）。
写 ${OUT}/reviews/theorem_adversary.md。返回 AdversaryResult。
不要修改 THEOREM.md 或任何脚本。`;
}

function revisionPrompt(attack: AdversaryResult): string {
  const items = attack.issues
    .map((x, i) => `I${i + 1} [${x.severity}] ${x.loc}: ${x.what} -> ${x.correction}`)
    .join("\n");
  return `挑错报告在 ${attack.reportPath}。逐条回应并修订：
${items}

要求：
- 每条要么修复（改定理/假设/脚本），要么明确写入"未解决/条件"并说明为什么不能修；不得静默删除。
- 修完后重写 ${OUT}/THEOREM.md 的相关小节与 ${OUT}/verify_landing.py（如需要），确保脚本仍 PASS。
- 返回 RevisionResult：新陈述、条件、parts、artifacts、open、responses（逐条对应 I1..In）。
不要新增未标注的假设；不要声称全局 EXT。`;
}

function notesPrompt(draft: RevisionResult, attack: AdversaryResult, gateExit: number, reviewPaths: string): string {
  return `${BRIEF}

写最终笔记 ${OUT}/NOTES.md（本轮交付物）。输入：${OUT}/THEOREM.md、${OUT}/landing_checks.json、
挑错报告 ${attack.reportPath}、三个方向的 RESULT.md 与 checks.json、四份审阅与两份复核报告（${reviewPaths}）。
修订稿自述的陈述：
${draft.statement}
修订稿自述的条件：${draft.conditions.join("; ")}
结构（参照 work_r1r2/NOTES.md 的风格）：
1. 中文摘要（10-15 行）：结论先行；明确哪些是 [A]/[B]/[C]；明确"未证明全局 EXT、K_clock 不变"。
2. 审阅结论：四份未审文档的标注与错误（只列已复核的；被 refuted 的也写）。
3. 目标定理的精确陈述与证明骨架；逐条写附加条件，并解释为什么它们是来源/相位条件而非参数上界。
4. 三个表示方向各自证明了什么、没证明什么；J 依赖审计。
5. 障碍 O1/O2/O3 如何被处理（或为何仍未解决）。
6. 未解决点与下一步（具体、可执行）。
7. 复算命令（含 gate 退出码 ${gateExit}）与所有 json 路径。
诚实性：不得把条件结果写成无条件；不得声称机器不停机；数值证据标 [B]，猜想标 [C]。
返回一段话说明写了什么；不要修改 THEOREM.md 或脚本。`;
}

function auditPrompt(notesPath: string, attack: AdversaryResult, gateExit: number, reviewPaths: string): string {
  return `${BRIEF}

你是最终独立审计者。检查 ${notesPath}、${OUT}/THEOREM.md、${OUT}/landing_checks.json、
挑错报告 ${attack.reportPath}、三个方向的 RESULT.md 与 checks.json、审阅报告（${reviewPaths}）。
任务：
1. 逐条核对 NOTES 的每个数值/范围/标注能否在 json 或脚本输出中找到；找不到就是 issue。
2. 逐条核对挑错报告的问题是否真的被修订解决（打开 THEOREM.md 对应小节；必要时重算最小反例）。
3. 检查诚实性：是否有"全局 EXT/不停机"的过度声称；K_clock 是否被改动；[A]/[B]/[C] 是否误标；
   条件结果是否被写成无条件；有限范围是否被写成所有 j。
4. 检查复算命令是否可运行（至少抽查 1-2 条；不要重跑已由 gate 决定的 verify_landing.py，gate exit=${gateExit}）。
5. 检查必需文件是否存在：reviews/ 四份审阅 + 两份复核、三个方向的 script/json/RESULT、THEOREM.md、
   verify_landing.py、landing_checks.json。
写 ${OUT}/reviews/final_audit.md。issues 每条以 "NOTES:"、"THEOREM:" 或 "SCRIPT:" 开头。
verdict 只有 pass / issues。返回 FinalAudit。不要修改任何文件。`;
}

async function gateDirection(direction: string): Promise<WorldRunResult> {
  if (direction === "rational") {
    return world.run("python", ["-B", "work_landing_symbolic/rational/verify_rational.py"], { timeoutMs: 900000 });
  }
  if (direction === "affine") {
    return world.run("python", ["-B", "work_landing_symbolic/affine/verify_affine.py"], { timeoutMs: 900000 });
  }
  return world.run("python", ["-B", "work_landing_symbolic/gateway/verify_gateway.py"], { timeoutMs: 900000 });
}

async function runLandingGate(): Promise<WorldRunResult> {
  return world.run("python", ["-B", "work_landing_symbolic/verify_landing.py"], { timeoutMs: 900000 });
}

function gateText(g: WorldRunResult): string {
  return `exit=${g.exitCode}\nstdout:\n${g.stdout.slice(-1400)}\nstderr:\n${g.stderr.slice(-1400)}`;
}

artifact.table("directions", {
  title: "三个表示方向的验证状态",
  columns: [
    { field: "direction", label: "方向" },
    { field: "status", label: "状态" },
    { field: "checks", label: "检查" },
    { field: "failures", label: "失败" },
  ],
  key: "direction",
});

phase("审查四份未审文档");

const baseline = await Promise.all([
  world.run("python", ["-B", "work_c3_drift/verify_rational_mode.py"], { timeoutMs: 300000 }),
  world.run("python", ["-B", "work_c3_drift/verify_odd_denominator.py"], { timeoutMs: 300000 }),
  world.run("python", ["-B", "work_c3_drift/verify_shift_transport.py"], { timeoutMs: 300000 }),
  world.run("python", ["-B", "work_c3_drift/verify_first_a.py"], { timeoutMs: 300000 }),
]);

const baseLine = [
  `RATIONAL_MODE.md -> verify_rational_mode.py: exit ${baseline[0].exitCode}; ${firstLine(baseline[0].stdout)}`,
  `ODD_DENOMINATOR.md -> verify_odd_denominator.py: exit ${baseline[1].exitCode}; ${firstLine(baseline[1].stdout)}`,
  `SHIFT_TRANSPORT.md -> verify_shift_transport.py: exit ${baseline[2].exitCode}; ${firstLine(baseline[2].stdout)}`,
  `FIRST_A_REDUCTION.md -> verify_first_a.py: exit ${baseline[3].exitCode}; ${firstLine(baseline[3].stdout)}`,
].join("\n");
log(`四份未审文档的验证脚本基线：exit ${baseline.map((b) => b.exitCode).join(", ")}`);

const groups: { name: string; docs: DocSpec[] }[] = [
  { name: "R", docs: [DOCS[0], DOCS[1]] },
  { name: "T", docs: [DOCS[2], DOCS[3]] },
];

const reviewed = await Promise.all(
  groups.map(async (g) => {
    const reviews = await Promise.all(
      g.docs.map((d) => agent(`审阅者-${d.short}`, REVIEWER_PERSONA).ask<ReviewResult>(reviewerPrompt(d, baseLine))),
    );
    const check = await agent(`复核者-${g.name}`, CHECKER_PERSONA).ask<CheckResult>(checkerPrompt(g, reviews));
    return { group: g, reviews: reviews, check: check };
  }),
);

const confirmedErrata: Finding[] = [];
let checkedErrors = 0;
for (const bundle of reviewed) {
  let cursor = 0;
  for (const r of bundle.reviews) {
    for (const e of r.errors) {
      const item = bundle.check.items[cursor];
      cursor += 1;
      checkedErrors += 1;
      if (!item) continue;
      if (item.verdict === "confirmed") {
        confirmedErrata.push({
          where: `${r.docFile}:${e.loc}`,
          what: e.what,
          evidence: item.evidence,
          status: "verified",
          severity: e.severity === "critical" ? "high" : e.severity === "major" ? "medium" : "low",
        });
      }
    }
  }
}
for (const f of confirmedErrata) report(f);
log(`审阅完成：${checkedErrors} 条被声称的错误，${confirmedErrata.length} 条经独立复核确认`);

const reviewPaths = reviewed
  .map((b) => `${b.reviews.map((r) => r.reportPath).join(", ")}; 复核 ${b.check.reportPath}`)
  .join("\n");

phase("三个表示方向并行攻关");

const directionResults = await Promise.all(
  DIRECTIONS.map(async (spec) => {
    try {
      const explorer = agent(`探索者-${spec.label}`, spec.persona);
      const plan = await explorer.ask<PlanResult>(planPrompt(spec, reviewPaths));
      await explorer.ask<ImplResult>(implPrompt(spec, plan));
      let gate = await gateDirection(spec.direction);
      let feedback = gateText(gate);
      let rounds = 0;
      while (gate.exitCode !== 0 && rounds < 2) {
        rounds += 1;
        await explorer.ask<string>(fixPrompt(spec, feedback, rounds));
        gate = await gateDirection(spec.direction);
        feedback = gateText(gate);
      }
      const result = await explorer.ask<DirectionResult>(resultPrompt(spec, gate, rounds));
      report(
        {
          direction: spec.label,
          status: gate.exitCode === 0 ? "脚本通过" : "脚本未通过",
          checks: result.checks.slice(0, 160),
          failures: gate.exitCode === 0 ? "0" : "见 stderr",
        },
        "directions",
      );
      return result;
    } catch (err) {
      const failed: DirectionResult = {
        direction: spec.label,
        theorem: `方向未完成：${String(err).slice(0, 300)}`,
        jDependence: "未知",
        gate: "fail",
        checks: "未运行",
        open: ["子代理失败，需要重跑该方向"],
        resultPath: `${spec.dir}/RESULT.md`,
      };
      report(
        { direction: spec.label, status: "子代理失败", checks: "未运行", failures: String(err).slice(0, 120) },
        "directions",
      );
      return failed;
    }
  }),
);
log(`三个方向完成：${directionResults.map((d) => `${d.direction}=${d.gate}`).join(", ")}`);

phase("汇总统一的着陆定理");

const assembler = agent("定理汇总者", ASSEMBLER_PERSONA);
const draft = await assembler.ask<TheoremDraft>(assemblerPrompt(directionResults, reviewPaths));
let theoremGate = await runLandingGate();
let theoremRounds = 0;
while (theoremGate.exitCode !== 0 && theoremRounds < 2) {
  theoremRounds += 1;
  await assembler.ask<string>(
    `verify_landing.py 的决定性运行失败（第 ${theoremRounds} 轮）。输出：\n${gateText(theoremGate)}\n` +
      `修脚本或修测试范围；不得删除硬检查来制造 PASS。若失败揭示定理陈述错误，改 THEOREM.md 的相应小节并说明。`,
  );
  theoremGate = await runLandingGate();
}
log(`verify_landing.py gate: exit ${theoremGate.exitCode}（修复 ${theoremRounds} 轮）`);

phase("请独立的人挑错");

const adversary = agent("挑错者", ADVERSARY_PERSONA);
const attack = await adversary.ask<AdversaryResult>(adversaryPrompt(draft));
for (const issue of attack.issues) {
  report({
    where: `${attack.reportPath}:${issue.loc}`,
    what: issue.what,
    evidence: issue.correction,
    status: "unconfirmed",
    severity: issue.severity === "critical" ? "high" : issue.severity === "major" ? "medium" : "low",
  });
}
log(`挑错完成：${attack.issues.length} 条问题，${attack.survived.length} 条结论在攻击后仍成立`);

phase("修订定理并回应挑错");

const revised = await assembler.ask<RevisionResult>(revisionPrompt(attack));
theoremGate = await runLandingGate();
theoremRounds = 0;
while (theoremGate.exitCode !== 0 && theoremRounds < 2) {
  theoremRounds += 1;
  await assembler.ask<string>(
    `修订后 verify_landing.py 失败（第 ${theoremRounds} 轮）。输出：\n${gateText(theoremGate)}\n修脚本；不得删硬检查。`,
  );
  theoremGate = await runLandingGate();
}
log(`修订后 gate: exit ${theoremGate.exitCode}`);

phase("写出最终笔记并做诚实性审计");

const notesWriter = agent("笔记作者", NOTES_PERSONA);
await notesWriter.ask<string>(notesPrompt(revised, attack, theoremGate.exitCode, reviewPaths));

const auditor = agent("最终审计者", AUDITOR_PERSONA);
let audit = await auditor.ask<FinalAudit>(auditPrompt(`${OUT}/NOTES.md`, attack, theoremGate.exitCode, reviewPaths));

if (audit.verdict === "issues") {
  const theoremIssues = audit.issues.filter((x) => x.startsWith("THEOREM:") || x.startsWith("SCRIPT:"));
  if (theoremIssues.length > 0) {
    await assembler.ask<string>(
      `最终审计发现定理/脚本问题，请逐条修复并说明：\n${theoremIssues.join("\n")}\n` +
        `修完确保 verify_landing.py 仍 PASS；不得删硬检查。`,
    );
    theoremGate = await runLandingGate();
  }
  await notesWriter.ask<string>(
    `最终审计发现以下问题，请修订 ${OUT}/NOTES.md（不得删除证据链；不能修的写成未解决点）：\n${audit.issues.join("\n")}`,
  );
  audit = await auditor.ask<FinalAudit>(auditPrompt(`${OUT}/NOTES.md`, attack, theoremGate.exitCode, reviewPaths));
}
log(`最终审计：${audit.verdict}`);

const publishedNotes = await (async () => {
  try {
    await artifact.file("notes", `${OUT}/NOTES.md`, {
      title: "着陆符号论证：最终笔记",
      description: "结论、[A]/[B]/[C] 标注、未解决点与复算命令。",
      primary: true,
    });
    return "published";
  } catch (err) {
    return `failed: ${String(err).slice(0, 200)}`;
  }
})();

let publishedTheorem = "published";
try {
  await artifact.file("theorem", `${OUT}/THEOREM.md`, {
    title: "统一着陆定理（含附加条件）",
    description: "THEOREM.md：正规形、可认证类、gateway 链、障碍与 J 依赖审计。",
  });
} catch (err) {
  publishedTheorem = `failed: ${String(err).slice(0, 200)}`;
}

const passed = directionResults.filter((d) => d.gate === "pass").length;
const findings: Finding[] = confirmedErrata.slice(0, 12);
for (const issue of attack.issues.slice(0, 8)) {
  findings.push({
    where: `${attack.reportPath}:${issue.loc}`,
    what: issue.what,
    evidence: issue.correction,
    status: "unconfirmed",
    severity: issue.severity === "critical" ? "high" : issue.severity === "major" ? "medium" : "low",
  });
}
for (const d of directionResults) {
  if (d.gate === "fail") {
    findings.push({
      where: d.resultPath,
      what: `${d.direction} 方向的验证脚本未通过`,
      evidence: d.checks,
      status: "verified",
      severity: "high",
    });
  }
}
for (const issue of audit.issues) {
  findings.push({
    where: `${audit.reportPath}`,
    what: issue,
    evidence: "最终审计（见报告）",
    status: "verified",
    severity: "medium",
  });
}

const verifiedList = [
  `四个基线验证脚本 exit: ${baseline.map((b) => b.exitCode).join(", ")}`,
  ...directionResults.map((d) => `${d.direction} 方向脚本 gate=${d.gate}（${d.checks.slice(0, 120)}）`),
  `verify_landing.py exit=${theoremGate.exitCode}`,
  `最终审计 ${audit.verdict}（${audit.reportPath}）`,
  `NOTES.md ${publishedNotes}；THEOREM.md ${publishedTheorem}`,
];

const notCovered = [
  "s in Z[1/3] 的一般来源公式：另一位研究者仍在推导，本轮只把 s 当参数",
  "J >= T4 的深部日历与全局控制；H5/C7/RES 等已接受的残余条件未在本轮证明",
  "规范实例只覆盖 Calendar(512)/小表可达范围；合成状态不可规范（已在各 json 标注）",
  "未证明全局 EXT、未证明机器不停机；K_clock 不变",
];
if (passed < 3) {
  notCovered.push(`${3 - passed} 个方向的验证脚本未通过，其结论只能算未完成`);
}

const conclusion =
  `三个表示方向中 ${passed}/3 通过了决定性脚本；统一笔记已写入 ${OUT}/NOTES.md。` +
  `核心陈述（摘自修订稿）：${revised.statement.slice(0, 700)} ` +
  `本轮未证明全局 EXT，K_clock 不变；附加条件、障碍处理与未解决点见 NOTES.md。`;

return {
  conclusion: conclusion,
  findings: findings,
  verified: verifiedList,
  notCovered: notCovered,
};
