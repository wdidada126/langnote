# java log



[Java中的日志](https://blog.csdn.net/luoweifu/article/details/46495045)


Java Logging API提供了七个日志级别用来控制输出。这七个级别分别是：

级别
SEVERE-WARNING-INFO-CONFIG-FINE-FINER-FINEST
调用方法
severe()-warning()-info()-config()-fine()-finer()-finest()
含意 严重 警告 信息 配置 良好 较好 最好


java log

日志实现

System.out

log4j apache顶级项目 定义了Logger、Appender、Level等概念
Slf4j 也是现在主流的日志门面框架
jul门面

slf4j默认日志实现类logback

https://blog.csdn.net/xiaoao20080/article/details/91285284

logback 日志实现

log4j
log4j2