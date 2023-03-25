# mybatis


idea插件 mybatisprohelper

mybatis，如何生成sql


https://blog.csdn.net/goligu/article/details/124878614

org.apache.ibatis.scripting.xmltags.XMLScriptBuilder#parseDynamicTags

public class XMLScriptBuilder extends BaseBuilder


TypeAliasRegistry
TypeHandlerRegistry

[Java、Mysql、MyBatis 中枚举 enum 的使用](https://blog.csdn.net/JoeBlackzqq/article/details/90216582)


D:\git\github\LangNote\java\mybatis.md



MyBatis

依赖mysql-connector-java这个jar
jdbc
连接池

接口
xml
SqlSessionFactory等核心类



MyBatis xml
1、if
2、choose、when、otherwise
3、trim、where、set
4、foreach
bind

MyBatis动态SQL

https://mybatis.org/mybatis-3/zh/dynamic-sql.html

script
https://blog.csdn.net/qq_32588349/article/details/51541871
https://blog.csdn.net/a18716374124/article/details/79638980

Jdbctemplate如何写动态sql

Restful HTTP 路径

### 面试题

mybatis批量插入数据有哪几种方式，有什么异同
1、mybatis xml文件中拼接xml

创建 UserMapper.xml 文件，使用 foreach 标签拼接 SQL，具体实现代码如下：

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.demo.mapper.UserMapper">
    <insert id="saveBatchByNative">
        INSERT INTO `USER`(`NAME`,`PASSWORD`) VALUES
        <foreach collection="list" separator="," item="item">
            (#{item.name},#{item.password})
        </foreach>
    </insert>
</mapper>

https://zhuanlan.zhihu.com/p/35305211


mybatis ExecutorType.BATCHMybatis内置的ExecutorType有3种，默认的是simple，该模式下它为每个语句的执行创建一个新的预处理语句，单条提交sql；而batch模式重复使用已经预处理的语句，并且批量执行所有更新语句，显然batch性能将更优； 但batch模式也有自己的问题，比如在Insert操作时，在事务没有提交之前，是没有办法获取到自增的id，这在某型情形下是不符合业务要求的具体用法如下:*方式一 spring+mybatis 的//获取sqlsession
//从spring注入原有的sqlSessionTemplate
@Autowired
private SqlSessionTemplate sqlSessionTemplate;
// 新获取一个模式为BATCH，自动提交为false的session
// 如果自动提交设置为true,将无法控制提交的条数，改为最后统一提交，可能导致内存溢出

```java
SqlSession session = sqlSessionTemplate.getSqlSessionFactory().openSession(ExecutorType.BATCH,false);
//通过新的session获取mapper
fooMapper = session.getMapper(FooMapper.class);
int size = 10000;
try{
for(int i = 0; i < size; i++) {
Foo foo = new Foo();
foo.setName(String.valueOf(System.currentTimeMillis()));
fooMapper.insert(foo);
if(i % 1000 == 0 || i == size - 1) {
//手动每1000个一提交，提交后无法回滚 
session.commit();
//清理缓存，防止溢出
session.clearCache();
}
}
} catch (Exception e) {
//没有提交的数据可以回滚
session.rollback();
} finally{
session.close();
}

```


spring+mybatis
方法二:结合通用mapper sql别名最好是包名＋类名public void insertBatch(Map<String,Object> paramMap, List<User> list) throws Exception {
// 新获取一个模式为BATCH，自动提交为false的session
// 如果自动提交设置为true,将无法控制提交的条数，改为最后统一提交，可能导致内存溢出

```java
SqlSession session = sqlSessionTemplate.getSqlSessionFactory().openSession(ExecutorType.BATCH, false);
try {
if(null != list || list.size()>0){
int lsize=list.size();
for (int i = 0, n=list.size(); i < n; i++) {
User user= list.get(i);
user.setIndate((String)paramMap.get("indate"));
user.setDatadate((String)paramMap.get("dataDate"));//数据归属时间
//session.insert("com.xx.mapper.UserMapper.insert",user);
//session.update("com.xx.mapper.UserMapper.updateByPrimaryKeySelective",_entity);
session.insert(“包名+类名", user);
if ((i>0 && i % 1000 == 0) || i == lsize - 1) {
// 手动每1000个一提交，提交后无法回滚
session.commit();
// 清理缓存，防止溢出
session.clearCache();
}
}
}
} catch (Exception e) {
// 没有提交的数据可以回滚
session.rollback();
e.printStackTrace();
} finally {
session.close();
}
}
```

### MyBatis四大组件之Executor执行器

每一个SqlSession都会拥有一个Executor对象，这个对象负责增删改查的具体操作，我们可以简单的将它理解为 JDBC中Statement 的封装版。
https://zhuanlan.zhihu.com/p/80497754

public enum ExecutorType {
  SIMPLE, REUSE, BATCH
}

