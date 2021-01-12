# innodb





.frm

.ibd

记录通过.frm和.ibd文件恢复数据到本地

.frm文件：保存了每个表的元数据，包括表结构的定义等；

.ibd文件：InnoDB引擎开启了独立表空间(my.ini中配置innodb_file_per_table = 1)产生的存放该表的数据和索引的文件。



https://www.cnblogs.com/zhujunxiong/p/7631001.html



