# apachepoi

https://gitee.com/edidada/testapachepoi

在Java栈中，常用的是JXL（目前改名为JExcel）和Apache POI。其中jxl最后的更新时间是2012，除了老系统中能看到影子，几乎见不到踪迹了。目前基本上是POI一统天下。
https://poi.apache.org/

```xml
    <dependency>
      <groupId>org.apache.poi</groupId>
      <artifactId>poi</artifactId>
      <version>4.1.2</version>
    </dependency>
```
今天要说的EasyExcel阿里巴巴开源的Excel导出类库，是对POI的封装，实现了很多高级功能，并且留出扩展口，支持扩展定制化功能。


