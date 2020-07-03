---
title: 图解tcpip 5st
date: 2017-10-24 19:56:36
categories:
- Diary
tags:
- Network
- Note
---

### Chap.1



cobol fortran 必须批处理系统为基础才能开发和运行

basic 分时操作系统 独占性 能够与计算机实时交互




DNS(Domain Name System)
域名系统
根据域名，找到IP地址

ARP
Address Regulation Protocal。只适用于IPv4。
功能，在数据链路层，根据ip地址，找到mac地址。

为什么同时需要ip地址和mac地址？
ip地址在网络间适用，mac地址在同一网络内适用。
如果只适用mac地址，交换机需要维护一个大的mac地址表，不合适。


DHCP
为了实现自动配置IP地址，统一管理IP地址分配，就产生了DHCP(Dynamic Host Configuration Protocal)协议。
DHCP协议既适用于IPv4，也适用于IPv6。

NAT
NAT(Network Address Translator)是用于在本地网络中适用私有地址，在连接互联网时转而适用全局IP地址的技术。
NAPT(Nerowrk Address Ports Translator)转换TCP、UDP端口号，可以实现用一个全局IP地址与多个主机的通信。

IP隧道
解决IPv4网络和IPv6网络之间的通信问题。在网络层的首部后面继续追加网络层首部的通信方法叫做“IP隧道“。





``





应用层协议 注意socks