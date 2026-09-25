# Stage 01 — 词法分析器（hand-written DFA lexer）

- **对应讲次**：`notes/L03-词法分析I-正则与DFA.md`、`notes/L04-词法分析II-自动机实现与生成器.md`
- **对应 CS143 PA**：PA1（同样是手写 tokenize，课程明确不许用 flex）

## 知识点落点（代码 ↔ 讲义）

| 讲义概念 | 代码位置（../common/lexer.h） |
| --- | --- |
| 正则 → 词法类别（关键字/标识符/数字/运算符） | `Tok` 枚举 + `kindFromIdent`（先 IDENT 后查表 = 最长匹配） |
| DFA 状态转移 | `next()` 的分派 + `readIdent/readNumber/readPunct` 内部循环 |
| 前瞻与回退（lookahead/putback） | `peek(k)` 一字符前瞻处理 `<=` vs `<`；浮点直接报错代替回退 |
| 嵌套注释超出正则能力 | `skipTrivia` 的 depth 计数器（见 notes/L03 的讨论） |
| 词法错误可局部恢复 | `LexerError` 携带行号；驱动端一次性报告 |
| token 属性（值+位置） | `Token{text, value, line, col}` |

## 构建

```sh
./build.sh          # g++ -std=c++17，产物 ./minic01
```
```bat
build.bat           # MSVC cl（x64 Native Tools 命令行），产物 minic01.exe
```
**请在 01_lexer/ 目录内构建与运行**（include 采用相对路径）。

## 运行

```sh
./minic01 ../samples/hello.minic     # 或无参数（默认读该样例）
```
逐行输出 `行:列 token类型 lexeme value`。动手实验：
把 `../samples/bad.minic` 里某处 `>=` 改成 `=>`，观察词法错误的行列定位。

## 延伸阅读
- Flex 手册 "How Flex Works"：把自己手写的状态机与生成表对照。
- rustc_lexer crate：工业级"为什么手写词法器"的注脚。
