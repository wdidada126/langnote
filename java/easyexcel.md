# easyexcel
在Java栈中，常用的是JXL（目前改名为JExcel）和Apache POI。其中jxl最后的更新时间是2012，除了老系统中能看到影子，几乎见不到踪迹了。目前基本上是POI一统天下。

```xml
    <dependency>
      <groupId>org.apache.poi</groupId>
      <artifactId>poi</artifactId>
      <version>4.1.2</version>
    </dependency>
```
今天要说的EasyExcel阿里巴巴开源的Excel导出类库，是对POI的封装，实现了很多高级功能，并且留出扩展口，支持扩展定制化功能。


https://github.com/alibaba/easyexcel


https://easyexcel.opensource.alibaba.com/

https://gitee.com/edidada/easyexceltest

excel文件空格 12后面跟空格，直接trim了，现在需要取消trim
https://easyexcel.opensource.alibaba.com/docs/current/api/

现在版本中，autotrim开启时，去除的只有半角空格。如果是其他空白字符（比如全角空格、office换行空格等），默认是不会去除的，如果在导入的为数字类型下会直接报错，让用户一个个手动去除的话，大数据量下几乎没法完成。如果社区需要这个功能，我很高兴提供PR

姬朋飞（玉霄)、庄家钜

## 版本 version
v3.3.3
v3.3.2
v3.3.1
v3.3.0
v3.2.1
v3.2.0
v3.1.5
v3.1.4
v2.0.3
v2.0.1
v2.0.0
v2.0.0-beta6
v2.0.0-beta4
v2.0.0-beta3
v2.0.0-beta2
v2.0.0-beta1
v1.1
2.2.0-beta2
2.2.0-beta1
2.1.2
