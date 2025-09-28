# MySQL核心优化课

吴炳锡

知数堂资深MySQL讲师

前新媒传信(⻜信运营) SA, MySQL DBA, DB Architect

新媒传信技术管理委员会成员 新媒传信高级讲师

专注于后端高性能服务及 DB 存储治理

中国MySQL用户组主席(acmug.com),知名MySQL DBA圈子FireFly DBA Club发起人



叶金荣

资深MySQL专家, MySQL布道师， Oracle ACE(MySQL)

曾任职搜狐畅游DBA主管，17173系统部经理

精通MySQL数据库，10多年专业MySQL DBA经验

专注于MySQL性能优化，擅长MySQL优化、架构设计、故障处理

中国MySQL用户组主席(acmug.com)

ChinaUnix社区MySQL版块版主





MySQL DBA优化班
MySQL运行环境部署规范
学习目标：
1、了解MySQL对CPU、内存、I/O子系统资源利用特点
2、根据MySQL的特点，制定通用的部署规范
MySQL容量规划、性能测试
学习目标
1、初步认识什么是性能基线
2、掌握性能容量规划方法
3、掌握MySQL性能测试的方法
深入理解MySQL体系结构
学习目标：
1、从整体上认识MySQL体系结构
2、了解MySQL内置支持了哪些存储引擎，关键几种存储引擎见的区别及其适用场景
3、了解当前最热门的几个第三方引擎
深入理解MySQL
学习目标：
1、深入理解MySQL索引知识
2、深入理解MySQL事务特性
3、深入理解InnoDB引擎
全面优化MySQL
学习目标
1、解读从硬件到系统的优化方法
2、解读MySQL中关键配置参数优化方法
3、选择典型Schema设计案例，解读Schema优化设计思路
4、全面认识索引的特点，以及优化使用实践经验
5、选取经典SQL优化案例进行讲解，掌握SQL优化思路
6、重点介绍Percona、MariaDB分支版本对原生版本的优化提升效果
7、分享MySQL最佳开发设计规范经验






MySQL DBA实战课程
初识MySQL
学习目标：
1、了解MySQL的历史及MySQL不同版本的Life Cycle
2、统一明确学习的重点知识方便大家系统的学习
MySQL安装及结构
学习目标：
1、初步学习MySQL的安装
2、DBA人生不再有数据库起不来的问题
3、全面认识MySQL的存储引擎，能了解不同的业务需要考虑选择不同的引擎来处理
认识数据库中的对象及高级特性（开发篇）
学习目标：
1、了解数据类型,会选择合适的数据类型
2、了解索引的使用及如何选择合适的列做为索引
3、正确对数据库的高级特性,明白这些特性在实际生产中的作用
MySQL管理维护
学习目标：
1、熟练MySQL帐号的管理
2、选择正确的字符集,能正确处理乱码案例
MySQL复制
学习目标：
1、了解复制的布署结构及约束
2、掌握几种复制的特点，应用注意事项
3、了解业务常见的复制架构，方便以后业务中选型
4、熟悉掌握复制中运维技能，有能力能管理相应的复制结构
MySQL备份恢复
学习目标：
1、从理论上学习备份恢复的概念
2、了解常见的备份工具工作的原理
3、熟悉掌握mysqldump的使用
4、熟练掌握xtrabackup的使用
5、认识mysql binlog的物理结构，了解binlog里都有什么内容
6、学习利用binlog恢复误操作
7、学习Innodb引擎单表移动的方法
8、从备份中恢复单表的方法
MySQL配置优化
学习目标：
1、全面理解MySQL配置文件
2、根据业务需要去优化MySQL的配置
MySQL监控指标
学习目标：
1、了解监控系统的意义
2、会使用监控系统中的重要指标
MySQL高可用
学习目标：
1、了解高可用的意义及实现方法
2、学习撑握高可用的方法及运维能力
3、学习proxy模型的工用原理及使用中的局限
4、了解MySQL NDBcluster的实现及优化缺点
MySQL和NoSQL结合优化
学习目标：
1、学习Redis的高可用架构
2、学习如何规范的使用Redis
3、在项目中可以学会使用Redis给MySQL加速
MySQL综合案例实践
学习目标：
1、学会并可以熟练使用在线表结构变更的方法
2、掌握SQL并发执行和串行执行的一些技巧；
3、利用sort,uniq,egrep命令代替sql统计的一些建议;
4、掌握大规模部署的一些技能
5、了解大规模运维中的一些注意事项，让工作少掉几次坑
6、学习数据拆分后表结构变更或是表数量变化后数据迁移的技巧
7、学习数据库升级的一些技巧
8、学习对于主从结构运行一段后数据一致性校验及修复的方法;
如何写简历及面试
学习目标：
1、学会自已写简历
2、学会全方位给自已争取到工作的机会



资深MySQL专家叶金荣、 吴炳锡联合推

出专业优质在线培训课程

知数堂培训&3306π社区联合创始人，资深MySQL专家，MySQL布道师，Oracle MySQL ACE，腾讯云TVP成员。曾任职搜狐畅游DBA主管，17173系统部经理，精通MySQL数据库，10多年专业MySQL DBA经验，擅长MySQL优化、架构设计、故障处理。



知数堂培训&3306π社区联合创始人，业界知名MySQL DBA从业人员，腾讯云TVP成员。曾任职新媒传信首席DBA。多年MySQL及系统架构设计及培训教学经验，擅长讲授：MySQL运维， 数据库高可用及多IDC架构设计，企业DB设计及系统架构和优化。





其中最句代表性的是Amazon的Dynamo以及Google的BigTable，以及他们对应的开源版本像Cassandra以及HBase。

http://mysql.taobao.org/monthly/2020/12/01/



NoSQL也有很明显的问题，由于缺乏强一致性及事务支持，很多业务场景被NoSQL拒之门外。同时，缺乏统一的高级数据模型、访问接口，又让业务代码承担了很多的负担。图灵奖得主Michael Stonebraker甚至专门发文声讨，”Why Enterprises Are ­Uninterested in NoSQL” [3] 一文中，列出了NoSQL的三大罪状：No ACID Equals No Interest， A Low-Level Query Language is Death，NoSQL Means No Standards。数据库的历史就这样经历了否定之否定，又螺旋上升的过程。


InnoDB为了支持多粒度(表锁与行锁)的锁并存，引入意向锁。
意向锁是表级锁，可分为意向共享锁(IS锁)和意向排他锁(IX锁)。



https://blog.csdn.net/ignorewho/article/details/86422137



@@innodb_page_size

select @@innodb_page_size;

+--------------------+

| @@innodb_page_size |

+--------------------+

|       16384 |

+--------------------+

1 row in set (0.04 sec)


stanford cs140e 2018 os课程

BestTrace 
租机器，跑亿级数据量的sql





计算机是一种实验的科学，性能优化是实战的艺术。



数据文件：.frm、.MYI、.MYD、.ibd、.ibdata*、.ib_logfile*、undo*、ibtmp1、auto.cnf、db.opt、.CSM、.CSV、.TRN、.TRG。
● .frm：表结构定义文件。
● .MYI:MyISAM存储引擎索引文件。
● .MYD:MyISAM存储引擎数据文件。
● .ibd:InnoDB存储引擎独立表空间文件。
● .ibdata*:InnoDB存储引擎共享表空间文件。
● .ib_logfile*:InnoDB存储引擎redo log文件。
● undo*:InnoDB存储引擎独立undo文件。
● ibtmp1:InnoDB存储引擎临时表空间文件。
● auto.cnf：用于存放MySQL实例的全局唯一的server-uuid的文件。
知数堂《MySQL核心优化课》大纲（2020年最新版）

https://imysql.com/2020/05/27/zhishutang-mysql-optimizing-trainning-course.shtml

