# Nand2Tetris 配套项目计划（projects/README.md）

> 官方 10 个 Project 为主干；本表补充「用现代语言重造轮子」的小项目。本轮只列计划不写代码。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| Ch.1–3 逻辑与电路 | nand2tetris HDL | 官方 Project 1–3；附加：用 Logisim 复现 16 位 ALU | 官方 Hardware Simulator 载入 .hdl 自动评测 |
| Ch.4–5 机器语言与 CPU | nand2tetris HDL + Hack 机器码 | 官方 Project 4–5；附加：手写字节序/立即数编码对照表 | Hardware Simulator 运行 .hack |
| Ch.6 汇编器 | Python 或 C | 官方 Project 6；附加：给汇编器加 `.org` 伪指令与错误行号报告 | Python: `python assembler.py xxx.asm`；C: `gcc -O2 -o hackasm` |
| Ch.7–8 虚拟机 | Python 或 C++ | 官方 Project 7–8；附加：VM 常量折叠优化（`push 2; push 3; add`→`push 5`） | 同上加优化开关参数 |
| Ch.9–10 编译器 | Python/C++/Java | 官方 Project 10；附加：输出带行号注释的 VM 码便于调试 | 按官方目录结构运行编译脚本 |
| Ch.11 操作系统 | Jack（官方） + C 对照 | 官方 Project 11；附加：用 C 写同接口 Sys.alloc 迷你版做对比 | Jack 用模拟器编译；C 版 `gcc -O2 -ffreestanding` |
| Ch.12 集成与延伸 | JavaScript/Python | 俄罗斯方块移植到自家 VM 全流程跑通；写一篇「我的 12 层抽象」笔记 | 官方 CPUEmulator 运行 |
