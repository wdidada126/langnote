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



```sql
-- 使用外连接生成嵌套式表侧栏 ：错误的 SQL 语句
SELECT
	MASTER1.age_class AS age_class,
	MASTER2.sex_cd AS sex_cd,
	DATA.pop_tohoku AS pop_tohoku,
	DATA.pop_kanto AS pop_kanto 
FROM
	(
SELECT
	age_class,
	sex_cd,
	SUM( CASE WHEN pref_name IN ( '青森', '秋田' ) THEN population ELSE NULL END ) AS pop_tohoku,
	SUM( CASE WHEN pref_name IN ( '东京', '千叶' ) THEN population ELSE NULL END ) AS pop_kanto 
FROM
	TblPop 
GROUP BY
	age_class,
	sex_cd 
	)
	DATA RIGHT OUTER JOIN TblAge MASTER1 -- 外连接1：和年龄层级主表进行外连接
	ON MASTER1.age_class = DATA.age_class
	RIGHT OUTER JOIN TblSex MASTER2 -- 外连接 2 ：和性别主表进行外连接
	ON MASTER2.sex_cd = DATA.sex_cd;
```

```sql
-- 停在第 1 个外连接处时 ：结果里包含年龄层级为 2 的数据
SELECT
	MASTER1.age_class AS age_class,
	DATA.sex_cd AS sex_cd,
	DATA.pop_tohoku AS pop_tohoku,
	DATA.pop_kanto AS pop_kanto 
FROM
	(
SELECT
	age_class,
	sex_cd,
	SUM( CASE WHEN pref_name IN ( '青森', '秋田' ) THEN population ELSE NULL END ) AS pop_tohoku,
	SUM( CASE WHEN pref_name IN ( '东京', '千叶' ) THEN population ELSE NULL END ) AS pop_kanto 
FROM
	TblPop 
GROUP BY
	age_class,
	sex_cd 
	)
	DATA RIGHT OUTER JOIN TblAge MASTER1 ON MASTER1.age_class = DATA.age_class;
```


```sql
-- 使用外连接生成嵌套式表侧栏 ：正确的 SQL 语句
SELECT MASTER
	.age_class AS age_class,
	MASTER.sex_cd AS sex_cd,
	DATA.pop_tohoku AS pop_tohoku,
	DATA.pop_kanto AS pop_kanto 
FROM
	( SELECT age_class, sex_cd FROM TblAge CROSS JOIN TblSex ) MASTER -- 使用交叉连接生成两张主表的笛卡儿积
	LEFT OUTER JOIN (
SELECT
	age_class,
	sex_cd,
	SUM( CASE WHEN pref_name IN ( '青森', '秋田' ) THEN population ELSE NULL END ) AS pop_tohoku,
	SUM( CASE WHEN pref_name IN ( '东京', '千叶' ) THEN population ELSE NULL END ) AS pop_kanto 
FROM
	TblPop 
GROUP BY
	age_class,
	sex_cd 
	) DATA ON MASTER.age_class = DATA.age_class 
	AND MASTER.sex_cd = DATA.sex_cd;
```



```sql
-- 解答 (1)：通过在连接前聚合来创建一对一的关系
SELECT
	I.item_no,
	SH.total_qty 
FROM
	Items I
	LEFT OUTER JOIN ( SELECT item_no, SUM( quantity ) AS total_qty FROM SalesHistory GROUP BY item_no ) SH ON I.item_no = SH.item_no;
```


```sql
-- 解答 (2) ：先进行一对多的连接再聚合
SELECT
	I.item_no,
	SUM( SH.quantity ) AS total_qty 
FROM
	Items I
	LEFT OUTER JOIN SalesHistory SH ON I.item_no = SH.item_no 一对多的连接 
GROUP BY
	I.item_no;
```

```sql
-- 全外连接保留全部信息
SELECT COALESCE
	( A.id, B.id ) AS id,
	A.NAME AS A_name,
	B.NAME AS B_name 
FROM
	Class_A A
	FULL OUTER JOIN Class_B B ON A.id = B.id;
```


```sql
-- 数据库不支持全外连接时的替代方案
SELECT
	A.id AS id,
	A.NAME,
	B.NAME 
FROM
	Class_A A
	LEFT OUTER JOIN Class_B B ON A.id = B.id UNION
SELECT
	B.id AS id,
	A.NAME,
	B.NAME 
FROM
	Class_A A
	RIGHT OUTER JOIN Class_B B ON A.id = B.id;
```


```sql
SELECT
	A.id AS id,
	A.NAME AS A_name 
FROM
	Class_A A
	LEFT OUTER JOIN Class_B B ON A.id = B.id 
WHERE
	B.NAME IS NULL;
```


```sql
SELECT
	B.id AS id,
	B.NAME AS B_name 
FROM
	Class_A A
	RIGHT OUTER JOIN Class_B B ON A.id = B.id 
WHERE
	A.NAME IS NULL;
```


```sql
SELECT COALESCE
	( A.id, B.id ) AS id,
	COALESCE ( A.NAME, B.NAME ) AS NAME 
FROM
	Class_A A
	FULL OUTER JOIN Class_B B ON A.id = B.id 
WHERE
	A.NAME IS NULL 
	OR B.NAME IS NULL;
```


```sql
-- 用外连接进行关系除法运算 ：差集的应用
SELECT DISTINCT
	shop 
FROM
	ShopItems SI1 
WHERE
	NOT EXISTS (
SELECT
	I.item 
FROM
	Items I
	LEFT OUTER JOIN ShopItems SI2 ON I.item = SI2.item 
	AND SI1.shop = SI2.shop 
WHERE
	SI2.item IS NULL 
	);
```


```sql
-- 求与上一年营业额一样的年份 (2)：使用自连接
SELECT
	S1.YEAR,
	S1.sale 
FROM
	Sales S1,
	Sales S2 
WHERE
	S2.sale = S1.sale 
	AND S2.YEAR = S1.YEAR - 1 
ORDER BY
	YEAR;
```


```sql
-- 求出是增长了还是减少了，抑或是维持现状 (1)：使用关联子查询
SELECT
	S1.YEAR,
	S1.sale,
CASE
	
	WHEN sale = ( SELECT sale FROM Sales S2 WHERE S2.YEAR = S1.YEAR - 1 ) THEN
	'→' -- 持平
	
	WHEN sale > ( SELECT sale FROM Sales S2 WHERE S2.YEAR = S1.YEAR - 1 ) THEN
	'↑' -- 增长
	
	WHEN sale < ( SELECT sale FROM Sales S2 WHERE S2.YEAR = S1.YEAR - 1 ) THEN
	'↓' -- 减少
	ELSE '—' 
	END AS var 
FROM
	Sales S1 
ORDER BY
YEAR;
```


```sql

-- 求出是增长了还是减少了，抑或是维持现状 (2)：使用自连接查询（最早的年份不会出现在结果里）
SELECT
	S1.YEAR,
	S1.sale,
CASE
	
	WHEN S1.sale = S2.sale THEN
	'→' 
	WHEN S1.sale > S2.sale THEN
	'↑' 
	WHEN S1.sale < S2.sale THEN
	'↓' ELSE '—' 
	END AS var 
FROM
	Sales S1,
	Sales S2 
WHERE
	S2.YEAR = S1.YEAR - 1 
ORDER BY
YEAR;
```



```sql
-- 查询与过去最临近的年份营业额相同的年份
SELECT YEAR
	,
	sale 
FROM
	Sales2 S1 
WHERE
	sale = (
SELECT
	sale 
FROM
	Sales2 S2 
WHERE
	S2.YEAR = ( SELECT MAX( YEAR ) -- 条件 2 ：在满足条件 1 的年份中，年份最早的一个
	FROM Sales2 S3 WHERE S1.YEAR > S3.YEAR ) 
	) -- 条件１ ：与该年份相比是过去的年份
	
ORDER BY
	YEAR;
```



```sql
SELECT
	S1.YEAR AS YEAR,
	S1.YEAR AS YEAR 
FROM
	Sales2 S1,
	Sales2 S2 
WHERE
	S1.sale = S2.sale 
	AND S2.YEAR = ( SELECT MAX( YEAR ) FROM Sales2 S3 WHERE S1.YEAR > S3.YEAR ) 
ORDER BY
	YEAR;
```


```sql
-- 求每一年与过去最临近的年份之间的营业额之差 (1)：结果里不包含最早的年份
SELECT
	S2.YEAR AS pre_year,
	S1.YEAR AS now_year,
	S2.sale AS pre_sale,
	S1.sale AS now_sale,
	S1.sale - S2.sale AS diff 
FROM
	Sales2 S1,
	Sales2 S2 
WHERE
	S2.YEAR = ( SELECT MAX( YEAR ) FROM Sales2 S3 WHERE S1.YEAR > S3.YEAR ) 
ORDER BY
	now_year;
```


```sql
-- 求每一年与过去最临近的年份之间的营业额之差 (2)：使用自外连接。结果里包含最早的年份
SELECT
	S2.YEAR AS pre_year,
	S1.YEAR AS now_year,
	S2.sale AS pre_sale,
	S1.sale AS now_sale,
	S1.sale - S2.sale AS diff 
FROM
	Sales2 S1
	LEFT OUTER JOIN Sales2 S2 ON S2.YEAR = ( SELECT MAX( YEAR ) FROM Sales2 S3 WHERE S1.YEAR > S3.YEAR ) 
ORDER BY
	now_year;
```


```sql
-- 求累计值 ：使用窗口函数
SELECT
	prc_date,
	prc_amt,
	SUM( prc_amt ) OVER ( ORDER BY prc_date ) AS onhand_amt 
FROM
	Accounts;
```


```sql
-- 求累计值 ：使用冯 · 诺依曼型递归集合
SELECT
	prc_date,
	A1.prc_amt,
	( SELECT SUM( prc_amt ) FROM Accounts A2 WHERE A1.prc_date >= A2.prc_date ) AS onhand_amt 
FROM
	Accounts A1 
ORDER BY
	prc_date;
```


```sql
-- 求移动累计值 (1)：使用窗口函数
SELECT
	prc_date,
	prc_amt,
	SUM( prc_amt ) OVER ( ORDER BY prc_date ROWS 2 PRECEDING ) AS onhand_amt 
FROM
	Accounts;
```


```sql
-- 求移动累计值 (2)：不满 3 行的时间区间也输出
SELECT
	prc_date,
	A1.prc_amt,
	(
SELECT
	SUM( prc_amt ) 
FROM
	Accounts A2 
WHERE
	A1.prc_date >= A2.prc_date 
	AND ( SELECT COUNT( * ) FROM Accounts A3 WHERE A3.prc_date BETWEEN A2.prc_date AND A1.prc_date ) <= 3 
	) AS mvg_sum 
FROM
	Accounts A1 
ORDER BY
	prc_date;
```


```sql
-- 移动累计值 (3)：不满 3 行的区间按无效处理
SELECT
	prc_date,
	A1.prc_amt,
	(
SELECT
	SUM( prc_amt ) 
FROM
	Accounts A2 
WHERE
	A1.prc_date >= A2.prc_date 
	AND ( SELECT COUNT( * ) FROM Accounts A3 WHERE A3.prc_date BETWEEN A2.prc_date AND A1.prc_date ) <= 3 
HAVING
	COUNT( * ) = 3 
	) AS mvg_sum -- 不满 3 行数据的不显示
	
FROM
	Accounts A1 
ORDER BY
	prc_date;
```



```sql
-- 去掉聚合并输出
SELECT
	A1.prc_date AS A1_date,
	A2.prc_date AS A2_date,
	A2.prc_amt AS amt 
FROM
	Accounts A1,
	Accounts A2 
WHERE
	A1.prc_date >= A2.prc_date 
	AND ( SELECT COUNT( * ) FROM Accounts A3 WHERE A3.prc_date BETWEEN A2.prc_date AND A1.prc_date ) <= 3 
ORDER BY
	A1_date,
	A2_date;
```


```sql
-- 求重叠的住宿期间
SELECT
	reserver,
	start_date,
	end_date 
FROM
	Reservations R1 
WHERE
	EXISTS (
SELECT
	* 
FROM
	Reservations R2 
WHERE
	R1.reserver <> R2.reserver -- 与自己以外的客人进行比较
	
	AND ( R1.start_date BETWEEN R2.start_date AND R2.end_date -- 条件 (1)：自己的入住日期在他人的住宿期间内
	OR R1.end_date BETWEEN R2.start_date AND R2.end_date ) 
);-- 条件 (2)：自己的离店日期在他人的住宿期间内
```


```sql
-- 升级版 ：把完全包含别人的住宿期间的情况也输出
SELECT
	reserver,
	start_date,
	end_date 
FROM
	Reservations R1 
WHERE
	EXISTS (
SELECT
	* 
FROM
	Reservations R2 
WHERE
	R1.reserver <> R2.reserver 
	AND (
	( R1.start_date BETWEEN R2.start_date AND R2.end_date OR R1.end_date BETWEEN R2.start_date AND R2.end_date ) 
	OR ( R2.start_date BETWEEN R1.start_date AND R1.end_date AND R2.end_date BETWEEN R1.start_date AND R1.end_date ) 
	) 
	);
```




