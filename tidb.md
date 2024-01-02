# tidb
屹tong
5.7.25-TiDB-v4.0.16

tidb解决的是容量问题

PingCAP 团队的论文《TiDB: A Raft-based HTAP Database 》入选 VLDB 2020 ，成为业界第一篇 Real-time HTAP 分布式数据库工业实现的论文。
https://blog.csdn.net/tidb_pingcap/article/details/108401113

infra底层类开源是大势所趋，除了star数，团队的布局也很厉害，无论是湾区设office，发VLDB提高reputation，用Rust写存储层做网红，D轮融资不断推进，同时做TP/AP甚至融合成一个HTAP（虽然说Hybrid现在更多是一个学术上的噱头，但是解决方案确实很新，学术上我认为是超过了Google那篇的），开源周边工具（其实这些轮子大公司都在造，但是PingCAP有开源的优势，比较新的比如TiCDC和Chaos Mesh），注重社区技术布道提升话语权和影响力，都让这个公司变得像一个综合性数据库公司。对比其他做infra开源的，你会发现PingCAP真的做得很好。甚至你以后说TiDB开始做分布式Cache或者Stream Service或者networking library我都不奇怪。更不用说中美脱钩的大环境下，保证自主知识产权的基础软件有多难得了。

硬件要求

16核心32G

https://pingcap.com/docs-cn/stable/hardware-and-software-requirements/#tidb-

TiDB 悲观锁 吴雪莲

tcc
tcc_cap
tcc_ord
tcc_red自带数据库

tidb客户端访问兼容myql协议

TiDB Slack

部署 TiDB 集群（包括 PD、TiDB、TiKV 等组件和监控组件） 

[CentOS6 x64下编译TiDB](https://www.cnblogs.com/blogzcan/p/8283883.html)

tidb耗硬件

pd（placement driver，提供时间戳服务和系统拓扑维护）

tidb 在线试用

无
## tikv
https://github.com/tikv/tikv

tidb 翼支付
https://www.infoq.cn/article/dhwGsHXsoIcsF5kPsWoO