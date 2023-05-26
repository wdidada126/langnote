spring_el

这里给出spring EL表达式的一些使用示例:

1. 引用bean: #{beanName}

```xml
<property name="someProperty">
    <ref bean="#{dataSource}" />  
</property>
```

2. 调用bean的方法: #{beanName.methodName()}

```xml
<property name="someProperty" value="#{dataSource.getConnection()}" />
```

3. 算术运算:

```xml
<property name="someInt" value="#{ 10 * 2}" />
```

4. 字符串连接:

```xml 
<property name="someStr" value="#{'Hello ' + 'World'}"/>
```

5. 判断:

```xml
<property name="online" value="#{ true}" />  
```

6. 引用配置值:

```xml
<property name="url" value="#{systemProperties['jdbc.url']}" />
```

7. 函数调用:

```xml
<property name="time" value="#{ T(java.lang.System).currentTimeMillis() }" />
```

8. 条件表达式:

```xml
<property name="#{activeProfile == 'dev' ? 'devConfig' : 'prodConfig' }" />
```

9. 调用静态方法:

```xml 
<property name="time" value= "#{ T(java.util.Calendar).getInstance().getTime().getTime()}"/>
```

希望以上示例给您提供参考! 如果还有其他任何问题,欢迎随时和我交流。