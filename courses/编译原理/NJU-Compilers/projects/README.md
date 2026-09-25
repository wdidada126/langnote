# NJU 编译原理 — 配套项目计划（本轮只列计划，不写代码）

> 统一语言 Java（与课程一致）。目标产物：一个 mini-C 子集编译器，随章节逐阶段提交；OJ 用例本地化后做回归。**本轮只写不编译**，集中编译验证稍后由用户执行。

## 章节 → 项目映射表

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2 词法 | Java | ANTLR 词法规则 + 手写 token 流格式化输出 | Gradle 单模块 `gradle run` |
| L3 语法 | Java | 四则运算语言解析 + visitor 解释器 | Gradle + JUnit |
| L7 语义 | Java | 符号表 + 类型检查器（给 L3 AST 加 checker） | Gradle |
| L9 中间代码 | Java | AST→三地址码生成器 + pretty printer | Gradle |
| L10 控制流翻译 | Java | if/while/call 全翻译 + 跳转回填正确性测试 | Gradle |
| L11 数据流 | Java | 可达定义/活跃变量框架（含单测不动点） | Gradle + JUnit |
| L12 寄存器分配 | Java | 干涉图 + 简化着色器（含 spilling 报告） | Gradle |
| L13 优化 | Java | 常量传播 + DCE pass 管线 | Gradle |
| L14 综合 | Java | mini-C→目标码完整编译器 + 回归脚本 `run.sh` | Gradle shadowJar / fat-jar |

## 里程碑验收标准

- 每阶段：对应 OJ/自造用例全绿；README 记录文法与 IR 设计决策。
- 综合项目：能编译含函数、数组、控制流的完整测试集；输出附汇编对照说明。
