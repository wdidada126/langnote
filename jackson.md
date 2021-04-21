# jackson

json规范，需要读一下

Spring用
Jackson是一个 Java 的用来处理 JSON 格式数据的类库，性能非常好。


https://github.com/FasterXML/jackson-core/
http://wiki.fasterxml.com/JacksonDownload

### jar包
- jackson-annotations
- jackson-core
- jackson-databind


com.fasterxml.jackson.databind.ObjectMapper
ObjectMapper

readValue()
writeValueAsString()


https://github.com/FasterXML/jackson-core/

https://blog.csdn.net/qq_43872529/article/details/104176433


springmvccurl jackson



List
https://blog.csdn.net/qq_35872456/article/details/96295943

```java
    ObjectMapper mapper = new ObjectMapper();

    List<User> users = null;
    try {
        users = mapper.readValue(json, new TypeReference<List<User>>(){});
    }catch (IOException e){
        throw new RuntimeException(e);
    }
```


com.fasterxml.jackson.core.type.TypeReference
new TypeReference<List<User>>(){};

匿名内部类


public @ResponseBody String  fileUpload(@RequestParam("file") CommonsMultipartFile file) throws IOException



org.springframework.web.multipart.commons.CommonsMultipartFile

