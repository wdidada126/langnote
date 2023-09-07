# fastjson

相信大家都用过 fastjson，初次接触 fastjson 肯定会被它简单的 API 所吸引，常用的序列化/反序列化统统一行代码搞定，比如 JSON.toJSONString()。通常来说，这种通过静态方法暴露的 API，其背后的设计与实现都是线程安全的，也就是在多线程环境中，你可以安心的使用 fastjson 的静态方法进行序列化和反序列化
    
https://github.com/alibaba/fastjson/

[test java demo testfastjson](https://github.com/edidada/testfastjson)	

JSON

JSONObject.toJSONString()



com.alibaba.fastjson.JSON
com.alibaba.fastjson.JSON.toJSONString(java.lang.Object)
com.alibaba.fastjson.JSON.parseObject(java.lang.String, com.alibaba.fastjson.TypeReference<T>, com.alibaba.fastjson.parser.Feature...)
com.alibaba.fastjson.TypeReference


public class JSONObject extends JSON



Fastjson的SerializerFeature序列化属性：
QuoteFieldNames———-输出key时是否使用双引号,默认为true
WriteMapNullValue——–是否输出值为null的字段,默认为false
WriteNullNumberAsZero—-数值字段如果为null,输出为0,而非null
WriteNullListAsEmpty—–List字段如果为null,输出为[],而非null
WriteNullStringAsEmpty—字符类型字段如果为null,输出为”“,而非null
WriteNullBooleanAsFalse–Boolean字段如果为null,输出为false,而非null

https://blog.csdn.net/CSDN2497242041/article/details/102618226


### fastjson与springmvc整合

FastJsonHttpMessageConverter类全路径在fastjson-1.2.78.jar包中。

FastJsonHttpMessageConverter是FastJson库提供的一个用于在Spring MVC中将Java对象序列化为JSON格式的HttpMessageConverter实现。在Spring MVC中，它可以替代默认的Jackson库提供的MappingJackson2HttpMessageConverter，从而提供更快的序列化和反序列化性能。

如果你想在自己的项目中使用FastJsonHttpMessageConverter，你需要在你的构建工具（如Maven或Gradle）中添加fastjson依赖，例如：