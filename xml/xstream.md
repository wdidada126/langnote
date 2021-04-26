# xstream

github repo testxstream


XStream的序列化和反序列化主要依靠toXML函数和fromXML函数


https://blog.csdn.net/qq_38497634/article/details/83381390


https://www.cnblogs.com/qlqwjy/p/11978608.html



http://x-stream.github.io/download.html


```xml
<list>
  <cn.wdidada.testxstream.entity.Province>
    <name>sdf</name>
    <description>fdsasd</description>
  </cn.wdidada.testxstream.entity.Province>
  <cn.wdidada.testxstream.entity.Province>
    <name>东城区</name>
    <description>张三</description>
  </cn.wdidada.testxstream.entity.Province>
</list>
```

```xml
<china>
  <province name="sdf">
    <description>fdsasd</description>
    <city>
      <name>fasdfa</name>
    </city>
  </province>
  <province name="东城区">
    <description>张三</description>
  </province>
</china>
```


问题：
xstream 输出的xml有空行
谷歌
xstream 输出的xml有空行
