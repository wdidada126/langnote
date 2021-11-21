# ldap

LDAP概念和原理介绍

https://www.ietf.org/rfc/rfc2251.txt
https://www.cnblogs.com/wilburxu/p/9174353.html

LDAP是一种通讯协议
https://www.jianshu.com/p/7e4d99f6baaf

适合读多写少场景



jldap

https://www.openldap.org/jldap/





<dependency>
    <groupId>com.novell.ldap</groupId>
    <artifactId>jldap</artifactId>
    <version>4.3</version>
</dependency>





OpenLDAP是轻型目录访问协议（Lightweight Directory Access Protocol，LDAP）的自由和开源的实现，在其OpenLDAP许可证下发行，并已经被包含在众多流行的Linux发行版中。
它主要包括下述4个部分：
slapd - 独立LDAP守护服务
slurpd - 独立的LDAP更新复制守护服务
实现LDAP协议的库
工具软件和示例客户端



brew install openldap

yum install openldap



mac系统自带openldap

https://blog.csdn.net/JustDI0209/article/details/74910295



https://blog.csdn.net/vivianliulu/article/details/90640737