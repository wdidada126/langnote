# jprofiler

yourkit

https://www.ej-technologies.com/download/jprofiler/files 支持mac

https://www.jb51.net/softs/608640.html

https://www.jb51.net/softs/609957.html#downintro2

类对象数量

A1.分析的数据主要来自于下面俩部分
1. 一部分来自于jvm的分析接口JVMTI(JVM Tool Interface) , JDK必须>=1.6
例如: 对象的生命周期，thread的生命周期等信息


A2. 数据收集的原理如图2
1. 用户在JProfiler GUI中下达监控的指令(一般就是点击某个按钮)
2. JProfiler GUI JVM 通过socket(默认端口8849)，发送指令给被分析的jvm中的JProfile Agent。
3. JProfiler Agent(如果不清楚Agent请看文章第三部分"启动模式") 收到指令后，将该指令转换成相关需要监听的事件或者指令,来注册到JVMTI上或者直接让JVMTI去执行某功能(例如dump jvm内存)
4. JVMTI 根据注册的事件，来收集当前jvm的相关信息。 例如: 线程的生命周期; jvm的生命周期;classes的生命周期;对象实例的生命周期;堆内存的实时信息等等
5. JProfiler Agent将采集好的信息保存到内存中，按照一定规则统计好(如果发送所有数据JProfiler GUI，会对被分析的应用网络产生比较大的影响)
6. 返回给JProfiler GUI Socket.
7. JProfiler GUI Socket 将收到的信息返回 JProfiler GUI Render
8. JProfiler GUI Render 渲染成最终的展示效果


https://www.cnblogs.com/jpfss/p/8488111.html


http://www.32r.com/soft/73878.html

JProfiler.11.1.4.zip


2020 年的数据显示， 24% 的用户使用 VisualVM ，其他用户使用 JProfiler、Java Mission Control、NetBeans profiler 和 YourKit。数据来自所有使用Java作为主要语言的开发者。