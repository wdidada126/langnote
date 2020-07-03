# shadow



#### 利用”影子表”实现表重建策略：

```
mysql> drop table if exists my_summary,my_summary_old;
mysql> create table my_summary_new like my_summary;
mysql> rename table my_summary to my_summary_old,my_summary_new to my_summary;
```

#### alter table 大表的”影子拷贝”技巧：

```
先创建一张和源表无关的新表，然后通过重命名和删表操作交换两张表；
```





https://cloud.tencent.com/developer/article/1068773



