# springboot_mybatis


https://gitee.com/edidada/springbootmybatis

```xml
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>2.1.4</version>
        </dependency>
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-autoconfigure</artifactId>
            <version>2.1.4</version>
        </dependency>
```

### mybatis-spring-boot-starter

没有任何类
引用 mybatis-spring-boot-autoconfigure

### mybatis-spring-boot-autoconfigure





| org.mybatis.spring.boot.autoconfigure                        |           |                             |
| ------------------------------------------------------------ | --------- | --------------------------- |
| ConfigurationCustomizer                                      | interface |                             |
| MybatisAutoConfiguration                                     |           | implements InitializingBean |
| MybatisAutoConfiguration.AutoConfiguredMapperScannerRegistrar |           |                             |
| MybatisAutoConfiguration.MapperScannerRegistrarNotFoundConfiguration |           |                             |
| MybatisLanguageDriverAutoConfiguration                       |           |                             |
| MybatisLanguageDriverAutoConfiguration.FreeMarkerConfiguration |           |                             |
| MybatisLanguageDriverAutoConfiguration.LegacyFreeMarkerConfiguration |           |                             |
| MybatisLanguageDriverAutoConfiguration.LegacyVelocityConfiguration |           |                             |
| MybatisLanguageDriverAutoConfiguration.ThymeleafConfiguration |           |                             |
| MybatisLanguageDriverAutoConfiguration.ThymeleafConfiguration.MetadataThymeleafLanguageDriverConfig |           |                             |
| MybatisLanguageDriverAutoConfiguration.VelocityConfiguration |           |                             |
| MybatisProperties                                            | property  |                             |
| SpringBootVFS                                                |           |                             |


MybatisLanguageDriverAutoConfiguration 作用
MybatisLanguageDriverAutoConfiguration 是 MyBatis-Spring-Boot-Starter 自动配置的一部分，用于自动配置 MyBatis 的自定义语言驱动（Language Driver）。

在 MyBatis 中，语言驱动是用于解析 MyBatis Mapper 文件中的动态 SQL 语句的组件。默认情况下，MyBatis 支持的语言驱动有 XMLLanguageDriver 和 AnnotationLanguageDriver 两种，分别用于解析 XML 和注解方式编写的动态 SQL 语句。除此之外，MyBatis 还允许开发者自定义语言驱动，以支持更多的动态 SQL 语法。

MybatisLanguageDriverAutoConfiguration 就是用于自动配置 MyBatis 的自定义语言驱动的。在启用了该自动配置之后，如果项目中存在自定义的语言驱动类（实现了 org.apache.ibatis.scripting.LanguageDriver 接口），那么 MybatisLanguageDriverAutoConfiguration 就会自动将其加入到 MyBatis 的语言驱动列表中，从而使得 MyBatis 可以支持该自定义语言驱动。

需要注意的是，如果你要使用自定义的语言驱动，除了将其实现的类加入到项目的类路径中之外，还需要在 MyBatis 的 Mapper 文件中将其配置为使用该自定义语言驱动，例如：

```xml
<mapper namespace="com.example.mapper.UserMapper">
    <select id="findUsers" resultType="User">
        <!-- 使用自定义语言驱动解析动态 SQL 语句 -->
        <script language="com.example.mybatis.CustomLanguageDriver">
            SELECT * FROM users WHERE 1=1
            <if test="name != null">
                AND name = #{name}
            </if>
            <if test="age != null">
                AND age = #{age}
            </if>
        </script>
    </select>
</mapper>
```

在上面的示例中，我们使用了自定义的语言驱动 `com.example.mybatis.CustomLanguageDriver` 来解析动态 SQL 语句。需要注意的是，使用自定义语言驱动时，需要将 `language` 属性设置为自定义语言驱动的类全名。