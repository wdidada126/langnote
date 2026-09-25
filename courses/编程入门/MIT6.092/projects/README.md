# MIT 6.092 配套项目计划（骨架，本轮不写代码）

语言统一 Java 17（可用 `javac` 直接编译，无需构建工具），对应 OCW 7 节 + 期末小项目。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L2 基础语法 | Java 17 | 温度/单位换算器 + 随机猜数字游戏 | `javac *.java && java Main` |
| L3 方法与风格 | Java 17 | 成绩 GPA 计算器（方法分解 + checkstyle 自查） | `javac` + google-java-format 检查 |
| L4 字符串 | Java 17 | 命令行 ToDo 解析器（split/substring/不可变实验） | `javac` |
| L5 类与对象 | Java 17 | 扑克牌发牌与比大小（Card/Deck/Hand） | `javac` |
| L6 继承与调试 | Java 17 | 图形面积体系 + assertion 驱动的测试 | `javac -ea` 运行 |
| L7 异常 | Java 17 | 简易银行账户：自定义异常 + try/catch 事务回滚 | `javac` |
| 综合（期末） | Java 17 | 控制台版"学生管理系统"或 Hangman：串联全部知识点 | `javac` + 单 jar 打包 `jar cfe` |

约定：本轮只做计划不写代码；每个项目预建 `src/` 目录说明。
