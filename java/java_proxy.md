# java proxy


内网通，有破解版，无广告
rocket.chat啥的就已经是很成熟的替代品了

Httpd服务器使用场景
httpd部署python
Httpd c cpp?

Tomcat部署java

软件开发过程中遇到的问题，不能放过

阿里jvm大致思路，调优，直接用G1

之前就是喜欢看直播，看直播，视频太费时间了
左小龙，在微信群里面说，关闭微信去看书，方法，先看Java基础结构 集合类源码，再看并发类源码
看框架

我觉得吧，刷完leetcode再看源码会更好一点，lc可以学习一些算法和数据结构，源码中可能会遇到，看起来更容易一点。
数据库表设计 数据建模
B站视频

看不懂动态代理的，自己抄一个例子然后看生成的动态代理class文件。如果接口里有多个方法，动态代理最麻烦的地方就是对接口内方法的特殊处理比较困难。

动态代理class文件反编译以后你会发现，它继承了你给的接口，并且方法内部都是统一的 return (XXX)super.h.invoke(this, m4, new Object【】{var1});那个h就是你自己写的InvocationHandler实现类。
换句话说就是什么呢，你要自己在InvocationHandler实现类的invoke里判断进来的method是接口里的哪一个方法并执行具体流程。举个例子(伪代码)就是
        if (method等于方法A){
            特殊处理;
            method.invoke(subject, args);
            特殊处理;
             return xxx;       
        }
        if (method等于方法B){
            特殊处理;
            method.invoke(subject, args);
            特殊处理;
            return xxx;
        }

昨天晚上刚看到initxxxpostprossor往下的源码，判断接口还是类，决定哪个代理，今天就刷到你了，不过cglib的原理asm太难了，学过一点字节码，不如javassist操作简单，面试问我的话，我是卷不到底层了，只能答出动态代理的细节

InvocationHandler     Invocation 求助; 祈祷; 调用; 启用;
MyBatis

JDK本身提供了动态代理的实现，要求被代理者必须实现接口。
public static Object newProxyInstance(ClassLoader loader,
Class<?>[] interfaces,InvocationHandler h)
复制代码第一个参数为类加载器，第二个参数是被代理者实现的接口列表，第三个参数是实现了InvocationHandler接口的对象。


CGLIB动态代理
JDK动态代理要求必须有接口，CGLIB（Code Generate Library）动态代理没有这个要求，它是通过创建一个被代理类的子类，然后使用ASM字节码库修改代码来实现的。

