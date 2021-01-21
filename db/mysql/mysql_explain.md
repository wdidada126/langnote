# mysql explain

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



