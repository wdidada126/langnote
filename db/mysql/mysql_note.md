# mysql


MySQL主键索引 层数
微信收藏


MySQL连接池 连接数有关


XA

数据库

MySQL
命令行可以执行


show status

```

#!/bin/bash
while true
do
mysqladmin -uroot -p "密码" ext | awk 
'/Queries/{q=$4}/Threads_connected/{c=$4}/Threads_running/{r=$4}END{printf("%d %d %d\n",q,c,r)}' >> status.txt
sleep 
1
done

```

Converting HEAP to MyISAM
##### 查询结果太大时，把结果放到磁盘，严重
Create tmp table 
#创建临时表，严重
Copying to tmp table on disk  
#把内存临时表复制到磁盘，严重
locked 
#被其他查询锁住，严重
loggin slow query 
#记录慢查询
Sorting result #排序





