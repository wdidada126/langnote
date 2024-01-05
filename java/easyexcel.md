# easyexcel

excel文档有两个显示数据的地方，一个是sheet页，一个是编辑栏。
easyexcel两个输入框.png

ReadCellData com.alibaba.excel.metadata.data.ReadCellData
DataFormatData(index=44, format=_("￥"* #,##0.00_);_("￥"* (#,##0.00);_("￥"* "-"??_);_(@_))


    public CellDataTypeEnum getType()
CellDataTypeEnum的枚举值
STRING
DIRECT_STRING
NUMBER
BOOLEAN
EMPTY
ERROR
DATE
RICH_TEXT_STRING

    public BigDecimal getNumberValue()  获取excel文件中

在Java栈中，常用的是JXL（目前改名为JExcel）和Apache POI。其中jxl最后的更新时间是2012，除了老系统中能看到影子，几乎见不到踪迹了。目前基本上是POI一统天下。
https://poi.apache.org/
apachepoi.md

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

## 源代码 3.0.1
https://javadoc.dev/online/api/com.alibaba/easyexcel/3.0.1/index.html

## com.alibaba.excel	 
### com.alibaba.excel.analysis	 
com.alibaba.excel.analysis.csv	 
com.alibaba.excel.analysis.v03	 
com.alibaba.excel.analysis.v03.handlers	 
com.alibaba.excel.analysis.v07	 
com.alibaba.excel.analysis.v07.handlers	 
com.alibaba.excel.analysis.v07.handlers.sax	 
### com.alibaba.excel.annotation	 
com.alibaba.excel.annotation.format	 
com.alibaba.excel.annotation.write.style	 
### com.alibaba.excel.cache	 
com.alibaba.excel.cache.selector	 
### com.alibaba.excel.constant	 
### com.alibaba.excel.context


XlsxReadContext (com.alibaba.excel.context.xlsx)
    DefaultXlsxReadContext (com.alibaba.excel.context.xlsx)
XlsReadContext (com.alibaba.excel.context.xls)
    DefaultXlsReadContext (com.alibaba.excel.context.xls)
CsvReadContext (com.alibaba.excel.context.csv)
    DefaultCsvReadContext (com.alibaba.excel.context.csv)
AnalysisContextImpl (com.alibaba.excel.context)
    DefaultCsvReadContext (com.alibaba.excel.context.csv)
    DefaultXlsxReadContext (com.alibaba.excel.context.xlsx)
    DefaultXlsReadContext (com.alibaba.excel.context.xls)



com.alibaba.excel.context.csv	 
com.alibaba.excel.context.xls	 
com.alibaba.excel.context.xlsx	 
### com.alibaba.excel.converters	 
com.alibaba.excel.converters.bigdecimal	 
com.alibaba.excel.converters.biginteger	 
com.alibaba.excel.converters.booleanconverter	 
com.alibaba.excel.converters.bytearray	 
com.alibaba.excel.converters.byteconverter	 
com.alibaba.excel.converters.date	 
com.alibaba.excel.converters.doubleconverter	 
com.alibaba.excel.converters.file	 
com.alibaba.excel.converters.floatconverter	 
com.alibaba.excel.converters.inputstream	 
com.alibaba.excel.converters.integer	 
com.alibaba.excel.converters.localdatetime	 
com.alibaba.excel.converters.longconverter	 
com.alibaba.excel.converters.shortconverter	 
com.alibaba.excel.converters.string	 
com.alibaba.excel.converters.url	 
### com.alibaba.excel.enums	

CellDataTypeEnum





com.alibaba.excel.enums.poi	 

### com.alibaba.excel.event	 
### com.alibaba.excel.exception	 
### com.alibaba.excel.metadata	 
com.alibaba.excel.metadata.csv	 
com.alibaba.excel.metadata.data	 
com.alibaba.excel.metadata.format	 
com.alibaba.excel.metadata.property	 

### com.alibaba.excel.read.builder	 
com.alibaba.excel.read.listener	 
com.alibaba.excel.read.metadata	 
com.alibaba.excel.read.metadata.holder	 
com.alibaba.excel.read.metadata.holder.csv	 
com.alibaba.excel.read.metadata.holder.xls	 
com.alibaba.excel.read.metadata.holder.xlsx	 
com.alibaba.excel.read.metadata.property	 
com.alibaba.excel.read.processor	 

### com.alibaba.excel.support	 
### com.alibaba.excel.util	 
### com.alibaba.excel.write	 
com.alibaba.excel.write.builder	 
com.alibaba.excel.write.executor	 
com.alibaba.excel.write.handler	 
com.alibaba.excel.write.handler.context	 
com.alibaba.excel.write.handler.impl	 
com.alibaba.excel.write.merge	 
com.alibaba.excel.write.metadata	 
com.alibaba.excel.write.metadata.fill	 
com.alibaba.excel.write.metadata.holder	 
com.alibaba.excel.write.metadata.style	 
com.alibaba.excel.write.property	 
com.alibaba.excel.write.style	 
com.alibaba.excel.write.style.column	 
com.alibaba.excel.write.style.row	 
### org.apache.poi.hssf.usermodel	 
