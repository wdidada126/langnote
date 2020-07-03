# openwrt

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



https://www.zhihu.com/question/354935688



br-lan

是交换层

分出wlan1

