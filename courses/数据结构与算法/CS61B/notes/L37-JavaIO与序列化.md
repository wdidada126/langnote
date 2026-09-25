# L37 Java I/O：字节流、字符流、缓冲与序列化

> 对应 spring2024 L37：InputStream/Reader 谱系、Buffered、try-with-resources 回收、序列化与文件处理。作业：Project2 依赖本讲。

## 1. 核心概念

- **两条平行谱系**：
  - 字节流：`InputStream/OutputStream`（`FileInputStream`、`ByteArrayInputStream`）——二进制真相。
  - 字符流：`Reader/Writer`（`FileReader`、`BufferedReader`、`PrintWriter`）——按字符集解码的视图。
- **装饰器模式（本课第二次结构性示范，第一次是 L08 接口层次）**：`BufferedInputStream` 包一个 `InputStream`、`InputStreamReader` 桥接两种谱系——能力按层叠加，无深继承。
  ```java
  try (BufferedWriter out = Files.newBufferedWriter(Path.of("log.txt"))) {
      out.write("state=" + s); out.newLine();
  } // L12 的 AutoCloseable 在此闭环
  ```
- **缓冲为何快**：每次 `read()` 裸 syscall ≈ 微秒级；8KB 缓冲把摊还成本除以 8192（L17 摊还思想的 I/O 版）。
- **序列化**：`Serializable` 标记接口 + `ObjectOutputStream` 把对象图写字节流——本课只取概念：**对象图 → 线性字节** 需要处理共享/环（流内部给每对象分配 handle），且版本 `serialVersionUID` 一变即断兼容（安全上 Java 原生反序列化是著名 RCE 面，生产用 JSON/Protobuf）。
- **NIO 一瞥**（`java.nio.Files.readString/writeString`，JDK11+）：小文件三行搞定；大文件用 `ByteBuffer`/`MappedByteBuffer`（mmap，CSAPP 视角=页表映射，零拷贝）。

## 2. 复杂度/成本视角

| 操作 | 量级 | 依据 |
| --- | --- | --- |
| 逐字节读未缓冲 | Θ(n) 次 syscall，纳秒变微秒 ×10⁵ | 缓冲缺失 |
| BufferedReader.readLine | Θ(n) 总，摊还 Θ(1)/字符 | 摊还 |
| 字符串拼接入流 | 用 StringBuilder，否则 O(n²)（L02） | |
| 序列化一个对象图 | Θ(对象数+字节数)；共享对象只写一次 | handle 表=HashMap |
| mmap 随机读页 | 缺页时一次盘读，后续 Θ(1) | 缓存复用 B 树哲学 |

## 3. 与前后讲联系

- 上承：L12 异常（I/O 全受检）、L07/L08 的接口-多态、L20 HashMap（序列化 handle 表）、L16 数组（buffer）。
- 下启：Project2（文本编辑器需读写文件与撤销栈）、**Project3 Gitlet：`.git/objects` 的 zlib 压缩对象、refs 文件、index 二进制格式全是本讲技能**；L38 总结的"数据结构的持久化"议题。

## 4. 跨课程联系

- **CS61A**：61A 文件即 `open().read()` 一行，抽象掉一切字节序/编码；61B 把"字符 ≠ 字节"（UTF-8 变长）与缓冲成本还给你。
- **6.006**：6.006 回避 I/O（RAM 模型假设读入免费）；61B 提醒"真实输入在磁盘上，Θ(1) 读字是谎言"——外部算法（external algorithms）是 6.006/15-445 的扩展话题。
- **CSAPP**：stdio 的 `FILE` buffer 与 `read/write` 系统调用关系正是本章内容；"为什么 printf 无 \n 不刷新"= 缓冲策略；本课 Java 流是同一设计的托管版。
- **DDCA/OS**：块设备页缓存（page cache）与本课 Buffered 层是同一"以空间换往返次数"原理在硬件-内核-应用三层的三次重现。
- **15-445/6.824**：WAL（write-ahead log）追加字节流 + fsync 语义；RPC 的序列化（protobuf）替代 Java Serializable——"对象图↔字节"是分布式系统的命脉工序。

## 5. 开源项目应用

- **JDK**：`Files.readAllBytes`/`transferTo`（JDK9 零拷贝）；`DataOutputStream` 的 UTF-8 变体（modified UTF-8，差异常被面试考）。
- **Git**：对象文件 = `zlib deflate(头+内容)`，`git cat-file` 即反序列化；index 文件按网络字节序（大端）写 32 位字段——与 `DataOutputStream.writeInt` 的"大端契约"完全一致。
- **Lucene**：自定义 `IndexInput/IndexOutput` 抽象（可换 mmap/内存/NRT），字段级编解码 + 前缀压缩；每段文件版本号防混读——序列化兼容管理的工业样板。
- **RocksDB**：SST block 格式（trailer+CRC+变长整数 varint，即"更省的序列化"）。
- **Kafka/Spring**：Kafka 协议全是手写 `ByteBuffer` 编解码（schema 演进用 Avro/JSON 替代原生序列化）；Spring `HttpMessageConverter` 是"序列化选型可插拔"的装饰器版。

## 6. 延伸阅读

- Hug 笔记 "Java I/O"；JDK javadoc：`BufferedReader`、`ObjectOutputStream`（"Serialization Principles" 一节必读）。
- 《CSAPP》10 章（System I/O）对照阅读；《Effective Java》Item 85–87（别用 Java 序列化、谨慎 serialVersionUID）。
- OWASP 关于 Java 反序列化漏洞的描述（为什么本课只教概念、生产禁用）。

## 7. 自测（合上笔记作答）

1. `InputStream` 与 `Reader` 的分界线是什么？"UTF-8 中一个汉字的字节数"说明了什么？
2. 为什么逐字节读文件慢 5 个数量级？缓冲把成本摊成了什么？（用 L17 语言回答。）
3. `try (var in = ...)` 相比 finally-close 的两个优势（异常路径、逆序关闭）。
4. Java 原生序列化如何处理共享/环？为什么生产系统改用 JSON/Protobuf？（契约 + 安全两条。）
5. Gitlet 中 `git show <id>:<path>` 的读取链路：refs → commit → tree → blob，每一步是 L20/L37 的哪个概念？
