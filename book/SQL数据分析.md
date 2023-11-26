# SQL数据分析 从基础破冰到面试题解

作者: 王大伟
出版年: 2022-1
ISBN: 9787121424182

https://book.douban.com/subject/35689619/

## 个人总结的核心知识点

上一条数据

下一条数据

随书代码
42418《SQL 数据分析： 从基础破冰到面试题解》配套资料.rar

1、活跃用户分析

```sql
select a.user_id,a.login_date
from(
	select user_id,login_date
	from (
		select user_id,login_date,
			rank() over (partition by user_id order by login_date desc) as ranking
		from actice_user_analysis
	)aa
	where ranking=1
)a
inner join(
	select user_id
	from active_user_analysis
	group by user_id
	order by count(*) desc
	limit 3
)b
on a.user_id=b.user_id
order by a.user_id,login_date desc
```


2、连续登录用户分析

```sql
select b.user_id,
	min(b.`date`) as min_date,
	max(b.`date`) as max_date,
	count(1) as num
from(
	select a.user_id,a.`date`,
		date_sub(a.`date`,interval a.ranking day) as diff
	from(
		select *,
			rank() over (partition by user_id order by `date`) as ranking
		from user_login
	)a
)b
group by b.user_id,b.diff
having num>2
```


3、商品价格中位数

```sql
select a.company,
	avg(a.price) as price
from(
	select a.company,
		a.price
	from(
		select company,
			commodity_id,
			price,
			row_number() over (partition by company order by price) as ranking,
			count(1) over (partition by company) as cnt,
			count(1) over (partition by company)/2 as even_mid,
			ceil(count(1) over (partition by company)/2) as odd_mid
		from commodity_price
	)a
	where (mod(cnt,2)=0 and ranking in (even_mid,even_mid+1)) or (mod(cnt,2)=1 and ranking=odd_mid)
	order by company
)a
group by a.company
```

4、特定时间的商品价格
```sql
select t1.commodity_id,
	t1.new_price as price
from commodity_price t1
where (commodity_id,adjust_date) in 
	(select commodity_id,max(adjust_date)
	from commodity_price
	where adjust_date>='2021-03-17'
	group by commodity_id)
union all
select distinct t2.commodity_id,
	100 as price
from commodity_price t2
where (commodity_id,adjust_date) in 
	(select commodity_id,min(adjust_date)
	from commodity_price
	group by commodity_id
	having min(adjust_date)>'2021-03-17')
```

5、团队积分赛
```sql
select team_id,
	team_name,
	sum(score) as score
from(
	select team_a as team_id,
		case when score_a>score_b then 100
			when score_a=score_b then 30
			else 0 end as score
	from team_competition
	union all
	select team_b as team_id,
		case when score_b>score_a then 100
			when score_a=score_b then 30
			else 0 end as score
	from team_competition
)a
inner join team t
on t.team_id=a.team_id
group by team_id,team_name
order by score desc,team_id
```

6、小程序体验分析
```sql
select applet,
	avg(new_ranking) as avg_ranking
from(
	select user_id,
		applet,
		visit_time,
		rank() over (partition by user_id order by visit_time) as new_ranking
	from(
		select user_id,
			applet,
			visit_time,
			rank() over (partition by user_id,applet order by visit_time) as ranking
		from applet_use
	)a 
	where ranking=1
)b
group by applet
```

7、用户购买渠道分析
```sql
select t1.purchase_date,
	t1.channel,
	t2.sum_amount,
	t2.total_users
from(
	select distinct a.purchase_date,b.channel
	from purchase_channel a,
	(
		select 'app' as channel
		union
		select 'web' as channel
		union
		select 'both' as channel)b
)t1
left join(
	select purchase_date,
		channel,
		sum(sum_amount) as sum_amount,
		sum(total_users) as total_users
	from(
		select purchase_date,
			min(channel) as channel,
			sum(purchase_amount) as sum_amount,
			count(distinct user_id) as total_users
		from purchase_channel
		group by purchase_date
		having count(distinct channel)=1
		union
		select purchase_date,
			'both' as channel,
			sum(purchase_amount) as sum_amount,
			count(distinct user_id) as total_users
		from purchase_channel
		group by purchase_date
		having count(distinct channel)>1
	)c
	group by purchase_date,channel
)t2
on t1.purchase_date=t2.purchase_date and t1.channel=t2.channel
```

8、游戏关卡分析
```sql
select count(*) as num
from(
	select a.user_id,
		count(distinct a.min_game_date) as num
	from(
		select user_id,
			level_id,
			game_date,
			min(game_date) over (partition by user_id,level_id) as min_game_date
		from game_level
		where game_date between '2021-03-01' and '2021-03-03'
	)a
	where a.game_date=a.min_game_date
	group by a.user_id
	having num=3
)b
```

9、直播中最大在线观众数量
```sql
select max(current_num) as max_num
from(
	select change_time,
		sum(change_num) over (order by change_time) as current_num
	from(
		select user_id,
			enter_time as change_time,
			1 as change_num
		from watch_live
		union all
		select user_id,
			quit_time as change_time,
			-1 as change_num
		from watch_live
	)a
)b
```

第 1 部分SQL数据分析基础与进阶
第1章 数据分析与SQL 2
1.1 数据库与SQL 2
1.2 数据分析与数据分析人员的日常工作2
1.3 数据分析工作的技能要求4
1.4 数据分析笔试/面试的SQL考点6
1.5 SQL环境搭建7
1.6 本章小结 18
第2章 破冰SELECT基础检索19
2.1 检索所需的列19
2.2 * 符号初体验21
2.3 独特的DISTINCT 21
2.4 使用ORDER BY排序检索结果23
2.5 使用LIMIT限制返回行数24
2.6 ORDER BY与LIMIT结合的妙用25
2.7 本章小结27
第3章 过滤数据，选你所想28
3.1 使用 WHERE 过滤数据28
3.2 BETWEEN 过滤的易错点31
3.3 NULL过滤的易错点33
3.4 使用IN与NOT IN过滤35
3.5 使用LIKE与通配符过滤37
3.6 复杂但精确的正则表达式39
3.7 本章小结40
第4章 计算字段真奇妙41
4.1 拼接字段的妙用 41
4.2 方便使用的别名 43
4.3 算数计算生成所需新字段44
4.4 本章小结 45
第5章 高效的数据处理函数 46
5.1 文本处理函数 46
5.2 日期/时间处理函数48
5.3 数值处理函数 50
5.4 本章小结 51
第6章 常用的聚合函数52
6.1 使用聚合函数的注意点52
6.2 DISTINCT和聚合函数的搭配55
6.3 本章小结56
第7章 分组的意义57
7.1 使用GROUP BY创建分组 57
7.2 GROUP BY的易错点 58
7.3 使用HAVING过滤分组59
7.4 分组排序的意义60
7.5 SELECT语句的执行顺序 60
7.6 本章小结 61
第8章 子查询没想象中的那么难 62
8.1 何时使用子查询62
8.2 EXISTS与NOT EXISTS 64
8.3 子查询的易错点67
8.4 如何写出子查询语句68
8.5 本章小结 68
第9章 多表连接实现复杂查询69
9.1 为什么使用多表连接查询69
9.2 多种类型的多表连接 70
9.3 多表连接的易错点74
9.4 本章小结75
第10章 组合查询的妙用76
10.1 何时使用组合查询76
10.2 UNION与UNION ALL 77
10.3 组合查询的易错点79
10.4 本章小结81
第11章 CASE WHEN真的很好用82
11.1 CASE WHEN的几种形式 82
11.2 何时使用CASE WHEN 85
11.3 巧妙使用CASE WHEN实现查询85
11.4 CASE WHEN的易错点87
11.5 本章小结88
第12章 强大的窗口函数89
12.1 什么是窗口函数89
12.2 常用的窗口函数89
12.3 其他窗口函数95
12.4 本章小结 99
第13章 除查询外的常用数据库操作100
13.1 创建表 100
13.2 修改表101
13.3 删除表101
13.4 本章小结102
第2部分 SQL题目与参考解析
第14章 22个简单的SQL题目 104
第15章 17个中等难度的SQL题目151
第16章 9个高难度的SQL题目 198



## 第 1 部分SQL数据分析基础与进阶
### 第1章 数据分析与SQL 2
1.1 数据库与SQL 2
1.2 数据分析与数据分析人员的日常工作2
1.3 数据分析工作的技能要求4
1.4 数据分析笔试/面试的SQL考点6

重点考察查

1.5 SQL环境搭建7
本书使用mysql，版本8.0.25

1.6 本章小结 18
### 第2章 破冰SELECT基础检索19
2.1 检索所需的列19
2.2 * 符号初体验21
2.3 独特的DISTINCT 21
2.4 使用ORDER BY排序检索结果23
2.5 使用LIMIT限制返回行数24
2.6 ORDER BY与LIMIT结合的妙用25
2.7 本章小结27
### 第3章 过滤数据，选你所想28
3.1 使用 WHERE 过滤数据28
3.2 BETWEEN 过滤的易错点31
3.3 NULL过滤的易错点33
3.4 使用IN与NOT IN过滤35
3.5 使用LIKE与通配符过滤37
3.6 复杂但精确的正则表达式39
3.7 本章小结40
### 第4章 计算字段真奇妙41
4.1 拼接字段的妙用 41
4.2 方便使用的别名 43
4.3 算数计算生成所需新字段44
4.4 本章小结 45
### 第5章 高效的数据处理函数 46
5.1 文本处理函数 46
5.2 日期/时间处理函数48
5.3 数值处理函数 50
5.4 本章小结 51
### 第6章 常用的聚合函数52
6.1 使用聚合函数的注意点52
6.2 DISTINCT和聚合函数的搭配55
6.3 本章小结56
### 第7章 分组的意义57
7.1 使用GROUP BY创建分组 57
7.2 GROUP BY的易错点 58
7.3 使用HAVING过滤分组59
7.4 分组排序的意义60
7.5 SELECT语句的执行顺序 60
7.6 本章小结 61
### 第8章 子查询没想象中的那么难 62
8.1 何时使用子查询62
8.2 EXISTS与NOT EXISTS 64
8.3 子查询的易错点67
8.4 如何写出子查询语句68
8.5 本章小结 68
### 第9章 多表连接实现复杂查询69
9.1 为什么使用多表连接查询69
9.2 多种类型的多表连接 70
9.3 多表连接的易错点74
9.4 本章小结75
### 第10章 组合查询的妙用76
10.1 何时使用组合查询76
10.2 UNION与UNION ALL 77
10.3 组合查询的易错点79
10.4 本章小结81
### 第11章 CASE WHEN真的很好用82
11.1 CASE WHEN的几种形式 82
11.2 何时使用CASE WHEN 85
11.3 巧妙使用CASE WHEN实现查询85
11.4 CASE WHEN的易错点87
11.5 本章小结88
### 第12章 强大的窗口函数89
12.1 什么是窗口函数89
12.2 常用的窗口函数89
12.3 其他窗口函数95
12.4 本章小结 99
### 第13章 除查询外的常用数据库操作100
13.1 创建表 100
13.2 修改表101
13.3 删除表101
13.4 本章小结102
## 第2部分 SQL题目与参考解析
### 第14章 22个简单的SQL题目 104
### 第15章 17个中等难度的SQL题目151

用户上一次退出app时间，下一次登录时间平均时间间隔

MySQL中的LEAD()函数是窗口函数，用于访问当前行之后的一行或若干行的值。它可以用于获取当前行的下一个行的值，而当前行并不一定是按顺序中的最后一行。

LEAD()函数的语法为LEAD(expression, offset, default)，其中expression是要获取的列名或任何内置函数，offset是当前行之后要获取的行数，default是可选的默认值，当未找到指定行时返回该值。

例如，以下查询将返回每个销售订单（sales_order）的下一个订单的订单号（order_num）：

```sql
SELECT order_num, LEAD(order_num) OVER (PARTITION BY sales_order ORDER BY order_date) AS next_order_num  
FROM orders;
```
在这个查询中，LEAD()函数通过PARTITION BY和ORDER BY子句指定了窗口，即每个销售订单（sales_order）按订单日期排序的订单行。LEAD()函数返回下一行的订单号作为“下一订单号（next_order_num）”。如果没有下一个订单，则返回NULL。

总之，MySQL中的LEAD()函数是一种用于获取当前行之后的一行或多行的值的窗口函数，它在分区或窗口内对每一行执行操作或计算，并返回类似聚合函数的结果，但每一行都保持唯一标识。

### 第16章 9个高难度的SQL题目 198
