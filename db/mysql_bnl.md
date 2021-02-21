# mysql bnl

MySQL Block Nested-Loop Join(BNL)
https://www.cnblogs.com/vadim/p/7403728.html

优化器管理参数optimizer_switch

【MySQL】MySQL性能优化之Block Nested-Loop Join(BNL)
https://blog.csdn.net/u014756578/article/details/52795545


https://cloud.tencent.com/developer/article/1181402

mysql left join 导致的 Using join buffer (Block Nested Loop)
https://www.jianshu.com/p/0307b9030f34


innodb_buffer_pool_size

SET GLOBAL innodb_buffer_pool_size=1*1024*1024*1024  
参与join的表，需要在连接条件上建索引
left join 和 right join 会影响表连接的策略，具体来说，大结果集放在left join的前面，或者right join 的后面。比如在以上案例中，右表因为没有索引，可以认为是大结果集，所以应该把left join 改为 right join或者join（如果不影响逻辑的话）。最合理的当然是创建索引了。

作者：一篮小土
链接：https://www.jianshu.com/p/0307b9030f34
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。