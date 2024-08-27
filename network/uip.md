# uip

uip这个库一千多行，有资料可参考有代码可借鉴的情况下确实不难。

UIP由瑞典计算机科学学院(网络嵌入式系统小组)的Adam Dunkels开发.
.良好的文档和源代码注释 - 几乎每一行代码都有注释.
.代码非常少.
.占用非常少的内存, 在编译时候可以设置.
.支持ARP, SLIP, IP, UDP, ICMP(ping)和TCP协议.
.提供一套实例程序: web服务器, web客户端, 电子邮件发送程序(SMTP客户端), Telnet服务器, DNS主机名解析程序.
.同时活动的TCP链接数没有限制, 在编译时候可以设置.
.可免费用于商业和非商业用途.
.TCP和IP协议遵循RFC标准, 包括流控制, 片断分割和重传超时估算.

UIP计算机网络库的源代码托管地址是：https://github.com/adamdunkels/uip

http://www.sics.se/~adam/uip/

uIP is a very small implementation of the TCP/IP stack that is written
by Adam Dunkels <adam@sics.se>. More information can be obtained 
at the uIP homepage at http://www.sics.se/~adam/uip/.

This is version $Name: uip-1-0 $.

The directory structure look as follows:

apps/  - Example applications
doc/   - Documentation
lib/   - Library code used by some applications
uip/   - uIP TCP/IP stack code
unix/  - uIP as a user space process under FreeBSD or Linux


## 编译
git clone https://github.com/adamdunkels/uip
cd uip/unix
make
sudo make install

## 精品
lwip
LIP（Lightweight Interlayer Protocol）
