# svrkit

[微信架构](https://www.cnblogs.com/SuperXJ/archive/2012/05/29/2523411.html)

[微信与朋友圈后台架构](https://blog.csdn.net/u013467442/article/details/51019691)

开源版本

phxrpc
更新日期截止2019年
https://github.com/Tencent/phxrpc

https://cloud.tencent.com/developer/article/1005762

raft代码简单而且开源，为啥不用，却要自研paxos？

虽然raft开源，facebook也在使用，但paxos真正理解后实现起来其实更为简单优雅，而且具有大神经典论文的数学证明，更有google和microsoft多年大规模使用作为证明。另外，自己研发的paxos，更能根据存储的特点进行各方面的定制化。微信海量用户的特点，促使在存储方面有大数据高性能的需求。经过微信后台团队的潜心钻研，基于PhxPaxos定制的强一致、高可用、高性能的PhxSQL便横空出世。

https://www.sohu.com/a/212137383_463994
