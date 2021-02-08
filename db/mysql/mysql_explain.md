# mysql explain

explain format=json 

expain出来的信息有10列，分别是id、select_type、table、type、possible_keys、key、key_len、ref、rows、Extra

概要描述：
id:选择标识符
select_type:表示查询的类型。
table:输出结果集的表
partitions:匹配的分区
type:表示表的连接类型
possible_keys:表示查询时，可能使用的索引
key:表示实际使用的索引
key_len:索引字段的长度
ref:列与索引的比较
rows:扫描出的行数(估算的行数)
filtered:按表条件过滤的行百分比
Extra:执行情况的描述和说明



select_type
表示查询中每个select子句的类型
(1) SIMPLE(简单SELECT，不使用UNION或子查询等)
(2) PRIMARY(子查询中最外层查询，查询中若包含任何复杂的子部分，最外层的select被标记为PRIMARY)
(3) UNION(UNION中的第二个或后面的SELECT语句)
(4) DEPENDENT UNION(UNION中的第二个或后面的SELECT语句，取决于外面的查询)
(5) UNION RESULT(UNION的结果，union语句中第二个select开始后面所有select)
(6) SUBQUERY(子查询中的第一个SELECT，结果不依赖于外部查询)
(7) DEPENDENT SUBQUERY(子查询中的第一个SELECT，依赖于外部查询)
(8) DERIVED(派生表的SELECT, FROM子句的子查询)
(9) UNCACHEABLE SUBQUERY(一个子查询的结果不能被缓存，必须重新评估外链接的第一行)


## EXPLAIN信息解读

* [EXPLAIN语法](https://dev.mysql.com/doc/refman/5.7/en/explain.html)
* [EXPLAIN输出信息](https://dev.mysql.com/doc/refman/5.7/en/explain-output.html)

### SELECT转换

指定了线上环境时SOAR会到线上环境进行EXPLAIN，然后对线上执行EXPLAIN的结果进行分析。由于低版本的MySQL不支持对INSERT， UPDATE， DELETE， REPLACE进行分析，SOAR会自动将这些类型的查询请求转换为SELECT请求再执行EXPLAIN信息。

另外当线上环境设置了read\_only或super\_readonly时即使是高版本的MySQL也无法对更新请求执行EXPLAIN。需要进行SELECT转换。

### 文本格式

SOAR也支持用户直接拷贝粘贴已有的EXPLAIN文本信息，格式可以是传统格式，\G输出的Verical格式，也可以是JSON格式。

JSON格式的EXPLAIN包含的内容很丰富，但不便于人查看，信息解读的时候会将JSON和Vertical格式统一转换成传统格式。Golang处理JSON格式需要提前定义结构体，这里不得不向[gojson](https://github.com/ChimeraCoder/gojson)献出膝盖，要是没有这个工具也许我们暂时会放弃对JSON格式的支持。

### Filtered

表示此查询条件所过滤的数据的百分比。低版本的MySQL EXPLAIN信息不包含Filtered字段，SOAR会按 `filtered = rows/total_rows` 计算补充。

5.7之前的版本Filtered计算可能出现大于100%的[BUG](https://bugs.mysql.com/bug.php?id=34124)，为了不对用户产生困扰，soar会将大于100%的Filered化整为100%。

### Scalability

Scalability表示单表查询的运算复杂度，是参考[explain-analyzer](https://github.com/Preetam/explain-analyzer)项目添加的。Scalability是对access\_type的映射表，由于是单表查询，所以最大复杂度为O(n)。

| Access Type      | Scalability |
| ---              | ---         |
| ALL              | O(n)        |
| index            | O(n)        |
| range            | O(log n)+   |
| index\_subquery  | O(log n)+   |
| unique\_subquery | O(log n)+   |
| index\_merge     | O(log n)+   |
| ref\_or\_null    | O(log n)+   |
| fulltext         | O(log n)+   |
| ref              | O(log n)    |
| eq\_ref          | O(log n)    |
| const            | O(1)        |
| system           | O(1)        |


