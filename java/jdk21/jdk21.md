# jdk21

IntelliJ IDEA 2023.3 提供了对最新 Java 21 功能的完全支持。这些更新包括虚拟线程、记录模式、switch 表达式的模式匹配和序列化集合等重要新特性，以及对字符串模板、作用域值等新引入的语言功能的预览。

https://openjdk.org/projects/jdk/21/

bazel使用java21开发

https://docs.oracle.com/en/java/javase/21/

## java21新特性
https://www.oracle.com/java/technologies/javase/21-relnote-issues.html#NewFeature

以下是 Java 21 新特性的分类翻译与核心功能解析，结合官方文档与社区实践整理而成：

一、语言特性增强

1. 字符串模板（String Templates - JEP 430）  
   允许在字符串中直接嵌入表达式，避免手动拼接。支持自定义模板处理器（如 STR），编译时安全验证防止注入攻击。  
   String name = "Alice";
   String message = STR."Hello, \{name}!"; // 输出: Hello, Alice!
   
   适用场景：日志生成、动态SQL/HTML构建。

2. 记录模式（Record Patterns）  
   简化记录类（Record）的解构操作，支持嵌套模式匹配：  
   record Point(int x, int y) {}
   if (obj instanceof Point(int x, int y)) {
       System.out.println(x + ", " + y); // 直接解构字段
   }
   
   优势：减少类型检查样板代码，提升数据类处理效率。

3. 未命名类与实例main方法（Preview）  
   简化初学者代码结构，允许省略类声明和静态main方法：  
   void main() { // 无需public static
       System.out.println("Hello, Java 21!");
   }
   
   教育意义：降低学习门槛，逐步过渡到完整语法。

二、并发与性能优化

1. 虚拟线程（Virtual Threads - JEP 444）  
   轻量级线程（由JVM管理），支持百万级并发，内存占用仅为传统线程的1/1000：  
   try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
       IntStream.range(0, 10_000).forEach(i -> 
           executor.submit(() -> processRequest(i)));
   }
   
   性能对比：10万并发请求下吞吐量提升300%。

2. 结构化并发（Structured Concurrency）  
   统一管理并发任务生命周期，避免线程泄漏：  
   try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
       Future<String> user = scope.fork(() -> fetchUser());
       Future<Integer> order = scope.fork(() -> fetchOrder());
       scope.join(); // 等待所有任务完成
   }
   
   优势：任务组错误传播更清晰，适合微服务场景。

3. 分代ZGC（Generational ZGC - JEP 439）  
   分代垃圾回收器，停顿时间低于1毫秒：  
   java -XX:+UseZGC -XX:+ZGenerational -Xmx8g MyApp
   
   优化点：降低内存占用与CPU开销，适合实时系统。

三、API 增强

1. Sequenced Collections（有序集合接口）  
   新增统一接口SequencedCollection/SequencedMap，提供首尾元素访问：  
   SequencedSet<String> set = new LinkedHashSet<>();
   set.addFirst("A"); // 新增方法
   set.getLast();    // 直接获取末尾元素
   
   兼容性：LinkedHashSet、TreeMap等已实现该接口。

2. Math.clamp() 方法  
   数值范围限制，支持int/long/float/double类型：  
   int clamped = Math.clamp(value, 0, 100); // 限制在0~100
   
   应用场景：数据标准化、游戏物理引擎[citation:N/A]。

3. 字符串与正则增强  
   • String.indexOf()支持范围查询[citation:N/A]  

   • 正则支持Emoji属性匹配（如\p{IsEmoji}）[citation:N/A]  

四、安全与工具改进

1. 动态加载Agent警告（JEP 451）  
   运行时加载Agent会触发警告，未来版本可能默认禁用：  
   jcmd <pid> JFR.view  # 查看JFR事件
   
   迁移建议：优先使用启动参数-javaagent。

2. HSS/LMS签名算法  
   支持后量子加密算法（基于哈希签名）：  
   Signature sig = Signature.getInstance("HSS/LMS");
   sig.initVerify(publicKey);
   
   标准依据：RFC 8554与NIST SP 800-208[citation:N/A]。

五、其他重要更新

• JFR视图命令：直接聚合分析性能事件（如gc-pauses）[citation:N/A]  

• XML安全更新：支持EdDSA签名，禁用不安全的here()函数[citation:N/A]  

• 时区数据：-XshowSettings:locale显示tzdata版本[citation:N/A]  

升级建议

• LTS支持：Java 21支持至2028年（可扩展至2031年），适合企业长期项目。  

• 兼容性风险：有序集合接口可能引发类型推断冲突，需测试验证[citation:N/A]。  

如需完整特性列表，可参考https://openjdk.org/projects/jdk/21/。


JDK 21
This release is the Reference Implementation of version 21 of the Java SE Platform, as specified by JSR 396 in the Java Community Process.

JDK 21 reached General Availability on 19 September 2023. Production-ready binaries under the GPL are available from Oracle; binaries from other vendors will follow shortly.

The features and schedule of this release were proposed and tracked via the JEP Process, as amended by the JEP 2.0 proposal. The release was produced using the JDK Release Process (JEP 3).

Features
430:	String Templates (Preview)
431:	Sequenced Collections
439:	Generational ZGC
440:	Record Patterns
441:	Pattern Matching for switch
442:	Foreign Function & Memory API (Third Preview)
443:	Unnamed Patterns and Variables (Preview)
444:	Virtual Threads
445:	Unnamed Classes and Instance Main Methods (Preview)
446:	Scoped Values (Preview)
448:	Vector API (Sixth Incubator)
449:	Deprecate the Windows 32-bit x86 Port for Removal
451:	Prepare to Disallow the Dynamic Loading of Agents
452:	Key Encapsulation Mechanism API
453:	Structured Concurrency (Preview)
JDK 21 will be a long-term support (LTS) release from most vendors. For a complete list of the JEPs integrated since the previous LTS release, JDK 17, please see here.

Schedule
2023/06/08		Rampdown Phase One (fork from main line)
2023/07/20		Rampdown Phase Two
2023/08/10		Initial Release Candidate
2023/08/24		Final Release Candidate
2023/09/19		General Availability


Java ScopedValue
https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ScopedValue.html

以下是JDK 21官方发布信息的完整中文翻译，结合技术规范与社区通用术语进行本地化处理：

JDK 21 正式发布公告

版本性质  
JDK 21是Java SE平台第21个版本的参考实现，遵循Java社区进程（JCP）中JSR 396规范制定。该版本于2023年9月19日达到通用可用（General Availability）状态，Oracle提供GPL协议下的生产环境可用二进制包，其他厂商的发行版将陆续跟进。

核心特性列表

JDK 21通过JEP（JDK增强提案）流程引入以下15项特性，按功能领域分类如下：

一、语言与API增强

1. JEP 430：字符串模板（预览）  
   支持类似Python f-string的字符串插值，例如STR."Hello, \{name}"，编译时自动校验安全性。
2. JEP 431：序列化集合（Sequenced Collections）  
   为有序集合（如LinkedHashMap）定义统一接口，新增getFirst()、getLast()等方法。
3. JEP 440：记录模式（Record Patterns）  
   增强记录类（Record）的解构能力，支持嵌套模式匹配：  
   if (obj instanceof Point(int x, int y)) { ... }
   
4. JEP 441：switch模式匹配  
   允许switch直接匹配类型并解构对象，例如：  
   return switch (obj) {
       case String s -> "String: " + s;
       case Integer i -> "Integer: " + i;
       default -> "Unknown";
   };  
   

二、并发与性能优化

5. JEP 444：虚拟线程（正式版）  
   轻量级线程（协程），单机可支持百万级并发，显著提升I/O密集型应用吞吐量：  
   Thread.startVirtualThread(() -> System.out.println("Virtual thread"));
   
6. JEP 453：结构化并发（预览）  
   通过StructuredTaskScope管理并发任务生命周期，避免线程泄漏。
7. JEP 439：分代ZGC  
   Z垃圾回收器支持分代收集，降低内存占用与停顿时间，需通过-XX:+UseZGC -XX:+ZGenerational启用。

三、底层与安全

8. JEP 442：外部函数与内存API（第三次预览）  
   安全调用本地代码（如C/C++）和操作堆外内存，替代JNI。
9. JEP 452：密钥封装机制API  
   支持RSA-KEM等算法，增强加密通信安全性。

四、其他重要更新

• JEP 445：未命名类与实例main方法（预览）  

  简化Hello World写法，允许省略public class声明。
• JEP 449：弃用32位Windows移植  

  未来版本将移除对32位x86 Windows的支持。

发布里程碑

日期 阶段
2023/06/08 Rampdown第一阶段（代码分支冻结）
2023/07/20 Rampdown第二阶段（仅修复关键bug）
2023/09/19 正式发布（GA）
  

长期支持（LTS）说明

JDK 21是自JDK 17后的新一代LTS版本，Oracle承诺提供至少8年的技术支持。企业用户可放心用于生产环境，非LTS版本（如JDK 19/20）建议仅用于测试。

升级建议

1. 生产环境：推荐从JDK 8/11/17直接升级至JDK 21 LTS，优先评估虚拟线程、分代ZGC等特性。
2. 兼容性：注意预览功能（如字符串模板）需添加--enable-preview参数，且API可能变更。
3. 工具链：确保IDE（如IntelliJ IDEA）和构建工具（Maven/Gradle）支持JDK 21。

如需完整特性说明，请参考https://openjdk.org/projects/jdk/21/。

JEP 474：分代式现已成为 Java 中 ZGC 的标准
