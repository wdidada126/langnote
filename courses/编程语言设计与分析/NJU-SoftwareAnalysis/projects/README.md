# NJU 软件分析 — 配套项目计划（本轮只列计划，不写代码）

> 语言统一 Java + Tai-e 框架（与课程作业一致）。8 个作业级小项目按分析技术分层；另设 1 个综合漏洞挖掘玩具。**本轮只写不编译**，集中编译验证稍后由用户执行。

## 章节 → 项目映射表

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2 程序表示 | Java | Tai-e API 热身：加载 jar、dump CFG/IR 为文本 | Gradle（Tai-e 依赖） |
| L3-L4 数据流 | Java | 通用工作表框架 + 可达定义/活跃变量/常量传播（HW1-HW2 复刻） | Gradle + JUnit |
| L5 调用图 | Java | CHA/RTA/0-CFA 三实现 + 边数对比报告（HW3） | Gradle |
| L6 指针分析 I | Java | Andersen 约束图 + 闭包求解（HW4/HW5） | Gradle |
| L7 指针分析 II | Java | 1-CFA/对象敏感扩展与开销曲线（HW6） | Gradle |
| L9 污点分析 | Java | source/sink 配置驱动的污点传播 + demo 漏洞检出（HW7/HW8） | Gradle |
| L10 IFDS | Java | 迷你 IFDS 求解器（超级图路径可达）玩具实现 | Gradle |
| 综合 | Java | 用自研管线扫一个真实开源库并对照 CodeQL 结果 | Gradle + 报告 md |

## 里程碑验收标准

- 每项目：`benchmarks/` 用例全过（可借 Tai-e 自带测试）；记录精度/耗时两组数据。
- 综合项目：与 Tai-e/CodeQL 基线的误报漏报对比表。
- 与 `notes/outline.md` 交叉引用每个算法的伪代码出处。
