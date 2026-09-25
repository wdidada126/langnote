# Stage 04 — 三地址中间代码生成

- **对应讲次**：`notes/L12`（IR 家族）、`notes/L13`（翻译模式/回填/短路模板）
- **对应 CS143 PA**：PA4（COOL 的 AST→抽象汇编树；MiniC 换成三地址码）
- **核心代码**：`icode.h`（本阶段新增），驱动 `main.cpp`

## 知识点落点（代码 ↔ 讲义）

| 讲义概念 | 实现位置（icode.h） |
| --- | --- |
| 三地址形式/临时量命名 | `Inst` + `newTmp()`：`t1, t2...` 至多写一次——"SSA 式奢侈命名" |
| 槽位 vs 值（mem2reg 的前半） | 变量编译为槽 `name@k`，每次绑定取新 `@k`——遮蔽在生成期消除 |
| 控制流翻译（if/while） | `genStmt(SIf/SWhile)`：前跳 `Jz`+标签，即龙书 8.4 的"真链假链"直译 |
| 短路 `&&`/`||` 翻译模式 | `genExpr(EBinary)`：`t=a; ifz a goto Lend; t=b; Lend:`（L13 核心例题） |
| 回边/可归约 CFG | `while` 的 `Jnz → Lbody`，目标支配跳转点 |
| 调用约定微缩模型 | 实参写全局箱 `$a<i>`，被调方序言拷入参数槽（notes/L11） |
| 翻译模式=底部语义规则 | 生成器是一个显式 AST 遍历，动作嵌在产生式对应位置 |

## 构建 / 运行

```sh
./build.sh && ./minic04 ../samples/hello.minic
```
```bat
build.bat && minic04.exe ..\samples\hello.minic
```
输出为每个函数一段三地址清单（带源码行号注释）。

## 动手实验
1. 在 `hello.minic` 里加 `print (3 > 2) && isEven(4);`，观察短路模板产生的 `ifz/jnz` 形状。
2. 写 `if (true) { print 1; } else { print 2; }`，对照 L13 的 backpatch：条件常量后跳转可折叠——这正是 stage 06 的素材。
3. 思考题（L12）：把 `a = a + 1` 编译成两条指令后，为什么 IR 已"接近"SSA 而槽位 `a@k` 不是？（答：一个槽可被多次写。）
