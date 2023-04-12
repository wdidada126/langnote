# 通用源码阅读指导书：MyBatis源码详解

https://www.zhihu.com/pub/reader/120079431

按照java的包来分类阅读代码的

### Chap. 3 Mybatis运行初探



### Chap. 


### Chap. 


### Chap. 


### Chap. 


### Chap. 


### Chap. 



### Chap. 8

BaseTypeHandler (org.apache.ibatis.type)
    NClobTypeHandler (org.apache.ibatis.type)
    ClobReaderTypeHandler (org.apache.ibatis.type)
    OffsetTimeTypeHandler (org.apache.ibatis.type)
    ByteObjectArrayTypeHandler (org.apache.ibatis.type)
    DateOnlyTypeHandler (org.apache.ibatis.type)
    BlobTypeHandler (org.apache.ibatis.type)
    DateTypeHandler (org.apache.ibatis.type)
    IntegerTypeHandler (org.apache.ibatis.type)
    SqlTimeTypeHandler (org.apache.ibatis.type)
    NStringTypeHandler (org.apache.ibatis.type)
    CharacterTypeHandler (org.apache.ibatis.type)
    ArrayTypeHandler (org.apache.ibatis.type)
    StringTypeHandler (org.apache.ibatis.type)
    EnumOrdinalTypeHandler (org.apache.ibatis.type)
    BigDecimalTypeHandler (org.apache.ibatis.type)
    BooleanTypeHandler (org.apache.ibatis.type)
    SqlTimestampTypeHandler (org.apache.ibatis.type)
    BlobInputStreamTypeHandler (org.apache.ibatis.type)
    BlobByteObjectArrayTypeHandler (org.apache.ibatis.type)
    MonthTypeHandler (org.apache.ibatis.type)
    EnumTypeHandler (org.apache.ibatis.type)
    FloatTypeHandler (org.apache.ibatis.type)
    TimeOnlyTypeHandler (org.apache.ibatis.type)
    ByteTypeHandler (org.apache.ibatis.type)
    YearMonthTypeHandler (org.apache.ibatis.type)
    InstantTypeHandler (org.apache.ibatis.type)
    ObjectTypeHandler (org.apache.ibatis.type)
    ClobTypeHandler (org.apache.ibatis.type)
    DoubleTypeHandler (org.apache.ibatis.type)
    ShortTypeHandler (org.apache.ibatis.type)
    LongTypeHandler (org.apache.ibatis.type)
    LocalDateTypeHandler (org.apache.ibatis.type)
    UnknownTypeHandler (org.apache.ibatis.type)
    BigIntegerTypeHandler (org.apache.ibatis.type)
    ByteArrayTypeHandler (org.apache.ibatis.type)
    OffsetDateTimeTypeHandler (org.apache.ibatis.type)
    JapaneseDateTypeHandler (org.apache.ibatis.type)
    LocalDateTimeTypeHandler (org.apache.ibatis.type)
    ZonedDateTimeTypeHandler (org.apache.ibatis.type)
    SqlDateTypeHandler (org.apache.ibatis.type)
    YearTypeHandler (org.apache.ibatis.type)
    LocalTimeTypeHandler (org.apache.ibatis.type)




- SimpleTypeRegistry
- TypeAliasRegistry
- TypeHandlerRegistry


https://blog.csdn.net/Michelle_Zhong/article/details/129099305




### Chap. 9
org.apache.ibatis.io


DefaultVFS



### Chap. 10


### Chap. 11

MyBatis源码学习之XPathParser及XNode
https://www.cnblogs.com/beckwu/p/16112890.html

这个方法使用XPath解析XML文档，并获得解析出的对象。

evalXxx方法在evaluate方法的基础上作了一些处理，其中一个最重要的处理是将XPath解析获得的Node对象包装为XNode对象


XNode
调用XPathParser的evalBoolean()返回对象

### Chap. 12


### Chap. 13

### Chap. 


