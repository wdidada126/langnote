# jackson

支持json和xml
springmvc默认的json序列化 反序列化工具

https://gitee.com/edidada/testjackson
http接口入参 出参 json格式的，用这个
日期参数，加上@JsonFormat @DateTimeFormat
注解@DateTimeFormat:主要是控制后台到前台的时间格式
注解@JsonFormat:主要是限制前台到后台的时间格式



json规范，需要读一下



[Jackson实现序列化和反序列化](https://blog.csdn.net/wus_shang/article/details/79286544)

Spring用
Jackson是一个 Java 的用来处理 JSON 格式数据的类库，性能非常好。


https://github.com/FasterXML/jackson-core/
http://wiki.fasterxml.com/JacksonDownload

### jar包
- jackson-annotations
- jackson-core
- jackson-databind

- jackson-dataformat-xml xml格式化的

```xml
<!--Jackson包-->
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-core</artifactId>
      <version>2.9.0</version>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.9.0</version>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-annotations</artifactId>
      <version>2.9.0</version>
    </dependency>
```


com.fasterxml.jackson.databind.ObjectMapper
ObjectMapper

readValue()
String writeValueAsString()               com.fasterxml.jackson.databind.ObjectMapper#writeValueAsString


ObjectMapper中的writeVaule和writeValueAsString方法之间的关系
https://blog.csdn.net/qq_43872529/article/details/104176433


springmvccurl jackson



List
https://blog.csdn.net/qq_35872456/article/details/96295943

```java
    ObjectMapper mapper = new ObjectMapper();

    List<User> users = null;
    try {
        users = mapper.readValue(json, new TypeReference<List<User>>(){});
        mapper.writeValueAsString(users);
    }catch (IOException e){
        throw new RuntimeException(e);
    }
```


com.fasterxml.jackson.core.type.TypeReference
new TypeReference<List<User>>(){};

匿名内部类


public @ResponseBody String  fileUpload(@RequestParam("file") CommonsMultipartFile file) throws IOException



org.springframework.web.multipart.commons.CommonsMultipartFile

