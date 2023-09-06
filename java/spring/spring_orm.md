# spring orm

## spring orm 跟spring oxm的区别
Spring ORM和Spring OXM是两个不同的模块,它们的区别如下:

1. 功能差异
- Spring ORM:用于实现对象关系映射,将Java对象映射到数据库表, simplifies JDBC and JPA operations. 常用的实现包括JDBC,JPA,Hibernate等。
- Spring OXM:用于实现对象XML映射,将Java对象转换成XML表示,或将XML转换成Java对象。可以看作是ORM的XML版本。常用的实现包括JAXB, Castor, XMLBeans等。
2. 使用场景差异
- Spring ORM主要用于处理关系型数据库,将对象持久化到RDBMS中。
- Spring OXM主要用于处理XML数据,在系统间交换对象时将对象实例转换成XML(或反向)。 
3. 典型应用差异
- Spring ORM用在需要将Java对象保存到数据库的时候,如Spring JPA。 
- Spring OXM用在需要生成或解析XML时,如与WebService交互转换对象。
总结:
Spring ORM处理对象关系映射,Spring OXM处理对象XML映射。
两者针对不同的应用场景,ORM擅长数据库映射,OXM擅长XML转换。


org.springframework.orm.hibernate5

org.springframework.orm.jpa
这两个包

org.springframework.orm.hibernate5.HibernateTransactionManager
这个类

## api doc
https://docs.spring.io/spring-framework/docs/5.2.x/javadoc-api/


org.springframework.orm	
Root package for Spring's O/R Mapping integration classes.


org.springframework.orm.hibernate5	
Package providing integration of Hibernate 5.x with Spring concepts.

org.springframework.orm.hibernate5.support	
Classes supporting the org.springframework.orm.hibernate5 package.

org.springframework.orm.jpa	
Package providing integration of JPA (Java Persistence API) with Spring concepts.


org.springframework.orm.jpa.persistenceunit	
Internal support for managing JPA persistence units.

org.springframework.orm.jpa.support	
Classes supporting the org.springframework.orm.jpa package.


org.springframework.orm.jpa.vendor	
Support classes for adapting to specific JPA vendors.
