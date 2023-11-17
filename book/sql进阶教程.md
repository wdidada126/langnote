# sql进阶教程

https://book.douban.com/subject/27194738/

图灵程序设计丛书·数据库系列 (共66册), 这套丛书还有 《Oracle Database 12c性能优化攻略》,《深入理解Oracle 12c数据库管理（第2版）》,《Oracle Database 11g数据库管理艺术》,《Oracle PL/SQL实战》,《SQL沉思录》 等。

作者简介：
MICK
日本知名数据库工程师，就职于SI企业，致力于数据仓库和商业智能的开发。日常除了在其个人主页“关系数据库的世界”中分享数据库和SQL的相关技术信息外，还为CodeZine（http://codezine.jp）及IT技术杂志WEB+DB PRESS撰写相关技术文章。同时还是《SQL解惑（第2版）》《SQL权威指南（第4版）》日文版的译者。

译者简介：
吴炎昌
毕业于西北工业大学软件工程专业。曾供职于日本多家软件公司，从事系统开发工作。2015年回国后加入美团点评，现任系统研发工程师。爱好旅行、电影，以及品尝各种美食，有一位志趣相投的伴侣。


第1章 神奇的 SQL
1-1　CASE表达式　　2
▲ 在SQL里表达条件分支　　2
练习题　　19
1-2　自连接的用法　　21
▲ 面向集合语言SQL　　21
练习题　　35
1-3　三值逻辑和NULL　　38
▲ SQL的温柔陷阱　　38
1-4　HAVING子句的力量　　55
▲ 出彩的配角　　55
练习题　　70
1-5　外连接的用法　　72
▲ SQL的弱点及其趋势和对策　　72
练习题　　92
1-6　用关联子查询比较行与行　　94
▲ 用SQL进行行与行之间的比较　　94
练习题　　110
1-7　用SQL进行集合运算　　112
▲ SQL和集合论　　112
练习题　　128
1-8　EXISTS谓词的用法　　　　130
▲ SQL中的谓词逻辑　　130
练习题　　146
1-9　用SQL处理数列　　　　149
▲ 灵活使用谓词逻辑　　149
练习题　　165
1-10　HAVING子句又回来了　　167
▲ 再也不要叫它配角了！　　167
练习题　　183
1-11　让SQL飞起来　　　　186
▲ 简单的性能优化　　186
1-12　关系数据库的世界　　　　216
▲ 确立SQL的编程风格　　201
第2章 SQL 编程方法
2-1　关系数据库的历史　　　　216
▲ 1969年——一切从这里开始　　216
2-2　为什么叫“关系”模型　　222
▲ 为什么不叫“表”模型　　222
2-3　开始于关系，结束于关系　　229
▲ 关于封闭世界的幸福　　229
2-4　地址这一巨大的怪物　　233
▲ 为什么关系数据库里没有指针　　233
2-5　GROUP BY和PARTITION BY　　238
▲ 物以“类”聚　　238
1-8　EXISTS谓词的用法
1-9　用SQL处理数列
1-10　HAVING子句又回来了
1-11　让SQL飞起来
1-12　关系数据库的世界
2-1　关系数据库的历史
2-2　为什么叫“关系”模型
2-3　开始于关系，结束于关系　　229
2-4　地址这一巨大的怪物
2-5　GROUP BY和PARTITION BY　　238
2-6　从面向过程思维向声明式思维、面向集合思维转变的7个关键点　　243
▲ 画圆　　243
2-7　SQL和递归集合　　　　250
▲ SQL和集合论之间　　250
2-8　人类的逻辑学　　　　256
▲ 浅谈逻辑学的历史　　256
2-9　消灭NULL委员会　　　　260
▲ 全世界的数据库工程师团结起来！　　260
2-10　SQL中的层级　　　　264
▲ 严格的等级社会　　266
第3章 附录
3-1　习题解答　　　　274
3-2　参考文献　　　　298
后　记　　　　302

三值逻辑和NULL

```sql
SELECT
	P1.NAME,
	MAX( P1.price ) AS price,
	COUNT( P2.NAME ) + 1 AS rank_1 
FROM
	Products P1
	LEFT OUTER JOIN Products P2 ON P1.price < P2.price 
GROUP BY
	P1.NAME 
ORDER BY
	rank_1;
```



```sql
SELECT
	* 
FROM
	Class_A A 
WHERE
	NOT EXISTS ( SELECT * FROM Class_B B WHERE A.age = NULL AND B.city = '东京' );
```


```sql
SELECT
	P1.NAME,
	P2.NAME 
FROM
	Products P1
	LEFT OUTER JOIN Products P2 ON P1.price < P2.price;
```

```sql
SELECT
	P1.NAME,
	MAX( P1.price ) AS price,
	COUNT( P2.NAME ) + 1 AS rank_1 
FROM
	Products P1
	INNER JOIN Products P2 ON P1.price < P2.price 
GROUP BY
	P1.NAME 
ORDER BY
	rank_1;
```


```sql
SELECT
	* 
FROM
	Students 
WHERE
	age = NULL 
	OR age <> NULL;
```


```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	age NOT IN ( SELECT age FROM Class_B WHERE city = '东京' );
```


```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	age NOT IN ( 22, 23, NULL );
```

```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	NOT age IN ( 22, 23, NULL );
```


```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	NOT ( ( age = 22 ) OR ( age = 23 ) OR ( age = NULL ) );
```


```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	NOT ( age = 22 ) 
	AND NOT ( age = 23 ) 
	AND NOT ( age = NULL );
```



```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	( age <> 22 ) 
	AND ( age <> 23 ) 
	AND ( age <> NULL );
```


```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	( age <> 22 ) 
	AND ( age <> 23 ) 
	AND unknown;
```


```sql
SELECT
	* 
FROM
	Class_A A 
WHERE
	NOT EXISTS ( SELECT * FROM Class_B B WHERE A.age = B.age AND B.city = '东京' );
```


```sql
SELECT
	* 
FROM
	Class_A A 
WHERE
	NOT EXISTS ( SELECT * FROM Class_B B WHERE A.age = NULL AND B.city = '东京' );
```


```sql
SELECT
	* 
FROM
	Class_A A 
WHERE
	NOT EXISTS ( SELECT * FROM Class_B B WHERE unknown AND B.city = '东京' );
```


```sql
SELECT
	* 
FROM
	Class_A A 
WHERE
	NOT EXISTS ( SELECT * FROM Class_B B WHERE FALSE 或 unknown );
```


```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	age < ALL ( SELECT age FROM Class_B WHERE city = '东京' );
```


```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	age < ALL ( 22, 23, NULL );
```


```sql
SELECT
	* 
FROM
	Class_A 
WHERE
	( age < 22 ) 
	AND ( age < 23 ) 
	AND ( age < NULL );
```


```sql
SELECT
	income,
	COUNT( * ) AS cnt 
FROM
	Graduates 
GROUP BY
	income 
HAVING
	COUNT( * ) >= ALL ( SELECT COUNT( * ) FROM Graduates 　　 GROUP BY income );
```


```sql
SELECT
	income,
	COUNT( * ) AS cnt 
FROM
	Graduates 
GROUP BY
	income 
HAVING
	COUNT( * ) >= ( SELECT MAX( cnt ) FROM ( SELECT COUNT( * ) AS cnt FROM Graduates GROUP BY income ) TMP );
```


```sql
SELECT
	AVG( DISTINCT income ) 
FROM
	(
SELECT
	T1.income 
FROM
	Graduates T1,
	Graduates T2 
GROUP BY
	T1.income --S 1 的条件 
HAVING
	SUM( CASE WHEN T2.income >= T1.income THEN 1 ELSE 0 END ) >= COUNT( * ) / 2 --S 2 的条件 
	AND SUM(
CASE
	
	WHEN T2.income <= T1
```

```sql
SELECT
	dpt 
FROM
	Students 
GROUP BY
	dpt 
HAVING
	COUNT( * ) = SUM( CASE WHEN sbmt_date IS NOT NULL THEN 1 ELSE 0 END );
```

```sql
SELECT DISTINCT
	shop 
FROM
	ShopItems 
WHERE
	item IN ( SELECT item FROM Items );
```


```sql
SELECT
	SI.shop 
FROM
	ShopItems SI,
	Items I 
WHERE
	SI.item = I.item 
GROUP BY
	SI.shop 
HAVING
	COUNT( SI.item ) = ( SELECT COUNT( item ) FROM Items );
```


```sql
SELECT
	SI.shop,
	COUNT( SI.item ),
	COUNT( I.item ) 
FROM
	ShopItems SI,
	Items I 
WHERE
	SI.item = I.item 
GROUP BY
	SI.shop;
```


```sql
SELECT
	SI.shop 
FROM
	ShopItems SI
	LEFT OUTER JOIN Items I ON SI.item = I.item 
GROUP BY
	SI.shop 
HAVING
	COUNT( SI.item ) = ( SELECT COUNT( item ) FROM Items ) 　　 -- 条件 1
	
	AND COUNT( I.item ) = ( SELECT COUNT( item ) FROM Items );-- 条件 2
```


```sql
-- 水平展开求交叉表 (1)：使用外连接
SELECT
	C0.NAME,
CASE
	
	WHEN C1.NAME IS NOT NULL THEN
	'○' ELSE NULL 
	END AS "SQL 入门",
CASE
		
		WHEN C2.NAME IS NOT NULL THEN
		'○' ELSE NULL 
	END AS "UNIX 基础",
CASE
		
		WHEN C3.NAME IS NOT NULL THEN
		'○' ELSE NULL 
	END AS "Java 中级" 
FROM
	( SELECT DISTINCT NAME FROM Courses ) C0 -- 这里的 C0 是侧栏
	LEFT OUTER JOIN ( SELECT NAME FROM Courses WHERE course = 'SQL 入门' ) C1 ON C0.NAME = C1.
	NAME LEFT OUTER JOIN ( SELECT NAME FROM Courses WHERE course = 'UNIX 基础' ) C2 ON C0.NAME = C2.
NAME LEFT OUTER JOIN ( SELECT NAME FROM Courses WHERE course = 'Java 中级' ) C3 ON C0.NAME = C3.NAME;
```


```sql
-- 水平展开 (2)：使用标量子查询
SELECT
	C0.NAME,
	( SELECT '○' FROM Courses C1 WHERE course = 'SQL 入门' AND C1.NAME = C0.NAME ) AS "SQL 入门",
	( SELECT '○' FROM Courses C2 WHERE course = 'UNIX 基础' AND C2.NAME = C0.NAME ) AS "UNIX 基础",
	( SELECT '○' FROM Courses C3 WHERE course = 'Java 中级' AND C3.NAME = C0.NAME ) AS "Java 中级" 
FROM
	( SELECT DISTINCT NAME FROM Courses ) C0;-- 这里的 C0 是表侧栏
```


```sql
-- 水平展开 (3)：嵌套使用 CASE 表达式
SELECT NAME
	,
CASE
	
	WHEN SUM( CASE WHEN course = 'SQL 入门' THEN 1 ELSE NULL END ) = 1 THEN
	'○' ELSE NULL 
		END AS "SQL 入门",
CASE
		
		WHEN SUM( CASE WHEN course = 'UNIX 基础' THEN 1 ELSE NULL END ) = 1 THEN
			'○' ELSE NULL 
		END AS "UNIX 基础",
	CASE
			
			WHEN SUM( CASE WHEN course = 'Java 中级' THEN 1 ELSE NULL END ) = 1 THEN
				'○' ELSE NULL 
			END AS "Java 中级 " 
		FROM
			Courses 
	GROUP BY
NAME;
```


```sql
-- 列数据转换成行数据 ：使用 UNION ALL
SELECT
	employee,
	child_1 AS child 
FROM
	Personnel UNION ALL
SELECT
	employee,
	child_2 AS child 
FROM
	Personnel UNION ALL
SELECT
	employee,
	child_3 AS child 
FROM
	Personnel;
```


```sql
-- 获取员工子女列表的 SQL 语句（没有孩子的员工也要输出）
SELECT
	EMP.employee,
	CHILDREN.child 
FROM
	Personnel EMP
	LEFT OUTER JOIN Children ON CHILDREN.child IN ( EMP.child_1, EMP.child_2, EMP.child_3 );
```



