# Ant

[Ant学习笔记（2） 在Eclipse中使用Ant](https://www.cnblogs.com/shijiaqi1066/p/3472982.html)

ant跟maven对比

maven有jar包仓库的概念

ant没有

ant对比make

## ubuntu 安装ant
sudo apt install ant -y


## ant编译zk老版本

ant compile_jute
Unable to locate tools.jar. Expected to find it in /usr/lib/jvm/java-8-openjdk-amd64/lib/tools.jar
Buildfile: /home/wdidada/zookeeper/build.xml

init:

jute:

BUILD FAILED
/home/wdidada/zookeeper/build.xml:240: Unable to find a javac compiler;
com.sun.tools.javac.Main is not on the classpath.
Perhaps JAVA_HOME does not point to the JDK.
It is currently set to "/usr/lib/jvm/java-8-openjdk-amd64/jre"

Total time: 0 seconds

## 下载安装ant
https://cloud.tencent.com/developer/article/1393883
 