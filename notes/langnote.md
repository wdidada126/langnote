# git repo reference

[Ubuntu 16.04下将ISO镜像制作成U盘启动的工具-UNetbootin（UltraISO的替代工具）](https://www.cnblogs.com/EasonJim/p/8169707.html)



[RE summary](https://deerchao.net/tutorials/regex/regex.htm)



TCP状态图

CLOSED: 表示初始状态。
LISTEN: 表示服务器端的某个SOCKET处于监听状态，可以接受连接。
SYN_SENT:在服务端监听后，客户端SOCKET执行CONNECT连接时，客户端发送SYN报文，此时客户端就进入
SYN_SENT状态，等待服务端的确认
SYN_RCVD: 表示服务端接受到了SYN报文，在正常情况下，这个状态是服务器端的SOCKET在建立TCP连接时的三
次握手会话过程中的一个中间状态，很短暂，基本上用netstat你是很难看到这种状态的，除非你特意写了一
个客户端测试程序，故意将三次TCP握手过程中最后一个ACK报文不予发送。因此这种状态时，当收到客户端的
ACK报文后，它会进入到ESTABLISHED状态。
ESTABLISHED：表示连接已经建立了。
FIN_WAIT_1: 这个是已经建立连接之后，其中一方请求终止连接，等待对方的FIN报文。FIN_WAIT_1状态是当
SOCKET在ESTABLISHED状态时，它想主动关闭连接，向对方发送了FIN报文，此时该SOCKET即进入到FIN_WAIT_1
状态。而当对方回应ACK报文后，则进入到FIN_WAIT_2状态，当然在实际的正常情况下，无论对方何种情况下
，都应该马上回应ACK报文，所以FIN_WAIT_1状态一般是比较难见到的，而FIN_WAIT_2状态还有时常常可以用
netstat看到。
FIN_WAIT_2：实际上FIN_WAIT_2状态下的SOCKET，表示半连接，也即有一方要求close连接，但另外还告诉对
方，我暂时还有点数据需要传送给你，稍后再关闭连接。
TIME_WAIT: 表示收到了对方的FIN报文，并发送出了ACK报文，就等2MSL后即可回到CLOSED可用状态了。如果
FIN_WAIT_1状态下，收到了对方同时带FIN标志和ACK标志的报文时，可以直接进入到TIME_WAIT状态，而无须
经过FIN_WAIT_2状态。
CLOSING: 这种状态比较特殊，实际情况中应该是很少见，属于一种比较罕见的例外状态。正常情况下，当你
发送FIN报文后，按理来说是应该先收到(或同时收到)对方的ACK报文，再收到对方的FIN报文。但是CLOSING状
态表示你发送FIN报文后，并没有收到对方的ACK报文，反而却也收到了对方的FIN报文。什么情况下会出现此
种情况呢？其实细想一下，也不难得出结论：那就是如果双方几乎在同时close一个SOCKET的话，那么就出现
了双方同时发送FIN报文的情况，也即会出现CLOSING状态，表示双方都正在关闭SOCKET连接。
CLOSE_WAIT: 这种状态的含义其实是表示在等待关闭。怎么理解呢？当对方close一个SOCKET后发送FIN报文给
自己，你系统毫无疑问地会回应一个ACK报文给对方，此时则进入到CLOSE_WAIT状态。接下来呢，实际上你真
正需要考虑的事情是察看你是否还有数据发送给对方，如果没有的话，那么你也就可以close这个SOCKET，发
送FIN报文给对方，也即关闭连接。所以你在CLOSE_WAIT状态下，需要完成的事情是等待你去关闭连接。
LAST_ACK: 这个状态还是比较容易好理解的，它是被动关闭一方在发送FIN报文后，最后等待对方的ACK报文。
当收到ACK报文后，也即可以进入到CLOSED可用状态了。



约定优先配置
conversion over configuration



SpringCloud是
Maven也是

- [Spring测试例子](https://github.com/edidada/SpringExample)
- [Java标准库例子](https://github.com/edidada/testjdk8)
- [iOS开发指南 随书源码](https://github.com/edidada/iOSBook14)
- [spring-framework-git-4.3.12](https://github.com/edidada/spring-framework-git-4.3.12)

##### c
##### oc
##### C++
##### Java

Lean note


c++ bind()报错

[报错日志](https://paste.ubuntu.com/p/9K3WtjDRpq/)

string作为函数参数 引用传递

```c
class LoginJsonForm {
public:
    void makejsons(string username,string & jsonResult);
private:

};
```
list遍历

```c
list<Blog> r;
list<Blog>::iterator iter;
for (iter = r.begin(); iter != r.end(); iter++) {
    std::cout << iter->userName << std::endl;
}
```

笔记散落在多个地方

git repo
（github，多个账号 gitee coding.net）

云笔记
有道 为知 

计算机硬盘md txt格式文件

git 分布式存储

科技论坛Hack News

LocalMQ：从零构建类 RocketMQ 高性能消息队列
https://zhuanlan.zhihu.com/p/27693508

Nana is a cross-platform library for GUI programming in modern C++ style
http://nanapro.org/en-us/

【Parser系列】实现LR分析——完成编译器前端
https://zhuanlan.zhihu.com/p/53070412
https://github.com/bajdcc/clibparser

PolarDB数据库性能大赛参赛总结
https://zhuanlan.zhihu.com/p/52348656

算法第四版C++答案
https://github.com/ISCASTEAM/Algorithm

yacc lex
http://dinosaur.compilertools.net/

[禁ping icmp](https://blog.csdn.net/selfi_xiaowen/article/details/70171273)

计算机相关问题：
开多少个线程
线程亲和性
怎么样跨进程传递数据最无痛
怎么减少内核态用户态切换
cache命中优化

在命令行模式下输入1G可以跳转到页面的头部位置

更多在vi中移动编辑位置的命令说明如下：

h Move left
j Move down
k Move up
l Move right
w Move to next word
W Move to next blank delimited word
b Move to the beginning of the word
B Move to the beginning of blank delimted word
e Move to the end of the word
E Move to the end of Blank delimited word
( Move a sentence back
) Move a sentence forward
{ Move a paragraph back
} Move a paragraph forward
0 Move to the begining of the line
$ Move to the end of the line
1G Move to the first line of the file
G Move to the last line of the file
nG Move to nth line of the file
:n Move to nth line of the file
fc Move forward to c
Fc Move back to c
H Move to top of screen
M Move to middle of screen
L Move to botton of screen
% Move to associated ( ), { }, [ ]

Windows平台，不能用记事本打开有汉字的文本，否则乱码
