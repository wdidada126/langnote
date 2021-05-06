# tcpdump

如何为Tcpdump指定主机，端口和协议
https://blog.csdn.net/cunjiu9486/article/details/109075736

tcpdump tcp port 8500 -n -X -s 0
抓包http，显示数据内容 测试显示不全

tcpdump tcp port 8500 -n -s 0 -w /tmp/tcp.cap

yum install tcpdump -y

[Linux 网络分析必备技能：tcpdump 实战详解](https://mp.weixin.qq.com/s/vzNgYRZigR1Buay17gcfrg)

tcpdump -i -s 0 

tcpdump -X -ni eth0 src host 36.7.110.63 dst port 8500

centos 6 7

kvm虚机

性能损耗



[linux tcpdump抓取HTTP包的详细解释](https://www.jb51.net/LINUXjishu/600345.html)



[使用tcpdump+Wireshark抓包分析kafka通信协议](https://blog.csdn.net/icycode/article/details/80034774)


```shell
tcpdump -n -i eth0
12:55:24.171093 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 541084:541232, ack 73, win 257, length 148
12:55:24.171150 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 541232:541380, ack 73, win 257, length 148
12:55:24.171598 IP 36.7.68.71.7535 > 172.16.0.17.ssh: Flags [.], ack 540092, win 1026, length 0
12:55:24.171617 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 541380:541528, ack 73, win 257, length 148
12:55:24.171695 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 541528:541780, ack 73, win 257, length 252
12:55:24.171756 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 541780:541928, ack 73, win 257, length 148
12:55:24.197586 IP 36.7.68.71.7535 > 172.16.0.17.ssh: Flags [.], ack 541380, win 1029, length 0
12:55:24.197641 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 541928:542076, ack 73, win 257, length 148
12:55:24.197792 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 542076:542328, ack 73, win 257, length 252
12:55:24.197900 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 542328:542476, ack 73, win 257, length 148
12:55:24.197973 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 542476:542624, ack 73, win 257, length 148
12:55:24.198076 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 542624:542772, ack 73, win 257, length 148
12:55:24.198139 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 542772:542920, ack 73, win 257, length 148
12:55:24.198199 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 542920:543068, ack 73, win 257, length 148
12:55:24.198257 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 543068:543216, ack 73, win 257, length 148
12:55:24.198582 IP 36.7.68.71.7535 > 172.16.0.17.ssh: Flags [.], ack 541928, win 1026, length 0
12:55:24.198601 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 543216:543364, ack 73, win 257, length 148
12:55:24.198677 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 543364:543616, ack 73, win 257, length 252
12:55:24.198735 IP 172.16.0.17.ssh > 36.7.68.71.7535: Flags [P.], seq 543616:543764, ack 73, win 257, length 148
12:55:24.202547 IP 36.7.68.71.7535 > 172.16.0.17.ssh: Flags [P.], seq 73:109, ack 541928, win 1026, length 36
```

tcpdump -ni eth0 host 192.168.1.100

tcpdump -ni eth0 src host 10.1.1.2

tcpdump -ni eth0 dst host 10.1.1.2

tcpdump -ni eth0 -c 10 dst host 192.168.1.200   7. 抓取 eth0 网卡上发往指定主机的数据包，抓到 10 个包就停止，这个参数也比较常用

tcpdump -ni eth0 dst port 22 8. 抓取 eth0 网卡上所有 SSH 请求数据包，SSH 默认端口是 22



```shell
tcpdump --version
tcpdump version 4.9.2
libpcap version 1.5.3
OpenSSL 1.0.2k-fips  26 Jan 2017
```
