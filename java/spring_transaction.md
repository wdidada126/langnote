# spring_transaction

spring transaction xml配置

1 配置事务管理器和数据源：
<!-- 配置数据源 -->
<bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
    <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
    <property name="url" value="jdbc:mysql://localhost:3306/test"/>
    <property name="username" value="root"/>
    <property name="password" value="root"/>
</bean>

<!-- 配置事务管理器 -->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <property name="dataSource" ref="dataSource"/>
</bean>

2 配置事务切面：
<!-- 配置事务切面 -->
<tx:advice id="txAdvice" transaction-manager="transactionManager">
    <tx:attributes>
        <!-- 配置事务的传播行为和隔离级别 -->
        <tx:method name="insert*" propagation="REQUIRED" isolation="DEFAULT"/>
        <tx:method name="update*" propagation="REQUIRED" isolation="DEFAULT"/>
        <tx:method name="delete*" propagation="REQUIRED" isolation="DEFAULT"/>
        <tx:method name="get*" read-only="true"/>
    </tx:attributes>
</tx:advice>

<aop:config>
    <aop:pointcut id="servicePointcut" expression="execution(* com.example.service.*.*(..))"/>
    <aop:advisor advice-ref="txAdvice" pointcut-ref="servicePointcut"/>
</aop:config>
3 在 Service 实现类中使用事务：
<bean id="userService" class="com.example.service.impl.UserServiceImpl">
    <property name="userDao" ref="userDao"/>
</bean>

<bean id="userDao" class="com.example.dao.impl.UserDaoImpl">
    <property name="dataSource" ref="dataSource"/>
</bean>



<!-- 使用声明式事务，引入 tx 命名空间 -->
<tx:annotation-driven transaction-manager="transactionManager"/>

<!-- Service 实现类中使用 @Transactional 注解开启事务 -->
<bean id="userService" class="com.example.service.impl.UserServiceImpl">
    <property name="userDao" ref="userDao"/>
</bean>

<bean id="userDao" class="com.example.dao.impl.UserDaoImpl">
    <property name="dataSource" ref="dataSource"/>
</bean>


其中，transactionManager 是事务管理器，txAdvice 是事务切面，tx:attributes 配置了事务的传播行为和隔离级别，servicePointcut 是切入点，userService 和 userDao 是 Service 和 DAO 实现类的 bean 定义，@Transactional 是开启事务的注解。




spring transaction注解声明式

在Spring中使用注解声明式事务可以通过@Transactional注解实现。可以将该注解添加到需要添加事务的方法上或类上，Spring将根据注解的信息自动为其创建代理对象，从而提供声明式事务管理。

使用@Transactional注解需要在Spring配置文件中开启事务管理器，例如：

<!-- 开启注解驱动的事务管理器 -->
<tx:annotation-driven transaction-manager="transactionManager"/>
 
<!-- 配置事务管理器 -->
<bean id="transactionManager"
      class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <property name="dataSource" ref="dataSource"/>
</bean>
然后在需要添加事务的方法上添加@Transactional注解，例如：

@Transactional
public void save(User user) {
    userDao.save(user);
}
这样，当调用save方法时，Spring将会在方法执行前创建一个新的事务，在方法执行完成后根据方法执行结果进行提交或回滚。通过这种方式，我们就可以方便地使用注解来声明式管理事务。
