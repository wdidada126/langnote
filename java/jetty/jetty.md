# jetty

[Jetty的配置说明](https://www.cnblogs.com/duanxz/p/3143374.html)


jetty服务器部署
jetty本身是java写的，有log4j相关的jar包
引入Spring框架，也有相关日志jar包
现在强制使用log4j2，多个日志相关jar包冲突，会选择哪个？

Jetty 输出到Consule的日志，就输出到Jetty上
Tomcat是不是也这样

https://github.com/eclipse/jetty.project


Jetty修改默认端口
8
9

‘-Djetty.port=8122’



jetty.sh start

```
java -jar jetty-distribution-9.4.28.v20200408/start.jar
```

https://www.cnblogs.com/pangxiansheng/p/5362813.html

https://blog.csdn.net/acm_lkl/article/details/78681659

https://blog.csdn.net/ywb201314/article/details/62424998/