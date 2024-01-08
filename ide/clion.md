# Clion

### 插件



2021版本支持make
https://blog.csdn.net/qiuyeyijian/article/details/109267543

Windows 只支持Makefile，makefile

https://www.jetbrains.com/help/clion/makefiles-support.html
选中makefile
gnumakefile
右键

clean一下

cmake

[CLion开发编译调试Makefile项目](https://blog.csdn.net/lylwo317/article/details/86673912)


Clion支持makefile



ThoughtWorks
如何评价 TAPIR 分布式事务协议

论文地址：[http://syslab.cs.washington.edu/papers/tapir-tr14.pdf](http://syslab.cs.washington.edu/papers/tapir-tr14.pdf)
通过区分 inconsistent 和 consensus 两种操作来放宽对事务中操作顺序的要求，另外通过一个 sync 过程来同步各副本间的记录。似乎有很多的限制条件，有很多 corner case 需要考虑。

有没有哪个已知生产系统使用了这个协议？





https://www.youtube.com/watch?v=yE3eMxYJDiE

我个人是这么理解的, 没 leader 的强一致复制协议(如经典 Paxos)是不保证多少次 RTT 才能达成一致的, 好巧, 分布式事务也是不保证的. 那么无穷大 + 无穷大还是等于无穷大.

那么就干脆别搞强一致了, client 直接广播请求到那个 shard 下所有 replicas, 让分布式事务层辛苦点可能要多重试几次. 确定性的收益是最优情况下, RTT 从 2 降低到了 1, 最差情况反正是无穷大, 不差再多几个 RTT.

没想得很明白的是 abort 要怎么做, 总感觉哪里有问题. 求教



https://www.zhihu.com/question/56763641/answer/1016947765






ThoughtWorks


### 快捷键
双击两次shift

搜索queue

https://gitee.com/edidada/clh-queue


https://icode.best/i/42074744400777

1. 最常用的技巧：全局搜索。
按住shift 二次即可。同时，也可以使用正则表达式





