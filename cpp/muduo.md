# muduo


知乎网友评价muduo

当然差，虽然使用了一些c++的新东西，如function取代虚函数之外，其实不如ace，因为设计有问题，随便说说吧
比如用户无法感知队头阻塞（收发窗口）而可能会导致爆内存，所以有一定使用场景限制；
比如复制用户数据到库内部，比如使用LT而不是ET（这个不算什么大问题，只是使用ET较为主流）；
比如多线程模型设计很糟糕（优秀的参考asio的io_contex，可轻松使用不同多线程模型，如以下组合：multithreads/contex, onethread/contex, mutlithreads/multicontex）；
比如使用reactor模型也是一个败笔，很难转换成现代协程模型。
代码水平写的也一般吧，不是很规范较为随意，好代码会像混然天成一样，风格错落有致，极为规范，国外那些优秀的开源项目基本都如此，差的很少。



有tag

ubuntu 20有编译

cmake组织
依赖boost probobuf

https://www.zhihu.com/question/24590359/answer/34834484

补充说明一下我对那位水木网友的看法的看法，我认为他关于 timer 的批判是站得住脚的---如果他说的属实的话，关于 signal 的看法有待商榷，实屏蔽大部分 signal（只留一个做启停）是实践上很实用的做法，一般也不特别需要网络框架去处理。
-------------------------------这是那位水木网友的文章：  hurricanelee (风的影子) 于  (Tue Sep 25 13:57:06 2012)  提到:muduo适用于什么环境？muduo的官方一句话自我介绍是：A C++ non-blocking multi-threaded networklibrary for Linux。在其readme和wiki中均未提及此lib是否适用于实际场景，于是我花了些时间翻看了一下，得出的结论是此lib仅限于展示epoll/poll的基本用法，对网络编程初学者是否有参考价值还有待进一步考察。任何一个网络产品除了要支持网络event之外，还必须处理另外两种事件：signal和timer。muduo也毫无例外。但近看一下就发现muduo对single和timer的支持很有喜感。除了SIGPIPE被mask之外，muduo没有接管signal。当然muduo这么做是有借口的，反正有signalfd嘛。在此我想问问各位做网络应用的同学，在你的实际项目中，不用POSIX的signal接口而用signalfd的，有几个？而如果是从编程初学者教育的角度来看，是介绍POSIX重要，还是介绍2.6.22引入的一个new feature重要？而抛弃signal的处理之后，muduo自然轻松了许多，还顺带可以说一句：muduo支持高级特性signalfd。--嗯，听起来很高级，不过signalfd不是muduo支持的，而是kernel支持的。一个网络编程库，timer是重中之重，比到底是用epoll还是select都重要。当然，话说回来，再吊的库无非也就是个heap为本的数据结构在支持，无非是有些库喜欢说自己的heap实现比别人都高效，比如haproxy。但muduo却独辟蹊径，用timerfd，泥玛又是一个高级特性啊，很唬人的。由kernel帮你管理timer，是不是很吊。不仅采用了timerfd，muduo还采用了set来保存event，每个big loop里要查超时的时候，再iterate一遍这个set。再然后，每次加一个timer，就要冒着一次settime的syscall的风险--这还不够，还得要一次gettimeofday。别不把syscall当不要钱的可以吗？你也许可以跑10万个连接，但你敢加上超时的特性吗？muduo如果有做过细致的benchmark就会知道，一个loop里最花时间的就是timer的处理。关于muduo的timer处理，槽点太多，我就不一一细述了。回头看看timer，很显然不适合工业应用，而给初学者做参考。嗯，负面参考价值很大。嗯，今天先说这么多吧。吐槽点还很多，比如那个全功能的http范例，比如对pthread/fork的支持，比如对内存的使用等等等等。都要一一吐过也不是不可以，不过就要耐下性子来慢慢写就是。

别的不多说，gettimeofday在64位linux上不是系统调用了
在 x86-64 平台上,gettimeofday 不是系统调用,而是在用户态实现的(搜
vsyscall),没有上下文切换和陷入内核的开销。
喷 signalfd 和 timerfd 站不住脚，内核提供新的接口显然是让人用的。如果内核比较老或者不用 linux，那大可不必使用 muduo。就像写 win10 的应用程序不必兼容 xp 一样。

1、std::set内部使用的红黑树
2、至于用不用timerfd，引用下stackoverflow上的回答：
When you use timerfd, it takes 3 system calls (timerfd_create(), timerfd_settime() and epoll_ctl()) just to create a timer.
And every time it expires you need to read() from that file descriptor.
timerfd could be useful for applications without an event loop, but for ones that already use a decent event loop it is pretty much useless.

看到timer比epoll或者select更重要我就不想往下看了

自己项目用timerfd还是很爽的，但是作为通用库，兼容性也是非常重要的。
libuv的timer也是红黑树实现，不过只是在windows上，Linux下还是最小堆
可试试corelooper，没有这些问题
大哥人家timer的做法有什么不对的吗？nginx也是用set管理timer的，你黑别人之前也要了解一下好吗？
nginx 又不是天王老子，nginx 做得就一定是对的？你只要手工管理过超时器，一定知道为什么有必要用优先队列或者最小堆。而且这又不是我说的，而且我也不能确定你关于 nginx 的说法对不对。

## muduo依赖
boost
protoc

## muduo安装
https://github.com/chenshuo/muduo

```shell

git clone https://github.com/chenshuo/muduo.git
sudo update
sudo apt install libboost-all-dev -y
sudo apt install protobuf-compiler -y
export Boost_INCLUDE_DIR=/usr/include
cd muduo
chmod +x ./build.sh
./build.sh
```