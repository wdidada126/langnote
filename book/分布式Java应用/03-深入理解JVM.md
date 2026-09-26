# 第 3 章　深入理解JVM

> 原书第 3 章是**工程价值最高、且 2026 年仍不过时**的一章：它把 JVM 的「代码怎么跑、
> 内存怎么分、线程怎么同步」讲透了。今天的 GC（G1/ZGC/Shenandoah）、JFR、容器感知 JVM
> 都是在这块地基上长出来的。但本书基于 **HotSpot + JDK 6** 视角：
> 没有 G1（JDK 7 引入、JDK 9 默认）、没有 ZGC/Shenandoah、没有虚拟线程（JDK 21）、
> 没有容器内存/CPU 感知（JDK 8u191+ 才补）。读这章要**保留它的心智模型，更新它的具体开关与算法**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 Java代码的执行机制 | 源码编译（javac → class）、类加载（装载/链接/初始化）、类执行（解释器 + JIT） | **class 文件是平台无关的中间表示**；JIT 是「热点才编译」的性能关键 |
| 3.1.1 源码编译机制 | 词法/语法分析 → 注解处理 → 语义分析 → 生成 class | class 含结构信息、元数据、方法信息 |
| 3.1.2 类加载机制 | 装载 → 链接（校验/准备/解析）→ 初始化（静态代码/构造器/静态属性） | 双亲委派是默认模型；可被破坏（SPI/OSGi） |
| 3.1.3 类执行机制 | 解释执行 + JIT（C1/C2）编译热点 | 热点方法被编译为本地码，性能接近 C |
| 3.2 JVM内存管理 | 内存空间（方法区/堆/栈/PC/本地方法栈）、分配、回收、分析工具 | **堆是 GC 主战场**；分代 + 可达性分析是回收基石 |
| 3.2.1 内存空间 | 方法区、堆、JVM 栈、PC 寄存器、本地方法栈 | 堆与栈分离，对象是堆里的引用 |
| 3.2.2 内存分配 | 对象优先 Eden、大对象直入老年代、TLAB | 分配策略决定 GC 频率 |
| 3.2.3 内存回收 | 引用计数（不用）/ 可达性分析；Serial/Parallel/CMS 等收集器 | 分代收集 + 可达性分析是 HotSpot 主线 |
| 3.2.4 查看方法和分析工具 | jps/jstat/jmap/jstack/VisualVM/MAT 等 | 排查靠「命令 + 快照 + 可视化」三步 |
| 3.3 JVM线程资源同步及交互机制 | 同步（synchronized/锁）、交互（wait/notify/volatile）、线程状态 | **Happens-Before 决定可见性**；锁升级是性能关键 |
| 3.3.1 线程资源同步机制 | synchronized、对象头 Mark Word、锁升级（偏向/轻量/重量） | 锁不是非黑即白，是分级的 |
| 3.3.2 线程交互机制 | wait/notify、volatile、JMM | 交互靠「可见性 + 唤醒」 |
| 3.3.3 线程状态及分析 | 运行/就绪/等待/阻塞；jstack 看栈 | 死锁/长时间等待靠线程栈定位 |

## 核心精讲

（以下为教学性梳理；所有片段均**教学示意，不参与构建**，绝不编译/运行。）

### 3.1 代码执行：从 `.java` 到机器码

```text
# 教学示意，不参与构建：Java 代码执行链路
.java --javac--> .class (字节码, 平台无关)
                  |
                  v
           类加载器 (装载->链接->初始化)
                  |
                  v
   方法区: 类结构/常量/静态变量   堆: 对象实例
                  |
                  v
   执行引擎: 解释器 (逐条) <----> JIT (C1/C2 编译热点为本地码)
                  |
                  v
              OS 本地指令
```

- **JIT 的精髓**：只有被频繁调用的方法/循环（热点）才编译成机器码，
  冷代码走解释器——兼顾启动速度与峰值性能。这是 Java「越跑越快」的原因。

### 3.2 内存与 GC：可达性分析 + 分代

```text
# 教学示意，不参与构建：HotSpot 分代堆（JDK 6 视角）
           年轻代(Young)                  老年代(Old)           方法区/元空间
   Eden  | Survivor0 | Survivor1 | <------ 长期存活对象 ------> | 类元数据/常量
   新对象 -> Eden -> Minor GC 存活 -> S0/S1 来回 -> 年龄到 -> Old
   老年代满 -> Major/Full GC (Stop-The-World, 更慢)
```

- **可达性分析**：从 GC Roots（栈帧本地变量、静态字段、JNI 引用等）出发，
  不可达的对象才回收；比引用计数能处理循环引用。
- **本书时代的收集器**：Serial / Parallel / CMS（JDK 6 晚期引入）。
  **G1（JDK 7u4 实验、JDK 9 默认）、ZGC/Shenandoah（JDK 11/12+）本书未及**，见「版本演进」。

### 3.3 线程同步与交互

- **synchronized 的锁升级**（教学示意，不参与构建）：

```text
无锁 -> 偏向锁(同一线程重入, 无竞争) -> 轻量锁(CAS 自旋) -> 重量锁(操作系统互斥, 阻塞)
竞争的激烈程度决定停在哪一级；重量锁代价最高
```

- **Happens-Before**（JMM 的核心规则，本书 3.3.2 的底层逻辑）：
  若操作 A happens-before B，则 A 的修改对 B 可见。典型规则：
  程序顺序、volatile 写-读、解锁-加锁、线程 start/.join。

> 读这一章时请对照 [04-分布式应用与SunJDK类库.md](04-分布式应用与SunJDK类库.md)：
> 3.3 的锁/JMM 正是 4.2 并发包（J.U.C）的底层保证；4.2 的 `ReentrantLock` 是 `synchronized` 的可中断/公平版替代。

## 版本演进

- **本书无第二版**；本节写 2010 年（HotSpot/JDK 6）口径 → 2026 年视角的变化。
- **GC 全面换代**：本书的 Serial/Parallel/CMS 已被 **G1（JDK 9+ 默认）、ZGC（JDK 15+ 生产）、
  Shenandoah** 取代；ZGC/Shenandoah 做到**亚毫秒级 STW、堆大小与停顿解耦**，CMS 已废弃（JDK 14 移除）。
- **元空间取代永久代**：JDK 8 把方法区（PermGen）改为**元空间（Metaspace，本地内存）**，
  告别 `PermGen OutOfMemory` 的调参噩梦（3.2.1/3.2.3 需更新）。
- **容器感知 JVM**：本书默认 JVM 读物理机内存；JDK 8u191+ 起 `-XX:+UseContainerSupport`
  （默认开）让 JVM 按容器 cgroup 限额设堆，避免「宿主机 64G、容器 4G、JVM 按 64G 设堆」的 OOM。
- **JFR（Java Flight Recorder）**：本书 3.2.4 的工具清单里没有；今天 JFR + JMC 是
  **低开销持续采样**首选，配合 async-profiler 出火焰图，远胜当年靠 jmap/jstack 反复捞快照。
- **虚拟线程（Project Loom, JDK 21）**：本书 3.3 的「一个请求一个线程」模型被颠覆——
  虚拟线程由 JVM 调度在少量载体线程上，百万级并发不再是线程池调参问题。这改写 3.3 全部心智模型。
- **类加载与模块化**：OSGi（本书作者出身 OSGi 背景）被 **JPMS（JDK 9 模块系统）** 取代主流地位；
  双亲委派在 JPMS 下变为分层加载。
- **GraalVM / 原生镜像（Native Image）**：AOT 编译出无 JVM 的二进制，启动毫秒级、内存极低，
  是 Serverless/云原生场景对 3.1「解释+JIT」路径的根本替代。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Lindholm, Yellin《The Java Virtual Machine Specification》 | Addison-Wesley / Oracle | JVM 字节码与内存模型的规范源头（本书 3.x 的权威依据） |
| Gosling et al.《The Java Language Specification》(JLS) | Oracle | 内存模型（JMM）、Happens-Before 的形式化定义（本书 3.3 的底座） |
| Oracle《HotSpot Virtual Machine Garbage Collection Tuning Guide》 | Oracle 文档 | 各代收集器（Serial/Parallel/CMS/G1）的官方调优手册 |
| Detlefs et al.《The Garbage Collection Handbook》 | Chapman & Hall 2012 | GC 算法全景（本书 3.2.3 的现代补全） |
| Platek《Shenandoah》/ Per Lidén 等 | OpenJDK JEP 189 | 低停顿并发 GC（本书未及） |
| Oracle《ZGC》 | OpenJDK JEP 333 | 亚毫秒 STW GC（本书未及） |
| Looms / JEP 444 Virtual Threads | OpenJDK | 虚拟线程（本书 3.3 模型的根本改写） |
| JSR-376 Java Platform Module System | JCP | JPMS，取代 OSGi 主流地位 |

> 注：以上规范/JEP 均为真实存在，未杜撰。具体 JDK 版本号以 Oracle/OpenJDK 官方发布记录为准。

## 近年研究与工业界开源实践（2015–2026）

- **GC 工程化**：G1/ZGC/Shenandoah 已是各 JDK 发行版（OpenJDK、Oracle、Eclipse Temurin、
  Azul Zing/Zulu、阿里巴巴 Dragonwell、腾讯 Tencent Kona）标配；本书的 CMS 调优经验基本作废。
- **诊断工具开源**：`async-profiler`（Java 火焰图事实标准）、Arthas（`alibaba/arthas`，
  线上不停机诊断，2026 视角补入）、`spring-boot` **81507★** 的 Actuator 暴露 JVM 指标。
- **虚拟线程生态**：JDK 21 起 `java.lang.Thread` 支持虚拟线程；Spring Boot 3.2+、
  Tomcat 10.1+、Reactor 全面适配，`quarkusio/quarkus` **15906★** 把虚拟线程作为云原生默认并发模型。
- **原生镜像**：GraalVM Native Image 让 Java 跑进 Serverless/CLI；`quarkusio/quarkus`、
  Spring Native 是其落地代表。
- **分布式 JVM 监控**：本书 3.2.4 的「单机工具」在 2026 年被 Prometheus + Grafana 聚合，
  配合 OpenTelemetry 做跨实例 JVM 指标与链路追踪（本书未及）。

> 说明：star 数均为 2026-09 `gh api` 实测，未杜撰；quarkus 15906★ 已核实。eclipse-jetty/jetty.project 返回 404（star 数未能核实，未杜撰）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「GC 调优就是调 -Xmx」 | 收集器选择、分代比例、停顿目标同样关键；且 G1/ZGC 已大幅降低手动调参需求 |
| 2 | 「永久代(PermGen)调大就行」 | JDK 8 起 PermGen 已改元空间（本地内存），本书 3.2.1/3.2.3 的 PermGen 论述需更新 |
| 3 | 「synchronized 一定慢」 | 锁升级（偏向/轻量/重量）后，低竞争下 synchronized 与 J.U.C 差距很小 |
| 4 | 「jstack 看一眼就能定位死锁」 | 死锁需对比多份快照 + 锁持有链；活锁/饥饿更隐蔽 |
| 5 | 「JVM 读物理机内存即可」 | 容器里必须开启容器感知（JDK 8u191+ 默认开），否则按宿主机设堆会 OOM |
| 6 | 🔧 3.2.3 没有 G1/ZGC/Shenandoah | CMS 已废弃；2026 默认 G1、可选 ZGC/Shenandoah（亚毫秒 STW） |
| 7 | 🔧 3.2 没有「容器感知 / 元空间」 | JDK 8u191+ 容器感知、JDK 8 元空间，本书均早于这些变更 |
| 8 | 🔧 3.3 没有虚拟线程 | JDK 21 虚拟线程颠覆「一请求一线程」；本书线程模型需重写 |
| 9 | 🔧 3.2.4 工具清单过时 | 2026 必补 JFR/JMC、async-profiler、Arthas、Prometheus；单靠 jmap/jstack 不够 |
| 10 | 🔧 3.1 没有 AOT / GraalVM 原生镜像 | Serverless/CLI 场景下 Native Image 是「解释+JIT」的替代路径，本书未及 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 3.1 类加载/执行 → [05-性能调优.md](05-性能调优.md)（5.2.1 JVM 调优的对象正是这里的内存/GC）；
  - 3.2 内存 → [05-性能调优.md](05-性能调优.md)（5.1 内存消耗分析、5.2.1 JVM 调优）；
  - 3.3 线程同步 → [04-分布式应用与SunJDK类库.md](04-分布式应用与SunJDK类库.md)（4.2 J.U.C 的底层保证）
    与 [01-分布式Java应用.md](01-分布式Java应用.md)（1.1.1 NIO 的线程模型依赖此处）。
- [../深入理解Java虚拟机3.md](../深入理解Java虚拟机3.md) —— 本书第 3、5 章的权威 2026 更新版，必配。
- [../实战Java高并发程序设计.md](../实战Java高并发程序设计.md) —— 本书 3.3/4.2 的深入与 2026 补全（含虚拟线程、Reactive）。
- [../设计数据密集型应用.md](../设计数据密集型应用.md)（DDIA 第 12 章「JVM 与 GC」相关内容）—— 跨书对照。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md) —— 不直接相关，但 JVM 线程模型是理解并发共识实现的基础。
