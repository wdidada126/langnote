# libpcap
BPF（Berkeley Packet Filter）过滤器表达式编译器
BPF（Berkeley Packet Filter，伯克利数据包过滤器）是类Unix系统数据链路层原始接口，由Steve McCanne和Van Jacobson于1992年提出，支持网卡驱动设置为洪泛模式以接收网络所有数据包（包括非本机目标地址），主要用于网络数据包过滤。
https://zhuanlan.zhihu.com/p/578357489

https://github.com/the-tcpdump-group/libpcap

c

https://www.tcpdump.org/

libpcap 项目使用了Bison。
Version: 1.10.5
Release Date: August 30, 2024

grammar.y.in编译后生成
grammar.y

这个.y文件，作用？

这个文件是一个Bison/Yacc语法规范文件，用于定义网络数据包过滤器的语法规则。它是libpcap/tcpdump项目中BPF（Berkeley Packet Filter）过滤器表达式编译器的核心组成部分。
主要作用
1. 网络数据包过滤语法解析
• 将人类可读的过滤表达式（如 tcp port 80 and host 192.168.1.1）转换为BPF字节码
• 支持复杂的过滤条件组合（AND、OR、NOT等逻辑运算）
2. 支持的协议和字段
从文件内容可以看出，它支持解析多种网络协议的过滤条件：
• 基础协议：TCP、UDP、ICMP、IP、ARP等
• 高级协议：SCTP、IGMP、VRRP、IPV6等
• 无线网络：IEEE 802.11帧类型、子类型、方向等
• 特殊协议：MPLS、VLAN、PPPoE、Geneve等
• PF防火墙：动作、原因等过滤条件
3. 语法特性
• 丰富的操作符：端口范围、比较操作、位运算等
• 地址类型限定：主机地址、网络地址、端口等
• 方向限定：源地址、目的地址、双向等

文件结构
词法定义部分（%token）
定义了所有的关键字和标识符，如：
%token DST SRC HOST PORT TCP UDP


语法规则部分（%% ... %%）
定义了表达式的语法结构，如：
expr: term
    | expr AND term
    | expr OR term


语义动作部分（{...}）

每个语法规则对应的C代码，用于生成BPF过滤指令。

技术特点
1. 可重入解析器（reentrant parser）
2. 错误处理：详细的语法错误报告
3. 平台兼容：处理不同Yacc实现的差异
4. 内存管理：支持动态内存分配和释放

这个文件是网络抓包工具（如tcpdump）能够理解复杂过滤表达式的关键组件，它将高级过滤语言转换为底层BPF虚拟机可以执行的低级指令。

libpcap确实使用了Flex，但使用方式比较特殊。让我详细解释一下：

实际情况

1. 有Flex词法分析器

libpcap确实有一个基于Flex的词法分析器，位于：
• scanner.l - Flex词法规则文件

2. 但语法分析器是手写的

你看到的这个.y文件不是Bison的输入文件，而是一个手写的LALR(1)语法分析器！

3. 文件扩展名误导

虽然文件扩展名是.y（通常用于Bison/Yacc），但实际内容是手写的C代码，只是按照Yacc的格式组织。

证据分析

从文件内容可以看出：

手写痕迹

%{
/* 大量的手写C代码 */
#include "gencode.h"
#include "grammar.h"
// ... 几百行手写代码
%}


非标准语法

%type	<blk>	expr id nid pid term rterm qid
%type	<blk>	head
%type	<i>	pqual dqual aqual ndaqual
// ... 这些看起来像Yacc指令，但实际上是手写的解析逻辑


直接嵌入C函数

static int
str2tok(const char *str, const struct tok *toks)
{
    // 手写的辅助函数
}


为什么这样设计？

1. 历史原因

• libpcap历史悠久，早期可能没有合适的解析器生成器

• 或者为了减少构建依赖

2. 性能考虑

• 手写解析器可以更精细地优化

• 网络过滤需要高性能处理

3. 控制粒度

• 手写可以完全控制错误处理和内存管理

• 特别是对于网络协议解析这种复杂场景

实际构建过程

真正的流程是：

1. Flex处理 scanner.l → scanner.c（词法分析）
2. 手写语法分析器 grammar.y → 直接编译（语法分析）
3. 两者链接 形成完整的过滤器编译器

总结

libpcap采用了混合方案：
• ✅ 使用Flex进行词法分析

• ❌ 但语法分析器是手写的，不是Bison生成的

• 手写解析器提供了更好的控制和性能

这种设计在系统编程中很常见，特别是在对性能和控制要求很高的网络、编译器等领域。手写解析器虽然开发复杂，但可以提供最佳的运行时性能。