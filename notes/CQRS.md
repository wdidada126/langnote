# CQRS



简单的说，CQRS（Command Query Responsibility Segration）就是一个系统，从架构上把 CRUD 系统拆分为两部分：命令（Command）处理和查询（Query）处理。其中命令处理包括增、删、改。


简单的说，就是一个系统，从架构上把它拆分为两部分：命令处理（写请求）+查询处理（读请求）。然后读写两边可以用不同的架构实现，以实现CQ两端（即Command Side，简称C端；Query Side，简称Q端）的分别优化。CQRS作为一个读写分离思想的架构，在数据存储方面，没有做过多的约束。


https://blog.csdn.net/gadbee5/article/details/50504660/

CQRS 实现方式

CQRS 可以有两种实现方式。

1、CQ 两端数据库共享，只是在上层代码上分离。

这样做的好处是可以让我们的代码读写分离，更容易维护，而且不存在 CQ 两端的数据一致性问题，

因为是共享一个数据库的。这种架构是非常实用的（也就是我上面画的那种）


2、CQ 两端不仅代码分离，数据库也分离，然后Q端数据由C端同步过来。

同步方式有两种：同步或异步，如果需要 CQ 两端的强一致性，则需要用同步；如果能接受 CQ 两端数据的最终一致性，则可以使用异步。

C端可以采用Event Sourcing（简称ES）模式，所有C端的最新数据全部用 Domain Event 表达即可

而要查询显示用的数据，则从Q端的 ReadDB（关系型数据库）查询即可（详细可以参考文献3）。


https://blog.csdn.net/frank_zhu_bj/article/details/53222078
