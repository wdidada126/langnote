# Dstributed Sysytems Concepts And Design

[分布式系统阅读笔记（一）-----分布式系统的特征](https://blog.csdn.net/Androidlushangderen/article/details/42004201)



[分布式系统阅读笔记](https://blog.csdn.net/Androidlushangderen/article/list/8)



[分布式系统阅读笔记（二十二）-----时钟和时钟同步](https://blog.csdn.net/Androidlushangderen/article/details/43564761)

[分布式系统阅读笔记（二十一）-----分布式系统设计(Google Case Study)](https://blog.csdn.net/Androidlushangderen/article/details/43271777)



[分布式系统阅读笔记（二十）-----分布式多媒体系统](https://blog.csdn.net/Androidlushangderen/article/details/43152989)



**第二章 系统模型**

**描述分布式系统的三种模型**

- Physical models : 用机器，网络，硬件等语言去描述整个系统。
- Architectural models : 用计算、计算任务、计算单元等语言去描述整个系统。（比上一中抽象）
- Fundametal models : 用抽象的方式去描述整个系统，主要包括三个方面：interaction models( 系统间的通信)，failure models （描述故障），security models

**Architectural models**

在这个模型中，考察四个方面：

- 在分布式系统中，通讯的实体（entity）是什么？
- 实体间的通信方式。（ interprocess communication - socket 调用，remote invocation - rpc ，indirect communication - 消息队列）
- 各个实体的在分布式系统的中的角色。
- 各个实体在物理层面，对应的是什么设施。

**Fundamental models**

用基本的模型主要为了解决两个问题

- 对于分布式系统中的一切假设去建模
- 对于一些假设去证明是否可能，或者不可能。

**interaction models**

主要影响系统间通信的两个方面：

1. 通信性能受限
2. 没有一个全局时间

**failures models**

主要关注系统是否故障，故障可以分类

1. Omission failures（无响应，未履行的故障）
2. 1.1 Process omission：进程挂了，在异步分布式系统中，这种故障检测只能靠timeout，但是timeout有可能只是因为系统响应慢了。
3. 1.2 Communication omission failures
4. Arbitrary failures（Byzantine failure）：随机的failures
5. Timing failures： 只在同步的分布式系统中有，指的是各种时间没有在bound中。例如消息延迟了。



