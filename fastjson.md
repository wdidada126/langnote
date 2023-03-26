# fastjson

https://github.com/alibaba/fastjson/

[test java demo](https://github.com/edidada/testfastjson)	

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
————————————————
版权声明：本文为CSDN博主「Java后端何哥」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/CSDN2497242041/article/details/102618226
