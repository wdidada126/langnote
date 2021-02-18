# 千金良方：MySQL性能优化金字塔法则

https://book.douban.com/subject/34860934/

李春，原阿里巴巴MySQL DBA团队技术Leader，全程参与阿里数据库架构从Oracle迁移到MySQL的过程，参与分布式中间件Cobar设计。现为沃趣科技联合创始人&首席架构师，负责MySQL、基础软件及部分关键组件的技术选型、风险评估等。
罗小波，沃趣科技高级数据库工程师，主要负责MySQL产品的数据库支撑与售后二线支撑。曾参与版本发布系统、轻量级监控系统、运维管理平台、数据库管理平台的设计与编写，熟悉MySQL体系结构，Innodb存储引擎，喜好专研开源技术，多次在公开场合做过线下线上数据库专题分享，发表过多篇与数据库相关的研究文章。
董红禹，沃趣科技MySQL DBA ， 为过多家大型企业进行过故障解决、架构设计、性能优化，例如中信证券、浙江农信、陕西农信、邮储银行等。规划并实施了浙江农信互联网核心金融平台。



本书一共分为3篇：基础篇、案例篇和工具篇。“基础篇”从理论基础和基本原理层面介绍了MySQL的安装与配置、升级和体系结构，information_schema、sys_schema、performance_schema和mysql_schema, MySQL复制，MySQL事务，SQL语句优化及架构设计基础知识。“案例篇”从硬件和系统、MySQL架构等方面给出了性能优化的十几个案例，包括：性能测试的基本优化思路和最需要关注的性能指标解释、对日常SQL语句执行慢的基本定位、避免x86可用性的一般性方法、节能模式会怎样影响性能、I/O 存储作为数据库最重要的依赖是如何影响数据库性能的、主备复制不一致可能有哪些原因、字符集不一致会造成哪些性能问题、在实际场景中锁的争用是怎样的。“工具篇”介绍了在MySQL性能优化过程中需要用到的各种工具，包括：dmidecode、top、dstat等硬件和系统排查工具；FIO、sysbench、HammerDB等压力测试工具；mysqldump、XtraBackup等备份工具；Percona、innotop、Prometheus等监控工具

下载了电子版，Mac电脑，讯飞公司电脑


刀片服务器

机架服务器

linux kernel
mysql source code

sysbeanch 测试mysq server

CPU： E5-2696 V3


第32章 MySQL挂起诊断思路

sysbeanch 测试


### Chap. 21 SQL优化

SQL审核平台

B+树特点
数据只存在叶子节点
非叶子节点，只存储索引

之所以采用B+Tree结构， 是因为数据库中有>、 <、 between … and这类范围查询语
句， 直接扫描叶子节点即可。

InnoDB的所有的表都是索引组织表， 主键与数据存放在一起。 InnoDB选择聚集索引
遵循以下原则：
• 在创建表时， 如果指定了主键， 则将其作为聚集索引。
• 如果没有指定主键， 则选择第一个NOT NULL的唯一索引作为聚集索引。
• 如果没有唯一索引， 则内部会生成一个6字节的rowid作为主键。




InnoDB为了支持多粒度(表锁与行锁)的锁并存，引入意向锁。

意向锁是表级锁，可分为意向共享锁(IS锁)和意向排他锁(IX锁)。



https://blog.csdn.net/ignorewho/article/details/86422137





@@innodb_page_size



select @@innodb_page_size;
+--------------------+
| @@innodb_page_size |
+--------------------+
|       16384       |
+--------------------+

1 row in set (0.04 sec)

https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html

Index Condition Pushdown
索引条件下推
https://dev.mysql.com/doc/refman/5.7/en/index-condition-pushdown-optimization.html
中文解释
https://www.cnblogs.com/zhoujinyi/archive/2013/04/16/3016223.html
