# 第20章 Guidelines支持库 — GSL: The Guidelines Support Library

> 本章目录版：[← 00-总览与阅读地图](00-总览与阅读地图.md) ｜ 单文件笔记：[../C++CoreGuidelines解析.md](../C++CoreGuidelines解析.md) ｜ 系列导航：[../C++系列·总索引.md](../C++系列·总索引.md)

**本章对象**：current master 实测 GSL 节**没有编号规则**（无 `GSL.n` 标题，grep 验证），
而是 6 个子节的**设施工厂**：GSL.view（视图）、GSL.owner（所有权指针）、GSL.assert
（断言）、GSL.util（杂项工具）、GSL.concept（概念）、GSL.ptr（智能指针概念）。FAQ.50–60
11 条问答专门答辩 GSL 的身份问题。定位一句话：**没有这些设施，指南就得对语言本身施加
多得多的限制**（GSL 节首原话的意译）。⚠️ 本书第 20 章与此节的对应系推断映射。

## 核心概念速览（中英对照）

- **支持库** — guidelines support library：一小族命名于 `gsl` 的类型/别名，给规则当落点
- **中转namespace** — indirection through `gsl`：名字可指标准库亦可在标准缺席时补位，
  留出实验与本地变体空间
- **视图/非拥有** — views are never owners (GSL.view)：`T*`/`T&`/`span`/`zstring` 一律借用
- **`owner<T*>`** — 标记住有指针：给"升不了 RAII handle"的遗留代码贴的唯一合法所有权标签
- **`not_null<T>`** — 非空承诺：把"别传 nullptr"从注释升格为类型（可包裹 owner）
- **`span<T>`** — 序列视图：`[p:p+n)`，GSL 版**默认带边界检查**（与 std::span 的唯一分歧，
  且承诺跟随标准演进、必要时退役）
- **`zstring`/`czstring`** — C 串类型名：区分"指向单个 char 的指针"与"以 0 结尾的串"
- **`stack_array`/`dyn_array`** — GSL.owner：栈上定长数组/构造定终身的不扩容堆数组
  （FAQ.57/58 逐条否认与 std::array/vector/dynarray 提案等同）
- **`Expects`/`Ensures`** — GSL.assert：前置/后置契约占位符，"不是 assert，是语言合约的
  预置语法"（FAQ.59/60 原文否认）
- **`finally`** — GSL.util：`final_action{f}`，析构即执行——NR.6 的正向解药
- **`narrow`/`narrow_cast`** — GSL.util： checked 收窄（不等则抛 `narrowing_error`）与
  明示放弃检查的 `static_cast` 别名（ES.46 的执法双轨）
- **`gsl::index`** — GSL.util：索引专用有符号类型（`ptrdiff_t` 别名），ES.107 的落点
- **`joining_thread`** — GSL.util：会 join 的 thread，CP.25 钦定 `std::thread` 替身
- **GSL.concept** — Origin/Range/TR 血统的概念集，逐条在 C++20 找到 `std::` 同义替身
- **`Pointer`/`Unique_pointer`** — GSL.ptr：给智能指针本身立概念（可解引用+可移动+不可复制）

## 动机：规则需要"词汇表"

448 条规则里大量条款的"正确写法"在 2015 年的标准库里**不存在**：没有 span 就没法替代
指针+长度对（I.13/Bound.1），没有 variant 化 narrowing 工具就只能禁窄化（ES.46），没有
joining 语义的 thread 就注定有 terminate 陷阱（CP.25）。GSL 的战略是"**先造出来用，
再把好的送进标准，然后删掉自己**"（FAQ.53 自供：它们是临时设施，目标是被标准库同能力
类型就地替换）。读 GSL 节 = 读一份"2015 年标准库缺口清单"——而 C++17/20 恰好逐项销账。

## 机制：六子节的分工

- **GSL.view 定语义坐标**：两轴四象——拥有/借用 × 单对象/序列。`owner<T*>` 是唯一被
  允许"拥有但不管理"的记号（仍要手工 delete，故 R.20 说优先 unique_ptr，owner 只是
  遗留/ABI 场景的墓碑标签）；其余裸指针一律解读为**非拥有、可空、指向单对象**。
- **GSL.owner 给拥有者花名册**：`unique_ptr`/`shared_ptr`（直接就是 std 名）+ 两个
  未标准化的数组容器（stack_array/dyn_array，现状：无人推进，事实上废弃——见演进节）。
- **GSL.assert 立契约占位**：`Expects(p)` 违即 terminate，语义上**不受 NDEBUG 管辖**
  （这是与 assert 的分水岭，FAQ.59 的"placeholder"指语法将来归语言）。
- **GSL.util/GSL.concept/GSL.ptr**：分别是"规则动词表"、"类型形容词表"、"指针抽象表"。

## 代表性设施深解析（设施 → 服务的规则 → 现代承接）

### `owner<T*>` → R.3/R.20（new 之后别裸传，所有权要显式） → 🔧 实测复制即编译错误

- 定义要点（view 子节原文）：`owner<T>` 区别于资源 handle 的地方**恰恰是它仍要求显式
  delete**——它是"我保证这块归你管"的类型化注释，不是智能指针。FAQ.56 特别澄清它
  **不是** `observer_ptr` 的反义词营销（observer_ptr 标**非**拥有，owner 标**拥有**，
  且 owner 可施加于任意间接类型）。
- 🔧 **实测两连（已实测 g++ 15.2）**。因本机未安装 Microsoft/GSL 头（⚠️ 环境缺口，19 章
  已记），按 FAQ.51"任何人都可实现"的授权手抄了最小教学版（**非**官方 GSL，仅演示语义）：

  ```cpp
  #include <cstdio>
  template <typename T> struct owner {            // pedagogical mini-GSL, NOT Microsoft GSL
      T* p;
      explicit owner(T* q) : p(q) {}
      ~owner() { delete p; }
      owner(const owner&) = delete;               // R.20: ownership is unique
      T& operator*() const { return *p; }
  };
  int main() {
      owner<int> o{new int{42}};
      std::printf("*o=%d, non-owning view=%d\n", *o, *o.p);
  }
  ```

  `g++ -std=gnu++23` 编译运行，真实输出：`*o=42, non-owning view=42`——拥有者（o）与
  借用者（`o.p` 这个裸 T*）同屏，正是 GSL.view 语义坐标的最小标本。
  再试复制拥有权（`owner<int> b = a;`，GSL 语义里这行不该存在——真正要传的是视图）：

  ```text
  error: use of deleted function 'owner<T>::owner(const owner<T>&) [with T = int]'
  ```

  编译器把"所有权不可复制"从纪律（R.20 的措辞）变成了**物理**。
- 现代承接：这条设施几乎已被 `std::unique_ptr` 事实上兼并——今天新项目直接 R.3 用
  智能指针；`owner` 的剩余领地就是它自述的三条（转换成本、ABI、handle 实现内部）。

### `span` → Bounds.1/ES.107/I.13 → `std::span`（P0896R4，302 已验）完成销账

- GSL 节那段罕见的"命名变更说明"原文值得完整转述：gsl::span（前身 array_view）被标准
  采纳为 std::span 后，GSL **改名让位并逐面对齐接口**，唯一保留的分歧是 **GSL span 默认
  全时边界检查**；若未来 std::span 自己带上检查，gsl::span 即删除。FAQ.55 给了三段
  决策表：只读无检查→`std::string_view`（C++17）；读写无检查→`std::span<char>`（C++20）；
  要检查→`gsl::span`。
- 这是"**过渡库的标准退出协议**"范本，也是 16 章 SL.2（先标准库）的时间差注解：
  2015 年 gsl::span 是先行者，2020 年后它是债。
- 16 章实测过 `std::span` 的越界行为（默认不查）；查的行为差异就是 FAQ.55 的整个存在理由。

### `Expects`/`Ensures` → I.6/P.4（契约入码） → 语言化进行中（21 章主讲）

- 当前形态自供"是宏（yuck!）"、只能写在函数体内——宏之丑正是占位诚意：等 `[[pre]]` 系
  语法（原文点名的契约提案链，P2900R14/P2388R4 均已 302 验证）落地即退位。
- 与 19 章 `_GLIBCXX_ASSERTIONS` 的断言消息同族对照：库内断言（供应商预置）vs 契约
  （作者显式）——Expects 的 terminate 语义 + 可控执法（选项化消息/替代动作）是运行期
  防线的"用户可编程层"。

### GSL.util 三件套：`narrow` / `finally` / `joining_thread` → ES.46 / NR.6·E.16 / CP.25

- `narrow<T>(x)`：值保持性检查版收窄，失配抛 `narrowing_error`；`narrow_cast` 则是
  "我就是不要检查"的**自我署名**（=static_cast 换皮）。ES.46 的执法双轨在 8 章 🔧 实测过
  其反面（-Wnarrowing 编译错误级）。
- `finally(f)`：作用域退出必执行 f——给禁异常域提供 NR.6 的替代清场方式（E 章 re-finally）。
- `joining_thread`：CP.25 原文"Prefer `gsl::joining_thread` over `std::thread`"，
  10 章 🔧 实测 std::jthread 已给出标准答案（-static 环境与 iterations=168 输出见彼章）——
  GSL 又一销账案例。

### GSL.concept 17 连 → T 章概念先行军 → C++20 全表平移

- master 原文逐条给了 `std::` 对应：`Range→std::ranges::range`、`Regular→std::regular`、
  `Function→std::invocable`、`Predicate→std::predicate` 等——血统注明借自 Andrew Sutton
  的 Origin 库、Range 提案与 PA TR。读它最好的姿势是当**考古对照表**：concepts 标准化
  过程中哪些名字被保留、哪些被改名（Function→invocable 是最著名迁葬）。
- 13 章 🔧 实测的 `std::integral` 约束拒绝（candidate/constraints not satisfied 输出）
  就是这条销账线的运行现场。

## 权衡与边界

- **GSL 的分裂现实**：FAQ.52 拒绝官方实现、FAQ.51 拒绝承认 Microsoft/GSL 的正统性——
  "接口规范"承诺至今停留在"too sparse, 计划补 WG21 式接口说明"的自供里。实践后果：
  各家 GSL 实现的 span 检查行为、not_null 诊断细节互有出入，可移植执法（19 章）在 GSL
  层其实**未达标**。
- **依赖决策**：新项目为 `narrow`/`index` 引整个 GSL 值不值？abseil 给出第三答案
  （`absl::Span`/`absl::variant` 线，不承诺检查语义）；纯 std 路线则 2025 年代已可
  覆盖 span/string_view/jthread/expected（11 章实测），GSL 剩余刚需只有 Expects/Ensures
  与 not_null 的"强制非空检查"变体。
- **`owner` 的哲学税**：它让"注释型类型别名"进入语言（GSL 文档自认 `[[implicit]]`、
  `move_owner` 条目还挂着 `???`）——占位符密度是全指南最高的一节，诚实读法是把每个
  存疑条目当 TODO 而不是钦定。

## 相邻概念对比

- **GSL vs 标准库（16 章）**：SL.3 禁向 std 加东西，GSL 用 `gsl` namespace 打擦边球——
  恰是"临时设施"身份的语法表达。
- **GSL vs Boost（FAQ.53）**：Boost 路线=先社区库后标准（周期以年计）；GSL 路线=指南
  直属、随规则即用即弃。GSL 明确拒绝 Boost 孵化，代价就是上面的正统性困境。
- **`not_null<T>` vs `Expects(p != nullptr)`**：类型检查在**入口**（构造即验）vs 断言在
  **使用点**——前者让不可能状态不可表示（2 章 P.4/6 章 Enum.1 的同一哲学），是"设计类型"
  与"防御代码"的分界标本。
- **mini-GSL 教学版 vs 官方**：🔧 样品的 owner 只有删除拷贝这一条语义，官方 not_null/GSL
  span 有完整检查、诊断与 constexpr 化——样品的结论（不可复制、可借用）可迁移，
  行为细节不可引用。

## 最新演进与工业实践

- 销账进度表（以 current master 口径实测）：span→std::span（C++20，P0896R4）✓；
  joining_thread→std::jthread（C++20）✓；概念集→std concepts（C++20，P0898R3）✓；
  zstring 系→无标准对应（C++23 `std::print` 的 `{}` 语义弱化其需求）；
  stack_array/dyn_array→**事实废弃**（dynarray 提案线死透，未再出现于任何近期邮件列表
  决议）⚠️（判断依据：master 文本仍挂而无 std 对应，未核对提案编号史）。
- Microsoft/GSL 仓库仍在维护（span 的 `_MSVC_IMPL` 检查、not_null 与 std::compare 三-way
  适配），abseil 部分重叠但拒绝 Expects 词汇——合约词汇统一最终押注 P2900 语法（21 章）。
- C++26 展望：若最小合约（P2388R4）先船到，GSL.assert 将是最先整节删除的对象；
  GSL.util 的 `narrow` 则可能随 safe-numerics 线（⚠️ 本次未做提案号验证，不落编号）
  重新洗牌。
- 工业案例：LLVM/Clang 源码以自家 `llvm::ArrayRef` 完成 span 的职能（早于 std::span 十年），
  印证 GSL 的"接口先行、名字随意"哲学——同一缺口，各家自填，GSL 提供的是**填法的语义标准**。

## 延伸阅读

- 上一站：[19-规格配置](19-规格配置.md) ｜ 下一站：[21-附录AC](21-附录AC-施行概念与契约.md)
- 被 GSL 服务的规则章：[07-资源管理](07-资源管理.md)（owner/R.3） ｜
  [10-并发](10-并发.md)（CP.25） ｜ [08-表达式和语句](08-表达式和语句.md)（ES.46/107）
- 智能指针概念的正统展开：[../Effective_Modern_C++/04-智能指针.md](../Effective_Modern_C++/04-智能指针.md)
- 原版 GSL 节：<https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>#s-gsl ｜
  Microsoft/GSL：<https://github.com/Microsoft/GSL>
