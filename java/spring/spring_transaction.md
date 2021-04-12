# spring transaction

[spring transaction](https://www.jianshu.com/p/9158c745802b)

spring-transaction-practice https://gitee.com/edidada/spring-transaction-practice

spring-transaction-demo          https://github.com/edidada/spring-transaction-demo.git


两个项目


spring transaction
#  <tx 注解 解析

org.springframework.jdbc.datasource.DataSourceTransactionManager

<tx:annotation-driven transaction-manager="txManager" proxy-target-class="true"/>    

    @Transactional(propagation=Propagation.REQUIRED , isolation = Isolation.DEFAULT)

