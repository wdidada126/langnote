# openwrt


lede编译
https://github.com/coolsnowwolf/lede

路由器无法连接 raw.githubusercontent.com
解决办法
https://linhongbo.com/posts/shadowsocks-on-openwrt/




https://linhongbo.com/posts/shadowsocks-on-openwrt/
这个网址有原理图


ChinaDNS原理及配置
ChinaDNS 分国内 DNS 和国外DNS。ChinaDNS 会同时向国内 DNS 和国外的 DNS 发请求，如果国外的 DNS 先返回，则采用可信 DNS 的数据；如果国内 DNS 先返回，又分两种情况，返回的数据是国内的 IP, 则采用，否则丢弃并转而采用国外 DNS 的结果。


luci汉化
https://blog.kobin.cn/blog/network/n2/1538.html

编辑opkg源

src/gz openwrt_core http://mirrors.ustc.edu.cn/lede/releases/19.07.3/targets/ramips/mt7620/packages
src/gz openwrt_base http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/base
src/gz openwrt_luci http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/luci
src/gz openwrt_packages http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/packages
src/gz openwrt_routing http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/routing
src/gz openwrt_telephony http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/telephony



src/gz openwrt_core http://mirrors.ustc.edu.cn/lede/releases/19.07.3/targets/ramips/mt7620/packages
src/gz openwrt_base http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/base
src/gz openwrt_luci http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/luci
src/gz openwrt_packages http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/packages
src/gz openwrt_routing http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/routing
src/gz openwrt_telephony http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/telephony





src/gz openwrt_core http://mirrors.aliyun.com/openwrt/releases/19.07.3/targets/ramips/mt7620/packages
src/gz openwrt_base http://mirrors.aliyun.com/openwrt/releases/19.07.3/packages/mipsel_24kc/base
src/gz openwrt_luci http://mirrors.aliyun.com/openwrt/releases/19.07.3/packages/mipsel_24kc/luci
src/gz openwrt_packages http://mirrors.aliyun.com/openwrt/releases/19.07.3/packages/mipsel_24kc/packages
src/gz openwrt_routing http://mirrors.aliyun.com/openwrt/releases/19.07.3/packages/mipsel_24kc/routing
src/gz openwrt_telephony http://mirrors.aliyun.com/openwrt/releases/19.07.3/packages/mipsel_24kc/telephony



https://mirrors.aliyun.com/openwrt/releases/19.07.3/targets/brcm2708/bcm2710/packages/
https://mirrors.aliyun.com/openwrt/releases/19.07.3/packages/aarch64_cortex-a53/base/
https://mirrors.aliyun.com/openwrt/releases/19.07.3/packages/aarch64_cortex-a53/luci/
https://mirrors.aliyun.com/openwrt/releases/19.07.3/packages/aarch64_cortex-a53/packages/
https://mirrors.aliyun.com/openwrt/releases/19.07.3/packages/aarch64_cortex-a53/routing/




阿里云镜像站官网：阿里巴巴开源镜像站-OPSX镜像站-阿里云开发者社区

阿里云openwrt源地址：https://mirrors.aliyun.com/openwrt

Openwrt更换阿里云源方法
手工替换

登录到路由器，并编辑 /etc/opkg/distfeeds.conf 文件，将其中的 downloads.openwrt.org 替换为 mirrors.aliyun.com/openwrt 即可。

自动替换

执行如下命令自动替换

sed -i 's_downloads.openwrt.org_mirrors.aliyun.com/openwrt_' /etc/opkg/distfeeds.conf

更新源

opkg update

openwrt其他推荐源地址
清华大学：mirrors.tuna.tsinghua.edu.cn/openwrt
中科大：mirrors.ustc.edu.cn/openwrt
腾讯：mirrors.cloud.tencent.com/openwrt

ss拍错思路

打印日志

Shadowsocks 输出 log
使用 - v 以让 Shadowsocks 记录 log 到指定文件：

$ /usr/bin/ss-redir -c /etc/shadowsocks.json -b 0.0.0.0 -u -v 1>>/var/log/ss-redir &
$ /usr/bin/ss-tunnel -c /etc/shadowsocks.json -b 0.0.0.0 -u -l 5353 -L 8.8.8.8:53 -v 1>>/var/log/ss-tunnel.log &
检查 Shadowsocks 中的 ss-tunnel 是否提供正确的 DNS 解析
你可以通过以下方式，在连接到 Openwrt 的主机上测试，是否可以正常通过 ss-tunnel 连接到 Shadowsocks Server 以获得未被污染的 DNS 解析结果：

首先在 Openwrt 上手动启动 ss-tunnel：

$ /usr/bin/ss-tunnel -c /etc/shadowsocks.json -b 192.168.16.1 -u -l 5353 -L 8.8.8.8:53 -v 1>>/var/log/ss-tunnel.log &
在主机上向 Openwrt 上的 ss-tunnel 请求 DNS 解析服务，注意我的 Openwrt IP 为 192.168.16.1，ss-tunnel 运行在 5353 端口下，你要根据实际情况修改：

$ dig @192.168.16.1 -p 5353 www.google.com
以下是 ss-tunnel 的日志：

2019-06-19 10:45:00 INFO: initializing ciphers... chacha20-ietf-poly1305
2019-06-19 10:45:00 INFO: listening at 192.168.16.1:5353
2019-06-19 10:45:00 INFO: UDP relay enabled
2019-06-19 10:45:04 INFO: [udp] server receive a packet
2019-06-19 10:45:04 INFO: [53] [udp] cache miss: 8.8.8.8:53 <-> 192.168.16.222:49491
2019-06-19 10:45:09 INFO: [udp] server receive a packet
2019-06-19 10:45:09 INFO: [53] [udp] cache hit: 8.8.8.8:53 <-> 192.168.16.222:49491
2019-06-19 10:45:14 INFO: [udp] server receive a packet
2019-06-19 10:45:14 INFO: [53] [udp] cache hit: 8.8.8.8:53 <-> 192.168.16.222:49491

ss-redir 建立透明代理
ss-rules 生成代理规则
ss-tunnel 提供 UDP 转发

OpenWrt的OPKG命令软件源的配置文件有以下两个：
/etc/opkg/customfeeds.conf：用户自定义源，建议把新增的软件源写在该文件中，格式为：src/gz 源名称 源地址
/etc/opkg/distfeeds.conf：发行版官方源，不建议更改，如果替换了同名称的源，可以将其内容注释掉以便恢复。

https://openwrt.org/packages/pkgdata/lsof

OpenWrt Shadowsocks 安装&配置指南
https://linhongbo.com/posts/shadowsocks-on-openwrt/


http://douxinchun.github.io/blog/20210302/install-shadowsocks-on-openwrt.html

切换中科大源
http://mirrors.ustc.edu.cn/help/openwrt.html

src/gz openwrt_core http://mirrors.ustc.edu.cn/lede/releases/19.07.3/targets/ramips/mt7620/packages
src/gz openwrt_base http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/base
src/gz openwrt_luci http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/luci
src/gz openwrt_packages http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/packages
src/gz openwrt_routing http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/routing
src/gz openwrt_telephony http://mirrors.ustc.edu.cn/lede/releases/19.07.3/packages/mipsel_24kc/telephony

https://openwrt.org/

lede
https://github.com/lede-project/source

### openwrt设置静态ip

openwrt这种网络设备，是不是对硬盘空间消耗不大？

```
ifconfig
br-lan    Link encap:Ethernet  HWaddr F2:B4:29:7E:31:66  
          inet addr:192.168.1.1  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fd33:a10d:411d::1/60 Scope:Global
          inet6 addr: fe80::f0b4:29ff:fe7e:3166/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:226507 errors:0 dropped:0 overruns:0 frame:0
          TX packets:69635 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:17890245 (17.0 MiB)  TX bytes:27538847 (26.2 MiB)

eth0      Link encap:Ethernet  HWaddr F0:B4:29:7E:31:66  
          inet6 addr: fe80::f2b4:29ff:fe7e:3166/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:141960 errors:0 dropped:0 overruns:0 frame:0
          TX packets:91312 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:68874296 (65.6 MiB)  TX bytes:13180038 (12.5 MiB)
          Interrupt:5 

eth0.1    Link encap:Ethernet  HWaddr F2:B4:29:7E:31:66  
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:141737 errors:0 dropped:27 overruns:0 frame:0
          TX packets:85525 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:66299630 (63.2 MiB)  TX bytes:10985604 (10.4 MiB)

eth0.2    Link encap:Ethernet  HWaddr F0:B4:29:7E:31:66  
          inet6 addr: fe80::f2b4:29ff:fe7e:3166/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:5007 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:1676764 (1.5 MiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:36272 errors:0 dropped:0 overruns:0 frame:0
          TX packets:36272 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:3382678 (3.2 MiB)  TX bytes:3382678 (3.2 MiB)

wlan0     Link encap:Ethernet  HWaddr F0:B4:29:7E:31:68  
          inet6 addr: fe80::f2b4:29ff:fe7e:3168/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:253470 errors:0 dropped:0 overruns:0 frame:0
          TX packets:155427 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:29780494 (28.4 MiB)  TX bytes:98494456 (93.9 MiB)
```

01

02 一个2.5g 一个5g？

bootloader (like u-boot)

https://openwrt.org/docs/guide-user/troubleshooting/failsafe_and_factory_reset

https://blog.csdn.net/csdn__lc/article/details/61451417

小米路由器上有txt文件


家用路由器Lan口之间的设备工作在IP层还是数据链路层？
https://www.zhihu.com/question/354935688

br-lan

是交换层

分出wlan1

## OpenWrt
OpenWrt是一个基于Linux的嵌入式操作系统，最初是为了支持家用无线路由器而开发的。其开发和演变有着独特的历史和背景：

起源：
Linksys WRT54G：OpenWrt的故事开始于2002年，Linksys发布了WRT54G无线路由器。这个设备运行的是一个基于Linux的操作系统，这意味着根据GPL协议，Linksys必须公开其源代码。
开发者社区：早期的黑客和开发者利用公开的源代码，开始为WRT54G开发自定义固件，以增加其功能和性能。这些自定义固件的不断演变最终形成了OpenWrt项目。
早期发展：

Freifunk和Sveasoft：在OpenWrt诞生之前，有几个项目已经开始尝试为WRT54G等设备开发自定义固件。Freifunk和Sveasoft就是其中两个重要的项目，它们为OpenWrt的发展奠定了基础。
OpenWrt的诞生：2004年，OpenWrt项目正式启动，目标是创建一个模块化、可扩展的嵌入式Linux系统，专注于路由和网络功能。