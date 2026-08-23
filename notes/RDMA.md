# RDMA
RDMA(Remote Direct Memory Access)技术全称远程直接数据存取。

https://my.oschina.net/SysuHuyh5LoveHqq/blog/842767

RDMA的好处与优势：
   1、零拷贝(zero-copy)
  “CPU 卸载（Offloading）” 
  “内核旁路（Kernel Bypass）”

在标准的 Oracle JDK 或 OpenJDK 中，官方并没有直接支持 RDMA 的 API。不过，通过一些特定厂商的 JDK 或第三方库，是可以在 Java 中使用 RDMA 的。

核心挑战在于，RDMA 是底层硬件直接访问内存的技术，Java 为了实现跨平台和内存安全，官方 API 默认不支持这种操作。

目前主要有下面这几种方式：

### 主要实现路径

1.  特定厂商的 JDK 扩展（如 IBM SDK）
    *   这是最接近“开箱即用”的方案。IBM 的 Java SDK 8 曾提供过名为 JSOR (Java Sockets over RDMA) 的扩展，它允许现有的 Java Socket 和 NIO 代码，通过添加特定的 JVM 启动参数（如 `-Dcom.ibm.net.rdma.conf`）和配置文件，“透明地”将网络通信从 TCP 切换到 RDMA，无需大幅修改业务代码。
    *   同时，IBM SDK 也提供了更底层的 jVerbs 库，供开发者更精细地控制 RDMA 的 Verbs 和 Endpoint API，以实现极致性能。
    *   需要注意的是：根据 IBM 的官方文档，这个 RDMA 实现在后续的版本中已经被移除了。这意味着这条路目前只针对特定版本的 IBM JDK，不是主流选择。

2.  第三方开源库
    *   这是目前更主流的做法。社区有多个开源项目致力于为 Java 提供 RDMA 支持：
        *   DiSNI (Direct Storage and Networking Interface)：一个由 IBM Research 发起的项目，提供了 Java 绑定，可以直接与 RDMA 网卡交互。像知名的 Java CIFS 客户端库 jcifs 就集成了 DiSNI 来提供 RDMA 支持。
        *   hadroNIO：一个旨在为 Java NIO 应用提供透明加速的库，它基于 UCX (Unified Communication X) 框架实现，支持 RDMA。
        *   此外，GitHub 上还能找到其他 RDMA 相关的 Java 项目，例如 DaRPC、jRCM 等，它们通常用于构建高性能的 RPC 框架或特定领域的系统。

3.  已经搁置的官方提案 (JEP 337)
    *   在 2018 年，OpenJDK 社区曾提出过一个 JEP 337: RDMA Network Sockets 的提案，计划在 JDK 的 `jdk.net` 包中添加对 RDMA 的原生支持。
    *   遗憾的是，这个提案最终状态为 'Closed / Withdrawn'（已关闭/撤回），并未被采纳到标准 JDK 中。因此，短期内我们无法期待官方 JDK 直接支持 RDMA。

### 关键的运行环境与限制

无论采用哪种方案，在 Java 中使用 RDMA 都面临着几乎一致的限制：

*   平台限制：RDMA 支持主要仅限于 Linux 平台。上述提到的 IBM JDK 扩展和大部分开源库都明确标注为“Linux only”。
*   硬件与驱动依赖：你的服务器必须配备支持 RDMA 的网卡（如 InfiniBand, RoCE, iWARP），并且安装好相应的驱动和用户态库（如 OpenFabrics Enterprise Distribution, OFED）。
*   内存锁定权限：RDMA 操作要求将通信缓冲区内存锁定（pinning）在物理内存中，防止被操作系统交换出去。因此，运行 Java 应用的用户必须拥有锁定内存的权限。

### 总结与建议

*   对于新项目：不建议寄希望于标准 JDK 提供官方支持。更可行的路径是评估并使用成熟的第三方库，如 DiSNI 或基于 UCX 的方案（如 hadroNIO）。
*   对于现有应用：如果应用运行在 IBM JDK 8 的特定环境中，可以研究其 JSOR 特性，看能否以最小改动实现 RDMA 加速。
*   核心要点：使用 RDMA 意味着你的应用将被深度绑定在 Linux 环境和特定的硬件上，这会显著增加开发和运维的复杂度。你需要权衡性能提升与这种平台绑定所带来的成本。
