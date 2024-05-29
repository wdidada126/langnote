# jvm

https://codeahoy.com/2017/08/06/basics-of-java-garbage-collection/

JVM 之 ParNew 和 CMS 日志分析

常用的两种垃圾收集器（ParNew：年轻代，CMS：老年代）

ParNew只能用于年轻代？

CMS：老年代

https://matt33.com/2018/07/28/jvm-cms/

https://www.oracle.com/java/technologies/javase/vmoptions-jsp.html

jvm启动参数大全

https://www.cnblogs.com/jpfss/p/12237079.html

java启动参数共分为三类；
其一是标准参数（-），所有的JVM实现都必须实现这些参数的功能，而且向后兼容；
其二是非标准参数（-X），默认jvm实现这些参数的功能，但是并不保证所有jvm实现都满足，且不保证向后兼容；
其三是非Stable参数（-XX），此类参数各个jvm实现会有所不同，将来可能会随时取消，需要慎重使用；

https://www.jianshu.com/p/bb6b91f2fb29

http://xstarcd.github.io/wiki/Java/JVM_GC.html