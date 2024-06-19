# dig

ubuntu系
sudo apt-get install dnsutils
centos系
sudo yum install bind-utils -y

Installed:
  bind-utils.x86_64 32:9.11.4-26.P2.el7_9.16                                                                                                                                      

Dependency Installed:
  GeoIP.x86_64 0:1.5.0-14.el7        bind-libs.x86_64 32:9.11.4-26.P2.el7_9.16   bind-libs-lite.x86_64 32:9.11.4-26.P2.el7_9.16   bind-license.noarch 32:9.11.4-26.P2.el7_9.16  
  geoipupdate.x86_64 0:2.5.0-2.el7 
  
https://www.jianshu.com/p/f6ef04bf6af2

dig工具
dig是另一款域名查询工具，其功能非常强大，并且可以指定源 IP 地址，这在主机上有多个接口及 IP 地址时非常有用。
dig 在进行域名查询时，如果第一个域名服务器无响应，将在 1 秒后向第二个 DNS 地 址发起请求。在这点上它和 nslookup 不同，nslookup 需要等待 5 秒之后再向第二个域名服 务器发起查询请求。
基本的用法
①@后面表示 DNS 服务器地址：
dig @server baidu.com
1.
②“-b”表示指定源 IP，在系统有多个接口地址时使用。
dig -b 192.168.1.100 baidu.com
1.
dig 提供了大量的查询选项和输出结果显示选项。一些查询选项会设置查询报头的标 志位，有些是设置超时和重试策略，还有些是控制屏幕输出。dig 的查询选项和其他软件 不同，采用“+”开头的标识符来表示。
dig 还有很多选项可以定制查询和输出。例如+short 可以简化输出。默认 dig 会输出 DNS 报头信息，包含查询问题个数和回答问题个数等信息。
-----------------------------------
©著作权归作者所有：来自51CTO博客作者董哥的黑板报的原创作品，请联系作者获取转载授权，否则将追究法律责任
全方面讲解OpenWrt的DNS配置与DHCP，并介绍dnsmasq DNS缓存工具、nslookup/dig DNS测试工具
https://blog.51cto.com/u_15346415/5224179


简略输出
dig www.google.com +short


dig www.google.com +noall +answer


指定 DNS 服务器
dig @8.8.8.8 www.google.com