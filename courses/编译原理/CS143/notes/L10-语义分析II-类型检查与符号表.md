# L10 语义分析 II：类型检查、作用域与符号表

> 讲次：CS143 L10 ｜ 阅读：龙书 ch6.1-6.3, 6.5, ch5.6 ｜ 配套：projects/03_semantic（对应 PA3）

## 核心概念

### 静态 vs 动态检查
- 静态（编译期）：作用域一致性、类型兼容、参数个数、return 路径——COOL/MiniC/Java 的主体。
- 动态（运行期）：数组越界、类型标签检查（COOL 的 `x.f` 要等 x 具体化）——静态检查看不到的部分必须有人兜底。
- 可判定性边界：类型检查器只保证"检查得过的程序不出这类错"，停机问题保证不存在完备静态检查（→ 与 CBMC/abstract interpretation 的联系见"跨课程"）。

### 作用域与符号表
```
数据结构（projects/03 实现）：
class SymbolTable { vector<Scope> stack;   // 每个 Scope: unordered_map<name, Symbol>
  Symbol = { kind: Var|Fun, type, 函数额外: 形参表 } }
操作: enterScope / exitScope / insert(冲突则 shadow 或报错) / lookup(自顶向下找首个)
COOL 规则：嵌套 let 作用域自左向右可见；形式参数遮蔽同名字段。
C 规则：块级作用域；projects 用与 C 一致的嵌套块语义。
```
- 绑定（binding）产生偏移（offset）：同一作用域内变量按序分配帧内槽位——语义分析顺手完成 L11 激活记录的部分布局。

### 类型检查算法（MiniC/COOL 规模）
1. 自顶向下遍历 AST，携带环境（继承属性 expected type 的风格，L9 的复现）。
2. 自底向上综合出每个表达式的类型：`type(e1 op e2)` 按运算规则表。
3. 子类型规则（COOL 特有）：`e1 <= e2`（整数序）、String 字面量 → String、`case/if` 分支类型求**最小公共祖先**（LCA）：
```
type(if c then e1 else e2) = lub(type e1, type e2)  // 类层次上最近公共祖先
lub 计算：先对齐深度再同步上移——类层次预处理 parent 链。
```
4. 报错策略：每个错误节点报告一次并给节点"哨兵类型 Error"，防止错误级联刷屏。

### 函数签名的两遍法
- 先收集全部函数头进符号表（允许前向引用/递归），再检查函数体——**任何语言只要有互递归就需要这一趟**。

## 与前后讲的联系
- 输入是 L5-L8 的 AST；输出是"类型标注 + 符号表绑定"的 AST，交给 L12-L13 生成 IR。
- 符号表是贯穿线：L1 就预告了它；L11 的帧布局、L18 的类表都复用它的数据结构。
- 与 L9：作用域解析是"继承属性"最典型的应用（环境向下传，类型向上汇）。

## 跨课程联系
- **CS242/CS3110**：COOL 子类型 vs OCaml 结构类型 vs Rust 特质——名义子类型（类层次 LCA）与类型推断的分野在这里最清晰；"类型检查是语言合同的一部分"由 CS242 的合同视角命名。
- **CSAPP**：静态作用域 = 编译期可解的偏移；动态作用域（Perl/早期 Lisp）= 运行时查名字——CSAPP 的"链接时符号解析"是介于两者之间的第三种绑定期。
- **6.006/CS170**：lub/LCA 是欧拉巡回 + RMQ 的经典用例（类层次查询）。
- **Z3/形式化**：完整程序等价性不可判定，但有界模型检查（CBMC）用 SMT 在固定展开深度内"检查到底"——把本讲的"可判定边界"变成工程参数。

## 开源项目中的应用
- **rustc**：`cargo check` 只做本讲这一步（解析+缩合+类型检查）不生成代码——语义分析作为独立产品。
- **clang**：`Sema Checking` 文档 + `-fsyntax-only` 同样暴露"只检查"的编译模式。
- **tree-sitter + 语言服务（LSP）**：IDE 类型提示需要"残缺代码上也能跑"的符号表与类型推断——错误恢复要求比编译器更激进。
- **CPython**：`ast` 模块的 symtable.c 就是教科书 scoping 实现；mypy 的 binder.py 是纯 Python 版符号表+类型检查。
- **RPython**：翻译器第一步就是 RPython 类型流分析（本质全局类型检查），检查不过直接拒绝翻译。

## 延伸阅读
- 龙书 ch6.1-6.3 全部例题 + ch5.6（hyphen 消歧：词法-语义接界的轶事级案例）。
- COOL Manual "Static Semantics" 一节逐条对照 projects/03 的规则表。
- Cardelli "Type Systems"（ACM CSUR 1997，短而全）；Pierce TAPL ch13-15（算法视角）。
