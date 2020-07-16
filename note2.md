多关注同行啊



金蝶的技术架构要比用友强

Odoo是目前发展最快的、最好的开源ERP厂商，https://github.com/odoo/odoo

用友、金蝶、鼎捷软件三款ERP对比各有千秋 

http://blog.sina.com.cn/s/blog_4f045b390102e8af.html





redis实现的分布式锁why要设置过期时间

执行时间长，不能分段执行，锁续期

redis实现的分布式锁why要设置过期时间 原创

2020-06-28

成长小草 

码龄3年

关注

1.网络抖动

进程A中的一个线程获取到了锁，然后执行finally中的释放锁的代码时，由程序到Redis的网络不好了，所以释放锁失败。此时对于redis服务端来说，它可不知道客户端曾经试图释放过锁，它会一直把锁给A,如此一来，其他进程的线程再也不能获取到这个锁了。

如果用设置过期时间的方式，即使客户端和服务端的网络不通了，服务端依然在进行时间的计算，时间到了直接把锁释放掉，等网络通了，不影响获取锁。

2.服务端宕机

进程A获取到了锁，Redis服务器宕机了，所以锁没有释放。等到Redis再次恢复的时候，Redis服务端还会保持这这个锁给到A,就会锁死。

如果是设置了过期时间的话，服务器恢复后就会继续倒计时，时间到了服务器自动把锁释放。

说白了，分布式锁用的是第三方的东西，所以要在第三方设置，不能只在客户端保证所的释放。



关于数据库

Rdb

存的是结构化数据

Redis

string hash set zset 链表类型（list）

mingodb

json

Tikv



Dubbo加状态，如何处理，分布式一致性协议同步数据



java基础，spring，jvm，多线程并发，redis，dubbo，rocketmq，mysql，zk。

系统设计 DDD 互联网的

知乎live覃超

互联网金融系统如何设计



VerilogHDL和VHDL



Java中间件开发

MyBatis

ONGL DSL吗？

OGNL是**对象图导航语言**(Object-Graph Navigation Languaged)的缩写

https://blog.csdn.net/qq_36748278/article/details/78013232

SqlSessionFactoryBuilder

Configure

Envrionment

代理

字节码修改技术

Tomcat 涉及到双亲委派模型



node c++书籍

https://book.douban.com/subject/30247892/



