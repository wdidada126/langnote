# 索引

数据库索引- 复合索引(多列索引)
https://www.cnblogs.com/aspirant/p/7157125.html

阿里巴巴云栖社区
https://www.jianshu.com/p/4ad7402a1e42

索引的分类？你知道哪些？
从物理存储角度:
聚簇索引和非聚簇索引
从数据结构角度:
B+树索引、hash索引、FULLTEXT索引、R-Tree索引
从逻辑角度:

主键索引：主键索引是一种特殊的唯一索引，不允许有空值

普通索引或者单列索引

多列索引（复合索引）：复合索引指多个字段上创建的索引，只有在查询条件中使用了创建索引时的第一个字段，索引才会被使用。使用复合索引时遵循最左前缀集合

唯一索引或者非唯一索引

空间索引：空间索引是对空间数据类型的字段建立的索引，MYSQL中的空间数据类型有4种，分别是GEOMETRY、POINT、LINESTRING、POLYGON。

我们平时在使用的Mysql中，使用下述语句

CREATE [UNIQUE|FULLTEXT|SPATIAL] INDEX index_name
    [USING index_type]
    ON tbl_name (index_col_name,...)

index_col_name:
    col_name [(length)] [ASC | DESC]


创建的索引，如复合索引、前缀索引、唯一索引，都是属于非聚簇索引，在有的书籍中，又将其称为辅助索引(secondary index)。

数据库引擎
innode 支持哪些类型的索引
Myisam

[MySQL-联合索引](https://www.jianshu.com/p/f65be52d5e2b)

聚集索引 clustered index
InnoDB存储引擎表是索引组织表，即按照主键的顺序存储数据。 
聚集索引（clustered index）就是按照每张表的主键构造一棵B+树，树中的叶子节点存放着表中的行记录数据，因此，也将聚集索引的叶子节点称为数据页；非叶子节点中存放着仅仅是键值和指向叶子节点的偏移量。每个叶子节点（数据页）都通过一个双向链表进行连接。 
由于实际的数据页只能按照一棵B+树进行排序，因此数据库中每张表只能有一个聚集索引。 
聚集索引能过特别快的访问针对范围值的查询。

非聚簇索引(secondary index)

联合索引又叫复合索引

a,b,c

a

a,b

a,b,c

索引的前缀生效特性

[mysql联合索引](https://www.cnblogs.com/softidea/p/5977860.html)

[MySQL 创建索引、修改索引、删除索引的命令语句](https://blog.csdn.net/CSDNones/article/details/50265295)

```mysql

alter table table_name add index index_name (column_list) ;
alter table table_name add unique (column_list) ;
alter table table_name add primary key (column_list) ;

```

unique 唯一索引 邮件列


btree/hash索引

主键索引

聚集索引

非聚集索引

create index语法

key index_name (name)

alter table删除索引/增加索引

[SQL CREATE INDEX 语句](https://www.w3school.com.cn/sql/sql_create_index.asp)
