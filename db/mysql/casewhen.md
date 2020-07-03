# SQL case when

`select  case when typeId = 1 then '博客' when typeId  = 2 then '未知' end from t_blog;`

desc t_blog;
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
| title       | varchar(200) | YES  |     | NULL    |                |
| summary     | varchar(400) | YES  |     | NULL    |                |
| releaseDate | datetime     | YES  |     | NULL    |                |
| clickHit    | int(11)      | YES  |     | NULL    |                |
| replyHit    | int(11)      | YES  |     | NULL    |                |
| content     | text         | YES  |     | NULL    |                |
| typeId      | int(11)      | YES  | MUL | NULL    |                |
| keyWord     | varchar(200) | YES  |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
9 rows in set (0.13 sec)

[SQL语句中CASE WHEN的使用实例](https://blog.csdn.net/haiross/article/details/46412581)
[SQL语句中CASE WHEN用法](https://blog.csdn.net/liuxq1986/article/details/15501239)
[SQL之CASE WHEN用法详解](https://blog.csdn.net/rongtaoup/article/details/82183743)
[SQL利用Case When Then 详细用法介绍](https://blog.csdn.net/weixin_42402688/article/details/81035175)
[sql case 函数与详细说明](https://www.cnblogs.com/xs-yqz/p/6420672.html)
[SQL case when的两种用法](https://www.cnblogs.com/shaopang/p/6903985.html)


select  case when typeId = 1 then '博客' when typeId  = 2 then '未知' end from t_blog;
select  case typeId when 1 then '博客' when 2 then '未知' end from t_blog;
select  case typeId when 1 then '博客' when 2 then 'Java' else 'unkonwn' end from t_blog;

[CASE WHEN 基本概念](https://blog.csdn.net/zhaomengszu/article/details/79816790)


