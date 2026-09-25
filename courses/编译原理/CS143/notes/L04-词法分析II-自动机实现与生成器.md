# L4 词法分析 II：自动机实现与词法器生成器

> 讲次：CS143 L4 ｜ 阅读：龙书 ch3.7-3.9；Flex 手册 ｜ 配套：projects/01_lexer 完成后阅读本讲

## 核心概念

### 两种 DFA 实现风格
1. **表驱动**：`state = T[state][ch]`，转移是数据不是代码。紧凑（可稀疏压缩），但每字符一次数组访问。
2. **goto 编码（手工）**：每个状态一段代码，转移隐含在控制流里。快（分支预测友好），但代码量随类别数膨胀。
- COOL/CS143 传统：**手写词法器**（PA1 明确禁用 flex），目的正是体验状态机编码、最长匹配与错误恢复。

### 词法器骨架（伪码，对应 projects/01）
```
loop:
  skip blanks/newlines (更新 line/col)
  ch = peek()
  match ch:
    letter  -> 循环吸收 [letter|digit|_]*，查关键字表，返回 IDENT/KW
    digit   -> 吸收 digit+，处理 '.' 分支：若后面不是 digit 则**回退输入指针**（最长匹配的回溯点）
    '"'     -> 吸收至 '"'；遇 '\n' 或未闭合 → 词法错误并恢复
    '<'     -> 前瞻 '=' → LE，否则 LT
    '/'     -> 前瞻 '/' 行注释；'/*' 块注释（COOL 为 (* *) 且需嵌套计数）
  返回 {token 类型, lexeme, 行号}
```
要点：
- **前瞻（lookahead）与回退（putback）**：一个字符的 lookahead 缓冲即可处理 `3.14` vs `3.` vs `...`。
- **最长匹配 vs 首匹配**：关键字不是特殊 token——先按标识符 DFA 走再查表，天然保证 `intx` 不是 `int`+`x`。
- **嵌套注释**：无界深度严格说超出正则能力；实践要么设深度上限把状态有限化（仍是 DFA），要么在词法器里放一个显式计数器（退化为带栈/计数器的自动机）。projects/01 选择计数器方案并注明。

### Flex 的工作方式（L8 的 yacc 前半）
- 规格 = 正则 → 动作；生成器构造 DFA 转移表（等价类压缩列），输出 C 的 `yylex()`。
- 默认最长匹配 + 规则先后破平；`yylval` 携带属性（数字值、字符串指针）。
- Flex 手工接口与 COOL 提供的 `string::tokenize()` 接口在 PA2 汇合：bison 调 `get_next_token()` 拉取 token。

## 与前后讲的联系
- 承接 L3 的数学（正则/DFA），本讲交付工程实现；下一讲 L5 语法分析消费 token 流。
- token 设计影响后续一切：属性位置（行号）决定 L10 报错质量；字符串 unescape 放词法层是惯例。
- PA1 的测试（good/string/classtest 等 .cl + .out 基线）是"按规格文档写测试"的编译课版本。

## 跨课程联系
- **6.006/CS170**：表驱动的 char-class 压缩是"等价类划分"技巧（与后缀数组/LZW 同源）。
- **CSAPP**：goto 版词法器的 switch 跳表与 `jumptable` 机器级表示可直接对照 objdump 观察。
- **DDCA/CS61C**：一个 DFA 状态寄存器 + 组合逻辑即可 RTL 实现词法器——硬件 regex 加速器（如 Aho-Corasick 网卡）是同一件事的极致。
- **CS61A**：正则表达式的递归下降解释器（小 Scheme 求值器）与本讲"把规格变成可执行状态机"互补。

## 开源项目中的应用
- **Flex**：本讲主角；GCC/CPython 等仍大量使用 flex+bison 组合。
- **rustc**：`rustc_lexer` crate 是 Unicode-aware 手工词法器，文档明确解释"为何不用生成器"（错误恢复策略需要自定义）。
- **V8 / SpiderMonkey**：JS 词法受 ASI（自动分号插入）污染，词法器必须与语法层协商——反例：词法不总是独立可判。
- **tree-sitter**：词法 DFA 由 grammar.js 内联正则编译而来，支持运行时外部扫描器（外部词法）处理 heredoc。
- **CPython**：3.12 起词法器从 tokenizer 重写为 PEG 生成器的"终端"层，说明词法/语法边界在工程上可以移动。

## 延伸阅读
- 龙书 ch3.6（词法分析器生成器构造细节，含等价类）；Flex 手册 "Using Flex"。
- rustc_lexer 源码（crate 极小，适合对照 projects/01 精读）。
- Appel "Modern Compiler Implementation in C" ch2（手写词法器一章的范本）。
