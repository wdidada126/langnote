# keepalived
Keepalived是一款用于实现高可用性（HA）和负载均衡的开源工具，核心功能包括健康检查、故障切换和VRRP协议支持。
虚拟ip
新建局域网
一旦局域网一台挂掉，可以动态添加

keepalive配置mysql自动故障转移
https://blog.csdn.net/u010391029/article/details/48470295

Keepalive+mysql主主同步
https://blog.csdn.net/hizamaru/article/details/88206068

利用keepalive+mysql replication 实现数据库的高可用

利用mysql自带的replication和keepalive提供的虚拟IP和故障检查来实现数据库的高可用
replication 就是主备
https://www.cnblogs.com/lengfo/p/4212910.html

本文主要记录了基于Linux环境下的Mysql Replication配置步骤。
https://dev.mysql.com/doc/refman/5.7/en/replication-solutions.html

## 官网
https://www.keepalived.org/

## 编程语言
c
## 协议

## 版本
v2.3.4 2025  Jun 11
2024-11-03 | Release 2.3.2
This release brings improvements and fix some issues reported. Refer to Release Notes for more infos.

2024-05-24 | Release 2.3.1
Minutes release to fix minor regression. Refer to Release Notes for more infos.

2024-05-21 | Release 2.3.0
This release brings improvements and fix some minor issues reported. Refer to Release Notes for more infos.

2023-05-31 | Release 2.2.8
This release brings improvements and fix some minor issues reported. It add some new VRRP and BFD features as well. Refer to Release Notes for more infos.

2022-01-16 | Release 2.2.7
This release brings lots of improvements and fix some minor issues reported. It add some new VRRP features as well. Stability has been even more extended. Refer to Release Notes for more infos.

2021-08-21 | Release 2.2.4
This release fix some minor build issues brought by last release. All coverity open issues are fixed. Refer to Release Notes for more infos.

2021-08-14 | Release 2.2.3
This release add some new features and fix some minor bugs. genhash utility is now part of the mainline daemon. Refer to Release Notes for more infos.

2021-03-05 | Release 2.2.2
This release fix some minor systemd integration issues. Its drops old kernel related support. Refer to Release Notes for more infos.

2021-01-17 | Release 2.2.1
This release fix some minor regressions brought by last release. Refer to Release Notes for more infos.

2021-01-09 | Release 2.2.0
This release bring a bunch of new features and extensions. This release targetted corner cases and resilient handling. This release is a major milestone for us ! please consider upgrading, this is the fruit of hard stabilization and non-regression effort. Refer to Release Notes for more infos.

2020-07-13 | Release 2.1.5
This is a minute fix release, fixing regression on include directive. Refer to Release Notes for more infos.

2020-07-10 | Release 2.1.4
This release extend some documentation elements. Some fix for the building process. DNS_CHECK fix and extensions. Properly handle ipvs_sync_daemon. Refer to Release Notes for more infos.

2020-06-23 | Release 2.1.3
This release fix 2 uninitialized list which can lead to a SEGV when using track_process or track_bfd. There are some minor fixes, IPVS configurations improvements and some cosmetics. Refer to Release Notes for more infos.

2020-06-14 | Release 2.1.2
This is a minute fix release. Refer to Release Notes for more infos.

2020-06-13 | Release 2.1.0
Lot of efforts have been put all together to make this new release even more robust. Refer to Release Notes for more infos.

2020-01-22 | Release 2.0.20
Fix track process and track script features. Some BFD extensions and cleanup. Reworked debug configuration. Snap updates. Docker updates. Add support to set pref lft for static and virtual IPv6 addresses. Refer to ChangeLog for more infos.

## 源代码编译
https://github.com/acassen/keepalived