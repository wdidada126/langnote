---
title: linux advance program 3rd chap 13
date: 2017-10-24 09:56:36
categories:
- Diary
tags:
- Linux
- Note

---
# linux advance program 3rd chap 13

## chap 13

https://zh.wikipedia.org/wiki/%E5%AD%97%E8%8A%82%E5%BA%8F

https://www.zhihu.com/question/637413724/answer/3344230189

x86、MOS Technology 6502、Z80、VAX、PDP-11、RISC-V等处理器为小端序；
Motorola 6800、Motorola 68000、PowerPC 970、System/370、SPARC（除V9外）等处理器为大端序；
ARM、PowerPC（除PowerPC 970外）、DEC Alpha、SPARC V9、MIPS、PA-RISC及IA64的字节序是可配置的。


小端(Little-endian)模式，操作数的存放方式为高地址存放高字节。
大端(Big-endian)模式，操作数的存放方式为高地址存放低字节。
目前，X86平台采用小端模式，网络字节顺序采用大端模式，而部分其他处理器，例如ARM处理机，既支持大端模式，亦支持小端模式。
为了统一，在网络编程时统一使用大端模式(因为网络字节顺序为大端)。

tonl()、htons()、ntohl()和ntohs()函数将实现网络字节顺序与主机字节顺序的转换。

BSD Socket网络编程

- 1、创建socket对象
socket()
- 2、绑定本地IP地址与端口
bind()
- 3、监听网络
listen()
- 4、客户端发起连接
connect()
- 5、服务器接受连接
accept()
- 6、读/写socket对象
read()
write()
- 7、TCP发送接受数据
send()
- 8、关闭socket对象
close()
