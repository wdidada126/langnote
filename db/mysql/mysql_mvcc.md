# mysql mvcc

https://gitee.com/edidada/mydb

mvcc 加了三个隐藏的字段 
事务id roll指针 行id
1.DB_TRX_ID：一个6byte的标识，每处理一个事务，其值自动+1
下面提到的“创建时间”和“删除时间”记录的就是这个DB_TRX_ID的值
如insert、update、delete操作时，删除操作用1个bit表示。 
DB_TRX_ID是最重要的一个，可以通过语句“show engine innodb status”来查找 
2.DB_ROLL_PTR: 大小是7byte,指向写到rollback segment（回滚段）的一条undo log记录
（update操作的话，记录update前的ROW值）
3.DB_ROW_ID: 大小是6byte,该值随新行插入单调增加。
当由innodb自动产生聚集索引时聚集索引(即没有主键时,因为MYSQL默认聚簇表,会自动生成一个ROWID)
包括这个DB_ROW_ID的值，
不然的话聚集索引中不包括这个值,这个用于索引当中。
