# spring log


spring core
exclude
common-logging

引入jcl-slf4j jar


原理 
jcl-slf4j jar包含common-logging 这个jar中的接口
Spring-core中引用Log LoggerFactory由jcl-slf4j jar 提供
因此运行的时候不会报错

https://www.martinfowler.com/articles/injection.html


SpringExample github项目
4.3.12.RELEASE.BUILD

core依赖

    <dependency>
      <groupId>commons-logging</groupId>
      <artifactId>commons-logging</artifactId>
      <version>1.2</version>
      <scope>compile</scope>
    </dependency>


commons-logging可以直接依赖log4j


