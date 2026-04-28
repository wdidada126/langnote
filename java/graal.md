# graal

[深入浅出Java 10的实验性JIT编译器Graal](https://blog.csdn.net/gv7lzb0y87u7c/article/details/79922799)

Graal 是 Oracle Labs 开发的、用 Java 编写的高性能 JIT/AOT 编译器，是 GraalVM 的核心组件，主打 Sea of Nodes（节点海）IR、SSA、激进优化、多语言支持。
全称：Graal Compiler，是 GraalVM 的核心编译器。
出身：Oracle Labs 2010 年启动，Java 9 引入为实验性 JIT（-XX:+UseJVMCICompiler），Java 17 后成熟可用。
本质：Java 写的 Java 编译器，可替换 HotSpot 的 C2，也可独立做 AOT 编译。