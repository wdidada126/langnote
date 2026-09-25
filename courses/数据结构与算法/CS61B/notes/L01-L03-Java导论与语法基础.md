# L01–L03 课程导论与 Java 语法基础（环境、类型、控制流）

> 对应 spring2024 L1–L3：JDK/IntelliJ 环境、编译运行模型、原始类型与表达式、整数溢出、控制流与作用域。作业：Lab1（Java 热身）、HW1。

## 1. 核心概念

- **编译运行模型**：`.java` 源文件 → `javac` 编译为 `.class` 字节码 → JVM 解释/JIT 执行。字节码使 Java "一次编写，到处运行"，代价是多一层虚拟机（与 C 直接编译到机器码对比，见 CS61C）。
- **JVM 内存粗分**：栈（局部变量、方法帧）/ 堆（`new` 出来的对象）。理解这一点是后面链表、数组"指向节点的指针"心智模型的基础。
- **8 种原始类型**：`byte/short/int/long/float/double/char/boolean`。`int` 恒为 32 位补码（不像 C 依赖平台），`char` 是 16 位 UTF-16 码元。
- **整数溢出是"回绕"而非异常**：
  ```java
  int x = Integer.MAX_VALUE; // 2147483647
  System.out.println(x + 1); // -2147483648（静默回绕）
  System.out.println(Math.addExact(x, 1)); // 抛 ArithmeticException
  ```
- **浮点精度**：`0.1 + 0.2 == 0.3` 为 `false`（二进制无法精确表示 0.1）。钱要用 `long`（分）或 `BigDecimal`。
- **作用域**：变量从声明处到所在 `{}` 结束有效；for 循环变量出循环即销毁——这一规则与后面 L15 循环成本分析直接相关。

## 2. 关键实现要点

- 表达式求值顺序、`==` 对 `String` 比较引用（**必须用 `equals`**）是初学者两大坑：
  ```java
  new String("hi") == new String("hi")      // false：两个对象
  new String("hi").equals(new String("hi")) // true
  ```
- 读代码训练（Softwear 式反编译练习）：先看循环边界与返回值，倒推功能，而不是逐行翻译。

## 3. 复杂度视角（为 L15 预热）

| 操作 | 成本 | 说明 |
| --- | --- | --- |
| 原始类型算术 | O(1) | 单条机器指令级别 |
| `new` 对象 | O(1) 摊还（含 JVM 分配） | 但触发后续 GC 成本 |
| 字符串拼接 `+=` 循环 n 次 | O(n²) | 每次拼接复制整个串；应用 `StringBuilder`（O(n)） |
| `String.equals` 最坏 | O(n) | 逐字符比较 |

## 4. 与前后讲联系

- L04–L06 的接口/封装建立在本讲的"引用类型存的是堆对象地址"心智模型上。
- L15 渐近分析将用本讲的循环计数法形式化；Project 1a 直接写二维数组游戏，依赖本讲的嵌套循环与二维索引。

## 5. 跨课程联系

- **CS61A**：61A 用 Python/Scheme 讲"求值模型"（环境帧、代换），61B 直接给你 JVM 的栈/堆——同一抽象的两种落地；61A 的"数据导向编程"思想在 Java 里由泛型与接口承担（L08–L11）。
- **CS61C/CSAPP**：Java 的 `int` 回绕就是 CS61C 补码电路的溢出行为；CSAPP 强调 `sizeof` 平台相关，而 Java 类型宽度由规范锁死，这是可移植性与内存控制的取舍。
- **6.006**：6.006 假设 RAM 模型 O(1) 字操作，本讲的溢出问题正是"字长有限"这一模型假设的体现。

## 6. 开源项目应用

- **JDK**：`Integer`/`Math` 中的 `Math.addExact`、`Integer.compareUnsigned` 都是对本讲溢出语义的工程化补丁。
- **javac**：语言规范的严格类型宽度让 error-prone、SpotBugs 等静态检查器能可靠地报"未检查的乘法可能溢出"。
- **Git 生态**：Git 的对象 ID 是 160 位 SHA-1/256，必须用 `long[]`/`BigInteger` 类库而非 `int` 表示——溢出意识在真实系统中的直接体现。

## 7. 延伸阅读

- Hug 笔记 "Java Setup" "Java Syntax" "Control Flow"（datastructur.org/notes）。
- 《Effective Java》Item 59–63（库优先、避免浮点做货币、理解溢出）。
- JLS §4.2（整型类型与补码回绕语义）。

## 8. 自测（合上笔记作答）

1. 为什么 `int` 溢出静默回绕而 `Math.addExact` 抛异常？两者各自适合什么场景？
2. `0.1 + 0.2 == 0.3` 的结果是什么？用二进制小数解释原因，并给出金额的两种正确表示。
3. `String s1 = "hi"; String s2 = new String("hi"); s1 == s2` 与 `s1.equals(s2)` 各是什么？为什么？
4. 循环里 `str += x` 做 n 次的总成本是多少？换成 `StringBuilder` 后呢？依据是什么？
5. 写出 `for (int i = 0; i < n; i++)` 中 `i` 的作用域边界，并说明为何循环结束后不能再用它。
