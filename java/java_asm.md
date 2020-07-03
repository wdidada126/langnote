# asm



hsdis

jdk里面有

jdk-jdk-13+16/src/utils/hsdis





查看Java的汇编指令

Java本身提供这个支持，使用hsdis

https://www.jianshu.com/p/93821b08e774



最近想学习下Hotspot的JIT，查找大量资料都说需要hsdis，但是又从哪都找不到windows64位的版本。
如果没有这个东西，直接运行代码，加上如下参数后
-XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly
会得到如下提示
Java HotSpot(TM) 64-Bit Server VM warning: PrintAssembly is enabled; turning on DebugNonSafepoints to gain additional output Could not load hsdis-amd64.dll; library not loadable; PrintAssembly is disabled

https://blog.csdn.net/yizishou/article/details/53423409