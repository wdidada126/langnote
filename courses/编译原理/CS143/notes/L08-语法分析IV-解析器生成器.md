# L8 语法分析 IV：解析器生成器 yacc/bison

> 讲次：CS143 L8 ｜ 阅读：龙书 ch4.9 ｜ 配套：CS143 PA2 实际使用 bison + flex（本讲读 .y 骨架即懂）

## 核心概念

### .y 文件的解剖（bison 输入）
```
%{ #include 头文件（用户代码） %}
%token INT BOOL IF WHILE SEMI ...      ← 来自 flex 的 token 枚举
%left '+' '-'                          ← 结合性声明 = 手工消解算符二义
%right '='
%type <node> exp stmt                  ← 属性类型：归约结果塞进 AST 指针
%%
program : func_list      { globalAST = $1; }        ← 规则体 = 归约动作
        ;
exp     : exp '+' exp    { $$ = new AddExp(@$, $1, $3); }
        | INT            { $$ = new IntConst(@1, $1); }
        ;
%%
```
- `$n` / `$$`：属性栈的读写；`@n`：位置信息（flex 的 YYLTYPE 传行号）。
- 声明优先级后，悬挂算符二义被生成器自动消解为移进/归约偏好——L7 冲突知识的"用户友好封装"。

### flex + bison 握手协议
- bison 生成的分析器循环调用 `yylex()` 拉 token；`yylval`/`yylloc` 携带值与位置。
- COOL 课程改造：不提供 yylex，而由 `cool-lex.cc` 暴露 `get_next_token(TokenElement&)`，PA1 的 tokenizer 直接对接——协议不变，只是词法来自手写。
- 错误钩子：`yyerror()`——分析器的 panic-mode（L6）在生成器里就是一次 yyerror + 丢弃 token。

### 生成器 vs 手写递归下降的取舍（课堂辩论题，PA2/PA1 各站一边）
- 生成器：文法即文档；LALR 覆盖面大；改文法不改代码；表驱动易出状态机级性能。
- 手写：错误消息质量（"期望 ;，找到了 }，可能是第 12 行 if 缺括号"级别的诊断）；AST 构造直接；无生成器依赖；现代编译器（rustc/Swift/Kotlin/Zig）几乎全部回到手写——**IDE 需要的是"永远不要放弃解析"的弹性**，LALR 在错误点上会整体罢工，递归下降可以任意恢复。
- tree-sitter 的出现（GLR + 错误节点实体化）是第三条路：生成器的文法驱动 + 手写的容错。

## 与前后讲的联系
- L5-L7 的算法被封装成黑盒后，本讲教你"当用户"；L9 的属性文法在 `.y` 里以动作代码的形态第一次真正运行。
- PA2 交付物 = 一个 `.cl` 程序 → 良构 AST；从这讲起错误从"我的代码 bug"变成"用户程序的 bug"，测试基线（.out 文件比对）成为课程工作流。

## 跨课程联系
- **CS3110**：在 OCaml/Haskell 里用 parser combinator 写同样的文法——函数式视角下 bison 的"动作+归约"就是 fold；三种流派（表驱动/递归下降/组合子）对照即是本讲的实践版。
- **6.031（软件工程）**：生成器 = "规格与实现分离"的极端案例；`.y` 是规格，表是实现。
- **CS242**：文法+优先级声明 ≈ 运算的"代数规格"；讨论 Swift 的 operator precedence 设计文档可见同一问题在语言设计层的延伸。

## 开源项目中的应用
- **GCC**：c-parse.y 曾长期是 C 前端；现仍用 bison 生成（C++ 模块仍在演进），`gcc -fdump-tree-original` 可观察其产物。
- **CPython**：2020 年前是 bison 生成的 LL(1)（Grammar/A）；PEG 替换案例说明"生成器换算法"是大工程。
- **tree-sitter / ANTLR**：现代生成器双雄；ANTLR 的 .g4 同时驱动分析器+IDE 高亮+代码补全（一份文法多处复用）。
- **RPython**：PyPy 的 ooflow 解析层由 Python 语法生成——生成器输出 IR 而非树，是 L12 视角的变体。

## 延伸阅读
- 龙书 ch4.9；bison 手册前三章 + "Advanced Grammar Features"（合并规则 %nonassoc、中缀 %destructor）。
- Doug Brown, "The Yacc Companion"（O'Reilly）；Levine, "flex & bison"（O'Reilly, 2012）。
- 对比读物：Kotlin 官方博客 "Making our compiler error-tolerant" 与 "Parsing tricks" 系列（一手工程理由：为何 IDE 场景放弃表驱动）。

## 自测问题
1. 把 COOL 的 `factor : primary '(' actuals ')'` 规则翻译成 .y 的一条规则（含 AST 构造动作）。
2. `%left '-' '+'` 与 `%right '='` 各自消解了什么冲突？若都漏写会怎样？
3. flex+bison 握手依赖哪三个全局量？（答：yylex/yylval/yylloc 及其对应物）
4. 为"IDE 输入中途"场景设计：给 projects/02 的 parseIf 加"缺少右括号时仍返回部分 AST"的恢复策略，写出伪码。
5. 若让你把 projects/02 改成 bison 版：列出 .y 需要定义的全部 %token/%left/%type 清单项。
