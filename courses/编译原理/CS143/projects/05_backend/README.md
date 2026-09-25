# Stage 05 — 后端：三地址码的执行（虚拟机）与汇编风格输出示例

- **对应讲次**：`notes/L11`（激活记录/调用约定）、`notes/L15`（指令选择/代码生成）
- **对应 CS143 PA**：PA5 的功能等价物。官方 PA5 把 COOL 编译到 **MIPS 汇编**并在
  SPIM 上运行；MiniC 这一步提供两个后端中的"解释器"路线（另一条"真汇编"路线
  需要目标 ISA 工程，超出本轮范围——见下文的文本示例与"如何升级"）。
- **核心代码**：`interp.h`（本阶段新增），驱动 `main.cpp`

## 知识点落点（代码 ↔ 讲义）

| 讲义概念 | 实现位置（interp.h） |
| --- | --- |
| 激活记录 = 栈上一帧 | `Frame{locals, pc, retDest}` + `frames_` 栈；Call 压帧、Ret 弹帧 |
| 调用约定/参数传递 | `$a<i>` 全局箱：调用方写、被调方序言读（notes/L11 的隐藏参数思想） |
| 返回值落地 | `Frame::retDest`：Ret 弹栈后写入**调用者**的临时量 |
| 分支 = 跳转表 | `labelAt()` 预建 标签→指令下标 的映射（分支目标缓冲的孪生） |
| 停机问题兜底 | `kMaxSteps`：语义错误（死循环）只能运行时发现——静态不可判定（notes/L10） |
| 除零 | `evalArith` 抛异常：动态检查的活教材 |

## 构建 / 运行

```sh
./build.sh && ./minic05 ../samples/hello.minic      # 执行
./minic05 -S ../samples/hello.minic                 # 顺便打印 IR
```
```bat
build.bat && minic05.exe ..\samples\hello.minic
```
`hello.minic` 预期输出：
```
6
false
30
=== main returned 0 ===
```

## 汇编风格输出长什么样（PA5 的精神图示，非本项目产物）

同一句 `s = s + i;`（槽位各配一个帧内偏移后），x86-64 风格文本为：

```asm
    mov  eax, [rbp-8]      ; load s
    add  eax, [rbp-16]     ; add  i
    mov  [rbp-8], eax      ; store s
```
而 `Call/Ret` 对应 `call` + 序言/尾声（`push %rbp; mov %rsp,%rbp; ...`），
比较跳转 `ifnz t goto Lbody` 对应 `cmp/setcc/test + jnz`——MIPS(COOL/PA5) 的
差别只在**没有标志寄存器**：`seq/slt` 把比较结果写进寄存器再分支。
对照 `notes/L15` 与 CSAPP ch3 可以逐条互译。

## 如何升级成真后端（练习路线）
1. 给每条 IOp 写发射模板 → 产出 `.s` 文本（先支持无函数版）。
2. 把 `t<i>` 直接放栈槽（`-O0` 风格），函数帧偏移由 IRGen 槽位计数决定。
3. 之后你会自然需要 stage 06 的优化来"修"生成质量——这正是 L15/L16/L17 的关系。

## 动手实验
1. `minic05 -S` 观察 gcd 循环的 `jmp L3 / L1 / L3 / ifnz` 结构，手画 CFG，验证"可归约"。
2. 让 `main` 除以 0：观察运行期异常与 `bad.minic` 类静态错误的边界。
3. 把 kMaxSteps 调小，观察"步数上限≈心跳"的调试用法。
