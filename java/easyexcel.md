# easyexcel
全角字符和半角字符在使用和存储上有明显的区别。首先，他们的形状不同。在全角状态下，字母或字符占用的空间相当于两个半角字符。相反，半角状态下的字母或字符只占用一个空间。例如，中文的全角标点符号比英文的半角标点符号更宽。
其次，全角和半角字符的使用场景也有所不同。在中文输入法中，全角字符通常用于中文字符、日文字符、全角标点符号等，而半角字符则用于英文字符、数字、半角标点符号等。
此外，当我们在使用某些输入法时，切换全角和半角非常方便。例如，在搜狗输入法中，只需要右击搜狗图标，会出现一个月牙形的图标，点击图标就能在全角和半角之间切换。

在Excel中，全角空格和半角空格的区别主要体现在显示和运算两个方面。如果只是用来记录数据，也就是不参与运算，两者没有太大区别，只是全角空格显得比半角空格要大一些。然而，在进行公式运算时，Excel默认只识别半角的符号，如果公式中输入了全角的符号，可能会导致计算错误。
此外，全角空格和半角空格在ASCII码上也有不同，普通空格键的ASCII码是32，而全角空格的ASCII码则是12288。
如果要在Excel工作表中批量删除全角和半角空格，可以使用SUBSTITUTE函数。这个函数可以将目标文本中的某个字符或字符串替换为其他字符或字符串，从而帮助我们一次性去除所有的全半角空格。

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


## source code
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


设计思路
氛围read
write
这两块是独立的

metadata
属性，excel的属性
不同excel文件的格式
csv
xls
xlsx

03版本
07版本

## com.alibaba.excel
EasyExcel
EasyExcelFactory
ExcelReader
ExcelWriter

### com.alibaba.excel.analysis
接口
ExcelAnalyser
ExcelReadExecutor
类
ExcelAnalyserImpl

#### com.alibaba.excel.analysis.csv
类
CsvExcelReadExecutor

#### com.alibaba.excel.analysis.v03

接口
IgnorableXlsRecordHandler
XlsRecordHandler
类
XlsListSheetListener
XlsSaxAnalyser

##### com.alibaba.excel.analysis.v03.handlers

类
AbstractXlsRecordHandler
BlankRecordHandler
BofRecordHandler
BoolErrRecordHandler
BoundSheetRecordHandler
DummyRecordHandler
EofRecordHandler
FormulaRecordHandler
HyperlinkRecordHandler
IndexRecordHandler
LabelRecordHandler
LabelSstRecordHandler
MergeCellsRecordHandler
NoteRecordHandler
NumberRecordHandler
ObjRecordHandler
RkRecordHandler
SstRecordHandler
StringRecordHandler
TextObjectRecordHandler

#### com.alibaba.excel.analysis.v07
类
XlsxSaxAnalyser

##### com.alibaba.excel.analysis.v07.handlers
接口
XlsxTagHandler
类
AbstractCellValueTagHandler
AbstractXlsxTagHandler
CellFormulaTagHandler
CellInlineStringValueTagHandler
CellTagHandler
CellValueTagHandler
CountTagHandler
HyperlinkTagHandler
MergeCellTagHandler
RowTagHandler

###### com.alibaba.excel.analysis.v07.handlers.sax
类
SharedStringsTableHandler
XlsxRowHandler

### com.alibaba.excel.annotation
注释类型
ExcelIgnore
ExcelIgnoreUnannotated
ExcelProperty

#### com.alibaba.excel.annotation.format
注释类型
DateTimeFormat
NumberFormat

#### com.alibaba.excel.annotation.write.style
注释类型
ColumnWidth
ContentFontStyle
ContentLoopMerge
ContentRowHeight
ContentStyle
HeadFontStyle
HeadRowHeight
HeadStyle
OnceAbsoluteMerge

### com.alibaba.excel.cache
接口
ReadCache
类
Ehcache
MapCache
XlsCache

#### com.alibaba.excel.cache.selector
接口
ReadCacheSelector
类
EternalReadCacheSelector
SimpleReadCacheSelector

### com.alibaba.excel.constant
类
BuiltinFormats
ExcelXmlConstants
OrderConstant

### com.alibaba.excel.context
接口
AnalysisContext
WriteContext
类
AnalysisContextImpl
WriteContextImpl

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



#### com.alibaba.excel.context.csv

接口
CsvReadContext
类
DefaultCsvReadContext

#### com.alibaba.excel.context.xls

接口
XlsReadContext
类
DefaultXlsReadContext

#### com.alibaba.excel.context.xlsx

接口
XlsxReadContext
类
DefaultXlsxReadContext


### com.alibaba.excel.converters

接口
Converter
NullableObjectConverter
类
AutoConverter
ConverterKeyBuild
DefaultConverterLoader
ReadConverterContext
WriteConverterContext

#### com.alibaba.excel.converters.bigdecimal
类
BigDecimalBooleanConverter
BigDecimalNumberConverter
BigDecimalStringConverter

#### com.alibaba.excel.converters.biginteger
类
BigIntegerBooleanConverter
BigIntegerNumberConverter
BigIntegerStringConverter

#### com.alibaba.excel.converters.booleanconverter
类
BooleanBooleanConverter
BooleanNumberConverter
BooleanStringConverter

#### com.alibaba.excel.converters.bytearray
类
BoxingByteArrayImageConverter
ByteArrayImageConverter

#### com.alibaba.excel.converters.byteconverter
类
ByteBooleanConverter
ByteNumberConverter
ByteStringConverter

#### com.alibaba.excel.converters.date
类
DateDateConverter
DateNumberConverter
DateStringConverter

#### com.alibaba.excel.converters.doubleconverter

类
DoubleBooleanConverter
DoubleNumberConverter
DoubleStringConverter

#### com.alibaba.excel.converters.file

类
FileImageConverter

#### com.alibaba.excel.converters.floatconverter
类
FloatBooleanConverter
FloatNumberConverter
FloatStringConverter

#### com.alibaba.excel.converters.inputstream
类
InputStreamImageConverter

#### com.alibaba.excel.converters.integer

类
IntegerBooleanConverter
IntegerNumberConverter
IntegerStringConverter	 

#### com.alibaba.excel.converters.localdatetime
类
LocalDateNumberConverter
LocalDateTimeDateConverter
LocalDateTimeStringConverter

#### com.alibaba.excel.converters.longconverter
类
LongBooleanConverter
LongNumberConverter
LongStringConverter

#### com.alibaba.excel.converters.shortconverter

类
ShortBooleanConverter
ShortNumberConverter
ShortStringConverter

#### com.alibaba.excel.converters.string
类
StringBooleanConverter
StringErrorConverter
StringImageConverter
StringNumberConverter
StringStringConverter

#### com.alibaba.excel.converters.url
类
UrlImageConverter

### com.alibaba.excel.enums	

枚举
BooleanEnum
CellDataTypeEnum
CellExtraTypeEnum
HeadKindEnum
HolderEnum
NumericCellTypeEnum
RowTypeEnum
WriteDirectionEnum
WriteLastRowTypeEnum
WriteTemplateAnalysisCellTypeEnum
WriteTypeEnum

CellDataTypeEnum

#### com.alibaba.excel.enums.poi	 
枚举
BorderStyleEnum
FillPatternTypeEnum
HorizontalAlignmentEnum
VerticalAlignmentEnum
### com.alibaba.excel.event

接口
Handler
Listener
NotRepeatExecutor
Order
类
AbstractIgnoreExceptionReadListener
AnalysisEventListener
SyncReadListener


### com.alibaba.excel.exception

异常错误
ExcelAnalysisException
ExcelAnalysisStopException
ExcelCommonException
ExcelDataConvertException
ExcelGenerateException

### com.alibaba.excel.metadata
接口
Cell
ConfigurationHolder
Holder
类
AbstractCell
AbstractHolder
AbstractParameterBuilder
BasicParameter
CellExtra
CellRange
Font
GlobalConfiguration
Head
NullObject

#### com.alibaba.excel.metadata.csv
类
CsvCell
CsvCellStyle
CsvDataFormat
CsvRichTextString
CsvRow
CsvSheet
CsvWorkbook

#### com.alibaba.excel.metadata.data
类
CellData
ClientAnchorData
CommentData
CoordinateData
DataFormatData
FormulaData
HyperlinkData
ImageData
ReadCellData
RichTextStringData
RichTextStringData.IntervalFont
WriteCellData
枚举
ClientAnchorData.AnchorType
HyperlinkData.HyperlinkType
ImageData.ImageType
 
#### com.alibaba.excel.metadata.format
类
DataFormatter
ExcelGeneralNumberFormat

#### com.alibaba.excel.metadata.property

类
ColumnWidthProperty
DateTimeFormatProperty
ExcelContentProperty
ExcelHeadProperty
FontProperty
LoopMergeProperty
NumberFormatProperty
OnceAbsoluteMergeProperty
RowHeightProperty
StyleProperty

### com.alibaba.excel.read.builder
类
AbstractExcelReaderParameterBuilder
ExcelReaderBuilder
ExcelReaderSheetBuilder

### com.alibaba.excel.read.listener
接口
ReadListener
类
ModelBuildEventListener
PageReadListener

### com.alibaba.excel.read.metadata

类
ReadBasicParameter
ReadSheet
ReadWorkbook

#### com.alibaba.excel.read.metadata.holder

接口
ReadHolder
类
AbstractReadHolder
ReadRowHolder
ReadSheetHolder
ReadWorkbookHolder


##### com.alibaba.excel.read.metadata.holder.csv
类
CsvReadSheetHolder
CsvReadWorkbookHolder

##### com.alibaba.excel.read.metadata.holder.xls
类
XlsReadSheetHolder
XlsReadWorkbookHolder

##### com.alibaba.excel.read.metadata.holder.xlsx
类
XlsxReadSheetHolder
XlsxReadWorkbookHolder

#### com.alibaba.excel.read.metadata.property
类
ExcelReadHeadProperty

### com.alibaba.excel.read.processor	 
接口
AnalysisEventProcessor
类
DefaultAnalysisEventProcessor

### com.alibaba.excel.support

枚举
ExcelTypeEnum

### com.alibaba.excel.util

类
BeanMapUtils
BeanMapUtils.EasyExcelNamingPolicy
BooleanUtils
ClassUtils
ConverterUtils
DateUtils
FieldUtils
FileTypeUtils
FileUtils
IntUtils
IoUtils
ListUtils
MapUtils
MemberUtils
NumberDataFormatterUtils
NumberUtils
PositionUtils
SheetUtils
StringUtils
StyleUtil
Validate
WorkBookUtil
WriteHandlerUtils

### com.alibaba.excel.write

接口
ExcelBuilder
类
ExcelBuilderImpl

#### com.alibaba.excel.write.builder

类
AbstractExcelWriterParameterBuilder
ExcelWriterBuilder
ExcelWriterSheetBuilder
ExcelWriterTableBuilder

#### com.alibaba.excel.write.executor

接口
ExcelWriteExecutor
类
AbstractExcelWriteExecutor
ExcelWriteAddExecutor
ExcelWriteFillExecutor

#### com.alibaba.excel.write.handler
接口
CellWriteHandler
RowWriteHandler
SheetWriteHandler
WorkbookWriteHandler
WriteHandler
类
AbstractCellWriteHandler
AbstractRowWriteHandler
AbstractSheetWriteHandler
AbstractWorkbookWriteHandler
DefaultWriteHandlerLoader

#### com.alibaba.excel.write.handler.context
类
CellWriteHandlerContext
RowWriteHandlerContext
SheetWriteHandlerContext
WorkbookWriteHandlerContext

#### com.alibaba.excel.write.handler.impl

类
DefaultRowWriteHandler
DimensionWorkbookWriteHandler
FillStyleCellWriteHandler

#### com.alibaba.excel.write.merge
类
AbstractMergeStrategy
LoopMergeStrategy
OnceAbsoluteMergeStrategy

#### com.alibaba.excel.write.metadata
接口
RowData
类
CollectionRowData
MapRowData
WriteBasicParameter
WriteSheet
WriteTable
WriteWorkbook

##### com.alibaba.excel.write.metadata.fill
类
AnalysisCell
FillConfig
FillWrapper

##### com.alibaba.excel.write.metadata.holder
接口
WriteHolder
类
AbstractWriteHolder
WriteSheetHolder
WriteTableHolder
WriteWorkbookHolder

##### com.alibaba.excel.write.metadata.style
类
WriteCellStyle
WriteFont

#### com.alibaba.excel.write.property
类
ExcelWriteHeadProperty

#### com.alibaba.excel.write.style
类
AbstractCellStyleStrategy
AbstractVerticalCellStyleStrategy
DefaultStyle
HorizontalCellStyleStrategy

##### com.alibaba.excel.write.style.column
类
AbstractColumnWidthStyleStrategy
AbstractHeadColumnWidthStyleStrategy
LongestMatchColumnWidthStyleStrategy
SimpleColumnWidthStyleStrategy

##### com.alibaba.excel.write.style.row
类
AbstractRowHeightStyleStrategy
SimpleRowHeightStyleStrategy

### org.apache.poi.hssf.usermodel	 
类
PoiUtils


## 读写excel优化思路
利用硬件新特性，api新特性
