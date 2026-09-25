# 第 6 章 编译器前端工具：用 Antlr 生成词法、语法分析器（讲 06、07）

> **一句话**：手写递归下降累死人，于是有了 yacc、ANTLR 这类「语法文件 → 代码生成器」。心智模型可以一句话说完——**就像 protobuf：`.proto` 文件本身不可执行，靠 `protoc` 生成各语言代码；`.g4` 也一样，靠 `antlr` 生成 parser。**

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 6.1 | 「像 protobuf 一样」的心智模型 | `.y` / `.g4` / `.proto` / `.thrift` / `.tars` 是同一类东西 |
| 6.2 | yacc 的 `.y` 长什么样 | 三段式：声明段 / 产生式段 / 程序段 |
| 6.3 | ANTLR 的 `.g4` 长什么样 | lexer 规则 + parser 规则 + 一个 start rule |
| 6.4 | 生成物的用法 | Parser / Listener / Visitor 三类产物 |
| 6.5 | 监听器 vs 访问器 | 事件驱动 vs 树遍历，选哪个 |
| 6.6 | StringTemplate 与代码生成 | ANTLR 3 时代的强绑定，ANTLR 4 的取舍 |
| 6.7 | Unicode 与错误处理 | 现代 ANTLR 的两条硬门槛 |
| 6.8 | 重构脚本语言（讲 07） | 用 ANTLR 重写讲 05 的 parser |

---

## 核心精讲

### 6.1 心智模型：`.g4` 就是编译器的 `.proto`

用户原摘录的这段类比非常准，值得展开成一张表：

> yacc 类工具的共同特点就是，通过编写 `.y` 格式的说明文件定义语法，然后使用 yacc 命令行工具生成对应语言的源代码。
> 所以它尝起来就比较像 protobuf，`proto` 文件就像 `.y` 文件一样本身不可执行，需要用一些 `protoc` 工具来生成对应每种语言的源代码文件。

| 工具 | 语法文件 | 生成器 | 产出 |
| --- | --- | --- | --- |
| **yacc / bison** | `.y` | `yacc` | `.c` 里的分析器 |
| **ANTLR** | `.g4` | `antlr` | Java/Python/Go/C#/TS… 的 parser |
| **protobuf** | `.proto` | `protoc` | 各语言的序列化代码 |
| **thrift** | `.thrift` | `thrift` | 各语言的 RPC/序列化代码 |
| **tars** | `.tars` | `tars2java` 等 | 各语言的 RPC 代码 |

**这个类比真正的价值在下面三点**：

1. 语法文件是**机器可读的契约**——人和工具、不同语言之间共享同一份定义。
2. 生成器是**一次性的**——语法不变就不用重新生成，但要进版本库。
3. 生成物**不该被手改**——改语法文件，重新生成，这是纪律。

### 6.2 yacc 的 `.y`：三段式

```yacc
/* 教学示意：yacc 的 .y 文件骨架（不参与构建） */
%{
#include <stdio.h>
void yyerror(const char *s);
int yylex(void);
%}

%token NUM PLUS MINUS
%left PLUS MINUS                 /* 优先级与结合性（见讲 04） */

%%                               /* 以下为产生式段 */
expr   : expr PLUS expr  { $$ = $1 + $3; }
       | expr MINUS expr { $$ = $1 - $3; }
       | NUM             { $$ = $1; }
       ;

%%
int main(void) { yyparse(); return 0; }
void yyerror(const char *s) { fprintf(stderr, "错误：%s\n", s); }
```

生成：`yacc -d calc.y` → `y.tab.c` + `y.tab.h`。

### 6.3 ANTLR 的 `.g4`：lexer 与 parser 同文件

```antlr
/* 教学示意：ANTLR 4 的 .g4（不参与构建） */
grammar Expr;

/* parser 规则（以小写开头） */
prog     : stat+ EOF ;
stat     : expr ';'                            # exprStat
         | ID '=' expr ';'                    # assignStat
         | 'print' expr ';'                   # printStat
         | 'if' '(' expr ')' block            # ifStat
         ;
block    : '{' stat* '}'                      # blockStat
         ;
expr     : expr op=(MUL|DIV) expr             # mulExpr
         | expr op=(PLUS|MINUS) expr          # addExpr
         | ID                                 # idRef
         | NUM                                # numLit
         | '(' expr ')'                       # parenExpr
         ;
/* 下面两行给上面产生式定优先级：写在越前面的优先级越低，ANTLR 自动处理直接左递归 */

/* lexer 规则（以大写开头） */
MUL : '*' ; DIV : '/' ; PLUS : '+' ; MINUS : '-' ;
ID  : [a-zA-Z_] [a-zA-Z_0-9]* ;
NUM : [0-9]+ ;
WS  : [ \t\r\n]+ -> skip ;           /* 关键：空白要 skip 而不是隐藏 */
```

生成：`antlr -Dlanguage=Java Expr.g4` → `ExprParser.java`、`ExprLexer.java`、`ExprListener.java`、`ExprVisitor.java`、`Expr.tokens`。

### 6.4 两类 API：Listener 与 Visitor

| | Listener（监听器） | Visitor（访问器） |
| --- | --- | --- |
| 范式 | **事件驱动**：遍历 parse tree 时逐个回调 `enterXxx` / `exitXxx` | **显式遍历**：`visitXxx(node)` 里手动 `visitChildren` |
| 能不能返回值 | 不能（要靠 `ParseTreeProperty<T>` 存上下文） | 能（`visitX` 返回 `T`） |
| 能不能剪枝 | 不能 | 能（不调 `visitChildren` 就是剪掉） |
| 适合 | 语义检查、符号收集（讲 11/12） | 建 AST、求值时变换（讲 05 的活） |
| 额外依赖 | 需要 `paint`/上下文栈 | 无 |

```java
// 教学示意：Visitor 模式建 AST（不参与构建）
class AstBuilder extends ExprBaseVisitor<AstNode> {
    @Override public AstNode visitMulExpr(ExprParser.MulExprContext ctx) {
        return new Binary(Op.MUL, visit(ctx.expr(0)), visit(ctx.expr(1)),
                          ctx.start.getLine(), ctx.start.getCharPositionInLine());
    }
}
// 教学示意：Listener 模式做语义检查（不参与构建）
class DeclCheck extends ExprBaseListener {
    Map<String, Type> scope = new HashMap<>();
    @Override public void enterAssignStat(ExprParser.AssignStatContext ctx) {
        requireDeclared(ctx.ID().getText());      /* 未声明就报错 */
    }
}
```

### 6.5 StringTemplate 与「生成代码」

ANTLR 3 与 **StringTemplate**（`antlr/stringtemplate4`，**1,034★**）深度耦合——`` `...` `` 模板语法既是代码的生成器，也是 ANTLR 3 输出 parse tree 的方式。ANTLR 4 把两者解耦了：

- **ANTLR 4 的取舍**：模板生成交给你自己写（Visitor 返回字符串即可），ANTLR 只管解析。
- **为什么这个取舍是对的**：模板这件事的高度定制化，塞进语法文件里会让 `.g4` 变得难以阅读。

```java
// 教学示意：用 Visitor 直接生成目标代码（不参与构建）
@Override public String visitNumLit(ExprParser.NumLitContext ctx) {
    return ctx.NUM().getText();                          // 常量直接输出
}
@Override public String visitAddExpr(ExprParser.AddExprContext ctx) {
    return String.format("(%s + %s)", visit(ctx.expr(0)), visit(ctx.expr(1)));
}
```

### 6.6 Unicode 与错误处理：现代 ANTLR 的两条硬门槛

课程 2019 年上线时这两条还只是配角，2026 年它们是必答题：

**（1）Unicode**：ANTLR 的 lexer 规则默认按**码点（code point）**工作而非 `char`，配合 `--encoding utf-8` 与 `InputStream`（而非 `Reader`）可正确处理 emoji、CJK 扩展区。规则里可直接写 `'你好'`、`\u4E00-\u9FA5`。

**（2）错误处理**：ANTLR 默认使用 `DefaultErrorStrategy`，策略是 **panic mode + single-token deletion/insertion**：

```java
// 教学示意：自定义错误监听（不参与构建）
parser.removeErrorListeners();
parser.addErrorListener(new BaseErrorListener() {
    @Override public void syntaxError(Recognizer<?,?> r, Object o, int line,
                                      int pos, String msg, RecognitionException e) {
        System.err.println("语法错误 @行 " + line + ":" + pos + " — " + msg);
        // 2026 年的加分项：在这里给出「你是不是想写 X」的建议
    }
});
```

### 6.7 用 ANTLR 重构脚本语言（讲 07）

把讲 05 的手写 parser 换成 ANTLR，收益与代价都很明确：

| 维度 | 手写递归下降 | ANTLR 生成 |
| --- | --- | --- |
| 写语法的时间 | 长 | 短（`.g4` 几十行） |
| 调试难度 | 低 | **高**（生成代码看不出逻辑） |
| 错误恢复 | 自己写 | 内建 |
| 多语言目标 | 要重写 | 换 `-Dlanguage=` 即可 |
| 极端性能 | 可控 | 生成代码较慢，但够用 |

**讲 07 的实际做法**：保留讲 05 的 AST 与解释器，只把「词法 + 语法」两层换成 ANTLR；AST 构造从「手写 if/else」变成「Visitor 的 `visitXxx`」。

---

## 版本演进

| 年份 | 事件 |
| --- | --- |
| 1975 | **yacc** 发布（ Johnson，Unix Programmer's Manual） |
| 1975 | **lex** 发布（Lesk & Schmidt） |
| 1989 | **PCCTS** 立项（Purdue），ANTLR 的直接前身 |
| 1992 | **ANTLR 1**（LL(k) + 语法谓词） |
| 1998 | Parr & Quong 发表 *ANTLR: A Predicated-LL(k) Parser Generator*（SIGPLAN Notices 33(4), PLDI） |
| 2006–2007 | **ANTLR 3**：自动生成 LL(k) 静态 DFA、tree parser、与 StringTemplate 深度耦合 |
| 2009 | 本书《Language Implementation Patterns》出版，ANTLR 3 世界观 |
| 2013 | **ANTLR 4.0**：**ALL(\*)** 自适应 LL(\*) + **直接左递归**支持；**StringTemplate 解耦** |
| 2014+ | 多目标运行时补齐（Python3、Go、Swift、R 的 typed bridge 等） |
| 2018 | **Tree-sitter 论文（ICSE 2018）**：增量 + 容错解析开始抢占 IDE 场景 |
| 2019 | 本专栏上线，讲 06/07 讲 ANTLR 的用法 |
| 2021 | **ANTLR 4.12.0** 新增 TypeScript 运行时（仓库运行时目录重排） |
| 2024 | **ANTLR 4.13.2** 为目前最新稳定版（BSD-3-Clause，工具本体仍是 Java） |
| 2025–2026 | **ANTLR 与 Tree-sitter 的分工定型**：ANTLR 管「语义精确 + 代码生成」，Tree-sitter 管「IDE 实时性」；LLM 大量生成 `.g4`（左递归/优先级错误高发） |

---

## 经典论文与原始文献

| 文献 | 出处 | 与本讲的关系 |
| --- | --- | --- |
| Johnson, S. C.，*Yacc: Yet Another Compiler-Compiler* | **UNIX Programmer's Manual, 1975** | `.y` 的源头 |
| Lesk, M. E. & Schmidt, E.，*LEX — A Lexical Analyzer Generator* | **UNIX Programmer's Manual, 1975** | `.l` 的源头 |
| Parr, T. & Quong, J.，*ANTLR: A Predicated-LL(k) Parser Generator* | **SIGPLAN Notices 33(4), PLDI 1998** | ANTLR 的学术身份 |
| Parr, T.，*Language Implementation Patterns* | **Pragmatic Bookshelf, 2009** | 与本课程同为「ANTLR 工程化」代表作 |
| Parr, T.，*The Definitive ANTLR Reference*（中译本《ANTLR 4 权威指南》） | **Pragmatic Bookshelf / 人民邮电** | `.g4` 的工具书 |
| DeRemer, F. & Pennello, T.，*Efficient Computation of LALR(1) Lookahead Sets* | **TOPLAS 4(1), 1982** | yacc 能稳定的理论保证 |
| Ford, B.，*Parsing Expression Grammars* | **POPL 2004** | lark 等工具的语法世界观 |
| Gamma, E. 等，*Design Patterns* | **Addison-Wesley, 1994** | **Visitor / Listener 的出处**：访问者模式是本章 6.4 的理论底座 |

---

## 近年研究与工业界开源实践（2015–2026）

| 项目 | star（2026-09-25 实测） | 与本讲的关系 |
| --- | --- | --- |
| `antlr/antlr4` | **19,015★** | 本章主角 |
| `antlr/grammars-v4` | **11,058★** | 上百种现成语法，**学 `.g4` 的最佳素材** |
| `antlr/stringtemplate4` | **1,034★** | 本章 6.5 的模板引擎（已趋维护状态） |
| `tree-sitter/tree-sitter` | **27,046★** | 增量/容错解析，ANTLR 在 IDE 场景的主要竞争者 |
| `javacc/javacc` | **1,277★** | 老牌 LL(k) 手写式生成器，与 ANTLR 直接竞争 |
| `lark-parser/lark` | **5,991★** | Python 侧的 ANTLR 替代品（PEG / LALR） |
| `dotnet/roslyn` | **20,688★** | 大型真实语言前端 + IDE 的教科书 |
| `apache/calcite` | **5,189★** | 用 JavaCC 解析 SQL 的工业范本 |
| `alibaba/druid` | **28,178★** | 讲 14 用 Druid 的 SQL 解析器做分库分表 |

**2026 年的选型建议**（这是本章最该带走的一张表）：

| 需求 | 选 |
| --- | --- |
| 要一棵精确树 + 好诊断 + 要生成代码 | **ANTLR 4** |
| 要 IDE 实时高亮/补全/折叠，输入边打边解析 | **Tree-sitter** |
| Python 里快速做个 DSL | **lark**（PEG 更直观） |
| 要完全控制生成代码的每一行为 | **手写递归下降 / Chevrotain** |
| C/C++ 生态，要 LALR 与 `%left` | **Bison**（无 GitHub 镜像，GNU savannah） |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「ANTLR 和 yacc 是一回事，只是语法不同」 | **不是**。ANTLR 是 LL(\*)/ALL(\*) 递归下降，yacc 是 LALR(1) 表驱动；冲突处理方式、错误恢复、生成物结构完全不同 |
| 2 | 「`.g4` 里的顺序无所谓」 | **顺序即优先级**！规则写得越靠前，优先级越低；这是 ANTLR 最容易踩的坑 |
| 3 | 「生成的代码可以直接改」 | 改语法、重新生成；手改会被下一次生成覆盖 |
| 4 | 「ANTLR 3 的 StringTemplate 是标配」 | ANTLR 4 **已解耦**，模板生成由你自己写；StringTemplate 4 已进入维护状态 |
| 5 | 「Listener 比 Visitor 方便所以选 Listener」 | Listener 不能返回值，做不了 AST 构造；Visitor 才是建树的标准做法 |
| 6 | 🔧 本课程未强调 **StringTemplate 已趋于停滞** | 2026 年写「生成代码」应直接用模板字符串或语言原生模板（Jinja/Mustache/StringTemplate 之外） |
| 7 | 🔧 未提 **ANTLR 4 的监听器/访问器双模式选择** | 本章 6.4 已补：语义检查用 Listener，建 AST 用 Visitor |
| 8 | 🔧 未提 **ANTLR 对 Unicode 与错误处理的现代实践** | 码点模式、`--encoding`、自定义 `ErrorListener` + 「你是不是想写 X」的建议，2026 年是硬门槛 |
| 9 | 🔧 未提 **Tree-sitter 的冲击** | 2018 年后 ANTLR 在编辑器插件场景大量被替代；ANTLR 仍需补「增量解析」这一课 |
| 10 | 🔧 未提 **LLM 生成 `.g4` 的实际经验** | 模型能写出可用的 `.g4`，但必须人工复核：直接左递归、分层顺序、二义性 |
| 11 | 🔧 未提 **ANTLR 4.13.x 仍是最新稳定版**、工具本体仍是 Java | 选型的现实约束：ANTLR 工具需要 JVM |

---

## 与其他章 / 其他书的联系

- **`02-正则文法和有限自动机.md`**：`.g4` 里的 lexer 规则就是那章的正则文法，ANTLR 替你做 NFA→DFA。
- **`03-语法分析入门.md`**：`.g4` 里的 parser 规则就是那章的 BNF/EBNF。
- **`04-二元表达式与优先级.md`**：ANTLR 用**规则书写顺序**表达优先级（隐式），yacc 用 `%left` 表达（显式）；这章讲清了二者。
- **`05-实现一门简单脚本语言.md`**：讲 07 要重构的就是这章的 parser。
- **`09-语义分析与类型系统.md`**：Listener 模式的主要战场。
- **`11-前端技术应用.md`**：Druid/ShardingSphere 的 SQL 解析器就是 `.g4` 的工业版。
- **`book/antlr4权威指南.md`**（同级单文件笔记）：`.g4` 的工具书，本章只讲骨架。
- **`book/Lex与Yacc.md`**、**`book/flex与bison中文版.md`**：`.y` / `.l` 的完整用法，本章 6.2 的展开版。
- **`book/编程语言实现模式/04-中间表示与语法树.md`**：P.8–P.11，与本章 6.4 的 Visitor 建 AST 同一件事。
- **`book/编程语言实现模式/05-树的遍历与重写.md`**：P.12–P.15，Listener/Visitor 的模式化表述。
