# tcp

HPCC

Tcp选项和各个字段含义

https://zhuanlan.zhihu.com/p/88621517


源端口，目标端口
校验和

hercules_3-2-8
windows平台tcp报文测试工具

tcp的数据，如何判断上层协议
首先，tcp拆包的时候，是不管上层协议类型的
判断应用层协议内容
根据port来？
HTTP/VERSION
kafka-apiversion 18 15之类的





同步异步

阻塞 非阻塞





## 几种开源的TCP/IP协议栈分析

https://blog.csdn.net/duanbingnan/article/details/1956084?utm_source=blogxgwz9





1、阻塞与非阻塞
是相对于连接过程是否等待，或者说连接中是否可做其它事。
serverSocket接收socket连接且等待直到连接上为止，即为阻塞。
serverSocket接口连接后，不等待连接上，又去接收新的连接，轮询地处理连接或连接就绪等事件，即为非阻塞。

2、同步与异步
是相对于结果而言的，即是否等待结果返回。等待结果的即是同步，不等待结果的即是异步。
在这里，socket等待直到读取到数据为止，即是同步。
socket不等待读取到数据，而去做别的事，当数据准备好后，会通知socket数据已经准备好了，这就是异步。

原文链接：https://blog.csdn.net/chinabestchina/article/details/78278054

### tcp实验
CS144

https://kiprey.github.io/2021/11/cs144-lab4/


stanford

## netstat

lwip

Twip（Tencent WEB Real-Time Communication Protocol）是腾讯公司开发的一种实时通信协议，用于在互联网上传输实时音视频数据。Twip基于UDP协议，提供了实时、高效和低延迟的通信能力。

KCP（KCP over UDP）是一种快速可靠的数据传输协议，它使用UDP协议进行传输，但在传输过程中采用了类似于TCP的可靠性和流量控制机制。KCP通过快速重传、快速恢复和拥塞控制等技术，提高了数据传输的可靠性和效率。


