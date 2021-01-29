# MyBatis Generator

java bean类
有了
WithId（）方法 能否去掉

The content of element type "context" must match "(property*,plugin*,commentGenerator?,(connectionFactory|jdbcConnection),javaTypeResolver?,javaModelGenerator,sqlMapGenerator?,javaClientGenerator?,table+)".


mbg生成的sql select的Query类
Criteria
n. 标准，条件（criterion的复数）

tablename-Query

public static class Criteria extends GeneratedCriteria

protected abstract static class GeneratedCriteria


String orderByClause
boolean distinct
List<Criteria> oredCriteria


[MyBatis Generator 使用 详解 java命令行的方式](https://blog.csdn.net/chenshun123/article/details/73501804)

[mybatis generator quickstart](http://www.mybatis.org/generator/quickstart.html)

java -jar E:/mavenrepository_testgit/mysql/mysql-connector-java/5.1.6/mysql-connector-java-5.1.6.jar
 -configfile generator.xml -overwrite

java -jar D:/mybatis-generator-core-1.3.7/lib/mybatis-generator-core-1.3.7.jar -configfile generator.xml -overwrite

如何运行MyBatis Generator

有以下四种运行方式：

1、从 命令提示符 使用 XML 配置文件
2、作为 Ant 任务 使用 XML 配置文件
3、作为 Maven Plugin
4、从另一个 Java 程序 使用 XML 配置文件
个人比较推荐作为maven插件运行，方便集成，部署


从 命令提示符 使用 XML 配置文件
使用步骤：


下载jar
配置xml文件 数据库url 用户名 密码

运行java 。。。
生成xml java interface文件

