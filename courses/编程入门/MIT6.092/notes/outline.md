# MIT 6.092 讲义要点（骨架，按 2010 IAP 7 节）

## L1 Java 入门与基本类型
- 源码 → 字节码 → JVM 的编译执行模型，与 C++ 直接编译对比。
- 八大基本类型（byte/short/int/long/float/double/char/boolean）与取值范围。
- 变量声明、赋值、Eclipse/JDK 环境搭建。

## L2 控制流与表达式
- 算术运算符与整型截断陷阱。
- if/while/for；随机数与简单模拟（随机游走）。
- Lab：小算法练习，强调亲手敲每一行代码。

## L3 方法与代码风格
- static 方法、参数与返回值；主方法作为程序入口。
- 命名规范、缩进、空行的可读性意义（本课特色重点）。
- 方法分解：一个方法做一件事。

## L4 字符串
- String 不可变性及其内存含义。
- 常用 API：substring、equals vs ==、拼接成本。
- 命令行参数 String[] 解析。

## L5 类与对象
- 字段/构造器/方法封装；this 的含义。
- 引用语义：对象变量存引用，赋值共享对象。
- 经典练习：Card/Deck 纸牌建模。

## L6 继承与调试
- 子类覆写、super、多态 basics。
- 把编译器/Eclipse warning 当错误清零。
- Assertion 用于写"可执行的假设"。

## L7 异常与收尾
- try/catch/finally、checked vs unchecked exception。
- 抛出与处理异常的设计时机；不滥用 catch-all。
- 指向进阶：MIT 6.005/6.031。
