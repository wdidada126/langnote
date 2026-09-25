# Stage 02 — 递归下降语法分析器 + AST

- **对应讲次**：`notes/L05`（CFG/推导/语法树）、`notes/L06`（递归下降与 LL(1)）、`notes/L08`（为何官方 PA2 用 bison）
- **核心代码**：`../common/parser.h`（新增），驱动与 AST 打印在本目录 `main.cpp`

## 知识点落点（代码 ↔ 讲义）

| 讲义概念 | 实现位置 |
| --- | --- |
| 非终结符 ↔ 过程的同构 | `parseFunc/parseBlock/parseDeclOrStmt/parseExpr` 一一对应文法（文件头有完整文法） |
| 左递归消解：`E -> E+T` 化归为循环 | `parseExpr` 的 `for(;;)` + 优先级爬升（Pratt, L6） |
| LL(1) 与前瞻集合 | `IDENT '=' ...` 用 2-token lookahead（`check(Tok::Assign, 1)`）——超出 LL(1) 的"手工前瞻"，正是 rustc/Kotlin 路线 |
| panic-mode 错误恢复 | `expect()` 抛同步标记 + `skipToSync()` 丢到 `;`/语句起点/`}` |
| AST = 产生式的构造函数 | `common/ast.h`：每类节点一个 struct，`kind` 枚举 = 消归的 switch |
| 语法制导（L9）最小预览 | 归约动作即 `make_unique<BinaryExpr>(...)`——"树是分析的副产品" |

## 构建 / 运行

```sh
./build.sh && ./minic02 ../samples/hello.minic
```
```bat
build.bat && minic02.exe ..\samples\bad.minic   # 看错误恢复："每错只报一次+继续"
```
输出：先报全部解析错误（若有），再打印行缩进式 AST。

## 动手实验
1. 故意删掉 `hello.minic` 中某条语句的 `;`：观察同步集如何把恢复限制在一条语句。
2. 给 `if` 加括号去掉：`if x { ... }`（COOL 风格），体会文法改动只需要动 `parseIf`。
3. 与 LALR 对照：把文法喂给 `bison -v`（需写 .y 骨架）看冲突报告——L7 实验。

## 注意
官方 PA2 使用 flex+bison（LALR），与本项目的手写路线互为镜像；两版的取舍见
`notes/L08`"生成器 vs 手写"。
