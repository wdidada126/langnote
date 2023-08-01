# Ribbon

G:\code_repos\ribbon>

https://github.com/Netflix/ribbon

```xml
           <exclusions>
                <exclusion>
                    <artifactId>guava</artifactId>
                    <groupId>com.google.guava</groupId>
                </exclusion>
                <exclusion>
                    <artifactId>archaius-core</artifactId>
                    <groupId>com.netflix.archaius</groupId>
                </exclusion>
                <exclusion>
                    <artifactId>jackson-annotations</artifactId>
                    <groupId>com.fasterxml.jackson.core</groupId>
                </exclusion>
                <exclusion>
                    <artifactId>rxjava</artifactId>
                    <groupId>io.reactivex</groupId>
                </exclusion>
                <exclusion>
                    <artifactId>servo-core</artifactId>
                    <groupId>com.netflix.servo</groupId>
                </exclusion>
                <exclusion>
                    <artifactId>slf4j-api</artifactId>
                    <groupId>org.slf4j</groupId>
                </exclusion>
            </exclusions>
```

spring starter ribbon源码核心类分析
https://blog.csdn.net/catoop/article/details/109668616

#### spring cloud ribbon

```xml
    <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-starter-netflix-ribbon</artifactId>
      <version>2.2.6.RELEASE</version>
    </dependency>
```

### jar包列表
- ribbon
- ribbon-core
- ribbon-httpclient

## 源码分包详解
### ribbon