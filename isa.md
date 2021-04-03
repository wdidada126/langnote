# isa

cpu是微架构处理器一种



指令集相当于函数头，微架构相当于函数体

isa

指令集只是一个规范，微架构相当于具体的实现

arm x86是指令集

微架构是cpu生产商具体实现



libuv不支持多线程，并会强制检测server的loop和connection的loop是否为同一个loop，所以做不到开多个线程及loop监听数据。

Node的库 C两个库





貌似不多，因为直接跨过中间件搞数据库本身去了。



数据集成系统

商业的有tibco data virtualization. Redhat 的 dv

开源的有teiid ，但是坑很多，社区不活跃

http://teiid.io/legacy/

穷则战术穿插，各种优化，富就加机器，加机器，加专用数据库机器

硬件有哪些？

tidb 16c32g

Nvm  2T的ssd





无论苹果 还是高通 还是华为，均为ARM构架。均是ARM授权。

高通：CPU-ARM授权构架，GPU-购买AMD的移动GPU部门。有自己的基带，有3G 4G 5G核心技术。 但是只卖硬件不卖终端，无自己的代工厂，需与其他厂商合作。

三星：CPU-ARM授权构架 ，GPU-ARM授权构架，基带有一部分，有一部分3G 4G 5G技术。卖硬件也卖终端，有自己的代工厂。

华为：CPU-ARM授权构架 ，GPU-ARM授权构架，有自己的基带，有3G 4G 5G核心技术。只卖终端不卖硬件，无代工厂。

苹果：CPU-ARM授权构架，GPU自研，基带无，无3G 4G 5G核心技术，只卖终端不卖硬件，无代工厂。



比如展锐

黄埔军校







企业 风控 100+T的数据 大量数据，是为了提高缓存命中率

携程

x-pi

知乎编程语言增加至 Python，Golang，Lua，C/C++，JVM 系（Java，Scala，Kotlin）等

如何解决Twemproxy 单 CPU 计算能力的限制

之后我们修改了Twemproxy 源码， 加入 SO_REUSEPORT 支持。

同一个容器内由Starter 启动多个 Twemproxy 实例并绑定到同一个端口，由操作系统进行负载均衡，对外仍然暴露一个端口，但是内部已经由系统均摊到了多个 Twemproxy 上。

同时Starter会定时去每个 Twemproxy 的 stats 端口获取 Twemproxy 运行状态进行聚合，此外 Starter 还承载了信号转发的职责。

原有的Agent 不需要用来启动 Twemproxy 实例，所以 Monitor 调用 Starter 获取聚合后的 stats 信息进行差值计算，最终对外界暴露出实时的运行状态信息。

Linux kernel 3.9带来了SO_REUSEPORT特性，可以解决以上大部分问题。

[Linux 最新SO_REUSEPORT特性](https://www.cnblogs.com/Anker/p/7076537.html)







X86集群对战ibm小型机

个人笔记本兴起，带动英特尔处理器销售量，有钱，研发至强处理器

arm 走量

navide收购 arm应用于服务器 挑战x86





redis用了哪些算法来实现他的数据结构

https://www.zhihu.com/answer/624278192

排序原理

有序list

facebook 改进leveldb的哪些方面











好多人分不清指令集(ISA)和微架构(microarchitecture)。其实x86就是典型的不怎么好的指令集。

指令集是架构的一部分



指令集包括汇编语言形式和二进制机器码格式，CPU执行的是二进制代码（这叫机器指令，机器能理解的），汇编就是给人看的，人能理解的。每条汇编指令都有对应的机器码指令。完成汇编语言和二进制机器码的转换时汇编器（现在都和编译器打包在一起了）。

微结构：每个cpu都有他的微结构，他描述cpu的一切逻辑。前端怎么实现取指令啊，解码怎么让其他部件的得知将要执行的指令，怎样分发指令，执行，写回，操作数旁路转移，预取指令，分支预测，分支出错流水线中指令如何回退，如何恢复，寄存器怎样实现存储等等还有很多很多，写都写不完。



https://zhuanlan.zhihu.com/p/67018861







现代cpu设计

硬件设计语言

C++去调用指令



c++编译器 机器码 intel 指令集







矢量（vector）是一种既有大小又有方向的量，又称为向量。一般来说，在物理学中称作矢量，例如速度、加速度、力等等就是这样的量。舍弃实际含义，就抽象为数学中的概念──向量。









苹果和三星现在的微架构都是自研的，高通以前自研现在不是。







内核，也就是微架构，比如说ARMv8是指令集，而Cortex A76就是一款基于ARMv8指令集的CPU微架构。