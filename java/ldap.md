# ldap

LDAP概念和原理介绍

LDAP服务器软件包括OpenLDAP和Microsoft Active Directory

LDAP（Lightweight Directory Access Protocol）是一种用于访问和维护分布式目录信息服务的应用层协议。LDAP通常用于在网络中共享目录信息，例如用户身份验证、访问控制、地址簿服务等。下面是LDAP的一些基本概念和原理介绍：

1. 目录服务：LDAP是用于访问目录服务的协议。目录服务是一种分层存储和组织信息的系统，类似于数据库，但通常更专注于提供快速读取和搜索的能力。
2. 目录树：LDAP使用目录树来组织信息。目录树类似于文件系统中的树结构，由一系列条目（entry）组成，每个条目都有一个唯一的标识符（DN，Distinguished Name）。
3. 条目和属性：LDAP目录树中的每个节点都是一个条目，每个条目可以包含一个或多个属性-值对。例如，一个用户条目可能包含属性如姓名、电子邮件地址、电话号码等。
4. LDAP服务器：LDAP服务器是提供LDAP服务的软件，负责存储和管理目录信息，并响应LDAP客户端的请求。常见的LDAP服务器软件包括OpenLDAP和Microsoft Active Directory。
5. LDAP客户端：LDAP客户端是通过LDAP协议与LDAP服务器通信的应用程序或工具。LDAP客户端可以执行各种操作，如搜索、添加、修改和删除条目等。
6. LDAP协议：LDAP协议定义了客户端和服务器之间进行通信的规则和格式。它基于TCP/IP协议栈，通常在389端口上运行。
7. LDAP基于文本的协议：LDAP通信基于文本，使用类似于XML的格式（称为LDIF，LDAP Data Interchange Format）来表示数据。这种文本格式使得LDAP通信相对轻量和易于解析。
8. 认证和授权：LDAP常用于认证和授权用户访问网络资源。通过LDAP，可以验证用户的身份，并根据其在目录中的属性配置访问权限。

总体来说，LDAP提供了一种标准化的方式来管理和访问分布式目录信息，使得在网络环境中共享和利用这些信息变得更加简单和高效。

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

https://github.com/openldap/openldap

https://www.openldap.org/devel/contributing.html

brew install openldap

yum install openldap

mac系统自带openldap

https://blog.csdn.net/JustDI0209/article/details/74910295

https://blog.csdn.net/vivianliulu/article/details/90640737