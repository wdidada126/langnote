# spring_aop_cglib



cglib不支持java17，不更新了，推荐使用

https://bytebuddy.net/#/



Spring的两种动态代理：Jdk和Cglib 的区别和实现

jdk只代理接口，cglib代理类

https://www.cnblogs.com/leifei/p/8263448.html

如何强制使用CGLIB实现AOP？
 （1）添加CGLIB库，SPRING_HOME/cglib/*.jar
 （2）在spring配置文件中加入<aop:aspectj-autoproxy proxy-target-class="true"/>		


https://www.cnblogs.com/coderxiaohei/p/11758239.html
总结
Spring 5.x中AOP默认依旧使用JDK动态代理。
SpringBoot 2.x开始，为了解决使用JDK动态代理可能导致的类型转化异常而默认使用CGLIB。
在SpringBoot 2.x中，如果需要默认使用JDK动态代理可以通过配置项spring.aop.proxy-target-class=false来进行修改，proxyTargetClass配置已无效。

