# lwip

windows编译 vs调试

lwip应用场景？ 单片机 没有操作系统

linux kernel实现了tcp ip协议栈

[LwIP常见问题](http://blog.sina.com.cn/s/blog_62a85b950102xdjx.html)

QQ群
224362301
群主博客
http://blog.sina.com.cn/s/blog_62a85b950102xdjx.html

嵌入式网络那些事：LwIP协议深度剖析与实战演练 书籍

https://book.douban.com/subject/20273405/

[TCP/IP协议栈之QEMU（零）--- LwIP开发调试环境搭建](https://blog.csdn.net/m0_37621078/article/details/103190694)
LwIP应用开发实战指南：基于STM32（书籍）
本书围绕LwIP 2.1.2版本源码讲解TCP/IP网络协议栈的基本知识，带领读者进入网络的世界。无论你是学生、嵌入式开发者还是物联网开发者，都可以从本书中学习到网络的相关知识，了解网络协议栈的处理思想。
本书将深入分析网络协议栈的原理与实现过程，涉及ARP、IP、ICMP、TCP、UDP、HTTP、MQTT等协议，还将深入讲解LwIP中内存管理、pbuf数据包、网卡接口管理的原理与实现，并详细介绍LwIP的移植过程，读者可以将其移植到无操作系统/有操作系统的环境中使用。

记忆tcp状态图

repo
https://github.com/lwip-tcpip/lwip

Reading Adam's papers, the files in docs/, browsing the source code
documentation and browsing the mailing list archives is a good way to
become familiar with the design of lwIP.

https://www.nongnu.org/lwip/2_1_x/index.html

https://lwip.fandom.com/wiki/LwIP_Wiki

https://gitee.com/edidada/lwip-2.1.3
file:///D:/git/gitee/lwip-2.1.3/doc/doxygen/output/html/changelog.html

lwip1.4.0 http server实现及POST 实现
https://blog.csdn.net/lijing198997/article/details/25987193

LwIP应用开发笔记之七：LwIP无操作系统HTTP服务器
http://t.zoukankan.com/foxclever-p-12045235.html

lwIP（Lightweight IP）是一个用于嵌入式系统的开源TCP/IP协议栈。它旨在在资源受限的环境中运行，如嵌入式系统和物联网设备。lwIP提供了一个轻量级的TCP/IP协议栈实现，具有低内存占用和低功耗的特点。
lwIP提供了常见的网络协议和功能，包括TCP、UDP、ARP、ICMP、DHCP、DNS等。它还提供了一些高级功能，如IP分片、TCP窗口缩放和IPv6支持。lwIP的设计目标是提供高效的协议实现，同时保持简单和易于移植性。
lwIP适用于各种嵌入式系统，如微控制器、FPGA和DSP等。它可以通过各种通信接口与硬件设备进行通信，如UART、SPI、Ethernet等。通过使用lwIP，嵌入式系统可以连接到互联网，与其他设备进行通信，并实现各种网络应用。
lwIP的源代码是用C语言编写的，易于阅读和理解。它提供了详细的文档和示例代码，以帮助开发者快速上手并使用lwIP。由于其开源性质，开发者可以根据自己的需求对lwIP进行定制和修改。
总的来说，lwIP是一个功能强大且易于使用的开源TCP/IP协议栈，适用于嵌入式系统和物联网设备。通过使用lwIP，开发者可以在资源受限的环境中实现可靠的网络通信和各种网络应用。

## source code 源代码
https://github.com/lwip-tcpip/lwip

c语言写的
### 编译
https://github.com/lwip-tcpip/lwip/blob/master/.github/workflows/ci-linux.yml

os：ubuntu

```shell
sudo apt-get install check ninja-build doxygen
git clone https://github.com/lwip-tcpip/lwip.git
cd lwip
git checkout STABLE-2_2_0_RELEASE
cp contrib/examples/example_app/lwipcfg.h.ci contrib/examples/example_app/lwipcfg.h
make -C contrib/ports/unix/check
make -C contrib/ports/unix/check check
mkdir build && cd build && cmake .. -G Ninja
cd build && cmake --build .
cd build && cmake --build . --target lwipdocs
cd contrib/ports/unix/example_app && ./iteropts.sh
cp contrib/examples/example_app/lwipcfg.h.example contrib/examples/example_app/lwipcfg.h
make -C contrib/ports/unix/example_app TESTFLAGS="-Wno-documentation" -j 4
```

### wiki
https://lwip.wikia.com/wiki/LwIP_Wiki
