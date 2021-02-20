# Mono

软件简介
Mono 是一个由Novell 公司主持的项目。该项目的目标是创建一系列符合ECMA 标准（Ecma-334 和Ecma-335）的.NET 工具，包括C# 编译器和共通语言执行平台。与微软的.NET Framework 不同，Mono 项目不仅可以运行于Windows 系统上，还可以运行于Linux，FreeBSD，Unix，Mac OS X 和Solaris。

Mono 的开发工具 MonoDevelop

微软开发了一个称为共享源码公共语言基础（Shared Source Common Language Infrastructure，Shared Source CLI）的可用于 FreeBSD，Windows 和 Mac OS X 的 .NET 实现版本。微软的共享源码协议并不是开源软件协议，且可能对于社区来说也是不足够的（它明文禁止了对软件的商业用途）。我们还可以见到另外一个 .NET 实现版本，Portable.NET 项目，该项目与 Mono 项目有着很多相同的目标。

Mono 虚拟机包含一个实时编译引擎，该引擎可用于如下处理器：x86，SPARC，PowerPC，ARM，S390（32位模式和64位模式），x86-64，IA64 和64位模式的 SPARC。该虚拟机可以将代码实时编译或者预先编译到原生代码。对于那些没有列出来的系统，则使用的是代码解释器。

下图是MONO的体系结构图