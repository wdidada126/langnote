# SQL数据分析 从基础破冰到面试题解

作者: 王大伟
出版年: 2022-1
ISBN: 9787121424182

https://book.douban.com/subject/35689619/

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
```
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
```
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
```
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
```
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
```
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
```
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

